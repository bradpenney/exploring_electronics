#!/usr/bin/env python3
"""Figures for docs/what_is_electricity.md.

circuit_loop.svg replaces the article's old mermaid chain (source -> resistance ->
load -> ground). Values match the article: a 5 V charger, the 250 Ohm worked
example from the Ohm's Law tabs rounded to the nearest standard part, 220 Ohm
(red-red-brown-gold, the value the article recommends), and an LED as the load.

Usage:
    python3 illustrations/what_is_electricity.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, MUTED, TEXT, common_defs, cyl_gradient,  # noqa: E402
                     led, panel, pill, render_all, shade, svg, text)

OUT = HERE.parent / "docs" / "images" / "what_is_electricity"


def wire(points, width=9):
    """A glossy copper wire along a polyline."""
    pts = " ".join(f"{x},{y}" for x, y in points)
    return [f'<polyline points="{pts}" fill="none" stroke="#3a1d0c" stroke-width="{width + 3}" stroke-linejoin="round" stroke-linecap="round"/>',
            f'<polyline points="{pts}" fill="none" stroke="#b8673a" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>',
            f'<polyline points="{pts}" fill="none" stroke="#ffd2b0" stroke-opacity="0.7" stroke-width="2.2" '
            f'stroke-linejoin="round" stroke-linecap="round" transform="translate(0,-2)"/>']


def electrons_along(points, every=46, offset=0):
    """Amber 'current' dots spaced along a polyline."""
    out, carry = [], offset
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        seg = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        d = carry
        while d < seg:
            f = d / seg
            x, y = x1 + (x2 - x1) * f, y1 + (y2 - y1) * f
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="10" fill="url(#glow)"/>'
                       f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="url(#vball)"/>')
            d += every
        carry = d - seg
    return out


def circuit_loop():
    w, h = 780, 420
    grads = cyl_gradient("battx", AMBER, vertical=True) + cyl_gradient("resbody", "#d9b382")
    parts = [common_defs(grads), panel(15, 15, w - 30, h - 30)]
    L, R, T, B = 150, 640, 110, 300
    loop = [(L, 170), (L, T), (R, T), (R, B), (L, B), (L, 240)]
    parts += wire(loop)
    dots = electrons_along([(L, T), (R, T), (R, B), (L, B)], offset=60)
    # keep the current dots off the LED body
    parts += [d for d in dots if not (abs(float(d.split('cx="')[1].split('"')[0]) - R) < 5
                                      and 170 < float(d.split('cy="')[1].split('"')[0]) < 250)]
    # direction chevrons
    for x, y, rot in ((300, T, 0), (R, 270, 90), (420, B, 180)):
        parts.append(f'<path d="M-8,-9 L6,0 L-8,9" fill="none" stroke="{AMBER_LIGHT}" stroke-width="3.5" '
                     f'stroke-linecap="round" stroke-linejoin="round" transform="translate({x},{y}) rotate({rot})"/>')
    # battery: vertical cylinder at the left
    bx, by, bw, bh = L - 28, 165, 56, 80
    parts.append(f'<ellipse cx="{L}" cy="{by + bh + 4}" rx="34" ry="8" fill="#000" fill-opacity="0.4"/>')
    parts.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="url(#battx)"/>')
    parts.append(f'<ellipse cx="{L}" cy="{by + bh}" rx="{bw / 2}" ry="8" fill="{shade(AMBER, -0.5)}"/>')
    parts.append(f'<ellipse cx="{L}" cy="{by}" rx="{bw / 2}" ry="8" fill="{shade(AMBER, 0.35)}"/>')
    parts.append(f'<rect x="{L - 9}" y="{by - 12}" width="18" height="10" rx="3" fill="#cbd5e0"/>')
    parts.append(f'<ellipse cx="{L}" cy="{by - 12}" rx="9" ry="3" fill="#ffffff"/>')
    parts.append(text(L, by + 34, "+", 22, "#1a1a1a", weight="bold"))
    parts.append(text(L, by + 62, "5 V", 15, "#1a1a1a", weight="bold"))
    # resistor on the top wire
    rx0, rlen, rr = 330, 130, 17
    parts.append(f'<rect x="{rx0}" y="{T - rr}" width="{rlen}" height="{rr * 2}" rx="{rr}" fill="url(#resbody)"/>')
    for i, (off, col) in enumerate(((26, "#e53e3e"), (44, "#e53e3e"), (62, "#8b4513"), (100, "#d4af37"))):
        parts.append(f'<rect x="{rx0 + off}" y="{T - rr + 1}" width="9" height="{rr * 2 - 2}" fill="{col}"/>')
        parts.append(f'<rect x="{rx0 + off}" y="{T - rr + 1}" width="9" height="{rr * 2 - 2}" fill="url(#gloss)"/>')
    # LED on the right wire
    parts += led(R, 205, "#68d391", lit=True, r=16)
    # ground symbol at the bottom-left return
    gx, gy = L + 60, B
    parts.append(f'<line x1="{gx}" y1="{gy}" x2="{gx}" y2="{gy + 22}" stroke="#a0aec0" stroke-width="3"/>')
    for i, half in enumerate((18, 12, 6)):
        parts.append(f'<line x1="{gx - half}" y1="{gy + 24 + i * 7}" x2="{gx + half}" y2="{gy + 24 + i * 7}" stroke="#a0aec0" stroke-width="3"/>')
    # labels
    parts += pill(L - 10, 62, "Voltage source · 5 V", "#d97706", "#1a1a1a", size=13, h=34)
    parts += pill(rx0 + rlen / 2, 62, "Resistance · 220 Ω", "#2d3748", size=13, h=34)
    parts += pill(R + 10, 62, "Load · LED", "#2f855a", size=13, h=34)
    parts += pill(gx + 125, B + 30, "back to ground · 0 V", "#1a202c", size=13, h=30)
    parts.append(text(w / 2, 384, "a voltage source drives current through resistance and a load, then back to ground", 13, MUTED, italic=True))
    parts.append(text(300, T + 28, "current", 13, AMBER_LIGHT, italic=True))
    return svg(w, h, "\n".join(parts), "A 3D circuit loop: a 5 volt battery drives current through a 220 ohm resistor and a lit LED, returning to ground at 0 volts")


FIGURES = {"circuit_loop.svg": circuit_loop}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
