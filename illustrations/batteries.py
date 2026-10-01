#!/usr/bin/env python3
"""Figures for docs/batteries.md.

Sources:
- Energizer datasheets: E91 alkaline AA (1.5 V, 23 g, 10-year shelf life,
  150-300 mOhm internal resistance, capacity chart roughly 3000/2500/2000/1500
  mAh at 25/100/250/500 mA, read from the bar chart); NH15 NiMH AA (1.2 V,
  2300 mAh, 28 g, ~30 mOhm charged); L91 lithium AA (Li/FeS2, 1.5 V, 15 g,
  25-year shelf life, -40 to 60 C).
- Wikipedia "Comparison of commercial battery types": nominal cell voltages and
  specific energy (Wh/kg) by chemistry.
- Canadian Forces Fire Marshal (canada.ca, 2025-10-01): lithium-ion warning
  signs and response.

Usage:
    python3 illustrations/batteries.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, box3d,  # noqa: E402
                     common_defs, cyl_gradient, panel, pill, render_all, shade,
                     svg, text)
from what_is_electricity import wire  # noqa: E402

OUT = HERE.parent / "docs" / "images" / "batteries"

# (name, nominal V, Wh/kg low, Wh/kg high, rechargeable)
CHEM = [("Zinc-carbon", 1.5, 36, 36, False), ("Alkaline", 1.5, 85, 190, False), ("Mercury", 1.35, 99, 123, False),
        ("Lithium primary", 1.5, 297, 297, False), ("NiCd", 1.2, 30, 30, True), ("Lead-acid", 2.1, 30, 50, True),
        ("NiMH", 1.2, 100, 100, True), ("Lithium-ion", 3.7, 195, 195, True)]


# 1. Inside an alkaline cell ------------------------------------------------------------
def cell_anatomy():
    w, h = 800, 440
    grads = (cyl_gradient("can", "#a0aec0", vertical=True) + cyl_gradient("mno2", "#2d3748", vertical=True) +
             cyl_gradient("zinc", "#cbd5e0", vertical=True))
    parts = [common_defs(grads), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "Inside an alkaline AA cell (cut open)", 16, TEXT, weight="bold"))
    cx, top, bot = 260, 90, 380
    parts.append(f'<ellipse cx="{cx}" cy="{bot + 8}" rx="80" ry="10" fill="#000" fill-opacity="0.4"/>')
    parts.append(f'<rect x="{cx - 70}" y="{top}" width="140" height="{bot - top}" rx="10" fill="url(#can)"/>')
    parts.append(f'<rect x="{cx - 58}" y="{top + 14}" width="116" height="{bot - top - 28}" rx="6" fill="url(#mno2)"/>')
    parts.append(f'<rect x="{cx - 34}" y="{top + 26}" width="68" height="{bot - top - 52}" rx="4" fill="#f7fafc" fill-opacity="0.85"/>')
    parts.append(f'<rect x="{cx - 30}" y="{top + 30}" width="60" height="{bot - top - 60}" rx="4" fill="url(#zinc)"/>')
    parts.append(f'<rect x="{cx - 4}" y="{top + 60}" width="8" height="{bot - top - 50}" fill="#d4af37"/>')
    parts.append(f'<rect x="{cx - 18}" y="{top - 14}" width="36" height="14" rx="3" fill="#cbd5e0"/>')
    parts.append(f'<rect x="{cx - 50}" y="{bot - 6}" width="100" height="10" rx="3" fill="#718096"/>')
    parts.append(text(cx, top - 22, "+", 20, AMBER_LIGHT, weight="bold"))
    parts.append(text(cx, bot + 30, "−", 22, "#90cdf4", weight="bold"))
    labels = [(cx + 66, 120, "steel can: the + terminal"), (cx + 50, 170, "manganese dioxide: the cathode"),
              (cx + 32, 220, "separator: keeps them apart, lets ions through"), (cx + 22, 270, "zinc gel: the anode"),
              (cx + 4, 320, "brass collector: carries current to the − cap")]
    for x, y, lab in labels:
        parts.append(f'<line x1="{x}" y1="{y}" x2="430" y2="{y}" stroke="{MUTED}" stroke-dasharray="3 3"/>')
        parts.append(f'<circle cx="{x}" cy="{y}" r="3.5" fill="{AMBER}"/>')
        parts.append(text(440, y + 4, lab, 13, TEXT, "start"))
    parts.append(text(560, 380, "the reaction pushes electrons from zinc to manganese dioxide", 12, MUTED, "middle", italic=True))
    parts.append(text(560, 398, "through the outside circuit: about 1.5 V per cell", 12, MUTED, "middle", italic=True))
    return svg(w, h, "\n".join(parts), "A cut-open alkaline AA cell: a steel can that forms the positive terminal, a manganese dioxide cathode lining it, a separator, a zinc gel anode in the centre, and a brass collector carrying current down to the negative cap.")


def battery_box(x, y, label, sub):
    """A 12 V battery block with + and - terminals on top; (x, y) = front-bottom-left."""
    out = box3d(x, y, 150, 50, 90, "#2d3748")
    out += [f'<rect x="{x + 18}" y="{y - 104}" width="22" height="14" rx="3" fill="#e53e3e"/>',
            f'<rect x="{x + 108}" y="{y - 104}" width="22" height="14" rx="3" fill="#1a1a1a" stroke="#cbd5e0" stroke-opacity="0.6"/>',
            text(x + 29, y - 108, "+", 14, "#fc8181", weight="bold"), text(x + 119, y - 108, "−", 14, "#90cdf4", weight="bold"),
            text(x + 75, y - 46, label, 16, "#ffffff", weight="bold"), text(x + 75, y - 26, sub, 12, "#e2e8f0")]
    return out


# 2. Series and parallel --------------------------------------------------------------
def series_parallel():
    w, h = 860, 430
    parts = [common_defs(), panel(15, 15, 405, h - 30), panel(440, 15, 405, h - 30)]
    parts.append(text(217, 48, "In series: voltages add", 16, AMBER_LIGHT, weight="bold"))
    parts.append(text(217, 68, "+ of one to − of the next", 12, MUTED, italic=True))
    parts += battery_box(40, 260, "12 V", "20 Ah") + battery_box(230, 260, "12 V", "20 Ah")
    parts += wire([(158, 157), (158, 130), (269, 130), (269, 157)], 6)
    parts += pill(217, 340, "24 V, 20 Ah", "#d97706", "#1a1a1a", wpx=200, size=18, h=44)
    parts.append(text(217, 384, "twice the push, same charge to deliver", 12, TEXT))
    parts.append(text(642, 48, "In parallel: capacities add", 16, AMBER_LIGHT, weight="bold"))
    parts.append(text(642, 68, "+ to +, − to −", 12, MUTED, italic=True))
    parts += battery_box(465, 260, "12 V", "20 Ah") + battery_box(655, 260, "12 V", "20 Ah")
    parts += wire([(494, 157), (494, 118), (684, 118), (684, 157)], 6)
    parts += wire([(584, 157), (584, 136), (774, 136), (774, 157)], 6)
    parts += pill(642, 340, "12 V, 40 Ah", "#2f855a", wpx=200, size=18, h=44)
    parts.append(text(642, 384, "same push, twice the charge (and current available)", 12, TEXT))
    return svg(w, h, "\n".join(parts), "Two pairs of 12 volt, 20 amp-hour batteries. Wired in series, positive of one to negative of the next, they make 24 volts at 20 amp-hours. Wired in parallel, positive to positive and negative to negative, they make 12 volts at 40 amp-hours.")


# 3. Energy per kilogram by chemistry ---------------------------------------------------
def chemistry_chart():
    w, h = 860, 480
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "Energy per kilogram, and nominal volts per cell, by chemistry", 16, TEXT, weight="bold"))
    base, scale = 370, 0.72
    for i, (name, v, lo, hi, rech) in enumerate(CHEM):
        x = 50 + i * 100
        color = "#2f855a" if rech else "#4a5568"
        if name == "Lithium-ion":
            color = AMBER
        parts += box3d(x, base, 70, 26, hi * scale, color, shadow=False)
        if hi != lo:
            parts.append(f'<line x1="{x}" y1="{base - lo * scale:.1f}" x2="{x + 70}" y2="{base - lo * scale:.1f}" stroke="#ffffff" stroke-dasharray="4 3" stroke-opacity="0.7"/>')
        val = f"{lo}–{hi}" if hi != lo else f"{hi}"
        parts.append(text(x + 35, base - hi * scale - 26, val, 13, TEXT, weight="bold"))
        parts.append(text(x + 35, base + 22, name, 12, TEXT, weight="bold"))
        parts.append(text(x + 35, base + 40, f"{v:g} V", 12, AMBER_LIGHT))
    parts.append(text(w / 2, 82, "Wh/kg (dashed line: low end of the range)", 12, MUTED, italic=True))
    parts += pill(260, 446, "single-use (primary)", "#4a5568", wpx=190, size=12, h=26)
    parts += pill(480, 446, "rechargeable (secondary)", "#2f855a", wpx=210, size=12, h=26)
    return svg(w, h, "\n".join(parts), "A 3D bar chart of energy per kilogram by battery chemistry, with each cell's nominal voltage: zinc-carbon 36 watt-hours per kilogram at 1.5 volts, alkaline 85 to 190 at 1.5, mercury 99 to 123 at 1.35, lithium primary 297 at 1.5, NiCd 30 at 1.2, lead-acid 30 to 50 at 2.1, NiMH 100 at 1.2, and lithium-ion 195 at 3.7.")


# 4. Internal resistance under load --------------------------------------------------
def internal_resistance_load():
    w, h = 820, 400
    parts = [common_defs(cyl_gradient("alk", AMBER, vertical=True) + cyl_gradient("nimh", "#38a169", vertical=True)),
             panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "Under a 1 A load, a cell loses I × R inside itself", 16, TEXT, weight="bold"))
    cases = [("Alkaline AA", "alk", 1.5, 0.150, 0.300), ("NiMH AA (charged)", "nimh", 1.2, 0.030, 0.030)]
    for i, (name, gid, v, rlo, rhi) in enumerate(cases):
        cx = 220 + i * 380
        parts.append(f'<rect x="{cx - 30}" y="110" width="60" height="140" rx="8" fill="url(#{gid})"/>')
        parts.append(f'<rect x="{cx - 10}" y="100" width="20" height="10" rx="2" fill="#cbd5e0"/>')
        parts.append(text(cx, 190, f"{v} V", 15, "#1a1a1a", weight="bold"))
        parts.append(text(cx, 82, name, 15, AMBER_LIGHT, weight="bold"))
        ir = f"{rlo * 1000:.0f}–{rhi * 1000:.0f} mΩ" if rlo != rhi else f"{rlo * 1000:.0f} mΩ"
        loss = f"{rlo:.2f}–{rhi:.2f} V" if rlo != rhi else f"{rlo:.2f} V"
        term = f"{v - rhi:.2f}–{v - rlo:.2f} V" if rlo != rhi else f"{v - rlo:.2f} V"
        parts.append(text(cx, 284, f"internal resistance: {ir}", 13, TEXT))
        parts.append(text(cx, 306, f"lost inside at 1 A: {loss}", 13, "#fc8181", weight="bold"))
        parts.append(text(cx, 330, f"left for the load: {term}", 14, "#9ae6b4", weight="bold"))
    parts.append(text(w / 2, 372, "Lower internal resistance is why NiMH cells handle high-current loads well, even at a lower nominal voltage", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Two AA cells under a 1 amp load. An alkaline cell with 150 to 300 milliohms of internal resistance loses 0.15 to 0.30 volts inside itself, leaving 1.20 to 1.35 volts. A charged NiMH cell with 30 milliohms loses only 0.03 volts, leaving 1.17 volts.")


# 5. Capacity shrinks at high current ------------------------------------------------
def capacity_vs_drain():
    w, h = 800, 400
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "One alkaline AA, four loads: drain it faster and it delivers less", 16, TEXT, weight="bold"))
    data = [(25, 3000), (100, 2500), (250, 2000), (500, 1500)]
    base, scale = 320, 0.075
    for i, (ma, mah) in enumerate(data):
        x = 110 + i * 160
        parts += box3d(x, base, 90, 30, mah * scale, AMBER if i == 0 else shade(AMBER, -0.15 * i), shadow=False)
        parts.append(text(x + 45, base - mah * scale - 22, f"~{mah:,} mAh", 15, TEXT, weight="bold"))
        parts.append(text(x + 45, base + 24, f"at {ma} mA", 14, AMBER_LIGHT, weight="bold"))
        parts.append(text(x + 45, base + 44, f"~{mah / ma:.0f} hours" if mah / ma >= 2 else f"~{mah / ma:.1f} hours", 12, MUTED, italic=True))
    parts.append(text(w / 2, 384, "approximate values read from the Energizer E91 datasheet's capacity chart", 11, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "A 3D bar chart of one alkaline AA cell's capacity at four currents: about 3,000 milliamp-hours at 25 milliamps, 2,500 at 100, 2,000 at 250, and 1,500 at 500, so heavier loads both drain it faster and get less total charge out of it.")


# 6. Lithium-ion warning signs ---------------------------------------------------------
def liion_warning():
    w, h = 860, 380
    parts = [common_defs()]
    parts.append(text(w / 2, 34, "A lithium-ion battery in trouble: stop using it if it…", 16, TEXT, weight="bold"))
    signs = [("smells strange", "~"), ("feels hot", "♨"), ("swells or bulges", "◯"), ("pops or hisses", "‼")]
    for i, (sign, glyph) in enumerate(signs):
        cx = 115 + i * 210
        parts.append(panel(cx - 95, 55, 190, 190))
        parts.append(f'<circle cx="{cx}" cy="135" r="46" fill="#c53030" fill-opacity="0.25" stroke="#fc8181" stroke-opacity="0.7"/>')
        if i == 2:
            parts.append(f'<rect x="{cx - 34}" y="108" width="68" height="54" rx="22" fill="#4a5568" stroke="#fc8181" stroke-width="2"/>')
        else:
            parts.append(text(cx, 150, glyph, 40, "#fc8181", weight="bold"))
        parts.append(text(cx, 218, sign, 15, TEXT, weight="bold"))
    parts.append(f'<rect x="70" y="270" width="720" height="86" rx="16" fill="#c53030" fill-opacity="0.85"/>')
    parts.append(f'<rect x="70" y="270" width="720" height="86" rx="16" fill="url(#gloss)"/>')
    parts.append(text(430, 303, "Move it away from anything that can burn, and call the fire department.", 16, "#ffffff", weight="bold"))
    parts.append(text(430, 330, "If it's already on fire: get everyone out, close the door behind you, and call 9-1-1.", 14, "#ffffff"))
    return svg(w, h, "\n".join(parts), "Four warning signs of a failing lithium-ion battery: it smells strange, feels hot, swells or bulges, or pops or hisses. Below, the response: move it away from anything that can burn and call the fire department; if it is already on fire, get everyone out, close the door, and call 9-1-1.")


FIGURES = {
    "cell_anatomy.svg": cell_anatomy,
    "series_parallel.svg": series_parallel,
    "chemistry_chart.svg": chemistry_chart,
    "internal_resistance_load.svg": internal_resistance_load,
    "capacity_vs_drain.svg": capacity_vs_drain,
    "liion_warning.svg": liion_warning,
}

if __name__ == "__main__":
    for name, e_wh, kg in (("alkaline AA", 2.5 * 1.25, 0.023), ("NiMH AA", 2.3 * 1.2, 0.028)):
        print(f"{name}: {e_wh:.2f} Wh / {kg * 1000:.0f} g = {e_wh / kg:.0f} Wh/kg")
    render_all(FIGURES, OUT)
