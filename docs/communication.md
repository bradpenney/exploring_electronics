---
date: "2026-10-04 23:30"
title: "Communication: How Boards and Sensors Talk"
description: "The Communication articles in reading order: serial between two devices, the I²C bus for many sensors on two wires, and fast SPI with a wire per device."
---

# Communication

A microcontroller rarely works alone. It reports to a computer, reads sensors that do their own measuring, and drives displays, all by sending bits one at a time down a wire or two. This topic covers how those conversations work at the level of the voltages on the wires, and how to wire and code them on an Arduino.

The articles assume [Digital Pins](digital_io.md) and the serial monitor from [arduino-cli](tools/arduino_cli.md).

<figure class="transit-map">
--8<-- "docs/images/landing/communication.svg"
<figcaption>The reading order as one line. Every stop is a link.</figcaption>
</figure>

---

## 1. Point to Point

- **[Serial Communication](serial_communication.md)** — one bit at a time with no clock, only an agreed baud rate; framing, wiring TX to RX, and voltage levels

## 2. Shared Buses

- **[I²C](i2c.md)** — many devices on two wires: open-drain lines and pull-ups, a clock, addresses, and reading an MCP9808 sensor
- **[SPI](spi.md)** — fast, full-duplex transfers with a chip-select wire per device, clock modes, and reading an MCP3008 converter

---

## Where to Start

Start with **[Serial Communication](serial_communication.md)**: it's what the serial monitor already uses, and I²C and SPI are easiest to understand as two different answers to serial's limits.
