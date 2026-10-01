#!/usr/bin/env python3
"""Figures for docs/magnetism.md.

Sources:
- Wikipedia "Orders of magnitude (magnetic field)": Earth 31 uT (equator) to
  58 uT (50 degrees latitude); refrigerator magnet 1-10 mT; penny-sized
  neodymium magnet ~0.1 T; loudspeaker voice-coil gap 1-2.4 T; MRI 1.5-7 T.
- History: Oersted 1820 (current deflects a compass), Faraday 1831 (induction).
- Transformer: ideal turns-ratio relation Vs / Vp = Ns / Np.

Usage:
    python3 illustrations/magnetism.py
"""

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, box3d,  # noqa: E402
                     common_defs, cyl_gradient, panel, pill, render_all, shade,
                     svg, text)
from what_is_electricity import wire  # noqa: E402

OUT = HERE.parent / "docs" / "images" / "magnetism"
NRED, SBLUE, FIELD = "#e53e3e", "#3182ce", "#90cdf4"


def bar_magnet(x, y, w=180, h=46, flip=False):
    """3D bar magnet, left-bottom-front corner at (x, y); N red, S blue."""
    left, right = (SBLUE, NRED) if flip else (NRED, SBLUE)
    out = box3d(x, y, w / 2, 30, h, left, shadow=True) + box3d(x + w / 2, y, w / 2, 30, h, right, shadow=False)
    out.append(text(x + w / 4, y - h / 2 + 7, "S" if flip else "N", 20, "#ffffff", weight="bold"))
    out.append(text(x + 3 * w / 4, y - h / 2 + 7, "N" if flip else "S", 20, "#ffffff", weight="bold"))
    return out


def arrowhead(x, y, ang, color=FIELD):
    return (f'<path d="M-6,-5 L4,0 L-6,5" fill="none" stroke="{color}" stroke-width="2" '
            f'transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f})"/>')


# 1. A bar magnet's field ----------------------------------------------------------------
def bar_field():
    w, h = 800, 440
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "Field lines leave the north pole and loop round to the south", 16, TEXT, weight="bold"))
    cx, cy = 400, 240
    nx, sx = 330, 470  # pole centres
    for k, spread in enumerate((40, 80, 125, 175)):
        for sign in (-1, 1):
            d = f"M{nx},{cy} C{nx - 60},{cy + sign * spread} {sx + 60},{cy + sign * spread} {sx},{cy}"
            parts.append(f'<path d="{d}" fill="none" stroke="{FIELD}" stroke-opacity="{0.85 - k * 0.15:.2f}" stroke-width="2"/>')
            parts.append(arrowhead(cx, cy + sign * spread * 0.75, 0))
    parts.append(f'<line x1="{nx - 90}" y1="{cy}" x2="{nx - 160}" y2="{cy}" stroke="{FIELD}" stroke-width="2"/>')
    parts.append(arrowhead(nx - 160, cy, 180))
    parts.append(f'<line x1="{sx + 160}" y1="{cy}" x2="{sx + 90}" y2="{cy}" stroke="{FIELD}" stroke-width="2"/>')
    parts.append(arrowhead(sx + 90, cy, 180))
    parts += bar_magnet(cx - 100, cy + 23)
    parts.append(text(cx, 405, "lines never cross · they form closed loops · closer lines mean a stronger field", 12, MUTED, italic=True))
    parts.append(text(120, 120, "strongest near the poles,", 12, AMBER_LIGHT, "start"))
    parts.append(text(120, 136, "where the lines crowd together", 12, AMBER_LIGHT, "start"))
    return svg(w, h, "\n".join(parts), "A 3D bar magnet, north end red and south end blue, with field lines leaving the north pole, curving around both sides, and entering the south pole; the lines crowd together near the poles where the field is strongest.")


# 2. Like repel, unlike attract ------------------------------------------------------------
def poles():
    w, h = 820, 380
    parts = [common_defs(), panel(15, 15, 385, h - 30), panel(420, 15, 385, h - 30)]
    parts.append(text(207, 48, "Unlike poles attract", 16, GREEN, weight="bold"))
    parts += bar_magnet(40, 220, w=140) + bar_magnet(232, 220, w=140)
    for dy in (-30, -15, 0, 15, 30):
        parts.append(f'<line x1="180" y1="{197 + dy}" x2="232" y2="{197 + dy}" stroke="{FIELD}" stroke-width="2"/>')
    parts.append(text(207, 290, "N faces S: lines run straight across", 12, TEXT))
    parts.append(text(207, 310, "and pull the magnets together", 12, TEXT))
    parts.append(text(612, 48, "Like poles repel", 16, "#fc8181", weight="bold"))
    parts += bar_magnet(440, 220, w=140) + bar_magnet(637, 220, w=140, flip=True)
    for sign in (-1, 1):
        for k in range(3):
            off = 10 + k * 14
            parts.append(f'<path d="M580,{197 + sign * 6} C600,{197 + sign * (off + 20)} 600,{197 + sign * (off + 50)} 590,{197 + sign * (off + 70)}" fill="none" stroke="{FIELD}" stroke-width="2"/>')
            parts.append(f'<path d="M637,{197 + sign * 6} C617,{197 + sign * (off + 20)} 617,{197 + sign * (off + 50)} 627,{197 + sign * (off + 70)}" fill="none" stroke="{FIELD}" stroke-width="2"/>')
    parts.append(text(612, 310, "S faces S: lines bend away and push them apart", 12, TEXT))
    return svg(w, h, "\n".join(parts), "Two pairs of bar magnets. Left: a north pole facing a south pole, with field lines running straight across the gap, pulling them together. Right: a south pole facing a south pole, with field lines bending away from each other, pushing them apart.")


# 3. The nail electromagnet --------------------------------------------------------------
def nail_electromagnet():
    w, h = 860, 420
    grads = cyl_gradient("nail", "#a0aec0") + cyl_gradient("battx", AMBER, vertical=True)
    parts = [common_defs(grads), panel(15, 15, 405, h - 30), panel(440, 15, 405, h - 30)]

    def scene(ox, on):
        out = []
        out.append(text(ox + 202, 48, "Switch closed: current flows" if on else "Switch open: no current", 16, AMBER_LIGHT if on else TEXT, weight="bold"))
        nx, ny = ox + 70, 170
        if on:
            out.append(f'<ellipse cx="{nx + 245}" cy="{ny}" rx="60" ry="48" fill="{FIELD}" fill-opacity="0.12"/>')
        out.append(f'<rect x="{nx}" y="{ny - 10}" width="250" height="20" rx="4" fill="url(#nail)"/>')
        out.append(f'<polygon points="{nx + 250},{ny - 10} {nx + 285},{ny} {nx + 250},{ny + 10}" fill="#a0aec0"/>')
        out.append(f'<rect x="{nx - 10}" y="{ny - 20}" width="12" height="40" rx="3" fill="#718096"/>')
        for k in range(14):
            x = nx + 30 + k * 13
            out.append(f'<ellipse cx="{x}" cy="{ny}" rx="5" ry="17" fill="none" stroke="#c8733c" stroke-width="4"/>')
        # paper clips
        clips = [(nx + 290, ny + 4), (nx + 302, ny + 22), (nx + 296, ny + 42)] if on else [(nx + 250, 330), (nx + 275, 335), (nx + 300, 328)]
        for cx, cy in clips:
            out.append(f'<rect x="{cx - 8}" y="{cy - 14}" width="16" height="28" rx="8" fill="none" stroke="#e2e8f0" stroke-width="2.5"/>')
            out.append(f'<rect x="{cx - 4}" y="{cy - 8}" width="8" height="18" rx="4" fill="none" stroke="#e2e8f0" stroke-width="2"/>')
        # battery and switch
        bx, by = ox + 90, 300
        out.append(f'<rect x="{bx - 22}" y="{by - 30}" width="44" height="60" rx="5" fill="url(#battx)"/>')
        out.append(text(bx, by + 6, "+", 16, "#1a1a1a", weight="bold"))
        out += wire([(nx + 30, ny + 17), (nx + 30, 240), (bx, 240), (bx, by - 30)], 4)
        out += wire([(nx + 199, ny + 17), (nx + 199, 260), (bx + 80, 260)], 4)
        out += wire([(bx + 110, 260), (bx + 110, 360), (bx, 360), (bx, by + 30)], 4)
        if on:
            out.append(f'<line x1="{bx + 80}" y1="260" x2="{bx + 110}" y2="260" stroke="#e2e8f0" stroke-width="4"/>')
        else:
            out.append(f'<line x1="{bx + 80}" y1="260" x2="{bx + 104}" y2="240" stroke="#e2e8f0" stroke-width="4"/>')
        out.append(text(bx + 95, 285, "switch", 11, MUTED))
        out.append(text(ox + 202, 395, "the nail is a magnet: clips cling" if on else "no current, no magnet: clips fall", 13, TEXT, weight="bold"))
        return out
    parts += scene(15, True) + scene(440, False)
    return svg(w, h, "\n".join(parts), "A steel nail wrapped in copper wire, wired to a battery through a switch. With the switch closed, current flows, the nail becomes a magnet, and paper clips cling to its tip. With the switch open, no current flows and the clips fall away.")


# 4. A wire's field, and a coil's -----------------------------------------------------------
def wire_field():
    w, h = 860, 420
    grads = cyl_gradient("cu", "#c8733c")
    parts = [common_defs(grads), panel(15, 15, 405, h - 30), panel(440, 15, 405, h - 30)]
    parts.append(text(217, 48, "A current makes rings of field around a wire", 15, AMBER_LIGHT, weight="bold"))
    cx = 217
    parts.append(f'<rect x="{cx - 8}" y="80" width="16" height="280" fill="url(#cu)"/>')
    for k, y in enumerate((130, 190, 250, 310)):
        for rx in (40, 70):
            parts.append(f'<ellipse cx="{cx}" cy="{y}" rx="{rx}" ry="{rx * 0.3:.0f}" fill="none" stroke="{FIELD}" stroke-opacity="0.7" stroke-width="2"/>')
        parts.append(arrowhead(cx + 2, y + 70 * 0.3, 0))
    parts.append(f'<line x1="{cx + 110}" y1="330" x2="{cx + 110}" y2="110" stroke="{AMBER}" stroke-width="3" marker-end="url(#arrow)"/>')
    parts.append(text(cx + 120, 230, "current", 12, AMBER_LIGHT, "start"))
    parts.append(text(217, 390, "right-hand rule: thumb along the current, fingers curl with the field", 11, MUTED, italic=True))
    parts.append(text(642, 48, "Coil it up, and the rings add into a bar-magnet field", 15, AMBER_LIGHT, weight="bold"))
    for k in range(9):
        x = 540 + k * 22
        parts.append(f'<ellipse cx="{x}" cy="210" rx="9" ry="46" fill="none" stroke="#c8733c" stroke-width="5"/>')
    for spread in (60, 100, 140):
        for sign in (-1, 1):
            parts.append(f'<path d="M716,210 C800,{210 + sign * spread} 470,{210 + sign * spread} 520,210" fill="none" stroke="{FIELD}" stroke-opacity="0.55" stroke-width="2"/>')
    parts.append(f'<line x1="530" y1="210" x2="740" y2="210" stroke="{FIELD}" stroke-width="2.5"/>')
    parts.append(arrowhead(740, 210, 0))
    parts.append(text(760, 214, "N", 20, NRED, "start", "bold"))
    parts.append(text(505, 214, "S", 20, SBLUE, "end", "bold"))
    parts.append(text(642, 390, "an iron core inside makes it far stronger: an electromagnet", 11, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Left: a copper wire carrying current upward, surrounded by rings of magnetic field, with the right-hand rule: thumb along the current, fingers curling with the field. Right: the same wire wound into a coil, whose rings add into a field like a bar magnet's, with a north and a south end.")


# 5. Induction ----------------------------------------------------------------------
def induction():
    w, h = 860, 400
    parts = [common_defs(), panel(15, 15, 270, h - 30), panel(295, 15, 270, h - 30), panel(575, 15, 270, h - 30)]
    cases = [("Magnet moving in", "the needle swings one way", 25), ("Magnet held still", "nothing: no change, no voltage", 0),
             ("Magnet pulled out", "the needle swings the other way", -25)]
    for i, (t, sub, defl) in enumerate(cases):
        ox = 15 + i * 280
        cx = ox + 135
        parts.append(text(cx, 48, t, 15, AMBER_LIGHT if defl else TEXT, weight="bold"))
        for k in range(7):
            parts.append(f'<ellipse cx="{cx - 30 + k * 12}" cy="150" rx="6" ry="34" fill="none" stroke="#c8733c" stroke-width="4"/>')
        mx = cx - 140 + (30 if defl > 0 else 0 if defl == 0 else -30)
        parts += bar_magnet(mx, 165, w=100, h=30)
        if defl:
            d = 1 if defl > 0 else -1
            parts.append(f'<line x1="{mx + 50 - d * 20}" y1="190" x2="{mx + 50 + d * 20}" y2="190" stroke="{AMBER}" stroke-width="3" marker-end="url(#arrow)"/>')
        parts.append(f'<path d="M{cx + 42},150 L{cx + 60},150 L{cx + 60},260 M{cx - 42},150 L{cx - 60},150 L{cx - 60},260" fill="none" stroke="#cbd5e0" stroke-width="2"/>')
        parts.append(f'<rect x="{cx - 70}" y="250" width="140" height="70" rx="10" fill="#1a1d23" stroke="#cbd5e0" stroke-opacity="0.5"/>')
        parts.append(f'<path d="M{cx - 45},300 A45,45 0 0 1 {cx + 45},300" fill="none" stroke="#4a5568" stroke-width="2"/>')
        a = math.radians(-90 + defl * 2)
        parts.append(f'<line x1="{cx}" y1="300" x2="{cx + 40 * math.cos(a):.1f}" y2="{300 + 40 * math.sin(a):.1f}" stroke="{AMBER_LIGHT}" stroke-width="3"/>')
        parts.append(text(cx, 350, sub, 12, TEXT))
    return svg(w, h, "\n".join(parts), "Three scenes of a magnet and a coil connected to a meter. Moving the magnet into the coil swings the needle one way. Holding the magnet still gives no reading. Pulling it out swings the needle the other way.")


# 6. Transformer ------------------------------------------------------------------
def transformer():
    w, h = 820, 420
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "A transformer: two coils on one iron core, voltage set by the turns ratio", 15, TEXT, weight="bold"))
    core_x, core_y, cw, ch, t = 230, 100, 360, 230, 46
    parts.append(f'<rect x="{core_x}" y="{core_y}" width="{cw}" height="{ch}" rx="10" fill="#4a5568"/>')
    parts.append(f'<rect x="{core_x + t}" y="{core_y + t}" width="{cw - 2 * t}" height="{ch - 2 * t}" rx="6" fill="#1e2128"/>')
    parts.append(f'<rect x="{core_x}" y="{core_y}" width="{cw}" height="{ch}" rx="10" fill="url(#gloss)" opacity="0.5"/>')
    for k in range(10):
        y = core_y + 30 + k * 17
        parts.append(f'<ellipse cx="{core_x + t / 2}" cy="{y}" rx="36" ry="7" fill="none" stroke="#c8733c" stroke-width="4"/>')
    for k in range(3):
        y = core_y + 85 + k * 22
        parts.append(f'<ellipse cx="{core_x + cw - t / 2}" cy="{y}" rx="36" ry="8" fill="none" stroke="#e8a07a" stroke-width="6"/>')
    parts.append(f'<path d="M{core_x + 70},{core_y + t / 2} L{core_x + cw - 70},{core_y + t / 2}" stroke="{FIELD}" stroke-width="3" marker-end="url(#arrow)"/>')
    parts.append(text(core_x + cw / 2, core_y + t / 2 - 10, "changing field circulates in the core", 11, FIELD, italic=True))
    parts += pill(110, 215, "120 V AC in", "#d97706", "#1a1a1a", wpx=150, size=14, h=36)
    parts.append(text(110, 250, "primary: many turns", 12, TEXT))
    parts += pill(710, 215, "12 V AC out", "#2f855a", wpx=150, size=14, h=36)
    parts.append(text(710, 250, "secondary: 1/10 as many", 12, TEXT))
    parts.append(text(w / 2, 370, "Vout ÷ Vin = turns out ÷ turns in: a 10 : 1 ratio turns 120 V into 12 V", 13, AMBER_LIGHT, weight="bold"))
    parts.append(text(w / 2, 392, "only a changing current makes a changing field, so transformers work on AC, not steady DC", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "A transformer: a square iron core with a primary coil of many turns on the left, fed 120 volts AC, and a secondary coil of one tenth as many turns on the right, delivering 12 volts AC. The changing field circulates through the core.")


# 7. Field strength scale --------------------------------------------------------------
def field_scale():
    w, h = 820, 330
    L, R = 50, 770
    lo, hi = -5, 1
    X = lambda v: L + (R - L) * (math.log10(v) - lo) / (hi - lo)
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "Magnetic field strength, in tesla (T), log scale", 16, TEXT, weight="bold"))
    ty, th = 160, 28
    parts.append(f'<rect x="{L}" y="{ty}" width="{R - L}" height="{th}" rx="14" fill="{SBLUE}" fill-opacity="0.4"/>')
    parts.append(f'<rect x="{L}" y="{ty}" width="{R - L}" height="{th}" rx="14" fill="url(#gloss)" stroke="#e2e8f0" stroke-opacity="0.35"/>')
    names = {-5: "10 µT", -4: "100 µT", -3: "1 mT", -2: "10 mT", -1: "0.1 T", 0: "1 T", 1: "10 T"}
    for p in range(lo, hi + 1):
        x = X(10 ** p)
        parts.append(f'<line x1="{x:.1f}" y1="{ty + th}" x2="{x:.1f}" y2="{ty + th + 6}" stroke="{MUTED}"/>')
        parts.append(text(x, ty + th + 20, names[p], 10, MUTED))
    items = [((31e-6, 58e-6), "Earth", "31–58 µT", True), ((1e-3, 1e-2), "fridge magnet", "1–10 mT", False),
             ((0.1, 0.1), "small neodymium", "≈ 0.1 T", True), ((1, 2.4), "loudspeaker gap", "1–2.4 T", False), ((1.5, 7), "MRI scanner", "1.5–7 T", True)]
    for (a, b), lab, val, above in items:
        x1, x2 = X(a), X(b)
        mid = (x1 + x2) / 2
        if b == a:
            parts.append(f'<circle cx="{x1:.1f}" cy="{ty + th / 2}" r="8" fill="url(#eball)"/>')
        else:
            parts.append(f'<rect x="{x1:.1f}" y="{ty + 7}" width="{x2 - x1:.1f}" height="14" rx="7" fill="url(#eball)"/>')
        y = ty - 30 if above else ty + th + 62
        parts.append(f'<line x1="{mid:.1f}" y1="{ty - 2 if above else ty + th + 28}" x2="{mid:.1f}" y2="{y + (6 if above else -14)}" stroke="{MUTED}"/>')
        parts.append(text(mid, y - (16 if above else 0), lab, 12, TEXT, weight="bold"))
        parts.append(text(mid, y + (0 if above else 16), val, 12, AMBER_LIGHT))
    return svg(w, h, "\n".join(parts), "A log scale of magnetic field strength from 10 microtesla to 10 tesla: Earth's field at 31 to 58 microtesla, a fridge magnet at 1 to 10 millitesla, a small neodymium magnet near 0.1 tesla, a loudspeaker's magnet gap at 1 to 2.4 tesla, and an MRI scanner at 1.5 to 7 tesla.")


FIGURES = {
    "bar_field.svg": bar_field,
    "poles.svg": poles,
    "nail_electromagnet.svg": nail_electromagnet,
    "wire_field.svg": wire_field,
    "induction.svg": induction,
    "transformer.svg": transformer,
    "field_scale.svg": field_scale,
}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
