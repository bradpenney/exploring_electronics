#!/usr/bin/env python3
"""Figures for docs/voltage_regulators.md.

Sources:
- TI LM340 / LM7805 datasheet (SNOSBT0): 5 V output, up to 1.5 A; dropout
  2 V at 1 A; TO-220 junction-to-ambient thermal resistance 23.9 C/W (Thermal
  Information table); TJ max 125 C; thermal shutdown above 150 C; quiescent
  current about 6 mA; ripple rejection 68-80 dB at 120 Hz.
- TI LM2596 datasheet: 3 A step-down (buck) switching regulator, 150 kHz;
  efficiency 80 % for the 5 V version at VIN = 12 V, ILOAD = 3 A.
- TI LM1117 datasheet: low-dropout regulator, 800 mA, dropout 1.2 V at
  800 mA.
- Linear regulator: input current = output current, so P_heat = (Vin - Vout) I.
Every number below is computed from those.

Usage:
    python3 illustrations/voltage_regulators.py
"""

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, box3d,  # noqa: E402
                     common_defs, panel, pill, render_all, shade, svg, text)
from ac_dc import axes, glow_line  # noqa: E402

OUT = HERE.parent / "docs" / "images" / "voltage_regulators"
BLUE = "#4299e1"
VIN, VOUT = 12.0, 5.0
THETA_JA = 23.9
TJ_MAX, T_SHUT, T_AMB = 125, 150, 25
SW_EFF = 0.80
DROP_7805, DROP_1117 = 2.0, 1.2


# 1. Two ways to make 5 V -------------------------------------------------------------------
def two_ways():
    w, h = 900, 470
    parts = [common_defs(), panel(15, 15, 425, h - 30), panel(460, 15, 425, h - 30)]
    i_out = 3.0
    p_out = VOUT * i_out
    cases = [(227, "Linear regulator", p_out / (VOUT / VIN), i_out),
             (672, "Switching regulator (LM2596)", p_out / SW_EFF, p_out / SW_EFF / VIN)]
    scale = 7.0  # px per watt
    base = 380
    for cx, title, p_in, i_in in cases:
        heat = p_in - p_out
        parts.append(text(cx, 50, title, 17, AMBER_LIGHT, weight="bold"))
        parts.append(text(cx, 72, "12 V in, 5 V at 3 A out", 12, MUTED, italic=True))
        bx = cx - 60
        parts += box3d(bx, base, 90, 50, p_out * scale, GREEN)
        parts += box3d(bx, base - p_out * scale, 90, 50, heat * scale, RED, shadow=False)
        parts.append(text(bx + 45, base - p_out * scale / 2 + 5, f"{p_out:.0f} W", 15, "#1a1a1a", weight="bold"))
        parts.append(text(bx + 45, base - p_out * scale / 2 + 22, "to the load", 11, "#1a1a1a"))
        if heat * scale > 30:
            parts.append(text(bx + 45, base - p_out * scale - heat * scale / 2 + 5, f"{heat:g} W", 15, "#ffffff", weight="bold"))
            parts.append(text(bx + 45, base - p_out * scale - heat * scale / 2 + 22, "as heat", 11, "#ffffff"))
        else:
            parts.append(text(bx + 150, base - p_out * scale - heat * scale / 2 + 5, f"{heat:g} W as heat", 13, RED, "start", weight="bold"))
        top = base - (p_out + heat) * scale
        parts.append(text(bx + 60, top - 26, f"{p_in:g} W in", 15, TEXT, weight="bold"))
        parts.append(text(cx, base + 34, f"draws {i_in:.2f} A from the 12 V supply", 12, MUTED))
        parts.append(text(cx, base + 52, f"{p_out / p_in * 100:.0f}% efficient", 13, AMBER_LIGHT, weight="bold"))
    return svg(w, h, "\n".join(parts), "Two stacked 3D bars for making 5 volts at 3 amps from 12 volts. A linear regulator takes in 36 watts: 15 go to the load and 21 become heat, 42 percent efficient, drawing the full 3 amps from the supply. The LM2596 switching regulator takes in 18.75 watts: 15 to the load and 3.75 as heat, 80 percent efficient, drawing only 1.56 amps.")


# 2. A linear regulator: an automatic resistor -------------------------------------------------
def linear_idea():
    w, h = 900, 440
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "A linear regulator: a transistor that soaks up the difference", 17, AMBER_LIGHT, weight="bold"))
    base, scale = 330, 20
    parts += box3d(90, base, 90, 50, VIN * scale, AMBER)
    parts.append(text(135, base - VIN * scale - 26, "12 V in", 15, TEXT, weight="bold"))
    parts += box3d(640, base, 90, 50, VOUT * scale, GREEN)
    parts.append(text(685, base - VOUT * scale - 26, "5 V out", 15, TEXT, weight="bold"))
    # pass element
    parts.append(f'<ellipse cx="410" cy="190" rx="110" ry="70" fill="url(#glow)"/>')
    parts += box3d(350, 240, 120, 50, 100, "#c53030", shadow=True)
    parts.append(text(410, 185, "pass", 15, "#ffffff", weight="bold"))
    parts.append(text(410, 203, "transistor", 15, "#ffffff", weight="bold"))
    parts.append(text(410, 222, "drops 7 V", 12, "#ffffff"))
    parts.append(f'<path d="M190,190 L345,190" stroke="{AMBER_LIGHT}" stroke-width="4" marker-end="url(#arrow)"/>')
    parts.append(f'<path d="M505,190 L630,220" stroke="{AMBER_LIGHT}" stroke-width="4" marker-end="url(#arrow)"/>')
    # feedback
    parts.append(f'<path d="M685,345 C685,395 410,395 410,300" stroke="#90cdf4" stroke-width="3" fill="none" stroke-dasharray="7 5" marker-end="url(#arrow)"/>')
    parts.append(text(548, 408, "feedback: compare the output with a fixed reference, open or close the pass transistor", 12, "#90cdf4", italic=True))
    return svg(w, h, "\n".join(parts), "A 12 volt amber column on the left and a 5 volt green column on the right, with a glowing red pass transistor between them that drops the 7 volt difference as heat. A dashed feedback loop from the output back to the transistor compares the output with a fixed reference and opens or closes the transistor to hold it at 5 volts.")


# 3. Heat in a 7805 without a heat sink ---------------------------------------------------------
def heat_curve():
    w, h = 900, 470
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "A 7805 in TO-220 with no heat sink, 12 V in, 5 V out", 17, AMBER_LIGHT, weight="bold"))
    L, R, T, B = 110, 840, 90, 380
    xi = lambda i: L + i / 1.0 * (R - L)
    yt = lambda t: B - t / 200 * (B - T)
    ticks = [(yt(t), f"{t} °C") for t in (25, 50, 100, 125, 150, 200)]
    axes(parts, L, R, T, B, B, "", ticks)
    for i in (0, 0.25, 0.5, 0.75, 1.0):
        parts.append(text(xi(i), B + 20, f"{i:g} A", 11, MUTED))
    parts.append(text((L + R) / 2, B + 44, "load current", 12, MUTED))
    for t, col, lab in [(TJ_MAX, AMBER, "125 °C: maximum operating"), (T_SHUT, RED, "above 150 °C: thermal shutdown")]:
        parts.append(f'<rect x="{L}" y="{yt(t) - 1}" width="{R - L}" height="2" fill="{col}"/>')
        parts.append(text(L + 8, yt(t) - 8, lab, 12, col, "start", weight="bold"))
    tj = lambda i: T_AMB + (VIN - VOUT) * i * THETA_JA
    i_end = (200 - T_AMB) / ((VIN - VOUT) * THETA_JA)
    i_shut = (T_SHUT - T_AMB) / ((VIN - VOUT) * THETA_JA)
    pts = [(xi(i_shut * k / 200), yt(tj(i_shut * k / 200))) for k in range(201)]
    parts.append(glow_line(pts, "#f6ad55"))
    parts.append(f'<line x1="{xi(i_shut):.1f}" y1="{yt(T_SHUT):.1f}" x2="{xi(i_end):.1f}" y2="{yt(200):.1f}" stroke="#f6ad55" stroke-width="2" stroke-dasharray="6 5" stroke-opacity="0.6"/>')
    parts.append(text(xi(i_end) - 6, yt(200) + 34, "would be, if it didn't shut down", 11, MUTED, "end", italic=True))
    for i in (0.1, 0.3, 0.5):
        x, y = xi(i), yt(tj(i))
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{AMBER_LIGHT}"/>')
        parts.append(text(x + 12, y + 18, f"{i:g} A: {(VIN - VOUT) * i:.1f} W, {tj(i):.0f} °C", 13, TEXT, "start", weight="bold"))
    i_max = (TJ_MAX - T_AMB) / ((VIN - VOUT) * THETA_JA)
    parts.append(f'<line x1="{xi(i_max):.1f}" y1="{yt(TJ_MAX):.1f}" x2="{xi(i_max):.1f}" y2="{B}" stroke="{AMBER}" stroke-dasharray="5 4"/>')
    parts.append(text(xi(i_max) + 8, B - 10, f"limit ≈ {i_max:.1f} A", 12, AMBER, "start", weight="bold"))
    return svg(w, h, "\n".join(parts), "A line of chip temperature against load current for a 7805 regulator in a TO-220 package with no heat sink, dropping 12 volts to 5. At 0.1 amps it dissipates 0.7 watts and reaches 42 degrees; at 0.3 amps, 2.1 watts and 75 degrees; at 0.5 amps, 3.5 watts and 109 degrees. It reaches its 125 degree maximum at about 0.6 amps, and above 150 degrees it shuts itself down.")


# 4. A buck converter's waveform ------------------------------------------------------------------
def buck_waveform():
    w, h = 900, 440
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "A buck converter: 12 V switched on 42% of the time averages 5 V", 17, AMBER_LIGHT, weight="bold"))
    L, R = 110, 720
    T1, B1 = 90, 230
    duty = VOUT / VIN
    y12 = lambda v: B1 - v / 12 * (B1 - T1)
    axes(parts, L, R, T1, B1, B1, "", [(y12(12), "12 V"), (y12(5), "5 V")])
    period = (R - L) / 5
    pts = []
    for k in range(5):
        x0 = L + k * period
        pts += [(x0, y12(0)), (x0, y12(12)), (x0 + duty * period, y12(12)), (x0 + duty * period, y12(0))]
    pts.append((R, y12(0)))
    parts.append(glow_line(pts, "#f6ad55", 3))
    parts.append(f'<rect x="{L}" y="{y12(5) - 1}" width="{R - L}" height="2" fill="{GREEN}"/>')
    parts.append(text(R + 12, y12(5) - 4, "average:", 12, GREEN, "start", weight="bold"))
    parts.append(text(R + 12, y12(5) + 12, "12 V × 0.42 = 5 V", 12, GREEN, "start", weight="bold"))
    parts.append(text(L + duty * period / 2, y12(12) - 10, "on", 12, TEXT, weight="bold"))
    parts.append(text(L + duty * period + (1 - duty) * period / 2, y12(0) - 10, "off", 12, TEXT, weight="bold"))
    parts.append(text((L + R) / 2, B1 + 22, "at the switch: 150,000 cycles a second on the LM2596", 12, MUTED, italic=True))
    T2, B2 = 290, 380
    y2 = lambda v: B2 - v / 12 * (B2 - T2)
    axes(parts, L, R, T2, B2, B2, "", [(y2(5), "5 V")])
    pts2 = [(L + k * (R - L) / 400, y2(5 + 0.15 * math.sin(k / 400 * 5 * 2 * math.pi))) for k in range(401)]
    parts.append(glow_line(pts2, GREEN, 3))
    parts.append(text((L + R) / 2, B2 + 22, "after the inductor and capacitor: steady 5 V (ripple exaggerated)", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Two traces. Top: the voltage at a buck converter's switch, a square wave between 0 and 12 volts that is on 42 percent of each cycle, averaging 5 volts, switching 150,000 times a second on the LM2596. Bottom: after the inductor and capacitor, a steady 5 volts with a small ripple.")


# 5. Dropout ------------------------------------------------------------------------------------------
def dropout():
    w, h = 900, 440
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Every linear regulator needs headroom: the dropout voltage", 17, AMBER_LIGHT, weight="bold"))
    L, R, T, B = 110, 840, 90, 360
    xv = lambda v: L + v / 12 * (R - L)
    yv = lambda v: B - v / 6 * (B - T)
    axes(parts, L, R, T, B, B, "", [(yv(v), f"{v} V") for v in (1, 2, 3, 4, 5, 6)])
    for v in range(0, 13, 2):
        parts.append(text(xv(v), B + 20, f"{v} V", 11, MUTED))
    parts.append(text((L + R) / 2, B + 44, "input voltage", 12, MUTED))
    for drop, col, lab in [(DROP_7805, "#f6ad55", "7805: needs 7 V (2 V dropout at 1 A)"),
                           (DROP_1117, "#90cdf4", "LM1117-5.0: needs 6.2 V (1.2 V dropout at 800 mA)")]:
        pts = [(xv(v / 20), yv(max(0, min(VOUT, v / 20 - drop)))) for v in range(0, 241)]
        parts.append(glow_line(pts, col, 3))
        knee = VOUT + drop
        parts.append(f'<circle cx="{xv(knee):.1f}" cy="{yv(VOUT):.1f}" r="6" fill="{col}"/>')
    parts.append(text(xv(7) + 10, yv(VOUT) - 34, "7805: needs 7 V (2 V dropout at 1 A)", 13, "#f6ad55", "start", weight="bold"))
    parts.append(text(xv(6.2) + 10, yv(VOUT) - 14, "LM1117-5.0: needs 6.2 V (1.2 V dropout at 800 mA)", 13, "#90cdf4", "start", weight="bold"))
    parts.append(text(xv(3.5), yv(1.0) + 30, "simplified: below the knee, the output follows the input, minus the dropout", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Output voltage against input voltage for two 5 volt linear regulators, simplified. Below a knee the output follows the input minus the dropout voltage; above it the output holds at 5 volts. The 7805 needs 7 volts in, with 2 volts of dropout at 1 amp. The low-dropout LM1117-5.0 needs 6.2 volts, with 1.2 volts of dropout at 800 milliamps.")


# 6. The linear power supply chain ---------------------------------------------------------------------
def supply_chain():
    w, h = 900, 400
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "A linear power supply, stage by stage", 17, AMBER_LIGHT, weight="bold"))
    stages = [("Transformer", "steps the voltage down,\nisolates from mains", "#718096", "sine_big"),
              ("Rectifier", "AC to one-way\npulses", BLUE, "humps"),
              ("Filter", "a capacitor smooths\nthe pulses", AMBER, "ripple"),
              ("Regulator", "holds the output\nsteady; needs a heat sink", RED, "flat")]
    base = 300
    for k, (name, sub, col, wave) in enumerate(stages):
        x = 60 + k * 205
        parts += box3d(x, base, 130, 50, 70, col)
        parts.append(text(x + 65, base - 30, name, 15, "#ffffff" if col != AMBER else "#1a1a1a", weight="bold"))
        for j, line in enumerate(sub.split("\n")):
            parts.append(text(x + 80, base + 30 + j * 16, line, 12, MUTED))
        # waveform above, showing the stage's output
        wx, wy, ww, wh = x + 10, 130, 130, 50
        pts = []
        for i in range(101):
            t = i / 100
            s = math.sin(t * 4 * math.pi)
            if wave == "sine_big":
                v = 0.5 - 0.45 * s
            elif wave == "humps":
                v = 0.95 - 0.85 * abs(s)
            elif wave == "ripple":
                v = 0.15 + 0.06 * abs(s)
            else:
                v = 0.3
            pts.append((wx + t * ww, wy + v * wh))
        parts.append(f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="none" stroke="#90cdf4" stroke-width="2.5"/>')
        if k < 3:
            parts.append(f'<path d="M{x + 160},{base - 35} l35,0" stroke="{MUTED}" stroke-width="2" marker-end="url(#arrow)"/>')
    parts.append(text(w / 2, 100, "what comes out of each stage", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Four 3D blocks in a row, each with the waveform it produces drawn above it. The transformer steps the mains voltage down and isolates it: a smaller sine wave. The rectifier turns it into one-way pulses: a row of humps. The filter capacitor smooths the pulses: a high line with a small ripple. The regulator, which needs a heat sink, holds the output perfectly steady: a flat line.")


FIGURES = {"two_ways.svg": two_ways, "linear_idea.svg": linear_idea, "heat_curve.svg": heat_curve,
           "buck_waveform.svg": buck_waveform, "dropout.svg": dropout, "supply_chain.svg": supply_chain}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
