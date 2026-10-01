#!/usr/bin/env python3
"""Figures for docs/resistance.md.

Numbers and their sources:
- Resistivity at 20 C (Wikipedia "Electrical resistivity and conductivity",
  CRC values): copper 1.68e-8, nichrome 110e-8 Ohm-m. Copper's temperature
  coefficient 0.00386 /C (HyperPhysics resistivity table).
- AWG diameters from the standard formula d = 0.127 mm x 92^((36 - n) / 39).
- Extension cord: 30 m of 16 AWG (60 m of copper out and back) feeding a
  1,500 W, 120 V heater (12.5 A).
- E12 series (IEC 60063): 10 12 15 18 22 27 33 39 47 56 68 82, at +/-10%.
- Body resistance: NIOSH 98-131 (about 100 kOhm dry, 1 kOhm wet). Multimeter
  voltage-input resistance: typically 10 MOhm.

Usage:
    python3 illustrations/resistance.py
"""

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, box3d,  # noqa: E402
                     common_defs, cyl_gradient, panel, pill, render_all, shade,
                     svg, text)

OUT = HERE.parent / "docs" / "images" / "resistance"
RHO_CU, RHO_NICR, ALPHA_CU = 1.68e-8, 110e-8, 0.00386
E12 = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82]


def awg_area_mm2(n):
    d = 0.127 * 92 ** ((36 - n) / 39)
    return math.pi * d * d / 4


CORD_R = RHO_CU * 60 / (awg_area_mm2(16) * 1e-6)
HEATER_I = 1500 / 120


def rod(x, y, length, radius, color, gid, glow=None):
    """A horizontal 3D rod (cylinder) whose left end centre is at (x, y)."""
    out = []
    if glow:
        out.append(f'<rect x="{x - 10}" y="{y - radius - 12}" width="{length + 20}" height="{2 * radius + 24}" '
                   f'rx="{radius + 12}" fill="{glow}" fill-opacity="0.22"/>')
    out += [f'<ellipse cx="{x + length / 2}" cy="{y + radius + 10}" rx="{length / 2 + 6}" ry="6" fill="#000" fill-opacity="0.35"/>',
            f'<rect x="{x}" y="{y - radius}" width="{length}" height="{2 * radius}" fill="url(#{gid})"/>',
            f'<ellipse cx="{x + length}" cy="{y}" rx="{radius * 0.4:.1f}" ry="{radius}" fill="url(#{gid})"/>',
            f'<ellipse cx="{x}" cy="{y}" rx="{radius * 0.4:.1f}" ry="{radius}" fill="{shade(color, 0.25)}"/>']
    return out


# 1. The extension cord --------------------------------------------------------------
def extension_cord():
    w, h = 800, 460
    grads = cyl_gradient("cord", "#f6ad55")
    parts = [common_defs(grads + '<radialGradient id="coilglow" r="50%"><stop offset="0" stop-color="#fc8181" stop-opacity="0.8"/>'
                         '<stop offset="1" stop-color="#fc8181" stop-opacity="0"/></radialGradient>'), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "A long, thin cord is a resistor too", 16, TEXT, weight="bold"))
    # outlet
    parts += box3d(50, 300, 80, 30, 120, "#e2e8f0")
    for dy in (-90, -55):
        parts.append(f'<rect x="78" y="{300 + dy}" width="6" height="16" rx="2" fill="#2d3748"/><rect x="96" y="{300 + dy}" width="6" height="16" rx="2" fill="#2d3748"/>')
    parts += pill(90, 340, "120 V", "#d97706", "#1a1a1a", wpx=80, size=14, h=32)
    # cord: a long looping path with a warm glow
    path = "M130,240 C210,240 200,120 290,120 S380,320 460,300 S540,110 600,170"
    parts.append(f'<path d="{path}" fill="none" stroke="#fc8181" stroke-opacity="0.22" stroke-width="30" stroke-linecap="round"/>')
    parts.append(f'<path d="{path}" fill="none" stroke="#9c4221" stroke-width="15" stroke-linecap="round"/>')
    parts.append(f'<path d="{path}" fill="none" stroke="#f6ad55" stroke-width="10" stroke-linecap="round"/>')
    parts.append(f'<path d="{path}" fill="none" stroke="#fefcbf" stroke-opacity="0.5" stroke-width="3" stroke-linecap="round" transform="translate(-1,-3)"/>')
    parts.append(text(400, 382, f"30 m of 16-gauge cord: {CORD_R:.2f} Ω", 14, AMBER_LIGHT, weight="bold"))
    parts.append(text(400, 402, f"it warms by {HEATER_I ** 2 * CORD_R:.0f} W along its whole length", 13, "#fc8181"))
    # heater
    parts += box3d(600, 300, 140, 40, 150, "#4a5568")
    for k in range(4):
        y = 175 + k * 26
        parts.append(f'<rect x="612" y="{y - 10}" width="116" height="20" fill="url(#coilglow)"/>')
        parts.append(f'<line x1="616" y1="{y}" x2="724" y2="{y}" stroke="#fc8181" stroke-width="4" stroke-linecap="round"/>')
    parts += pill(670, 340, f"{120 - HEATER_I * CORD_R:.1f} V at the heater", "#2d3748", wpx=190, size=13, h=32)
    parts.append(text(w / 2, 430, f"1,500 W heater draws {HEATER_I:.1f} A; the cord takes {HEATER_I * CORD_R:.1f} V of the 120 V before the heater gets any",
                      12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), f"An outlet at 120 volts feeds a 1,500 watt heater through a long, coiled 16-gauge extension cord. The cord measures {CORD_R:.2f} ohms, glows warm, and turns {HEATER_I ** 2 * CORD_R:.0f} watts into heat along its length, leaving {120 - HEATER_I * CORD_R:.1f} volts at the heater.")


# 2. Four things set resistance ------------------------------------------------------
def four_factors():
    w, h = 820, 470
    grads = cyl_gradient("cu", "#c8733c") + cyl_gradient("nicr", "#8e9aab") + cyl_gradient("cuhot", "#e05a2a")
    parts = [common_defs(grads)]
    parts.append(text(w / 2, 34, "Four things set a wire's resistance (each compared with 1 m of 1 mm² copper at 20 °C)", 15, TEXT, weight="bold"))
    base_r = RHO_CU * 1 / 1e-6
    cards = [
        ("Material", [("copper", "cu", 120, 12, None, 1.0), ("nichrome", "nicr", 120, 12, None, RHO_NICR / RHO_CU)]),
        ("Length", [("1 m", "cu", 70, 12, None, 1.0), ("2 m", "cu", 140, 12, None, 2.0)]),
        ("Thickness", [("1 mm²", "cu", 120, 9, None, 1.0), ("2 mm²", "cu", 120, 13, None, 0.5)]),
        ("Temperature", [("20 °C", "cu", 120, 12, None, 1.0), ("70 °C", "cuhot", 120, 12, "#fc8181", 1 + ALPHA_CU * 50)]),
    ]
    for i, (title, rods) in enumerate(cards):
        cx = 110 + i * 200
        parts.append(panel(cx - 95, 52, 190, 400))
        parts.append(text(cx, 82, title, 16, AMBER_LIGHT, weight="bold"))
        for j, (lab, gid, length, rad, glow, rel) in enumerate(rods):
            y = 160 + j * 130
            color = {"cu": "#c8733c", "nicr": "#8e9aab", "cuhot": "#e05a2a"}[gid]
            parts += rod(cx - length / 2, y, length, rad, color, gid, glow)
            parts.append(text(cx, y - rad - 16, lab, 13, TEXT, weight="bold"))
            parts.append(text(cx, y + rad + 34, f"{rel:.2f}× the resistance" if rel < 10 else f"{rel:.0f}× the resistance",
                              13, "#9ae6b4" if rel <= 1 else "#fc8181", weight="bold"))
    parts.append(text(w / 2, h - 8, f"reference: 1 m of 1 mm² copper at 20 °C is {base_r * 1000:.1f} mΩ", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Four panels of 3D rods. Material: nichrome has 65 times the resistance of the same copper rod. Length: doubling the length doubles the resistance. Thickness: doubling the cross-section halves it. Temperature: copper at 70 degrees Celsius has 1.19 times its resistance at 20.")


# 3. Wire gauges ------------------------------------------------------------------
def wire_gauges():
    w, h = 800, 400
    grads = cyl_gradient("cuv", "#c8733c", vertical=True)
    parts = [common_defs(grads), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "Thicker wire, lower resistance: common copper gauges", 16, TEXT, weight="bold"))
    parts.append(text(w / 2, 66, "cross-sections drawn to scale with each other (AWG: a smaller number means a thicker wire)", 12, MUTED, italic=True))
    gauges = [(22, "hookup wire"), (18, "lamp cord"), (14, "15 A house circuit"), (10, "30 A dryer circuit")]
    scale = 34  # px per mm of diameter
    for i, (n, use) in enumerate(gauges):
        cx = 120 + i * 185
        d = 0.127 * 92 ** ((36 - n) / 39)
        r = d * scale / 2
        a = awg_area_mm2(n)
        r100 = RHO_CU * 100 / (a * 1e-6)
        cy = 190
        # insulation ring, then the copper end-on
        parts.append(f'<ellipse cx="{cx}" cy="{cy + r + 28}" rx="{r + 22}" ry="7" fill="#000" fill-opacity="0.4"/>')
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r + 14}" fill="#2b6cb0" fill-opacity="0.55" stroke="#90cdf4" stroke-opacity="0.5"/>')
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#copperball)"/>')
        parts.append(text(cx, 280, f"{n} AWG", 16, AMBER_LIGHT, weight="bold"))
        parts.append(text(cx, 300, f"{a:.2f} mm²", 13, TEXT))
        parts.append(text(cx, 320, f"{r100:.2f} Ω per 100 m", 13, "#9ae6b4", weight="bold"))
        parts.append(text(cx, 342, use, 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Four copper wires seen end-on, drawn to scale: 22 AWG at 0.33 square millimetres and 5.2 ohms per 100 metres, 18 AWG at 0.82 and 2.0, 14 AWG at 2.08 and 0.81, and 10 AWG at 5.26 and 0.32.")


# 4. Conductance: parallel paths add -----------------------------------------------------
def conductance_paths():
    w, h = 800, 430
    parts = [common_defs(cyl_gradient("pipe", "#2b6cb0")), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "Conductance: how easily current flows. Side-by-side paths simply add.", 15, TEXT, weight="bold"))
    paths = [(100, 10.0, 150), (220, 1000 / 220, 290)]
    for R, G, y in paths:
        width = G * 3.2
        parts.append(f'<path d="M110,220 C190,220 200,{y} 280,{y} L520,{y} C600,{y} 610,220 690,220" fill="none" '
                     f'stroke="#90cdf4" stroke-opacity="0.18" stroke-width="{width + 18:.1f}"/>')
        parts.append(f'<path d="M110,220 C190,220 200,{y} 280,{y} L520,{y} C600,{y} 610,220 690,220" fill="none" '
                     f'stroke="#3182ce" stroke-width="{width:.1f}" stroke-linecap="round"/>')
        parts += pill(400, y, f"{R} Ω  =  {G:.1f} mS", "#1a202c", "#e2e8f0", wpx=200, size=14, h=34)
    gt = sum(g for _, g, _ in paths)
    parts += pill(110, 220, "in", "#d97706", "#1a1a1a", wpx=54, size=13, h=30)
    parts += pill(690, 220, "out", "#d97706", "#1a1a1a", wpx=60, size=13, h=30)
    parts.append(text(400, 368, f"total conductance: 10.0 + 4.5 = {gt:.1f} mS", 16, "#9ae6b4", weight="bold"))
    parts.append(text(400, 392, f"so the pair together is 1 ÷ {gt / 1000:.4f} S = {1000 / gt:.1f} Ω, less than either path alone", 13, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), f"Two parallel paths drawn as pipes whose width shows conductance: a 100 ohm path of 10 millisiemens and a thinner 220 ohm path of 4.5 millisiemens. Together they conduct {gt:.1f} millisiemens, which is {1000 / gt:.1f} ohms, less than either path alone.")


# 5. Tolerance and the E12 ladder -----------------------------------------------------
def tolerance_ladder():
    w, h = 820, 430
    L, R = 60, 780
    X = lambda v: L + (R - L) * math.log10(v / 9) / math.log10(100 / 9)
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "The E12 values, each with its ±10% tolerance band (one decade, log scale)", 15, TEXT, weight="bold"))
    for i, v in enumerate(E12):
        lo, hi = v * 0.9, v * 1.1
        y = 130 + (i % 2) * 70
        parts.append(f'<rect x="{X(lo):.1f}" y="{y - 13}" width="{X(hi) - X(lo):.1f}" height="26" rx="13" fill="{AMBER}" fill-opacity="0.55"/>')
        parts.append(f'<rect x="{X(lo):.1f}" y="{y - 13}" width="{X(hi) - X(lo):.1f}" height="26" rx="13" fill="url(#gloss)"/>')
        parts.append(f'<circle cx="{X(v):.1f}" cy="{y}" r="6" fill="url(#eball)"/>')
        parts.append(text(X(v), y - 22, str(v), 14, TEXT, weight="bold"))
        parts.append(f'<line x1="{X(v):.1f}" y1="{y + 13}" x2="{X(v):.1f}" y2="268" stroke="{MUTED}" stroke-opacity="0.4" stroke-dasharray="2 4"/>')
    parts.append(f'<line x1="{L}" y1="270" x2="{R}" y2="270" stroke="{MUTED}" stroke-width="1.5"/>')
    gaps = [(a * 1.1, b * 0.9) for a, b in zip(E12 + [100], (E12 + [100])[1:]) if a * 1.1 < b * 0.9]
    for g1, g2 in gaps:
        xm = (X(g1) + X(g2)) / 2
        parts.append(f'<rect x="{X(g1):.1f}" y="262" width="{max(3, X(g2) - X(g1)):.1f}" height="16" fill="{RED}"/>')
        parts.append(f'<line x1="{xm:.1f}" y1="282" x2="{xm:.1f}" y2="306" stroke="#fc8181"/>')
        parts.append(text(xm, 322, f"gap: {g1:g} to {g2:g}", 12, "#fc8181", weight="bold"))
    parts.append(text(w / 2, 362, "Almost every value's band reaches the next one, so almost any resistance is within 10% of a stock part.", 13, TEXT))
    parts.append(text(w / 2, 384, "The rounded historic values leave two hairline gaps per decade.", 13, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "One decade of the E12 resistor series on a log scale, each value from 10 to 82 drawn with its plus or minus 10 percent tolerance band. The bands almost tile the whole decade, leaving two tiny gaps, from 13.2 to 13.5 and from 24.2 to 24.3.")


# 6. Resistance scale ----------------------------------------------------------------
def resistance_scale():
    w, h = 800, 340
    L, R = 50, 750
    lo, hi = -3, 8
    X = lambda v: L + (R - L) * (math.log10(v) - lo) / (hi - lo)
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "Resistances you'll meet, log scale (each tick is 10×)", 16, TEXT, weight="bold"))
    ty, th = 160, 28
    parts.append(f'<rect x="{L}" y="{ty}" width="{R - L}" height="{th}" rx="14" fill="#4a5568" fill-opacity="0.55"/>')
    parts.append(f'<rect x="{L}" y="{ty}" width="{R - L}" height="{th}" rx="14" fill="url(#gloss)" stroke="#e2e8f0" stroke-opacity="0.35"/>')
    names = {-3: "1 mΩ", -2: "10 mΩ", -1: "0.1 Ω", 0: "1 Ω", 1: "10 Ω", 2: "100 Ω", 3: "1 kΩ", 4: "10 kΩ", 5: "100 kΩ", 6: "1 MΩ", 7: "10 MΩ", 8: "100 MΩ"}
    for p in range(lo, hi + 1):
        x = X(10 ** p)
        parts.append(f'<line x1="{x:.1f}" y1="{ty + th}" x2="{x:.1f}" y2="{ty + th + 6}" stroke="{MUTED}"/>')
        parts.append(text(x, ty + th + 20, names[p], 10, MUTED))
    one_m = RHO_CU / (awg_area_mm2(14) * 1e-6)
    items = [(one_m, "1 m of 14 AWG", True), (CORD_R, "30 m cord", False), (330, "LED resistor", True),
             (1000, "wet skin", False), (1e5, "dry skin", True), (1e7, "meter input", False)]
    for v, lab, above in items:
        x = X(v)
        parts.append(f'<circle cx="{x:.1f}" cy="{ty + th / 2}" r="8" fill="url(#eball)"/>')
        y = ty - 30 if above else ty + th + 62
        parts.append(f'<line x1="{x:.1f}" y1="{ty - 2 if above else ty + th + 28}" x2="{x:.1f}" y2="{y + (6 if above else -14)}" stroke="{MUTED}"/>')
        val = (f"{v * 1000:.0f} mΩ" if v < 0.1 else f"{v:.2f} Ω" if v < 10 else f"{v:g} Ω" if v < 1000 else f"{v / 1000:g} kΩ" if v < 1e6 else f"{v / 1e6:g} MΩ")
        parts.append(text(x, y - (16 if above else 0), lab, 13, TEXT, weight="bold"))
        parts.append(text(x, y + (0 if above else 16), val, 12, AMBER_LIGHT))
    return svg(w, h, "\n".join(parts), "A log scale of resistance from 1 milliohm to 100 megohms: 1 metre of 14-gauge copper at about 8 milliohms, a 30 metre extension cord at 0.77 ohms, a 330 ohm LED resistor, wet skin at about 1 kilohm, dry skin at about 100 kilohms, and a multimeter's 10 megohm input.")


FIGURES = {
    "extension_cord.svg": extension_cord,
    "four_factors.svg": four_factors,
    "wire_gauges.svg": wire_gauges,
    "conductance_paths.svg": conductance_paths,
    "tolerance_ladder.svg": tolerance_ladder,
    "resistance_scale.svg": resistance_scale,
}

if __name__ == "__main__":
    print(f"cord {CORD_R:.3f} ohm, drop {HEATER_I * CORD_R:.2f} V, heat {HEATER_I ** 2 * CORD_R:.1f} W")
    render_all(FIGURES, OUT)
