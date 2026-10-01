#!/usr/bin/env python3
"""Figures for docs/open_short_fuses.md.

Sources:
- Energizer E91 AA datasheet: nominal internal resistance 150-300 mOhm (fresh),
  so a dead short draws roughly 1.5 / 0.3 = 5 A to 1.5 / 0.15 = 10 A.
- Littelfuse Fuseology Design Guide: the voltage rating is the voltage at which
  the fuse can safely interrupt its rated short-circuit current; an arc forms
  just before the element opens; standard small-fuse voltage ratings 32, 63,
  125, 250, 600 V; derate the current rating 25% (a 10 A fuse should normally
  carry no more than 7.5 A at 25 C); speed classes very fast-acting,
  fast-acting, and Slo-Blo (time-lag).

Usage:
    python3 illustrations/open_short_fuses.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, common_defs,  # noqa: E402
                     cyl_gradient, panel, pill, render_all, shade, svg, text)
from voltage import multimeter, probe_lead  # noqa: E402
from what_is_electricity import wire  # noqa: E402

OUT = HERE.parent / "docs" / "images" / "open_short_fuses"
IR_LO, IR_HI = 0.150, 0.300


def battery(cx, cy, h=64):
    return [f'<rect x="{cx - 20}" y="{cy - h / 2}" width="40" height="{h}" rx="5" fill="url(#battx)"/>',
            f'<rect x="{cx - 7}" y="{cy - h / 2 - 8}" width="14" height="8" rx="2" fill="#cbd5e0"/>',
            text(cx, cy + 6, "+", 18, "#1a1a1a", weight="bold")]


def lamp(cx, cy, lit):
    out = []
    if lit:
        out += [f'<circle cx="{cx}" cy="{cy}" r="44" fill="#fefcbf" fill-opacity="0.18"/>',
                f'<circle cx="{cx}" cy="{cy}" r="28" fill="#fefcbf" fill-opacity="0.3"/>']
    out += [f'<circle cx="{cx}" cy="{cy}" r="18" fill="{"#fefcbf" if lit else "#4a5568"}" fill-opacity="{0.9 if lit else 0.6}" stroke="#e2e8f0" stroke-opacity="0.6"/>',
            f'<path d="M{cx - 8},{cy + 2} q4,-8 8,0 t8,0" fill="none" stroke="{"#d69e2e" if lit else "#a0aec0"}" stroke-width="2"/>']
    return out


# 1. Closed, open, short ---------------------------------------------------------------
def three_circuits():
    w, h = 860, 400
    parts = [common_defs(cyl_gradient("battx", AMBER, vertical=True))]
    titles = [("Closed circuit", "a complete loop: current flows", GREEN),
              ("Open circuit", "a break anywhere: nothing flows", MUTED),
              ("Short circuit", "a path that skips the load", RED)]
    for i, (t1, t2, c) in enumerate(titles):
        ox = 25 + i * 280
        parts.append(panel(ox, 15, 260, 370))
        parts.append(text(ox + 130, 48, t1, 16, c if i != 1 else TEXT, weight="bold"))
        parts.append(text(ox + 130, 68, t2, 12, MUTED, italic=True))
        L, R, T, B = ox + 45, ox + 215, 110, 300
        if i == 1:
            parts += wire([(L, 175), (L, T), (ox + 110, T)]) + wire([(ox + 150, T), (R, T), (R, B), (L, B), (L, 240)])
            parts.append(f'<path d="M{ox + 110},{T} l14,-18" stroke="#b8673a" stroke-width="7" stroke-linecap="round"/>')
            parts.append(text(ox + 130, T - 26, "break", 12, "#fc8181", italic=True))
        else:
            parts += wire([(L, 175), (L, T), (R, T), (R, B), (L, B), (L, 240)])
        parts += battery(L, 208)
        parts += lamp(R, 205, lit=(i == 0))
        if i == 2:
            parts.append(f'<path d="M{R},{T + 30} C{R - 70},{T + 60} {R - 70},{B - 60} {R},{B - 30}" fill="none" stroke="#fc8181" stroke-opacity="0.35" stroke-width="16"/>')
            parts += wire([(R, T + 30), (R - 50, T + 45), (R - 50, B - 45), (R, B - 30)], 7)
            parts.append(f'<path d="M{R},{T + 30} L{R - 50},{T + 45} L{R - 50},{B - 45} L{R},{B - 30}" fill="none" stroke="#fc8181" stroke-width="3" stroke-opacity="0.7"/>')
            parts.append(text(R - 60, 205, "short", 12, "#fc8181", "end", "bold"))
            parts.append(f'<circle cx="{L}" cy="208" r="36" fill="#fc8181" fill-opacity="0.18"/>')
        status = ["lamp lit", "lamp dark", "lamp dark, wire and battery heat up"][i]
        parts.append(text(ox + 130, 345, status, 13, TEXT, weight="bold"))
    return svg(w, h, "\n".join(parts), "Three battery-and-lamp circuits. Closed: a complete loop and the lamp is lit. Open: a break in the top wire and the lamp is dark. Short: a wire connects across the lamp, so current bypasses it; the lamp is dark while the short wire glows hot.")


# 2. What limits a short: internal resistance -----------------------------------------------
def internal_resistance():
    w, h = 800, 400
    grads = cyl_gradient("cellv", AMBER, vertical=True) + cyl_gradient("resbody", "#d9b382")
    parts = [common_defs(grads), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "A dead short isn't infinite current: the cell's own resistance limits it", 15, TEXT, weight="bold"))
    cx, top, bot = 200, 100, 320
    parts.append(f'<rect x="{cx - 60}" y="{top}" width="120" height="{bot - top}" rx="14" fill="url(#cellv)" opacity="0.35"/>')
    parts.append(f'<rect x="{cx - 60}" y="{top}" width="120" height="{bot - top}" rx="14" fill="none" stroke="{AMBER}" stroke-width="2"/>')
    parts.append(f'<rect x="{cx - 14}" y="{top - 14}" width="28" height="14" rx="3" fill="#cbd5e0"/>')
    parts.append(text(cx, 140, "ideal 1.5 V", 13, "#ffffff", weight="bold"))
    parts.append(text(cx, 156, "source", 13, "#ffffff", weight="bold"))
    parts.append(f'<rect x="{cx - 46}" y="225" width="92" height="28" rx="14" fill="url(#resbody)"/>')
    parts.append(text(cx, 278, "internal", 12, "#ffffff", weight="bold"))
    parts.append(text(cx, 294, "resistance", 12, "#ffffff", weight="bold"))
    parts.append(text(cx, 345, "an AA cell, opened up (in principle)", 12, MUTED, italic=True))
    parts += wire([(cx, top - 14), (cx, 70), (360, 70), (360, 360), (cx, 360), (cx, bot)], 7)
    parts.append(text(372, 214, "a wire straight", 12, "#fc8181", "start", italic=True))
    parts.append(text(372, 230, "across the cell", 12, "#fc8181", "start", italic=True))
    parts.append(f'<rect x="490" y="120" width="270" height="170" rx="12" fill="#1a1d23" stroke="#9ae6b4" stroke-opacity="0.5"/>')
    parts.append(text(625, 152, "Energizer AA datasheet:", 13, MUTED))
    parts.append(text(625, 174, f"{IR_LO * 1000:.0f} to {IR_HI * 1000:.0f} mΩ internal", 14, TEXT, weight="bold"))
    parts.append(text(625, 210, f"I = 1.5 V ÷ {IR_HI:.2f} Ω = {1.5 / IR_HI:.0f} A", 15, "#9ae6b4", weight="bold"))
    parts.append(text(625, 234, f"I = 1.5 V ÷ {IR_LO:.2f} Ω = {1.5 / IR_LO:.0f} A", 15, "#9ae6b4", weight="bold"))
    parts.append(text(625, 268, "enough to make the wire and cell hot", 12, "#fc8181", italic=True))
    return svg(w, h, "\n".join(parts), f"An AA cell drawn as an ideal 1.5 volt source in series with its own internal resistance, shorted by a wire. With the datasheet's 150 to 300 milliohms of internal resistance, the short-circuit current is {1.5 / IR_HI:.0f} to {1.5 / IR_LO:.0f} amps.")


# 3. Fuse anatomy -----------------------------------------------------------------------
def fuse_anatomy():
    w, h = 800, 420
    glass = ('<linearGradient id="glassf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2e8f0" stop-opacity="0.45"/>'
             '<stop offset="0.35" stop-color="#e2e8f0" stop-opacity="0.08"/><stop offset="0.85" stop-color="#1a202c" stop-opacity="0.2"/>'
             '<stop offset="1" stop-color="#e2e8f0" stop-opacity="0.35"/></linearGradient>')
    parts = [common_defs(glass + cyl_gradient("cap", "#cbd5e0") + cyl_gradient("blade", "#3182ce")), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "A fuse is a deliberate weak link, and it carries three ratings", 16, TEXT, weight="bold"))
    x0, y0, L, r = 120, 150, 340, 30
    parts.append(f'<ellipse cx="{x0 + L / 2}" cy="{y0 + r + 14}" rx="{L / 2 + 20}" ry="7" fill="#000" fill-opacity="0.4"/>')
    parts.append(f'<path d="M{x0 + 50},{y0} q24,-14 48,0 t48,0 t48,0 t48,0 t48,0" fill="none" stroke="#cbd5e0" stroke-width="2.5"/>')
    parts.append(f'<rect x="{x0 + 40}" y="{y0 - r}" width="{L - 80}" height="{2 * r}" fill="url(#glassf)"/>')
    for ex in (x0, x0 + L - 50):
        parts.append(f'<rect x="{ex}" y="{y0 - r - 3}" width="50" height="{2 * r + 6}" rx="6" fill="url(#cap)"/>')
    parts.append(text(x0 + L / 2, y0 + 64, "thin metal element inside a glass tube", 12, MUTED, italic=True))
    labels = [("Current rating", "the current it carries without melting;", "run it at no more than about 75% of this"),
              ("Voltage rating", "the highest voltage it can safely break:", "32, 63, 125, 250, 600 V are standard"),
              ("Speed", "very fast-acting, fast-acting, or slow-blow", "(slow-blow rides through switch-on surges)")]
    for i, (t, a, b) in enumerate(labels):
        y = 250 + i * 50
        parts += pill(150, y, t, "#d97706" if i == 1 else "#2d3748", "#1a1a1a" if i == 1 else "#fff", wpx=170, size=13, h=30)
        parts.append(text(250, y - 2, a, 12, TEXT, "start"))
        parts.append(text(250, y + 14, b, 12, MUTED, "start", italic=True))
    # blade fuse
    bx, by = 600, 120
    parts.append(f'<rect x="{bx}" y="{by}" width="90" height="70" rx="10" fill="url(#blade)" opacity="0.9"/>')
    parts.append(text(bx + 45, by + 44, "15", 22, "#ffffff", weight="bold"))
    for lx in (bx + 14, bx + 58):
        parts.append(f'<rect x="{lx}" y="{by + 70}" width="18" height="44" fill="url(#cap)"/>')
    parts.append(text(bx + 45, by + 140, "car blade fuse:", 12, TEXT, weight="bold"))
    parts.append(text(bx + 45, by + 156, "rated 32 V", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "A glass cartridge fuse with a thin wavy metal element between two end caps, labelled with its three ratings: current, voltage, and speed. Beside it, a blue 15 amp car blade fuse, rated 32 volts.")


# 4. How a fuse opens ---------------------------------------------------------------------
def fuse_opening():
    w, h = 820, 360
    glass = ('<linearGradient id="glassf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2e8f0" stop-opacity="0.45"/>'
             '<stop offset="0.35" stop-color="#e2e8f0" stop-opacity="0.08"/><stop offset="1" stop-color="#e2e8f0" stop-opacity="0.3"/></linearGradient>')
    parts = [common_defs(glass + cyl_gradient("cap", "#cbd5e0"))]
    stages = [("Normal", "element cool, current flows", "#cbd5e0", None),
              ("Overload", "element heats and glows", "#fc8181", "glow"),
              ("Melting", "a gap opens; an arc tries to bridge it", "#fc8181", "arc"),
              ("Open", "the arc dies; the circuit is broken", "#4a5568", "gap")]
    for i, (t, sub, color, state) in enumerate(stages):
        ox = 25 + i * 200
        parts.append(panel(ox, 15, 185, 330))
        parts.append(text(ox + 92, 48, t, 16, AMBER_LIGHT if i == 2 else TEXT, weight="bold"))
        cy, x1, x2 = 170, ox + 30, ox + 155
        if state == "glow":
            parts.append(f'<rect x="{x1 + 20}" y="{cy - 22}" width="{x2 - x1 - 40}" height="44" rx="22" fill="#fc8181" fill-opacity="0.25"/>')
        if state in ("arc", "gap"):
            parts.append(f'<line x1="{x1 + 26}" y1="{cy}" x2="{ox + 82}" y2="{cy}" stroke="{color}" stroke-width="3"/>')
            parts.append(f'<line x1="{ox + 104}" y1="{cy}" x2="{x2 - 26}" y2="{cy}" stroke="{color}" stroke-width="3"/>')
            if state == "arc":
                parts.append(f'<circle cx="{ox + 93}" cy="{cy}" r="22" fill="url(#glow)"/>')
                parts.append(f'<path d="M{ox + 82},{cy} l5,-8 l4,12 l5,-10 l5,9" fill="none" stroke="#fefcbf" stroke-width="3"/>')
        else:
            parts.append(f'<line x1="{x1 + 26}" y1="{cy}" x2="{x2 - 26}" y2="{cy}" stroke="{color}" stroke-width="{4 if state else 3}"/>')
        parts.append(f'<rect x="{x1 + 20}" y="{cy - 26}" width="{x2 - x1 - 40}" height="52" fill="url(#glassf)"/>')
        for ex in (x1, x2 - 26):
            parts.append(f'<rect x="{ex}" y="{cy - 28}" width="26" height="56" rx="5" fill="url(#cap)"/>')
        parts.append(text(ox + 92, 250, sub.split(";")[0], 12, TEXT))
        if ";" in sub:
            parts.append(text(ox + 92, 268, sub.split(";")[1].strip(), 12, TEXT))
    parts.append(text(w / 2, 330, "the voltage rating is about stage 3: below its rated voltage, the fuse is guaranteed to put the arc out", 12, AMBER_LIGHT, italic=True))
    return svg(w, h, "\n".join(parts), "Four stages of a fuse blowing: normal, with a cool element; overload, with the element glowing; melting, where a gap opens and an arc jumps across it; and open, where the arc has died and the circuit is broken.")


# 5. Continuity -------------------------------------------------------------------------
def continuity():
    w, h = 800, 420
    parts = [common_defs(), panel(15, 15, 375, h - 30), panel(410, 15, 375, h - 30)]
    for i, (t, reading, broken) in enumerate((("Continuity: a closed path", "0.3 Ω", False), ("No continuity: open", "OL", True))):
        ox = 15 + i * 395
        cx = ox + 187
        parts.append(text(cx, 48, t, 16, GREEN if not broken else "#fc8181", weight="bold"))
        if broken:
            parts += wire([(ox + 40, 120), (cx - 10, 120)], 8) + wire([(cx + 14, 120), (ox + 335, 120)], 8)
            parts.append(text(cx + 2, 100, "broken inside", 11, "#fc8181", italic=True))
        else:
            parts += wire([(ox + 40, 120), (ox + 335, 120)], 8)
        parts += multimeter(cx - 60, 220, reading, mode="·))")
        parts += probe_lead(cx - 26, 356, ox + 60, 120 - 4, "#e53e3e") + probe_lead(cx + 26, 356, ox + 315, 120 - 4, "#111")
        if not broken:
            for k in range(3):
                parts.append(f'<path d="M{cx + 70 + k * 10},{246 - k * 4} q8,14 0,28" fill="none" stroke="{AMBER_LIGHT}" stroke-width="2.5" opacity="{1 - k * 0.25}"/>')
            parts.append(text(cx + 100, 236, "beep", 12, AMBER_LIGHT, "start", "bold"))
        parts.append(text(cx, 398, "a few tenths of an ohm: the meter beeps" if not broken else "OL: over limit, an open circuit", 12, TEXT))
    return svg(w, h, "\n".join(parts), "Two continuity tests. Left: probes on the ends of an intact wire, the meter reads 0.3 ohms and beeps. Right: the same test on a wire broken inside, the meter reads OL, meaning over limit, an open circuit.")


FIGURES = {
    "three_circuits.svg": three_circuits,
    "internal_resistance.svg": internal_resistance,
    "fuse_anatomy.svg": fuse_anatomy,
    "fuse_opening.svg": fuse_opening,
    "continuity.svg": continuity,
}

if __name__ == "__main__":
    print(f"AA short-circuit current {1.5 / IR_HI:.0f}-{1.5 / IR_LO:.0f} A")
    render_all(FIGURES, OUT)
