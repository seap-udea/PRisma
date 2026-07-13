"""Convert Exorings Python 2 scripts into Python 3 copies.

This script:
- reads sources from `exorings/python2/`
- writes converted copies to `exorings/python3/` (same relative paths)
- never overwrites the originals under `python2/`
"""

from __future__ import annotations

import argparse
import os
import py_compile
import shutil
import sys
import tokenize
from pathlib import Path

from lib2to3.refactor import RefactoringTool, get_fixers_from_package


def _iter_py_files(root_dir: Path) -> list[Path]:
    return sorted(path for path in root_dir.rglob("*.py") if path.is_file())


def _read_text(path: Path) -> str:
    with tokenize.open(path) as handle:
        return handle.read()


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")


def _convert_file(tool: RefactoringTool, src_path: Path, dst_path: Path) -> None:
    src_text = _read_text(src_path)
    converted = str(tool.refactor_string(src_text, str(src_path)))
    _write_text(dst_path, converted)
    shutil.copymode(src_path, dst_path)


def _compile_file(path: Path) -> None:
    py_compile.compile(str(path), doraise=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert exorings/python2 scripts to Python 3 copies")
    parser.add_argument("--src", default="python2", help="Source directory (relative to this script)")
    parser.add_argument("--dst", default="python3", help="Destination directory (relative to this script)")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    src_root = (script_dir / args.src).resolve()
    dst_root = (script_dir / args.dst).resolve()

    if not src_root.exists() or not src_root.is_dir():
        raise SystemExit(f"Source directory not found: {src_root}")

    if src_root == dst_root:
        raise SystemExit("Refusing to run with --dst equal to --src (would overwrite sources)")

    # Prevent accidental recursion if dst is inside src
    try:
        dst_root.relative_to(src_root)
    except ValueError:
        pass
    else:
        raise SystemExit("Refusing to run with --dst inside --src (would recurse into outputs)")

    tool = RefactoringTool(get_fixers_from_package("lib2to3.fixes"))

    src_files = _iter_py_files(src_root)
    if not src_files:
        print(f"No .py files found under {src_root}")
        return 0

    converted_files: list[Path] = []
    for src_path in src_files:
        rel = src_path.relative_to(src_root)
        dst_path = dst_root / rel
        _convert_file(tool, src_path, dst_path)
        converted_files.append(dst_path)

    missing = [p for p in converted_files if not p.exists()]
    if missing:
        raise SystemExit(f"Conversion incomplete; missing outputs: {missing}")

    compile_errors: list[tuple[Path, Exception]] = []
    for dst_path in converted_files:
        try:
            _compile_file(dst_path)
        except Exception as exc:  # noqa: BLE001
            compile_errors.append((dst_path, exc))

    if compile_errors:
        print("Python 3 compilation failed for:")
        for path, exc in compile_errors:
            print(f"- {path}: {exc}")
        return 2

    print(f"Created/updated {len(converted_files)} Python 3 file(s) under: {dst_root}")
    for path in converted_files:
        print(f"- {path.relative_to(script_dir)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())