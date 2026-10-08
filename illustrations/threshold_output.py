#!/usr/bin/env python3
"""Figures for docs/threshold_output.md.

threshold_ladder.svg replaces the old mermaid decision ladder. It follows the
article's actual sketch, which tests from the bottom up:
    temperature < baseline + 4  -> stage 0 (all off)
    else < baseline + 6         -> stage 1 (one LED)
    else < baseline + 8         -> stage 2 (two LEDs)
    else                        -> stage 3 (all three)
with baselineTemp = 20.0 as in the sketch. (The old mermaid tested top-down with
>=, which did not match the code.)

Usage:
    python3 illustrations/threshold_output.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER_LIGHT, MUTED, TEXT, box3d, common_defs, led,  # noqa: E402
                     panel, render_all, svg, text)

OUT = HERE.parent / "docs" / "images" / "threshold_output"

BASELINE = 20.0
BANDS = [(0, 4, 0), (4, 6, 1), (6, 8, 2), (8, None, 3)]  # (from, to, LEDs lit), offsets above baseline
COLORS = ["#4a5568", "#d69e2e", "#dd6b20", "#c53030"]


def threshold_ladder():
    w, h = 780, 470
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, f"One reading, four stages (baseline = {BASELINE:g} °C)", 16, TEXT, weight="bold"))
    x0, base, sw = 70, 380, 160
    for i, (lo, hi, lit) in enumerate(BANDS):
        hgt = 50 + i * 52
        x = x0 + i * sw
        parts += box3d(x, base, sw - 12, 40, hgt, COLORS[i])
        rng = (f"below {BASELINE + 4:g} °C" if i == 0 else
               f"{BASELINE + lo:g} to {BASELINE + hi:g} °C" if hi else f"{BASELINE + lo:g} °C and up")
        parts.append(text(x + (sw - 12) / 2, base - hgt + 26, f"Stage {i}", 15, "#ffffff", weight="bold"))
        parts.append(text(x + (sw - 12) / 2, base - hgt + 46, rng, 12, "#ffffff"))
        for k in range(3):
            parts += led(x + 30 + k * 44, base - hgt - 58, "#fc8181", lit=k < lit, r=10, glow=0.62)
    # the order the sketch checks: bottom up
    parts.append(f'<path d="M{x0 + 60},{base + 30} L{x0 + 3 * sw + 60},{base + 30}" fill="none" stroke="{AMBER_LIGHT}" '
                 f'stroke-width="3" marker-end="url(#arrow)"/>')
    parts.append(text(w / 2, base + 56, "the sketch tests the lowest band first; the first test that passes wins", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "A 3D staircase of four stages above a 20 degree baseline: below 24 degrees all LEDs off, 24 to 26 one LED, 26 to 28 two LEDs, 28 and up all three, tested from the lowest band up")


import math  # noqa: E402
from style3d import AMBER, panel as _panel  # noqa: E402
from ac_dc import axes, glow_line  # noqa: E402


def _lit(t):
    off = t - BASELINE
    for lo, hi, n in BANDS:
        if hi is None or off < hi:
            return n
    return 3


# 2. A warming and cooling trace, with the LEDs it lights ------------------------------------------------
def warm_trace():
    w, h = 900, 480
    parts = [common_defs(), _panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "A hand warming the sensor, and the LEDs the sketch lights", 17, AMBER_LIGHT, weight="bold"))
    L, R, T, B = 110, 840, 90, 330
    yt = lambda t: B - (t - 18) / (32 - 18) * (B - T)
    xs = lambda s: L + s / 60 * (R - L)
    for lo, hi, n in BANDS:
        y0 = yt(BASELINE + lo)
        y1 = yt(BASELINE + (hi if hi is not None else 12))
        parts.append(f'<rect x="{L}" y="{y1:.1f}" width="{R - L}" height="{y0 - y1:.1f}" fill="{COLORS[n]}" fill-opacity="0.18"/>')
        parts.append(text(R + 6, (y0 + y1) / 2 + 4, f"{n} lit", 11, MUTED, "start"))
    axes(parts, L, R, T, B, B, "", [(yt(t), f"{t} °C") for t in (20, 24, 26, 28, 30)])
    temp = lambda s: BASELINE + 10 * (1 - math.exp(-s / 8)) if s < 30 else BASELINE + 10 * (1 - math.exp(-30 / 8)) * math.exp(-(s - 30) / 10)
    pts = [(xs(s / 4), yt(temp(s / 4))) for s in range(241)]
    parts.append(glow_line(pts, "#f6ad55", 3))
    for s in range(0, 61, 6):
        n = _lit(temp(s))
        for j in range(3):
            parts += led(xs(s) - 14 + j * 14, 372, ["#ecc94b", "#ed8936", "#e53e3e"][j], lit=j < n, r=6, glow=0.6)
    for s in (0, 15, 30, 45, 60):
        parts.append(text(xs(s), 405, f"{s} s", 11, MUTED))
    parts.append(text(w / 2, 440, "baseline 20 °C as in the sketch; the warming curve is illustrative", 11, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "A temperature trace over 60 seconds that climbs from the 20 degree baseline toward 30 degrees while a hand holds the sensor, then falls back. Shaded bands mark the sketch's stages: below 24 degrees no LEDs, 24 to 26 one, 26 to 28 two, above 28 all three. A row of three LEDs under the trace every six seconds shows the stage lighting up and going out again.")


FIGURES = {"threshold_ladder.svg": threshold_ladder, "warm_trace.svg": warm_trace}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
