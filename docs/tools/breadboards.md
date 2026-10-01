---
date: "2026-05-25 21:19"
title: "Breadboards: Prototype Circuits Without Soldering"
description: "How breadboard holes connect internally, how to use the power rails, and the wiring mistakes that kill every beginner's first circuit before it even starts."
---

# Breadboards

!!! abstract "Practical Tools"
    This article is part of the **Practical Tools** section: foundational reading before building your first circuit. If voltage, current, and resistance are new to you, start with [What Is Electricity?](../what_is_electricity.md).

A new circuit rarely works on the first try. Without a breadboard, testing it means soldering components together, and solder is semi-permanent: get a connection wrong or choose the wrong resistor, and everything has to be desoldered to try again. It's slow, it stresses components, and it discourages experimenting.

A breadboard removes all of that. Push components into holes, connect them with jumper wires, and the circuit works, with no heat and no commitment. Pull everything out and the board resets. Every circuit on this site starts on one.

A full-size 830-point breadboard costs $5–15 and will last years. It's the first thing to buy alongside any microcontroller kit.

![A full-size solderless breadboard in portrait orientation. Power rails run along each long edge. The center gap divides the component area into two halves, with columns a–e on the left and columns f–j on the right.](../images/breadboard_full.svg){ .breadboard-crop }

<p style="text-align: center; font-size: 0.75rem; color: var(--md-default-fg-color--light);">A full-size breadboard. Partial image: Giacomo Alessandroni, <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>.</p>

---

## How the Holes Connect

Look at the component area in the image: the dense grid of holes between the power rails. It's divided into a left half (columns `a` through `e`) and a right half (columns `f` through `j`), separated by the channel running down the middle. Rows are numbered starting from 1.

The internal connection pattern:

``` text title="Breadboard connections, rows 1 to 3"
  + -       a    b    c    d    e       f    g    h    i    j    - +
  o o   1  [o]--[o]--[o]--[o]--[o]  |  [o]--[o]--[o]--[o]--[o]   o o
  o o   2  [o]--[o]--[o]--[o]--[o]  |  [o]--[o]--[o]--[o]--[o]   o o
  o o   3  [o]--[o]--[o]--[o]--[o]  |  [o]--[o]--[o]--[o]--[o]   o o
```

`--` marks connected holes. `|` is the centre gap, where nothing connects.

Inside the board, each row of five holds a metal clip. Anything inserted into `a5`, `b5`, `c5`, `d5`, or `e5` touches the same clip, so they're all one electrical **node**. `f5` through `j5` are a separate clip on the other side of the gap.

The center gap is designed for components that intentionally span it. Integrated circuits (ICs), small chips with a row of pins on each side, are the most common example: one row lands in columns `a–e`, the other in columns `f–j`, keeping both sides electrically separate. Tactile switches are designed the same way. So the rule is to know whether a component is meant to span the gap.

---

## Power Rails

The red and blue strips along each long edge are the power rails. Unlike the component rows, they run the length of the board:

- **`+` rail** (red stripe): the supply voltage, whether 3.3V, 5V, or whatever the circuit needs
- **`−` rail** (blue stripe): ground, 0V reference

Connect power once to the rails, then use short jumper wires to bring it into the component area wherever you need it.

!!! warning "The Rail Break"
    Many breadboards, especially full-size 830-point boards, have a **break in the middle of each power rail**, often marked by a gap in the red and blue lines. The two halves are **not connected**. A multimeter in continuity mode settles it: probe from one end of the `+` rail to the other, and no beep means a break ([Open Circuits, Short Circuits, and Fuses](../open_short_fuses.md#continuity-testing-for-a-complete-path) explains the continuity test).

    If your circuit spans the full board, bridge the gap with a short jumper. Miss this and that half of the rail won't have power, and nothing connected to it will work.

---

## A Circuit on a Breadboard

Here's a real circuit on a breadboard: an Arduino powering components through the power rails, with jumper wires routing signals into the component area. This is the parallel switch circuit from [Series and Parallel Circuits](../series_and_parallel.md).

<figure markdown>
  ![An Arduino Uno connected to a half-size breadboard with two tactile buttons, a resistor, and an LED wired in parallel, showing power rails, jumper wires, and component placement.](../images/parallel_circuit.jpg){ style="width: 60%;" }
  <figcaption>A real breadboard circuit: jumper wires carry power and ground from the Arduino into the rails, and each component occupies its own rows.</figcaption>
</figure>

Notice the jumper wires carrying power and ground from the Arduino into the rails, and how each component occupies its own rows. Components sharing a row are electrically connected through the clip inside the board, with no wires needed between them.

---

## Common Mistakes

??? warning "Bridging the center gap with a component"

    There's no connection across the channel. ICs and tactile switches are designed to span it; a resistor or LED usually isn't. An LED with one leg on each side lands in two separate nodes, so it isn't connected to anything else in either row the way you meant.

??? warning "Off-by-one row"

    Row 10 and row 11 look identical. Miscounting by one row creates a broken circuit or an accidental short. Count carefully. On large circuits, different-coloured jumper wires help track what connects to what.

??? warning "Ignoring the rail break"

    The most common reason a circuit works on one half of the board but not the other. Test your rails once in continuity mode before trusting them.

??? warning "Partially seated components"

    A leg pushed in at an angle may not be making contact with the internal clip. Push straight down until it stops. Intermittent connections, working when you press on them and failing when you don't, are almost always a seating problem.

??? warning "Running out of row space"

    Each row has five holes. When a row fills up, bridge to an adjacent empty row with a short jumper. Don't force two legs into one hole: it spreads the clip and damages the board permanently.

---

## Practice

??? question "Which holes are connected?"

    On a standard breadboard, which of these pairs share an electrical connection?

    - `a5` and `e5`
    - `a5` and `a6`
    - `f5` and `j5`
    - `a5` and `f5`

    ??? tip "Solution"

        - ✅ `a5` and `e5`: same row, same side of the gap
        - ❌ `a5` and `a6`: same column letter, different rows; columns don't connect
        - ✅ `f5` and `j5`: same row, same side of the gap
        - ❌ `a5` and `f5`: same row number, opposite sides of the centre gap

??? question "Find the mistake"

    A circuit isn't working. Tracing the wiring: the LED's anode is in `e10`, its cathode is in `f10`, and a resistor runs from `a10` to the `+` rail. What's wrong?

    ??? tip "Solution"

        The LED straddles the center gap. `e10` and `f10` are on opposite sides, and the gap between columns `e` and `f` breaks the row. Both LED legs need to land on the same side of the gap. Move the LED so both legs are in `a10`–`e10` or `f10`–`j10`, then connect to the other side with a jumper if the circuit requires it.

??? question "Rail break diagnosis"

    Components on one half of your board work; the other half is dead. Power and ground are confirmed good on the working side. What's the most likely cause, and how do you fix it?

    ??? tip "Solution"

        The power rail break. Many full-size breadboards have a gap midway along each rail, and the two halves are not connected. Check continuity along both the `+` and `−` rails with a multimeter in continuity mode. If either doesn't beep end-to-end, bridge the gap with a short jumper wire connecting the two halves.

---

## Quick Recap

<div class="grid cards two-col" markdown>

-   **Component Rows**

    ---

    Holes `a–e` in a row are connected. Holes `f–j` in the same row are a separate node. The center gap separates the two halves.

-   **Power Rails**

    ---

    Red `+` and blue `−` strips run the length of the board. Watch for a break in the middle, and bridge it with a jumper if your circuit spans both halves.

-   **Center Gap**

    ---

    Deliberate: it's there for components designed to span it, like DIP-package ICs and tactile switches. The question is whether your component is meant to bridge it.

-   **No Commitment**

    ---

    Pull everything out and start over. Breadboards are for prototyping. Once a circuit works, move to something permanent.

</div>

---

## What's Next

The breadboard appears in every circuit on this site. The next step is putting it to work: **[Series and Parallel Circuits](../series_and_parallel.md)** builds two wiring patterns on this exact board, and explains why the difference matters for every circuit you'll design.

---

## Further Reading

**Visual Guides**

- [How to Use a Breadboard — SparkFun](https://learn.sparkfun.com/tutorials/how-to-use-a-breadboard) — photos and diagrams showing the internal clip structure
- [Breadboards for Beginners — Adafruit](https://learn.adafruit.com/breadboards-for-beginners) — wire management tips for keeping circuits readable as they grow

**Related Articles**

- [What Is Electricity?](../what_is_electricity.md) — voltage, current, and resistance: the theory behind every circuit you'll build on a breadboard
- [Series and Parallel Circuits](../series_and_parallel.md) — the two wiring configurations demonstrated on the breadboard in this article
- [How to Read a Schematic](../reading_schematics.md) — read the circuit diagram first, then build it on the board
- [Resistor Color Codes](../resistor_color_codes.md) — identify the right resistor by its bands before it goes in the board
- [What Is an Arduino?](../what_is_an_arduino.md) — the board pictured throughout this article, and what's actually on it
- [Digital Pins](../digital_io.md) — the button-and-LED circuit this board is built for, and what a microcontroller does with it
- [arduino-cli](arduino_cli.md) — once the circuit is built, compile and upload the code that brings it to life

