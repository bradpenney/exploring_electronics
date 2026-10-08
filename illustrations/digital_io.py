#!/usr/bin/env python3
"""Figures for docs/digital_io.md.

Sources:
- ATmega328P datasheet input thresholds at a 5 V supply: HIGH above 0.6 VCC
  (3 V), LOW below 0.3 VCC (1.5 V), as the article states.
- The article's own example values (a sag to 4.6 V still reads HIGH).

Usage:
    python3 illustrations/digital_io.py
"""

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, box3d,  # noqa: E402
                     common_defs, led, panel, pill, render_all, shade, svg, text)

OUT = HERE.parent / "docs" / "images" / "digital_io"
VCC = 5.0
V_HIGH, V_LOW = 0.6 * VCC, 0.3 * VCC


# 1. What a pin reads -------------------------------------------------------------------------------
def thresholds():
    w, h = 900, 440
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "What an Uno's input pin reads, by voltage", 17, AMBER_LIGHT, weight="bold"))
    x0, base, bw, scale = 300, 380, 120, 60
    zones = [(0, V_LOW, "#2b6cb0", "LOW", "#ffffff"), (V_LOW, V_HIGH, "#4a5568", "not guaranteed", "#e2e8f0"),
             (V_HIGH, VCC, GREEN, "HIGH", "#1a1a1a")]
    for k, (a, b, col, lab, fg) in enumerate(zones):
        parts += box3d(x0, base - a * scale, bw, 50, (b - a) * scale, col, shadow=(k == 0))
        parts.append(text(x0 + bw / 2, base - (a + b) / 2 * scale + 5, lab, 14, fg, weight="bold"))
    for v in (0, V_LOW, V_HIGH, VCC):
        y = base - v * scale
        parts.append(text(x0 - 14, y + 4, f"{v:g} V", 13, TEXT, "end", weight="bold"))
    marks = [(4.6, "4.6 V (a sagging supply): still HIGH", GREEN),
             (0.3, "0.3 V of noise on a LOW: still LOW", "#90cdf4"),
             (2.2, "2.2 V: could read either way", RED)]
    for v, lab, col in marks:
        y = base - v * scale
        parts.append(f'<line x1="{x0 + bw + 40}" y1="{y:.1f}" x2="{x0 + bw + 70}" y2="{y:.1f}" stroke="{col}" stroke-width="3"/>')
        parts.append(f'<circle cx="{x0 + bw + 40}" cy="{y:.1f}" r="5" fill="{col}"/>')
        parts.append(text(x0 + bw + 78, y + 5, lab, 13, col, "start", weight="bold"))
    parts.append(text(140, 200, "above 3 V", 13, MUTED, italic=True))
    parts.append(text(140, 218, "(60% of 5 V)", 12, MUTED, italic=True))
    parts.append(text(140, 320, "below 1.5 V", 13, MUTED, italic=True))
    parts.append(text(140, 338, "(30% of 5 V)", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "A 3D column from 0 to 5 volts in three bands: below 1.5 volts reads LOW, above 3 volts reads HIGH, and the band between is not guaranteed. A supply sagging to 4.6 volts still reads HIGH, 0.3 volts of noise on a LOW still reads LOW, and 2.2 volts could read either way.")


# 2. Output drives, input listens ------------------------------------------------------------------------
def pin_jobs():
    w, h = 900, 420
    parts = [common_defs(), panel(15, 15, 425, h - 30), panel(460, 15, 425, h - 30)]
    # OUTPUT
    parts.append(text(227, 50, "OUTPUT: the pin pushes current", 16, AMBER_LIGHT, weight="bold"))
    parts += box3d(60, 300, 110, 40, 150, "#2d3748")
    parts.append(text(115, 200, "pin 3", 14, "#ffffff", weight="bold"))
    parts.append(text(115, 220, "HIGH = 5 V", 12, GREEN, weight="bold"))
    parts.append(f'<path d="M190,210 L270,210" stroke="{AMBER_LIGHT}" stroke-width="5" marker-end="url(#arrow)"/>')
    parts.append(f'<rect x="275" y="198" width="50" height="22" rx="9" fill="#d6b98c"/>')
    parts.append(text(300, 245, "resistor", 11, MUTED))
    parts += led(370, 209, "#fc8181", lit=True, r=16)
    parts.append(text(370, 268, "LED lit", 11, MUTED))
    parts.append(text(227, 345, "current flows out of the pin,", 12, TEXT))
    parts.append(text(227, 362, "through the LED, to ground", 12, TEXT))
    # INPUT
    parts.append(text(672, 50, "INPUT: the pin only listens", 16, AMBER_LIGHT, weight="bold"))
    parts += box3d(505, 300, 110, 40, 150, "#2d3748")
    parts.append(text(560, 200, "pin 2", 14, "#ffffff", weight="bold"))
    parts.append(text(560, 220, "reads HIGH", 12, GREEN, weight="bold"))
    parts.append(f'<path d="M760,210 L640,210" stroke="#90cdf4" stroke-width="2" stroke-dasharray="5 5"/>')
    parts.append(text(700, 172, "voltage, almost no current", 11, "#90cdf4", weight="bold"))
    parts.append(f'<rect x="760" y="186" width="80" height="48" rx="8" fill="#4a5568"/>')
    parts.append(text(800, 215, "button", 12, "#ffffff", weight="bold"))
    parts.append(text(672, 345, "the pin measures the voltage", 12, TEXT))
    parts.append(text(672, 362, "something else holds it at", 12, TEXT))
    return svg(w, h, "\n".join(parts), "Two panels. OUTPUT: pin 3, set HIGH at 5 volts, pushes current through a resistor and lights an LED. INPUT: pin 2 only listens, measuring the voltage a button holds it at while drawing almost no current.")


# 3. Read, decide, drive --------------------------------------------------------------------------------------
def read_decide_drive():
    w, h = 900, 440
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "The heartbeat of a microcontroller program, inside loop()", 17, AMBER_LIGHT, weight="bold"))
    cx, cy, r = 450, 245, 125
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#4a5568" stroke-width="14"/>')
    steps = [("Read inputs", "digitalRead(2)", -90, "#2b6cb0"), ("Decide", "if (pressed) ...", 30, AMBER),
             ("Drive outputs", "digitalWrite(3, HIGH)", 150, GREEN)]
    for name, code, ang, col in steps:
        a = math.radians(ang)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="46" fill="{col}"/>')
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="46" fill="url(#gloss)" opacity="0.4"/>')
        parts.append(text(x, y + 5, name.split()[0], 14, "#ffffff" if col != AMBER else "#1a1a1a", weight="bold"))
        if len(name.split()) > 1:
            parts.append(text(x, y + 21, name.split()[1], 12, "#ffffff" if col != AMBER else "#1a1a1a"))
        tx = x + (60 if abs(math.cos(a)) < 0.3 else (0 if math.cos(a) > 0 else 0))
        ty = y + (5 if abs(math.cos(a)) < 0.3 else 66)
        parts.append(text(tx, ty, code, 12, MUTED, "start" if abs(math.cos(a)) < 0.3 else "middle", italic=True))
    for ang in (-30, 90, 210):
        a = math.radians(ang)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        da = math.radians(ang + 90)
        parts.append(f'<path d="M{x - 10 * math.cos(da):.1f},{y - 10 * math.sin(da):.1f} l{20 * math.cos(da):.1f},{20 * math.sin(da):.1f}" stroke="{AMBER_LIGHT}" stroke-width="4" marker-end="url(#arrow)"/>')
    parts.append(text(cx, cy + 5, "then again", 13, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "A ring of three steps that repeats forever inside loop(): read the inputs, for example digitalRead on the button's pin; decide what to do, for example if the button is pressed; drive the outputs, for example digitalWrite to an LED; then again.")


FIGURES = {"thresholds.svg": thresholds, "pin_jobs.svg": pin_jobs, "read_decide_drive.svg": read_decide_drive}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
