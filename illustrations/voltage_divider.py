#!/usr/bin/env python3
"""Figures for docs/voltage_divider.md.

Sources:
- Divider: Vout = Vin x R2 / (R1 + R2); a load RL sits in parallel with R2.
  Thevenin equivalent: Vth = Vin x R2 / (R1 + R2), Rth = R1 || R2.
  Every number below is computed from these.
- ATmega328P datasheet (Microchip DS40002061B), 24.6.1 Analog Input Circuitry:
  "The ADC is optimized for analog signals with an output impedance of
  approximately 10 k[ohm] or less."
- Arduino analogRead(): 10-bit, 0-1023 on the Uno; this site converts with
  value / 1024.0 x 5.0 (see analog_input.md).

Usage:
    python3 illustrations/voltage_divider.py
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

OUT = HERE.parent / "docs" / "images" / "voltage_divider"
BLUE = "#4299e1"
VIN, R1, R2 = 9.0, 10e3, 10e3


def par(a, b):
    return a * b / (a + b)


def vout(r1, r2, vin=VIN, load=None):
    low = r2 if load is None else par(r2, load)
    return vin * low / (r1 + low)


# 1. The split, unloaded and loaded --------------------------------------------------
def split():
    w, h = 900, 470
    parts = [common_defs(), panel(15, 15, 425, h - 30), panel(460, 15, 425, h - 30)]
    scale = 30.0  # px per volt
    for cx, load, title, sub in [
        (227, None, "Nothing attached", "same current through both: equal shares"),
        (672, 1e3, "A 1 kΩ load attached", "R2 and the load together: 909 Ω"),
    ]:
        v_low = vout(R1, R2, load=load)
        v_high = VIN - v_low
        base = 405
        parts.append(text(cx, 50, title, 17, AMBER_LIGHT, weight="bold"))
        parts.append(text(cx, 72, sub, 12, MUTED, italic=True))
        # volt scale
        ax = cx - 140
        parts.append(f'<line x1="{ax}" y1="{base}" x2="{ax}" y2="{base - VIN * scale}" stroke="{MUTED}" stroke-width="1.5"/>')
        for v in range(0, 10, 3):
            y = base - v * scale
            parts.append(f'<line x1="{ax - 5}" y1="{y}" x2="{ax}" y2="{y}" stroke="{MUTED}"/>')
            parts.append(text(ax - 9, y + 4, f"{v} V", 11, MUTED, "end"))
        bx, bw, bd = cx - 60, 70, 40
        h_low, h_high = v_low * scale, v_high * scale
        parts += box3d(bx, base, bw, bd, h_low, BLUE)
        parts += box3d(bx, base - h_low, bw, bd, h_high, AMBER, shadow=False)
        if h_high > 40:
            parts.append(text(bx + bw / 2, base - h_low - h_high / 2, "R1", 15, "#1a1a1a", weight="bold"))
            parts.append(text(bx + bw / 2, base - h_low - h_high / 2 + 18, f"{v_high:.2f} V".replace(".50", ".5"), 12, "#1a1a1a"))
        if h_low > 40:
            parts.append(text(bx + bw / 2, base - h_low / 2, "R2", 15, "#ffffff", weight="bold"))
            parts.append(text(bx + bw / 2, base - h_low / 2 + 18, f"{v_low:.1f} V", 12, "#ffffff"))
        else:
            parts.append(text(bx - 12, base - h_low / 2 + 4, "R2", 13, "#90cdf4", "end", weight="bold"))
        tap_y = base - h_low
        parts.append(f'<line x1="{bx + bw + 30}" y1="{tap_y}" x2="{bx + bw + 62}" y2="{tap_y}" stroke="{TEXT}" stroke-width="2" stroke-dasharray="4 3"/>')
        parts += pill(bx + bw + 112, tap_y, f"{v_low:.2f} V out".replace("4.50", "4.5"), GREEN if load is None else RED, size=13, h=30)
    return svg(w, h, "\n".join(parts), "Two 3D stacks of two resistor blocks on a 9 volt scale. With nothing attached, R1 and R2 each take 4.5 volts and the output between them is 4.5 volts. With a 1 kilohm load across R2, the bottom block shrinks to 0.75 volts and R1 takes 8.25 volts, so the output falls to 0.75 volts.")


# 2. Same ratio, different current ---------------------------------------------------
def same_ratio():
    w, h = 900, 420
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 50, "Same ratio, same 4.5 V out: the resistor values set the waste", 17, AMBER_LIGHT, weight="bold"))
    base = 330
    for i, r in enumerate((1e3, 10e3, 100e3)):
        cx = 180 + i * 270
        i_ma = VIN / (2 * r) * 1e3
        p_mw = VIN ** 2 / (2 * r) * 1e3
        bh = 50 + 75 * math.log10(p_mw / 0.405)
        parts += box3d(cx - 45, base, 90, 50, bh, AMBER if i == 0 else (AMBER_LIGHT if i == 1 else GREEN))
        parts.append(text(cx + 17, base - bh - 30, f"{p_mw:g} mW".replace("0.405", "0.4"), 16, TEXT, weight="bold"))
        name = {1e3: "1 kΩ", 10e3: "10 kΩ", 100e3: "100 kΩ"}[r]
        parts.append(text(cx + 17, base + 34, f"{name} + {name}", 15, TEXT, weight="bold"))
        cur = f"{i_ma:g} mA" if i_ma >= 0.1 else f"{i_ma * 1000:g} µA"
        parts.append(text(cx + 17, base + 54, f"{cur} through both, all the time", 12, MUTED, italic=True))
    parts.append(text(w / 2, 74, "power wasted as heat from a 9 V battery (bar height on a log scale)", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Three 3D bars for three dividers that all give 4.5 volts from 9 volts. Two 1 kilohm resistors pass 4.5 milliamps and waste 40.5 milliwatts; two 10 kilohm resistors pass 0.45 milliamps and waste 4.05 milliwatts; two 100 kilohm resistors pass 45 microamps and waste 0.4 milliwatts.")


# 3. What the output sees -----------------------------------------------------------
def _battery(parts, x, y, hgt, label, gid):
    parts.append(f'<rect x="{x}" y="{y - hgt}" width="44" height="{hgt}" rx="6" fill="url(#{gid})"/>')
    parts.append(f'<ellipse cx="{x + 22}" cy="{y - hgt}" rx="22" ry="6" fill="{shade(AMBER, 0.3)}"/>')
    parts.append(f'<rect x="{x + 15}" y="{y - hgt - 10}" width="14" height="8" rx="2" fill="#cbd5e0"/>')
    parts.append(text(x + 22, y - hgt / 2 + 5, label, 14, "#1a1a1a", weight="bold"))


def _resistor(parts, x, y, length, label, vertical, gid):
    if vertical:
        parts.append(f'<rect x="{x - 11}" y="{y}" width="22" height="{length}" rx="10" fill="url(#{gid})"/>')
        for k in (0.3, 0.45, 0.6):
            parts.append(f'<rect x="{x - 11}" y="{y + length * k}" width="22" height="5" fill="#5a3a1a"/>')
        parts.append(text(x + 20, y + length / 2 + 5, label, 14, TEXT, "start", weight="bold"))
    else:
        parts.append(f'<rect x="{x}" y="{y - 11}" width="{length}" height="22" rx="10" fill="url(#{gid})"/>')
        for k in (0.3, 0.45, 0.6):
            parts.append(f'<rect x="{x + length * k}" y="{y - 11}" width="5" height="22" fill="#5a3a1a"/>')
        parts.append(text(x + length / 2, y - 20, label, 14, TEXT, weight="bold"))


def equivalent():
    w, h = 900, 430
    extra = (cyl_gradient("vd-bat", AMBER, vertical=True) + cyl_gradient("vd-res", "#d6b98c")
             + cyl_gradient("vd-resv", "#d6b98c", vertical=True))
    parts = [common_defs(extra), panel(15, 15, 400, h - 30), panel(485, 15, 400, h - 30)]
    wire = f'stroke="{TEXT}" stroke-width="3" fill="none"'
    parts.append(text(215, 50, "The divider", 17, AMBER_LIGHT, weight="bold"))
    parts.append(text(685, 50, "What its output sees", 17, AMBER_LIGHT, weight="bold"))
    # left: battery + R1 + R2, output tap
    _battery(parts, 70, 300, 150, "9 V", "vd-bat")
    parts.append(f'<path d="M92,140 L92,110 L230,110 L230,130" {wire}/>')
    _resistor(parts, 230, 130, 70, "R1 10 kΩ", True, "vd-resv")
    parts.append(f'<path d="M230,200 L230,225" {wire}/>')
    _resistor(parts, 230, 225, 70, "R2 10 kΩ", True, "vd-resv")
    parts.append(f'<path d="M230,295 L230,340 L92,340 L92,300" {wire}/>')
    parts.append(f'<path d="M230,212 L360,212" {wire}/>')
    parts.append(f'<circle cx="365" cy="212" r="6" fill="{GREEN}"/>')
    parts.append(f'<path d="M230,340 L360,340" {wire}/>')
    parts.append(f'<circle cx="365" cy="340" r="6" fill="{MUTED}"/>')
    parts.append(text(365, 196, "out", 13, GREEN, weight="bold"))
    parts.append(text(365, 368, "0 V", 13, MUTED))
    # equals sign
    parts.append(text(450, 240, "=", 44, AMBER_LIGHT, weight="bold"))
    # right: 4.5 V cell behind 5 kOhm
    _battery(parts, 560, 300, 120, "4.5 V", "vd-bat")
    parts.append(f'<path d="M582,170 L582,150 L650,150" {wire}/>')
    _resistor(parts, 650, 150, 90, "5 kΩ", False, "vd-res")
    parts.append(f'<path d="M740,150 L830,150" {wire}/>')
    parts.append(f'<circle cx="835" cy="150" r="6" fill="{GREEN}"/>')
    parts.append(f'<path d="M582,300 L582,340 L830,340" {wire}/>')
    parts.append(f'<circle cx="835" cy="340" r="6" fill="{MUTED}"/>')
    parts.append(text(835, 134, "out", 13, GREEN, weight="bold"))
    parts.append(text(835, 368, "0 V", 13, MUTED))
    parts.append(text(700, 230, "4.5 V = the unloaded output", 12, MUTED, italic=True))
    parts.append(text(700, 250, "5 kΩ = R1 and R2 in parallel", 12, MUTED, italic=True))
    parts.append(text(700, 400, "add a 1 kΩ load: 4.5 V × 1 ÷ (5 + 1) = 0.75 V", 13, TEXT, weight="bold"))
    return svg(w, h, "\n".join(parts), "Left, a 9 volt battery with two 10 kilohm resistors in series and the output taken between them. Right, the same thing as the output sees it: a 4.5 volt cell behind a single 5 kilohm resistor, which is R1 and R2 in parallel. Adding a 1 kilohm load gives 4.5 volts times 1 over 6, or 0.75 volts.")


# 4. The loading curve ---------------------------------------------------------------
def loading_curve():
    w, h = 900, 470
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Output of a 9 V, 10 kΩ + 10 kΩ divider as the load gets lighter", 17, AMBER_LIGHT, weight="bold"))
    L, R, T, B = 100, 850, 90, 380
    lo, hi = 2, 7  # 100 ohm .. 10 Mohm
    xr = lambda rl: L + (math.log10(rl) - lo) / (hi - lo) * (R - L)
    yv = lambda v: B - v / 5.0 * (B - T)
    rth = par(R1, R2)
    # zones: < 10x Rth, 10x-100x, > 100x
    for a, b_, col, lab in [(100, 10 * rth, RED, "load under 10× the 5 kΩ: sags more than 9%"),
                            (10 * rth, 100 * rth, AMBER, "10× to 100×"),
                            (100 * rth, 1e7, GREEN, "over 100×: within 1%")]:
        parts.append(f'<rect x="{xr(a):.1f}" y="{T}" width="{xr(b_) - xr(a):.1f}" height="{B - T}" fill="{col}" fill-opacity="0.08"/>')
        parts.append(text((xr(a) + xr(b_)) / 2, T + 16, lab, 11, shade(col, 0.2), italic=True))
    ticks = [(yv(v), f"{v} V") for v in (1, 2, 3, 4, 4.5)]
    axes(parts, L, R, T, B, B, "", ticks)
    parts.append(text((L + R) / 2, B + 44, "load resistance (log scale)", 12, MUTED))
    for e, lab in [(2, "100 Ω"), (3, "1 kΩ"), (4, "10 kΩ"), (5, "100 kΩ"), (6, "1 MΩ"), (7, "10 MΩ")]:
        parts.append(text(xr(10 ** e), B + 18, lab, 11, MUTED))
    pts = []
    for k in range(301):
        rl = 10 ** (lo + (hi - lo) * k / 300)
        pts.append((xr(rl), yv(vout(R1, R2, load=rl))))
    parts.append(glow_line(pts, "#90cdf4"))
    for rl, dx, dy in [(1e3, 14, 10), (10e3, 14, 14), (100e3, -12, -14), (1e7, -10, 26)]:
        v = vout(R1, R2, load=rl)
        x, y = xr(rl), yv(v)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{AMBER_LIGHT}"/>')
        parts.append(text(x + dx, y + dy, f"{v:.2f} V", 13, TEXT, "start" if dx > 0 else "end", weight="bold"))
    return svg(w, h, "\n".join(parts), "A curve of divider output against load resistance on a log scale from 100 ohms to 10 megohms. A 1 kilohm load gives 0.75 volts, 10 kilohms gives 3.00 volts, 100 kilohms gives 4.29 volts, and 10 megohms gives 4.50 volts. Shaded zones show loads under ten times the divider's 5 kilohm output resistance sagging more than 9 percent, and loads over a hundred times it staying within 1 percent.")


# 5. Battery monitor scales -----------------------------------------------------------
def monitor_scales():
    w, h = 900, 460
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "A 20 kΩ + 10 kΩ divider maps a battery onto the Arduino's range", 17, AMBER_LIGHT, weight="bold"))
    T, B = 100, 400
    cols = [(170, "battery", 15.0, "V"), (450, "A0 pin", 5.0, "V"), (730, "analogRead()", 1024, "")]
    for x, name, full, unit in cols:
        parts += box3d(x - 18, B, 36, 20, B - T, "#4a5568", shadow=True)
        parts.append(text(x, B + 34, name, 15, TEXT, weight="bold"))
        steps = 5 if unit else 4
        for k in range(steps + 1):
            val = full * k / steps
            y = B - (B - T) * k / steps
            lab = f"{val:g} {unit}".strip() if unit else f"{min(1023, int(val))}"
            parts.append(text(x - 28, y + 4, lab, 11, MUTED, "end"))
    def mark(col, frac, label, color):
        x = cols[col][0]
        y = B - (B - T) * frac
        parts.append(f'<circle cx="{x + 4}" cy="{y:.1f}" r="7" fill="{color}"/>')
        parts.append(text(x + 30, y + 5, label, 13, color, "start", weight="bold"))
        return x, y
    for v, color in [(12.6, AMBER_LIGHT), (15.0, RED)]:
        pin = v / 3
        reading = min(1023, int(pin / 5 * 1024))
        a = mark(0, v / 15, f"{v:g} V", color)
        b = mark(1, pin / 5, f"{pin:g} V", color)
        c = mark(2, reading / 1024, f"{reading}", color)
        for (x1, y1), (x2, y2) in [(a, b), (b, c)]:
            parts.append(f'<line x1="{x1 + 80:.1f}" y1="{y1:.1f}" x2="{x2 - 75:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="2" stroke-dasharray="6 4"/>')
    parts.append(text(310, 440, "÷ 3 (the divider)", 13, MUTED, italic=True))
    parts.append(text(590, 440, "× 1024 ÷ 5 V (the ADC)", 13, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Three 3D scale columns linked by dashed lines. A 12.6 volt battery becomes 4.2 volts at the A0 pin and an analogRead value of 860. The 15 volt maximum becomes 5 volts at the pin and reads 1023, the top of the scale.")


FIGURES = {"split.svg": split, "same_ratio.svg": same_ratio, "equivalent.svg": equivalent,
           "loading_curve.svg": loading_curve, "monitor_scales.svg": monitor_scales}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
