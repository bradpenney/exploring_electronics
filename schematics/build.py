#!/usr/bin/env python3
"""Regenerate every schematic SVG from its Python source.

Each circuit lives in ``circuits/<name>.py`` and exposes a ``build(path)``
function that writes one SVG. Output goes to ``docs/images/schematics/`` so
articles can reference it like any other image. The committed SVGs — not this
script — are what the site serves, so a tool migration never touches the
markdown; it only needs to re-emit files with the same names here.

Usage:
    poetry run python schematics/build.py
"""

import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CIRCUITS_DIR = HERE / "circuits"
OUTPUT_DIR = HERE.parent / "docs" / "images" / "schematics"

# Make ``style`` and the circuit modules importable.
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(CIRCUITS_DIR))


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sources = sorted(p for p in CIRCUITS_DIR.glob("*.py") if p.stem != "__init__")
    if not sources:
        print("No circuit sources found in", CIRCUITS_DIR)
        return

    for src in sources:
        module = importlib.import_module(src.stem)
        out = OUTPUT_DIR / f"{src.stem}.svg"
        module.build(out)
        print(f"  {src.stem}.py -> {out.relative_to(HERE.parent)}")

    print(f"Done. {len(sources)} schematic(s) written to {OUTPUT_DIR}.")


if __name__ == "__main__":
    main()
