#!/usr/bin/env python3
"""Figures for docs/transistors.md.

Sources (datasheet values; every other number is computed):
- onsemi P2N2222A (NPN, TO-92, pins 1 C / 2 B / 3 E): VCEO 40 V, IC 600 mA,
  PD 625 mW at 25 degC ambient, hFE 100-300 at 150 mA (VCE 10 V),
  VCE(sat) 0.3 V max at IC 150 mA / IB 15 mA, VBE(sat) 0.6-1.2 V, fT 300 MHz.
- Infineon IRLZ44N (logic-level N-channel MOSFET, TO-220, G D S):
  VDS 55 V, RDS(on) 0.025 ohm at VGS 5 V, VGS(th) 1-2 V, RthJA 62 degC/W.
The worked load is a 12 V fan drawing 150 mA, modelled as 80 ohm.

Usage:
    python3 illustrations/transistors.py
"""

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, box3d,  # noqa: E402
                     common_defs, cyl_gradient, panel, pill, render_all, shade,
                     svg, text)
from ac_dc import axes, glow_line  # noqa: E402

OUT = HERE.parent / "docs" / "images" / "transistors"
NBLUE, PRED = "#2c5282", "#9b2c2c"

VCC, R_LOAD, HFE, VSAT = 12.0, 80.0, 150.0, 0.3
IC_MAX = (VCC - VSAT) / R_LOAD


def ic_of_ib(ib):
    return min(HFE * ib, IC_MAX)


# 1. A valve worked by a smaller valve -------------------------------------------------------
def valve():
    w, h = 860, 420
    parts = [common_defs(cyl_gradient("bigpipe", "#4a5568") + cyl_gradient("smallpipe", "#b7791f"))]
    parts.append(panel(15, 15, w - 30, h - 30))
    parts.append(text(w / 2, 48, "A small flow sets the size of a big one", 16, TEXT, weight="bold"))
    # big pipe: collector (top) to emitter (bottom)
    parts.append(f'<rect x="380" y="80" width="70" height="290" rx="8" fill="url(#bigpipe)"/>')
    for k in range(5):
        parts.append(f'<line x1="415" y1="{100 + k * 54}" x2="415" y2="{136 + k * 54}" stroke="#90cdf4" stroke-width="3" marker-end="url(#arrow)"/>')
    parts += box3d(355, 250, 120, 40, 50, "#2d3748")
    parts.append(text(415, 232, "gate", 12, MUTED))
    # small pipe: base
    parts.append(f'<rect x="150" y="214" width="205" height="18" rx="6" fill="url(#smallpipe)"/>')
    parts.append(f'<line x1="170" y1="223" x2="330" y2="223" stroke="#fff7e0" stroke-width="2" marker-end="url(#arrow)"/>')
    parts.append(text(150, 200, "base: 1 mA", 14, AMBER_LIGHT, "start", "bold"))
    parts.append(text(480, 100, "collector", 14, TEXT, "start", "bold"))
    parts.append(text(480, 118, "(from the load)", 12, MUTED, "start"))
    parts.append(text(480, 350, "emitter: 150 mA", 14, "#90cdf4", "start", "bold"))
    parts.append(text(480, 368, "(to ground)", 12, MUTED, "start"))
    parts.append(text(650, 220, "×150", 34, AMBER_LIGHT, weight="bold"))
    parts.append(text(650, 246, "current gain", 13, MUTED))
    return svg(w, h, "\n".join(parts), "A transistor as a valve. A thin amber pipe carrying 1 milliamp into the base opens a gate in a wide pipe, letting 150 milliamps flow from the collector down to the emitter: a current gain of 150.")


# 2. NPN and PNP structure --------------------------------------------------------------
def structure():
    w, h = 880, 440
    parts = [common_defs()]
    for k, (name, layers, arrow_out) in enumerate((("NPN", ("N", "P", "N"), True), ("PNP", ("P", "N", "P"), False))):
        x0 = 20 + k * 430
        parts.append(panel(x0, 20, 410, 400))
        parts.append(text(x0 + 205, 52, name, 18, AMBER_LIGHT, weight="bold"))
        bx, by = x0 + 50, 200
        widths = (110, 40, 110)
        x = bx
        for lab, wd in zip(layers, widths):
            col = NBLUE if lab == "N" else PRED
            parts += box3d(x, by, wd, 50, 90, col, shadow=(x == bx))
            parts.append(text(x + wd / 2, by - 40, lab, 20, "#ffffff", weight="bold"))
            x += wd
        labels = (("emitter", bx + 55), ("base", bx + 130), ("collector", bx + 205))
        for lab, lx in labels:
            parts.append(f'<rect x="{lx - 2}" y="{by}" width="4" height="40" fill="#cbd5e0"/>')
            parts.append(text(lx, by + 58, lab, 12, TEXT))
        # symbol
        sx, sy = x0 + 205, 330
        parts.append(f'<line x1="{sx - 60}" y1="{sy}" x2="{sx - 18}" y2="{sy}" stroke="{TEXT}" stroke-width="2.5"/>')
        parts.append(f'<line x1="{sx - 18}" y1="{sy - 26}" x2="{sx - 18}" y2="{sy + 26}" stroke="{TEXT}" stroke-width="4"/>')
        parts.append(f'<line x1="{sx - 18}" y1="{sy - 10}" x2="{sx + 22}" y2="{sy - 40}" stroke="{TEXT}" stroke-width="2.5"/>')
        if arrow_out:
            parts.append(f'<line x1="{sx - 18}" y1="{sy + 10}" x2="{sx + 22}" y2="{sy + 40}" stroke="{TEXT}" stroke-width="2.5" marker-end="url(#arrow)"/>')
            parts.append(text(sx + 30, sy + 50, "E", 13, TEXT, "start"))
            parts.append(text(sx + 30, sy - 40, "C", 13, TEXT, "start"))
            parts.append(text(x0 + 205, 404, "arrow points out: \"Not Pointing iN\"", 12, MUTED, italic=True))
        else:
            parts.append(f'<line x1="{sx + 22}" y1="{sy + 40}" x2="{sx - 16}" y2="{sy + 12}" stroke="{TEXT}" stroke-width="2.5" marker-end="url(#arrow)"/>')
            parts.append(text(sx + 30, sy + 50, "E", 13, TEXT, "start"))
            parts.append(text(sx + 30, sy - 40, "C", 13, TEXT, "start"))
            parts.append(text(x0 + 205, 404, "arrow points in: every polarity reversed", 12, MUTED, italic=True))
        parts.append(text(sx - 68, sy + 5, "B", 13, TEXT, "end"))
    return svg(w, h, "\n".join(parts), "Left: an NPN transistor as a 3D sandwich, N-type emitter, a thin P-type base, and N-type collector, with its symbol whose emitter arrow points out. Right: a PNP transistor, P, thin N, P, whose symbol's emitter arrow points in.")


# 3. Cutoff, active, saturation -------------------------------------------------------------
def regions():
    w, h = 880, 460
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Three regions: off, in proportion, fully on", 16, TEXT, weight="bold"))
    L, R, T, B = 90, 830, 90, 380
    ib_max = 2.0e-3
    y_of = lambda i: B - (B - T) * i / 0.18
    x_of = lambda ib: L + (R - L) * ib / ib_max
    axes(parts, L, R, T, B, B, "base current (0 to 2 mA)", [(y_of(0.15), "150 mA"), (y_of(0.075), "75 mA")])
    ib_sat = IC_MAX / HFE
    parts.append(f'<rect x="{L}" y="{T}" width="{x_of(0.05e-3) - L:.1f}" height="{B - T}" fill="#4a5568" fill-opacity="0.35"/>')
    parts.append(f'<rect x="{x_of(ib_sat):.1f}" y="{T}" width="{R - x_of(ib_sat):.1f}" height="{B - T}" fill="{GREEN}" fill-opacity="0.12"/>')
    pts = [(x_of(ib_max * k / 400), y_of(ic_of_ib(ib_max * k / 400))) for k in range(401)]
    parts.append(glow_line(pts, AMBER))
    parts.append(text(L + 10, B - 20, "cutoff", 13, MUTED, "start", "bold"))
    parts.append(text((L + x_of(ib_sat)) / 2 + 30, y_of(0.06), "active: collector current", 13, AMBER_LIGHT, "start", "bold"))
    parts.append(text((L + x_of(ib_sat)) / 2 + 30, y_of(0.06) + 18, f"= {HFE:.0f} × base current", 13, AMBER_LIGHT, "start", "bold"))
    parts.append(text(x_of(1.3e-3), y_of(0.15) + 34, "saturation: the load limits it", 13, GREEN, "middle", "bold"))
    parts.append(text(x_of(1.3e-3), y_of(0.15) + 52, f"(12 − {VSAT}) V ÷ 80 Ω ≈ {IC_MAX * 1000:.0f} mA", 12, TEXT))
    parts.append(f'<line x1="{x_of(ib_sat):.1f}" y1="{T}" x2="{x_of(ib_sat):.1f}" y2="{B}" stroke="{GREEN}" stroke-dasharray="5 4"/>')
    parts.append(text(x_of(ib_sat) + 6, B - 10, f"{ib_sat * 1000:.2f} mA", 11, GREEN, "start"))
    parts.append(text(w / 2, 432, "P2N2222A-style NPN, gain 150, switching a 12 V, 150 mA fan (modelled)", 11, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Collector current against base current for an NPN transistor driving a 12 volt, 80 ohm fan. Near zero base current it is in cutoff. In the active region collector current rises at 150 times the base current. Above about 1 milliamp of base current it saturates at about 146 milliamps, limited by the load.")


# 4. Where the heat goes ---------------------------------------------------------------------
def heat():
    w, h = 880, 440
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "A switch runs cool at both ends and hot in the middle", 16, TEXT, weight="bold"))
    L, R, T, B = 90, 830, 90, 360
    pmax = VCC ** 2 / (4 * R_LOAD)
    axes(parts, L, R, T, B, B, "how far on: collector current as a share of full (0 to 100%)", [(T + 20, f"{pmax * 1000:.0f} mW"), ((T + 20 + B) / 2, f"{pmax * 500:.0f} mW")])
    pts = []
    for k in range(401):
        f = k / 400
        ic = f * IC_MAX
        vce = max(VCC - ic * R_LOAD, VSAT)
        p = vce * ic
        pts.append((L + (R - L) * f, B - (B - T - 20) * p / pmax))
    parts.append(glow_line(pts, RED))
    on_p = VSAT * IC_MAX
    parts.append(text(L + 8, B - 14, "off: no current, 0 W", 12, MUTED, "start"))
    parts.append(text(R - 8, B - 14, f"fully on: {VSAT} V × {IC_MAX * 1000:.0f} mA ≈ {on_p * 1000:.0f} mW", 12, GREEN, "end", "bold"))
    parts.append(text((L + R) / 2, B - 100, f"half on: 6 V × 75 mA ≈ {pmax * 1000:.0f} mW", 13, RED, weight="bold"))
    parts.append(text((L + R) / 2, B - 82, "most of the P2N2222A's 625 mW rating", 12, TEXT))
    return svg(w, h, "\n".join(parts), f"Power dissipated in the transistor against how far it is turned on. Off, it dissipates nothing. Fully on, about {on_p * 1000:.0f} milliwatts. Half on, with 6 volts across it and 75 milliamps through it, about {pmax * 1000:.0f} milliwatts, most of the P2N2222A's 625 milliwatt rating.")


# 5. MOSFET channel ---------------------------------------------------------------------------
def mosfet():
    w, h = 880, 420
    parts = [common_defs()]
    for k, (title, on) in enumerate((("Gate at 0 V: no channel, off", False), ("Gate at 5 V: a channel forms, on", True))):
        x0 = 20 + k * 430
        parts.append(panel(x0, 20, 410, 380))
        parts.append(text(x0 + 205, 52, title, 15, GREEN if on else MUTED, weight="bold"))
        bx, by = x0 + 45, 300
        parts += box3d(bx, by, 300, 60, 120, PRED)
        parts += box3d(bx + 10, by - 70, 80, 40, 50, NBLUE, shadow=False)
        parts += box3d(bx + 210, by - 70, 80, 40, 50, NBLUE, shadow=False)
        parts += box3d(bx + 100, by - 112, 100, 40, 8, "#e2e8f0", shadow=False)
        parts += box3d(bx + 100, by - 120, 100, 40, 18, "#a0aec0", shadow=False)
        if on:
            parts.append(f'<rect x="{bx + 90}" y="{by - 112}" width="120" height="12" fill="#90cdf4" fill-opacity="0.85"/>')
            for j in range(6):
                parts.append(f'<circle cx="{bx + 98 + j * 21}" cy="{by - 106}" r="4" fill="url(#eball)"/>')
            parts.append(f'<line x1="{bx + 70}" y1="{by + 26}" x2="{bx + 230}" y2="{by + 26}" stroke="{AMBER}" stroke-width="3" marker-end="url(#arrow)"/>')
            parts.append(text(bx + 150, by + 48, "electrons: source to drain", 12, AMBER_LIGHT))
        else:
            parts.append(text(bx + 150, by + 30, "P-type body blocks the path", 12, MUTED))
        parts.append(text(bx + 50, by - 160, "source", 12, TEXT))
        parts.append(text(bx + 160, by - 178, "gate (on oxide)", 12, TEXT))
        parts.append(text(bx + 260, by - 160, "drain", 12, TEXT))
        parts.append(text(x0 + 205, 382, "no current flows into the gate: the oxide is an insulator", 11, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Cross-section of an N-channel MOSFET: two blue N-type regions, source and drain, in a red P-type body, with a metal gate sitting on a thin insulating oxide between them. With the gate at 0 volts there is no path. With 5 volts on the gate, electrons gather under the oxide to form a channel and electrons flow from source to drain.")


# 6. JFET pinch ---------------------------------------------------------------------------
def jfet():
    w, h = 880, 360
    parts = [common_defs()]
    for k, (vg, width) in enumerate(((0, 70), (-1, 40), (-3, 0))):
        x0 = 20 + k * 290
        parts.append(panel(x0, 20, 270, 320))
        parts.append(text(x0 + 135, 52, f"gate at {vg} V" if vg else "gate at 0 V", 15, AMBER_LIGHT, weight="bold"))
        cy = 180
        parts.append(f'<rect x="{x0 + 30}" y="{cy - 50}" width="210" height="100" rx="6" fill="{NBLUE}"/>')
        dep = (100 - width) / 2
        parts.append(f'<rect x="{x0 + 90}" y="{cy - 50}" width="90" height="{dep + 8:.0f}" rx="8" fill="#4a5568"/>')
        parts.append(f'<rect x="{x0 + 90}" y="{cy + 50 - dep - 8:.0f}" width="90" height="{dep + 8:.0f}" rx="8" fill="#4a5568"/>')
        parts.append(f'<rect x="{x0 + 110}" y="{cy - 62}" width="50" height="12" fill="{PRED}"/>')
        parts.append(f'<rect x="{x0 + 110}" y="{cy + 50}" width="50" height="12" fill="{PRED}"/>')
        parts.append(text(x0 + 135, cy - 70, "gate", 11, "#fc8181"))
        parts.append(text(x0 + 36, cy + 70, "source", 11, MUTED, "start"))
        parts.append(text(x0 + 234, cy + 70, "drain", 11, MUTED, "end"))
        if width:
            parts.append(f'<line x1="{x0 + 40}" y1="{cy}" x2="{x0 + 230}" y2="{cy}" stroke="{AMBER}" stroke-width="{max(2, width / 9):.0f}" marker-end="url(#arrow)"/>')
        parts.append(text(x0 + 135, 270, ("channel wide open", "squeezed: less current", "pinched off: none")[k], 13, TEXT))
        parts.append(text(x0 + 135, 292, ("most current", "more reverse bias", "")[k], 12, MUTED))
    return svg(w, h, "\n".join(parts), "Three views of an N-channel JFET. At 0 volts on the gate the channel between source and drain is wide open. At minus 1 volt the reverse-biased gate junction's depletion zones squeeze it narrower and less current flows. Further negative, the zones meet and pinch the channel off.")


# 7. Amplifying and distortion -------------------------------------------------------------
def amplify():
    w, h = 880, 400
    parts = [common_defs()]
    panels = (("A small input", 0.18, False, "#90cdf4"), ("Amplified: bigger, same shape", 0.8, False, AMBER),
              ("Overdriven: clipped, distorted", 1.6, True, RED))
    for k, (title, amp, clip, col) in enumerate(panels):
        x0 = 20 + k * 290
        parts.append(panel(x0, 20, 270, 360))
        parts.append(text(x0 + 135, 52, title, 14, col if k else "#90cdf4", weight="bold"))
        L, R, mid, scale = x0 + 20, x0 + 250, 200, 110
        parts.append(f'<line x1="{L}" y1="{mid}" x2="{R}" y2="{mid}" stroke="{MUTED}"/>')
        if clip:
            for yy in (mid - scale, mid + scale):
                parts.append(f'<line x1="{L}" y1="{yy}" x2="{R}" y2="{yy}" stroke="{MUTED}" stroke-dasharray="4 4"/>')
        pts = []
        for j in range(401):
            v = amp * math.sin(4 * math.pi * j / 400)
            if clip:
                v = max(-1, min(1, v))
            pts.append((L + (R - L) * j / 400, mid - scale * v))
        parts.append(glow_line(pts, col, 3))
        parts.append(text(x0 + 135, 345, ("", "gain: output ÷ input", "the supply's limits flatten the peaks")[k], 12, TEXT))
    return svg(w, h, "\n".join(parts), "Three waveforms. A small input sine wave. The same wave amplified, larger with the same shape. Overdriven, the peaks hit the limits set by the supply and are flattened: the output is distorted.")


# 8. The parts you'll meet -----------------------------------------------------------------
def parts_fig():
    w, h = 880, 380
    parts = [common_defs(cyl_gradient("to92", "#1a1a1a", vertical=True))]
    cards = (("P2N2222A", "NPN, TO-92", "40 V, 600 mA", ("C", "B", "E")),
             ("IRLZ44N", "N-channel MOSFET, TO-220", "55 V, 0.025 Ω at 5 V", ("G", "D", "S")),
             ("SOT-23", "surface-mount", "small transistors on boards", ("1", "2", "3")))
    for k, (name, kind, spec, pins) in enumerate(cards):
        cx = 160 + k * 280
        parts.append(panel(cx - 130, 20, 260, 340))
        cy = 150
        if k == 0:
            parts.append(f'<path d="M{cx - 34},{cy + 30} L{cx - 34},{cy - 20} A34,34 0 0 1 {cx + 34},{cy - 20} L{cx + 34},{cy + 30} Z" fill="url(#to92)"/>')
            parts.append(f'<rect x="{cx - 34}" y="{cy - 20}" width="68" height="50" fill="#2d3748" fill-opacity="0.6"/>')
            parts.append(text(cx, cy + 10, "2222A", 11, "#e2e8f0"))
            xs = (cx - 20, cx, cx + 20)
            ylead = cy + 30
        elif k == 1:
            parts += box3d(cx - 46, cy - 30, 92, 10, 40, "#a0aec0", shadow=False)
            parts.append(f'<circle cx="{cx + 3}" cy="{cy - 50}" r="9" fill="#2d3748"/>')
            parts += box3d(cx - 46, cy + 30, 92, 18, 60, "#1a1a1a")
            parts.append(text(cx, cy + 6, "IRLZ44N", 11, "#e2e8f0"))
            xs = (cx - 28, cx, cx + 28)
            ylead = cy + 30
        else:
            parts += box3d(cx - 20, cy + 10, 40, 22, 14, "#1a1a1a")
            xs = (cx - 14, cx + 14, cx)
            ylead = cy + 10
            parts.append(f'<rect x="{cx - 2}" y="{cy - 22}" width="4" height="10" fill="#cbd5e0"/>')
        for j, x in enumerate(xs):
            if k == 2 and j == 2:
                parts.append(text(x, cy - 28, pins[j], 12, AMBER_LIGHT, weight="bold"))
                continue
            parts.append(f'<rect x="{x - 2}" y="{ylead}" width="4" height="{60 if k < 2 else 12}" fill="#cbd5e0"/>')
            parts.append(text(x, ylead + (78 if k < 2 else 30), pins[j], 13, AMBER_LIGHT, weight="bold"))
        parts.append(text(cx, 290, name, 16, AMBER_LIGHT, weight="bold"))
        parts.append(text(cx, 312, kind, 12, TEXT))
        parts.append(text(cx, 332, spec, 12, MUTED))
    return svg(w, h, "\n".join(parts), "Three transistor packages with pin labels. A P2N2222A NPN in a black TO-92, pins collector, base, emitter. An IRLZ44N MOSFET in a TO-220 with a metal tab, pins gate, drain, source. And a tiny surface-mount SOT-23. Pin orders differ between parts, so always check the datasheet.")


FIGURES = {"valve.svg": valve, "structure.svg": structure, "regions.svg": regions, "heat.svg": heat,
           "mosfet.svg": mosfet, "jfet.svg": jfet, "amplify.svg": amplify, "parts.svg": parts_fig}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
