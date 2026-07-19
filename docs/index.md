---
date: "2026-05-10 21:41"
title: "Exploring Electronics"
description: "Electronics from first principles — voltage, current, resistance, and circuit design explained clearly. Real components, real numbers, no prior knowledge assumed."
---

<img src="images/exploring_electronics.png" alt="Exploring Electronics" class="img-responsive-right" width="300">

# Exploring Electronics

Electronics is everywhere. The question is whether you understand it or just work around it.

This site teaches electronics from first principles — not just how to follow a wiring diagram, but why circuits are designed the way they are. Every concept is explained directly, grounded in real components and real numbers, so you can read a datasheet, design a circuit, and understand what's actually happening when you power something up.

## Where Do You Start?

Articles are grouped into **topics** — the subjects of electronics, like circuit foundations and microcontrollers. Each article carries a difficulty tag (Beginner, Intermediate, Advanced) so you can gauge depth at a glance, but there's no paywall or tier to unlock — just start wherever your project and your questions are.

<div class="grid cards two-col" markdown>

-   :material-flag-checkered: **New to electronics?**

    ---

    Start at the very beginning — no prior knowledge assumed.

    [:octicons-arrow-right-24: Start with What Is Electricity?](what_is_electricity.md)

-   :material-tools: **Ready to build?**

    ---

    Pick up the physical tools alongside the Beginner articles whenever you're ready to wire something.

    [:octicons-arrow-right-24: Start with Breadboards](tools/breadboards.md)

</div>

---

## Topics

**Circuit Foundations**

- [What Is Electricity?](what_is_electricity.md) — Voltage, current, and resistance from first principles
- [Series and Parallel Circuits](series_and_parallel.md) — How components connect changes everything about how a circuit behaves

**Reading Circuits**

- [How to Read a Schematic](reading_schematics.md) — The symbols and rules for reading any circuit diagram

**Components**

- [Resistor Color Codes](resistor_color_codes.md) — Decode any resistor's value and tolerance from its painted bands
- [Temperature Sensors](temperature_sensors.md) — How thermistors, analog ICs, and digital sensors each turn heat into a voltage
- [Package Types](package_types.md) — Through-hole vs. surface-mount, and why every part on this site plugs into a breadboard

**Microcontrollers**

- [What Is an Arduino?](what_is_an_arduino.md) — The board itself, and how to read a sketch's `setup()`/`loop()` structure
- [Digital Pins](digital_io.md) — How a microcontroller drives an LED and reads a button, and why every pin needs a resistor
- [Blink an LED](blink_an_led.md) — Build a single-LED circuit and flash your first sketch, end to end
- [Pull-up and Pull-down Resistors](pull_resistors.md) — Why an unconnected input floats, and how a resistor gives it a reliable HIGH or LOW
- [Reading an Analog Sensor](analog_input.md) — Wire a temperature sensor to an Arduino and read a continuous value with the ADC
- [Building a Threshold Ladder](threshold_output.md) — Turn one sensor reading into staged, at-a-glance LED output

**Communication, Power** *(coming soon)*

---

## Practical Tools

The physical tools used throughout the site — read these as you need them.

- [Breadboards](tools/breadboards.md) — How breadboards work internally, and the wiring mistakes that stop every beginner's first circuit
- [arduino-cli](tools/arduino_cli.md) — Compile and upload Arduino sketches from the terminal, no IDE required

## Part of the BradPenney.io Network

This site is part of a family of progressive technical learning resources:

- [Exploring Linux](https://linux.bradpenney.io) — Linux for developers and platform engineers
- [Exploring Kubernetes](https://k8s.bradpenney.io) — Kubernetes from first deployment to production clusters
- [Exploring Python](https://python.bradpenney.io) — Python automation for platform engineers
- [Exploring Computer Science](https://cs.bradpenney.io) — CS theory for working engineers
