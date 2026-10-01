#!/usr/bin/env python3
"""Figures for docs/temperature_sensors.md.

sensor_types.svg replaces the old mermaid (temperature -> thermistor / analog IC
/ digital IC -> what each one hands you). Parts drawn: a bead thermistor, the
MCP9700A analog IC (TO-92), and the DS18B20 digital IC (also TO-92), matching
the article's cards.

Usage:
    python3 illustrations/temperature_sensors.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, TEXT, common_defs,  # noqa: E402
                     panel, render_all, shade, svg, text)

OUT = HERE.parent / "docs" / "images" / "temperature_sensors"


def to92(cx, base, label):
    """TO-92 package: black half-cylinder body with three legs."""
    gid = f"to92{cx}"
    out = [f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4a5568"/>'
           f'<stop offset="0.3" stop-color="#718096"/><stop offset="1" stop-color="#0d1117"/></linearGradient>',
           f'<ellipse cx="{cx}" cy="{base + 4}" rx="34" ry="6" fill="#000" fill-opacity="0.4"/>']
    for dx in (-12, 0, 12):
        out.append(f'<rect x="{cx + dx - 2}" y="{base - 60}" width="4" height="62" fill="#cbd5e0"/>')
        out.append(f'<rect x="{cx + dx - 2}" y="{base - 60}" width="1.5" height="62" fill="#ffffff" fill-opacity="0.6"/>')
    out.append(f'<path d="M{cx - 24},{base - 58} L{cx - 24},{base - 110} A24,10 0 0 1 {cx + 24},{base - 110} '
               f'L{cx + 24},{base - 58} A24,10 0 0 1 {cx - 24},{base - 58} Z" fill="url(#{gid})"/>')
    out.append(f'<ellipse cx="{cx}" cy="{base - 110}" rx="24" ry="10" fill="#2d3748"/>')
    out.append(f'<rect x="{cx - 24}" y="{base - 100}" width="48" height="38" fill="url(#gloss)" opacity="0.5"/>')
    out.append(text(cx, base - 80, label, 9, "#cbd5e0", weight="bold"))
    return out


def thermistor(cx, base):
    out = [f'<ellipse cx="{cx}" cy="{base + 4}" rx="30" ry="6" fill="#000" fill-opacity="0.4"/>']
    for dx in (-8, 8):
        out.append(f'<path d="M{cx + dx},{base} L{cx + dx},{base - 70} Q{cx + dx},{base - 82} {cx + dx * 0.4},{base - 88}" '
                   f'fill="none" stroke="#cbd5e0" stroke-width="3"/>')
    out.append(f'<ellipse cx="{cx}" cy="{base - 100}" rx="20" ry="16" fill="url(#bead)"/>')
    return out


def sensor_types():
    w, h = 780, 470
    extra = ('<radialGradient id="bead" cx="35%" cy="30%" r="75%"><stop offset="0" stop-color="#fbd38d"/>'
             '<stop offset="0.5" stop-color="#b7791f"/><stop offset="1" stop-color="#4a2c0a"/></radialGradient>')
    parts = [common_defs(extra)]
    parts.append(text(w / 2, 34, "Temperature in: three ways to get it out", 16, TEXT, weight="bold"))
    cols = [(135, "Thermistor", "resistance changes", "steeply and non-linearly", "you build a divider and do the maths"),
            (390, "Analog IC (MCP9700A)", "voltage changes", "linearly: 10 mV per °C", "read it with an analog pin"),
            (645, "Digital IC (DS18B20)", "the sensor does the maths", "and sends a number", "over a single data wire")]
    for i, (cx, name, a, b, c) in enumerate(cols):
        parts.append(panel(cx - 120, 52, 240, 400))
        parts.append(text(cx, 82, name, 15, AMBER_LIGHT if i == 1 else TEXT, weight="bold"))
        if i == 0:
            parts += thermistor(cx, 230)
            # an ohmmeter-style dial
            parts.append(f'<path d="M{cx - 50},300 A50,50 0 0 1 {cx + 50},300" fill="none" stroke="#4a5568" stroke-width="10" stroke-linecap="round"/>')
            parts.append(f'<path d="M{cx - 50},300 A50,50 0 0 1 {cx + 20},253" fill="none" stroke="{AMBER}" stroke-width="10" stroke-linecap="round"/>')
            parts.append(text(cx, 296, "Ω", 20, TEXT, weight="bold"))
        elif i == 1:
            parts += to92(cx, 230, "9700A")
            pts = " ".join(f"{cx - 55 + k * 11},{310 - k * 6}" for k in range(11))
            parts.append(f'<polyline points="{pts}" fill="none" stroke="{GREEN}" stroke-width="4" stroke-linecap="round"/>')
            parts.append(f'<line x1="{cx - 60}" y1="315" x2="{cx + 60}" y2="315" stroke="#4a5568" stroke-width="2"/>')
            parts.append(text(cx + 64, 262, "V", 14, GREEN, "start", "bold"))
        else:
            parts += to92(cx, 230, "18B20")
            for k, bit in enumerate("10110100"):
                x = cx - 60 + k * 15
                hgt = 26 if bit == "1" else 6
                parts.append(f'<rect x="{x}" y="{306 - hgt}" width="11" height="{hgt}" rx="2" fill="{AMBER if bit == "1" else "#4a5568"}"/>')
            parts.append(text(cx, 325, "a number, bit by bit", 11, MUTED, italic=True))
        parts.append(text(cx, 360, a, 13, TEXT, weight="bold"))
        parts.append(text(cx, 380, b, 13, TEXT))
        parts.append(text(cx, 420, c, 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Three temperature sensors: a bead thermistor whose resistance changes, an MCP9700A analog IC whose voltage changes linearly, and a DS18B20 digital IC that sends a number over a data wire")


FIGURES = {"sensor_types.svg": sensor_types}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
