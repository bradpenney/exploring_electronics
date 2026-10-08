#!/usr/bin/env python3
"""Figures for docs/tools/soldering.md.

Sources:
- Wikipedia "Solder": Sn63/Pb37 eutectic melts at 183 C; Sn60/Pb40 melts at
  188 C with a plastic range; SAC (tin-silver-copper) lead-free 217 C.
- Wikipedia "Soldering": cold joints never pass the liquidus, look dull,
  cracked or pock-marked; a concave fillet with a low contact angle shows good
  wetting; lead-free joints cool dull even when good; the iron heats the parts
  and the parts melt the solder; trim leads to about the pad's radius.
- Hakko FX-888D manual: 200-480 C range, +/-1 C stability, default 399 C
  (750 F); tip maintenance at 250 C.
- HSE INDG249: rosin flux fume levels can triple between 250 and 400 C.

Usage:
    python3 illustrations/soldering.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, box3d,  # noqa: E402
                     common_defs, panel, pill, render_all, shade, svg, text)

OUT = HERE.parent / "docs" / "images" / "soldering"
BLUE = "#4299e1"
SOLDER = ('<linearGradient id="sd-solder" x1="0" y1="0" x2="1" y2="1">'
          '<stop offset="0" stop-color="#f7fafc"/><stop offset="0.5" stop-color="#a0aec0"/>'
          '<stop offset="1" stop-color="#4a5568"/></linearGradient>'
          '<linearGradient id="sd-dull" x1="0" y1="0" x2="1" y2="1">'
          '<stop offset="0" stop-color="#a0aec0"/><stop offset="1" stop-color="#4a5568"/></linearGradient>'
          '<linearGradient id="sd-lead" x1="0" y1="0" x2="1" y2="0">'
          '<stop offset="0" stop-color="#4a5568"/><stop offset="0.4" stop-color="#e2e8f0"/>'
          '<stop offset="1" stop-color="#4a5568"/></linearGradient>')


def _board(parts, cx, y, pad=True):
    """Cross-section of a board with a plated hole and a component lead."""
    parts.append(f'<rect x="{cx - 70}" y="{y}" width="140" height="22" fill="#2f855a"/>')
    parts.append(f'<rect x="{cx - 70}" y="{y}" width="140" height="22" fill="url(#gloss)" opacity="0.3"/>')
    if pad:
        parts.append(f'<rect x="{cx - 38}" y="{y - 5}" width="76" height="6" fill="#c8733c"/>')
    parts.append(f'<rect x="{cx - 6}" y="{y - 70}" width="12" height="105" rx="3" fill="url(#sd-lead)"/>')


# 1. Good and bad joints ---------------------------------------------------------------------------
def joints():
    w, h = 900, 310
    parts = [common_defs(SOLDER)]
    cases = [("Good", "concave fillet, low angle", GREEN),
             ("Cold", "a ball that never bonded", RED),
             ("Too much", "bulging: can hide a cold joint", AMBER),
             ("Too little", "pad not covered", AMBER),
             ("Bridge", "solder joins two pads", RED)]
    for k, (name, sub, col) in enumerate(cases):
        x0 = 15 + k * 176
        cx = x0 + 84
        parts.append(panel(x0, 15, 168, h - 30))
        parts.append(text(cx, 44, name, 15, shade(col, 0.2), weight="bold"))
        y = 190
        if name == "Bridge":
            for dx in (-40, 40):
                parts.append(f'<rect x="{cx + dx - 22}" y="{y - 5}" width="44" height="6" fill="#c8733c"/>')
                parts.append(f'<rect x="{cx + dx - 5}" y="{y - 60}" width="10" height="95" rx="3" fill="url(#sd-lead)"/>')
            parts.append(f'<rect x="{cx - 70}" y="{y}" width="140" height="22" fill="#2f855a"/>')
            parts.append(f'<path d="M{cx - 62},{y - 4} Q{cx - 40},{y - 40} {cx - 20},{y - 18} Q{cx},{y - 6} {cx + 20},{y - 18} Q{cx + 40},{y - 40} {cx + 62},{y - 4} Z" fill="url(#sd-solder)"/>')
        else:
            _board(parts, cx, y)
            if name == "Good":
                parts.append(f'<path d="M{cx - 38},{y - 5} Q{cx - 10},{y - 10} {cx - 6},{y - 42} L{cx + 6},{y - 42} Q{cx + 10},{y - 10} {cx + 38},{y - 5} Z" fill="url(#sd-solder)"/>')
            elif name == "Cold":
                parts.append(f'<ellipse cx="{cx}" cy="{y - 30}" rx="24" ry="18" fill="url(#sd-dull)"/>')
                parts.append(f'<path d="M{cx - 10},{y - 40} l8,10 l-4,6" stroke="#2d3748" stroke-width="2" fill="none"/>')
                parts.append(f'<line x1="{cx - 30}" y1="{y - 8}" x2="{cx + 30}" y2="{y - 8}" stroke="#1a202c" stroke-width="3" stroke-dasharray="3 3"/>')
            elif name == "Too much":
                parts.append(f'<path d="M{cx - 38},{y - 5} C{cx - 60},{y - 50} {cx - 20},{y - 75} {cx},{y - 72} C{cx + 20},{y - 75} {cx + 60},{y - 50} {cx + 38},{y - 5} Z" fill="url(#sd-solder)"/>')
            else:
                parts.append(f'<path d="M{cx - 14},{y - 5} Q{cx - 8},{y - 8} {cx - 6},{y - 18} L{cx + 6},{y - 18} Q{cx + 8},{y - 8} {cx + 14},{y - 5} Z" fill="url(#sd-solder)"/>')
        for j, line in enumerate(sub.split(": ")):
            parts.append(text(cx, 258 + j * 15, line, 11, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Five cross-sections of a component lead soldered to a copper pad on a green board. Good: a shiny concave fillet that meets the pad at a low angle. Cold: a dull, cracked ball sitting on the pad with a gap under it, never bonded. Too much: a bulging blob, which can hide a cold joint. Too little: solder covering only part of the pad. Bridge: solder running across from one pad to the next.")


# 2. Heat the parts, not the solder --------------------------------------------------------------------
def heat_path():
    w, h = 900, 420
    parts = [common_defs(SOLDER), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Heat the pad and the lead together; feed solder to them, not to the iron", 16, AMBER_LIGHT, weight="bold"))
    cx, y = 450, 300
    parts.append(f'<rect x="{cx - 200}" y="{y}" width="400" height="30" fill="#2f855a"/>')
    parts.append(f'<rect x="{cx - 60}" y="{y - 7}" width="120" height="8" fill="#c8733c"/>')
    parts.append(f'<rect x="{cx - 7}" y="{y - 160}" width="14" height="210" rx="3" fill="url(#sd-lead)"/>')
    # iron from the left, touching pad and lead at the corner
    parts.append(f'<ellipse cx="{cx - 30}" cy="{y - 12}" rx="70" ry="40" fill="url(#glow)"/>')
    parts.append(f'<path d="M{cx - 260},{y - 150} L{cx - 22},{y - 16} L{cx - 10},{y - 8} L{cx - 30},{y - 2} L{cx - 280},{y - 132} Z" fill="#a0aec0"/>')
    parts.append(f'<path d="M{cx - 330},{y - 190} L{cx - 260},{y - 150} L{cx - 280},{y - 132} L{cx - 350},{y - 172} Z" fill="#1a202c"/>')
    parts.append(text(cx - 300, y - 200, "iron", 14, TEXT, weight="bold"))
    # solder wire from the right
    parts.append(f'<path d="M{cx + 300},{y - 160} C{cx + 180},{y - 150} {cx + 60},{y - 80} {cx + 14},{y - 14}" stroke="url(#sd-solder)" stroke-width="9" fill="none" stroke-linecap="round"/>')
    parts.append(text(cx + 280, y - 172, "solder", 14, TEXT, weight="bold"))
    parts.append(f'<path d="M{cx - 6},{y - 6} Q{cx + 12},{y - 10} {cx + 50},{y - 7}" stroke="url(#sd-solder)" stroke-width="6" fill="none"/>')
    parts.append(text(cx - 200, y + 60, "1. The iron's tip touches pad and lead at once", 13, TEXT, "start", weight="bold"))
    parts.append(text(cx - 200, y + 80, "2. Solder touches the hot joint on the far side and flows toward the heat", 13, TEXT, "start", weight="bold"))
    return svg(w, h, "\n".join(parts), "A soldering iron's tip, from the left, touches a copper pad and a component lead together, heating both. Solder wire comes in from the right and touches the joint on the far side from the iron, where it melts on the hot metal and flows across the pad toward the heat.")


# 3. A temperature scale ---------------------------------------------------------------------------------
def temperatures():
    w, h = 900, 470
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "The temperatures that matter, from melting to the iron's maximum", 17, AMBER_LIGHT, weight="bold"))
    L, R = 120, 820
    xt = lambda t: L + (t - 150) / (500 - 150) * (R - L)
    y = 250
    parts.append(f'<rect x="{L}" y="{y - 10}" width="{R - L}" height="20" rx="10" fill="#2d3748"/>')
    parts.append(f'<rect x="{xt(200):.1f}" y="{y - 10}" width="{xt(480) - xt(200):.1f}" height="20" rx="10" fill="{AMBER}" fill-opacity="0.35"/>')
    parts.append(text((xt(200) + xt(480)) / 2, y + 40, "Hakko FX-888D setting range: 200 to 480 °C", 12, AMBER_LIGHT, weight="bold"))
    for t in range(150, 501, 50):
        parts.append(text(xt(t), y + 64, f"{t} °C", 11, MUTED))
    marks = [(183, "Sn63/Pb37 melts", GREEN, -1, 0),
             (188, "Sn60/Pb40 fully melted", GREEN, -1, 1),
             (217, "lead-free SAC melts", BLUE, -1, 2),
             (250, "fume level here…", "#fc8181", 1, 0),
             (400, "…can triple by here", "#fc8181", 1, 1),
             (399, "Hakko default setting", AMBER_LIGHT, -1, 3)]
    for t, lab, col, side, row in marks:
        x = xt(t)
        ty = y - 40 - row * 30 if side < 0 else y + 100 + row * 26
        parts.append(f'<line x1="{x:.1f}" y1="{y + (-10 if side < 0 else 10)}" x2="{x:.1f}" y2="{ty + (8 if side < 0 else -14):.1f}" stroke="{col}" stroke-width="1.5"/>')
        parts.append(f'<circle cx="{x:.1f}" cy="{y}" r="6" fill="{col}"/>')
        parts.append(text(x + 6, ty, f"{t} °C: {lab}", 12, col, "start", weight="bold"))
    parts.append(text(w / 2, 440, "fume figure: HSE INDG249, rosin-based flux fume between 250 and 400 °C", 11, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "A temperature scale from 150 to 500 degrees Celsius. Tin-lead Sn63/Pb37 solder melts at 183, Sn60/Pb40 is fully melted at 188, and lead-free SAC solder melts at 217. A Hakko FX-888D iron can be set from 200 to 480, with a default of 399. The UK Health and Safety Executive notes that flux fume levels can triple between 250 and 400 degrees.")


# 4. The five steps ------------------------------------------------------------------------------------------
def steps():
    w, h = 900, 300
    parts = [common_defs(SOLDER)]
    names = [("1. Tin the tip", "a thin coat of fresh solder"),
             ("2. Heat both", "tip on pad and lead together"),
             ("3. Feed solder", "into the joint, opposite the iron"),
             ("4. Solder off, then iron off", "and don't move it while it sets"),
             ("5. Trim the lead", "to about the pad's radius")]
    for k, (name, sub) in enumerate(names):
        x0 = 15 + k * 176
        cx = x0 + 84
        parts.append(panel(x0, 15, 168, h - 30))
        parts.append(text(cx, 44, name, 13, AMBER_LIGHT, weight="bold"))
        y = 200
        if k == 0:
            parts.append(f'<path d="M{cx - 60},{y - 100} L{cx + 10},{y - 30} L{cx + 2},{y - 20} L{cx - 72},{y - 86} Z" fill="#a0aec0"/>')
            parts.append(f'<path d="M{cx - 4},{y - 36} L{cx + 10},{y - 30} L{cx + 2},{y - 20} L{cx - 10},{y - 26} Z" fill="url(#sd-solder)"/>')
        else:
            parts.append(f'<rect x="{cx - 60}" y="{y}" width="120" height="18" fill="#2f855a"/>')
            parts.append(f'<rect x="{cx - 32}" y="{y - 5}" width="64" height="6" fill="#c8733c"/>')
            top = y - (40 if k == 4 else 90)
            parts.append(f'<rect x="{cx - 5}" y="{top}" width="10" height="{y + 40 - top}" rx="3" fill="url(#sd-lead)"/>')
            if k in (1, 2):
                parts.append(f'<ellipse cx="{cx - 14}" cy="{y - 8}" rx="34" ry="20" fill="url(#glow)"/>')
                parts.append(f'<path d="M{cx - 80},{y - 80} L{cx - 8},{y - 10} L{cx - 14},{y - 2} L{cx - 90},{y - 70} Z" fill="#a0aec0"/>')
            if k == 2:
                parts.append(f'<path d="M{cx + 70},{y - 70} L{cx + 10},{y - 10}" stroke="url(#sd-solder)" stroke-width="7" stroke-linecap="round"/>')
            if k >= 3:
                parts.append(f'<path d="M{cx - 32},{y - 5} Q{cx - 8},{y - 8} {cx - 5},{y - 34} L{cx + 5},{y - 34} Q{cx + 8},{y - 8} {cx + 32},{y - 5} Z" fill="url(#sd-solder)"/>')
            if k == 4:
                parts.append(f'<path d="M{cx + 20},{y - 60} l20,-20 M{cx + 20},{y - 80} l20,20" stroke="{MUTED}" stroke-width="3"/>')
        parts.append(text(cx, 262, sub, 11, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Five panels of a through-hole joint being made. 1: tin the tip with a thin coat of fresh solder. 2: heat the pad and the lead together with the tip. 3: feed solder into the joint on the side opposite the iron. 4: take the solder away, then the iron, and don't move the joint while it sets. 5: trim the lead to about the pad's radius.")


FIGURES = {"joints.svg": joints, "heat_path.svg": heat_path, "temperatures.svg": temperatures, "steps.svg": steps}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
