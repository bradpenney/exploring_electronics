#!/usr/bin/env python3
"""Figures for docs/serial_communication.md.

Sources:
- Arduino Serial reference (arduino/reference-en): Serial.begin(speed) sets
  bits per second (baud); default config 8 data bits, no parity, one stop bit;
  TX/RX use TTL levels (5 V or 3.3 V); RS-232 ports run at +/-12 V and can
  damage the board.
- Wikipedia "Universal asynchronous receiver-transmitter": idle high, start
  bit low, least significant bit first, stop bit high; receivers sample in
  the middle of each bit.
- ASCII: 'A' = 65 = 0x41.
The mismatched-baud panels are simulated below: a receiver that sees the start
edge and then samples at the middle of each of its own bit times.

Usage:
    python3 illustrations/serial_communication.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, box3d,  # noqa: E402
                     common_defs, panel, pill, render_all, shade, svg, text)
from ac_dc import glow_line  # noqa: E402

OUT = HERE.parent / "docs" / "images" / "serial_communication"
BLUE = "#4299e1"
BAUD = 9600


def frame(byte):
    """8N1: start (0), 8 data bits LSB first, stop (1)."""
    return [0] + [(byte >> i) & 1 for i in range(8)] + [1]


def receive(byte, tx_baud, rx_baud):
    """What a receiver at rx_baud makes of byte sent at tx_baud."""
    bits = frame(byte)

    def level(t):
        k = int(t * tx_baud)
        return bits[k] if k < len(bits) else 1
    samples = [(1.5 + k) / rx_baud for k in range(8)]
    value = sum(level(t) << k for k, t in enumerate(samples))
    stop_ok = level(9.5 / rx_baud) == 1
    return value, samples, stop_ok


def _wave(parts, L, R, top, low, bits, color, idle=1.0):
    """Draw idle, the frame bits, idle, across [L, R]; returns x per bit."""
    n = len(bits) + 2 * idle
    bw = (R - L) / n
    y = lambda b: top if b else low
    pts = [(L, y(1)), (L + idle * bw, y(1))]
    x = L + idle * bw
    for b in bits:
        pts += [(x, y(b)), (x + bw, y(b))]
        x += bw
    pts += [(x, y(1)), (R, y(1))]
    parts.append(glow_line(pts, color, 3))
    return L + idle * bw, bw


# 1. One character on the wire -----------------------------------------------------------------
def frame_a():
    w, h = 900, 420
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "The letter A (65, binary 01000001) leaving a TX pin at 9600 baud", 17, AMBER_LIGHT, weight="bold"))
    bits = frame(ord("A"))
    L, R, top, low = 70, 830, 150, 250
    x0, bw = _wave(parts, L, R, top, low, bits, "#90cdf4")
    parts.append(text(L - 8, top + 4, "5 V", 11, MUTED, "end"))
    parts.append(text(L - 8, low + 4, "0 V", 11, MUTED, "end"))
    names = ["start"] + [f"bit {k}" for k in range(8)] + ["stop"]
    colors = [RED] + [AMBER] * 8 + [GREEN]
    for k, (b, nm, col) in enumerate(zip(bits, names, colors)):
        cx = x0 + (k + 0.5) * bw
        parts.append(f'<rect x="{x0 + k * bw + 2:.1f}" y="{top - 40}" width="{bw - 4:.1f}" height="22" rx="5" fill="{col}" fill-opacity="0.25"/>')
        parts.append(text(cx, top - 24, str(b), 14, TEXT, weight="bold"))
        parts.append(text(cx, low + 26, nm, 11, shade(col, 0.3), weight="bold"))
    parts.append(text(L + (x0 - L) / 2, top - 24, "idle", 12, MUTED, italic=True))
    parts.append(text(R - (x0 - L) / 2, top - 24, "idle", 12, MUTED, italic=True))
    us = 1e6 / BAUD
    parts.append(f'<path d="M{x0:.1f},{low + 50} l{bw:.1f},0" stroke="{MUTED}" stroke-width="2"/>')
    parts.append(text(x0 + bw / 2, low + 68, f"{us:.0f} µs", 12, MUTED))
    parts.append(text(w / 2, 365, f"least significant bit first: 1, 0, 0, 0, 0, 0, 1, 0 is 01000001 read backwards", 13, TEXT))
    parts.append(text(w / 2, 385, f"10 bits per character: {10 * us / 1000:.2f} ms each, {BAUD // 10} characters a second", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "The waveform of the letter A sent at 9600 baud. The line idles high at 5 volts, drops low for one start bit, then sends the eight data bits least significant first, 1, 0, 0, 0, 0, 0, 1, 0, which is binary 01000001 read backwards, then returns high for the stop bit. Each bit lasts 104 microseconds; the ten-bit character takes 1.04 milliseconds, so 960 characters fit in a second.")


# 2. Sampling at the right and wrong speeds -------------------------------------------------------
def sampling():
    w, h = 900, 560
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "The same A, read by receivers set to three speeds", 17, AMBER_LIGHT, weight="bold"))
    byte = ord("A")
    bits = frame(byte)
    L, R = 70, 830
    n = len(bits) + 2
    bw = (R - L) / n
    rows = [(9600, "receiver at 9600: samples land mid-bit", GREEN),
            (19200, "receiver at 19200: samples bunch up early", RED),
            (4800, "receiver at 4800: samples run past the end", RED)]
    for r, (rx, label, col) in enumerate(rows):
        top, low = 110 + r * 150, 160 + r * 150
        x0, _ = _wave(parts, L, R, top, low, bits, "#90cdf4")
        value, samples, stop_ok = receive(byte, BAUD, rx)
        for t in samples:
            x = x0 + t * BAUD * bw
            if x < R:
                parts.append(f'<line x1="{x:.1f}" y1="{top - 12}" x2="{x:.1f}" y2="{low + 12}" stroke="{col}" stroke-width="1.5" stroke-dasharray="3 3"/>')
                parts.append(f'<circle cx="{x:.1f}" cy="{top - 12}" r="5" fill="{col}"/>')
        ch = chr(value) if 32 <= value < 127 or value >= 160 else f"0x{value:02X}"
        result = f"reads {value:08b}"[::1]
        parts.append(text(L, top - 26, label, 12, shade(col, 0.3), "start", weight="bold"))
        verdict = f'"{ch}"' + ("" if stop_ok else ", no stop bit: framing error")
        parts += pill(R - 120, low + 32, f"gets {verdict}", col, size=12, h=26, wpx=300 if not stop_ok else 160)
    return svg(w, h, "\n".join(parts), "Three copies of the letter A sent at 9600 baud, each with the sample points of a receiver. A receiver at 9600 samples the middle of every bit and reads A. A receiver at 19200 samples twice as fast, bunched into the first half of the character, reads the byte 0x06 and finds no stop bit, a framing error. A receiver at 4800 samples half as fast, runs past the end of the character, and reads 0xFC, the character ü.")


# 3. Wiring: TX to RX ---------------------------------------------------------------------------------
def wiring():
    w, h = 900, 380
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Two wires and a ground: each TX talks to the other's RX", 17, AMBER_LIGHT, weight="bold"))
    for bx, name in [(90, "Device A"), (610, "Device B")]:
        parts += box3d(bx, 300, 200, 60, 180, "#2f855a")
        parts.append(text(bx + 100, 145, name, 16, "#ffffff", weight="bold"))
    pins_a = {"TX": 170, "RX": 220, "GND": 270}
    pins_b = {"RX": 170, "TX": 220, "GND": 270}
    for nm, y in pins_a.items():
        parts.append(text(270, y + 5, nm, 13, "#ffffff", "end", weight="bold"))
        parts.append(f'<circle cx="290" cy="{y}" r="6" fill="#e2e8f0"/>')
    for nm, y in pins_b.items():
        parts.append(text(630, y + 5, nm, 13, "#ffffff", "start", weight="bold"))
        parts.append(f'<circle cx="610" cy="{y}" r="6" fill="#e2e8f0"/>')
    parts.append(f'<path d="M296,170 L604,170" stroke="{AMBER_LIGHT}" stroke-width="4" marker-end="url(#arrow)"/>')
    parts.append(f'<path d="M604,220 L296,220" stroke="#90cdf4" stroke-width="4"/>')
    parts.append(f'<path d="M300,220 l16,-8 l0,16 z" fill="#90cdf4"/>')
    parts.append(f'<path d="M296,270 L604,270" stroke="{MUTED}" stroke-width="4"/>')
    parts.append(text(450, 160, "A's TX → B's RX", 13, AMBER_LIGHT, weight="bold"))
    parts.append(text(450, 210, "A's RX ← B's TX", 13, "#90cdf4", weight="bold"))
    parts.append(text(450, 296, "ground to ground: the reference both sides measure from", 12, TEXT))
    parts.append(text(w / 2, 345, "TX always connects to RX. Two TX pins wired together means two talkers and no listener.", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Two 3D boards, A and B. A's TX pin connects to B's RX, and B's TX pin connects to A's RX, so the two signal wires cross; a third wire joins their grounds, the reference both sides measure from.")


# 4. Voltage levels ------------------------------------------------------------------------------------
def levels():
    w, h = 900, 440
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Same idea, different voltages: check before connecting", 17, AMBER_LIGHT, weight="bold"))
    zero = 220
    scale = 9
    cases = [("5 V logic", "Arduino Uno", 5, 0, GREEN),
             ("3.3 V logic", "many sensors, ESP32", 3.3, 0, BLUE),
             ("RS-232", "old PC serial ports", 12, -12, RED)]
    parts.append(f'<line x1="70" y1="{zero}" x2="830" y2="{zero}" stroke="{MUTED}" stroke-width="1.5"/>')
    parts.append(text(62, zero + 4, "0 V", 11, MUTED, "end"))
    for k, (name, sub, hi, lo, col) in enumerate(cases):
        x = 130 + k * 250
        parts += box3d(x, zero, 70, 36, hi * scale, col)
        parts.append(text(x + 35, zero - hi * scale - 28, f"{hi:g} V", 14, TEXT, weight="bold"))
        if lo < 0:
            parts.append(f'<rect x="{x}" y="{zero}" width="70" height="{-lo * scale}" fill="{shade(col, -0.3)}"/>')
            parts.append(text(x + 35, zero - lo * scale + 20, f"{lo:g} V", 14, TEXT, weight="bold"))
        parts.append(text(x + 35, 398, name, 15, AMBER_LIGHT, weight="bold"))
        parts.append(text(x + 35, 416, sub, 12, MUTED, italic=True))
    parts.append(text(w / 2, 76, "RS-232 must never be wired straight to an Arduino pin", 13, RED, weight="bold"))
    return svg(w, h, "\n".join(parts), "Three 3D bars of serial signal voltages. 5 volt logic on an Arduino Uno swings from 0 to 5 volts. 3.3 volt logic on many sensors and the ESP32 swings from 0 to 3.3 volts. RS-232 on old PC serial ports swings to plus and minus 12 volts, and must never be wired straight to an Arduino pin.")


# 5. Throughput -----------------------------------------------------------------------------------------
def throughput():
    w, h = 900, 400
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    line = "Raw: 205, Volts: 1.00, Celsius: 50.00\r\n"
    nbytes = len(line)
    parts.append(text(w / 2, 48, f"Time to send one {nbytes}-character line from Reading an Analog Sensor", 17, AMBER_LIGHT, weight="bold"))
    base = 320
    rates = [9600, 57600, 115200]
    for k, b in enumerate(rates):
        ms = nbytes * 10 / b * 1000
        hgt = ms / 45 * 200
        x = 160 + k * 230
        col = AMBER if b == 9600 else GREEN
        parts += box3d(x, base, 90, 46, hgt, col)
        parts.append(text(x + 45 + 16, base - hgt - 26, f"{ms:.1f} ms", 15, TEXT, weight="bold"))
        parts.append(text(x + 45, base + 30, f"{b:,} baud", 15, TEXT, weight="bold"))
        parts.append(text(x + 45, base + 48, f"{b // 10:,} characters/s", 12, MUTED))
    parts.append(text(w / 2, 82, "10 bits per character (start, 8 data, stop)", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Three 3D bars of the time to send a 39-character line, including its line ending. At 9600 baud it takes 40.6 milliseconds; at 57600, 6.8; at 115200, 3.4.")


FIGURES = {"frame_a.svg": frame_a, "sampling.svg": sampling, "wiring.svg": wiring,
           "levels.svg": levels, "throughput.svg": throughput}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
