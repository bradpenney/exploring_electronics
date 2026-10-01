#!/usr/bin/env python3
"""Figures for docs/ohms_law.md.

Numbers and their sources:
- 100 W, 120 V incandescent bulb: hot R = V^2 / P = 144 Ohm.
- Tungsten resistivity (Physics Factbook table, from Desai et al., J. Phys.
  Chem. Ref. Data 13, 1984): 5.65 uOhm-cm at 300 K, 84.70 at 2,800 K, a ratio
  of 15.0, so the cold filament is about 144 / 15 = 9.6 Ohm. Filaments run at
  2,000-3,300 K (Wikipedia, Incandescent light bulb).
- LED loop from the voltage/current articles: 9 V, 330 Ohm, red LED ~2 V,
  I = 21.2 mA. Resistor power I^2 R; a 1/4 W through-hole resistor.
- Charger 5 V x 2 A = 10 W and laptop 20 V x 3.25 A = 65 W, from What Is
  Electricity?; the 1,500 W heater from the resistance article.
- I-V curves for the bulb and the LED are drawn as shapes (labelled
  illustrative); the resistor's line is exact.

Usage:
    python3 illustrations/ohms_law.py
"""

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, box3d,  # noqa: E402
                     common_defs, cyl_gradient, led, panel, pill, render_all,
                     shade, svg, text)
from voltage import multimeter, probe_lead  # noqa: E402

OUT = HERE.parent / "docs" / "images" / "ohms_law"
R_HOT = 120 ** 2 / 100
RATIO = 84.70 / 5.65
R_COLD = R_HOT / RATIO
I_LOOP = (9 - 2) / 330


def bulb(cx, cy, hot):
    """An incandescent bulb: glass globe, filament, screw base."""
    glass = ('<radialGradient id="glass{0}" cx="35%" cy="30%" r="75%"><stop offset="0" stop-color="#ffffff" stop-opacity="{1}"/>'
             '<stop offset="0.6" stop-color="{2}" stop-opacity="{3}"/><stop offset="1" stop-color="#a0aec0" stop-opacity="0.35"/>'
             '</radialGradient>').format(int(hot), 0.55 if hot else 0.35, "#fefcbf" if hot else "#cbd5e0", 0.55 if hot else 0.08)
    out = [glass]
    if hot:
        out.append(f'<circle cx="{cx}" cy="{cy}" r="120" fill="#fefcbf" fill-opacity="0.12"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="80" fill="#fefcbf" fill-opacity="0.18"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="58" fill="url(#glass{int(hot)})" stroke="#e2e8f0" stroke-opacity="0.5"/>')
    fil = "#fffbe6" if hot else "#718096"
    out.append(f'<path d="M{cx - 14},{cy + 52} L{cx - 14},{cy + 6} M{cx + 14},{cy + 52} L{cx + 14},{cy + 6}" stroke="#a0aec0" stroke-width="2"/>')
    out.append(f'<path d="M{cx - 14},{cy + 6} q4,-10 7,0 t7,0 t7,0 t7,0" fill="none" stroke="{fil}" stroke-width="{3 if hot else 2}"/>')
    for k in range(4):
        out.append(f'<rect x="{cx - 26}" y="{cy + 54 + k * 9}" width="52" height="8" rx="3" fill="#a0aec0"/>')
    out.append(f'<rect x="{cx - 14}" y="{cy + 90}" width="28" height="10" rx="4" fill="#2d3748"/>')
    return out


# 1. The bulb puzzle -----------------------------------------------------------------
def bulb_puzzle():
    w, h = 800, 500
    parts = [common_defs(), panel(15, 15, 375, h - 30), panel(410, 15, 375, h - 30)]
    parts.append(text(202, 48, "Cold, on a multimeter", 16, TEXT, weight="bold"))
    parts += bulb(202, 160, hot=False)
    parts += multimeter(142, 290, f"{R_COLD:.1f} Ω", mode="Ω")
    parts.append(text(202, 470, "room temperature, about 300 K", 12, MUTED, italic=True))
    parts.append(text(597, 48, "Hot, from its rating", 16, AMBER_LIGHT, weight="bold"))
    parts += bulb(597, 160, hot=True)
    parts.append(text(597, 330, "100 W at 120 V", 15, TEXT, weight="bold"))
    parts.append(text(597, 360, f"R = V² ÷ P = {R_HOT:.0f} Ω", 18, AMBER_LIGHT, weight="bold"))
    parts.append(text(597, 470, "filament glowing at about 2,800 K", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), f"Two copies of a 100 watt bulb. Cold, a multimeter reads {R_COLD:.1f} ohms across it. Hot and glowing, its rating of 100 watts at 120 volts means {R_HOT:.0f} ohms, fifteen times more.")


# 2. I-V curves ------------------------------------------------------------------
def iv_curves():
    w, h = 760, 480
    L, R, T, B = 95, 600, 60, 400
    vmax, imax = 9.0, 0.06
    X = lambda v: L + (R - L) * v / vmax
    Y = lambda i: B - (B - T) * i / imax
    parts = [common_defs(), panel(L - 10, T - 10, R - L + 20, B - T + 20)]
    for v in range(1, 10):
        parts.append(f'<line x1="{X(v):.1f}" y1="{T}" x2="{X(v):.1f}" y2="{B}" stroke="#4a5568" stroke-opacity="0.35"/>')
    for i in (0.01, 0.02, 0.03, 0.04, 0.05):
        parts.append(f'<line x1="{L}" y1="{Y(i):.1f}" x2="{R}" y2="{Y(i):.1f}" stroke="#4a5568" stroke-opacity="0.35"/>')
    parts.append(f'<line x1="{L}" y1="{B}" x2="{R}" y2="{B}" stroke="{MUTED}" stroke-width="1.5"/>')
    parts.append(f'<line x1="{L}" y1="{B}" x2="{L}" y2="{T}" stroke="{MUTED}" stroke-width="1.5"/>')
    for v in range(0, 10):
        parts.append(text(X(v), B + 20, f"{v} V", 12, MUTED))
    for i in (0, 0.02, 0.04, 0.06):
        parts.append(text(L - 10, Y(i) + 4, f"{i * 1000:.0f} mA", 12, MUTED, "end"))
    parts.append(text((L + R) / 2, B + 48, "Voltage across the part", 14))
    parts.append(f'<text x="28" y="{(T + B) / 2}" font-size="14" fill="{TEXT}" text-anchor="middle" '
                 f'transform="rotate(-90 28 {(T + B) / 2})">Current through it</text>')
    # resistor: exact straight line, 150 ohm so it fits the chart
    res = [(v / 10, v / 10 / 150) for v in range(0, 91)]
    # lamp (illustrative): resistance climbs as it heats, I ~ V^0.6
    lamp = [(v / 10, 0.045 * (v / 90) ** 0.6) for v in range(0, 91)]
    # LED (illustrative Shockley shape, red LED ~1.8-2 V knee), clipped to the chart
    ledc = []
    for k in range(0, 300):
        v = k / 100
        i = 1e-19 * (math.exp(v / (2 * 0.02585)) - 1)
        if i > imax:
            break
        ledc.append((v, i))
    for pts, color, lab, lx, ly, anc in ((res, AMBER, "resistor (150 Ω): a straight line", 2.4, 0.045, "start"),
                                         (lamp, "#f7fafc", "lamp: bends over as it heats", 9.0, 0.024, "end"),
                                         (ledc, "#fc8181", "LED: nothing, then a wall", 2.25, 0.055, "start")):
        line = " ".join(f"{X(v):.1f},{Y(i):.1f}" for v, i in pts)
        parts.append(f'<polyline points="{line}" fill="none" stroke="{color}" stroke-width="3.5" filter="url(#softglow)"/>')
        parts.append(text(X(lx), Y(ly), lab, 13, color, anc, "bold"))
    parts.append(text(R + 18, T + 20, "Ohm's Law holds", 13, AMBER_LIGHT, "start", "bold"))
    parts.append(text(R + 18, T + 38, "only where the", 13, AMBER_LIGHT, "start"))
    parts.append(text(R + 18, T + 56, "line is straight", 13, AMBER_LIGHT, "start"))
    parts.append(text(R + 18, B - 20, "lamp and LED curves", 11, MUTED, "start", italic=True))
    parts.append(text(R + 18, B - 4, "show typical shapes", 11, MUTED, "start", italic=True))
    return svg(w, h, "\n".join(parts), "Current against voltage for three parts. A resistor's line is perfectly straight. A lamp's curve bends over as the filament heats and its resistance climbs. An LED's curve stays flat near zero until about 1.8 volts, then rises almost vertically.")


# 3. The triangle ----------------------------------------------------------------
def ohm_triangle():
    w, h = 800, 400
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "One relationship, three ways to read it", 16, TEXT, weight="bold"))

    def tri(cx, cy, size, hide=None):
        out = []
        top, bl, br = (cx, cy - size * 0.62), (cx - size * 0.6, cy + size * 0.38), (cx + size * 0.6, cy + size * 0.38)
        depth = 14
        out.append(f'<polygon points="{bl[0]},{bl[1]} {br[0]},{br[1]} {br[0] + depth},{br[1] - depth * 0.6} {top[0] + depth},{top[1] - depth * 0.6} {top[0]},{top[1]}" fill="#1a202c"/>')
        out.append(f'<polygon points="{top[0]},{top[1]} {bl[0]},{bl[1]} {br[0]},{br[1]}" fill="#d97706"/>')
        out.append(f'<polygon points="{top[0]},{top[1]} {bl[0]},{bl[1]} {br[0]},{br[1]}" fill="url(#gloss)"/>')
        out.append(f'<line x1="{cx - size * 0.38}" y1="{cy - 2}" x2="{cx + size * 0.38}" y2="{cy - 2}" stroke="#1a1a1a" stroke-width="3"/>')
        out.append(f'<line x1="{cx}" y1="{cy - 2}" x2="{cx}" y2="{cy + size * 0.38}" stroke="#1a1a1a" stroke-width="3"/>')
        for lab, (x, y) in (("V", (cx, cy - size * 0.14)), ("I", (cx - size * 0.2, cy + size * 0.27)), ("R", (cx + size * 0.2, cy + size * 0.27))):
            if lab == hide:
                out.append(f'<circle cx="{x}" cy="{y - 8}" r="{size * 0.13:.1f}" fill="#2d3748" stroke="#e2e8f0" stroke-opacity="0.6"/>')
                out.append(text(x, y - 2, "?", int(size * 0.15), "#f7fafc", weight="bold"))
            else:
                out.append(text(x, y, lab, int(size * 0.17), "#1a1a1a", weight="bold"))
        return out
    for i, (hide, eq) in enumerate((("V", "V = I × R"), ("I", "I = V ÷ R"), ("R", "R = V ÷ I"))):
        cx = 150 + i * 250
        parts += tri(cx, 200, 190, hide)
        parts += pill(cx, 335, eq, "#2d3748", wpx=150, size=16, h=40)
    parts.append(text(w / 2, 375, "cover the one you want; what's left shows how to get it (side by side multiply, one over the other divide)", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Three copies of the Ohm's Law triangle, V on top and I and R below, each with one letter covered: covering V gives V equals I times R, covering I gives I equals V over R, covering R gives R equals V over I.")


# 4. Power: joules per coulomb times coulombs per second ------------------------------------
def power_units():
    w, h = 820, 380
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "Power is voltage times current, and the units say why", 16, TEXT, weight="bold"))
    blocks = [(130, "9 V", "9 joules", "per coulomb", AMBER), (410, f"{I_LOOP * 1000:.1f} mA", f"{I_LOOP:.4f} coulombs", "per second", "#3182ce"),
              (690, f"{9 * I_LOOP:.2f} W", f"{9 * I_LOOP:.2f} joules", "per second", "#2f855a")]
    for cx, big, l1, l2, c in blocks:
        parts += box3d(cx - 95, 260, 190, 40, 150, c)
        parts.append(text(cx, 160, big, 30, "#ffffff", weight="bold"))
        parts.append(text(cx, 200, l1, 15, "#ffffff", weight="bold"))
        parts.append(text(cx, 222, l2, 14, "#ffffff"))
    parts.append(text(270, 190, "×", 40, TEXT, weight="bold"))
    parts.append(text(550, 190, "=", 40, TEXT, weight="bold"))
    parts.append(text(w / 2, 312, "the coulombs cancel: joules per coulomb × coulombs per second = joules per second = watts", 13, AMBER_LIGHT, weight="bold"))
    parts.append(text(w / 2, 336, "the LED loop from Voltage and Current: the battery delivers 0.19 W, all of it spent in the resistor and the LED", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), f"Three 3D blocks: 9 volts, meaning 9 joules per coulomb, times {I_LOOP * 1000:.1f} milliamps, meaning {I_LOOP:.4f} coulombs per second, equals {9 * I_LOOP:.2f} watts, meaning {9 * I_LOOP:.2f} joules per second.")


# 5. How hot does a 1/4 W resistor run? ----------------------------------------------
def resistor_heat():
    w, h = 800, 430
    grads = cyl_gradient("resbody", "#d9b382")
    parts = [common_defs(grads), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "Three 330 Ω, ¼ W resistors: how much of their rating each one uses", 15, TEXT, weight="bold"))
    cases = [("5 V LED circuit", (5 - 2) ** 2 / 330), ("9 V LED circuit", I_LOOP ** 2 * 330), ("straight across 9 V", 9 ** 2 / 330)]
    for i, (lab, p) in enumerate(cases):
        cx = 140 + i * 260
        frac = p / 0.25
        color = GREEN if frac < 0.5 else (AMBER if frac < 0.8 else RED)
        parts.append(f'<circle cx="{cx}" cy="170" r="{40 + 70 * frac:.0f}" fill="{color}" fill-opacity="{0.08 + 0.25 * frac:.2f}"/>')
        parts.append(f'<rect x="{cx - 100}" y="167" width="200" height="6" rx="3" fill="#cbd5e0"/>')
        parts.append(f'<rect x="{cx - 55}" y="152" width="110" height="36" rx="18" fill="url(#resbody)"/>')
        for off, col in ((18, "#f6ad55"), (36, "#f6ad55"), (54, "#8b4513"), (88, "#d4af37")):
            parts.append(f'<rect x="{cx - 55 + off}" y="153" width="8" height="34" fill="{col}"/>')
        parts.append(text(cx, 278, lab, 14, TEXT, weight="bold"))
        parts.append(text(cx, 302, f"{p * 1000:.0f} mW", 22, color, weight="bold"))
        # rating gauge
        parts.append(f'<rect x="{cx - 80}" y="320" width="160" height="14" rx="7" fill="#2d3748"/>')
        parts.append(f'<rect x="{cx - 80}" y="320" width="{160 * min(1, frac):.1f}" height="14" rx="7" fill="{color}"/>')
        parts.append(text(cx, 356, f"{frac * 100:.0f}% of its ¼ W rating", 13, TEXT))
    parts.append(text(w / 2, 396, "rule of thumb: keep a resistor at or below half its rating; near 100% it runs hot enough to burn a finger", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Three identical 330 ohm, quarter-watt resistors. In a 5 volt LED circuit one dissipates 27 milliwatts, 11 percent of its rating, and stays cool. In the 9 volt LED circuit one dissipates 148 milliwatts, 59 percent. Wired straight across 9 volts one dissipates 245 milliwatts, 98 percent, and glows hot.")


# 6. Power scale ------------------------------------------------------------------
def power_scale():
    w, h = 800, 330
    L, R = 50, 750
    lo, hi = -2, 4
    X = lambda v: L + (R - L) * (math.log10(v) - lo) / (hi - lo)
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "Power you'll meet, log scale (each tick is 10×)", 16, TEXT, weight="bold"))
    ty, th = 160, 28
    parts.append(f'<rect x="{L}" y="{ty}" width="{R - L}" height="{th}" rx="14" fill="{AMBER}" fill-opacity="0.35"/>')
    parts.append(f'<rect x="{L}" y="{ty}" width="{R - L}" height="{th}" rx="14" fill="url(#gloss)" stroke="#e2e8f0" stroke-opacity="0.35"/>')
    for p in range(lo, hi + 1):
        x = X(10 ** p)
        lab = {-2: "10 mW", -1: "0.1 W", 0: "1 W", 1: "10 W", 2: "100 W", 3: "1 kW", 4: "10 kW"}[p]
        parts.append(f'<line x1="{x:.1f}" y1="{ty + th}" x2="{x:.1f}" y2="{ty + th + 6}" stroke="{MUTED}"/>')
        parts.append(text(x, ty + th + 20, lab, 11, MUTED))
    items = [(2 * I_LOOP, "LED", True), (I_LOOP ** 2 * 330, "its resistor", False), (10, "phone charger", True),
             (65, "laptop charger", False), (100, "old 100 W bulb", True), (1500, "space heater", False)]
    for v, lab, above in items:
        x = X(v)
        parts.append(f'<circle cx="{x:.1f}" cy="{ty + th / 2}" r="8" fill="url(#eball)"/>')
        y = ty - 30 if above else ty + th + 62
        parts.append(f'<line x1="{x:.1f}" y1="{ty - 2 if above else ty + th + 28}" x2="{x:.1f}" y2="{y + (6 if above else -14)}" stroke="{MUTED}"/>')
        val = f"{v * 1000:.0f} mW" if v < 1 else f"{v:g} W"
        parts.append(text(x, y - (16 if above else 0), lab, 13, TEXT, weight="bold"))
        parts.append(text(x, y + (0 if above else 16), val, 12, AMBER_LIGHT))
    return svg(w, h, "\n".join(parts), "A log scale of power from 10 milliwatts to 10 kilowatts: an LED at 42 milliwatts, its resistor at 148 milliwatts, a 10 watt phone charger, a 65 watt laptop charger, an old 100 watt bulb, and a 1,500 watt space heater.")


FIGURES = {
    "bulb_puzzle.svg": bulb_puzzle,
    "iv_curves.svg": iv_curves,
    "ohm_triangle.svg": ohm_triangle,
    "power_units.svg": power_units,
    "resistor_heat.svg": resistor_heat,
    "power_scale.svg": power_scale,
}

if __name__ == "__main__":
    print(f"hot {R_HOT:.0f} ohm, ratio {RATIO:.2f}, cold {R_COLD:.2f} ohm; inrush {120 / R_COLD:.1f} A vs {100 / 120:.2f} A")
    print(f"loop {I_LOOP * 1000:.1f} mA, resistor {I_LOOP ** 2 * 330 * 1000:.0f} mW, LED {2 * I_LOOP * 1000:.0f} mW, total {9 * I_LOOP * 1000:.0f} mW")
    render_all(FIGURES, OUT)
