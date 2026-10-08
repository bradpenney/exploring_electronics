#!/usr/bin/env python3
"""Figures for docs/vacuum_tubes.md.

Sources:
- Wikipedia "Vacuum tube": thermionic emission; Edison effect 1883; Fleming
  valve 1904; oxide-coated cathodes at about 700 C (dull red); plate voltages
  in the hundreds of volts.
- Wikipedia "Triode": de Forest's Audion patent, 29 January 1907; grid held
  slightly negative to the cathode; a small grid voltage controls a much
  larger plate current.
- Wikipedia "12AX7": RCA, released 15 September 1947; heater 12.6 V at 150 mA
  or 6.3 V at 300 mA; amplification factor 100; max plate 300 V, 1 W per
  section.
- Wikipedia "Transistor": first working transistor, Bell Labs, December 1947.
The grid-control panels are qualitative (no currents plotted).

Usage:
    python3 illustrations/vacuum_tubes.py
"""

import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, box3d,  # noqa: E402
                     common_defs, panel, pill, render_all, shade, svg, text)

OUT = HERE.parent / "docs" / "images" / "vacuum_tubes"
BLUE = "#4299e1"
GLASS = ('<linearGradient id="vt-glass" x1="0" y1="0" x2="1" y2="0">'
         '<stop offset="0" stop-color="#cbd5e0" stop-opacity="0.32"/>'
         '<stop offset="0.25" stop-color="#ffffff" stop-opacity="0.10"/>'
         '<stop offset="0.75" stop-color="#cbd5e0" stop-opacity="0.06"/>'
         '<stop offset="1" stop-color="#cbd5e0" stop-opacity="0.30"/></linearGradient>'
         '<linearGradient id="vt-metal" x1="0" y1="0" x2="1" y2="0">'
         '<stop offset="0" stop-color="#4a5568"/><stop offset="0.3" stop-color="#cbd5e0"/>'
         '<stop offset="0.6" stop-color="#718096"/><stop offset="1" stop-color="#2d3748"/></linearGradient>'
         '<radialGradient id="vt-heat" r="50%"><stop offset="0" stop-color="#ff8a3d" stop-opacity="0.9"/>'
         '<stop offset="1" stop-color="#ff8a3d" stop-opacity="0"/></radialGradient>')


def _electron(x, y, r=4):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="url(#eball)"/>'


def _envelope(parts, cx, top, bot, half):
    parts.append(f'<ellipse cx="{cx + 8}" cy="{bot + 26}" rx="{half + 14}" ry="9" fill="#000" fill-opacity="0.45"/>')
    parts.append(f'<path d="M{cx - half},{bot} L{cx - half},{top + half} A{half},{half} 0 0 1 {cx + half},{top + half} '
                 f'L{cx + half},{bot} Z" fill="url(#vt-glass)" stroke="#cbd5e0" stroke-opacity="0.55" stroke-width="2"/>')
    parts.append(f'<rect x="{cx - half - 4}" y="{bot}" width="{2 * half + 8}" height="22" rx="5" fill="#1a1a1a"/>')
    for k in range(-2, 3):
        parts.append(f'<rect x="{cx + k * 14 - 2}" y="{bot + 22}" width="4" height="16" fill="#a0aec0"/>')


# 1. Anatomy -----------------------------------------------------------------------------------
def anatomy():
    w, h = 900, 560
    parts = [common_defs(GLASS), panel(15, 15, w - 30, h - 30)]
    cx, top, bot, half = 450, 60, 460, 120
    _envelope(parts, cx, top, bot, half)
    # plate: an open metal box seen from the front (two side walls)
    parts.append(f'<rect x="{cx - 92}" y="150" width="30" height="250" rx="4" fill="url(#vt-metal)"/>')
    parts.append(f'<rect x="{cx + 62}" y="150" width="30" height="250" rx="4" fill="url(#vt-metal)"/>')
    # grid: a helix of fine wire around the cathode
    for k in range(13):
        y = 165 + k * 18
        parts.append(f'<ellipse cx="{cx}" cy="{y}" rx="34" ry="5" fill="none" stroke="#e2e8f0" stroke-width="1.6" stroke-opacity="0.85"/>')
    parts.append(f'<line x1="{cx - 34}" y1="160" x2="{cx - 34}" y2="400" stroke="#e2e8f0" stroke-width="2"/>')
    parts.append(f'<line x1="{cx + 34}" y1="160" x2="{cx + 34}" y2="400" stroke="#e2e8f0" stroke-width="2"/>')
    # cathode sleeve glowing, with heater inside
    parts.append(f'<ellipse cx="{cx}" cy="280" rx="40" ry="130" fill="url(#vt-heat)"/>')
    parts.append(f'<rect x="{cx - 9}" y="170" width="18" height="225" rx="6" fill="#c05621"/>')
    parts.append(f'<rect x="{cx - 9}" y="170" width="18" height="225" rx="6" fill="url(#gloss)" opacity="0.5"/>')
    random.seed(3)
    for _ in range(26):
        side = random.choice((-1, 1))
        x = cx + side * random.uniform(14, 58)
        y = random.uniform(180, 390)
        parts.append(_electron(x, y, 3.2))
    # leads to pins
    for dx in (-77, -20, 0, 20, 77):
        parts.append(f'<line x1="{cx + dx}" y1="400" x2="{cx + dx * 0.36:.1f}" y2="{bot}" stroke="#a0aec0" stroke-width="2"/>')
    def callout(x1, y1, x2, y2, label, sub, anchor):
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{MUTED}" stroke-width="1.5"/>')
        parts.append(f'<circle cx="{x1}" cy="{y1}" r="4" fill="{AMBER_LIGHT}"/>')
        dx = -8 if anchor == "end" else 8
        parts.append(text(x2 + dx, y2 - 4, label, 15, AMBER_LIGHT, anchor, weight="bold"))
        parts.append(text(x2 + dx, y2 + 14, sub, 12, MUTED, anchor, italic=True))
    callout(cx - 4, 300, 250, 330, "Cathode and heater", "heated until it boils off electrons", "end")
    callout(cx - 34, 210, 250, 210, "Grid", "a fine wire mesh: the control", "end")
    callout(cx - 78, 150, 250, 110, "Plate (anode)", "the most positive electrode", "end")
    callout(cx + 110, 120, 680, 110, "Glass envelope", "air pumped out: a vacuum", "start")
    callout(cx + 40, 330, 680, 330, "Electrons", "crossing the vacuum to the plate", "start")
    callout(cx + 42, bot + 30, 680, 470, "Pins", "heater, cathode, grid, plate", "start")
    return svg(w, h, "\n".join(parts), "A 3D triode inside a glass envelope with the air pumped out. In the centre, a glowing orange cathode sleeve with a heater inside it boils off electrons. Around it, a fine wire helix forms the grid. Outside that, two metal plate walls collect the electrons crossing the vacuum. Pins at the base connect the heater, cathode, grid and plate.")


# 2. The diode: one-way valve ---------------------------------------------------------------------
def diode_action():
    w, h = 900, 420
    parts = [common_defs(GLASS), panel(15, 15, 425, h - 30), panel(460, 15, 425, h - 30)]
    for cx, title, plate_pos in [(227, "Plate positive: current flows", True), (672, "Plate negative: nothing flows", False)]:
        parts.append(text(cx, 50, title, 16, AMBER_LIGHT, weight="bold"))
        # cathode at bottom, plate at top
        parts.append(f'<ellipse cx="{cx}" cy="320" rx="120" ry="40" fill="url(#vt-heat)"/>')
        parts.append(f'<rect x="{cx - 110}" y="310" width="220" height="20" rx="8" fill="#c05621"/>')
        parts.append(text(cx, 360, "hot cathode", 13, TEXT, weight="bold"))
        parts.append(f'<rect x="{cx - 110}" y="90" width="220" height="18" rx="4" fill="url(#vt-metal)"/>')
        parts.append(text(cx + 130, 104, "+" if plate_pos else "−", 24, GREEN if plate_pos else RED, "start", weight="bold"))
        parts.append(text(cx, 136, "plate", 13, TEXT, weight="bold"))
        random.seed(7)
        if plate_pos:
            for k in range(7):
                x = cx - 90 + k * 30
                parts.append(f'<line x1="{x}" y1="300" x2="{x}" y2="150" stroke="#90cdf4" stroke-width="2" stroke-dasharray="4 6" marker-end="url(#arrow)"/>')
                for j in range(3):
                    parts.append(_electron(x + random.uniform(-6, 6), 170 + j * 45 + random.uniform(-8, 8)))
            parts += pill(cx, 395, "electrons cross: current", GREEN, size=12, h=26)
        else:
            for k in range(14):
                x = cx - 100 + random.uniform(0, 200)
                y = 270 + random.uniform(-25, 20)
                parts.append(_electron(x, y))
            parts.append(text(cx, 220, "repelled: the cloud stays near the cathode", 12, MUTED, italic=True))
            parts += pill(cx, 395, "no current", RED, size=12, h=26)
    return svg(w, h, "\n".join(parts), "Two panels of a vacuum diode. Left, with the plate positive, electrons boiled off the hot cathode cross the vacuum to the plate and current flows. Right, with the plate negative, the electrons are repelled and stay in a cloud near the cathode, and no current flows.")


# 3. The grid as a control --------------------------------------------------------------------------
def grid_control():
    w, h = 900, 430
    parts = [common_defs(GLASS)]
    cases = [("Grid slightly negative", 9, "some electrons pass"),
             ("Grid more negative", 4, "fewer pass"),
             ("Grid far negative: cut off", 0, "none pass")]
    for k, (title, n, sub) in enumerate(cases):
        x0 = 15 + k * 295
        cx = x0 + 140
        parts.append(panel(x0, 15, 280, h - 30))
        parts.append(text(cx, 50, title, 14, AMBER_LIGHT, weight="bold"))
        parts.append(f'<rect x="{cx - 100}" y="80" width="200" height="16" rx="4" fill="url(#vt-metal)"/>')
        parts.append(text(cx, 120, "plate (+)", 12, TEXT, weight="bold"))
        for j in range(9):
            parts.append(f'<circle cx="{cx - 96 + j * 24}" cy="225" r="3" fill="#e2e8f0"/>')
        parts.append(text(cx + 112, 230, "grid", 12, TEXT, "start", weight="bold"))
        parts.append(f'<ellipse cx="{cx}" cy="330" rx="110" ry="34" fill="url(#vt-heat)"/>')
        parts.append(f'<rect x="{cx - 100}" y="320" width="200" height="18" rx="8" fill="#c05621"/>')
        parts.append(text(cx, 362, "cathode", 12, TEXT, weight="bold"))
        random.seed(11 + k)
        for _ in range(12):
            parts.append(_electron(cx - 95 + random.uniform(0, 190), 290 + random.uniform(-14, 14), 3.5))
        for j in range(n):
            x = cx - 88 + j * (176 / max(n - 1, 1)) if n > 1 else cx
            parts.append(f'<line x1="{x:.1f}" y1="270" x2="{x:.1f}" y2="140" stroke="#90cdf4" stroke-width="2" stroke-dasharray="4 6" marker-end="url(#arrow)"/>')
            parts.append(_electron(x, 180 + (j % 3) * 15, 3.5))
        col = GREEN if n > 6 else (AMBER if n else RED)
        parts += pill(cx, 395, sub, col, size=12, h=26)
    return svg(w, h, "\n".join(parts), "Three panels of a triode with the plate positive at the top, the hot cathode at the bottom, and a row of grid wires between. With the grid slightly negative, some electrons pass through the gaps to the plate. More negative, fewer pass. Far enough negative, none pass and the tube is cut off.")


# 4. Triode and FET, side by side ---------------------------------------------------------------------
def tube_vs_fet():
    w, h = 900, 430
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 50, "A triode and a field-effect transistor do the same job", 17, AMBER_LIGHT, weight="bold"))
    rows = [("emits the carriers", "cathode", "source"),
            ("controls by voltage", "grid", "gate"),
            ("collects the output", "plate", "drain")]
    for k, (role, tube, fet) in enumerate(rows):
        y = 120 + k * 80
        parts += pill(250, y, tube, "#c05621", wpx=170, size=16, h=44)
        parts += pill(650, y, fet, BLUE, wpx=170, size=16, h=44)
        parts.append(f'<line x1="345" y1="{y}" x2="555" y2="{y}" stroke="{MUTED}" stroke-width="2" stroke-dasharray="6 5"/>')
        parts.append(text(450, y - 8, role, 13, TEXT, weight="bold"))
    parts.append(text(250, 365, "heater: 1.9 W before any signal (12AX7)", 12, MUTED, italic=True))
    parts.append(text(250, 385, "plate: up to 300 V", 12, MUTED, italic=True))
    parts.append(text(650, 365, "no heater; works the moment power arrives", 12, MUTED, italic=True))
    parts.append(text(650, 385, "logic-level parts run from a few volts", 12, MUTED, italic=True))
    parts.append(text(250, 80, "TRIODE", 14, "#f6ad55", weight="bold"))
    parts.append(text(650, 80, "FET", 14, "#90cdf4", weight="bold"))
    return svg(w, h, "\n".join(parts), "A comparison of a triode and a field-effect transistor. The cathode matches the source, which emits the carriers; the grid matches the gate, which controls by voltage; the plate matches the drain, which collects the output. Beneath the triode: its heater uses 1.9 watts before any signal, and its plate runs up to 300 volts. Beneath the FET: no heater, and logic-level parts run from a few volts.")


# 5. Timeline -------------------------------------------------------------------------------------------
def timeline():
    w, h = 900, 330
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 50, "From a curiosity in a light bulb to the transistor", 17, AMBER_LIGHT, weight="bold"))
    events = [(1883, "Edison effect", "current from a hot filament"),
              (1904, "Fleming valve", "the vacuum diode"),
              (1907, "Audion patent", "de Forest's triode"),
              (1947, "12AX7 released", "and the transistor, Dec 1947")]
    x0, x1, y = 90, 810, 180
    lo, hi = 1880, 1950
    parts.append(f'<rect x="{x0}" y="{y - 5}" width="{x1 - x0}" height="10" rx="5" fill="#4a5568"/>')
    for yr in range(1880, 1951, 10):
        x = x0 + (yr - lo) / (hi - lo) * (x1 - x0)
        parts.append(f'<line x1="{x:.1f}" y1="{y + 8}" x2="{x:.1f}" y2="{y + 16}" stroke="{MUTED}"/>')
        parts.append(text(x, y + 32, str(yr), 11, MUTED))
    for k, (yr, name, sub) in enumerate(events):
        x = x0 + (yr - lo) / (hi - lo) * (x1 - x0)
        up = k % 2 == 0
        ty = y - 70 if up else y + 85
        parts.append(f'<line x1="{x:.1f}" y1="{y}" x2="{x:.1f}" y2="{ty + (22 if up else -22)}" stroke="{AMBER_LIGHT}" stroke-width="2"/>')
        parts.append(f'<circle cx="{x:.1f}" cy="{y}" r="9" fill="url(#vball)"/>')
        parts += pill(x, ty, f"{yr}: {name}", "#c05621", size=13, h=32)
        parts.append(text(x, ty + (32 if up else 34), sub, 12, MUTED, italic=True) if not up else
                     text(x, ty - 24, sub, 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "A timeline from 1880 to 1950. 1883, the Edison effect: current from a hot filament. 1904, the Fleming valve, the vacuum diode. 1907, de Forest's Audion triode patent. 1947, RCA releases the 12AX7, and Bell Labs demonstrates the first transistor in December.")


FIGURES = {"anatomy.svg": anatomy, "diode_action.svg": diode_action, "grid_control.svg": grid_control,
           "tube_vs_fet.svg": tube_vs_fet, "timeline.svg": timeline}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
