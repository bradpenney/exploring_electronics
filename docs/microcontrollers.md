---
date: "2026-10-02 23:00"
title: "Microcontrollers: Making an Arduino Sense and React"
description: "The Microcontrollers articles in reading order: the Arduino board and its code, digital pins, blinking an LED, reading buttons and analog sensors, and staged output."
---

# Microcontrollers

A microcontroller is a tiny computer that runs one program and connects straight to circuits through its pins. This topic uses an Arduino Uno to go from an empty board to a project that measures temperature and shows the result on a row of LEDs.

The articles assume the basics of voltage, current, and resistance from [Circuit Foundations](circuit_foundations.md), and no coding background: the code is introduced a line at a time.

<figure class="transit-map">
--8<-- "docs/images/landing/microcontrollers.svg"
<figcaption>The reading order as one line, from an empty board to a working project. Every stop is a link.</figcaption>
</figure>

---

## 1. Meet the Board

- **[What Is an Arduino?](what_is_an_arduino.md)** — what's on the board, what a microcontroller is, and how to read your first sketch
- **[Digital Pins](digital_io.md)** — how a pin drives an LED and reads a button, and why each pin needs a resistor

## 2. Outputs and Inputs

- **[Blink an LED](blink_an_led.md)** — your first complete build, from wiring to code running on the chip
- **[Pull-up and Pull-down Resistors](pull_resistors.md)** — giving an input a steady resting state so a button reads reliably

## 3. Measuring the World

- **[Reading an Analog Sensor](analog_input.md)** — measuring a voltage between the extremes, with a temperature sensor and `analogRead()`
- **[Building a Threshold Ladder](threshold_output.md)** — turning one reading into staged, at-a-glance LED output

---

## What You'll Need

An Arduino Uno (or a compatible board) and its USB cable, a [breadboard](tools/breadboards.md), a few LEDs, resistors, and pushbuttons from any starter kit, and [arduino-cli](tools/arduino_cli.md) to load the code.

## Where to Start

Start with **[What Is an Arduino?](what_is_an_arduino.md)**. If you want something running in the next ten minutes, jump to **[Blink an LED](blink_an_led.md)** and come back for the why.
