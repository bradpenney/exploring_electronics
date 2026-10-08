#!/usr/bin/env python3
"""Figures for docs/diodes_and_leds.md.

Sources (datasheet values; every other number is computed):
- Kingbright WP7113SRD (red): VF 1.85 V typ / 2.5 V max at 20 mA, dominant
  wavelength 640 nm, VR 5 V, DC IF 30 mA, TCV -1.9 mV/degC.
- Kingbright WP7113SGD (green): VF 2.2 V typ at 20 mA, 568 nm.
- Kingbright WP7113QBC/D (blue): VF 3.3 V typ / 4.0 V max at 20 mA, 465 nm.
- onsemi 1N914/1N4148: VF 0.62-0.72 V at 5 mA (1N914B/4448), 100 V, 4 ns.
- onsemi 1N4001-1N4007: 50-1000 V, 1 A, VF 0.93 V typ / 1.1 V max at 1 A.
- onsemi 1N5817: VF 0.32 V at 0.1 A, 0.45 V at 1 A; 20 V.
- Vishay 1N4733A: 5.1 V Zener.
- Photon energy E = hc / lambda.
The I-V curves are the Shockley diode equation, I = Is (exp(V / (n Vt)) - 1),
fitted through those datasheet points; they show typical shapes, not a guarantee.

Usage:
    python3 illustrations/diodes_and_leds.py
"""

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, box3d,  # noqa: E402
                     common_defs, cyl_gradient, led, panel, pill, render_all,
                     shade, svg, text)
from ac_dc import axes, glow_line  # noqa: E402

OUT = HERE.parent / "docs" / "images" / "diodes_and_leds"
VT = 0.02585
NBLUE, PRED, HOLE = "#90cdf4", "#fc8181", "#fbd38d"
H, C, Q = 6.62607015e-34, 299792458, 1.602176634e-19


def photon_ev(nm):
    return H * C / (nm * 1e-9) / Q


def shockley(v0, i0, n):
    """Return I(V) through (v0, i0) with ideality factor n."""
    i_s = i0 / (math.exp(v0 / (n * VT)) - 1)
    return lambda v: i_s * (math.exp(v / (n * VT)) - 1)


# Schottky fitted through its two datasheet points
N_SCH = (0.45 - 0.32) / (VT * math.log(10))
DIODES = [
    ("Schottky 1N5817", shockley(0.32, 0.1, N_SCH), "#e2e8f0"),
    ("Silicon 1N4148", shockley(0.67, 0.005, 1.9), "#a0aec0"),
    ("Red LED", shockley(1.85, 0.020, 2.0), "#fc5c5c"),
    ("Green LED", shockley(2.2, 0.020, 2.0), "#48bb78"),
    ("Blue LED", shockley(3.3, 0.020, 2.0), "#4f8ef7"),
]


def v_at(fn, i, lo=0.0, hi=5.0):
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if fn(mid) < i else (lo, mid)
    return (lo + hi) / 2


def silicon_block(x, y, w, h, color):
    return box3d(x, y, w, 40, h, color, shadow=False)


# 1. The PN junction in three states -------------------------------------------------------
def junction():
    w, h = 900, 470
    parts = [common_defs()]
    states = [("No voltage", 46, "a thin depletion zone forms by itself", None),
              ("Forward biased", 16, "zone squeezed thin: current flows", "fwd"),
              ("Reverse biased", 110, "zone widened: almost nothing flows", "rev")]
    for k, (title, dz, note, mode) in enumerate(states):
        x0 = 30 + k * 290
        parts.append(panel(x0, 20, 270, 430))
        parts.append(text(x0 + 135, 52, title, 16, AMBER_LIGHT, weight="bold"))
        bx, by, bw, bh = x0 + 30, 300, 200, 120
        pw = (bw - dz) / 2
        parts += silicon_block(bx, by, pw, bh, "#9b2c2c")
        parts += silicon_block(bx + pw, by, dz, bh, "#4a5568")
        parts += silicon_block(bx + pw + dz, by, pw, bh, "#2c5282")
        parts.append(text(bx + pw / 2, by - bh - 28, "P", 18, "#ffffff", weight="bold"))
        parts.append(text(bx + pw + dz + pw / 2, by - bh - 28, "N", 18, "#ffffff", weight="bold"))
        ncols = max(1, min(3, int(pw // 24)))
        for j in range(ncols):
            fx = (j + 0.5) / ncols
            for r in range(3):
                parts.append(f'<circle cx="{bx + pw * fx:.1f}" cy="{by - 24 - r * 34}" r="6" fill="none" stroke="{HOLE}" stroke-width="2"/>')
                parts.append(f'<circle cx="{bx + pw + dz + pw * fx:.1f}" cy="{by - 24 - r * 34}" r="5" fill="url(#eball)"/>')
        parts.append(text(bx + pw + dz / 2, by + 26, "depletion", 11, MUTED))
        parts.append(text(bx + pw + dz / 2, by + 40, "zone", 11, MUTED))
        if mode:
            plus_left = mode == "fwd"
            parts.append(text(bx - 6, by - bh / 2, "+" if plus_left else "−", 22, PRED if plus_left else NBLUE, "end", "bold"))
            parts.append(text(bx + bw + 34, by - bh / 2, "−" if plus_left else "+", 22, NBLUE if plus_left else PRED, "start", "bold"))
        if mode == "fwd":
            parts.append(f'<line x1="{bx + 20}" y1="{by + 62}" x2="{bx + bw - 10}" y2="{by + 62}" stroke="{AMBER}" stroke-width="4" marker-end="url(#arrow)"/>')
            parts.append(text(bx + bw / 2, by + 84, "conventional current, P to N", 11, AMBER_LIGHT))
        elif mode == "rev":
            parts.append(f'<line x1="{bx + 70}" y1="{by + 62}" x2="{bx + 130}" y2="{by + 62}" stroke="{RED}" stroke-width="4"/>')
            parts.append(f'<line x1="{bx + 70}" y1="{by + 52}" x2="{bx + 130}" y2="{by + 72}" stroke="{RED}" stroke-width="3"/>')
            parts.append(text(bx + bw / 2, by + 84, "blocked (a few µA leak)", 11, RED))
        else:
            parts.append(text(bx + bw / 2, by + 84, "anode = P · cathode = N", 11, TEXT))
        parts.append(text(x0 + 135, 432, note, 12, TEXT))
    return svg(w, h, "\n".join(parts), "Three 3D silicon blocks, P-type in red with holes and N-type in blue with free electrons, separated by a grey depletion zone. With no voltage the zone is thin. Forward biased, positive on the P side, the zone is squeezed almost away and current flows from P to N. Reverse biased, the zone widens and almost nothing flows.")


# 2. Check-valve analogy ------------------------------------------------------------------
def check_valve():
    w, h = 860, 380
    parts = [common_defs(cyl_gradient("pipe", "#718096"))]
    for k, (title, fwd) in enumerate((("Push forward: the flap opens", True), ("Push backward: the flap seals", False))):
        x0 = 20 + k * 420
        parts.append(panel(x0, 20, 400, 340))
        parts.append(text(x0 + 200, 52, title, 15, AMBER_LIGHT if fwd else RED, weight="bold"))
        py = 180
        parts.append(f'<rect x="{x0 + 30}" y="{py - 34}" width="340" height="68" rx="10" fill="url(#pipe)" fill-opacity="0.5"/>')
        parts.append(f'<rect x="{x0 + 196}" y="{py - 40}" width="8" height="12" fill="#2d3748"/>')
        hx, hy = x0 + 200, py - 30
        if fwd:
            parts.append(f'<line x1="{hx}" y1="{hy}" x2="{hx + 46}" y2="{hy + 26}" stroke="{AMBER}" stroke-width="7" stroke-linecap="round"/>')
            for j in range(4):
                parts.append(f'<line x1="{x0 + 60 + j * 80}" y1="{py + 14}" x2="{x0 + 110 + j * 80}" y2="{py + 14}" stroke="{NBLUE}" stroke-width="3" marker-end="url(#arrow)"/>')
            parts.append(text(x0 + 200, 260, "once the push beats the spring", 13, TEXT))
            parts.append(text(x0 + 200, 280, "(the forward voltage)", 13, MUTED))
        else:
            parts.append(f'<line x1="{hx}" y1="{hy}" x2="{hx}" y2="{hy + 60}" stroke="{AMBER}" stroke-width="7" stroke-linecap="round"/>')
            parts.append(f'<line x1="{x0 + 330}" y1="{py + 14}" x2="{x0 + 230}" y2="{py + 14}" stroke="{NBLUE}" stroke-width="3" marker-end="url(#arrow)"/>')
            parts.append(text(x0 + 200, 260, "no flow, however hard you push", 13, TEXT))
            parts.append(text(x0 + 200, 280, "(until something breaks: breakdown)", 13, MUTED))
        parts.append(text(x0 + 200, 330, "anode side → cathode side" if fwd else "cathode side → anode side", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "A diode as a check valve in a pipe. Left: flow pushing forward swings a spring-loaded flap open once the push beats the spring, the forward voltage. Right: flow pushing backward presses the flap shut, and nothing flows until something breaks.")


# 3. Part to symbol -----------------------------------------------------------------------
def anatomy():
    w, h = 860, 380
    parts = [common_defs(cyl_gradient("dbody", "#1a1a1a"))]
    parts.append(panel(20, 20, 400, 340))
    parts.append(text(220, 52, "Rectifier diode: the band is the cathode", 15, AMBER_LIGHT, weight="bold"))
    parts.append(f'<rect x="60" y="118" width="320" height="4" fill="#cbd5e0"/>')
    parts.append(f'<rect x="150" y="98" width="140" height="44" rx="10" fill="url(#dbody)"/>')
    parts.append(f'<rect x="258" y="98" width="16" height="44" fill="#e2e8f0"/>')
    parts.append(text(220, 170, "1N4001", 13, MUTED))
    # symbol
    sy = 250
    parts.append(f'<line x1="70" y1="{sy}" x2="190" y2="{sy}" stroke="{TEXT}" stroke-width="3"/>')
    parts.append(f'<polygon points="190,{sy - 22} 190,{sy + 22} 236,{sy}" fill="{TEXT}"/>')
    parts.append(f'<line x1="238" y1="{sy - 24}" x2="238" y2="{sy + 24}" stroke="{TEXT}" stroke-width="4"/>')
    parts.append(f'<line x1="238" y1="{sy}" x2="370" y2="{sy}" stroke="{TEXT}" stroke-width="3"/>')
    parts.append(text(110, sy - 16, "anode", 13, TEXT))
    parts.append(text(320, sy - 16, "cathode", 13, TEXT))
    parts.append(f'<line x1="266" y1="146" x2="240" y2="{sy - 28}" stroke="{AMBER}" stroke-dasharray="4 4" stroke-width="2"/>')
    parts.append(text(220, 320, "arrow = conventional current; bar = band", 12, MUTED, italic=True))
    parts.append(panel(440, 20, 400, 340))
    parts.append(text(640, 52, "LED: long leg anode, flat edge cathode", 15, AMBER_LIGHT, weight="bold"))
    parts += led(580, 120, "#fc5c5c", lit=True, r=26)
    parts.append(f'<line x1="610" y1="135" x2="625" y2="135" stroke="{AMBER}" stroke-width="2"/>')
    parts.append(text(632, 139, "flat on the rim", 12, AMBER_LIGHT, "start"))
    parts.append(text(560, 202, "+", 14, TEXT, weight="bold"))
    parts.append(text(600, 194, "−", 14, TEXT, weight="bold"))
    sy = 270
    parts.append(f'<line x1="480" y1="{sy}" x2="600" y2="{sy}" stroke="{TEXT}" stroke-width="3"/>')
    parts.append(f'<polygon points="600,{sy - 22} 600,{sy + 22} 646,{sy}" fill="{TEXT}"/>')
    parts.append(f'<line x1="648" y1="{sy - 24}" x2="648" y2="{sy + 24}" stroke="{TEXT}" stroke-width="4"/>')
    parts.append(f'<line x1="648" y1="{sy}" x2="790" y2="{sy}" stroke="{TEXT}" stroke-width="3"/>')
    for dx in (0, 16):
        parts.append(f'<line x1="{622 + dx}" y1="{sy - 30}" x2="{640 + dx}" y2="{sy - 48}" stroke="{AMBER}" stroke-width="2.5" marker-end="url(#arrow)"/>')
    parts.append(text(640, 330, "the outward arrows mean light comes out", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Left: a black 1N4001 rectifier diode with a white band at one end, and its schematic symbol beneath: a triangle pointing into a bar, with the band corresponding to the bar, the cathode. Right: a red LED with a longer anode leg and a flat edge on its rim on the cathode side, and the LED symbol with two arrows pointing outward.")


# 4. I-V curves ---------------------------------------------------------------------------
def iv_family():
    w, h = 880, 480
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Each diode has its own wall: the forward voltage", 16, TEXT, weight="bold"))
    L, R, T, B = 80, 830, 80, 390
    vmax, imax = 4.0, 0.030
    axes(parts, L, R, T, B, B, "forward voltage (0 to 4 V)", [(T, "30 mA"), (B - (B - T) * 20 / 30, "20 mA"), (B - (B - T) * 10 / 30, "10 mA")])
    for v in range(1, 5):
        x = L + (R - L) * v / vmax
        parts.append(text(x + 4, B - 6, f"{v} V", 11, MUTED, "start"))
    for name, fn, col in DIODES:
        pts = []
        for k in range(801):
            v = vmax * k / 800
            i = fn(v)
            if i > imax:
                pts.append((L + (R - L) * v_at(fn, imax) / vmax, T))
                break
            pts.append((L + (R - L) * v / vmax, B - (B - T) * i / imax))
        parts.append(glow_line(pts, col, 3))
        v20 = v_at(fn, 0.020)
        parts.append(text(L + (R - L) * v20 / vmax + 8, B - (B - T) * 20 / 30 + 4, f"{v20:.2f} V", 11, col, "start", "bold"))
        parts.append(text(pts[-1][0], T - 8, name, 11, col, "middle", "bold"))
    parts.append(text(w / 2, 440, "Modelled from datasheet points (Kingbright WP7113 LEDs, onsemi 1N4148 and 1N5817), 25 °C", 11, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Current against forward voltage for five diodes, each flat until it reaches its forward voltage and then rising steeply. At 20 milliamps: a Schottky about 0.23 volts, a silicon 1N4148 about 0.70, a red LED 1.85, a green LED 2.2 and a blue LED 3.3.")


# 5. Colour sets the voltage --------------------------------------------------------------
def colour_voltage():
    w, h = 880, 440
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Shorter wavelength, more energy per photon, higher forward voltage", 16, TEXT, weight="bold"))
    L, R = 80, 800
    lo, hi = 420, 680
    stops = []
    for nm, col in ((420, "#7c3aed"), (465, "#2563eb"), (500, "#06b6d4"), (530, "#22c55e"), (575, "#eab308"), (600, "#f97316"), (640, "#ef4444"), (680, "#991b1b")):
        stops.append(f'<stop offset="{(nm - lo) / (hi - lo):.3f}" stop-color="{col}"/>')
    parts.append(f'<defs><linearGradient id="spec" x1="0" x2="1">{"".join(stops)}</linearGradient></defs>')
    parts.append(f'<rect x="{L}" y="340" width="{R - L}" height="26" rx="6" fill="url(#spec)"/>')
    parts.append(text(L, 384, f"{lo} nm", 11, MUTED, "start"))
    parts.append(text(R, 384, f"{hi} nm", 11, MUTED, "end"))
    leds = [("Blue", 465, 3.3, "#4f8ef7"), ("Green", 568, 2.2, "#48bb78"), ("Red", 640, 1.85, "#fc5c5c")]
    base = 330
    scale = 45
    for name, nm, vf, col in leds:
        x = L + (R - L) * (nm - lo) / (hi - lo)
        ev = photon_ev(nm)
        parts += box3d(x - 40, base, 30, 24, ev * scale, shade(col, -0.2))
        parts += box3d(x + 4, base, 30, 24, vf * scale, "#4a5568")
        parts.append(text(x - 25, base - ev * scale - 18, f"{ev:.2f} eV", 11, col, weight="bold"))
        parts.append(text(x + 19, base - vf * scale - 18, f"{vf} V", 11, TEXT, weight="bold"))
        parts += led(x, 82, col, lit=True, r=12)
        parts.append(text(x, 128, f"{name}, {nm} nm", 12, col, weight="bold"))
    parts.append(text(L, 410, "coloured bars: energy of one photon, in electron-volts  ·  grey bars: datasheet forward voltage at 20 mA", 11, MUTED, "start", italic=True))
    return svg(w, h, "\n".join(parts), "Three LEDs placed along a visible spectrum. Blue at 465 nanometres: photon energy 2.67 electron-volts, forward voltage 3.3 volts. Green at 568: 2.18 electron-volts, 2.2 volts. Red at 640: 1.94 electron-volts, 1.85 volts. Bluer light carries more energy per photon and needs a higher forward voltage.")


# 6. Three ways to wire several LEDs ---------------------------------------------------------
def three_wirings():
    w, h = 900, 420
    parts = [common_defs()]
    cards = [("A resistor each", GREEN, "✓ each current set on its own"),
             ("A series string", GREEN, "✓ one current through all three"),
             ("One shared resistor", RED, "✗ the lowest-VF LED hogs it")]
    for k, (title, col, note) in enumerate(cards):
        x0 = 20 + k * 293
        parts.append(panel(x0, 20, 275, 380))
        parts.append(text(x0 + 137, 52, title, 15, col, weight="bold"))
        rail_x0, rail_x1 = x0 + 40, x0 + 235
        parts.append(f'<line x1="{rail_x0}" y1="90" x2="{rail_x1}" y2="90" stroke="{PRED}" stroke-width="3"/>')
        parts.append(f'<line x1="{rail_x0}" y1="320" x2="{rail_x1}" y2="320" stroke="{NBLUE}" stroke-width="3"/>')
        parts.append(text(rail_x0 - 6, 94, "+", 14, PRED, "end", "bold"))
        parts.append(text(rail_x0 - 6, 324, "−", 14, NBLUE, "end", "bold"))
        if k == 0:
            for j in range(3):
                cx = x0 + 70 + j * 68
                parts.append(f'<line x1="{cx}" y1="90" x2="{cx}" y2="320" stroke="#cbd5e0" stroke-width="2"/>')
                parts.append(f'<rect x="{cx - 8}" y="120" width="16" height="50" rx="4" fill="#d9b382"/>')
                parts += led(cx, 230, "#fc5c5c", lit=True, r=11)
        elif k == 1:
            cx = x0 + 137
            parts.append(f'<line x1="{cx}" y1="90" x2="{cx}" y2="320" stroke="#cbd5e0" stroke-width="2"/>')
            parts.append(f'<rect x="{cx - 8}" y="104" width="16" height="36" rx="4" fill="#d9b382"/>')
            for j in range(3):
                parts += led(cx, 166 + j * 52, "#fc5c5c", lit=True, r=10)
        else:
            parts.append(f'<rect x="{x0 + 129}" y="100" width="16" height="40" rx="4" fill="#d9b382"/>')
            parts.append(f'<line x1="{x0 + 137}" y1="90" x2="{x0 + 137}" y2="170" stroke="#cbd5e0" stroke-width="2"/>')
            parts.append(f'<line x1="{x0 + 70}" y1="170" x2="{x0 + 206}" y2="170" stroke="#cbd5e0" stroke-width="2"/>')
            for j, glow in enumerate((1.6, 0.6, 0.5)):
                cx = x0 + 70 + j * 68
                parts.append(f'<line x1="{cx}" y1="170" x2="{cx}" y2="320" stroke="#cbd5e0" stroke-width="2"/>')
                parts += led(cx, 236, "#fc5c5c", lit=True, r=11, glow=glow)
        parts.append(text(x0 + 137, 360, note, 12, TEXT))
    return svg(w, h, "\n".join(parts), "Three ways to wire three red LEDs. Left, each LED with its own resistor: correct. Middle, three LEDs in series with one resistor: correct, one current through all of them. Right, three LEDs in parallel sharing one resistor: wrong, the LED with the lowest forward voltage takes most of the current and glows brightest.")


# 7. The diode family ----------------------------------------------------------------------
def kinds():
    w, h = 900, 400
    parts = [common_defs(cyl_gradient("blk", "#1a1a1a") + cyl_gradient("glass", "#f6ad55"))]
    cards = [("Rectifier", "1N4001: 1 A, 50 V", "power, AC to DC", "blk", "#e2e8f0"),
             ("Small-signal", "1N4148: 100 V, 4 ns", "fast, low current", "glass", "#1a1a1a"),
             ("Schottky", "1N5817: 0.45 V at 1 A", "low forward drop", "blk", "#e2e8f0"),
             ("Zener", "1N4733A: 5.1 V", "used in reverse", "glass", "#1a1a1a"),
             ("LED", "red 1.85 V, blue 3.3 V", "light out", None, None)]
    for i, (name, part, use, grad, band) in enumerate(cards):
        cx = 95 + i * 177
        parts.append(panel(cx - 82, 20, 164, 360))
        cy = 150
        if grad:
            parts.append(f'<rect x="{cx - 70}" y="{cy - 2}" width="140" height="4" fill="#cbd5e0"/>')
            parts.append(f'<rect x="{cx - 38}" y="{cy - 18}" width="76" height="36" rx="9" fill="url(#{grad})"/>')
            parts.append(f'<rect x="{cx + 18}" y="{cy - 18}" width="10" height="36" fill="{band}"/>')
        else:
            parts += led(cx, cy - 10, "#fc5c5c", lit=True, r=20)
        parts.append(text(cx, 270, name, 16, AMBER_LIGHT, weight="bold"))
        parts.append(text(cx, 294, part, 12, TEXT))
        parts.append(text(cx, 316, use, 12, MUTED))
    return svg(w, h, "\n".join(parts), "Five members of the diode family, each with its cathode band. A black 1N4001 rectifier, 1 amp. A small glass 1N4148 signal diode, fast. A black 1N5817 Schottky, 0.45 volts at 1 amp. An orange glass 1N4733A Zener, 5.1 volts, used in reverse. And an LED.")


# 8. Rectification ---------------------------------------------------------------------------
def rectify():
    w, h = 900, 400
    parts = [common_defs()]
    titles = (("AC in", "#90cdf4"), ("Half-wave: one diode", AMBER), ("Full-wave: a bridge of four", AMBER))
    for k, (title, col) in enumerate(titles):
        x0 = 20 + k * 293
        parts.append(panel(x0, 20, 275, 360))
        parts.append(text(x0 + 137, 52, title, 15, AMBER_LIGHT if k else "#90cdf4", weight="bold"))
        L, R, mid, amp = x0 + 25, x0 + 250, 210, 90
        parts.append(f'<line x1="{L}" y1="{mid}" x2="{R}" y2="{mid}" stroke="{MUTED}"/>')
        pts = []
        for j in range(401):
            s = math.sin(4 * math.pi * j / 400)
            v = s if k == 0 else (max(s, 0) if k == 1 else abs(s))
            pts.append((L + (R - L) * j / 400, mid - amp * v))
        parts.append(glow_line(pts, col, 3))
        sub = ("swings + and −", "every other half thrown away", "both halves, flipped up")[k]
        parts.append(text(x0 + 137, 340, sub, 12, TEXT))
    return svg(w, h, "\n".join(parts), "Three waveforms. AC in swings above and below zero. After one diode, half-wave rectification keeps only the positive halves, with gaps between: pulsating DC. After a bridge of four diodes, full-wave rectification flips the negative halves up, so every half-cycle is used.")


FIGURES = {"junction.svg": junction, "check_valve.svg": check_valve, "anatomy.svg": anatomy,
           "iv_family.svg": iv_family, "colour_voltage.svg": colour_voltage,
           "three_wirings.svg": three_wirings, "kinds.svg": kinds, "rectify.svg": rectify}

if __name__ == "__main__":
    for name, fn, _ in DIODES:
        print(f"{name}: {v_at(fn, 0.020):.3f} V at 20 mA")
    render_all(FIGURES, OUT)
