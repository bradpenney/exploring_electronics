#!/usr/bin/env python3
"""Figures for docs/tools/multimeter.md.

Sources:
- Fluke 114/115/116/117 detailed specifications (media.fluke.com):
  DC volts input impedance > 10 Mohm; 6,000 counts; DC volts ranges 6.000 /
  60.00 / 600.0 V, accuracy +/-(0.5 % + 2 counts); A input burden 37 mV/A
  on the 10 A input (about 0.037 ohm); A input fuse 11 A, 1000 V, 17 kA
  interrupting; CAT III 600 V.
- Fluke "ABCs of multimeter safety": measurement categories CAT IV / III / II /
  0 and examples; test transients for 600 V ratings: CAT 0 2500 V, CAT II
  4000 V, CAT III 6000 V, CAT IV 8000 V.
- Battery: 12.6 V, a full 12 V lead-acid battery (see batteries.md).

Usage:
    python3 illustrations/multimeter.py
"""

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, box3d,  # noqa: E402
                     common_defs, panel, pill, render_all, shade, svg, text)

OUT = HERE.parent / "docs" / "images" / "multimeter"
BLUE = "#4299e1"
V_BATT = 12.6
R_VOLTS = 10e6
R_AMPS = 0.037


def _lcd(parts, x, y, w, h, reading, small=None):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#9fb59a"/>')
    parts.append(f'<rect x="{x + 4}" y="{y + 4}" width="{w - 8}" height="{h - 8}" rx="4" fill="#b8ccb2"/>')
    parts.append(f'<text x="{x + w - 14}" y="{y + h * 0.72:.1f}" font-size="{h * 0.6:.0f}" fill="#1f2a1d" '
                 f'text-anchor="end" font-family="DejaVu Sans Mono, monospace" font-weight="bold">{reading}</text>')
    if small:
        parts.append(f'<text x="{x + 10}" y="{y + 18}" font-size="11" fill="#1f2a1d" font-weight="bold">{small}</text>')


def _jack(parts, x, y, label, plug=None):
    parts.append(f'<circle cx="{x}" cy="{y}" r="17" fill="#111"/>')
    parts.append(f'<circle cx="{x}" cy="{y}" r="17" fill="none" stroke="{shade("#4a5568", 0.3)}" stroke-width="3"/>')
    parts.append(f'<circle cx="{x}" cy="{y}" r="6" fill="#555"/>')
    if plug:
        parts.append(f'<circle cx="{x}" cy="{y}" r="13" fill="{plug}"/>')
        parts.append(f'<circle cx="{x - 4}" cy="{y - 4}" r="4" fill="#ffffff" fill-opacity="0.45"/>')
    parts.append(text(x, y + 34, label, 12, TEXT, weight="bold"))


# 1. Anatomy ----------------------------------------------------------------------------
def anatomy():
    w, h = 900, 560
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    bx, by, bw, bh = 300, 60, 300, 450
    parts.append(f'<rect x="{bx + 10}" y="{by + 14}" width="{bw}" height="{bh}" rx="28" fill="#000" fill-opacity="0.45"/>')
    parts.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="28" fill="{AMBER}"/>')
    parts.append(f'<rect x="{bx + 14}" y="{by + 14}" width="{bw - 28}" height="{bh - 28}" rx="18" fill="#2d3748"/>')
    parts.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="28" fill="url(#gloss)" opacity="0.35"/>')
    _lcd(parts, bx + 40, by + 40, bw - 80, 80, "12.60", "DC V")
    # dial
    cx, cy, r = bx + bw / 2, by + 245, 62
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#1a202c" stroke="#4a5568" stroke-width="3"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r - 16}" fill="url(#core)"/>')
    labels = ["OFF", "V~", "V⎓", "mV", "Ω", "•)))", "→|", "A"]
    for k, lab in enumerate(labels):
        ang = math.radians(-150 + k * 300 / (len(labels) - 1))
        lx, ly = cx + (r + 22) * math.sin(ang), cy - (r + 22) * math.cos(ang)
        parts.append(text(lx, ly + 4, lab, 12, AMBER_LIGHT if lab == "V⎓" else TEXT, weight="bold"))
    ang = math.radians(-150 + 2 * 300 / 7)
    parts.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + (r - 10) * math.sin(ang):.1f}" y2="{cy - (r - 10) * math.cos(ang):.1f}" '
                 f'stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>')
    # jacks
    jy = by + 395
    _jack(parts, bx + 70, jy, "A")
    _jack(parts, bx + 150, jy, "COM", "#1a1a1a")
    _jack(parts, bx + 230, jy, "VΩ", RED)
    # leads
    parts.append(f'<path d="M{bx + 150},{jy} C{bx + 150},{jy + 90} {bx + 40},{jy + 60} {bx - 120},{jy + 40}" stroke="#222" stroke-width="7" fill="none"/>')
    parts.append(f'<path d="M{bx + 230},{jy} C{bx + 230},{jy + 90} {bx + 340},{jy + 60} {bx + 460},{jy + 40}" stroke="{RED}" stroke-width="7" fill="none"/>')
    # callouts
    def callout(x1, y1, x2, y2, label, sub, anchor):
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{MUTED}" stroke-width="1.5"/>')
        parts.append(f'<circle cx="{x1}" cy="{y1}" r="4" fill="{AMBER_LIGHT}"/>')
        dx = -8 if anchor == "end" else 8
        parts.append(text(x2 + dx, y2 - 4, label, 15, AMBER_LIGHT, anchor, weight="bold"))
        parts.append(text(x2 + dx, y2 + 14, sub, 12, MUTED, anchor, italic=True))
    callout(bx + 40, by + 80, 250, 100, "Display", "the reading, its unit, and OL for overload", "end")
    callout(cx - r, cy, 250, 260, "Dial", "chooses what to measure", "end")
    callout(bx + 70, jy - 17, 250, 400, "Jacks", "choose how the meter is wired inside", "end")
    callout(cx + r + 30, cy - 40, 650, 220, "Symbols", "V⎓ DC volts, V~ AC volts, Ω ohms,", "start")
    parts.append(text(658, 250, "•))) continuity, →| diode, A amps", 12, MUTED, "start", italic=True))
    callout(bx + 230, jy + 17, 650, 420, "Probe leads", "black always in COM; red moves", "start")
    return svg(w, h, "\n".join(parts), "A 3D handheld multimeter. The display at the top reads 12.60 DC volts. Below it, a rotary dial surrounded by symbols: off, AC volts, DC volts, millivolts, ohms, continuity, diode and amps, set to DC volts. At the bottom, three jacks: A, COM with the black lead, and V-ohms with the red lead. Callouts explain that the dial chooses what to measure and the jacks choose how the meter is wired inside.")


# 2. Two roles, a billion-to-one apart --------------------------------------------------
def two_roles():
    w, h = 900, 490
    parts = [common_defs(), panel(15, 15, 425, h - 55), panel(460, 15, 425, h - 55)]
    rows = [(227, "Leads in VΩ: a voltmeter", R_VOLTS, GREEN), (672, "Leads in A: an ammeter", R_AMPS, RED)]
    base = 360
    for cx, title, r, color in rows:
        i = V_BATT / r
        parts.append(text(cx, 50, title, 17, AMBER_LIGHT, weight="bold"))
        parts.append(text(cx, 72, f"probes across a {V_BATT:g} V battery", 12, MUTED, italic=True))
        # resistance bar (log, 0.01 ohm .. 100 Mohm => 10 decades)
        hr = (math.log10(r) + 2) / 10 * 230
        parts += box3d(cx - 120, base, 70, 34, hr, "#718096")
        rl = "10 MΩ" if r > 1e6 else f"{r:.3f} Ω"
        parts.append(text(cx - 85, base - hr - 28, rl, 15, TEXT, weight="bold"))
        parts.append(text(cx - 85, base + 28, "resistance", 13, MUTED))
        # current bar (log, 1e-7 .. 1e3 A => 10 decades)
        hi = (math.log10(i) + 7) / 10 * 230
        parts += box3d(cx + 40, base, 70, 34, hi, color)
        il = f"{i * 1e6:.2f} µA" if i < 1e-3 else f"≈{round(i, -1):.0f} A"
        parts.append(text(cx + 75, base - hi - 28, il, 15, TEXT, weight="bold"))
        parts.append(text(cx + 75, base + 28, "current it allows", 13, MUTED))
    parts.append(text(227, 420, "harmless: the battery doesn't notice", 13, GREEN, weight="bold"))
    parts.append(text(672, 420, "a short: only the 11 A fuse stops it", 13, RED, weight="bold"))
    parts.append(text(w / 2, 476, "bar heights on log scales; the meter alone would allow this current, before battery and lead resistance", 11, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Two panels of 3D bars on log scales for a meter's probes across a 12.6 volt battery. With the leads in the volts jack, the meter is 10 megohms and allows 1.26 microamps, which is harmless. With the leads in the amps jack, it is 0.037 ohms and would allow about 340 amps, a short circuit that only the meter's 11 amp fuse stops.")


# 3. Which jacks for which job ------------------------------------------------------------
def jack_setups():
    w, h = 900, 330
    parts = [common_defs()]
    setups = [("Volts, ohms, continuity, diode", "VΩ", "the everyday setup", GREEN),
              ("Small currents (mA, µA)", "mA", "in series, small fuse", AMBER),
              ("Large currents (up to 10 A)", "A", "in series, large fuse", RED)]
    for k, (title, red_in, sub, col) in enumerate(setups):
        x0 = 15 + k * 295
        parts.append(panel(x0, 15, 280, h - 30))
        parts.append(text(x0 + 140, 50, title, 14, AMBER_LIGHT, weight="bold"))
        parts.append(f'<rect x="{x0 + 24}" y="110" width="232" height="110" rx="16" fill="#2d3748" stroke="#4a5568" stroke-width="2"/>')
        for j, lab in enumerate(["A", "mA", "COM", "VΩ"]):
            plug = "#1a1a1a" if lab == "COM" else (RED if lab == red_in else None)
            _jack(parts, x0 + 56 + j * 56, 150, lab, plug)
        parts += pill(x0 + 140, 262, sub, col, size=13, h=30)
    parts.append(text(w / 2, h - 2, "", 1, MUTED))
    return svg(w, h, "\n".join(parts), "Three panels of a four-jack meter: A, mA, COM and V-ohms. For volts, ohms, continuity and diode tests, the black lead goes in COM and the red in V-ohms. For small currents the red lead moves to mA, which has a small fuse. For currents up to 10 amps it moves to A, which has a large fuse. The black lead stays in COM every time.")


# 4. Ranging and resolution ------------------------------------------------------------------
def ranging():
    w, h = 900, 330
    parts = [common_defs()]
    v = 9.27
    ranges = [("6.000 V range", "OL", "too small: overload"),
              ("60.00 V range", f"{v:.2f}", "auto-ranging picks this one"),
              ("600.0 V range", f"{v:.1f}", "fits, but one digit lost")]
    for k, (title, reading, sub) in enumerate(ranges):
        x0 = 15 + k * 295
        parts.append(panel(x0, 15, 280, h - 30))
        parts.append(text(x0 + 140, 50, title, 15, AMBER_LIGHT, weight="bold"))
        _lcd(parts, x0 + 30, 90, 220, 90, reading, "DC V")
        col = RED if reading == "OL" else (GREEN if k == 1 else AMBER)
        parts += pill(x0 + 140, 230, sub, col, size=13, h=30)
    parts.append(text(w / 2, 300, f"the same {v} V battery on a 6,000-count meter's three ranges", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Three meter displays reading the same 9.27 volt battery on a 6,000-count meter. On the 6 volt range the display shows OL for overload. On the 60 volt range it shows 9.27, the range auto-ranging picks. On the 600 volt range it shows 9.3, which fits but loses a digit.")


# 5. Measurement categories --------------------------------------------------------------------
def categories():
    w, h = 900, 470
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Measurement categories: the closer to the utility supply, the bigger the spikes", 16, AMBER_LIGHT, weight="bold"))
    cats = [("CAT IV", "service drop, outdoor lines,\nelectricity meter", 8000, "#c53030"),
            ("CAT III", "distribution panel, fixed\nwiring, short branch circuits", 6000, "#dd6b20"),
            ("CAT II", "outlets and long branch\ncircuits, plug-in appliances", 4000, AMBER),
            ("CAT 0", "protected electronics,\nbattery circuits", 2500, GREEN)]
    base = 330
    for k, (name, where, spike, col) in enumerate(cats):
        x = 70 + k * 205
        hgt = spike / 8000 * 200
        parts += box3d(x, base, 110, 50, hgt, col)
        parts.append(text(x + 55, base - hgt / 2 + 6, name, 17, "#ffffff" if k < 2 else "#1a1a1a", weight="bold"))
        parts.append(text(x + 72, base - hgt - 34, f"{spike:,} V", 15, TEXT, weight="bold"))
        for j, line in enumerate(where.split("\n")):
            parts.append(text(x + 55, base + 30 + j * 16, line, 12, MUTED))
        if k < 3:
            parts.append(f'<path d="M{x + 140},{base - 20} l40,0" stroke="{MUTED}" stroke-width="2" marker-end="url(#arrow)"/>')
    parts.append(text(w / 2, 420, "bar height: the test spike a 600 V meter must survive in each category", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Four 3D bars from left to right, following power from the utility into a building. CAT IV, the service drop and electricity meter: a 600 volt meter must survive 8,000 volt test spikes. CAT III, the distribution panel and fixed wiring: 6,000 volts. CAT II, outlets and plug-in appliances: 4,000 volts. CAT 0, protected electronics and battery circuits: 2,500 volts.")


FIGURES = {"anatomy.svg": anatomy, "two_roles.svg": two_roles, "jack_setups.svg": jack_setups,
           "ranging.svg": ranging, "categories.svg": categories}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
