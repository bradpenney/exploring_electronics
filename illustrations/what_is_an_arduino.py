#!/usr/bin/env python3
"""Figures for docs/what_is_an_arduino.md.

arduino_uno.svg replaces the old flat images/arduino_board_anatomy.svg. It is a
simplified 3D Arduino Uno R3 seen from above, USB port on the left, laid out like
the real board (Arduino's Uno R3 board drawing): digital pins 0-13 along the far
(top) edge, power and analog pins A0-A5 along the near (bottom) edge, the reset
button beside the USB port, the "L" LED by pin 13, and the ATmega328P (a 28-pin
DIP) at the lower right. (The old flat diagram had the two header rows swapped.)

Board size 68.6 x 53.4 mm; drawn at SCALE px per mm.

Usage:
    python3 illustrations/what_is_an_arduino.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, MUTED, common_defs, panel, pill,  # noqa: E402
                     render_all, shade, svg, text)

OUT = HERE.parent / "docs" / "images" / "what_is_an_arduino"
SCALE = 6.4
BOARD_W, BOARD_D, BOARD_T = 68.6, 53.4, 1.6
TEAL = "#0e7c86"


def arduino_uno():
    w, h = 820, 560
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    x0, y0 = 175, 455          # board front-bottom-left, on screen
    DX, DY, DZ = 0.30, 0.74, 0.42  # oblique camera: depth shift right/up, height squash

    def at(u, v, z=0.0):
        return (x0 + u * SCALE + v * SCALE * DX,
                y0 - BOARD_T * SCALE * DZ - v * SCALE * DY - z * SCALE * DZ)

    def prism(u, v, wmm, dmm, hmm, color, z0=0.0):
        """Box on the board: top face, front face (v), right face (u + w)."""
        f = [at(u, v, z0), at(u + wmm, v, z0), at(u + wmm, v, z0 + hmm), at(u, v, z0 + hmm)]
        t = [at(u, v, z0 + hmm), at(u + wmm, v, z0 + hmm), at(u + wmm, v + dmm, z0 + hmm), at(u, v + dmm, z0 + hmm)]
        r = [at(u + wmm, v, z0), at(u + wmm, v + dmm, z0), at(u + wmm, v + dmm, z0 + hmm), at(u + wmm, v, z0 + hmm)]
        poly = lambda pts, c: '<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="{c}"/>'
        return [poly(r, shade(color, -0.45)), poly(f, shade(color, -0.2)), poly(t, color),
                poly(t, "url(#gloss)").replace('fill="url(#gloss)"', 'fill="url(#gloss)" opacity="0.5"')]

    # board slab
    bl, br, tr, tl = at(0, 0), at(BOARD_W, 0), at(BOARD_W, BOARD_D), at(0, BOARD_D)
    parts.append(f'<ellipse cx="{(bl[0] + tr[0]) / 2:.1f}" cy="{y0 + 14}" rx="300" ry="20" fill="#000" fill-opacity="0.45"/>')
    parts += prism(0, 0, BOARD_W, BOARD_D, BOARD_T, TEAL, z0=-BOARD_T)
    for u, v in ((14, 2.5), (66, 7.6), (66, 35.5), (15.2, 50.8)):
        x, y = at(u, v)
        parts.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="7" ry="5.5" fill="#063c42" stroke="#cbd5e0" stroke-opacity="0.5"/>')
    for v in (20, 23, 26, 29):
        a, b = at(20, v), at(46, v)
        parts.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#4fd1c5" stroke-opacity="0.25" stroke-width="2"/>')
    parts.append(text(*at(52, 30), "UNO", 26, "#e6fffa", weight="bold").replace(">UNO<", ' opacity="0.35">UNO<'))

    labels = []
    # drawn back to front
    parts += prism(17.5, 49.5, 25.4, 2.5, 8.5, "#22262e")
    parts += prism(44.5, 49.5, 20.3, 2.5, 8.5, "#22262e")
    labels.append((at(54, 51, 8.5), (600, 62), "Digital pins 0–13"))
    parts += prism(5.5, 44, 6, 6, 3.2, "#4a5568")
    rx, ry = at(8.5, 47, 3.2)
    parts.append(f'<ellipse cx="{rx:.1f}" cy="{ry:.1f}" rx="9" ry="7" fill="#e53e3e"/>')
    labels.append(((rx, ry), (150, 62), "Reset button"))
    parts += prism(27.5, 44, 1.6, 0.8, 0.6, "#fbd38d")
    lx, ly = at(28.3, 44.4, 0.6)
    parts.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="14" fill="url(#glow)"/>')
    labels.append(((lx, ly), (370, 62), "Onboard LED “L” (pin 13)"))
    parts += prism(-6.3, 31, 16, 12, 10.9, "#cbd5e0")
    labels.append((at(-2, 37, 10.9), (140, 150), "USB port (power + code)"))
    # ATmega328P in its socket
    parts += prism(31, 4.5, 35.6, 7.6, 1.2, "#111418")
    for k in range(14):
        for v in (4.6, 11.6):
            x, y = at(32.5 + k * 2.54, v, 1.2)
            parts.append(f'<rect x="{x - 1.5:.1f}" y="{y - 2.5:.1f}" width="3" height="4" fill="#cbd5e0"/>')
    parts += prism(31.4, 5, 34.8, 6.6, 3.6, "#2a2f38", z0=1.2)
    cx_, cy_ = at(48.8, 8.3, 4.8)
    parts.append(text(cx_, cy_ + 4, "ATMEGA328P", 11, "#a0aec0", weight="bold"))
    labels.append(((cx_ + 70, cy_), (660, 330), "ATmega328P (the microcontroller)"))
    parts += prism(-1.8, 3.3, 13.7, 9, 11, "#1a1d23")
    labels.append((at(2, 7, 11), (150, 470), "Power jack (external power)"))
    parts += prism(26.7, 0.8, 20.3, 2.5, 8.5, "#22262e")
    parts += prism(49.6, 0.8, 15.2, 2.5, 8.5, "#22262e")
    labels.append((at(40, 1.2, 8.5), (560, 500), "Power and analog pins A0–A5"))

    for (ax, ay), (px, py), lab in labels:
        parts.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{px}" y2="{py}" stroke="{AMBER}" stroke-opacity="0.7" stroke-width="1.5"/>')
        parts.append(f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="3.5" fill="{AMBER}"/>')
    for (ax, ay), (px, py), lab in labels:
        parts += pill(px, py, lab, "#2d3748", size=12, h=28)
    parts.append(text(w / 2, h - 30, "simplified, but every part shown is really there, in the place it really is", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "A simplified 3D Arduino Uno seen from above with the USB port on the left: digital pins along the far edge, power and analog pins along the near edge, reset button by the USB port, the onboard L LED by pin 13, and the ATmega328P chip at the lower right")


from style3d import AMBER_LIGHT, GREEN, TEXT, box3d  # noqa: E402
import math  # noqa: E402


# 2. Inside the microcontroller (ATmega328P datasheet: 32 KB flash, 2 KB SRAM) ------------------------
def inside_chip():
    w, h = 900, 430
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "A whole computer on one chip: the ATmega328P", 17, AMBER_LIGHT, weight="bold"))
    parts += box3d(170, 360, 560, 90, 250, "#1a202c")
    for k in range(14):
        x = 186 + k * 39
        parts.append(f'<rect x="{x}" y="360" width="10" height="26" fill="#a0aec0"/>')
    blocks = [(190, "Processor", "runs the sketch, one", "instruction at a time", "#c05621"),
              (370, "Flash: 32 KB", "the program; kept", "when power is off", "#2b6cb0"),
              (550, "SRAM: 2 KB", "working data; lost", "when power is off", "#2f855a")]
    for x, name, l1, l2, col in blocks:
        parts += box3d(x, 300, 150, 34, 140, col, shadow=False)
        parts.append(text(x + 75, 215, name, 14, "#ffffff", weight="bold"))
        parts.append(text(x + 75, 245, l1, 11, "#ffffff"))
        parts.append(text(x + 75, 261, l2, 11, "#ffffff"))
    parts.append(text(w / 2, 404, "pins: the chip's only connection to the outside world", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "A 3D microcontroller chip opened to show three blocks inside: a processor that runs the sketch one instruction at a time; 32 kilobytes of flash memory that holds the program and keeps it with the power off; and 2 kilobytes of SRAM for working data, lost when the power goes off. Pins along the bottom edge are its only connection to the outside world.")


# 3. setup() once, loop() forever ------------------------------------------------------------------------
def setup_loop():
    w, h = 900, 420
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "What the board does with a sketch", 17, AMBER_LIGHT, weight="bold"))
    parts += pill(140, 230, "power on / reset", "#4a5568", size=13, h=40, wpx=170)
    parts.append(f'<path d="M228,230 L300,230" stroke="{AMBER_LIGHT}" stroke-width="4" marker-end="url(#arrow)"/>')
    parts += pill(380, 230, "setup()", "#c05621", size=16, h=56, wpx=140)
    parts.append(text(380, 285, "runs once", 12, MUTED, italic=True))
    parts.append(f'<path d="M452,230 L540,230" stroke="{AMBER_LIGHT}" stroke-width="4" marker-end="url(#arrow)"/>')
    cx, cy, r = 650, 230, 95
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GREEN}" stroke-width="12"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#gloss)" stroke-width="12" opacity="0.4"/>')
    a = math.radians(-40)
    ax, ay = cx + r * math.cos(a), cy + r * math.sin(a)
    parts.append(f'<path d="M{ax - 6:.1f},{ay - 12:.1f} l14,6 l-12,10 z" fill="{GREEN}"/>')
    parts.append(text(cx, cy + 2, "loop()", 18, TEXT, weight="bold"))
    parts.append(text(cx, cy + 24, "again and again", 12, MUTED, italic=True))
    parts.append(text(cx, cy + r + 34, "until the power goes off", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Power on or reset leads to setup(), which runs once, and then to loop(), drawn as a ring that runs again and again until the power goes off.")


FIGURES = {"arduino_uno.svg": arduino_uno, "inside_chip.svg": inside_chip, "setup_loop.svg": setup_loop}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
