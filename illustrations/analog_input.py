#!/usr/bin/env python3
"""Figures for docs/analog_input.md.

analog_read.svg replaces the old mermaid (analogRead -> print raw / convert). It
uses the article's own maths: a 10-bit ADC on 0-5 V, voltage = value / 1024 * 5,
and the MCP9700A's 500 mV offset at 10 mV per degree C. The example reading is
computed, not typed: a sensor at 22.4 C outputs 0.724 V, which the ADC reports
as step 148, which converts back to about 22.3 C (the half-degree resolution the
article's practice problem works out).

Usage:
    python3 illustrations/analog_input.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, MUTED, TEXT, box3d, common_defs,  # noqa: E402
                     panel, pill, render_all, svg, text)

OUT = HERE.parent / "docs" / "images" / "analog_input"

TEMP = 22.4
VOUT = 0.5 + 0.010 * TEMP                 # MCP9700A: 500 mV + 10 mV/C
STEP = int(VOUT / 5.0 * 1024)             # what analogRead() returns
V_BACK = STEP / 1024.0 * 5.0              # the article's conversion
T_BACK = (V_BACK - 0.5) * 100


def analog_read():
    w, h = 780, 440
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "analogRead() turns a voltage into a step number from 0 to 1023", 15, TEXT, weight="bold"))
    # 3D staircase: 0-5 V rising in steps (drawn as 16 coarse steps; the real ADC has 1,024)
    x0, base, sw, n = 50, 300, 24, 16
    for i in range(n):
        hgt = 14 + i * 9
        hl = i == int(VOUT / 5.0 * n)
        parts += box3d(x0 + i * sw, base, sw - 2, 16, hgt, AMBER if hl else "#4a5568", shadow=(i == 0))
    parts.append(text(x0, base + 30, "0 V → step 0", 12, MUTED, "start"))
    parts.append(text(x0 + n * sw + 14, base + 30, "5 V → step 1023", 12, MUTED, "end"))
    parts.append(text(x0 + n * sw / 2 + 10, base + 52, "1,024 steps, each about 4.9 mV (16 drawn here)", 12, MUTED, italic=True))
    hx = x0 + int(VOUT / 5.0 * n) * sw + sw / 2
    parts.append(f'<line x1="{hx}" y1="{base - 70}" x2="{hx}" y2="118" stroke="{AMBER}" stroke-width="2" stroke-dasharray="5 4"/>')
    parts += pill(hx + 40, 100, f"A0 reads {VOUT:.3f} V", "#d97706", "#1a1a1a", size=13, h=32)
    # outputs
    ox = 640
    parts.append(f'<path d="M{x0 + n * sw + 30},210 C560,210 560,150 {ox - 95},150" fill="none" stroke="{AMBER}" stroke-width="3" marker-end="url(#arrow)"/>')
    parts.append(f'<path d="M{x0 + n * sw + 30},230 C560,230 560,300 {ox - 95},300" fill="none" stroke="{AMBER}" stroke-width="3" marker-end="url(#arrow)"/>')
    parts += pill(ox, 150, f"Serial.print → {STEP}", "#2d3748", size=14, h=44, wpx=180)
    parts.append(text(ox, 190, "watch the raw number live", 12, MUTED, italic=True))
    parts += pill(ox, 300, f"→ {V_BACK:.3f} V → {T_BACK:.1f} °C", "#2f855a", size=14, h=44, wpx=200)
    parts.append(text(ox, 340, "convert to voltage, then temperature", 12, MUTED, italic=True))
    parts.append(text(w / 2, 400, f"A sensor at {TEMP} °C outputs {VOUT:.3f} V; the ADC rounds it down to step {STEP}, about half a degree of resolution",
                      12, AMBER_LIGHT, italic=True))
    return svg(w, h, "\n".join(parts), f"A 3D staircase of ADC steps from 0 to 5 volts. A reading of {VOUT:.3f} volts lands on step {STEP}, which is printed raw or converted back to {V_BACK:.3f} volts and {T_BACK:.1f} degrees Celsius")


FIGURES = {"analog_read.svg": analog_read}

if __name__ == "__main__":
    print(f"{TEMP} C -> {VOUT:.4f} V -> step {STEP} -> {V_BACK:.4f} V -> {T_BACK:.2f} C")
    render_all(FIGURES, OUT)
