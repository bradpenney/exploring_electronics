#!/usr/bin/env python3
"""Figures for docs/i2c.md.

Sources:
- TI "Understanding the I2C Bus" (SLVA704): open-drain lines pulled up by
  resistors; START = SDA falls while SCL is high, STOP = SDA rises while SCL
  is high; data stable while SCL is high; most significant bit first; a ninth
  clock for ACK (receiver pulls SDA low) or NACK (SDA left high).
- Microchip MCP9808 datasheet: address 0011 A2 A1 A0 (0x18-0x1F); ambient
  temperature register 0x05, read as two bytes.
- ATmega328P datasheet, Two-wire Serial Bus Requirements: Rp min =
  (VCC - 0.4 V) / 3 mA; Rp max = 1000 ns / Cb at 100 kHz; Cb up to 400 pF.

Usage:
    python3 illustrations/i2c.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, box3d,  # noqa: E402
                     common_defs, panel, pill, render_all, shade, svg, text)
from ac_dc import glow_line  # noqa: E402

OUT = HERE.parent / "docs" / "images" / "i2c"
BLUE = "#4299e1"
ADDR = 0x18


# 1. Open drain: pull down, never push up ----------------------------------------------------------
def open_drain():
    w, h = 900, 400
    parts = [common_defs(), panel(15, 15, 425, h - 30), panel(460, 15, 425, h - 30)]
    for cx, title, pulled in [(227, "Everyone lets go: the line is HIGH", None), (672, "Anyone pulls down: the line is LOW", 1)]:
        parts.append(text(cx, 50, title, 15, AMBER_LIGHT, weight="bold"))
        line_y = 150
        lx0, lx1 = cx - 170, cx + 170
        col = GREEN if pulled is None else RED
        parts.append(f'<rect x="{lx0}" y="{line_y - 6}" width="{lx1 - lx0}" height="12" rx="6" fill="{col}"/>')
        parts.append(text(lx0, line_y - 14, "5 V" if pulled is None else "0 V", 13, col, "start", weight="bold"))
        # pull-up resistor to 5 V
        parts.append(f'<rect x="{cx - 160}" y="76" width="44" height="18" rx="8" fill="#d6b98c"/>')
        parts.append(f'<line x1="{cx - 138}" y1="94" x2="{cx - 138}" y2="{line_y - 6}" stroke="{TEXT}" stroke-width="3"/>')
        parts.append(f'<line x1="{cx - 116}" y1="85" x2="{cx - 90}" y2="85" stroke="{TEXT}" stroke-width="3"/>')
        parts.append(text(cx - 84, 90, "pull-up to 5 V", 12, MUTED, "start", italic=True))
        for k in range(3):
            x = cx - 70 + k * 100
            closed = pulled == k
            parts.append(f'<line x1="{x}" y1="{line_y + 6}" x2="{x}" y2="215" stroke="{TEXT}" stroke-width="3"/>')
            # switch to ground
            if closed:
                parts.append(f'<line x1="{x}" y1="215" x2="{x}" y2="255" stroke="{RED}" stroke-width="4"/>')
            else:
                parts.append(f'<line x1="{x}" y1="215" x2="{x + 22}" y2="248" stroke="{TEXT}" stroke-width="4"/>')
            parts.append(f'<circle cx="{x}" cy="215" r="5" fill="{TEXT}"/>')
            parts.append(f'<line x1="{x - 16}" y1="258" x2="{x + 16}" y2="258" stroke="{TEXT}" stroke-width="3"/>')
            parts.append(f'<line x1="{x - 10}" y1="265" x2="{x + 10}" y2="265" stroke="{TEXT}" stroke-width="3"/>')
            parts += box3d(x - 34, 330, 68, 26, 40, "#2f855a" if not closed else "#c53030", shadow=False)
            parts.append(text(x, 318, f"device {k + 1}", 11, "#ffffff", weight="bold"))
        sub = "no switch closed: the resistor lifts the line" if pulled is None else "one switch closed: the line goes to ground"
        parts.append(text(cx, 365, sub, 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Two panels of an open-drain line shared by three devices, each able only to connect the line to ground through a switch, with a pull-up resistor to 5 volts. Left: no switch closed, so the resistor lifts the line to 5 volts, HIGH. Right: device 2 closes its switch and the line goes to 0 volts, LOW. No device ever drives the line high, so two devices can never fight.")


# 2. The shared bus ------------------------------------------------------------------------------------
def bus():
    w, h = 900, 420
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "One controller, many targets, two shared wires", 17, AMBER_LIGHT, weight="bold"))
    sda_y, scl_y = 130, 170
    parts.append(f'<rect x="80" y="{sda_y - 5}" width="760" height="10" rx="5" fill="{AMBER}"/>')
    parts.append(f'<rect x="80" y="{scl_y - 5}" width="760" height="10" rx="5" fill="#90cdf4"/>')
    parts.append(text(848, sda_y + 5, "SDA", 13, AMBER_LIGHT, "start", weight="bold"))
    parts.append(text(848, scl_y + 5, "SCL", 13, "#90cdf4", "start", weight="bold"))
    nodes = [(150, "Arduino", "controller", "drives the clock", "#c05621"),
             (370, "MCP9808", "target 0x18", "A0 to ground", "#2f855a"),
             (560, "MCP9808", "target 0x19", "A0 to 5 V", "#2f855a"),
             (750, "MCP9808", "target 0x1A", "A1 to 5 V", "#2f855a")]
    for x, name, role, sub, col in nodes:
        for y in (sda_y, scl_y):
            parts.append(f'<circle cx="{x - 12 if y == sda_y else x + 12}" cy="{y}" r="6" fill="#e2e8f0"/>')
        parts.append(f'<line x1="{x - 12}" y1="{sda_y}" x2="{x - 12}" y2="250" stroke="{AMBER}" stroke-width="3"/>')
        parts.append(f'<line x1="{x + 12}" y1="{scl_y}" x2="{x + 12}" y2="250" stroke="#90cdf4" stroke-width="3"/>')
        parts += box3d(x - 60, 330, 120, 40, 80, col)
        parts.append(text(x, 285, name, 14, "#ffffff", weight="bold"))
        parts.append(text(x, 305, role, 12, "#ffffff"))
        parts.append(text(x + 10, 355, sub, 11, MUTED, italic=True))
    parts.append(text(w / 2, 390, "each target answers only to its own 7-bit address; up to eight MCP9808s fit on one bus", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "A two-wire bus, SDA and SCL, running the width of the figure. An Arduino, the controller that drives the clock, and three MCP9808 temperature sensors, targets at addresses 0x18, 0x19 and 0x1A set by their address pins, all connect to the same two wires. Each target answers only to its own 7-bit address, and up to eight MCP9808s fit on one bus.")


# 3. The address byte on the wires -------------------------------------------------------------------
def address_byte():
    w, h = 900, 430
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "START, then address 0x18 (0011000) and a write bit, then ACK", 17, AMBER_LIGHT, weight="bold"))
    bits = [(ADDR >> (6 - k)) & 1 for k in range(7)] + [0]
    L, R = 90, 840
    n = 12  # idle, start, 8 bits, ack, stop-ish
    cw = (R - L) / n
    scl_hi, scl_lo = 110, 160
    sda_hi, sda_lo = 230, 280
    parts.append(text(L - 10, (scl_hi + scl_lo) / 2 + 4, "SCL", 13, "#90cdf4", "end", weight="bold"))
    parts.append(text(L - 10, (sda_hi + sda_lo) / 2 + 4, "SDA", 13, AMBER_LIGHT, "end", weight="bold"))
    # SCL: high idle, high during start, then 9 pulses
    scl = [(L, scl_hi), (L + 1.75 * cw, scl_hi), (L + 1.75 * cw, scl_lo)]
    for k in range(9):
        x = L + (2 + k) * cw
        scl += [(x + 0.25 * cw, scl_lo), (x + 0.25 * cw, scl_hi), (x + 0.75 * cw, scl_hi), (x + 0.75 * cw, scl_lo)]
    scl += [(L + 11.25 * cw, scl_lo), (L + 11.25 * cw, scl_hi), (R, scl_hi)]
    parts.append(glow_line(scl, "#90cdf4", 3))
    # SDA
    def lv(b):
        return sda_hi if b else sda_lo
    sda = [(L, sda_hi), (L + 1.4 * cw, sda_hi), (L + 1.4 * cw, sda_lo)]
    seq = bits + [0]  # ACK pulled low by the target
    prev = 0
    for k, b in enumerate(seq):
        x = L + (2 + k) * cw
        sda += [(x, lv(prev)), (x, lv(b)), (x + cw, lv(b))]
        prev = b
    sda += [(L + 11 * cw, lv(0)), (L + 11.6 * cw, lv(0)), (L + 11.6 * cw, sda_hi), (R, sda_hi)]
    parts.append(glow_line(sda, AMBER_LIGHT, 3))
    labels = [f"{b}" for b in bits[:7]] + ["W"] + ["ACK"]
    for k, lab in enumerate(labels):
        x = L + (2.5 + k) * cw
        col = GREEN if lab == "ACK" else (RED if lab == "W" else TEXT)
        parts.append(text(x, sda_lo + 30, lab, 14, col, weight="bold"))
        sub = "target" if lab == "ACK" else ("write" if lab == "W" else f"bit {6 - k}")
        parts.append(text(x, sda_lo + 48, sub, 10, MUTED))
    parts.append(text(L + 1.4 * cw, scl_hi - 14, "START", 12, GREEN, weight="bold"))
    parts.append(text(L + 11.6 * cw, scl_hi - 14, "STOP", 12, RED, weight="bold"))
    parts.append(text(w / 2, 395, "SDA only changes while SCL is low; a change while SCL is high is START or STOP", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Two waveforms, SCL above SDA. While SCL is high, SDA falls: the START condition. Then SCL pulses nine times. During the first seven, SDA carries the address 0x18 most significant bit first, 0 0 1 1 0 0 0; the eighth is a 0 for write; on the ninth the target pulls SDA low to acknowledge. Finally SDA rises while SCL is high: STOP. SDA only changes while SCL is low, except at START and STOP.")


# 4. A whole read transaction ---------------------------------------------------------------------------
def transaction():
    w, h = 900, 330
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Reading the temperature: one transaction, thirteen pieces", 17, AMBER_LIGHT, weight="bold"))
    pieces = [("S", "c"), ("0x18 W", "c"), ("ACK", "t"), ("reg 0x05", "c"), ("ACK", "t"), ("Sr", "c"),
              ("0x18 R", "c"), ("ACK", "t"), ("upper", "t"), ("ACK", "c"), ("lower", "t"), ("NACK", "c"), ("P", "c")]
    widths = {"S": 34, "Sr": 34, "P": 34, "ACK": 44, "NACK": 50}
    total = sum(widths.get(p, 86) for p, _ in pieces) + 4 * (len(pieces) - 1)
    x = (w - total) / 2
    y = 160
    for name, who in pieces:
        pw = widths.get(name, 86)
        col = "#c05621" if who == "c" else "#2f855a"
        parts += box3d(x, y, pw, 18, 44, col, shadow=False)
        parts.append(text(x + pw / 2, y - 17, name, 12 if pw < 60 else 13, "#ffffff", weight="bold"))
        x += pw + 4
    parts.append(f'<rect x="250" y="210" width="18" height="18" rx="3" fill="#c05621"/>')
    parts.append(text(276, 224, "sent by the controller (Arduino)", 12, TEXT, "start"))
    parts.append(f'<rect x="530" y="210" width="18" height="18" rx="3" fill="#2f855a"/>')
    parts.append(text(556, 224, "sent by the target (MCP9808)", 12, TEXT, "start"))
    parts.append(text(w / 2, 262, "S = START, Sr = repeated START, P = STOP. Write the register number, then turn around and read two bytes.", 12, MUTED, italic=True))
    parts.append(text(w / 2, 282, "The final NACK tells the target the controller has all it wants.", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "A strip of thirteen blocks, coloured by who sends each. The controller sends START, address 0x18 with write, then register 0x05, each acknowledged by the target; then a repeated START and address 0x18 with read, acknowledged; then the target sends the upper byte, which the controller acknowledges, and the lower byte, which the controller answers with NACK before sending STOP.")


# 5. Choosing a pull-up ---------------------------------------------------------------------------------------
def pullup_range():
    w, h = 900, 430
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Choosing pull-ups at 100 kHz on a 5 V bus (ATmega328P limits)", 17, AMBER_LIGHT, weight="bold"))
    rmin = (5.0 - 0.4) / 0.003
    L, R = 120, 840
    xr = lambda r: L + r / 12000 * (R - L)
    for k, cb in enumerate((100e-12, 200e-12, 400e-12)):
        y = 140 + k * 80
        rmax = 1000e-9 / cb
        parts.append(f'<rect x="{L}" y="{y - 16}" width="{R - L}" height="32" rx="6" fill="#2d3748"/>')
        parts.append(f'<rect x="{xr(rmin):.1f}" y="{y - 16}" width="{xr(rmax) - xr(rmin):.1f}" height="32" rx="6" fill="{GREEN}" fill-opacity="0.75"/>')
        parts.append(f'<rect x="{xr(rmin):.1f}" y="{y - 16}" width="{xr(rmax) - xr(rmin):.1f}" height="32" rx="6" fill="url(#gloss)" opacity="0.5"/>')
        parts.append(text(L - 10, y + 5, f"{cb * 1e12:.0f} pF", 13, TEXT, "end", weight="bold"))
        parts.append(text(xr(rmax) + 8, y + 5, f"up to {rmax / 1000:.1f} kΩ", 13, GREEN, "start", weight="bold"))
    x47 = xr(4700)
    parts.append(f'<line x1="{x47:.1f}" y1="110" x2="{x47:.1f}" y2="330" stroke="{AMBER_LIGHT}" stroke-width="2" stroke-dasharray="6 4"/>')
    parts.append(text(x47, 104, "4.7 kΩ", 13, AMBER_LIGHT, weight="bold"))
    parts.append(f'<line x1="{xr(rmin):.1f}" y1="110" x2="{xr(rmin):.1f}" y2="330" stroke="{RED}" stroke-width="2"/>')
    parts.append(text(xr(rmin) - 6, 104, f"{rmin / 1000:.2f} kΩ min", 12, RED, "end", weight="bold"))
    for r in (0, 2000, 4000, 6000, 8000, 10000, 12000):
        parts.append(text(xr(r), 352, f"{r // 1000} kΩ", 11, MUTED))
    parts.append(text(w / 2, 376, "pull-up resistance; rows are the bus's total capacitance", 12, MUTED, italic=True))
    parts.append(text(w / 2, 398, "too small: devices can't pull the line low enough. Too large: the line rises too slowly.", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Three bars of allowed pull-up resistance on a 5 volt bus at 100 kilohertz, from the ATmega328P datasheet. The minimum for every row is 1.53 kilohms, set by the 3 milliamps a device can sink while holding the line below 0.4 volts. The maximum falls as the bus capacitance rises: 10 kilohms at 100 picofarads, 5 at 200, 2.5 at 400. A common 4.7 kilohm resistor sits inside the range for up to about 200 picofarads.")


FIGURES = {"open_drain.svg": open_drain, "bus.svg": bus, "address_byte.svg": address_byte,
           "transaction.svg": transaction, "pullup_range.svg": pullup_range}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
