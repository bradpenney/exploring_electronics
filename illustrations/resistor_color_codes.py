#!/usr/bin/env python3
"""Figures for docs/resistor_color_codes.md.

resistor_bands.svg replaces the old flat images/resistor_color_bands.svg: the same
220 Ohm red-red-brown-gold resistor (22 x 10 = 220 Ohm, +/-5%), drawn as a lit 3D
cylinder with the classic bulging ends, bands wrapping the body, and the tolerance
band set apart (the gap is the reading-direction clue the article teaches).

Usage:
    python3 illustrations/resistor_color_codes.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, MUTED, TEXT, common_defs, cyl_gradient,  # noqa: E402
                     render_all, svg, text)

OUT = HERE.parent / "docs" / "images" / "resistor_color_codes"

BANDS = [  # (x offset on body, colour, value label, role label)
    (88, "#e53e3e", "2", "1st digit"),
    (150, "#e53e3e", "2", "2nd digit"),
    (212, "#8b4513", "×10", "Multiplier"),
    (330, "#d4af37", "±5%", "Tolerance"),
]


def resistor_bands():
    w, h = 680, 300
    grads = cyl_gradient("body", "#dcb787") + cyl_gradient("lead", "#cbd5e0")
    for i, (_, col, _, _) in enumerate(BANDS):
        grads += cyl_gradient(f"band{i}", col)
    parts = [common_defs(grads)]
    cx0, cy, length, r = 150, 150, 380, 34
    # leads
    parts.append(f'<ellipse cx="{w / 2}" cy="{cy + r + 18}" rx="290" ry="10" fill="#000" fill-opacity="0.4"/>')
    parts.append(f'<rect x="20" y="{cy - 4}" width="{cx0 + 10}" height="8" rx="4" fill="url(#lead)"/>')
    parts.append(f'<rect x="{cx0 + length - 10}" y="{cy - 4}" width="{w - 20 - cx0 - length + 10}" height="8" rx="4" fill="url(#lead)"/>')
    # body: a capsule with bulged end caps
    parts.append(f'<rect x="{cx0 + 40}" y="{cy - r + 5}" width="{length - 80}" height="{2 * r - 10}" fill="url(#body)"/>')
    for ex in (cx0 + 40, cx0 + length - 40):
        parts.append(f'<ellipse cx="{ex}" cy="{cy}" rx="44" ry="{r}" fill="url(#body)"/>')
    for i, (off, col, val, role) in enumerate(BANDS):
        x = cx0 + off
        bulge = off < 60 or off > length - 60
        hh = 2 * r if bulge else 2 * r - 10
        parts.append(f'<rect x="{x}" y="{cy - hh / 2}" width="24" height="{hh}" rx="3" fill="url(#band{i})"/>')
        parts.append(text(x + 12, cy - r - 14, val, 18, TEXT, weight="bold"))
        parts.append(f'<line x1="{x + 12}" y1="{cy + r + 4}" x2="{x + 12}" y2="{cy + r + 26}" stroke="{MUTED}" stroke-dasharray="2 3"/>')
        parts.append(text(x + 12, cy + r + 44, role, 14, TEXT))
    parts.append(f'<rect x="{cx0 + 40}" y="{cy - r + 7}" width="{length - 80}" height="8" rx="4" fill="#ffffff" fill-opacity="0.18"/>')
    parts.append(f'<line x1="{cx0 + 80}" y1="44" x2="{cx0 + 310}" y2="44" stroke="{AMBER}" stroke-width="3" marker-end="url(#arrow)"/>')
    parts.append(text(cx0 + 195, 32, "Read left → right", 15, AMBER_LIGHT, weight="bold"))
    parts.append(text(cx0 + 300, cy + 6, "gap", 11, "#5c4426", italic=True))
    parts.append(text(w / 2, h - 14, "22 × 10 = 220 Ω ±5%", 17, TEXT, weight="bold"))
    return svg(w, h, "\n".join(parts), "A 3D resistor with four colour bands, red, red, brown and gold, labelled 2, 2, times 10 and plus or minus 5 percent, read left to right: 22 times 10 equals 220 ohms, plus or minus 5 percent")


FIGURES = {"resistor_bands.svg": resistor_bands}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
