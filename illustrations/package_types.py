#!/usr/bin/env python3
"""Figures for docs/package_types.md.

through_hole.svg and surface_mount.svg replace the article's two mermaid trees.
Both are drawn TO THE SAME SCALE (SCALE px per mm) on a slice of 1.6 mm circuit
board, so the size difference between the families is real, not illustrative.
Nominal body sizes (mm, from the common JEDEC outlines):
    TO-92   4.8 W x 3.8 D x 4.8 H        TO-220  10 W x 4.5 D x 9 H (+ 6 mm tab)
    DIP-8   9.8 L x 6.4 W x 3.3 H        SOT-23  2.9 L x 1.3 W x 1.0 H
    SOIC-8  4.9 L x 3.9 W x 1.5 H        QFN-16  4.0 x 4.0 x 0.9
    0805    2.0 L x 1.25 W x 0.5 H

Usage:
    python3 illustrations/package_types.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER_LIGHT, MUTED, TEXT, box3d, common_defs, panel,  # noqa: E402
                     render_all, shade, svg, text)

OUT = HERE.parent / "docs" / "images" / "package_types"
SCALE = 9.0          # px per mm
BOARD_T = 1.6        # mm
PCB = "#2f6f4e"
BODY = "#22262e"


def board(x, y, w, d):
    """PCB slab; returns parts and a function mapping (u mm, v mm) on its top to screen."""
    parts = box3d(x, y, w, d, BOARD_T * SCALE, PCB)
    top_y = y - BOARD_T * SCALE

    def at(u, v):
        return x + u * SCALE + v * SCALE * 0.7, top_y - v * SCALE * 0.45
    return parts, at


def through_hole():
    w, h = 780, 440
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "Through-hole: legs go through the board", 16, TEXT, weight="bold"))
    parts.append(text(w / 2, 66, f"drawn to scale with the surface-mount figure ({SCALE:g} px per mm)", 12, MUTED, italic=True))
    bx, by = 70, 300
    bparts, at = board(bx, by, 600, 9 * SCALE)
    parts += bparts
    # legs poking out under the board
    def legs_below(xs):
        out = []
        for lx in xs:
            out.append(f'<rect x="{lx - 1.5:.1f}" y="{by}" width="3" height="34" fill="#cbd5e0"/>')
            out.append(f'<ellipse cx="{lx:.1f}" cy="{by + 34:.1f}" rx="5" ry="2.5" fill="#a0aec0"/>')
        return out
    # TO-92 at u=8
    x, y = at(8, 2.5)
    parts += legs_below([x + k * 2.54 * SCALE for k in (0.3, 1.0, 1.7)])
    for k in (0.3, 1.0, 1.7):
        parts.append(f'<rect x="{x + k * 2.54 * SCALE - 1.5:.1f}" y="{y - 10:.1f}" width="3" height="10" fill="#cbd5e0"/>')
    parts += box3d(x, y - 10, 4.8 * SCALE, 3.8 * SCALE, 4.8 * SCALE, BODY, shadow=False)
    parts.append(text(x + 24, y - 30, "TO-92", 9, "#a0aec0"))
    lab = [(x + 30, "TO-92", "sensors, small transistors")]
    # TO-220 at u=26
    x, y = at(25, 2.5)
    parts += legs_below([x + k * 2.54 * SCALE for k in (0.6, 1.6, 2.6)])
    for k in (0.6, 1.6, 2.6):
        parts.append(f'<rect x="{x + k * 2.54 * SCALE - 2:.1f}" y="{y - 30:.1f}" width="4" height="30" fill="#cbd5e0"/>')
    tab_h = 6 * SCALE
    parts += box3d(x, y - 30 - 9 * SCALE, 10 * SCALE, 1.3 * SCALE, tab_h, "#a0aec0", shadow=False)
    tx, ty = x + 5 * SCALE, y - 30 - 9 * SCALE - tab_h * 0.55
    parts.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="{1.8 * SCALE:.1f}" fill="#1a202c"/>')
    parts += box3d(x, y - 30, 10 * SCALE, 4.5 * SCALE, 9 * SCALE, BODY, shadow=False)
    parts.append(text(x + 45, y - 66, "TO-220", 10, "#a0aec0"))
    lab.append((x + 55, "TO-220", "regulators, power transistors"))
    # DIP-8 at u=48
    x, y = at(46, 0.6)
    for side, v in ((0, 0), (1, 7.62)):
        for k in range(4):
            lx, ly = at(46 + 1.2 + k * 2.54, 0.6 + v)
            if side == 0:
                parts.append(f'<rect x="{lx - 2:.1f}" y="{ly - 8:.1f}" width="4" height="8" fill="#cbd5e0"/>')
    parts += legs_below([at(46 + 1.2 + k * 2.54, 0.6)[0] for k in range(4)])
    x, y = at(46, 0.6 + 0.6)
    parts += box3d(x, y - 8, 9.8 * SCALE, 6.4 * SCALE, 3.3 * SCALE, BODY, shadow=False)
    parts.append(f'<ellipse cx="{x + 1.5 * SCALE:.1f}" cy="{y - 8 - 3.3 * SCALE - 1.2 * SCALE:.1f}" rx="5" ry="3" fill="#0d1117"/>')
    parts.append(text(x + 45, y - 22, "DIP-8", 10, "#a0aec0"))
    lab.append((x + 55, "DIP", "classic hobby ICs, the Uno's chip"))
    for lx, name, use in lab:
        parts.append(text(lx, 372, name, 15, AMBER_LIGHT, weight="bold"))
        parts.append(text(lx, 392, use, 12, TEXT))
    parts.append(text(w / 2, 418, "every leg passes through a hole and is soldered on the far side", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Three through-hole packages to scale on a circuit board, legs passing through it: a TO-92, a TO-220 with its metal tab, and an 8-pin DIP")


def surface_mount():
    w, h = 780, 440
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "Surface-mount: parts sit on pads on top of the board", 16, TEXT, weight="bold"))
    parts.append(text(w / 2, 66, f"board drawn at the same scale as the through-hole figure ({SCALE:g} px per mm); lenses magnify each part", 12, MUTED, italic=True))
    bx, by = 70, 300
    bparts, at = board(bx, by, 600, 9 * SCALE)
    parts += bparts
    pad = "#d4af37"

    def pads(u, v, n, pitch, length, side_v):
        out = []
        for k in range(n):
            x, y = at(u + k * pitch, v + side_v)
            out.append(f'<polygon points="{x:.1f},{y:.1f} {x + 0.6 * SCALE:.1f},{y:.1f} {x + 0.6 * SCALE + length * SCALE * 0.7:.1f},'
                       f'{y - length * SCALE * 0.45:.1f} {x + length * SCALE * 0.7:.1f},{y - length * SCALE * 0.45:.1f}" fill="{pad}"/>')
        return out
    groups = []  # (svg parts, visual centre, name, use)
    # SOT-23 at u=7
    g = pads(7.1, 2.8, 2, 1.9, 0.9, -0.9) + pads(8.05, 2.8, 1, 0, 0.9, 1.3)
    x, y = at(7, 2.8)
    g += box3d(x, y, 2.9 * SCALE, 1.3 * SCALE, 1.0 * SCALE, BODY, shadow=False)
    groups.append((g, (x + (2.9 + 1.3 * 0.7) * SCALE / 2, y - (1.0 + 1.3 * 0.45) * SCALE / 2), "SOT-23", "small transistors", 3.6))
    # SOIC-8 at u=23
    g = pads(23.4, 2, 4, 1.27, 1.0, -1.0) + pads(23.4, 2, 4, 1.27, 1.0, 3.9)
    x, y = at(23, 2)
    g += box3d(x, y, 4.9 * SCALE, 3.9 * SCALE, 1.5 * SCALE, BODY, shadow=False)
    g.append(f'<ellipse cx="{x + 0.9 * SCALE:.1f}" cy="{y - 1.5 * SCALE - 0.7 * SCALE:.1f}" rx="3" ry="2" fill="#0d1117"/>')
    groups.append((g, (x + (4.9 + 3.9 * 0.7) * SCALE / 2, y - (1.5 + 3.9 * 0.45) * SCALE / 2), "SOIC", "most modern ICs", 2.0))
    # QFN-16 at u=39
    x, y = at(39, 2.2)
    g = box3d(x, y, 4.0 * SCALE, 4.0 * SCALE, 0.9 * SCALE, BODY, shadow=False)
    for k in range(4):
        px = x + (0.6 + k * 0.85) * SCALE
        g.append(f'<rect x="{px:.1f}" y="{y - 2:.1f}" width="{0.35 * SCALE:.1f}" height="2.5" fill="{pad}"/>')
    groups.append((g, (x + (4.0 + 4.0 * 0.7) * SCALE / 2, y - (0.9 + 4.0 * 0.45) * SCALE / 2), "QFN", "no legs: pads underneath", 2.3))
    # 0805 at u=55
    x, y = at(54.7, 3.4)
    g = box3d(x, y, 2.0 * SCALE, 1.25 * SCALE, 0.5 * SCALE, BODY, shadow=False)
    for ex in (0, 1.6):
        g += box3d(x + ex * SCALE, y, 0.4 * SCALE, 1.25 * SCALE, 0.5 * SCALE, "#cbd5e0", shadow=False)
    groups.append((g, (x + (2.0 + 1.25 * 0.7) * SCALE / 2, y - (0.5 + 1.25 * 0.45) * SCALE / 2), "0805", "resistors, capacitors", 4.5))
    lens_x = [150, 310, 470, 630]
    for (g, (px, py), name, use, zoom), lx in zip(groups, lens_x):
        parts += g
        ly, r = 165, 62
        parts.append(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{lx}" y2="{ly + r}" stroke="{MUTED}" stroke-dasharray="3 4"/>')
        parts.append(f'<clipPath id="lens{lx}"><circle cx="{lx}" cy="{ly}" r="{r - 3}"/></clipPath>')
        parts.append(f'<circle cx="{lx}" cy="{ly}" r="{r}" fill="{PCB}" stroke="#cbd5e0" stroke-opacity="0.6" stroke-width="3"/>')
        parts.append(f'<g clip-path="url(#lens{lx})"><g transform="translate({lx},{ly}) scale({zoom}) translate({-px:.1f},{-py:.1f})">'
                     + "".join(g) + '</g></g>')
        parts.append(f'<circle cx="{lx}" cy="{ly}" r="{r - 3}" fill="url(#gloss)" opacity="0.5"/>')
        parts.append(text(lx + r - 6, ly - r + 8, f"{zoom:g}×", 11, AMBER_LIGHT, "start", "bold"))
        parts.append(text(lx, 372, name, 15, AMBER_LIGHT, weight="bold"))
        parts.append(text(lx, 392, use, 12, TEXT))
    parts.append(text(w / 2, 418, "nothing goes through the board: each part is soldered to copper pads on the surface", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Four surface-mount packages to scale on a circuit board, sitting on gold pads, each with a magnifying lens above it: a SOT-23, an 8-lead SOIC, a leadless QFN, and a tiny 0805 chip resistor")


FIGURES = {"through_hole.svg": through_hole, "surface_mount.svg": surface_mount}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
