---
date: "2026-10-04 15:00"
title: "Vacuum Tubes: Electrons Across Empty Space"
description: "How a vacuum tube works: a heated cathode, a positive plate, and a grid that controls the stream. Diodes and triodes, why tubes resemble FETs, and why they're still made."
---

# Vacuum Tubes

!!! abstract "Beginner"
    This article is in the **Components** topic. It builds on [Diodes and LEDs](diodes_and_leds.md) and [Transistors](transistors.md), especially the field-effect transistor. No other prior knowledge required.

The `12AX7` is a small glass tube that RCA released in 1947, the same year the transistor was invented. It's still in production. Before it amplifies anything, its heater draws 300 mA at 6.3 V, nearly 2 W spent just keeping it hot, and it wants up to 300 V on one of its electrodes. A transistor doing a similar job needs no heater, runs from a few volts, and costs a fraction as much. Yet new guitar amplifiers are still built around 12AX7s, and high-power radio transmitters still use tubes.

Two ideas explain how a tube works, and why it has outlived its replacement in a few places:

1. **Heat boils electrons off a metal surface, and a positive electrode collects them across a vacuum.** That alone makes a one-way valve for current: a diode, built from empty space instead of silicon.
2. **A wire mesh placed in the electrons' path controls the stream with voltage.** A small voltage on the mesh, the **grid**, controls a much larger current, which makes the tube an amplifier, and one that behaves very like a field-effect transistor.

The second half explains why anyone still chooses one.

---

## Inside a Tube

A vacuum tube is a set of metal electrodes sealed inside a glass (or metal) envelope with the air pumped out. The triode below is the classic arrangement, nested like the layers of an onion.

<figure markdown>
  ![A 3D triode inside a glass envelope with the air pumped out. In the centre, a glowing orange cathode sleeve with a heater inside it boils off electrons. Around it, a fine wire helix forms the grid. Outside that, two metal plate walls collect the electrons crossing the vacuum. Pins at the base connect the heater, cathode, grid and plate.](images/vacuum_tubes/anatomy.svg){ width="760" }
  <figcaption>From the centre outward: heater, cathode, grid, plate, and the vacuum around them all.</figcaption>
</figure>

- **The heater** is a filament, like a light bulb's, that heats the cathode. In older tubes and many power tubes the filament *is* the cathode (a **directly heated** cathode); most small tubes use a separate heater inside a cathode sleeve (**indirectly heated**).
- **The cathode** is the electrode that emits electrons. Wikipedia's article on [vacuum tubes](https://en.wikipedia.org/wiki/Vacuum_tube) gives oxide-coated cathodes a working temperature of about 700 °C, a dull red glow.
- **The grid** is a fine wire mesh or helix between cathode and plate, close to the cathode. It's the control electrode.
- **The plate**, also called the **anode**, surrounds the rest and collects the electrons. It runs at the highest positive voltage in the tube, typically hundreds of volts.
- **The envelope** holds a **vacuum**.

---

## Idea One: Electrons Boiled Into Empty Space

Metals are full of free electrons ([Conductors, Insulators, and Semiconductors](conductors_and_insulators.md) explains why), but at room temperature they can't escape the surface. Heat the metal enough and the fastest ones do, the way the fastest water molecules escape a pot as steam. That's **thermionic emission**, and Thomas Edison noticed its effect in 1883 while experimenting with light bulbs: current could flow across the vacuum from a hot filament to a separate metal plate, but only one way.

Once electrons have left the cathode, what happens next depends on the plate's voltage:

<figure markdown>
  ![Two panels of a vacuum diode. Left, with the plate positive, electrons boiled off the hot cathode cross the vacuum to the plate and current flows. Right, with the plate negative, the electrons are repelled and stay in a cloud near the cathode, and no current flows.](images/vacuum_tubes/diode_action.svg){ width="760" }
  <figcaption>The cathode can emit; the plate can't. That asymmetry is the whole diode.</figcaption>
</figure>

- **Plate positive:** it attracts the electrons, and they cross the gap. Current flows.
- **Plate negative:** it repels them, and they hang in a cloud near the cathode. No current flows.

The cold plate can't emit electrons of its own, so nothing can ever flow the other way. A two-electrode tube is a **diode**, exactly the one-way valve in [Diodes and LEDs](diodes_and_leds.md#idea-one-a-one-way-valve), with the same names for its ends: current enters at the anode (plate) and the cathode is where electrons come from. John Ambrose Fleming built the first practical one in 1904 to detect radio signals, and called it a valve, which is still the British name for a tube.

???+ info "Definition: Thermionic Emission"
    The release of electrons from a surface heated enough that some of its electrons have the energy to escape. It's why a tube needs a heater, and why it takes a few seconds to warm up before it works.

### Why the Vacuum

The electrons have to cross the gap without hitting anything. Air in the way would scatter them, and at the voltages tubes use, collisions knock electrons off gas molecules, ionizing the gas: Wikipedia notes that early tubes with leftover gas showed a blue glow once the plate voltage passed about 60 V. A hot filament in air also burns out, just as a light bulb's does. Pumping the envelope down to a hard vacuum solves both. That's what's inside: nothing.

---

## Idea Two: A Grid That Controls the Stream

In 1906, Lee de Forest added a third electrode between cathode and plate, a bent wire he called a grid, and patented the result as the **Audion** in January 1907 ([Triode](https://en.wikipedia.org/wiki/Triode) on Wikipedia). Three electrodes, one grid: a **triode**.

The grid sits much closer to the cathode than the plate does, so its voltage has an outsized effect on the electrons just leaving the cathode. Held slightly negative relative to the cathode, it repels some of them and lets the rest through its gaps to the plate. Make it more negative and fewer get through. Make it negative enough and none do: the tube is **cut off**.

<figure markdown>
  ![Three panels of a triode with the plate positive at the top, the hot cathode at the bottom, and a row of grid wires between. With the grid slightly negative, some electrons pass through the gaps to the plate. More negative, fewer pass. Far enough negative, none pass and the tube is cut off.](images/vacuum_tubes/grid_control.svg){ width="760" }
  <figcaption>The grid doesn't supply the current; it only decides how much of the cathode's stream reaches the plate.</figcaption>
</figure>

Two details make this an amplifier:

- **The output current flows between cathode and plate.** The grid only steers it. Because the grid is kept negative, it repels electrons rather than collecting them, so it draws almost no current itself.
- **A small grid voltage controls a large plate current.** A tube's **amplification factor**, written μ (the Greek letter mu), says how much more effective the grid is than the plate: a change of 1 V on the grid moves the plate current as much as a change of μ volts on the plate would. The 12AX7's is about 100 ([12AX7](https://en.wikipedia.org/wiki/12AX7) on Wikipedia).

Wire the plate to the high-voltage supply through a resistor and the changing plate current becomes a changing voltage across that resistor, a much bigger copy of the signal on the grid:

<figure markdown>
  ![Left, the schematic symbols for a vacuum diode and a triode, a circle containing a heater, a cathode, and a plate, with the triode adding a dashed grid between them. Right, a triode amplifier stage: the plate connects through a plate resistor to the high-voltage supply, labelled B-plus, hundreds of volts, and to the output; the grid connects to the input and through a grid resistor to ground; the cathode connects through a cathode resistor to ground.](images/schematics/triode_stage.svg){ width="620" }
  <figcaption>The dashed line is the grid. The supply is still called B+ from the days when it came from a "B" battery.</figcaption>
</figure>

### More Grids: Tetrodes and Pentodes

The triode's plate and grid sit close enough to act as a small [capacitor](capacitors.md), which limits how well it works at high frequencies. Adding a second grid, the **screen grid**, makes a four-electrode **tetrode**; a third, the **suppressor grid**, makes a five-electrode **pentode**. Each name counts the electrodes: cathode, plate, and one, two, or three grids. They're refinements of the triode's idea, not different ones.

---

## The Tube and the Transistor

[Transistors](transistors.md) do the same job as tubes with no heater and no vacuum, and they replaced tubes almost everywhere within a couple of decades of 1947. But one family is a close cousin.

<figure markdown>
  ![A comparison of a triode and a field-effect transistor. The cathode matches the source, which emits the carriers; the grid matches the gate, which controls by voltage; the plate matches the drain, which collects the output. Beneath the triode: its heater uses 1.9 watts before any signal, and its plate runs up to 300 volts. Beneath the FET: no heater, and logic-level parts run from a few volts.](images/vacuum_tubes/tube_vs_fet.svg){ width="760" }
  <figcaption>Same three roles, same control by voltage, very different power bills.</figcaption>
</figure>

A bipolar transistor is controlled by a current into its base. A triode is controlled by a voltage on its grid, which draws almost no current, and that's how a **field-effect transistor** works too. The match is closest with the junction FET from [Transistors](transistors.md#field-effect-transistors-controlled-by-voltage): its channel conducts with 0 V on the gate, and making the gate more negative pinches it off, exactly as a more negative grid cuts off a triode. Cathode, grid, and plate line up with source, gate, and drain.

Both tubes and transistors can amplify, and both can switch. What separates them is everything around the job: a tube needs heater power and a warm-up, high voltages, and a glass envelope that can break, and it wears out as its cathode loses the ability to emit. Wikipedia sums up the comparison: semiconductors are "smaller, safer, cooler, and more efficient, reliable, durable, and economical."

### Why Tubes Are Still Made

So why is the 12AX7 still in production? Because there are jobs a tube still does better, or that people prefer it for:

<div class="grid cards" markdown>

-   **High power at high frequency**

    ---

    **Why it matters:** a tube has no semiconductor junction to overheat or break down, and it handles high voltages and high power. Triodes are still used in high-power amplifiers for radio transmitters and in industrial radio-frequency heating ([Triode](https://en.wikipedia.org/wiki/Triode)).

-   **Guitar and hi-fi amplifiers**

    ---

    **Why it matters:** musicians and audiophiles prize how tube amplifiers sound, especially pushed hard. The 12AX7 stays in production mainly for guitar amplifiers' preamp stages ([12AX7](https://en.wikipedia.org/wiki/12AX7)).

-   **Microwave ovens**

    ---

    **Why it matters:** the magnetron that generates a microwave oven's power is a vacuum tube ([Vacuum tube](https://en.wikipedia.org/wiki/Vacuum_tube)), in nearly every kitchen.

-   **History, and old equipment**

    ---

    **Why it matters:** radios, televisions, and amplifiers from before the 1960s are tube equipment, and restoring them is a hobby of its own.

</div>

That's the opening puzzle solved: for small signals, a transistor wins on every count, but when the job is large power, or a particular sound, a tube can still be the right part.

<figure markdown>
  ![A timeline from 1880 to 1950. 1883, the Edison effect: current from a hot filament. 1904, the Fleming valve, the vacuum diode. 1907, de Forest's Audion triode patent. 1947, RCA releases the 12AX7, and Bell Labs demonstrates the first transistor in December.](images/vacuum_tubes/timeline.svg){ width="760" }
  <figcaption>Sixty-four years from Edison's curiosity to the transistor that replaced the tube.</figcaption>
</figure>

---

## Safety: Hundreds of Volts, and Heat

Tube equipment is the most dangerous kind most hobbyists will ever open, because of the voltages it needs to work.

!!! danger "Tube Equipment Holds Lethal Voltages"
    The plate supply in tube equipment is typically hundreds of volts, generated from mains, and the filter capacitors that smooth it can stay charged long after the power is switched off ([Capacitors](capacitors.md#safety-charge-outlasts-the-power) explains how much energy they hold). Never open a tube amplifier, radio, or television unless you've been trained to discharge and verify its supply safely. Unplugging it is not enough.

!!! warning "Tubes Are Hot"
    A working tube's glass gets hot enough to burn, and power tubes run hotter still. Let equipment cool before touching or removing tubes, and keep tubes clear of anything that can melt or catch fire.

---

## Practice

??? question "1. Which Electrode?"

    In a triode, which electrode emits electrons, which controls them, and which runs at the highest positive voltage?

    ??? tip "Solution"
        The **cathode** emits (once it's heated). The **grid** controls. The **plate** (anode) is the most positive, so it attracts the electrons.

??? question "2. Where the Output Flows"

    Which two electrodes of a triode carry its output current, and why doesn't the grid carry much of it?

    ??? tip "Solution"
        **The cathode and the plate**: electrons leave the cathode and arrive at the plate. The grid is held negative relative to the cathode, so it repels electrons rather than collecting them, and draws almost no current. It controls the stream without being part of it.

??? question "3. Why the Vacuum?"

    What's inside a tube's envelope, and what would go wrong if it were filled with air?

    ??? tip "Solution"
        **A vacuum.** Air would scatter the electrons, the plate voltage would ionize the gas, and the hot filament would burn out, as a light bulb's does in air.

??? question "4. Counting Electrodes"

    A tube has a cathode, one grid, and a plate. What's it called? What about one with three grids?

    ??? tip "Solution"
        A **triode** (three electrodes). With three grids it has five electrodes: a **pentode**. The names count the electrodes.

??? question "5. Its Closest Cousin"

    Which semiconductor device behaves most like a triode, and why?

    ??? tip "Solution"
        **A field-effect transistor**, especially a JFET. Both are controlled by a voltage on an electrode that draws almost no current (grid or gate), and in both, making that electrode more negative reduces the main current until it's cut off. A bipolar transistor, by contrast, is controlled by a current into its base.

??? question "6. Tube or Transistor?"

    Give one reason a designer might still choose a tube over a transistor, and two reasons not to.

    ??? tip "Solution"
        **For:** a tube can handle higher power and voltage, which is why the biggest radio transmitter amplifiers still use them (or, in audio, for its sound). **Against:** heater power wasted before any signal (nearly 2 W for a 12AX7), high supply voltages, warm-up time, fragility, and a limited life.

---

## Quick Recap

<div class="grid cards two-col" markdown>

-   **Thermionic emission**

    ---

    A heated cathode boils off electrons into the vacuum. That's why a tube needs a heater.

-   **The diode**

    ---

    Cathode and plate: electrons cross only when the plate is positive. A one-way valve.

-   **The grid controls**

    ---

    A slightly negative grid near the cathode sets how much of the stream reaches the plate. More negative, less current; far enough, cut off.

-   **Output between cathode and plate**

    ---

    The grid draws almost no current. A small grid voltage controls a large plate current.

-   **Names count electrodes**

    ---

    Diode two, triode three, tetrode four, pentode five.

-   **Like a FET**

    ---

    Cathode, grid, plate match source, gate, drain. Both are voltage-controlled.

-   **Why tubes survive**

    ---

    High power, high voltage, and a sound musicians like. Plus the magnetron in every microwave oven.

-   **Lethal voltages**

    ---

    Hundreds of volts, held by capacitors after switch-off. Don't open tube equipment untrained.

</div>

---

## What's Next

Back to silicon: a transistor's junctions shift their voltage by a couple of millivolts per degree, a nuisance in an amplifier and a gift for measuring heat. **[Temperature Sensors](temperature_sensors.md)** shows how an analog temperature chip turns exactly that behaviour into a clean 10 mV per °C.

---

## Further Reading

**Deep Dives**

- [Vacuum Tube — Wikipedia](https://en.wikipedia.org/wiki/Vacuum_tube) — thermionic emission, the Edison effect, Fleming's valve, cathode types, and where tubes are still used
- [Triode — Wikipedia](https://en.wikipedia.org/wiki/Triode) — de Forest's Audion, how the grid controls the plate current, and modern uses
- [12AX7 — Wikipedia](https://en.wikipedia.org/wiki/12AX7) — the heater, amplification factor, and ratings used in this article, and why it's still made

**Related Articles**

- [Diodes and LEDs](diodes_and_leds.md) — the semiconductor one-way valve
- [Transistors](transistors.md) — bipolar transistors and the FETs that most resemble a triode
- [Capacitors](capacitors.md) — the stored charge that makes tube equipment dangerous after switch-off
