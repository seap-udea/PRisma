#!/usr/bin/env python3
"""generate_figures.py — Corner / reduced-corner / PPC figures for saved runs.

Reads one or more ``.npz`` posterior files (from ``run_sweep`` / nested sampling)
and writes publication-style figures under ``<case>/results/figures/`` as::

    {CASE}_{PLANET}_{ORDKEY}-{tag}_corner.png
    {CASE}_{PLANET}_{ORDKEY}-{tag}_corner_reduced.png
    {CASE}_{PLANET}_{ORDKEY}-{tag}_ppc.png

``ORDKEY`` is a sortable key derived from ``z1`` (larger ``z1`` -> smaller key), so
alphabetical file ordering places the best PPC agreement first.

Usage
-----
From ``pipeline/``::

    python generate_figures.py kepler_51/results/exorings/kepler_51_b_NS_….npz
    python generate_figures.py kepler_51/results/exorings/*.npz

Options
-------
    --only corner|reduced|ppc   Generate a subset of figure types (repeatable).
    --dry-run                   List targets without drawing.
    --latex                     Enable full LaTeX text rendering (needs a TeX install).
"""

from __future__ import annotations

import argparse
import re
import sys
import traceback
import warnings
from pathlib import Path
import numpy as np

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Allow ``python generate_figures.py …`` from pipeline/ without an install.
_PIPELINE = Path(__file__).resolve().parent.parent
if str(_PIPELINE) not in sys.path:
    sys.path.insert(0, str(_PIPELINE))

import photoring as pr
import photoring.plotting as plot
from photoring.io import load_observables, load_run

warnings.filterwarnings("ignore")

PPC_OBSERVABLES = ["delta", "T14", "T23", "rho_obs", "b_obs"]
FIGURE_KINDS = ("corner", "reduced", "ppc")
_KIND_SUFFIX = {
    "corner": "corner",
    "reduced": "corner_reduced",
    "ppc": "ppc",
}

CATEGORY_MAPPING = {
    "[Excellent] Golden Sample": "cat1_GoldenSample",
    "[Acceptable] Low Bayesian Evidence": "cat2_LowEvidence",
    "[Acceptable] Multimodal Angles": "cat3_MultimodalAngles",
    "[Degenerate] Ringless": "cat4_Ringless",
    "[Rejected] Unphysical Nuisance": "cat5_UnphysicalNuisance",
    "[Rejected] Poor Individual Fit": "cat6_PoorIndividualFit",
    "[Rejected] Poor Fit": "cat7_PoorFit",
    "[Rejected] Missing PPC": "cat8_MissingPPC"
}


class _ResultsFiguresPaths:
    """Minimal stand-in for :class:`CasePaths` that points ``_save`` at results/figures."""

    def __init__(self, case_root: Path):
        self._base = Path(case_root) / "results" / "figures"

    def figures_dir(self, figure_type: str = "") -> Path:
        return self._base / figure_type if figure_type else self._base


def _infer_case_root(npz_path: Path) -> Path:
    """``…/<case>/results/<model>/<tag>.npz`` → ``…/<case>``."""
    p = npz_path.resolve()
    for parent in [p.parent, *p.parents]:
        if (parent / "inputs").is_dir() and (parent / "results").is_dir():
            return parent
    return p.parents[2]


def _resolve_npz_args(raw: list[str]) -> list[Path]:
    """Expand directories / globs already expanded by the shell into sorted .npz paths."""
    out: list[Path] = []
    for item in raw:
        p = Path(item)
        if p.is_dir():
            out.extend(sorted(p.glob("*.npz")))
        elif p.suffix == ".npz":
            out.append(p)
        else:
            print(f"  skip (not .npz): {p}", file=sys.stderr)
    seen, uniq = set(), []
    for p in out:
        key = str(p.resolve())
        if key not in seen:
            seen.add(key)
            uniq.append(p)
    return uniq


def _load_ttv_cache(case_paths: pr.CasePaths, cache: dict) -> dict:
    """Lazy-load empirical observables per planet."""
    def get(planet: str):
        if planet not in cache:
            f = case_paths.observables_file(planet)
            if not f.exists():
                raise FileNotFoundError(f"Observables file missing for planet {planet}: {f}")
            cache[planet] = load_observables(f)
        return cache[planet]
    return get


def _fig_name(prefix: str, tag: str, kind: str, ext: str) -> str:
    """``{CASE}_{PLANET}_{ORDKEY}-{tag}_corner.png`` (and variants)."""
    if prefix:
        return f"{prefix}-{tag}_{_KIND_SUFFIX[kind]}.{ext}"
    return f"{tag}_{_KIND_SUFFIX[kind]}.{ext}"


def generate_for_run(npz_path: Path, kinds: set[str], ttv_get,
                     score_info: dict | None = None,
                     index: int = 1, dry_run: bool = False,
                     no_prefix: bool = False, force: bool = False) -> dict:
    """Draw the requested figures for one ``.npz``. Returns a status dict."""
    npz_path = Path(npz_path)
    if not npz_path.exists():
        return {"tag": npz_path.name, "ok": False, "error": "file not found"}

    case_root = _infer_case_root(npz_path)
    case_paths = pr.CasePaths(case_root.name, pipeline_dir=_PIPELINE)
    version = plot.run_version_id([npz_path])
    ext = plot.STYLE["fig_format"]
    out_dir = npz_path.parent / "figures"

    run = load_run(npz_path)
    tag = run["tag"]
    planet = run["planet"]
    case_name = run.get("case", case_root.name)

    if not no_prefix and score_info is None:
        return {"tag": tag, "ok": False, "error": f"Run '{tag}' not found in scoring_{case_name}_{planet}.json. Run score_retrievals.py or use --no-prefix"}

    if no_prefix or score_info is None:
        prefix = ""
        z1 = float("nan")
        zkey = "ord99999-z1_nan"
    else:
        cat_str = score_info.get("category", "Unknown")
        cat_prefix = CATEGORY_MAPPING.get(cat_str, "cat9_Unknown")
        zkey = score_info.get("zkey", "ord99999-z1_nan")
        z1 = score_info.get("raw_z1", float("nan"))
        prefix = f"{case_name}_{planet}_{cat_prefix}_{zkey}"

    all_exist = True
    for k in kinds:
        out = out_dir / _fig_name(prefix, tag, k, ext)
        if not out.exists():
            all_exist = False
            break

    if all_exist and not force and not dry_run:
        return {
            "tag": tag, "planet": planet, "ok": True, "index": index,
            "z1": z1, "zkey": zkey,
            "made": [], "skipped": list(kinds), "error": None,
            "already_exist": True
        }

    if dry_run:
        preview = [_fig_name(prefix, tag, k, ext) for k in FIGURE_KINDS if k in kinds]
        return {
            "tag": tag,
            "ok": True,
            "dry_run": True,
            "case": case_root.name,
            "kinds": sorted(kinds),
            "index": index,
            "out": str(out_dir),
            "preview": preview,
            "z1": z1,
            "zkey": zkey,
        }
    status = {
        "tag": tag, "planet": planet, "ok": True, "index": index,
        "z1": z1, "zkey": zkey,
        "made": [], "skipped": [], "error": None,
    }

    try:
        out_dir.mkdir(parents=True, exist_ok=True)

        rho_true_dist = None
        if case_paths.rho_true_samples.exists():
            rho_true_dist = np.loadtxt(case_paths.rho_true_samples) / 1000.0
            
        b_obs_dist = None
        try:
            b_obs_dist = ttv_get(planet).get("b")
        except Exception:
            pass

        if "corner" in kinds:
            fig = plot.plot_results_panel_inset(run, rho_true_dist=rho_true_dist, b_obs_dist=b_obs_dist, paths=None, title=True)
            if fig is None:
                status["skipped"].append("corner")
            else:
                plot.add_run_version_label(fig, version)
                out = out_dir / _fig_name(prefix, tag, "corner", ext)
                fig.savefig(out, dpi=plot.STYLE["fig_dpi"], bbox_inches="tight")
                print(f"  Saved -> {out}")
                status["made"].append(str(out))
                plt.close(fig)

        if "reduced" in kinds:
            fig = plot.plot_results_panel_reduced_inset(run, paths=None, title=True)
            if fig is None:
                status["skipped"].append("reduced")
            else:
                plot.add_run_version_label(fig, version)
                out = out_dir / _fig_name(prefix, tag, "reduced", ext)
                fig.savefig(out, dpi=plot.STYLE["fig_dpi"], bbox_inches="tight")
                print(f"  Saved -> {out}")
                status["made"].append(str(out))
                plt.close(fig)

        if "ppc" in kinds:
            if run.get("ppc") is None:
                status["skipped"].append("ppc")
            else:
                ttv = ttv_get(planet)
                fig, _stats = plot.plot_ppc(run, ttv, obs_keys=PPC_OBSERVABLES, paths=None)
                if fig is None:
                    status["skipped"].append("ppc")
                else:
                    plot.add_run_version_label(fig, version)
                    out = out_dir / _fig_name(prefix, tag, "ppc", ext)
                    fig.savefig(out, dpi=plot.STYLE["fig_dpi"], bbox_inches="tight")
                    print(f"  Saved -> {out}")
                    status["made"].append(str(out))
                    plt.close(fig)
    except Exception as exc:
        status["ok"] = False
        status["error"] = f"{type(exc).__name__}: {exc}"
        traceback.print_exc()
        plt.close("all")

    return status


_FIG_SUFFIX_RE = re.compile(
    r"^(?:\d{3}-)?(?P<tag>.+?)_(?P<kind>corner_reduced|corner|ppc)\.(?P<ext>\w+)$"
)


def renumber_existing_figures(fig_dir: Path) -> int:
    """Assign ``001-``, ``002-``, … prefixes to existing figures, grouped by tag."""
    fig_dir = Path(fig_dir)
    if not fig_dir.is_dir():
        return 0

    by_tag: dict[str, list[Path]] = {}
    for p in fig_dir.iterdir():
        if not p.is_file():
            continue
        m = _FIG_SUFFIX_RE.match(p.name)
        if not m:
            continue
        by_tag.setdefault(m.group("tag"), []).append(p)

    n_moved = 0
    for i, tag in enumerate(sorted(by_tag), 1):
        for src in by_tag[tag]:
            m = _FIG_SUFFIX_RE.match(src.name)
            dest = fig_dir / f"{i:03d}-{tag}_{m.group('kind')}.{m.group('ext')}"
            if src.resolve() == dest.resolve():
                continue
            if dest.exists():
                dest.unlink()
            src.rename(dest)
            n_moved += 1
            print(f"  renamed -> {dest.name}")
    return n_moved


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Generate corner / reduced-corner / PPC figures for Photo-Ring runs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument(
        "npz", nargs="*",
        help="One or more .npz files (shell-expanded globs OK), or a results directory.",
    )
    ap.add_argument(
        "--only", choices=FIGURE_KINDS, action="append", default=None,
        help="Restrict to one figure kind (repeatable). Default: all three.",
    )
    ap.add_argument("--dry-run", action="store_true", help="List targets without drawing.")
    ap.add_argument(
        "--latex", action="store_true",
        help="Use full LaTeX text rendering (requires a TeX installation).",
    )
    ap.add_argument(
        "--no-prefix", action="store_true",
        help="Do not include the ordering prefix in figure filenames.",
    )
    ap.add_argument(
        "--force", action="store_true",
        help="Force regeneration of figures. By default, skips if all requested figures already exist.",
    )
    ap.add_argument(
        "--renumber", type=Path, nargs="?", const=None, default=False,
        metavar="FIG_DIR",
        help="Only renumber existing figures in FIG_DIR "
             "(default: kepler_51/results/figures). No drawing.",
    )
    args = ap.parse_args(argv)

    if args.renumber is not False:
        fig_dir = args.renumber or (_PIPELINE / "kepler_51" / "results" / "figures")
        print(f"Renumbering figures in {fig_dir}")
        n = renumber_existing_figures(fig_dir)
        print(f"Done: {n} file(s) renamed.")
        return 0

    if not args.npz:
        ap.error("npz paths required (or use --renumber)")

    kinds = set(args.only) if args.only else set(FIGURE_KINDS)
    npz_files = _resolve_npz_args(args.npz)
    if not npz_files:
        print("No .npz files found.", file=sys.stderr)
        return 1

    style = dict(plot.PAPER_STYLE)
    style["use_latex"] = bool(args.latex)
    plot.apply_style(style)

    print(f"Generating {sorted(kinds)} for {len(npz_files)} run(s)")
    print(f"  output: <npz_dir>/figures/{{case}}_{{planet}}_{{ORDKEY}}-{{tag}}_corner|_corner_reduced|_ppc")

    per_case_ttv: dict[str, object] = {}

    def ttv_get_for(npz_path: Path):
        case_root = _infer_case_root(npz_path)
        key = str(case_root.resolve())
        if key not in per_case_ttv:
            case_paths = pr.CasePaths(case_root.name, pipeline_dir=_PIPELINE)
            per_case_ttv[key] = _load_ttv_cache(case_paths, {})
        return per_case_ttv[key]

    scoring_cache = {}
    def get_score_info(npz_path: Path, tag: str, case: str, planet: str):
        scoring_file = npz_path.parent / f"scoring_{case}_{planet}.json"
        if scoring_file not in scoring_cache:
            if not scoring_file.exists():
                scoring_cache[scoring_file] = None
            else:
                import json
                with open(scoring_file) as f:
                    data = json.load(f)
                scoring_cache[scoring_file] = {item["tag"]: item for item in data}
        if scoring_cache[scoring_file] is None:
            return None
        return scoring_cache[scoring_file].get(tag)

    n_ok = n_fail = 0
    for i, npz in enumerate(npz_files, 1):
        print(f"\n[{i:03d}/{len(npz_files)}] {npz.name}")
        
        # Read basic info to get the score
        import json
        meta_file = npz.with_name(npz.stem + "_meta.json")
        planet = "?"
        case = _infer_case_root(npz).name
        if meta_file.exists():
            with open(meta_file) as f:
                meta = json.load(f)
                planet = meta.get("planet", "?")
                case = meta.get("case", case)
        
        score_info = get_score_info(npz, npz.stem, case, planet)

        st = generate_for_run(
            npz, kinds=kinds, ttv_get=ttv_get_for(npz), score_info=score_info,
            index=i, dry_run=args.dry_run, no_prefix=args.no_prefix, force=args.force
        )
        if st.get("dry_run"):
            z1_txt = "nan" if not np.isfinite(st.get("z1", float("nan"))) else f"{st['z1']:.3f}"
            print(f"  dry-run  case={st['case']}  index={st['index']:03d}  z1={z1_txt}  ordkey={st.get('zkey')}")
            for name in st["preview"]:
                print(f"    → {name}")
            n_ok += 1
            continue
        if st["ok"]:
            n_ok += 1
            if st.get("already_exist"):
                print("  Skipped (figures already exist)")
            else:
                for k in st["skipped"]:
                    print(f"  skip   {k}")
        else:
            n_fail += 1
            print(f"  FAIL   {st['error']}", file=sys.stderr)

    print(f"\nDone: {n_ok} ok, {n_fail} failed, {len(npz_files)} total.")
    return 0 if n_fail == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
