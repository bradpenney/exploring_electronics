#!/usr/bin/env python3
"""Figures for docs/spi.md.

Sources:
- Wikipedia "Serial Peripheral Interface": Motorola, early 1980s; full duplex;
  SCLK, COPI (MOSI), CIPO (MISO), CS (SS, active low); the two shift
  registers form a ring; no acknowledgement; unselected peripherals must
  tri-state CIPO; modes from clock polarity (CPOL) and phase (CPHA).
- Arduino SPI reference: Uno pins 10 (CS), 11 (COPI), 12 (CIPO), 13 (SCK);
  SPISettings(speed, MSBFIRST, SPI_MODE0..3).
- Microchip MCP3008 datasheet: SPI modes 0,0 and 1,1; mode 0,0 idles the clock
  low and the controller latches data on rising edges; max clock 3.6 MHz at
  5 V; three-byte exchange (seven leading zeros, start bit, single-ended +
  channel bits, then a null bit and the 10-bit result); code = 1024 Vin / Vref.
- ATmega328P datasheet: SPI SCK up to fosc/2 = 8 MHz on a 16 MHz Uno.
- I2C 100/400 kbit/s (Wire.setClock reference).

Usage:
    python3 illustrations/spi.py
"""

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, box3d,  # noqa: E402
                     common_defs, panel, pill, render_all, shade, svg, text)
from ac_dc import glow_line  # noqa: E402

OUT = HERE.parent / "docs" / "images" / "spi"
BLUE = "#4299e1"


def _register(parts, x, y, bits, col, cell=34):
    for k, b in enumerate(bits):
        parts.append(f'<rect x="{x + k * cell}" y="{y}" width="{cell - 4}" height="34" rx="5" fill="{col}"/>')
        parts.append(f'<rect x="{x + k * cell}" y="{y}" width="{cell - 4}" height="34" rx="5" fill="url(#gloss)" opacity="0.4"/>')
        parts.append(text(x + k * cell + (cell - 4) / 2, y + 23, str(b), 15, "#ffffff", weight="bold"))


# 1. Two shift registers in a ring ----------------------------------------------------------------
def ring():
    w, h = 900, 470
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Every SPI transfer is a swap: eight clocks, eight bits each way", 17, AMBER_LIGHT, weight="bold"))
    c_bits, p_bits = "10110010", "01101100"
    for row, (label, cbits, pbits) in enumerate([("before", c_bits, p_bits), ("after 8 clocks", p_bits, c_bits)]):
        y = 110 + row * 170
        parts.append(text(70, y + 23, label, 13, MUTED, "start", italic=True))
        parts.append(text(330, y - 10, "controller (Arduino)", 13, "#f6ad55", weight="bold"))
        _register(parts, 195, y, cbits, "#c05621")
        parts.append(text(640, y - 10, "peripheral", 13, "#9ae6b4", weight="bold"))
        _register(parts, 505, y, pbits, "#2f855a")
        if row == 0:
            parts.append(f'<path d="M467,{y + 10} L500,{y + 10}" stroke="{AMBER_LIGHT}" stroke-width="3" marker-end="url(#arrow)"/>')
            parts.append(text(484, y - 2, "COPI", 11, AMBER_LIGHT, weight="bold"))
            parts.append(f'<path d="M780,{y + 17} C840,{y + 17} 840,{y + 80} 740,{y + 80} L230,{y + 80} C150,{y + 80} 150,{y + 17} 190,{y + 17}" stroke="#90cdf4" stroke-width="3" fill="none" marker-end="url(#arrow)"/>')
            parts.append(text(480, y + 98, "CIPO: the peripheral's bits come back round, one per clock", 12, "#90cdf4", weight="bold"))
    parts.append(text(w / 2, 432, "To read a byte, the controller must send one, even if it's only zeros.", 13, TEXT))
    return svg(w, h, "\n".join(parts), "Two 8-bit shift registers, the controller's and the peripheral's, joined in a ring: the controller's bits leave on COPI into the peripheral while the peripheral's bits leave on CIPO back to the controller, one bit each way per clock. Before: the controller holds 10110010 and the peripheral 01101100. After eight clocks they have swapped. To read a byte, the controller must send one.")


# 2. The bus with chip selects -----------------------------------------------------------------------
def bus():
    w, h = 900, 440
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Shared clock and data lines, and one select wire per peripheral", 17, AMBER_LIGHT, weight="bold"))
    lines = [("SCK", 110, "#90cdf4"), ("COPI", 140, AMBER), ("CIPO", 170, GREEN)]
    for name, y, col in lines:
        parts.append(f'<rect x="200" y="{y - 4}" width="640" height="8" rx="4" fill="{col}"/>')
        parts.append(text(848, y + 5, name, 12, col, "start", weight="bold"))
    parts += box3d(40, 360, 140, 40, 200, "#c05621")
    parts.append(text(110, 190, "Arduino", 15, "#ffffff", weight="bold"))
    parts.append(text(110, 210, "controller", 12, "#ffffff"))
    for name, y, col in lines:
        parts.append(f'<line x1="180" y1="{y}" x2="200" y2="{y}" stroke="{col}" stroke-width="4"/>')
    peris = [(330, "ADC", True), (530, "SD card", False), (730, "display", False)]
    for k, (x, name, sel) in enumerate(peris):
        col = "#2f855a" if sel else "#4a5568"
        for j, (_, y, lc) in enumerate(lines):
            parts.append(f'<line x1="{x - 20 + j * 20}" y1="{y}" x2="{x - 20 + j * 20}" y2="270" stroke="{lc}" stroke-width="3" stroke-opacity="{1 if sel or j < 2 else 0.35}"/>')
        parts += box3d(x - 60, 360, 120, 36, 90, col)
        parts.append(text(x, 305, name, 14, "#ffffff", weight="bold"))
        parts.append(text(x, 325, "selected" if sel else "CIPO let go", 11, "#ffffff"))
        # chip-select wire from the controller
        cy = 230 + k * 12
        cs_col = RED if sel else MUTED
        parts.append(f'<path d="M180,{cy} L{x + 40},{cy} L{x + 40},270" stroke="{cs_col}" stroke-width="2.5" fill="none" stroke-dasharray="{"0" if sel else "5 4"}"/>')
        parts.append(text(x + 46, cy - 4, f"CS{k + 1} {'LOW' if sel else 'HIGH'}", 10, cs_col, "start", weight="bold"))
    parts.append(text(w / 2, 400, "Only the peripheral whose CS is LOW listens and drives CIPO; the others ignore the clock.", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "An Arduino controller with three shared lines, SCK, COPI and CIPO, running to three peripherals: an ADC, an SD card and a display. Each peripheral also has its own chip-select wire from the Arduino. The ADC's CS is LOW, so it is selected and drives CIPO; the SD card's and display's CS lines are HIGH, so they let go of CIPO and ignore the clock.")


# 3. The four modes ------------------------------------------------------------------------------------
def modes():
    w, h = 900, 470
    parts = [common_defs()]
    cases = [(0, 0, 0, "rising"), (1, 0, 1, "falling"), (2, 1, 0, "falling"), (3, 1, 1, "rising")]
    for k, (mode, cpol, cpha, edge) in enumerate(cases):
        x0 = 15 + (k % 2) * 440
        y0 = 15 + (k // 2) * 225
        parts.append(panel(x0, y0, 425, 210))
        parts.append(text(x0 + 212, y0 + 32, f"Mode {mode}: CPOL {cpol}, CPHA {cpha}", 15, AMBER_LIGHT, weight="bold"))
        parts.append(text(x0 + 212, y0 + 52, f"clock idles {'HIGH' if cpol else 'LOW'}; data sampled on the {edge} edge", 12, MUTED, italic=True))
        L, R = x0 + 40, x0 + 390
        hi, lo = y0 + 85, y0 + 135
        idle = hi if cpol else lo
        act = lo if cpol else hi
        pts = [(L, idle), (L + 40, idle)]
        period = 70
        for p in range(4):
            x = L + 40 + p * period
            pts += [(x, idle), (x, act), (x + period / 2, act), (x + period / 2, idle)]
        pts += [(L + 40 + 4 * period, idle), (R, idle)]
        parts.append(glow_line(pts, "#90cdf4", 3))
        for p in range(4):
            x = L + 40 + p * period
            first = x
            second = x + period / 2
            ex = first if cpha == 0 else second
            parts.append(f'<circle cx="{ex}" cy="{(hi + lo) / 2}" r="7" fill="{GREEN}"/>')
            parts.append(f'<line x1="{ex}" y1="{hi - 8}" x2="{ex}" y2="{lo + 8}" stroke="{GREEN}" stroke-width="1.5" stroke-dasharray="3 3"/>')
        parts.append(text(x0 + 212, y0 + 168, "green: the moment both sides read a bit", 11, GREEN))
        if mode == 0:
            parts += pill(x0 + 212, y0 + 192, "MCP3008 uses mode 0 (or 3)", GREEN, size=11, h=24)
        if mode == 3:
            parts += pill(x0 + 212, y0 + 192, "MCP3008 also supports this", GREEN, size=11, h=24)
    return svg(w, h, "\n".join(parts), "Four panels of an SPI clock. Mode 0: clock polarity 0, phase 0, the clock idles low and data is sampled on each rising edge. Mode 1: idles low, sampled on falling edges. Mode 2: idles high, sampled on falling edges. Mode 3: idles high, sampled on rising edges. The MCP3008 supports modes 0 and 3.")


# 4. The MCP3008 exchange ---------------------------------------------------------------------------------
def exchange():
    w, h = 900, 400
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Reading channel 0 of an MCP3008: three bytes out, three bytes back", 17, AMBER_LIGHT, weight="bold"))
    code = 512
    sent = ["00000001", "1000????", "????????"]
    recv = ["????????", f"?????0{code >> 8 & 3:02b}", f"{code & 0xFF:08b}"]
    cell = 22
    for row, (label, data, col, y) in enumerate([("controller sends (COPI)", sent, "#c05621", 130),
                                                  ("MCP3008 sends (CIPO)", recv, "#2f855a", 240)]):
        parts.append(text(60, y - 36, label, 13, "#f6ad55" if row == 0 else "#9ae6b4", "start", weight="bold"))
        for b, byte in enumerate(data):
            bx = 60 + b * (8 * cell + 70)
            for k, ch in enumerate(byte):
                fill = col if ch != "?" else "#4a5568"
                parts.append(f'<rect x="{bx + k * cell}" y="{y}" width="{cell - 3}" height="30" rx="4" fill="{fill}"/>')
                parts.append(text(bx + k * cell + (cell - 3) / 2, y + 21, "x" if ch == "?" else ch, 13, "#ffffff", weight="bold"))
            parts.append(text(bx + 4 * cell, y + 52, f"byte {b + 1}", 11, MUTED))
    notes = [(60 + 7 * 22, 118, "start bit", "#f6ad55"),
             (60 + (8 * 22 + 70) + 0 * 22, 118, "single-ended", "#f6ad55"),
             (60 + (8 * 22 + 70) + 2 * 22, 104, "channel 000", "#f6ad55"),
             (60 + (8 * 22 + 70) + 5 * 22, 308, "null bit", "#9ae6b4"),
             (60 + (8 * 22 + 70) + 7 * 22, 324, "result bits 9-8", "#9ae6b4"),
             (60 + 2 * (8 * 22 + 70) + 4 * 22, 308, "result bits 7-0", "#9ae6b4")]
    for x, y, lab, col in notes:
        parts.append(text(x + 10, y, lab, 11, col, weight="bold"))
    parts.append(text(w / 2, 360, f"x = don't care. With 2.50 V on a 5 V reference, code = 1024 × 2.5 ÷ 5 = {code}: binary 10 0000 0000.", 13, TEXT))
    return svg(w, h, "\n".join(parts), "Two rows of three bytes. The controller sends 00000001, a start bit after seven zeros; then 1000 followed by don't-care bits, meaning single-ended channel 0; then a don't-care byte. At the same time the MCP3008 sends back a don't-care byte; then a null bit and result bits 9 and 8; then result bits 7 to 0. With 2.5 volts on a 5 volt reference the result is 512, binary 10 0000 0000.")


# 5. Speed and wires compared ---------------------------------------------------------------------------------
def compare():
    w, h = 900, 420
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Three ways to talk, on an Uno", 17, AMBER_LIGHT, weight="bold"))
    rows = [("Serial", "115,200 baud", 115200, "2 wires, 2 devices", AMBER),
            ("I²C fast mode", "400 kbit/s", 400000, "2 wires, many devices", "#38b2ac"),
            ("SPI, MCP3008 limit", "3.6 MHz", 3.6e6, "3 wires + 1 per device", GREEN),
            ("SPI, Uno's limit", "8 MHz", 8e6, "", GREEN)]
    base = 330
    for k, (name, lab, rate, wires, col) in enumerate(rows):
        x = 110 + k * 190
        hgt = (math.log10(rate) - 4.5) / (7 - 4.5) * 220
        parts += box3d(x, base, 90, 40, hgt, col)
        parts.append(text(x + 60, base - hgt - 26, lab, 14, TEXT, weight="bold"))
        parts.append(text(x + 45, base + 28, name, 13, TEXT, weight="bold"))
        if wires:
            parts.append(text(x + 45, base + 46, wires, 11, MUTED, italic=True))
    parts.append(text(w / 2, 82, "top speed, log scale", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Four 3D bars of top speed on a log scale for an Arduino Uno. Serial at 115,200 baud on two wires between two devices. I2C fast mode at 400 kilobits per second on two wires shared by many devices. SPI at the MCP3008's 3.6 megahertz limit and the Uno's own 8 megahertz limit, on three shared wires plus one select wire per device.")


FIGURES = {"ring.svg": ring, "bus.svg": bus, "modes.svg": modes, "exchange.svg": exchange, "compare.svg": compare}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
