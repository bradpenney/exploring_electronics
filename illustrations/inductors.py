#!/usr/bin/env python3
"""Figures for docs/inductors.md.

Sources:
- Wheeler, "Simple Inductance Formulas for Radio Coils" (Proc. IRE, 1928):
  L (uH) = d^2 n^2 / (18 d + 40 l), d and l in inches, for single-layer
  air-core coils. Every coil value below is computed from it.
- Wikipedia "Permeability (electromagnetism)": NiZn ferrite 1.26e-5 to
  2.89e-3 H/m, MnZn ferrite 4.4e-4 to 2.51e-2 H/m, iron (99.8%) 6.3e-3 H/m,
  i.e. relative permeability ~10-2,300, ~350-20,000, ~5,000.
- Wikipedia "Ignition coil": outputs from 15 kV (lawnmower) to 40 kV.
- RL circuit: i(t) = (V/R)(1 - e^(-tR/L)); V = L di/dt.

Usage:
    python3 illustrations/inductors.py
"""

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, box3d,  # noqa: E402
                     common_defs, cyl_gradient, panel, pill, render_all, shade,
                     svg, text)
from ac_dc import axes, glow_line  # noqa: E402

OUT = HERE.parent / "docs" / "images" / "inductors"
COPPER = "#c8733c"


def wheeler_uh(n, d_cm, l_cm):
    d, length = d_cm / 2.54, l_cm / 2.54
    return d * d * n * n / (18 * d + 40 * length)


def coil(cx, cy, turns, radius, length, core=None):
    """A 3D helix seen from the side: each turn is a dim back arc and a bright
    front arc, offset by one pitch so the wire visibly advances."""
    out = []
    if core:
        out += box3d(cx - length / 2 - 12, cy + radius * 0.75, length + 24, radius * 0.9, radius * 1.5, core, shadow=False)
    pitch = length / max(turns, 1)
    rx = max(radius * 0.28, 4)
    x0 = cx - length / 2
    for k in range(turns):
        x = x0 + k * pitch
        out.append(f'<path d="M{x + pitch:.1f},{cy - radius:.1f} A{rx:.1f},{radius:.1f} 0 0 0 {x + pitch:.1f},{cy + radius:.1f}" '
                   f'fill="none" stroke="{shade(COPPER, -0.55)}" stroke-width="2.5"/>')
    for k in range(turns):
        x = x0 + k * pitch
        out.append(f'<path d="M{x:.1f},{cy + radius:.1f} A{rx:.1f},{radius:.1f} 0 0 0 {x + pitch:.1f},{cy - radius:.1f}" '
                   f'fill="none" stroke="{COPPER}" stroke-width="3.5" stroke-linecap="round"/>')
    out.append(f'<ellipse cx="{cx:.1f}" cy="{cy + radius + 14:.1f}" rx="{length / 2 + 10:.1f}" ry="6" fill="#000" fill-opacity="0.35"/>')
    return out


# 1. Inertia: the flywheel picture -----------------------------------------------------------
def flywheel():
    w, h = 860, 400
    parts = [common_defs(cyl_gradient("pipe", "#718096"))]
    for k, (title, sub, spin) in enumerate((("Starting the flow", "the wheel must be spun up: flow builds slowly", 1),
                                           ("Stopping the flow", "the spinning wheel keeps pushing: a pressure surge", -1))):
        x0 = 20 + k * 420
        parts.append(panel(x0, 20, 400, 360))
        parts.append(text(x0 + 200, 52, title, 15, AMBER_LIGHT, weight="bold"))
        py = 200
        parts.append(f'<rect x="{x0 + 30}" y="{py - 26}" width="340" height="52" rx="10" fill="url(#pipe)" fill-opacity="0.45"/>')
        parts.append(f'<circle cx="{x0 + 200}" cy="{py}" r="62" fill="#2d3748" stroke="#a0aec0" stroke-width="4"/>')
        for j in range(6):
            a = math.radians(j * 60 + (15 if k else 0))
            parts.append(f'<line x1="{x0 + 200}" y1="{py}" x2="{x0 + 200 + 58 * math.cos(a):.1f}" y2="{py + 58 * math.sin(a):.1f}" stroke="#cbd5e0" stroke-width="5"/>')
        parts.append(f'<circle cx="{x0 + 200}" cy="{py}" r="12" fill="url(#core)"/>')
        if k == 0:
            for j, wdt in enumerate((1.5, 2.5, 3.5)):
                parts.append(f'<line x1="{x0 + 50 + j * 30}" y1="{py}" x2="{x0 + 70 + j * 30}" y2="{py}" stroke="#90cdf4" stroke-width="{wdt}" marker-end="url(#arrow)"/>')
            parts.append(text(x0 + 200, 296, "pump switched on", 13, TEXT))
        else:
            parts.append(f'<line x1="{x0 + 290}" y1="{py}" x2="{x0 + 335}" y2="{py}" stroke="{RED}" stroke-width="4" marker-end="url(#arrow)"/>')
            parts.append(f'<rect x="{x0 + 345}" y="{py - 30}" width="10" height="60" fill="{RED}"/>')
            parts.append(text(x0 + 350, py - 40, "valve slammed", 12, RED, "end"))
            parts.append(text(x0 + 200, 296, "flow cut off suddenly", 13, TEXT))
        parts.append(text(x0 + 200, 330, sub, 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "An inductor pictured as a heavy flywheel turned by water in a pipe. Left: when the pump starts, the wheel has to be spun up, so the flow builds slowly. Right: when a valve slams shut, the spinning wheel keeps pushing water and causes a pressure surge.")


# 2. Current rise and the switch-off spike ---------------------------------------------------
def rl_curves():
    w, h = 900, 440
    parts = [common_defs()]
    L_H, R_OHM, V = 0.1, 20.0, 12.0
    tau = L_H / R_OHM
    parts.append(panel(20, 20, 420, 400))
    parts.append(text(230, 52, "Switch on: current builds over τ = L ÷ R", 15, AMBER_LIGHT, weight="bold"))
    Lx, Rx, T, B = 70, 420, 90, 360
    axes(parts, Lx, Rx, T, B, B, f"time (0 to 25 ms); τ = {tau * 1000:.0f} ms", [(T, f"{V / R_OHM:.1f} A"), (B - 0.632 * (B - T), "63%")])
    pts = [(Lx + (Rx - Lx) * k / 400, B - (B - T) * (1 - math.exp(-(0.025 * k / 400) / tau))) for k in range(401)]
    parts.append(glow_line(pts, AMBER))
    parts.append(text(240, 400, "100 mH coil with 20 Ω of wire, on 12 V", 11, MUTED, italic=True))
    parts.append(panel(460, 20, 420, 400))
    parts.append(text(670, 52, "Switch off: the coil fights back", 15, RED, weight="bold"))
    Lx, Rx, T, B = 520, 860, 90, 360
    parts.append(f'<line x1="{Lx}" y1="{B - 60}" x2="{Rx}" y2="{B - 60}" stroke="{MUTED}"/>')
    parts.append(f'<line x1="{Lx}" y1="{T}" x2="{Lx}" y2="{B}" stroke="{MUTED}"/>')
    parts.append(text(Lx - 6, B - 56, "0 V", 11, MUTED, "end"))
    parts.append(text(Lx - 6, B - 104, "12 V", 11, MUTED, "end"))
    sx = Lx + 120
    pts = [(Lx, B - 108), (sx, B - 108), (sx, T + 6), (sx + 6, B - 60), (Rx, B - 60)]
    parts.append(glow_line(pts, RED))
    vspike = L_H * (V / R_OHM) / 1e-6
    parts.append(text(sx + 14, T + 20, f"L × ΔI ÷ Δt = 0.1 H × 0.6 A ÷ 1 µs", 12, RED, "start", "bold"))
    parts.append(text(sx + 14, T + 38, f"= {vspike:,.0f} V, in theory", 12, RED, "start", "bold"))
    parts.append(text(sx + 14, T + 60, "in practice an arc across the", 12, TEXT, "start"))
    parts.append(text(sx + 14, T + 76, "switch contacts, or a dead transistor", 12, TEXT, "start"))
    parts.append(text(670, 400, "coil voltage when the switch opens in 1 µs, no diode", 11, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Left: the current through a 100 millihenry coil with 20 ohms of wire, connected to 12 volts, rises over a time constant of 5 milliseconds toward 0.6 amps. Right: when the switch opens in 1 microsecond, the coil's voltage spikes; L times the change in current over time gives 60,000 volts in theory, in practice an arc across the switch or a destroyed transistor.")


# 3. What sets L ------------------------------------------------------------------------------
def what_sets_l():
    w, h = 900, 400
    parts = [common_defs()]
    cases = [("Starting coil", 20, 2.5, 5, "20 turns, 2.5 cm across, 5 cm long"),
             ("Twice the turns", 40, 2.5, 5, "40 turns, same size"),
             ("Twice the diameter", 20, 5.0, 5, "5 cm across"),
             ("Stretched to twice the length", 20, 2.5, 10, "10 cm long")]
    for i, (title, n, d, length, sub) in enumerate(cases):
        cx = 115 + i * 223
        parts.append(panel(cx - 104, 20, 208, 360))
        parts.append(text(cx, 52, title, 14, AMBER_LIGHT, weight="bold"))
        parts += coil(cx, 170, n // 2, 12 * d, 16 * length)
        L = wheeler_uh(n, d, length)
        parts.append(text(cx, 290, f"{L:.1f} µH", 24, TEXT, weight="bold"))
        parts.append(text(cx, 318, sub, 11, MUTED))
    parts.append(text(450, 365, "single-layer air-core coils, Wheeler's formula", 11, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Four air-core coils with inductance from Wheeler's formula. 20 turns, 2.5 centimetres across and 5 long: 4.0 microhenries. Twice the turns in the same space: 16.1. Twice the diameter: 13.6. Stretched to twice the length: 2.2.")


# 4. Series and parallel ----------------------------------------------------------------------
def series_parallel():
    w, h = 860, 360
    parts = [common_defs(), panel(15, 15, 405, h - 30), panel(440, 15, 405, h - 30)]
    parts.append(text(217, 48, "Series: inductances add", 16, AMBER_LIGHT, weight="bold"))
    parts += coil(140, 160, 8, 26, 120) + coil(295, 160, 8, 26, 120)
    parts.append(f'<line x1="40" y1="186" x2="80" y2="186" stroke="#cbd5e0" stroke-width="3"/>')
    parts.append(f'<line x1="355" y1="186" x2="395" y2="186" stroke="#cbd5e0" stroke-width="3"/>')
    parts.append(text(140, 120, "12 mH", 13, TEXT))
    parts.append(text(295, 120, "12 mH", 13, TEXT))
    parts.append(text(217, 260, "L = L₁ + L₂ = 24 mH", 16, TEXT, weight="bold"))
    parts.append(text(217, 284, "like resistors in series", 12, MUTED, italic=True))
    parts.append(text(642, 48, "Parallel: like parallel resistors", 16, AMBER_LIGHT, weight="bold"))
    parts += coil(642, 120, 8, 24, 120) + coil(642, 205, 8, 24, 120)
    parts.append(text(642, 92, "20 mH", 13, TEXT))
    parts.append(text(642, 250, "20 mH", 13, TEXT))
    parts.append(text(642, 290, "1/L = 1/L₁ + 1/L₂ → 10 mH", 16, TEXT, weight="bold"))
    parts.append(text(642, 314, "(coils far apart, fields not coupled)", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Left: two 12 millihenry coils in series make 24 millihenries, adding like resistors in series. Right: two 20 millihenry coils in parallel make 10 millihenries, combining like resistors in parallel, provided their fields don't couple.")


# 5. Kinds of inductors -----------------------------------------------------------------------
def kinds():
    w, h = 900, 400
    parts = [common_defs(cyl_gradient("ferr", "#2d3748") + cyl_gradient("mold", "#38a169"))]
    cards = [("Air core", "nH to tens of µH", "radio tuning, VHF"),
             ("Ferrite rod", "µH to mH", "AM radio antennas"),
             ("Toroid", "µH to mH", "field stays in the ring"),
             ("Iron-core choke", "mH to henries", "power-line filtering"),
             ("Moulded / chip", "nH to mH", "on circuit boards")]
    for i, (name, rng, use) in enumerate(cards):
        cx = 95 + i * 177
        parts.append(panel(cx - 82, 20, 164, 360))
        cy = 150
        if i == 0:
            parts += coil(cx, cy, 7, 28, 90)
        elif i == 1:
            parts.append(f'<rect x="{cx - 66}" y="{cy - 12}" width="132" height="24" rx="12" fill="url(#ferr)"/>')
            parts += coil(cx, cy, 9, 18, 80)
        elif i == 2:
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="46" fill="none" stroke="#4a5568" stroke-width="24"/>')
            for k in range(18):
                a = math.radians(k * 20)
                x1, y1 = cx + 32 * math.cos(a), cy + 32 * math.sin(a)
                x2, y2 = cx + 60 * math.cos(a), cy + 60 * math.sin(a)
                parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{COPPER}" stroke-width="3.5"/>')
        elif i == 3:
            parts += box3d(cx - 50, cy + 50, 100, 30, 100, "#4a5568")
            parts.append(f'<rect x="{cx - 32}" y="{cy - 36}" width="64" height="72" rx="8" fill="{COPPER}"/>')
            parts.append(f'<rect x="{cx - 32}" y="{cy - 36}" width="64" height="72" rx="8" fill="url(#gloss)"/>')
        else:
            parts.append(f'<rect x="{cx - 70}" y="{cy - 2}" width="140" height="4" fill="#cbd5e0"/>')
            parts.append(f'<rect x="{cx - 36}" y="{cy - 16}" width="72" height="32" rx="14" fill="url(#mold)"/>')
            for k, col in enumerate(("#e53e3e", "#e53e3e", "#2d3748", "#d69e2e")):
                parts.append(f'<rect x="{cx - 24 + k * 13}" y="{cy - 16}" width="6" height="32" fill="{col}"/>')
            parts += box3d(cx - 14, cy + 60, 28, 16, 12, "#4a5568")
        parts.append(text(cx, 280, name, 15, AMBER_LIGHT, weight="bold"))
        parts.append(text(cx, 304, rng, 12, TEXT))
        parts.append(text(cx, 324, use, 12, MUTED))
    return svg(w, h, "\n".join(parts), "Five kinds of inductor. An air-core coil, nanohenries to tens of microhenries, for radio tuning. A coil on a ferrite rod, used in AM radio antennas. A toroid, a ring-shaped core that keeps its field inside. An iron-core choke, millihenries to henries, for power filtering. And a moulded inductor with colour bands, beside a tiny chip inductor.")


# 6. Ignition: 12 V to a spark --------------------------------------------------------------
def ignition():
    w, h = 900, 400
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "A 12 V battery, a coil, and a sudden stop: 15 to 40 kV", 16, TEXT, weight="bold"))
    parts += box3d(60, 280, 120, 60, 90, "#2d3748")
    parts.append(text(120, 236, "12 V", 18, "#ffffff", weight="bold"))
    parts.append(text(120, 310, "car battery", 12, MUTED))
    parts.append(f'<line x1="200" y1="220" x2="300" y2="220" stroke="#cbd5e0" stroke-width="4"/>')
    parts.append(text(250, 205, "a few amps build", 11, TEXT))
    parts.append(text(250, 250, "then switched off", 11, RED, weight="bold"))
    parts.append(f'<line x1="250" y1="225" x2="270" y2="238" stroke="{RED}" stroke-width="3"/>')
    parts += box3d(310, 290, 180, 50, 150, "#4a5568")
    parts += coil(400, 175, 6, 30, 100)
    parts += coil(400, 245, 16, 18, 120)
    parts.append(text(400, 130, "primary: few turns", 11, TEXT))
    parts.append(text(400, 316, "secondary: thousands of turns", 11, TEXT))
    parts.append(f'<line x1="520" y1="215" x2="640" y2="215" stroke="{AMBER}" stroke-width="5" marker-end="url(#arrow)"/>')
    parts.append(text(580, 200, "self-induced kick,", 11, AMBER_LIGHT))
    parts.append(text(580, 240, "stepped up", 11, AMBER_LIGHT))
    parts.append(f'<rect x="680" y="150" width="40" height="110" rx="6" fill="#e2e8f0"/>')
    parts.append(f'<rect x="690" y="260" width="20" height="30" fill="#a0aec0"/>')
    parts.append(f'<ellipse cx="700" cy="304" rx="40" ry="22" fill="url(#glow)"/>')
    parts.append(f'<path d="M700,292 L694,302 L704,304 L698,316" fill="none" stroke="#fff7e0" stroke-width="3" filter="url(#softglow)"/>')
    parts.append(text(780, 220, "spark plug", 13, TEXT, "start"))
    parts.append(text(780, 240, "15 to 40 kV", 13, AMBER_LIGHT, "start", "bold"))
    return svg(w, h, "\n".join(parts), "A car's 12 volt battery drives a few amps through the ignition coil's primary winding. When that current is switched off, the primary's self-induced voltage is stepped up by a secondary of thousands of turns, and the spark plug fires at 15 to 40 kilovolts.")


FIGURES = {"flywheel.svg": flywheel, "rl_curves.svg": rl_curves, "what_sets_l.svg": what_sets_l,
           "series_parallel.svg": series_parallel, "kinds.svg": kinds, "ignition.svg": ignition}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
