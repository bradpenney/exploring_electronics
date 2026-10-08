#!/usr/bin/env python3
"""Figures for docs/pull_resistors.md.

Sources: the article's own numbers: Uno input thresholds 3 V / 1.5 V; the
ATmega328P's internal pull-up of 20 to 50 kOhm; currents through a pull resistor
while the button is pressed: 5 V / 100 Ohm = 50 mA, 5 V / 10 kOhm = 0.5 mA.
The floating trace is illustrative noise (seeded random walk), not a
measurement.

Usage:
    python3 illustrations/pull_resistors.py
"""

import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, box3d,  # noqa: E402
                     common_defs, panel, pill, render_all, shade, svg, text)
from ac_dc import axes, glow_line  # noqa: E402

OUT = HERE.parent / "docs" / "images" / "pull_resistors"


# 1. A floating pin versus a pulled-down one -----------------------------------------------------------
def floating():
    w, h = 900, 470
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "An input with nothing connected, and the same input with a pull-down", 17, AMBER_LIGHT, weight="bold"))
    L, R = 110, 840
    for row, (title, pulled) in enumerate([("floating: no resistor", False), ("with a 10 kΩ pull-down", True)]):
        T, B = 90 + row * 180, 230 + row * 180
        yv = lambda v, T=T, B=B: B - v / 5 * (B - T)
        parts.append(f'<rect x="{L}" y="{yv(3):.1f}" width="{R - L}" height="{yv(1.5) - yv(3):.1f}" fill="#4a5568" fill-opacity="0.35"/>')
        axes(parts, L, R, T, B, B, "", [(yv(1.5), "1.5 V"), (yv(3), "3 V"), (yv(5), "5 V")])
        parts.append(text(L + 6, T - 6, title, 13, GREEN if pulled else RED, "start", weight="bold"))
        random.seed(5)
        v, pts, reads = 1.8, [], []
        for k in range(200):
            if pulled:
                v = 0.02 + 0.01 * random.uniform(-1, 1)
            else:
                v = min(4.8, max(0.2, v + random.uniform(-0.45, 0.45) + 0.4 * math.sin(k / 6)))
            x = L + (R - L) * k / 199
            pts.append((x, yv(v)))
        parts.append(glow_line(pts, "#90cdf4" if not pulled else GREEN, 2.5))
        # sampled readings
        for k in range(0, 200, 25):
            x, y = pts[k]
            vv = 5 * (B - y) / (B - T)
            reading = "HIGH" if vv > 3 else ("LOW" if vv < 1.5 else "?")
            col = GREEN if reading == "HIGH" else ("#90cdf4" if reading == "LOW" else RED)
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{col}"/>')
            parts.append(text(x, B + 18, reading, 11, col, weight="bold"))
    parts.append(text(w / 2, 448, "grey band: neither HIGH nor LOW is guaranteed. Floating trace is illustrative.", 11, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Two voltage traces on an input pin, with readings taken at intervals. Floating, with nothing connected, the voltage wanders up and down through the grey band between 1.5 and 3 volts, and the readings flip between HIGH, LOW and uncertain at random. With a 10 kilohm pull-down, the voltage sits steady near 0 volts and every reading is LOW.")


# 2. The four states -----------------------------------------------------------------------------------------
def pull_states():
    w, h = 900, 440
    parts = [common_defs()]
    cases = [("Pull-down, open", "rests LOW", False, False), ("Pull-down, pressed", "reads HIGH", False, True),
             ("Pull-up, open", "rests HIGH", True, False), ("Pull-up, pressed", "reads LOW", True, True)]
    for k, (title, result, up, pressed) in enumerate(cases):
        x0 = 15 + (k % 2) * 440
        y0 = 15 + (k // 2) * 215
        parts.append(panel(x0, y0, 425, 200))
        cx = x0 + 212
        parts.append(text(cx, y0 + 30, title, 15, AMBER_LIGHT, weight="bold"))
        high = (pressed and not up) or (up and not pressed)
        rail_top, rail_bot = y0 + 60, y0 + 175
        parts.append(f'<line x1="{x0 + 40}" y1="{rail_top}" x2="{x0 + 385}" y2="{rail_top}" stroke="{RED}" stroke-width="3"/>')
        parts.append(text(x0 + 36, rail_top + 4, "5 V", 11, RED, "end", weight="bold"))
        parts.append(f'<line x1="{x0 + 40}" y1="{rail_bot}" x2="{x0 + 385}" y2="{rail_bot}" stroke="#90cdf4" stroke-width="3"/>')
        parts.append(text(x0 + 36, rail_bot + 4, "GND", 11, "#90cdf4", "end", weight="bold"))
        node_y = (rail_top + rail_bot) / 2
        px = x0 + 150
        # resistor to its rail
        ry0, ry1 = (rail_top, node_y) if up else (node_y, rail_bot)
        parts.append(f'<line x1="{px}" y1="{ry0}" x2="{px}" y2="{ry1}" stroke="{TEXT}" stroke-width="2"/>')
        parts.append(f'<rect x="{px - 9}" y="{(ry0 + ry1) / 2 - 18:.1f}" width="18" height="36" rx="7" fill="#d6b98c"/>')
        parts.append(text(px - 16, (ry0 + ry1) / 2 + 4, "10 kΩ", 11, MUTED, "end"))
        # button to the other rail
        bx = x0 + 260
        by0, by1 = (node_y, rail_bot) if up else (rail_top, node_y)
        parts.append(f'<line x1="{bx}" y1="{by0}" x2="{bx}" y2="{by0 + 12 if by0 < by1 else by0}" stroke="{TEXT}" stroke-width="2"/>')
        parts.append(f'<line x1="{bx}" y1="{by1 - 12}" x2="{bx}" y2="{by1}" stroke="{TEXT}" stroke-width="2"/>')
        if pressed:
            parts.append(f'<line x1="{bx}" y1="{by0 + 12}" x2="{bx}" y2="{by1 - 12}" stroke="{AMBER}" stroke-width="4"/>')
        else:
            parts.append(f'<line x1="{bx}" y1="{by0 + 12}" x2="{bx + 22}" y2="{by1 - 16}" stroke="{TEXT}" stroke-width="3"/>')
        parts.append(text(bx + 30, (by0 + by1) / 2 + 4, "button", 11, MUTED, "start"))
        # node to pin
        parts.append(f'<line x1="{px}" y1="{node_y}" x2="{bx}" y2="{node_y}" stroke="{TEXT}" stroke-width="2"/>')
        parts.append(f'<circle cx="{px}" cy="{node_y}" r="4" fill="{TEXT}"/>')
        parts.append(f'<line x1="{bx}" y1="{node_y}" x2="{x0 + 330}" y2="{node_y}" stroke="{TEXT}" stroke-width="2"/>')
        parts += pill(x0 + 355, node_y, "HIGH" if high else "LOW", GREEN if high else "#2b6cb0", size=12, h=26, wpx=58)
        parts.append(text(cx, y0 + 196, result, 12, GREEN if high else "#90cdf4", weight="bold"))
    return svg(w, h, "\n".join(parts), "Four panels. Pull-down, button open: a 10 kilohm resistor ties the pin to ground and it rests LOW. Pull-down, pressed: the button connects the pin to 5 volts and it reads HIGH. Pull-up, button open: the resistor ties the pin to 5 volts and it rests HIGH. Pull-up, pressed: the button connects the pin to ground and it reads LOW.")


# 3. Sizing the resistor -------------------------------------------------------------------------------------
def sizing():
    w, h = 900, 420
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Current wasted while the button is held, 5 V across the pull resistor", 17, AMBER_LIGHT, weight="bold"))
    base = 320
    rows = [(100, "100 Ω", "too strong: wastes current", RED),
            (10e3, "10 kΩ", "the everyday default", GREEN),
            (35e3, "20–50 kΩ", "the Uno's built-in pull-up", "#38b2ac"),
            (10e6, "10 MΩ", "too weak: noise wins", AMBER)]
    for k, (r, lab, sub, col) in enumerate(rows):
        x = 110 + k * 190
        i_ma = 5 / r * 1000
        hgt = max(6, (math.log10(i_ma) + 4) / (math.log10(50) + 4) * 210)
        parts += box3d(x, base, 90, 40, hgt, col)
        if r == 35e3:
            cur = f"{5 / 50e3 * 1000:.1f}–{5 / 20e3 * 1000:.2f} mA"
        elif i_ma >= 1:
            cur = f"{i_ma:g} mA"
        elif i_ma >= 0.1:
            cur = f"{i_ma:g} mA"
        else:
            cur = f"{i_ma * 1000:g} µA"
        parts.append(text(x + 60, base - hgt - 26, cur, 15, TEXT, weight="bold"))
        parts.append(text(x + 45, base + 28, lab, 15, TEXT, weight="bold"))
        parts.append(text(x + 45, base + 46, sub, 11, shade(col, 0.25), italic=True))
    parts.append(text(w / 2, 82, "bar height on a log scale", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Four 3D bars of the current wasted through a pull resistor while the button is held, on a log scale. 100 ohms wastes 50 milliamps, too strong. 10 kilohms wastes 0.5 milliamps, the everyday default. The Uno's built-in 20 to 50 kilohm pull-up wastes 0.1 to 0.25 milliamps. 10 megohms wastes half a microamp but is so weak that noise wins.")


FIGURES = {"floating.svg": floating, "pull_states.svg": pull_states, "sizing.svg": sizing}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
