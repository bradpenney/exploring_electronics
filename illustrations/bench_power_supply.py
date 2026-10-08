#!/usr/bin/env python3
"""Figures for docs/tools/bench_power_supply.md.

Sources:
- Rigol DP800 series datasheet and user guide (DP832): CV mode holds the set
  voltage with current set by the load; CC mode holds the set current with
  voltage set by the load; switches automatically; 30 V / 3 A channels;
  ripple and noise < 350 uVrms / 2 mVpp; readback accuracy 0.05 % + 10 mV,
  0.15 % + 5 mA; sense terminals compensate for lead voltage drop.
- Batteries: alkaline AA internal resistance 150-300 mOhm (Energizer, see
  batteries.md), so four in series are 0.6-1.2 Ohm.
- Wire resistance: 22 AWG 5.16 Ohm and 18 AWG 2.04 Ohm per 100 m (resistance.md).
Every number below is computed.

Usage:
    python3 illustrations/bench_power_supply.py
"""

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, box3d,  # noqa: E402
                     common_defs, panel, pill, render_all, shade, svg, text)
from ac_dc import axes, glow_line  # noqa: E402

OUT = HERE.parent / "docs" / "images" / "bench_power_supply"
BLUE = "#4299e1"
VSET, ISET = 5.0, 0.1


def operate(r):
    """CV/CC operating point for a resistive load r."""
    if VSET / r < ISET:
        return VSET, VSET / r, "CV"
    return ISET * r, ISET, "CC"


def _lcd(parts, x, y, w, h, reading, unit, col):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#0b1020"/>')
    parts.append(f'<text x="{x + w - 46}" y="{y + h * 0.72:.1f}" font-size="{h * 0.55:.0f}" fill="{col}" '
                 f'text-anchor="end" font-family="DejaVu Sans Mono, monospace" font-weight="bold">{reading}</text>')
    parts.append(text(x + w - 14, y + h * 0.7, unit, 16, col, "end", weight="bold"))


# 1. The front panel ---------------------------------------------------------------------------------
def front_panel():
    w, h = 900, 500
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    bx, by, bw, bh = 250, 90, 400, 300
    parts += box3d(bx, by + bh, bw, 70, bh, "#4a5568")
    parts.append(f'<rect x="{bx + 14}" y="{by + 14}" width="{bw - 28}" height="{bh - 28}" rx="10" fill="#2d3748"/>')
    _lcd(parts, bx + 30, by + 30, 200, 60, "5.000", "V", "#68d391")
    _lcd(parts, bx + 30, by + 100, 200, 60, "0.045", "A", "#fbd38d")
    parts.append(f'<rect x="{bx + 245}" y="{by + 30}" width="54" height="28" rx="5" fill="{GREEN}"/>')
    parts.append(text(bx + 272, by + 50, "CV", 15, "#1a1a1a", weight="bold"))
    parts.append(f'<rect x="{bx + 245}" y="{by + 66}" width="54" height="28" rx="5" fill="#4a5568"/>')
    parts.append(text(bx + 272, by + 86, "CC", 15, "#a0aec0", weight="bold"))
    for k, lab in enumerate(("VOLTAGE", "CURRENT")):
        cx = bx + 70 + k * 120
        parts.append(f'<circle cx="{cx}" cy="{by + 215}" r="26" fill="url(#core)"/>')
        parts.append(f'<line x1="{cx}" y1="{by + 215}" x2="{cx + 12}" y2="{by + 195}" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>')
        parts.append(text(cx, by + 258, lab, 11, TEXT, weight="bold"))
    for k, (lab, col) in enumerate((("+", RED), ("−", "#1a1a1a"), ("⏚", GREEN))):
        cx = bx + 270 + k * 40
        parts.append(f'<circle cx="{cx}" cy="{by + 215}" r="14" fill="{col}" stroke="#cbd5e0" stroke-width="2"/>')
        parts.append(text(cx, by + 248, lab, 14, TEXT, weight="bold"))
    parts.append(f'<rect x="{bx + 300}" y="{by + 130}" width="70" height="30" rx="6" fill="#c05621"/>')
    parts.append(text(bx + 335, by + 151, "OUTPUT", 11, "#ffffff", weight="bold"))

    def callout(x1, y1, x2, y2, label, sub, anchor):
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{MUTED}" stroke-width="1.5"/>')
        parts.append(f'<circle cx="{x1}" cy="{y1}" r="4" fill="{AMBER_LIGHT}"/>')
        dx = -8 if anchor == "end" else 8
        parts.append(text(x2 + dx, y2 - 4, label, 14, AMBER_LIGHT, anchor, weight="bold"))
        parts.append(text(x2 + dx, y2 + 13, sub, 11, MUTED, anchor, italic=True))
    callout(bx + 30, by + 60, 200, 110, "Voltage readback", "what the output is", "end")
    callout(bx + 30, by + 130, 200, 200, "Current readback", "what the circuit draws", "end")
    callout(bx + 70, by + 215, 200, 300, "Two knobs", "set the voltage, set the limit", "end")
    callout(bx + 299, by + 44, 710, 120, "CV / CC lamp", "which limit is in charge", "start")
    callout(bx + 370, by + 145, 710, 210, "Output button", "off while you wire", "start")
    callout(bx + 350, by + 215, 710, 300, "Terminals", "+, −, and a separate earth", "start")
    return svg(w, h, "\n".join(parts), "A 3D bench power supply. Two displays read 5.000 volts and 0.045 amps. A lit lamp says CV, constant voltage; a dark one says CC. Two knobs set the voltage and the current limit. An output button switches the terminals on and off, and three terminals give plus, minus and a separate earth.")


# 2. The CV/CC boundary in the V-I plane ----------------------------------------------------------------
def cv_cc_curve():
    w, h = 900, 500
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Set 5 V and a 100 mA limit: the output lives on the amber boundary", 17, AMBER_LIGHT, weight="bold"))
    L, R, T, B = 110, 820, 90, 390
    xi = lambda i: L + i / 0.15 * (R - L)
    yv = lambda v: B - v / 7 * (B - T)
    axes(parts, L, R, T, B, B, "", [(yv(v), f"{v} V") for v in (1, 2, 3, 4, 5, 6)])
    for i in (0, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15):
        parts.append(text(xi(i), B + 20, f"{i * 1000:.0f} mA", 11, MUTED))
    parts.append(text((L + R) / 2, B + 42, "output current", 12, MUTED))
    # boundary
    parts.append(glow_line([(xi(0), yv(VSET)), (xi(ISET), yv(VSET)), (xi(ISET), yv(0))], "#f6ad55", 4))
    parts.append(text(xi(0.003), yv(VSET) + 22, "CV: voltage held at 5 V", 13, GREEN, "start", weight="bold"))
    parts.append(text(xi(ISET) + 10, yv(2.6), "CC: current held at 100 mA", 13, "#f6ad55", "start", weight="bold"))
    for r, col in [(100, "#90cdf4"), (50, AMBER_LIGHT), (20, "#fc8181")]:
        i_end = min(0.15, 7 / r)
        parts.append(f'<line x1="{xi(0):.1f}" y1="{yv(0):.1f}" x2="{xi(i_end):.1f}" y2="{yv(i_end * r):.1f}" stroke="{col}" stroke-width="1.5" stroke-dasharray="5 4"/>')
        v, i, mode = operate(r)
        parts.append(f'<circle cx="{xi(i):.1f}" cy="{yv(v):.1f}" r="7" fill="{col}"/>')
        lab = f"{r} Ω: {v:g} V, {i * 1000:.0f} mA" + (" (crossover)" if r == 50 else f", {mode}")
        dy = 24 if r == 100 else (24 if r == 20 else -34)
        parts.append(text(xi(i) + (12 if r != 50 else -10), yv(v) + dy, lab, 12, col, "start" if r != 50 else "end", weight="bold"))
    parts.append(text((L + R) / 2, 462, "dashed lines: each load's own V = I × R. The output sits where the load line meets the boundary.", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "A voltage against current graph with the supply's boundary: a horizontal line at 5 volts out to 100 milliamps, then a vertical line down at 100 milliamps. Three dashed load lines from the origin meet it: a 100 ohm load at 5 volts and 50 milliamps in constant voltage; a 50 ohm load at the corner, the crossover, 5 volts and 100 milliamps; a 20 ohm load at 2 volts and 100 milliamps in constant current.")


# 3. Sweeping the load ---------------------------------------------------------------------------------------
def load_sweep():
    w, h = 900, 460
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Voltage and current as the load resistance falls (5 V, 100 mA limit)", 17, AMBER_LIGHT, weight="bold"))
    L, R, T, B = 110, 780, 90, 380
    lo, hi = -1, 3  # 0.1 ohm .. 1 kOhm
    xr = lambda r: R - (math.log10(r) - lo) / (hi - lo) * (R - L)
    yv = lambda v: B - v / 6 * (B - T)
    yi = lambda i: B - i / 0.12 * (B - T)
    axes(parts, L, R, T, B, B, "", [(yv(v), f"{v} V") for v in (1, 2, 3, 4, 5)])
    for i in (0.025, 0.05, 0.075, 0.1):
        parts.append(text(R + 8, yi(i) + 4, f"{i * 1000:.0f} mA", 11, "#f6ad55", "start"))
    for e, lab in [(3, "1 kΩ"), (2, "100 Ω"), (1, "10 Ω"), (0, "1 Ω"), (-1, "0.1 Ω")]:
        parts.append(text(xr(10 ** e), B + 20, lab, 11, MUTED))
    parts.append(text((L + R) / 2, B + 42, "load resistance, falling to the right (log scale)", 12, MUTED))
    pv, pi = [], []
    for k in range(301):
        r = 10 ** (hi - (hi - lo) * k / 300)
        v, i, _ = operate(r)
        pv.append((xr(r), yv(v)))
        pi.append((xr(r), yi(i)))
    parts.append(glow_line(pv, GREEN, 3))
    parts.append(glow_line(pi, "#f6ad55", 3))
    x50 = xr(50)
    parts.append(f'<line x1="{x50:.1f}" y1="{T}" x2="{x50:.1f}" y2="{B}" stroke="{MUTED}" stroke-dasharray="5 4"/>')
    parts.append(text(x50, T - 6, "50 Ω: crossover", 12, MUTED))
    parts.append(text(xr(400), yv(5) - 12, "voltage (CV)", 13, GREEN, weight="bold"))
    parts.append(text(xr(300), yi(0.02) - 12, "current", 13, "#f6ad55", weight="bold"))
    parts.append(text(xr(0.5), yv(0.4) - 14, "a short: 100 mA at 0.01 V", 12, "#fc8181", weight="bold"))
    return svg(w, h, "\n".join(parts), "Two curves as the load resistance falls from 1 kilohm to 0.1 ohm on a log scale. The voltage holds at 5 volts while the current rises, until the load reaches 50 ohms, the crossover. Below that the current holds at 100 milliamps and the voltage falls, until a short circuit sees 100 milliamps at only 0.01 volts.")


# 4. A short on a battery versus a bench supply ----------------------------------------------------------------
def short_compare():
    w, h = 900, 430
    parts = [common_defs(), panel(15, 15, 425, h - 30), panel(460, 15, 425, h - 30)]
    cases = [(227, "Four AA cells, 0.1 Ω short", [6 / (1.2 + 0.1), 6 / (0.6 + 0.1)], "limited only by the cells' own resistance", RED),
             (672, "Bench supply, 100 mA limit", [ISET], "limited by the setting", GREEN)]
    base = 330
    for cx, title, currents, sub, col in cases:
        parts.append(text(cx, 50, title, 16, AMBER_LIGHT, weight="bold"))
        top = max(currents)
        hgt = max(8, top / 9 * 220)
        parts += box3d(cx - 50, base, 100, 44, hgt, col)
        lab = (f"{min(currents):.1f} to {max(currents):.1f} A" if len(currents) > 1 else f"{top * 1000:.0f} mA")
        parts.append(text(cx + 18, base - hgt - 26, lab, 17, TEXT, weight="bold"))
        parts.append(text(cx, base + 34, sub, 12, MUTED, italic=True))
        heat = [c ** 2 * 0.1 for c in currents]
        hl = (f"{min(heat):.1f} to {max(heat):.1f} W heating the short" if len(heat) > 1 else f"{heat[0] * 1000:.0f} mW heating the short")
        parts.append(text(cx, base + 54, hl, 13, col, weight="bold"))
    parts.append(text(w / 2, 410, "bars on the same scale; alkaline AA internal resistance 150 to 300 mΩ each", 11, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Two 3D bars for the same 0.1 ohm short circuit. Four alkaline AA cells, with 0.6 to 1.2 ohms of internal resistance between them, push 4.6 to 8.6 amps, heating the short with 2.1 to 7.3 watts. A bench supply with a 100 milliamp limit pushes 100 milliamps, heating it with 1 milliwatt.")


# 5. Lead drop and sense terminals -------------------------------------------------------------------------------
def lead_drop():
    w, h = 900, 420
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "1 m leads each way at 2 A: the voltage the circuit actually gets", 17, AMBER_LIGHT, weight="bold"))
    base = 320
    cases = [("22 AWG hookup wire", 5.16), ("18 AWG lamp cord", 2.04)]
    for k, (name, per100) in enumerate(cases):
        r = 2 * per100 / 100
        drop = r * 2
        x = 170 + k * 290
        hgt_set = 5 / 6 * 200
        hgt_load = (5 - drop) / 6 * 200
        parts += box3d(x, base, 70, 36, hgt_set, "#4a5568")
        parts += box3d(x + 100, base, 70, 36, hgt_load, AMBER if drop > 0.1 else GREEN)
        parts.append(text(x + 35, base - hgt_set - 24, "5.00 V", 13, TEXT, weight="bold"))
        parts.append(text(x + 135, base - hgt_load - 24, f"{5 - drop:.2f} V", 13, TEXT, weight="bold"))
        parts.append(text(x + 35, base + 24, "at the supply", 11, MUTED))
        parts.append(text(x + 135, base + 24, "at the circuit", 11, MUTED))
        parts.append(text(x + 85, base + 48, f"{name}: {r * 1000:.0f} mΩ, {drop:.2f} V lost", 12, TEXT, weight="bold"))
    x = 760
    parts += box3d(x - 35, base, 70, 36, 5 / 6 * 200, GREEN)
    parts.append(text(x, base - 5 / 6 * 200 - 24, "5.00 V", 13, TEXT, weight="bold"))
    parts.append(text(x, base + 24, "with sense leads", 11, MUTED))
    parts.append(text(x, base + 48, "supply raises its output", 12, TEXT, weight="bold"))
    parts.append(text(x, base + 64, "to make up the drop", 12, TEXT, weight="bold"))
    return svg(w, h, "\n".join(parts), "Pairs of 3D bars for a supply set to 5 volts driving 2 amps through 1 metre leads each way. With 22 AWG hookup wire the leads are 103 milliohms and the circuit gets 4.79 volts. With 18 AWG lamp cord they are 41 milliohms and it gets 4.92 volts. With sense leads the supply measures at the circuit and raises its output, so the circuit gets 5.00 volts.")


FIGURES = {"front_panel.svg": front_panel, "cv_cc_curve.svg": cv_cc_curve, "load_sweep.svg": load_sweep,
           "short_compare.svg": short_compare, "lead_drop.svg": lead_drop}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
