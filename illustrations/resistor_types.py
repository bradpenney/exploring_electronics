#!/usr/bin/env python3
"""Figures for docs/resistor_types.md.

Sources:
- Yageo CFR datasheet (carbon film): CFR-25 type, under 100 kOhm,
  temperature coefficient -500 to +350 ppm/C.
- Yageo MFR datasheet (metal film): +/-50 or +/-100 ppm/C.
- Log ("audio") taper drawn as the common 10%-at-midpoint shape; labelled as a
  typical curve, since tapers vary by maker.

Usage:
    python3 illustrations/resistor_types.py
"""

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, box3d,  # noqa: E402
                     common_defs, cyl_gradient, panel, pill, render_all, shade,
                     svg, text)

OUT = HERE.parent / "docs" / "images" / "resistor_types"


def body(x, cy, length, r, gid):
    return [f'<rect x="{x}" y="{cy - r}" width="{length}" height="{2 * r}" rx="{r}" fill="url(#{gid})"/>']


def leads(x, cy, length, span=40):
    return [f'<rect x="{x - span}" y="{cy - 2}" width="{span}" height="4" fill="#cbd5e0"/>',
            f'<rect x="{x + length}" y="{cy - 2}" width="{span}" height="4" fill="#cbd5e0"/>']


# 1. The fixed-resistor family, opened up -------------------------------------------------
def fixed_family():
    w, h = 880, 520
    grads = (cyl_gradient("comp", "#7b5a3a") + cyl_gradient("cfilm", "#d9b382") + cyl_gradient("mfilm", "#3b6fb6") +
             cyl_gradient("ceramic", "#e2e8f0") + cyl_gradient("cutcore", "#f7fafc"))
    parts = [common_defs(grads), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "Fixed resistors: what's inside each kind", 16, TEXT, weight="bold"))
    rows = [
        ("Carbon composition", "a solid slug of carbon powder and binder", "comp", None),
        ("Carbon film", "a thin carbon film, spiral-cut to set the value", "cfilm", "#3a2a12"),
        ("Metal film", "a thin metal film, finer spiral, tighter tolerance", "mfilm", "#0d2340"),
        ("Wire-wound", "resistance wire wound on a ceramic core", "ceramic", "wire"),
    ]
    for i, (name, sub, gid, cut) in enumerate(rows):
        cy = 110 + i * 82
        x, L, r = 90, 200, 20
        parts += leads(x, cy, L)
        parts += body(x, cy, L, r, gid)
        # cutaway window showing the inside
        wx, ww = x + 70, 80
        if cut is None:
            parts.append(f'<rect x="{wx}" y="{cy - r + 4}" width="{ww}" height="{2 * r - 8}" fill="#4a3424"/>')
            for k in range(20):
                parts.append(f'<circle cx="{wx + 4 + (k * 37) % ww}" cy="{cy - 10 + (k * 13) % 20}" r="1.6" fill="#1a1a1a"/>')
        elif cut == "wire":
            parts.append(f'<rect x="{wx}" y="{cy - r + 4}" width="{ww}" height="{2 * r - 8}" fill="url(#cutcore)"/>')
            for k in range(11):
                parts.append(f'<line x1="{wx + 4 + k * 7}" y1="{cy - r + 5}" x2="{wx + 8 + k * 7}" y2="{cy + r - 5}" stroke="#b8673a" stroke-width="2.5"/>')
        else:
            parts.append(f'<rect x="{wx}" y="{cy - r + 4}" width="{ww}" height="{2 * r - 8}" fill="url(#cutcore)"/>')
            pitch = 10 if gid == "cfilm" else 6
            for k in range(int(ww / pitch)):
                parts.append(f'<line x1="{wx + k * pitch}" y1="{cy - r + 5}" x2="{wx + k * pitch + pitch * 0.6}" y2="{cy + r - 5}" stroke="{cut}" stroke-width="{pitch * 0.55:.1f}"/>')
        parts.append(f'<rect x="{wx}" y="{cy - r + 4}" width="{ww}" height="{2 * r - 8}" fill="none" stroke="{AMBER}" stroke-dasharray="3 3"/>')
        parts.append(text(380, cy - 4, name, 15, AMBER_LIGHT, "start", "bold"))
        parts.append(text(380, cy + 16, sub, 12, TEXT, "start"))
    # surface mount chip
    cy = 110 + 4 * 82 - 8
    parts += box3d(140, cy + 14, 90, 30, 18, "#22262e", shadow=False)
    for ex in (140, 214):
        parts += box3d(ex, cy + 14, 16, 30, 18, "#cbd5e0", shadow=False)
    parts.append(text(185, cy + 2, "472", 12, "#e2e8f0", weight="bold"))
    parts.append(text(380, cy - 4, "Surface-mount chip (thick or thin film)", 15, AMBER_LIGHT, "start", "bold"))
    parts.append(text(380, cy + 16, "a film printed on a ceramic chip; marked with a short code (472 = 4.7 kΩ)", 12, TEXT, "start"))
    parts.append(text(w / 2, h - 30, "dashed windows: the body cut open", 11, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Five kinds of fixed resistor, each with a window cut into its body: carbon composition, a solid slug of carbon and binder; carbon film, a spiral-cut carbon film on a ceramic rod; metal film, a finer spiral in a metal film; wire-wound, resistance wire wound on a ceramic core; and a surface-mount chip marked 472, meaning 4.7 kilohms.")


# 2. Temperature coefficient ------------------------------------------------------------
def tempco():
    w, h = 820, 400
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "A 10 kΩ resistor warmed by 30 °C: how far can its value move?", 16, TEXT, weight="bold"))
    cases = [("Carbon film (CFR-25)", -500, 350, AMBER), ("Metal film (MFR)", -50, 50, GREEN)]
    base, scale = 200, 0.5
    for i, (name, lo, hi, color) in enumerate(cases):
        cx = 230 + i * 360
        dlo, dhi = 10000 * lo * 1e-6 * 30, 10000 * hi * 1e-6 * 30
        parts.append(f'<line x1="{cx - 150}" y1="{base}" x2="{cx + 150}" y2="{base}" stroke="{MUTED}"/>')
        parts.append(f'<rect x="{cx - 26}" y="{base - dhi * scale:.1f}" width="52" height="{(dhi - dlo) * scale:.1f}" rx="6" fill="{color}" fill-opacity="0.75"/>')
        parts.append(f'<rect x="{cx - 26}" y="{base - dhi * scale:.1f}" width="52" height="{(dhi - dlo) * scale:.1f}" rx="6" fill="url(#gloss)"/>')
        parts.append(text(cx + 40, base - dhi * scale + 5, f"+{dhi:.0f} Ω", 13, TEXT, "start", "bold"))
        parts.append(text(cx + 40, base - dlo * scale + 5, f"{dlo:.0f} Ω", 13, TEXT, "start", "bold"))
        parts.append(text(cx - 150, base - 6, "10 kΩ", 12, MUTED, "start"))
        parts.append(text(cx, 345, name, 15, AMBER_LIGHT if i == 0 else "#9ae6b4", weight="bold"))
        parts.append(text(cx, 366, f"{lo:+d} to {hi:+d} ppm/°C", 13, TEXT))
    parts.append(text(w / 2, 390, "ppm/°C: parts per million of the value, per degree. 350 ppm/°C × 30 °C = 10,500 ppm ≈ 1%", 11, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Two bars showing how far a 10 kilohm resistor's value can move when warmed by 30 degrees. A carbon film resistor rated minus 500 to plus 350 parts per million per degree can move from minus 150 to plus 105 ohms. A metal film resistor rated plus or minus 50 can move only 15 ohms either way.")


# 3. Inside a potentiometer -------------------------------------------------------------
def potentiometer():
    w, h = 820, 440
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "A potentiometer: a resistive track and a sliding wiper", 16, TEXT, weight="bold"))
    cx, cy, r = 260, 230, 110
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r + 30}" fill="#2d3748"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r + 30}" fill="url(#gloss)" opacity="0.4"/>')
    a0, a1, wa = math.radians(135), math.radians(405), math.radians(250)
    def arc(a_from, a_to, color, width):
        x1, y1 = cx + r * math.cos(a_from), cy + r * math.sin(a_from)
        x2, y2 = cx + r * math.cos(a_to), cy + r * math.sin(a_to)
        large = 1 if (a_to - a_from) > math.pi else 0
        return f'<path d="M{x1:.1f},{y1:.1f} A{r},{r} 0 {large} 1 {x2:.1f},{y2:.1f}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'
    parts.append(arc(a0, wa, AMBER, 18))
    parts.append(arc(wa, a1, "#3182ce", 18))
    wx, wy = cx + r * math.cos(wa), cy + r * math.sin(wa)
    parts.append(f'<line x1="{cx}" y1="{cy}" x2="{wx:.1f}" y2="{wy:.1f}" stroke="#e2e8f0" stroke-width="7" stroke-linecap="round"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="18" fill="url(#core)"/>')
    parts.append(f'<circle cx="{wx:.1f}" cy="{wy:.1f}" r="9" fill="url(#vball)"/>')
    for a, lab in ((a0, "1"), (a1, "3")):
        tx, ty = cx + (r + 52) * math.cos(a), cy + (r + 52) * math.sin(a)
        parts.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="12" fill="#cbd5e0"/>')
        parts.append(text(tx, ty + 5, lab, 13, "#1a1a1a", weight="bold"))
    parts.append(f'<circle cx="{cx}" cy="{cy + r + 52}" r="12" fill="#cbd5e0"/>')
    parts.append(text(cx, cy + r + 57, "2", 13, "#1a1a1a", weight="bold"))
    parts.append(text(cx, cy + r + 82, "wiper", 12, MUTED, italic=True))
    parts.append(text(560, 150, "Terminals 1 and 3: the two ends of the track", 13, TEXT, "start"))
    parts.append(text(560, 170, "(the full, fixed resistance)", 12, MUTED, "start", italic=True))
    parts.append(text(560, 220, "Terminal 2: the wiper, which slides along it", 13, TEXT, "start"))
    parts.append(f'<rect x="560" y="255" width="16" height="10" fill="{AMBER}"/>')
    parts.append(text(584, 265, "track from 1 to the wiper", 12, AMBER_LIGHT, "start"))
    parts.append(f'<rect x="560" y="280" width="16" height="10" fill="#3182ce"/>')
    parts.append(text(584, 290, "track from the wiper to 3", 12, "#90cdf4", "start"))
    parts.append(text(560, 330, "Turn the shaft: one share grows,", 13, TEXT, "start"))
    parts.append(text(560, 350, "the other shrinks, the total stays put", 13, TEXT, "start"))
    return svg(w, h, "\n".join(parts), "Inside a rotary potentiometer: a curved resistive track between terminals 1 and 3, and a wiper, terminal 2, that sweeps along it as the shaft turns, splitting the track into two parts whose total stays constant.")


# 4. Kinds of variable resistor ----------------------------------------------------------
def variable_types():
    w, h = 880, 360
    parts = [common_defs(cyl_gradient("shaft", "#cbd5e0", vertical=True))]
    cards = [("Rotary pot", "a panel knob: volume, tuning"), ("Slide pot", "a straight track: faders"),
             ("Trimmer", "set once with a screwdriver"), ("Wire-wound pot", "resistance wire track: high power")]
    for i, (name, use) in enumerate(cards):
        cx = 115 + i * 215
        parts.append(panel(cx - 100, 20, 200, 320))
        cy = 150
        if i == 0:
            parts.append(f'<circle cx="{cx}" cy="{cy + 20}" r="46" fill="#2d3748"/>')
            parts.append(f'<rect x="{cx - 9}" y="{cy - 70}" width="18" height="70" fill="url(#shaft)"/>')
            parts.append(f'<rect x="{cx - 14}" y="{cy - 20}" width="28" height="22" rx="3" fill="#a0aec0"/>')
            for dx in (-24, 0, 24):
                parts.append(f'<rect x="{cx + dx - 3}" y="{cy + 60}" width="6" height="34" fill="#cbd5e0"/>')
        elif i == 1:
            parts += box3d(cx - 80, cy + 40, 160, 24, 22, "#2d3748", shadow=True)
            parts.append(f'<rect x="{cx - 60}" y="{cy + 8}" width="120" height="4" fill="#1a1a1a"/>')
            parts += box3d(cx - 10, cy + 18, 20, 14, 34, "#a0aec0", shadow=False)
        elif i == 2:
            parts += box3d(cx - 30, cy + 40, 60, 30, 40, "#3182ce", shadow=True)
            parts.append(f'<circle cx="{cx + 10}" cy="{cy - 6}" r="17" fill="#e2e8f0"/>')
            parts.append(f'<line x1="{cx - 2}" y1="{cy - 14}" x2="{cx + 22}" y2="{cy + 2}" stroke="#2d3748" stroke-width="4"/>')
        else:
            parts.append(f'<circle cx="{cx}" cy="{cy + 10}" r="56" fill="#e2e8f0" fill-opacity="0.85"/>')
            for k in range(36):
                a = math.radians(135 + k * 7.5)
                x1, y1 = cx + 40 * math.cos(a), cy + 10 + 40 * math.sin(a)
                x2, y2 = cx + 52 * math.cos(a), cy + 10 + 52 * math.sin(a)
                parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#b8673a" stroke-width="2.5"/>')
            parts.append(f'<circle cx="{cx}" cy="{cy + 10}" r="14" fill="url(#core)"/>')
        parts.append(text(cx, 268, name, 16, AMBER_LIGHT, weight="bold"))
        parts.append(text(cx, 292, use, 12, TEXT))
    return svg(w, h, "\n".join(parts), "Four kinds of variable resistor: a rotary potentiometer with a knob shaft, a slide potentiometer with a straight track, a small trimmer adjusted with a screwdriver, and a wire-wound potentiometer whose track is visible turns of resistance wire.")


# 5. Tapers ------------------------------------------------------------------------
def tapers():
    w, h = 760, 420
    L, R, T, B = 100, 600, 70, 350
    X = lambda f: L + (R - L) * f
    Y = lambda f: B - (B - T) * f
    parts = [common_defs(), panel(L - 10, T - 10, R - L + 20, B - T + 20)]
    for f in (0.25, 0.5, 0.75):
        parts.append(f'<line x1="{X(f):.1f}" y1="{T}" x2="{X(f):.1f}" y2="{B}" stroke="#4a5568" stroke-opacity="0.35"/>')
        parts.append(f'<line x1="{L}" y1="{Y(f):.1f}" x2="{R}" y2="{Y(f):.1f}" stroke="#4a5568" stroke-opacity="0.35"/>')
    lin = " ".join(f"{X(k / 100):.1f},{Y(k / 100):.1f}" for k in range(101))
    # log taper: 10% of resistance at half rotation, exponential shape
    b = 2 * math.log(9)  # gives 0.1 at f=0.5
    aud = " ".join(f"{X(k / 100):.1f},{Y((math.exp(b * k / 100) - 1) / (math.exp(b) - 1)):.1f}" for k in range(101))
    parts.append(f'<polyline points="{lin}" fill="none" stroke="{AMBER}" stroke-width="3.5" filter="url(#softglow)"/>')
    parts.append(f'<polyline points="{aud}" fill="none" stroke="#90cdf4" stroke-width="3.5" filter="url(#softglow)"/>')
    parts.append(text(X(0.32), Y(0.45), "linear: half-way turned, half the resistance", 13, AMBER_LIGHT, "start", "bold"))
    parts.append(text(X(0.42), Y(0.03), "log (audio): about a tenth at half-way", 13, "#90cdf4", "start", "bold"))
    for f, lab in ((0, "0%"), (0.5, "50%"), (1, "100%")):
        parts.append(text(X(f), B + 22, lab, 12, MUTED))
        parts.append(text(L - 10, Y(f) + 4, lab, 12, MUTED, "end"))
    parts.append(text((L + R) / 2, B + 48, "how far the shaft is turned", 13))
    parts.append(f'<text x="34" y="{(T + B) / 2}" font-size="13" fill="{TEXT}" text-anchor="middle" transform="rotate(-90 34 {(T + B) / 2})" font-family="IBM Plex Sans, sans-serif">resistance, end to wiper</text>')
    parts.append(text(R + 20, B - 30, "a typical log curve;", 11, MUTED, "start", italic=True))
    parts.append(text(R + 20, B - 14, "makers vary", 11, MUTED, "start", italic=True))
    return svg(w, h, "\n".join(parts), "Resistance from one end to the wiper against shaft rotation, for two potentiometer tapers. A linear taper is a straight line: half-way turned gives half the resistance. A logarithmic, or audio, taper curves up slowly, giving about a tenth of the resistance at half-way, then rises steeply.")


# 6. A tapped resistor ----------------------------------------------------------------
def tapped():
    w, h = 820, 330
    grads = cyl_gradient("ceramic", "#e2e8f0")
    parts = [common_defs(grads), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "A tapped resistor: fixed connection points partway along", 16, TEXT, weight="bold"))
    x, cy, L, r = 140, 160, 520, 36
    parts.append(f'<ellipse cx="{x + L / 2}" cy="{cy + r + 12}" rx="{L / 2 + 10}" ry="8" fill="#000" fill-opacity="0.4"/>')
    parts.append(f'<rect x="{x}" y="{cy - r}" width="{L}" height="{2 * r}" rx="10" fill="url(#ceramic)"/>')
    for k in range(60):
        xx = x + 14 + k * 8.4
        parts.append(f'<line x1="{xx:.1f}" y1="{cy - r + 4}" x2="{xx + 4:.1f}" y2="{cy + r - 4}" stroke="#b8673a" stroke-width="2.5"/>')
    taps = [(x + 6, "end"), (x + L * 0.3, "tap"), (x + L * 0.65, "tap"), (x + L - 6, "end")]
    for tx, kind in taps:
        parts.append(f'<rect x="{tx - 8}" y="{cy - r - 30}" width="16" height="34" rx="3" fill="#a0aec0"/>')
        parts.append(f'<circle cx="{tx}" cy="{cy - r - 20}" r="5" fill="#1a202c"/>')
        parts.append(text(tx, cy - r - 40, kind, 12, AMBER_LIGHT if kind == "tap" else TEXT, weight="bold"))
    parts.append(text(x + L * 0.15, cy + r + 40, "30%", 13, TEXT, weight="bold"))
    parts.append(text(x + L * 0.475, cy + r + 40, "35%", 13, TEXT, weight="bold"))
    parts.append(text(x + L * 0.825, cy + r + 40, "35%", 13, TEXT, weight="bold"))
    parts.append(text(w / 2, 282, "like a potentiometer whose wiper is fixed in place: each tap gives a set fraction of the voltage", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "A long wire-wound power resistor on a ceramic tube, with a terminal at each end and two taps partway along, dividing it into sections of 30, 35 and 35 percent.")


FIGURES = {
    "fixed_family.svg": fixed_family,
    "tempco.svg": tempco,
    "potentiometer.svg": potentiometer,
    "variable_types.svg": variable_types,
    "tapers.svg": tapers,
    "tapped.svg": tapped,
}

if __name__ == "__main__":
    for name, lo, hi in (("carbon film", -500, 350), ("metal film", -50, 50)):
        print(f"{name}: 10k over 30C -> {10000 * lo * 1e-6 * 30:+.0f} to {10000 * hi * 1e-6 * 30:+.0f} ohm")
    render_all(FIGURES, OUT)
