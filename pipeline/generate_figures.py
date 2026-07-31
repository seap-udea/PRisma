#!/usr/bin/env python3
"""generate_figures.py — Corner / reduced-corner / PPC figures for saved runs.

Reads one or more ``.npz`` posterior files (from ``run_sweep`` / nested sampling)
and writes publication-style figures under ``<case>/results/figures/`` as::

    {NNN}-{tag}_corner.png
    {NNN}-{tag}_corner_reduced.png
    {NNN}-{tag}_ppc.png

``NNN`` is a zero-padded index in generation order (001, 002, …), so the three
figures of each configuration stay together when the directory is sorted.

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

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Allow ``python generate_figures.py …`` from pipeline/ without an install.
_PIPELINE = Path(__file__).resolve().parent
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


def _fig_name(index: int, tag: str, kind: str, ext: str) -> str:
    """``001-{tag}_corner.png`` (and ``_corner_reduced`` / ``_ppc``)."""
    return f"{index:03d}-{tag}_{_KIND_SUFFIX[kind]}.{ext}"


def generate_for_run(npz_path: Path, kinds: set[str], ttv_get,
                     index: int = 1, dry_run: bool = False) -> dict:
    """Draw the requested figures for one ``.npz``. Returns a status dict."""
    npz_path = Path(npz_path)
    if not npz_path.exists():
        return {"tag": npz_path.name, "ok": False, "error": "file not found"}

    case_root = _infer_case_root(npz_path)
    case_paths = pr.CasePaths(case_root.name, pipeline_dir=case_root.parent)
    fig_paths = _ResultsFiguresPaths(case_root)
    version = plot.run_version_id([npz_path])
    ext = plot.STYLE["fig_format"]
    out_dir = fig_paths.figures_dir()

    if dry_run:
        preview = [_fig_name(index, npz_path.stem, k, ext) for k in FIGURE_KINDS if k in kinds]
        return {
            "tag": npz_path.stem,
            "ok": True,
            "dry_run": True,
            "case": case_root.name,
            "kinds": sorted(kinds),
            "index": index,
            "out": str(out_dir),
            "preview": preview,
        }

    run = load_run(npz_path)
    tag = run["tag"]
    planet = run["planet"]
    status = {
        "tag": tag, "planet": planet, "ok": True, "index": index,
        "made": [], "skipped": [], "error": None,
    }

    try:
        out_dir.mkdir(parents=True, exist_ok=True)

        if "corner" in kinds:
            fig = plot.plot_results_panel_inset(run, paths=None, title=True)
            if fig is None:
                status["skipped"].append("corner")
            else:
                plot.add_run_version_label(fig, version)
                out = out_dir / _fig_name(index, tag, "corner", ext)
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
                out = out_dir / _fig_name(index, tag, "reduced", ext)
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
                    out = out_dir / _fig_name(index, tag, "ppc", ext)
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
    print(f"  output: <case>/results/figures/{{NNN}}-{{tag}}_corner|_corner_reduced|_ppc")

    per_case_ttv: dict[str, object] = {}

    def ttv_get_for(npz_path: Path):
        case_root = _infer_case_root(npz_path)
        key = str(case_root.resolve())
        if key not in per_case_ttv:
            case_paths = pr.CasePaths(case_root.name, pipeline_dir=case_root.parent)
            per_case_ttv[key] = _load_ttv_cache(case_paths, {})
        return per_case_ttv[key]

    n_ok = n_fail = 0
    for i, npz in enumerate(npz_files, 1):
        print(f"\n[{i:03d}/{len(npz_files)}] {npz.name}")
        st = generate_for_run(
            npz, kinds=kinds, ttv_get=ttv_get_for(npz),
            index=i, dry_run=args.dry_run,
        )
        if st.get("dry_run"):
            print(f"  dry-run  case={st['case']}  index={st['index']:03d}")
            for name in st["preview"]:
                print(f"    → {name}")
            n_ok += 1
            continue
        if st["ok"]:
            n_ok += 1
            for k in st["skipped"]:
                print(f"  skip   {k}")
        else:
            n_fail += 1
            print(f"  FAIL   {st['error']}", file=sys.stderr)

    print(f"\nDone: {n_ok} ok, {n_fail} failed, {len(npz_files)} total.")
    return 0 if n_fail == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
