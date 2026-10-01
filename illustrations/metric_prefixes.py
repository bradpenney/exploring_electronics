#!/usr/bin/env python3
"""Figures for docs/metric_prefixes.md.

Sources: SI prefixes from the BIPM SI Brochure (bipm.org, "SI prefixes");
letter-for-decimal-point marking (4K7, 4n7) from IEC 60062 (the RKM code).
Example values: the 25 mA reading is the article's own example; 7.040 MHz is
in the 40 m amateur band; 2.4 GHz is the common Wi-Fi band.

Usage:
    python3 illustrations/metric_prefixes.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, MUTED, TEXT, box3d, common_defs,  # noqa: E402
                     cyl_gradient, panel, pill, render_all, svg, text)
from voltage import multimeter  # noqa: E402

OUT = HERE.parent / "docs" / "images" / "metric_prefixes"

PREFIXES = [("G", "giga", 9, "2.4 GHz Wi-Fi"), ("M", "mega", 6, "7.040 MHz radio"), ("k", "kilo", 3, "4.7 kΩ resistor"),
            ("", "the unit", 0, "1.5 V cell"), ("m", "milli", -3, "20 mA LED"), ("µ", "micro", -6, "10 µF capacitor"),
            ("n", "nano", -9, "100 nF capacitor"), ("p", "pico", -12, "47 pF capacitor")]


# 1. Same current, three ranges -------------------------------------------------------
def meter_ranges():
    w, h = 800, 330
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "One current, three readings: only the unit changed", 16, TEXT, weight="bold"))
    for i, (reading, rng) in enumerate((("0.025", "amps (A)"), ("25.0", "milliamps (mA)"), ("25000", "microamps (µA)"))):
        x = 110 + i * 230
        parts += multimeter(x, 80, reading, mode="A⎓")
        parts.append(text(x + 60, 270, rng, 14, AMBER_LIGHT, weight="bold"))
        parts.append(text(x + 60, 290, "setting", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Three multimeters measuring the same current. On the amps setting it reads 0.025, on milliamps 25.0, and on microamps 25000.")


# 2. The prefix staircase -------------------------------------------------------------
def prefix_ladder():
    w, h = 860, 470
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "The prefixes electronics uses: every step is 1,000×", 16, TEXT, weight="bold"))
    x0, base, sw = 40, 410, 100
    for i, (sym, name, exp, example) in enumerate(PREFIXES):
        hgt = 84 + (exp + 12) * 10
        x = x0 + i * sw
        color = AMBER if exp == 0 else ("#4a5568" if exp > 0 else "#2c5282")
        parts += box3d(x, base, sw - 12, 30, hgt, color, shadow=False)
        top = base - hgt
        cx = x + (sw - 12) / 2
        parts.append(text(cx, top + 30, sym if sym else "—", 24, "#1a1a1a" if exp == 0 else "#ffffff", weight="bold"))
        parts.append(text(cx, top + 50, name, 13, "#1a1a1a" if exp == 0 else "#ffffff", weight="bold"))
        exp_txt = "×1" if exp == 0 else f"×10{''.join('⁰¹²³⁴⁵⁶⁷⁸⁹'[int(d)] if d.isdigit() else '⁻' for d in str(exp))}"
        parts.append(text(cx, top + 68, exp_txt, 12, "#1a1a1a" if exp == 0 else "#e2e8f0"))
        parts.append(text(cx, top - 12, example, 11, MUTED, italic=True))
    parts.append(text(x0 + 3 * sw + 44, base + 26, "centi (c, ×10⁻²) is the odd one out: centimetres, almost never in circuits", 12, MUTED, "middle", italic=True))
    return svg(w, h, "\n".join(parts), "A 3D staircase of prefixes from giga down to pico: G giga times 10 to the 9, M mega, k kilo, the base unit, m milli, µ micro, n nano, and p pico times 10 to the minus 12, each a factor of 1,000 from the next, with a real example on each step.")


# 3. Sliding the decimal point ------------------------------------------------------------
def decimal_slide():
    w, h = 800, 380
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "Converting is sliding the decimal point three places at a time", 16, TEXT, weight="bold"))
    rows = [("0.025", "A", "a big unit: a small number"), ("25", "mA", "1,000× smaller unit: 1,000× bigger number"),
            ("25 000", "µA", "another 1,000×")]
    for i, (num, unit, note) in enumerate(rows):
        y = 120 + i * 80
        parts += pill(250, y, f"{num} {unit}", "#2d3748", "#9ae6b4", wpx=220, size=22, h=50)
        parts.append(text(400, y + 6, note, 14, TEXT, "start"))
        if i < 2:
            parts.append(f'<path d="M250,{y + 28} L250,{y + 52}" stroke="{AMBER}" stroke-width="3" marker-end="url(#arrow)"/>')
            parts.append(text(262, y + 46, "× 1,000", 12, AMBER_LIGHT, "start", "bold"))
    parts.append(text(w / 2, 352, "bigger unit → smaller number; smaller unit → bigger number. The amount never changes.", 13, AMBER_LIGHT, weight="bold"))
    return svg(w, h, "\n".join(parts), "Three rows showing the same current: 0.025 amps, then 25 milliamps, then 25,000 microamps, with arrows marking a factor of 1,000 at each step down to a smaller unit.")


# 4. Prefixes in the wild --------------------------------------------------------------
def in_the_wild():
    w, h = 880, 400
    grads = cyl_gradient("elec", "#2b6cb0", vertical=True) + cyl_gradient("resb", "#3b6fb6")
    parts = [common_defs(grads)]
    parts.append(text(w / 2, 34, "Prefixes as they're actually printed on parts and dials", 16, TEXT, weight="bold"))
    cards = [("47 pF", "marked 47 or 47p", "ceramic capacitor"), ("100 nF", "marked 104", "ceramic capacitor"),
             ("10 µF", "marked 10µF", "electrolytic capacitor"), ("4.7 kΩ", "printed 4K7", "metal-film resistor"),
             ("7.040 MHz", "= 7040 kHz", "radio frequency")]
    for i, (val, mark, what) in enumerate(cards):
        cx = 100 + i * 170
        parts.append(panel(cx - 78, 52, 156, 330))
        y = 160
        if i in (0, 1):
            parts.append(f'<line x1="{cx - 8}" y1="{y + 20}" x2="{cx - 8}" y2="{y + 80}" stroke="#cbd5e0" stroke-width="3"/>')
            parts.append(f'<line x1="{cx + 8}" y1="{y + 20}" x2="{cx + 8}" y2="{y + 80}" stroke="#cbd5e0" stroke-width="3"/>')
            parts.append(f'<ellipse cx="{cx}" cy="{y}" rx="34" ry="30" fill="url(#{"goldball" if i == 0 else "copperball"})"/>')
            parts.append(text(cx, y + 6, "47" if i == 0 else "104", 16, "#1a1a1a", weight="bold"))
        elif i == 2:
            parts.append(f'<rect x="{cx - 26}" y="{y - 46}" width="52" height="96" rx="8" fill="url(#elec)"/>')
            parts.append(f'<ellipse cx="{cx}" cy="{y - 46}" rx="26" ry="8" fill="#a0aec0"/>')
            parts.append(text(cx, y + 6, "10µF", 14, "#ffffff", weight="bold"))
            parts.append(f'<rect x="{cx + 12}" y="{y - 40}" width="10" height="86" fill="#e2e8f0" fill-opacity="0.6"/>')
            parts.append(f'<line x1="{cx - 10}" y1="{y + 50}" x2="{cx - 10}" y2="{y + 84}" stroke="#cbd5e0" stroke-width="3"/>')
            parts.append(f'<line x1="{cx + 10}" y1="{y + 50}" x2="{cx + 10}" y2="{y + 76}" stroke="#cbd5e0" stroke-width="3"/>')
        elif i == 3:
            parts.append(f'<rect x="{cx - 70}" y="{y - 2}" width="140" height="5" rx="2" fill="#cbd5e0"/>')
            parts.append(f'<rect x="{cx - 44}" y="{y - 18}" width="88" height="36" rx="18" fill="url(#resb)"/>')
            parts.append(text(cx, y + 5, "4K7", 15, "#ffffff", weight="bold"))
        else:
            parts.append(f'<rect x="{cx - 60}" y="{y - 34}" width="120" height="58" rx="8" fill="#1a1d23" stroke="#9ae6b4" stroke-opacity="0.5"/>')
            parts.append(text(cx, y + 6, "7.040.00", 20, "#9ae6b4", weight="bold"))
            parts.append(text(cx, y + 50, "MHz", 12, MUTED))
        parts.append(text(cx, 290, val, 20, AMBER_LIGHT, weight="bold"))
        parts.append(text(cx, 316, mark, 12, TEXT))
        parts.append(text(cx, 340, what, 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Five panels: a ceramic capacitor marked 47, meaning 47 picofarads; a ceramic capacitor marked 104, meaning 100 nanofarads; an electrolytic capacitor marked 10 microfarads; a resistor printed 4K7, meaning 4.7 kilohms; and a radio display reading 7.040 megahertz, which is 7040 kilohertz.")


FIGURES = {
    "meter_ranges.svg": meter_ranges,
    "prefix_ladder.svg": prefix_ladder,
    "decimal_slide.svg": decimal_slide,
    "in_the_wild.svg": in_the_wild,
}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
