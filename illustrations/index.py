#!/usr/bin/env python3
"""Figure for docs/index.md: the Circuit Foundations path as a 3D staircase.

The step order matches the Circuit Foundations nav in mkdocs.yaml.

Usage:
    python3 illustrations/index.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, MUTED, TEXT, box3d, common_defs,  # noqa: E402
                     panel, render_all, svg, text)

OUT = HERE.parent / "docs" / "images" / "index"

STEPS = [
    (("Conductors",), "the atom"),
    (("What Is", "Electricity?"), "big picture"),
    (("Metric", "Prefixes"), "milli to mega"),
    (("Voltage",), "the push"),
    (("Current",), "the flow"),
    (("Resistance",), "the limit"),
    (("Ohm's Law",), "and power"),
    (("Shorts and", "Fuses"), "when it fails"),
    (("AC vs DC",), "and RMS"),
    (("Magnetism",), "and coils"),
    (("Series &", "Parallel"), "real circuits"),
]


def foundations_path():
    w, h = 960, 440
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Circuit Foundations: eleven steps from the atom to real circuits", 16, TEXT, weight="bold"))
    x0, base, sw = 40, 380, 82
    for i, (name, sub) in enumerate(STEPS):
        hgt = 96 + i * 20
        x = x0 + i * sw
        color = AMBER if i == 0 else ("#4a5568" if i % 2 else "#3c4658")
        parts += box3d(x, base, sw - 10, 34, hgt, color, shadow=(i == 0))
        top = base - hgt
        cx = x + (sw - 10) / 2
        fg = "#1a1a1a" if i == 0 else TEXT
        parts.append(f'<circle cx="{cx + 12}" cy="{top - 32}" r="15" fill="url(#{"vball" if i == 0 else "eball"})"/>')
        parts.append(text(cx + 12, top - 27, str(i + 1), 14, "#1a1a1a", weight="bold"))
        for k, line in enumerate(name):
            parts.append(text(cx, top + 24 + k * 15, line, 11, fg, weight="bold"))
        parts.append(text(cx, top + 26 + len(name) * 15, sub, 9, "#1a1a1a" if i == 0 else MUTED, italic=True))
    parts.append(text(x0 + (sw - 10) / 2, base + 30, "start here", 13, AMBER_LIGHT, weight="bold"))
    return svg(w, h, "\n".join(parts), "A 3D staircase of eleven numbered steps: 1 Conductors, 2 What Is Electricity, 3 Metric Prefixes, 4 Voltage, 5 Current, 6 Resistance, 7 Ohm's Law and power, 8 Shorts and Fuses, 9 AC vs DC, 10 Magnetism, 11 Series and Parallel circuits. The first step is lit amber and marked start here.")


FIGURES = {"foundations_path.svg": foundations_path}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
