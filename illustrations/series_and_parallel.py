#!/usr/bin/env python3
"""Figures for docs/series_and_parallel.md.

Sources: none beyond the series and parallel rules and P = I^2 R = V^2 / R;
every number below is computed.

Usage:
    python3 illustrations/series_and_parallel.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, box3d,  # noqa: E402
                     common_defs, cyl_gradient, panel, pill, render_all, shade,
                     svg, text)

OUT = HERE.parent / "docs" / "images" / "series_and_parallel"
BLUE = "#4299e1"


def par(*rs):
    return 1 / sum(1 / r for r in rs)


def _resistor(parts, x, y, length, label, gid, vertical=False, glow=None):
    """A lit cylinder resistor; glow is a colour for a heat halo."""
    if glow:
        cx, cy = (x, y + length / 2) if vertical else (x + length / 2, y)
        parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{(28 if vertical else length * 0.75):.0f}" '
                     f'ry="{(length * 0.75 if vertical else 28):.0f}" fill="{glow}" fill-opacity="0.28" filter="url(#softglow)"/>')
    if vertical:
        parts.append(f'<rect x="{x - 11}" y="{y}" width="22" height="{length}" rx="10" fill="url(#{gid})"/>')
        for k in (0.3, 0.45, 0.6):
            parts.append(f'<rect x="{x - 11}" y="{y + length * k:.1f}" width="22" height="5" fill="#5a3a1a"/>')
    else:
        parts.append(f'<rect x="{x}" y="{y - 11}" width="{length}" height="22" rx="10" fill="url(#{gid})"/>')
        for k in (0.3, 0.45, 0.6):
            parts.append(f'<rect x="{x + length * k:.1f}" y="{y - 11}" width="5" height="22" fill="#5a3a1a"/>')
    if label:
        lx, ly = (x + 22, y + length / 2 + 5) if vertical else (x + length / 2, y - 20)
        parts.append(text(lx, ly, label, 14, TEXT, "start" if vertical else "middle", weight="bold"))


# 1. Reducing a network one step at a time ------------------------------------------
def reduction():
    w, h = 900, 380
    parts = [common_defs(cyl_gradient("sp-res", "#d6b98c") + cyl_gradient("sp-resv", "#d6b98c", vertical=True))]
    wire = f'stroke="{TEXT}" stroke-width="3" fill="none"'
    steps = [(15, "1. As drawn"), (310, "2. Combine the parallel pair"), (605, "3. Add the series part")]
    for x, title in steps:
        parts.append(panel(x, 15, 280, h - 30))
        parts.append(text(x + 140, 50, title, 15, AMBER_LIGHT, weight="bold"))
    # stage 1: 100 then (300 || 600)
    x0 = 15
    parts.append(f'<path d="M{x0 + 40},120 L{x0 + 60},120" {wire}/>')
    _resistor(parts, x0 + 60, 120, 70, "100 Ω", "sp-res")
    parts.append(f'<path d="M{x0 + 130},120 L{x0 + 200},120 M{x0 + 165},120 L{x0 + 165},150 M{x0 + 235},120 L{x0 + 235},150 M{x0 + 200},120 L{x0 + 235},120" {wire}/>')
    _resistor(parts, x0 + 165, 150, 80, "", "sp-resv", vertical=True)
    _resistor(parts, x0 + 235, 150, 80, "", "sp-resv", vertical=True)
    parts.append(text(x0 + 140, 195, "300 Ω", 13, TEXT, "end", weight="bold"))
    parts.append(text(x0 + 260, 195, "600 Ω", 13, TEXT, "start", weight="bold"))
    parts.append(f'<path d="M{x0 + 165},230 L{x0 + 165},260 L{x0 + 235},260 L{x0 + 235},230" {wire}/>')
    parts.append(text(x0 + 140, 320, "9 V across the whole network", 12, MUTED, italic=True))
    # stage 2
    x1 = 310
    rp = par(300, 600)
    parts.append(f'<path d="M{x1 + 40},120 L{x1 + 60},120" {wire}/>')
    _resistor(parts, x1 + 60, 120, 70, "100 Ω", "sp-res")
    parts.append(f'<path d="M{x1 + 130},120 L{x1 + 200},120 L{x1 + 200},150" {wire}/>')
    _resistor(parts, x1 + 200, 150, 80, f"{rp:.0f} Ω", "sp-resv", vertical=True)
    parts.append(text(x1 + 140, 300, "300 × 600 ÷ (300 + 600) = 200 Ω", 12, TEXT))
    parts.append(text(x1 + 140, 320, "product over sum", 12, MUTED, italic=True))
    # stage 3
    x2 = 605
    total = 100 + rp
    _resistor(parts, x2 + 105, 110, 110, f"{total:.0f} Ω", "sp-resv", vertical=True)
    parts.append(text(x2 + 140, 270, "100 + 200 = 300 Ω", 13, TEXT, weight="bold"))
    i = 9 / total
    parts += pill(x2 + 140, 310, f"9 V ÷ {total:.0f} Ω = {i * 1000:.0f} mA", GREEN, size=13, h=30)
    return svg(w, h, "\n".join(parts), "Three panels reducing a resistor network. First, a 100 ohm resistor in series with a 300 ohm and a 600 ohm resistor in parallel. Second, the parallel pair replaced by its equivalent, 200 ohms, from product over sum. Third, 100 plus 200 gives one 300 ohm resistor, and 9 volts across it drives 30 milliamps.")


# 2. Who gets hot: series vs parallel --------------------------------------------------
def heat_sharing():
    w, h = 900, 470
    parts = [common_defs(), panel(15, 15, 425, h - 30), panel(460, 15, 425, h - 30)]
    rating = 0.25
    base, full = 380, 200  # px for 0.25 W
    for cx, title, sub, powers in [
        (227, "In series across 12 V", "same current: the bigger resistor runs hotter",
         [(100, 12 ** 2 * 100 / 1100 ** 2), (1000, 12 ** 2 * 1000 / 1100 ** 2)]),
        (672, "In parallel across 12 V", "same voltage: the smaller resistor runs hotter",
         [(100, 12 ** 2 / 100), (1000, 12 ** 2 / 1000)]),
    ]:
        parts.append(text(cx, 50, title, 16, AMBER_LIGHT, weight="bold"))
        parts.append(text(cx, 72, sub, 12, MUTED, italic=True))
        ry = base - full
        parts.append(f'<line x1="{cx - 170}" y1="{ry}" x2="{cx + 170}" y2="{ry}" stroke="{RED}" stroke-width="2" stroke-dasharray="7 5"/>')
        parts.append(text(cx + 170, ry - 8, "¼ W rating", 12, RED, "end", weight="bold"))
        for k, (r, p) in enumerate(powers):
            bx = cx - 110 + k * 130
            over = p > rating
            bh = min(p, rating * 1.08) / rating * full
            color = RED if over else (AMBER if p > rating / 2 else GREEN)
            parts += box3d(bx, base, 70, 36, bh, color)
            label = f"{p:.2f} W" if p >= 1 else f"{p * 1000:.0f} mW"
            parts.append(text(bx + 47, base - bh - 44, label, 15, TEXT, weight="bold"))
            pct = f"{p / rating * 100:.0f}% of rating"
            parts.append(text(bx + 47, base - bh - 26, pct + (", burns" if over else ""), 11, shade(color, 0.3)))
            if over:
                parts.append(f'<path d="M{bx - 4},{base - bh + 14} l84,-10 M{bx - 4},{base - bh + 24} l84,-10" stroke="#1a202c" stroke-width="5"/>')
            parts.append(text(bx + 35, base + 30, f"{r:,} Ω".replace(",000", " k").replace("1 k Ω", "1 kΩ"), 15, TEXT, weight="bold"))
    return svg(w, h, "\n".join(parts), "Two panels of 3D bars against a quarter-watt rating line. A 100 ohm and a 1 kilohm quarter-watt resistor in series across 12 volts dissipate 12 milliwatts and 119 milliwatts: the bigger resistor runs hotter, both are safe. The same pair in parallel across 12 volts dissipate 1.44 watts and 144 milliwatts: the 100 ohm resistor is at 576 percent of its rating and burns.")


# 3. Same resistance, more power ---------------------------------------------------------
def test_load():
    w, h = 900, 400
    parts = [common_defs(cyl_gradient("sp-resv2", "#c9a46b", vertical=True)), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 50, "Four 200 Ω, 2 W resistors in parallel: one 50 Ω resistor rated 8 W", 16, AMBER_LIGHT, weight="bold"))
    wire = f'stroke="{TEXT}" stroke-width="4" fill="none"'
    top, bot = 110, 300
    parts.append(f'<path d="M180,{top} L720,{top} M180,{bot} L720,{bot}" {wire}/>')
    total_p = 5.0
    v = (total_p * 50) ** 0.5
    each = v ** 2 / 200
    for k in range(4):
        x = 240 + k * 140
        parts.append(f'<path d="M{x},{top} L{x},{top + 35} M{x},{bot - 35} L{x},{bot}" {wire}/>')
        _resistor(parts, x, top + 35, 120, "", "sp-resv2", vertical=True, glow=AMBER)
        parts.append(text(x + 22, top + 80, "200 Ω", 13, TEXT, "start", weight="bold"))
        parts.append(text(x + 22, top + 98, "2 W", 13, MUTED, "start"))
        parts.append(text(x, bot + 28, f"{each:.2f} W each", 13, AMBER_LIGHT, weight="bold"))
    parts.append(f'<circle cx="170" cy="{top}" r="7" fill="{GREEN}"/><circle cx="170" cy="{bot}" r="7" fill="{MUTED}"/>')
    parts.append(text(150, (top + bot) / 2 - 6, f"{v:.1f} V", 15, TEXT, "end", weight="bold"))
    parts.append(text(150, (top + bot) / 2 + 14, "5 W total", 12, MUTED, "end", italic=True))
    parts.append(text(w / 2, 365, f"At 5 W total, each carries a quarter: {each:.2f} W, {each / 2 * 100:.0f}% of its 2 W rating", 13, TEXT))
    return svg(w, h, "\n".join(parts), "Four 200 ohm, 2 watt resistors in parallel between two bus bars, each glowing. Together they make 50 ohms rated for 8 watts. With 5 watts in total, about 15.8 volts across them, each carries 1.25 watts, 62 percent of its rating.")


FIGURES = {"reduction.svg": reduction, "heat_sharing.svg": heat_sharing, "test_load.svg": test_load}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
