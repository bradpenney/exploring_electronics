#!/usr/bin/env python3
"""Figures for docs/voltage.md.

Numbers and their sources:
- 1 C = 6.242e18 electrons (elementary charge 1.602176634e-19 C, exact SI value)
- Energizer E91 AA datasheet: 1.5 V nominal alkaline, ~2,500 mAh at 100 mA
  (9,000 C); voltage sags from ~1.5 V toward the 0.8 V cutoff, mid-discharge
  ~1.25 V, so ~11 kJ.
- Energizer 522 datasheet: 9 V, IEC 6LR61 = six 1.5 V cells in series.
- Lead-acid car battery: six ~2.1 V cells, ~12.6 V fully charged.
- NOAA JetStream lightning FAQ: ~300 million volts.
- Hydro-Quebec: 735 kV lines, the world's first, commissioned 1965.
- Canadian outlets: 120 V nominal. Dry-air breakdown ~3 kV per mm (see the
  conductors article), so a visible spark of a few mm needs several kV.

Usage:
    python3 illustrations/voltage.py
"""

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, box3d,  # noqa: E402
                     common_defs, cyl_gradient, panel, pill, render_all, shade,
                     svg, text)

OUT = HERE.parent / "docs" / "images" / "voltage"


def multimeter(x, y, reading, w=120, h=150, mode="V⎓"):
    """A handheld meter: body, LCD with reading, dial set to `mode`; (x, y) = top-left."""
    return [
        f'<ellipse cx="{x + w / 2}" cy="{y + h + 6}" rx="{w / 2 + 8}" ry="8" fill="#000" fill-opacity="0.4"/>',
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#d69e2e"/>',
        f'<rect x="{x + 8}" y="{y + 8}" width="{w - 16}" height="{h - 16}" rx="10" fill="#1a1d23"/>',
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="url(#gloss)" opacity="0.5"/>',
        f'<rect x="{x + 16}" y="{y + 18}" width="{w - 32}" height="42" rx="4" fill="#9ae6b4"/>',
        f'<rect x="{x + 16}" y="{y + 18}" width="{w - 32}" height="14" rx="4" fill="#ffffff" fill-opacity="0.25"/>',
        text(x + w / 2, y + 48, reading, 22 if len(reading) <= 5 else 17, "#1a202c", weight="bold"),
        f'<circle cx="{x + w / 2}" cy="{y + 100}" r="22" fill="url(#core)"/>',
        f'<line x1="{x + w / 2}" y1="{y + 100}" x2="{x + w / 2 - 12}" y2="{y + 84}" stroke="#f7fafc" stroke-width="3"/>',
        text(x + w / 2 + 34, y + 92, mode, 11, AMBER_LIGHT, weight="bold"),
        f'<circle cx="{x + 34}" cy="{y + h - 14}" r="6" fill="#e53e3e"/>',
        f'<circle cx="{x + w - 34}" cy="{y + h - 14}" r="7.5" fill="#cbd5e0" fill-opacity="0.55"/>',
        f'<circle cx="{x + w - 34}" cy="{y + h - 14}" r="6" fill="#111"/>',
    ]


def probe_lead(x1, y1, x2, y2, color):
    """A test lead from a meter socket to a probe tip touching (x2, y2).

    Leads are drawn as glossy cables with a pale halo underneath, so the black
    (common) lead stays visible on the dark slate background.
    """
    mx, my = (x1 + x2) / 2, max(y1, y2) + 60
    path = f'M{x1},{y1} Q{mx},{my} {x2},{y2 + 26}'
    hi = shade(color, 0.55) if color != "#111" else "#718096"
    return [f'<path d="{path}" fill="none" stroke="#cbd5e0" stroke-opacity="0.55" stroke-width="7.5"/>',
            f'<path d="{path}" fill="none" stroke="{color}" stroke-width="4.5"/>',
            f'<path d="{path}" fill="none" stroke="{hi}" stroke-opacity="0.8" stroke-width="1.4" transform="translate(-1,-1)"/>',
            f'<rect x="{x2 - 6.5}" y="{y2 + 4.5}" width="13" height="29" rx="5" fill="#cbd5e0" fill-opacity="0.55"/>',
            f'<rect x="{x2 - 5}" y="{y2 + 6}" width="10" height="26" rx="4" fill="{color}"/>',
            f'<rect x="{x2 - 3}" y="{y2 + 8}" width="2.5" height="22" rx="1" fill="{hi}" fill-opacity="0.7"/>',
            f'<line x1="{x2}" y1="{y2 + 6}" x2="{x2}" y2="{y2 - 2}" stroke="#e2e8f0" stroke-width="2.5"/>']


# 1. Two points ------------------------------------------------------------------
def two_points():
    w, h = 800, 460
    parts = [common_defs(cyl_gradient("wire", "#b8673a") + cyl_gradient("gnd", "#4a5568")), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "Voltage only exists between two points", 16, TEXT, weight="bold"))
    # live wire across the top, ground bar along the bottom
    parts.append(f'<rect x="40" y="96" width="720" height="18" rx="9" fill="url(#wire)"/>')
    parts.append(text(56, 88, "live wire: 120 V above ground", 12, AMBER_LIGHT, "start", italic=True))
    parts.append(f'<rect x="40" y="380" width="720" height="16" rx="8" fill="url(#gnd)"/>')
    parts.append(text(56, 414, "ground: 0 V, the reference", 12, MUTED, "start", italic=True))
    # meter A: both probes on the wire
    parts += multimeter(150, 190, "0.0")
    parts += probe_lead(184, 326, 150, 114, "#e53e3e") + probe_lead(236, 326, 280, 114, "#111")
    parts.append(text(210, 170, "both probes on the same wire", 13, TEXT, weight="bold"))
    parts.append(text(210, 362, "same height: no difference", 12, MUTED, italic=True))
    # meter B: wire to ground
    parts += multimeter(520, 190, "120.0")
    parts += probe_lead(554, 326, 520, 114, "#e53e3e")
    parts.append('<path d="M606,326 Q640,360 650,380" fill="none" stroke="#cbd5e0" stroke-opacity="0.55" stroke-width="7.5"/>')
    parts.append('<path d="M606,326 Q640,360 650,380" fill="none" stroke="#111" stroke-width="4.5"/>')
    parts.append('<path d="M606,326 Q640,360 650,380" fill="none" stroke="#718096" stroke-opacity="0.8" stroke-width="1.4" transform="translate(-1,-1)"/>')
    parts.append(text(580, 170, "one on the wire, one on ground", 13, TEXT, weight="bold"))
    parts.append(text(700, 300, "a 120 V", 12, AMBER_LIGHT, "start", italic=True))
    parts.append(text(700, 316, "difference", 12, AMBER_LIGHT, "start", italic=True))
    return svg(w, h, "\n".join(parts), "Two voltmeters on a live 120 volt wire. With both probes on the wire, the meter reads 0 volts. With one probe on the wire and one on ground, it reads 120 volts.")


# 2. Energy per charge: lift and roll -------------------------------------------------
def energy_hill():
    w, h = 800, 470
    parts = [common_defs(cyl_gradient("tower", AMBER, vertical=True)), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "A 9 V battery gives every coulomb 9 joules; the circuit takes them back", 15, TEXT, weight="bold"))
    base, top = 380, 130
    # battery as a lift tower
    parts.append(f'<ellipse cx="135" cy="{base + 6}" rx="60" ry="10" fill="#000" fill-opacity="0.4"/>')
    parts.append(f'<rect x="85" y="{top}" width="100" height="{base - top}" rx="8" fill="url(#tower)"/>')
    parts.append(f'<rect x="85" y="{top}" width="100" height="{base - top}" rx="8" fill="url(#gloss)" opacity="0.4"/>')
    parts.append(text(135, top + 40, "9 V", 26, "#1a1a1a", weight="bold"))
    parts.append(text(135, top + 66, "battery", 13, "#1a1a1a"))
    parts.append(f'<line x1="166" y1="{base - 20}" x2="166" y2="{top + 90}" stroke="#1a1a1a" stroke-width="3" marker-end="url(#arrow)"/>')
    parts.append(text(122, base - 48, "lifts each", 12, "#1a1a1a", weight="bold"))
    parts.append(text(122, base - 32, "coulomb", 12, "#1a1a1a", weight="bold"))
    # high ledge and ramp down through a load
    parts += box3d(185, top + 30, 140, 40, 14, "#4a5568", shadow=False)
    ramp = f'M325,{top + 18} L600,{base - 40}'
    parts.append(f'<path d="{ramp}" stroke="#2d3748" stroke-width="22" stroke-linecap="round"/>')
    parts.append(f'<path d="{ramp}" stroke="#4a5568" stroke-width="16" stroke-linecap="round"/>')
    parts += box3d(185, base, 470, 40, 12, "#2d3748", shadow=False)
    # balls (coulombs)
    for k, (bx, by) in enumerate([(210, top + 4), (250, top + 4), (290, top + 4)] +
                                 [(325 + t * 275, top + 4 + t * (base - 40 - top - 18)) for t in (0.18, 0.62)] +
                                 [(560 - k2 * 60, base - 26) for k2 in range(4)]):
        parts.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="22" fill="url(#glow)"/><circle cx="{bx:.1f}" cy="{by:.1f}" r="10" fill="url(#vball)"/>')
    # load: a lamp the balls drive on the way down
    lx, ly = 470, 210
    parts.append(f'<circle cx="{lx}" cy="{ly}" r="44" fill="#fefcbf" fill-opacity="0.25"/>')
    parts.append(f'<circle cx="{lx}" cy="{ly}" r="24" fill="url(#vball)"/>')
    parts.append(text(lx + 40, ly - 30, "the load spends the energy", 12, AMBER_LIGHT, "start", italic=True))
    parts.append(text(lx + 40, ly - 14, "(light, heat, motion)", 12, AMBER_LIGHT, "start", italic=True))
    # height scale
    parts.append(f'<line x1="720" y1="{top + 16}" x2="720" y2="{base}" stroke="{MUTED}" stroke-width="2"/>')
    for lab, yy in (("9 J per coulomb", top + 16), ("0 J per coulomb", base)):
        parts.append(f'<line x1="712" y1="{yy}" x2="728" y2="{yy}" stroke="{MUTED}" stroke-width="2"/>')
        parts.append(text(712, yy - 8, lab, 12, TEXT, "end", "bold"))
    parts.append(text(w / 2, 432, "height = voltage: energy per coulomb, not how many coulombs there are", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Voltage as height: a 9 volt battery lifts each coulomb of charge to a height worth 9 joules; the charges roll down a ramp through a glowing load that spends the energy, and return to the bottom at 0 joules per coulomb")


# 3. Reference zero ----------------------------------------------------------------
def reference_zero():
    w, h = 800, 440
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "Zero is a choice: only the difference is real", 16, TEXT, weight="bold"))
    base = 340
    cols = [(70, 220, "#4a5568", "Hilltop A"), (330, 120, "#4a5568", "Valley B")]
    for x, hgt, c, lab in cols:
        parts += box3d(x, base, 150, 60, hgt, c)
        parts.append(text(x + 75, base - hgt - 40, lab, 14, TEXT, weight="bold"))
    parts.append(text(145, base - 70, "300 m above sea", 13, "#ffffff", weight="bold"))
    parts.append(text(145, base - 50, "+200 m above B", 13, AMBER_LIGHT, weight="bold"))
    parts.append(text(405, base - 70, "100 m above sea", 13, "#ffffff", weight="bold"))
    parts.append(text(405, base - 50, "0 m above B", 13, AMBER_LIGHT, weight="bold"))
    parts.append(text(275, base + 40, "measured from sea level or from B, A is always 200 m higher", 12, MUTED, italic=True))
    # circuit equivalent: rails as glossy bars
    parts.append(text(650, 100, "In a circuit", 14, TEXT, weight="bold"))
    for lab, y, c in (("5 V rail", 150, AMBER), ("3.3 V rail", 205, "#d69e2e"), ("ground: 0 V", 300, "#4a5568")):
        parts += pill(650, y, lab, c, "#1a1a1a" if c != "#4a5568" else "#fff", wpx=170, size=13, h=34)
    parts.append(text(650, 340, "“5 V on this pin” means", 12, MUTED, italic=True))
    parts.append(text(650, 356, "5 V above ground", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Two blocks of land: hilltop A at 300 metres and valley B at 100 metres above sea level. Measured from B instead, A is 200 metres and B is 0. In a circuit, rails at 5 volts and 3.3 volts are measured from ground at 0 volts.")


# 4. Cells in series -----------------------------------------------------------------
def cells_in_series():
    w, h = 800, 460
    grads = cyl_gradient("cell", "#a0aec0", vertical=True) + cyl_gradient("lead", "#718096", vertical=True)
    parts = [common_defs(grads), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "Stack cells in series and their voltages add", 16, TEXT, weight="bold"))

    def stack(cx, n, v_each, color_id, cell_h, label, sub):
        out = []
        base = 380
        for k in range(n):
            y = base - (k + 1) * cell_h
            out.append(f'<rect x="{cx - 26}" y="{y}" width="52" height="{cell_h - 4}" rx="6" fill="url(#{color_id})"/>')
            out.append(f'<ellipse cx="{cx}" cy="{y}" rx="26" ry="6" fill="#e2e8f0" fill-opacity="0.6"/>')
            out.append(text(cx + 44, y + cell_h / 2 + 4, f"+{v_each:g} V", 12, MUTED, "start"))
            out.append(text(cx - 44, y + cell_h / 2 + 4, f"{v_each * (k + 1):.1f} V", 12, AMBER_LIGHT, "end", "bold"))
        out.append(f'<ellipse cx="{cx}" cy="{base + 4}" rx="40" ry="8" fill="#000" fill-opacity="0.4"/>')
        out.append(text(cx, base + 30, label, 15, TEXT, weight="bold"))
        out.append(text(cx, base + 50, sub, 12, MUTED, italic=True))
        return out
    parts += stack(240, 6, 1.5, "cell", 46, "9 V battery", "six 1.5 V alkaline cells (IEC 6LR61)")
    parts += stack(560, 6, 2.1, "lead", 46, "12 V car battery", "six ~2.1 V lead-acid cells")
    return svg(w, h, "\n".join(parts), "Two stacks of six cells. A 9 volt battery is six 1.5 volt cells adding up to 9 volts. A car battery is six roughly 2.1 volt cells adding up to about 12.6 volts.")


# 5. Voltage scale ------------------------------------------------------------------
def voltage_scale():
    w, h = 800, 330
    L, R = 50, 750
    lo, hi = -1, 9
    X = lambda v: L + (R - L) * (math.log10(v) - lo) / (hi - lo)
    edge = (X(50) - L) / (R - L)  # ~50 V: the usual extra-low-voltage safety line
    stops = (f'<stop offset="0" stop-color="{GREEN}"/><stop offset="{edge:.3f}" stop-color="{GREEN}"/>'
             f'<stop offset="{edge:.3f}" stop-color="{RED}"/><stop offset="1" stop-color="{RED}"/>')
    parts = [common_defs(f'<linearGradient id="vbands" x1="0" y1="0" x2="1" y2="0">{stops}</linearGradient>'),
             panel(15, 15, w - 30, h - 30)]
    ty, th = 140, 28
    parts.append(f'<rect x="{L}" y="{ty}" width="{R - L}" height="{th}" rx="14" fill="url(#vbands)" fill-opacity="0.5"/>')
    parts.append(f'<rect x="{L}" y="{ty}" width="{R - L}" height="{th}" rx="14" fill="url(#gloss)" stroke="#e2e8f0" stroke-opacity="0.35"/>')
    for p in range(lo, hi + 1):
        x = X(10 ** p)
        parts.append(f'<line x1="{x:.1f}" y1="{ty + th}" x2="{x:.1f}" y2="{ty + th + 6}" stroke="{MUTED}"/>')
        parts.append(f'<text x="{x:.1f}" y="{ty + th + 22}" font-size="11" fill="{MUTED}" text-anchor="middle">10<tspan dy="-5" font-size="8">{p}</tspan></text>')
    items = [(0.6, "solar cell", True), (1.5, "AA cell", False), (5, "USB", True), (12.6, "car battery", False),
             (120, "outlet", True), (735e3, "Hydro-Québec line", True), (3e8, "lightning", False)]
    for v, lab, above in items:
        x = X(v)
        parts.append(f'<circle cx="{x:.1f}" cy="{ty + th / 2}" r="8" fill="url(#eball)"/>')
        y = ty - 26 if above else ty + th + 62
        parts.append(f'<line x1="{x:.1f}" y1="{ty - 2 if above else ty + th + 28}" x2="{x:.1f}" y2="{y + (6 if above else -14)}" stroke="{MUTED}"/>')
        vs = (f"{v:g} V" if v < 1000 else (f"{v / 1000:g} kV" if v < 1e6 else f"{v / 1e6:g} MV"))
        parts.append(text(x, y - (16 if above else 0), lab, 13, TEXT, weight="bold"))
        parts.append(text(x, y + (0 if above else 16), vs, 12, AMBER_LIGHT))
    parts.append(text(w / 2, 46, "Voltages you'll meet, log scale: each tick is 10×", 16, TEXT, weight="bold"))
    parts.append(text(w / 2, h - 30, "green: under about 50 V, where hobby circuits live · red: mains and above, can kill", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "A log scale of voltages from a 0.6 volt solar cell through a 1.5 volt AA cell, 5 volt USB, a 12.6 volt car battery and a 120 volt outlet, up to a 735 kilovolt Hydro-Québec transmission line and 300 megavolt lightning")


# 6. Where voltage comes from ----------------------------------------------------------
def sources():
    w, h = 970, 400
    parts = [common_defs(cyl_gradient("bat", AMBER, vertical=True) + cyl_gradient("coil", "#b8673a")), ]
    parts.append(text(w / 2, 34, "Every source separates charge; they differ in what does the pushing", 15, TEXT, weight="bold"))
    cards = [("Chemistry", "battery", "1.5 V per alkaline cell"), ("Light", "solar cell", "about 0.6 V per silicon cell"),
             ("Magnetism", "generator", "rises with speed and turns"), ("Heat", "thermocouple", "millivolts"),
             ("Pressure", "piezo crystal", "a squeeze makes a spark"), ("Friction", "static", "thousands of volts, tiny charge")]
    for i, (what, name, val) in enumerate(cards):
        cx = 86 + i * 159
        parts.append(panel(cx - 74, 52, 148, 330))
        parts.append(text(cx, 80, what, 15, AMBER_LIGHT, weight="bold"))
        y = 180
        if i == 0:
            parts.append(f'<rect x="{cx - 22}" y="{y - 50}" width="44" height="100" rx="6" fill="url(#bat)"/>')
            parts.append(f'<rect x="{cx - 8}" y="{y - 58}" width="16" height="9" rx="2" fill="#cbd5e0"/>')
            parts.append(text(cx, y + 6, "+", 20, "#1a1a1a", weight="bold"))
        elif i == 1:
            pts = f"{cx - 52},{y + 30} {cx + 30},{y + 30} {cx + 52},{y - 30} {cx - 30},{y - 30}"
            parts.append(f'<polygon points="{pts}" fill="#2b4c9b"/>')
            for k in range(1, 4):
                parts.append(f'<line x1="{cx - 52 + k * 20.5:.1f}" y1="{y + 30}" x2="{cx - 30 + k * 20.5:.1f}" y2="{y - 30}" stroke="#90cdf4" stroke-opacity="0.6"/>')
            parts.append(f'<polygon points="{pts}" fill="url(#gloss)" opacity="0.7"/>')
            parts.append(f'<circle cx="{cx + 40}" cy="{y - 62}" r="16" fill="#fefcbf"/><circle cx="{cx + 40}" cy="{y - 62}" r="30" fill="#fefcbf" fill-opacity="0.2"/>')
        elif i == 2:
            for k in range(6):
                parts.append(f'<ellipse cx="{cx - 30 + k * 12}" cy="{y}" rx="7" ry="30" fill="none" stroke="url(#coil)" stroke-width="5"/>')
            parts.append(f'<rect x="{cx - 54}" y="{y - 10}" width="44" height="20" rx="3" fill="#e53e3e"/>')
            parts.append(f'<rect x="{cx - 32}" y="{y - 10}" width="22" height="20" rx="3" fill="#3182ce"/>')
            parts.append(text(cx - 43, y + 5, "N", 11, "#fff", weight="bold"))
            parts.append(text(cx - 21, y + 5, "S", 11, "#fff", weight="bold"))
        elif i == 3:
            parts.append(f'<circle cx="{cx}" cy="{y + 20}" r="34" fill="#fc8181" fill-opacity="0.25"/>')
            parts.append(f'<path d="M{cx - 40},{y - 40} L{cx},{y + 20}" stroke="#b8673a" stroke-width="6" stroke-linecap="round"/>')
            parts.append(f'<path d="M{cx + 40},{y - 40} L{cx},{y + 20}" stroke="#cbd5e0" stroke-width="6" stroke-linecap="round"/>')
            parts.append(f'<circle cx="{cx}" cy="{y + 20}" r="7" fill="url(#vball)"/>')
        elif i == 4:
            # a crystal squeezed between two jaws; charge piles up on its faces
            parts += box3d(cx - 30, y + 26, 60, 26, 52, "#7f9cf5", shadow=False)
            for dy, rot in ((-58, 90), (58, -90)):
                parts.append(f'<path d="M-9,-9 L5,0 L-9,9" fill="none" stroke="{AMBER_LIGHT}" stroke-width="4" '
                             f'stroke-linecap="round" transform="translate({cx + 8},{y + dy}) rotate({rot})"/>')
            parts.append(text(cx - 44, y - 4, "+", 18, "#fc8181", weight="bold"))
            parts.append(text(cx + 54, y + 16, "−", 18, "#90cdf4", weight="bold"))
        else:
            parts.append(f'<circle cx="{cx}" cy="{y - 8}" r="36" fill="url(#eball)"/>')
            for k in range(5):
                a = -0.6 + k * 0.3
                x1, y1 = cx + 40 * math.cos(a), y - 8 + 40 * math.sin(a)
                parts.append(f'<path d="M{x1:.1f},{y1:.1f} l12,-6 l-4,10 l14,-6" fill="none" stroke="{AMBER_LIGHT}" stroke-width="2.5"/>')
        parts.append(text(cx, 290, name, 14, TEXT, weight="bold"))
        parts.append(text(cx, 314, val.split(",")[0], 11, MUTED))
        if "," in val:
            parts.append(text(cx, 330, val.split(",")[1].strip(), 11, MUTED))
    return svg(w, h, "\n".join(parts), "Six voltage sources: a battery uses chemistry, a solar cell uses light, a generator uses magnetism, a thermocouple uses heat, a piezoelectric crystal uses pressure, and static uses friction")


FIGURES = {
    "two_points.svg": two_points,
    "energy_hill.svg": energy_hill,
    "reference_zero.svg": reference_zero,
    "cells_in_series.svg": cells_in_series,
    "voltage_scale.svg": voltage_scale,
    "sources.svg": sources,
}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
