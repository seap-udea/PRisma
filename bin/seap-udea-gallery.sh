#!/usr/bin/env bash
# seap-udea-gallery.sh — generate lightweight WebP previews for SEAP galleries.
#
# Run inside a repository that contains `.seap-udea-gallery.json` at its root
# (or pass the path to that JSON / the repo root).
#
# For each image under the configured `path`, writes:
#   <path>/.gallery/<stem>.webp
#
# The seap-udea.github.io gallery page uses those previews in the filmstrip and
# grid; only the main stage loads the original file.
#
# Usage:
#   ./seap-udea-gallery.sh
#   ./seap-udea-gallery.sh /path/to/repo
#   ./seap-udea-gallery.sh /path/to/.seap-udea-gallery.json
#   MAX_WIDTH=480 QUALITY=75 ./seap-udea-gallery.sh
#
# Requires: python3 + Pillow  (preferred)
# Fallback: sips + cwebp

set -euo pipefail

MAX_WIDTH="${MAX_WIDTH:-640}"
QUALITY="${QUALITY:-78}"
CONFIG_NAME=".seap-udea-gallery.json"
FORCE="${FORCE:-0}"

die() {
  echo "error: $*" >&2
  exit 1
}

log() {
  echo "▶  $*"
}

resolve_config() {
  local arg="${1:-}"
  if [[ -z "$arg" ]]; then
    if [[ -f "./$CONFIG_NAME" ]]; then
      echo "$(pwd)/$CONFIG_NAME"
      return
    fi
    die "no $CONFIG_NAME in $(pwd). Pass a repo path or config file."
  fi
  if [[ -f "$arg" && "$(basename "$arg")" == "$CONFIG_NAME" ]]; then
    echo "$(cd "$(dirname "$arg")" && pwd)/$CONFIG_NAME"
    return
  fi
  if [[ -d "$arg" ]]; then
    if [[ -f "$arg/$CONFIG_NAME" ]]; then
      echo "$(cd "$arg" && pwd)/$CONFIG_NAME"
      return
    fi
    die "no $CONFIG_NAME in directory: $arg"
  fi
  die "not a config file or directory: $arg"
}

# Prints: PATH_LINE (relative path from repo root, no trailing slash)
read_gallery_paths() {
  local config="$1"
  python3 - "$config" <<'PY'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
raw = re.sub(r",\s*([}\]])", r"\1", raw)
data = json.loads(raw)
if isinstance(data, dict):
    data = [data]
for item in data:
    path = str(item.get("path") or "").strip().lstrip("./").rstrip("/")
    if not path:
        raise SystemExit("missing required field \"path\" in gallery config")
    print(path)
PY
}

have_pillow() {
  python3 - <<'PY' >/dev/null 2>&1
from PIL import Image, ImageOps
PY
}

convert_one_pillow() {
  local src="$1" dst="$2" width="$3" quality="$4"
  python3 - "$src" "$dst" "$width" "$quality" <<'PY'
import sys
from pathlib import Path
from PIL import Image, ImageOps

src, dst, max_w, quality = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
im = Image.open(src)
im = ImageOps.exif_transpose(im)
# Flatten transparency onto white for consistent thumbs
if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
    rgba = im.convert("RGBA")
    bg = Image.new("RGB", rgba.size, (255, 255, 255))
    bg.paste(rgba, mask=rgba.split()[-1])
    im = bg
else:
    im = im.convert("RGB")

if im.width > max_w:
    h = max(1, round(im.height * (max_w / im.width)))
    im = im.resize((max_w, h), Image.Resampling.LANCZOS)

Path(dst).parent.mkdir(parents=True, exist_ok=True)
im.save(dst, "WEBP", quality=quality, method=6)
PY
}

convert_one_sips_cwebp() {
  local src="$1" dst="$2" width="$3" quality="$4"
  local tmp
  tmp="$(mktemp -t seap-gallery.XXXXXX).png"
  # sips resizes preserving aspect; -Z is max dimension
  sips -s format png --resampleHeightWidthMax "$width" "$src" --out "$tmp" >/dev/null
  cwebp -quiet -q "$quality" "$tmp" -o "$dst"
  rm -f "$tmp"
}

main() {
  local config repo_root
  config="$(resolve_config "${1:-}")"
  repo_root="$(cd "$(dirname "$config")" && pwd)"

  local converter=""
  if have_pillow; then
    converter="pillow"
  elif command -v sips >/dev/null 2>&1 && command -v cwebp >/dev/null 2>&1; then
    converter="sips+cwebp"
  else
    die "need python3+Pillow, or sips+cwebp"
  fi

  log "config:  $config"
  log "engine:  $converter  (max width=${MAX_WIDTH}px, quality=${QUALITY})"

  local -a gallery_paths=()
  local line
  while IFS= read -r line; do
    [[ -n "$line" ]] && gallery_paths+=("$line")
  done < <(read_gallery_paths "$config")

  local total_made=0 total_skipped=0 total_failed=0
  local gallery_rel gallery_dir out_dir

  for gallery_rel in "${gallery_paths[@]}"; do
    gallery_dir="$repo_root/$gallery_rel"
    out_dir="$gallery_dir/.gallery"

    log "processing gallery: $gallery_rel"
    [[ -d "$gallery_dir" ]] || die "gallery path does not exist: $gallery_dir"
    
    log "source:  $gallery_dir"
    log "output:  $out_dir"

    mkdir -p "$out_dir"

    # Ignore previews and non-images
    local -a images=()
    local f name stem dst
    while IFS= read -r -d '' f; do
      name="$(basename "$f")"
      # skip anything already under .gallery
      case "$f" in
        */.gallery/*) continue ;;
      esac
      images+=("$f")
    done < <(
      find "$gallery_dir" -maxdepth 1 -type f \
        \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' \
           -o -iname '*.gif' -o -iname '*.webp' -o -iname '*.bmp' \
           -o -iname '*.tif' -o -iname '*.tiff' \) \
        -print0 | sort -z
    )

    local total="${#images[@]}"
    if [[ "$total" -eq 0 ]]; then
      log "no images found in $gallery_dir, skipping"
      continue
    fi
    log "found $total image(s)"

    local i=0
    for f in "${images[@]}"; do
      i=$((i + 1))
      name="$(basename "$f")"
      stem="${name%.*}"
      dst="$out_dir/${stem}.webp"

      if [[ "$FORCE" != "1" && -f "$dst" && "$dst" -nt "$f" ]]; then
        total_skipped=$((total_skipped + 1))
        printf "  [%d/%d] skip  %s\n" "$i" "$total" "$name"
        continue
      fi

      printf "  [%d/%d] make  %s → .gallery/%s.webp\n" "$i" "$total" "$name" "$stem"
      if [[ "$converter" == "pillow" ]]; then
        if convert_one_pillow "$f" "$dst" "$MAX_WIDTH" "$QUALITY"; then
          total_made=$((total_made + 1))
        else
          total_failed=$((total_failed + 1))
          echo "         FAILED" >&2
        fi
      else
        if convert_one_sips_cwebp "$f" "$dst" "$MAX_WIDTH" "$QUALITY"; then
          total_made=$((total_made + 1))
        else
          total_failed=$((total_failed + 1))
          echo "         FAILED" >&2
        fi
      fi
    done

    # Optional: keep .gallery listed by GitHub / tooling
    if [[ ! -f "$out_dir/.gitkeep" ]]; then
      : >"$out_dir/.gitkeep"
    fi
  done

  log "done: made=$total_made skipped=$total_skipped failed=$total_failed"
  log "commit and push .gallery/ folders so the site can load previews."
  [[ "$total_failed" -eq 0 ]]
}

main "$@"
