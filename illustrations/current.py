#!/usr/bin/env python3
"""Figures for docs/current.md.

Numbers and their sources:
- 1 A = 1 C/s; 20 mA = 1.25e17 electrons per second (e = 1.602176634e-19 C).
- The loop is the voltage article's circuit: 9 V, 330 Ohm, red LED (~2 V),
  so I = (9 - 2) / 330 = 21 mA everywhere in the loop.
- NIOSH Publication 98-131, Table 1 (60 Hz AC through the body): 1 mA barely
  perceptible, 16 mA let-go limit, 20 mA respiratory paralysis, 100 mA
  ventricular fibrillation threshold, 2 A cardiac standstill.
- ATmega328P datasheet (Microchip DS40002061B), absolute maximum: 40 mA per I/O
  pin, 200 mA through VCC/GND. USB 2.0: 500 mA per port. Household breaker
  15 A (NIOSH 98-131). Lightning ~30,000 A (NOAA JetStream lightning FAQ).

Usage:
    python3 illustrations/current.py
"""

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, common_defs,  # noqa: E402
                     cyl_gradient, led, panel, pill, render_all, shade, svg, text)
from voltage import multimeter, probe_lead  # noqa: E402
from what_is_electricity import wire  # noqa: E402

OUT = HERE.parent / "docs" / "images" / "current"
E = 1.602176634e-19
I_LOOP = (9 - 2) / 330


def ball(x, y, r=7, energy=1.0, glow=True):
    """An electron/coulomb ball; energy (0..1) dims it toward grey."""
    gid = "vball" if energy > 0.66 else ("midball" if energy > 0.33 else "lowball")
    g = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * 2.4:.1f}" fill="url(#glow)" opacity="{energy:.2f}"/>' if glow else ""
    return g + f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="url(#{gid})"/>'


EXTRA_BALLS = ('<radialGradient id="midball" cx="35%" cy="32%" r="70%"><stop offset="0" stop-color="#fde8c0"/>'
               '<stop offset="0.45" stop-color="#b7791f"/><stop offset="1" stop-color="#4a2c0a"/></radialGradient>'
               '<radialGradient id="lowball" cx="35%" cy="32%" r="70%"><stop offset="0" stop-color="#e2e8f0"/>'
               '<stop offset="0.45" stop-color="#718096"/><stop offset="1" stop-color="#1a202c"/></radialGradient>')


# 1. Counting at a point -----------------------------------------------------------
def counting_gate():
    w, h = 800, 400
    tube = ('<linearGradient id="glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2e8f0" stop-opacity="0.35"/>'
            '<stop offset="0.3" stop-color="#e2e8f0" stop-opacity="0.05"/><stop offset="0.85" stop-color="#1a202c" stop-opacity="0.25"/>'
            '<stop offset="1" stop-color="#e2e8f0" stop-opacity="0.3"/></linearGradient>')
    parts = [common_defs(tube + EXTRA_BALLS), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "Current is a count: how much charge passes one point each second", 15, TEXT, weight="bold"))
    ty, th = 150, 90
    parts.append(f'<rect x="60" y="{ty}" width="680" height="{th}" rx="45" fill="#b8673a" fill-opacity="0.18"/>')
    for k in range(26):
        x = 80 + k * 26
        y = ty + th / 2 + 22 * math.sin(k * 1.7)
        parts.append(ball(x, y, 7))
    gx = 420
    parts.append(f'<ellipse cx="{gx}" cy="{ty + th / 2}" rx="18" ry="{th / 2 + 14}" fill="none" stroke="{AMBER_LIGHT}" stroke-width="5" opacity="0.9"/>')
    parts.append(f'<ellipse cx="{gx}" cy="{ty + th / 2}" rx="26" ry="{th / 2 + 22}" fill="none" stroke="{AMBER}" stroke-width="10" opacity="0.18"/>')
    parts.append(f'<rect x="60" y="{ty}" width="680" height="{th}" rx="45" fill="url(#glass)" stroke="#e2e8f0" stroke-opacity="0.45"/>')
    parts.append(f'<line x1="120" y1="{ty + th + 26}" x2="700" y2="{ty + th + 26}" stroke="{AMBER}" stroke-width="3" marker-end="url(#arrow)"/>')
    n = 0.020 / E
    parts += pill(gx, 100, "the counting point", "#d97706", "#1a1a1a", size=13, h=30)
    parts.append(f'<rect x="{gx - 170}" y="300" width="340" height="56" rx="10" fill="#1a1d23" stroke="#9ae6b4" stroke-opacity="0.5"/>')
    parts.append(text(gx, 324, f"{n / 1e17:.2f} × 10¹⁷ electrons per second", 16, "#9ae6b4", weight="bold"))
    parts.append(text(gx, 345, "= 0.020 coulombs per second = 20 mA", 13, "#9ae6b4"))
    return svg(w, h, "\n".join(parts), "A glass wire full of electrons flowing past a glowing ring that marks one counting point. A counter reads 1.25 times 10 to the 17 electrons per second, which is 0.020 coulombs per second, or 20 milliamps.")


# 2. Same current everywhere, energy spent along the way ------------------------------------
def same_everywhere():
    w, h = 800, 470
    parts = [common_defs(cyl_gradient("battx", AMBER, vertical=True) + cyl_gradient("resbody", "#d9b382") + EXTRA_BALLS),
             panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "The same current flows everywhere in the loop; the energy is what gets spent", 15, TEXT, weight="bold"))
    L, R, T, B = 150, 650, 120, 330
    parts += wire([(L, 190), (L, T), (R, T), (R, B), (L, B), (L, 250)])
    # balls: evenly spaced all round; full energy before the resistor, less after, least after the LED
    path = [(L, T), (R, T), (R, B), (L, B)]
    seglens = [abs(x2 - x1) + abs(y2 - y1) for (x1, y1), (x2, y2) in zip(path, path[1:])]
    total, step = sum(seglens), 44
    d = 30
    while d < total:
        acc, (x, y) = d, path[0]
        for (x1, y1), (x2, y2), sl in zip(path, path[1:], seglens):
            if acc <= sl:
                f = acc / sl
                x, y = x1 + (x2 - x1) * f, y1 + (y2 - y1) * f
                break
            acc -= sl
        if not (330 <= x <= 470 and y == T) and not (x == R and 190 <= y <= 260):
            energy = 1.0 if (y == T and x < 330) else (0.55 if (y == T or (x == R and y < 200)) else 0.2)
            parts.append(ball(x, y, 6, energy))
        d += step
    parts.append(f'<rect x="330" y="{T - 17}" width="140" height="34" rx="17" fill="url(#resbody)"/>')
    for off, col in ((26, "#f6ad55"), (46, "#f6ad55"), (66, "#8b4513"), (104, "#d4af37")):
        parts.append(f'<rect x="{330 + off}" y="{T - 16}" width="9" height="32" fill="{col}"/>')
    parts += led(R, 220, "#fc8181", lit=True, r=15, glow=0.8)
    # battery
    parts.append(f'<rect x="{L - 28}" y="190" width="56" height="70" rx="6" fill="url(#battx)"/>')
    parts.append(text(L, 232, "9 V", 15, "#1a1a1a", weight="bold"))
    # ammeter badges
    for x, y in ((240, T - 42), (560, T - 42), (R + 70, 290), (400, B + 40)):
        parts += pill(x, y, f"{I_LOOP * 1000:.0f} mA", "#1a1d23", "#9ae6b4", wpx=84, size=13, h=28)
    parts.append(text(400, 410, "every meter reads the same: no charge is used up", 13, "#9ae6b4", weight="bold"))
    parts.append(text(400, 432, "the balls dim as they pass the resistor and the LED: that's energy (voltage) being spent", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "A loop with a 9 volt battery, a 330 ohm resistor and a red LED. Evenly spaced glowing balls of charge circle the loop and four meters all read 21 milliamps. The balls are bright before the resistor, dimmer after it, and dimmest after the LED.")


# 3. A junction splits and rejoins --------------------------------------------------------
def junction():
    w, h = 800, 380
    parts = [common_defs(EXTRA_BALLS), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "At a junction, current splits; every coulomb that arrives must leave", 15, TEXT, weight="bold"))
    parts += wire([(60, 200), (260, 200)], 12) + wire([(540, 200), (740, 200)], 12)
    parts += wire([(260, 200), (300, 120), (500, 120), (540, 200)], 9)
    parts += wire([(260, 200), (300, 280), (500, 280), (540, 200)], 9)
    for k in range(9):
        parts.append(ball(70 + k * 22, 200, 6))
        parts.append(ball(550 + k * 22, 200, 6))
    for k in range(6):
        parts.append(ball(310 + k * 36, 120, 6))
    for k in range(3):
        parts.append(ball(320 + k * 72, 280, 6))
    parts += pill(160, 250, "30 mA in", "#d97706", "#1a1a1a", size=13, h=30)
    parts += pill(400, 86, "20 mA", "#2d3748", size=13, h=28)
    parts += pill(400, 316, "10 mA", "#2d3748", size=13, h=28)
    parts += pill(640, 250, "30 mA out", "#d97706", "#1a1a1a", size=13, h=30)
    parts.append(text(400, 206, "20 + 10 = 30", 15, "#9ae6b4", weight="bold"))
    return svg(w, h, "\n".join(parts), "A wire carrying 30 milliamps splits into two branches carrying 20 and 10 milliamps, which rejoin to carry 30 milliamps again")


# 4. Two directions ----------------------------------------------------------------------
def two_directions():
    w, h = 800, 380
    parts = [common_defs(cyl_gradient("battx", AMBER, vertical=True) + EXTRA_BALLS), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "Two conventions, one current", 16, TEXT, weight="bold"))
    parts += wire([(100, 200), (700, 200)], 14)
    parts += pill(70, 200, "+", "#d97706", "#1a1a1a", wpx=44, size=18, h=44)
    parts += pill(730, 200, "−", "#2d3748", wpx=44, size=18, h=44)
    parts.append(f'<line x1="150" y1="140" x2="650" y2="140" stroke="{AMBER}" stroke-width="6" marker-end="url(#arrow)"/>')
    parts.append(text(400, 120, "Conventional current: + to −", 15, AMBER_LIGHT, weight="bold"))
    parts.append(text(400, 102, "the direction every schematic and every formula uses", 12, MUTED, italic=True))
    for k in range(12):
        parts.append(ball(150 + k * 45, 200, 6, energy=0.2, glow=False).replace("lowball", "eball"))
    parts.append(f'<line x1="650" y1="262" x2="150" y2="262" stroke="#90cdf4" stroke-width="6" marker-end="url(#arrowblue)"/>')
    parts.append(text(400, 296, "Electron flow: − to +", 15, "#90cdf4", weight="bold"))
    parts.append(text(400, 316, "what the electrons physically do (they carry negative charge)", 12, MUTED, italic=True))
    parts.append(text(400, 350, "The convention came first, in the 1700s; the electron wasn't discovered until 1897", 12, MUTED, italic=True))
    s = svg(w, h, "\n".join(parts), "A wire between a positive and a negative terminal. An amber arrow labelled conventional current points from plus to minus. Below, the electrons in the wire and a blue arrow labelled electron flow point the other way, from minus to plus.")
    return s.replace("</defs>", '<marker id="arrowblue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                                 'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#90cdf4"/></marker></defs>', 1)


# 5. Current scale, with the body's thresholds --------------------------------------------
def current_scale():
    w, h = 800, 400
    L, R = 50, 750
    lo, hi = -4, 5
    X = lambda v: L + (R - L) * (math.log10(v) - lo) / (hi - lo)
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "Currents you'll meet, log scale (each tick is 10×), with what each does to a body", 15, TEXT, weight="bold"))
    ty, th = 170, 28
    parts.append(f'<rect x="{L}" y="{ty}" width="{R - L}" height="{th}" rx="14" fill="#4a5568" fill-opacity="0.5"/>')
    parts.append(f'<rect x="{X(0.001):.1f}" y="{ty}" width="{R - X(0.001):.1f}" height="{th}" rx="14" fill="{RED}" fill-opacity="0.35"/>')
    parts.append(f'<rect x="{L}" y="{ty}" width="{R - L}" height="{th}" rx="14" fill="url(#gloss)" stroke="#e2e8f0" stroke-opacity="0.35"/>')
    for p in range(lo, hi + 1):
        x = X(10 ** p)
        lab = {-4: "0.1 mA", -3: "1 mA", -2: "10 mA", -1: "100 mA", 0: "1 A", 1: "10 A", 2: "100 A", 3: "1 kA", 4: "10 kA", 5: "100 kA"}[p]
        parts.append(f'<line x1="{x:.1f}" y1="{ty + th}" x2="{x:.1f}" y2="{ty + th + 6}" stroke="{MUTED}"/>')
        parts.append(text(x, ty + th + 20, lab, 10, MUTED))
    devices = [(0.020, "LED", 0), (0.040, "Uno pin max", 1), (0.5, "USB 2.0 port", 0), (15, "household breaker", 1), (30000, "lightning", 0)]
    for v, lab, row in devices:
        x = X(v)
        y = ty - 30 - row * 34
        parts.append(f'<circle cx="{x:.1f}" cy="{ty + th / 2}" r="8" fill="url(#eball)"/>')
        parts.append(f'<line x1="{x:.1f}" y1="{ty - 2}" x2="{x:.1f}" y2="{y + 6}" stroke="{MUTED}"/>')
        parts.append(text(x, y, lab, 12, TEXT, weight="bold"))
    body = [(0.001, "1 mA", "barely felt", 0), (0.018, "16–20 mA", "can't let go; breathing stops", 1),
            (0.1, "100 mA", "heart fibrillates", 0), (2, "2 A", "heart stops", 1)]
    for v, lab, eff, row in body:
        x = X(v)
        y = ty + th + 52 + row * 42
        parts.append(f'<line x1="{x:.1f}" y1="{ty + th + 26}" x2="{x:.1f}" y2="{y - 14}" stroke="#fc8181" stroke-opacity="0.7"/>')
        parts.append(text(x, y, lab, 12, "#fc8181", weight="bold"))
        parts.append(text(x, y + 15, eff, 11, "#fc8181"))
    parts.append(text(w / 2, h - 28, "red zone: effects of 60 Hz current through the body (NIOSH 98-131, Table 1)", 11, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "A log scale of current from 0.1 milliamps to 100 kiloamps. Devices above it: an LED at 20 milliamps, an Arduino pin's 40 milliamp maximum, a 500 milliamp USB port, a 15 amp household breaker, and 30,000 amp lightning. Below it in red, the body's thresholds: 1 milliamp barely felt, 16 can't let go, 20 breathing stops, 100 the heart fibrillates, 2 amps the heart stops.")


# 6. Where the meter goes: across vs in line ---------------------------------------------
def meter_placement():
    w, h = 800, 470
    parts = [common_defs(cyl_gradient("resbody", "#d9b382")), panel(15, 15, 375, h - 30), panel(410, 15, 375, h - 30)]

    def resistor(x, y):
        out = [f'<rect x="{x}" y="{y - 15}" width="110" height="30" rx="15" fill="url(#resbody)"/>']
        for off, col in ((22, "#f6ad55"), (38, "#f6ad55"), (54, "#8b4513"), (84, "#d4af37")):
            out.append(f'<rect x="{x + off}" y="{y - 14}" width="8" height="28" fill="{col}"/>')
        return out
    # left: voltage, meter across
    parts.append(text(202, 48, "Voltage: meter across", 16, AMBER_LIGHT, weight="bold"))
    parts.append(text(202, 68, "the circuit stays whole", 12, MUTED, italic=True))
    parts += wire([(40, 130), (147, 130)], 8) + wire([(257, 130), (365, 130)], 8)
    parts += resistor(147, 130)
    parts += multimeter(142, 230, "7.0")
    parts += probe_lead(176, 366, 147, 130 - 4, "#e53e3e") + probe_lead(228, 366, 257, 130 - 4, "#111")
    parts.append(text(202, 430, "probes on either side of the part", 12, TEXT))
    # right: current, meter in line
    parts.append(text(597, 48, "Current: meter in line", 16, AMBER_LIGHT, weight="bold"))
    parts.append(text(597, 68, "break the circuit; the meter closes the gap", 12, MUTED, italic=True))
    parts += wire([(430, 130), (520, 130)], 8)
    parts += resistor(520, 130)
    parts += wire([(630, 130), (660, 130)], 8)
    parts.append(f'<path d="M660,130 l8,-10 m-8,10 l-6,-10" stroke="#fc8181" stroke-width="2"/>')
    parts += wire([(715, 130), (760, 130)], 8)
    parts.append(text(688, 108, "gap", 11, "#fc8181", italic=True))
    parts += multimeter(537, 230, "21.2 mA", mode="A⎓")
    parts += probe_lead(571, 366, 660, 130 - 4, "#e53e3e") + probe_lead(623, 366, 715, 130 - 4, "#111")
    parts.append(text(597, 420, "all the current now flows through the meter", 12, TEXT))
    parts.append(text(597, 438, "(red lead moved to the mA jack)", 11, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Two panels. Left: measuring voltage, a meter's probes touch either side of a resistor and it reads 7.0 volts while the circuit stays whole. Right: measuring current, the wire is cut and the meter's probes bridge the gap so all the current flows through the meter, which reads 21.2 milliamps.")


FIGURES = {
    "counting_gate.svg": counting_gate,
    "same_everywhere.svg": same_everywhere,
    "junction.svg": junction,
    "two_directions.svg": two_directions,
    "current_scale.svg": current_scale,
    "meter_placement.svg": meter_placement,
}

if __name__ == "__main__":
    print(f"loop current {I_LOOP * 1000:.1f} mA; 20 mA = {0.02 / E:.3e} e/s")
    render_all(FIGURES, OUT)
