#!/usr/bin/env python3
"""Figures for docs/ac_dc.md.

Numbers and sources:
- Canadian outlets: 120 V RMS at 60 Hz. Peak = 120 x sqrt(2) = 169.7 V; period
  1/60 s = 16.7 ms; two zero crossings per cycle = 120 per second.
- Wikipedia "Utility frequency": Niagara's first Westinghouse generators (1895)
  ran at 25 Hz; Europe standardized on 50 Hz.
- 100 W, 120 V bulb from the Ohm's Law article: 144 Ohm hot, 0.83 A RMS.
- Frequency examples: the 40 m amateur band (7 MHz), the 2 m band (146 MHz),
  AM broadcast around 1 MHz, Wi-Fi at 2.4 GHz.

Usage:
    python3 illustrations/ac_dc.py
"""

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, common_defs,  # noqa: E402
                     cyl_gradient, panel, pill, render_all, shade, svg, text)

OUT = HERE.parent / "docs" / "images" / "ac_dc"
VRMS, F = 120.0, 60.0
VPK = VRMS * math.sqrt(2)


def axes(parts, L, R, T, B, mid, xlab, ylabs):
    for y, lab in ylabs:
        parts.append(f'<line x1="{L}" y1="{y:.1f}" x2="{R}" y2="{y:.1f}" stroke="#4a5568" stroke-opacity="0.4"/>')
        parts.append(text(L - 8, y + 4, lab, 11, MUTED, "end"))
    parts.append(f'<line x1="{L}" y1="{mid}" x2="{R}" y2="{mid}" stroke="{MUTED}" stroke-width="1.5"/>')
    parts.append(f'<line x1="{L}" y1="{T}" x2="{L}" y2="{B}" stroke="{MUTED}" stroke-width="1.5"/>')
    parts.append(text((L + R) / 2, B + 22, xlab, 12, MUTED))


def glow_line(pts, color, width=3.5):
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polyline points="{line}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round" filter="url(#softglow)"/>'


# 1. DC versus AC ---------------------------------------------------------------------
def dc_vs_ac():
    w, h = 860, 400
    parts = [common_defs(), panel(15, 15, 405, h - 30), panel(440, 15, 405, h - 30)]
    # DC
    L, R, T, B = 70, 395, 90, 330
    mid = 240
    parts.append(text(217, 48, "DC: one direction, steady", 16, AMBER_LIGHT, weight="bold"))
    axes(parts, L, R, T, B, mid, "time", [(mid - 120, "+9 V")])
    # no blur filter here: a perfectly horizontal line has a zero-height box and vanishes
    parts.append(f'<rect x="{L}" y="{mid - 128}" width="{R - L}" height="16" rx="8" fill="{AMBER}" fill-opacity="0.2"/>')
    parts.append(f'<line x1="{L}" y1="{mid - 120}" x2="{R}" y2="{mid - 120}" stroke="{AMBER}" stroke-width="3.5"/>')
    parts.append(text(217, 100, "a 9 V battery: always +9 V", 12, TEXT))
    # AC
    L2, R2, T2, B2, mid2 = 495, 820, 80, 340, 210
    amp = 110
    parts.append(text(642, 48, "AC: reverses 60 times a second", 16, AMBER_LIGHT, weight="bold"))
    axes(parts, L2, R2, T2, B2, mid2, "time: two cycles = 33 ms", [(mid2 - amp, f"+{VPK:.0f} V"), (mid2 + amp, f"−{VPK:.0f} V")])
    pts = [(L2 + (R2 - L2) * k / 400, mid2 - amp * math.sin(4 * math.pi * k / 400)) for k in range(401)]
    parts.append(glow_line(pts, "#90cdf4"))
    rms_y = mid2 - amp / math.sqrt(2)
    parts.append(f'<line x1="{L2}" y1="{rms_y:.1f}" x2="{R2}" y2="{rms_y:.1f}" stroke="{AMBER}" stroke-dasharray="6 5" stroke-width="2"/>')
    parts.append(text(R2, rms_y - 6, "120 V RMS", 12, AMBER_LIGHT, "end", "bold"))
    return svg(w, h, "\n".join(parts), "Two graphs of voltage against time. DC from a 9 volt battery is a flat line at plus 9 volts. AC from a Canadian outlet is a sine wave swinging between plus and minus 170 volts, two cycles in 33 milliseconds, with a dashed line marking its 120 volt RMS value.")


# 2. The elementary generator ----------------------------------------------------------
def generator():
    w, h = 860, 430
    grads = cyl_gradient("coilw", "#c8733c")
    parts = [common_defs(grads), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "A loop turning between magnet poles makes AC", 16, TEXT, weight="bold"))
    # magnet poles
    from style3d import box3d
    parts += box3d(50, 300, 90, 40, 190, "#c53030")
    parts += box3d(330, 300, 90, 40, 190, "#2b6cb0")
    parts.append(text(95, 210, "N", 30, "#ffffff", weight="bold"))
    parts.append(text(375, 210, "S", 30, "#ffffff", weight="bold"))
    for y in (140, 170, 200, 230, 260):
        parts.append(f'<line x1="145" y1="{y}" x2="328" y2="{y}" stroke="#90cdf4" stroke-opacity="0.35" stroke-dasharray="4 6"/>')
        parts.append(f'<path d="M318,{y - 5} L328,{y} L318,{y + 5}" fill="none" stroke="#90cdf4" stroke-opacity="0.5"/>')
    parts.append(text(236, 112, "magnetic field", 11, "#90cdf4", italic=True))
    # rotating loop drawn in perspective
    parts.append(f'<ellipse cx="236" cy="200" rx="60" ry="74" fill="none" stroke="#9c4221" stroke-width="10"/>')
    parts.append(f'<ellipse cx="236" cy="200" rx="60" ry="74" fill="none" stroke="#f6ad55" stroke-width="5"/>')
    parts.append(f'<path d="M290,150 A70,80 0 0 1 300,230" fill="none" stroke="{AMBER_LIGHT}" stroke-width="3" marker-end="url(#arrow)"/>')
    parts.append(text(312, 160, "turns", 12, AMBER_LIGHT, "start", italic=True))
    # shaft, slip rings, brushes
    parts.append(f'<line x1="236" y1="274" x2="236" y2="340" stroke="#cbd5e0" stroke-width="5"/>')
    for k, y in enumerate((320, 340)):
        parts.append(f'<ellipse cx="236" cy="{y}" rx="22" ry="7" fill="none" stroke="#d4af37" stroke-width="4"/>')
        parts.append(f'<rect x="262" y="{y - 6}" width="14" height="12" fill="#4a5568"/>')
        parts.append(f'<line x1="276" y1="{y}" x2="470" y2="{y}" stroke="#cbd5e0" stroke-width="2"/>')
    parts.append(text(236, 370, "slip rings and brushes carry the current out", 11, MUTED, italic=True))
    # output waveform with loop positions
    L, R, mid, amp = 480, 820, 210, 90
    parts.append(f'<line x1="{L}" y1="{mid}" x2="{R}" y2="{mid}" stroke="{MUTED}" stroke-width="1.5"/>')
    pts = [(L + (R - L) * k / 300, mid - amp * math.sin(2 * math.pi * k / 300)) for k in range(301)]
    parts.append(glow_line(pts, "#90cdf4"))
    for deg, lab in ((0, "0°"), (90, "90°: max"), (180, "180°"), (270, "270°: max, reversed"), (360, "360°")):
        x = L + (R - L) * deg / 360
        y = mid - amp * math.sin(math.radians(deg))
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="url(#vball)"/>')
        dy = {0: 20, 90: -14, 180: 20, 270: 26, 360: 20}[deg]
        parts.append(text(x, y + dy, lab, 11, TEXT))
    parts.append(text((L + R) / 2, 362, "one full turn of the loop = one cycle", 13, AMBER_LIGHT, weight="bold"))
    parts.append(text((L + R) / 2, 382, "60 turns per second = 60 Hz", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "An elementary generator: a copper loop turns between a north and a south magnet pole, with slip rings and brushes carrying the current out. Beside it, one cycle of the sine wave it produces, marked at 0, 90, 180, 270 and 360 degrees of rotation: zero, maximum, zero, maximum reversed, and zero.")


# 3. RMS: the heating equivalent --------------------------------------------------------
def rms():
    w, h = 860, 420
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "RMS: the steady DC voltage that heats a resistor just as much", 16, TEXT, weight="bold"))
    L, R, mid, amp = 70, 470, 220, 120
    parts.append(f'<line x1="{L}" y1="{mid}" x2="{R}" y2="{mid}" stroke="{MUTED}" stroke-width="1.5"/>')
    pts = [(L + (R - L) * k / 300, mid - amp * math.sin(2 * math.pi * k / 300)) for k in range(301)]
    sq = [(L + (R - L) * k / 300, mid - amp * math.sin(2 * math.pi * k / 300) ** 2) for k in range(301)]
    fill = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in sq) + f" L{R},{mid} L{L},{mid} Z"
    parts.append(f'<path d="{fill}" fill="{AMBER}" fill-opacity="0.18"/>')
    parts.append(glow_line(pts, "#90cdf4", 3))
    parts.append(glow_line(sq, AMBER, 2.5))
    rms_y = mid - amp / math.sqrt(2)
    parts.append(f'<line x1="{L}" y1="{rms_y:.1f}" x2="{R}" y2="{rms_y:.1f}" stroke="#9ae6b4" stroke-dasharray="6 5" stroke-width="2"/>')
    parts.append(text(L + 6, mid - amp - 8, f"peak {VPK:.0f} V", 12, "#90cdf4", "start", "bold"))
    parts.append(text(R - 4, rms_y - 8, f"RMS {VRMS:.0f} V = 0.707 × peak", 12, "#9ae6b4", "end", "bold"))
    parts.append(text((L + R) / 2, 372, "amber: voltage squared, always positive (heating goes with V²)", 11, AMBER_LIGHT, "middle", italic=True))
    parts.append(text((L + R) / 2, 390, "average the amber, take the square root: that's the RMS", 11, MUTED, "middle", italic=True))
    # two heaters glowing equally
    for i, (lab, sub) in enumerate((("120 V DC", "steady"), ("120 V RMS AC", f"swinging to ±{VPK:.0f} V"))):
        cx = 600 + i * 150
        parts.append(f'<circle cx="{cx}" cy="200" r="58" fill="#fc8181" fill-opacity="0.18"/>')
        for k in range(3):
            parts.append(f'<path d="M{cx - 40},{176 + k * 24} q10,-10 20,0 t20,0 t20,0 t20,0" fill="none" stroke="#fc8181" stroke-width="4"/>')
        parts.append(text(cx, 300, lab, 13, TEXT, weight="bold"))
        parts.append(text(cx, 318, sub, 11, MUTED, italic=True))
    parts.append(text(675, 350, "same heat, same RMS", 13, "#9ae6b4", weight="bold"))
    return svg(w, h, "\n".join(parts), "Left: one cycle of a sine wave peaking at 170 volts, its square in amber (always positive), and a dashed line at 120 volts RMS, 0.707 times the peak. Right: two identical heaters, one on 120 volts DC and one on 120 volts RMS AC, glowing equally.")


# 4. Voltage and current in phase in a resistor --------------------------------------------
def in_phase():
    w, h = 820, 400
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "In a resistor, current follows voltage step for step: they're in phase", 15, TEXT, weight="bold"))
    L, R, mid = 90, 760, 210
    ipk = VPK / 144
    parts.append(f'<line x1="{L}" y1="{mid}" x2="{R}" y2="{mid}" stroke="{MUTED}" stroke-width="1.5"/>')
    vp = [(L + (R - L) * k / 400, mid - 120 * math.sin(4 * math.pi * k / 400)) for k in range(401)]
    ip = [(L + (R - L) * k / 400, mid - 70 * math.sin(4 * math.pi * k / 400)) for k in range(401)]
    parts.append(glow_line(vp, "#90cdf4"))
    parts.append(glow_line(ip, AMBER))
    for k in (0.125, 0.625):
        x = L + (R - L) * k
        parts.append(f'<line x1="{x:.1f}" y1="{mid - 140}" x2="{x:.1f}" y2="{mid + 140}" stroke="#9ae6b4" stroke-dasharray="3 4" stroke-opacity="0.7"/>')
    parts.append(text(L + 8, mid - 128, f"voltage: peak {VPK:.0f} V", 12, "#90cdf4", "start", "bold"))
    parts.append(text(L + 8, mid - 76, f"current: peak {ipk:.2f} A", 12, AMBER_LIGHT, "start", "bold"))
    parts.append(text(w / 2, 372, f"a 100 W bulb (144 Ω hot) on a 120 V outlet: {VRMS / 144:.2f} A RMS, {ipk:.2f} A peak; both peak together and cross zero together", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), f"Voltage and current through a 144 ohm bulb on a 120 volt outlet, two sine waves that peak together and cross zero together: voltage peaking at {VPK:.0f} volts and current at {VPK / 144:.2f} amps.")


# 5. Waveforms ----------------------------------------------------------------------
def waveforms():
    w, h = 860, 340
    parts = [common_defs()]
    parts.append(text(w / 2, 34, "Three common waveforms, each with the same peak", 16, TEXT, weight="bold"))
    shapes = [("Sine", "mains power, radio signals", lambda t: math.sin(2 * math.pi * t), "RMS = 0.707 × peak"),
              ("Square", "digital circuits, clock signals", lambda t: 1 if (t % 1) < 0.5 else -1, "RMS = peak"),
              ("Triangle", "some test signals and synthesizers", lambda t: 1 - 4 * abs((t % 1) - 0.5) if True else 0, "RMS = 0.577 × peak")]
    for i, (name, use, fn, note) in enumerate(shapes):
        ox = 25 + i * 280
        parts.append(panel(ox, 55, 260, 270))
        parts.append(text(ox + 130, 86, name, 16, AMBER_LIGHT, weight="bold"))
        L, R, mid, amp = ox + 25, ox + 235, 175, 55
        parts.append(f'<line x1="{L}" y1="{mid}" x2="{R}" y2="{mid}" stroke="{MUTED}"/>')
        pts = []
        for k in range(401):
            t = 2 * k / 400
            v = fn(t if name != "Triangle" else t + 0.25)
            pts.append((L + (R - L) * k / 400, mid - amp * v))
        if name == "Square":
            sq = []
            for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                sq.append((x1, y1))
                if y1 != y2:
                    sq.append((x2, y1))
            pts = sq + [pts[-1]]
        parts.append(glow_line(pts, "#90cdf4", 3))
        parts.append(text(ox + 130, 262, note, 13, "#9ae6b4", weight="bold"))
        parts.append(text(ox + 130, 286, use, 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Three waveforms with the same peak: a sine wave, used by mains power and radio, with an RMS of 0.707 times the peak; a square wave, used in digital circuits, whose RMS equals its peak; and a triangle wave, with an RMS of 0.577 times the peak.")


# 6. Frequency scale ----------------------------------------------------------------
def frequency_scale():
    w, h = 860, 330
    L, R = 50, 810
    lo, hi = 1, 10
    X = lambda v: L + (R - L) * (math.log10(v) - lo) / (hi - lo)
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 46, "Alternating current at every speed: from mains to Wi-Fi (log scale)", 16, TEXT, weight="bold"))
    ty, th = 160, 28
    parts.append(f'<rect x="{L}" y="{ty}" width="{R - L}" height="{th}" rx="14" fill="#3182ce" fill-opacity="0.4"/>')
    parts.append(f'<rect x="{L}" y="{ty}" width="{R - L}" height="{th}" rx="14" fill="url(#gloss)" stroke="#e2e8f0" stroke-opacity="0.35"/>')
    names = {1: "10 Hz", 2: "100 Hz", 3: "1 kHz", 4: "10 kHz", 5: "100 kHz", 6: "1 MHz", 7: "10 MHz", 8: "100 MHz", 9: "1 GHz", 10: "10 GHz"}
    for p in range(lo, hi + 1):
        x = X(10 ** p)
        parts.append(f'<line x1="{x:.1f}" y1="{ty + th}" x2="{x:.1f}" y2="{ty + th + 6}" stroke="{MUTED}"/>')
        parts.append(text(x, ty + th + 20, names[p], 10, MUTED))
    items = [(25, "Niagara, 1895", "25 Hz", True), (60, "Canadian mains", "60 Hz", False), (1000, "a 1 kHz tone", "1 kHz", True),
             (1e6, "AM radio", "~1 MHz", False), (7e6, "40 m amateur band", "7 MHz", True), (146e6, "2 m amateur band", "146 MHz", False),
             (2.4e9, "Wi-Fi", "2.4 GHz", True)]
    for v, lab, val, above in items:
        x = X(v)
        parts.append(f'<circle cx="{x:.1f}" cy="{ty + th / 2}" r="8" fill="url(#eball)"/>')
        y = ty - 30 if above else ty + th + 62
        parts.append(f'<line x1="{x:.1f}" y1="{ty - 2 if above else ty + th + 28}" x2="{x:.1f}" y2="{y + (6 if above else -14)}" stroke="{MUTED}"/>')
        parts.append(text(x, y - (16 if above else 0), lab, 12, TEXT, weight="bold"))
        parts.append(text(x, y + (0 if above else 16), val, 12, AMBER_LIGHT))
    return svg(w, h, "\n".join(parts), "A log scale of frequency from 10 hertz to 10 gigahertz: Niagara's original 25 hertz power, Canadian mains at 60 hertz, a 1 kilohertz tone, AM radio near 1 megahertz, the 40 metre amateur band at 7 megahertz, the 2 metre band at 146 megahertz, and Wi-Fi at 2.4 gigahertz.")


FIGURES = {
    "dc_vs_ac.svg": dc_vs_ac,
    "generator.svg": generator,
    "rms.svg": rms,
    "in_phase.svg": in_phase,
    "waveforms.svg": waveforms,
    "frequency_scale.svg": frequency_scale,
}

if __name__ == "__main__":
    print(f"peak {VPK:.1f} V, period {1000 / F:.1f} ms, bulb {VRMS / 144:.3f} A RMS / {VPK / 144:.3f} A peak")
    render_all(FIGURES, OUT)
