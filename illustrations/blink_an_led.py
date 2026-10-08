#!/usr/bin/env python3
"""Figures for docs/blink_an_led.md.

Sources: the article's own sketch (delay(1000) on and off) and wiring (longer
leg is the anode; the rim has a flat edge on the cathode side; 220 ohm resistor).

Usage:
    python3 illustrations/blink_an_led.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, common_defs,  # noqa: E402
                     led, panel, render_all, svg, text)
from ac_dc import axes, glow_line  # noqa: E402

OUT = HERE.parent / "docs" / "images" / "blink_an_led"


# 1. What the pin does over time ---------------------------------------------------------------------
def blink_timing():
    w, h = 900, 400
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Pin 3 over four seconds of the Blink sketch", 17, AMBER_LIGHT, weight="bold"))
    L, R, T, B = 110, 820, 120, 280
    xs = lambda t: L + t / 4.0 * (R - L)
    hi, lo = T + 10, B - 10
    axes(parts, L, R, T, B, B, "", [(hi, "5 V"), (lo, "0 V")])
    pts = []
    for k in range(4):
        v = hi if k % 2 == 0 else lo
        pts += [(xs(k), v), (xs(k + 1), v)]
    parts.append(glow_line(pts, "#90cdf4", 3))
    for k in range(4):
        x = (xs(k) + xs(k + 1)) / 2
        on = k % 2 == 0
        parts += led(x, 90, "#fc8181", lit=on, r=13)
        line = "digitalWrite(3, HIGH);" if on else "digitalWrite(3, LOW);"
        parts.append(text(x, B + 26, line, 11, AMBER_LIGHT if on else MUTED))
        parts.append(text(x, B + 44, "delay(1000);", 11, MUTED))
    for t in range(5):
        parts.append(text(xs(t), B + 70, f"{t} s", 11, MUTED))
    return svg(w, h, "\n".join(parts), "A square wave on pin 3 over four seconds: 5 volts for one second while digitalWrite HIGH and delay(1000) run, then 0 volts for one second for digitalWrite LOW and delay(1000), repeating. An LED above each second shows it lit, dark, lit, dark.")


# 2. Which leg is which ------------------------------------------------------------------------------------
def led_legs():
    w, h = 900, 400
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Telling an LED's legs apart", 17, AMBER_LIGHT, weight="bold"))
    cx = 300
    # body
    parts.append(f'<ellipse cx="{cx}" cy="185" rx="48" ry="12" fill="#c53030"/>')
    parts.append(f'<path d="M{cx - 40},185 L{cx - 40},120 A40,40 0 0 1 {cx + 40},120 L{cx + 40},185 Z" fill="#fc8181" fill-opacity="0.9"/>')
    parts.append(f'<path d="M{cx - 40},185 L{cx - 40},120 A40,40 0 0 1 {cx + 40},120 L{cx + 40},185 Z" fill="url(#gloss)" opacity="0.5"/>')
    # flat edge on the cathode (right) side of the rim
    parts.append(f'<rect x="{cx + 40}" y="173" width="8" height="24" fill="#1e1e1e"/>')
    # legs: anode long (left), cathode short (right)
    parts.append(f'<rect x="{cx - 22}" y="195" width="6" height="150" fill="#cbd5e0"/>')
    parts.append(f'<rect x="{cx + 16}" y="195" width="6" height="110" fill="#cbd5e0"/>')
    parts.append(text(cx - 40, 340, "anode (+)", 14, GREEN, "end", weight="bold"))
    parts.append(text(cx - 40, 358, "longer leg: toward the pin", 12, MUTED, "end", italic=True))
    parts.append(text(cx + 40, 300, "cathode (−)", 14, "#90cdf4", "start", weight="bold"))
    parts.append(text(cx + 40, 318, "shorter leg: toward GND", 12, MUTED, "start", italic=True))
    parts.append(f'<line x1="{cx + 52}" y1="185" x2="{cx + 110}" y2="150" stroke="{MUTED}"/>')
    parts.append(text(cx + 116, 148, "flat edge on the rim:", 13, AMBER_LIGHT, "start", weight="bold"))
    parts.append(text(cx + 116, 166, "the cathode side, even when", 12, MUTED, "start", italic=True))
    parts.append(text(cx + 116, 182, "the legs have been trimmed", 12, MUTED, "start", italic=True))
    # symbol
    sx, sy = 690, 260
    parts.append(f'<line x1="{sx - 80}" y1="{sy}" x2="{sx - 20}" y2="{sy}" stroke="{TEXT}" stroke-width="3"/>')
    parts.append(f'<path d="M{sx - 20},{sy - 22} L{sx - 20},{sy + 22} L{sx + 18},{sy} Z" fill="{TEXT}"/>')
    parts.append(f'<line x1="{sx + 18}" y1="{sy - 22}" x2="{sx + 18}" y2="{sy + 22}" stroke="{TEXT}" stroke-width="4"/>')
    parts.append(f'<line x1="{sx + 18}" y1="{sy}" x2="{sx + 80}" y2="{sy}" stroke="{TEXT}" stroke-width="3"/>')
    parts.append(text(sx - 80, sy - 14, "anode", 12, GREEN, "start"))
    parts.append(text(sx + 80, sy - 14, "cathode", 12, "#90cdf4", "end"))
    parts.append(text(sx, sy + 56, "the symbol's bar is the cathode", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "A red LED with its two legs. The longer leg is the anode, the positive side, which goes toward the pin; the shorter leg is the cathode, which goes toward ground. A flat edge on the rim marks the cathode side even when the legs have been trimmed. Beside it, the LED schematic symbol: a triangle pointing to a bar, with the bar on the cathode side.")


FIGURES = {"blink_timing.svg": blink_timing, "led_legs.svg": led_legs}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
