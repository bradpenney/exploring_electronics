---
date: "2026-10-02 08:00"
title: "Magnetism and Electromagnetism: Fields, Poles, and Coils"
description: "How magnets work, why a current makes a magnetic field and a moving magnet makes a voltage, and how electromagnets, generators, and transformers use both."
---

# Magnetism and Electromagnetism

!!! abstract "Beginner"
    This article is in the **Circuit Foundations** topic. It builds on [Current](current.md) and [AC vs DC](ac_dc.md). No other prior knowledge required.

Wrap insulated wire around an ordinary steel nail, connect the two ends to a battery, and the nail picks up paper clips. Disconnect the battery and the clips drop. There's no magnet anywhere in the setup: just a nail, some wire, and a battery.

Two ideas explain where the magnet came from:

1. **Magnets surround themselves with a field.** It has a north pole and a south pole, it can be mapped with lines, and like poles repel while unlike poles attract.
2. **Electricity and magnetism are the same force.** A current makes a magnetic field, and a *changing* magnetic field makes a voltage. Those two facts run electromagnets, motors, generators, transformers, and, in the end, radio.

---

## One of Four Forces

Physics recognizes four fundamental forces: gravity, the strong and weak nuclear forces (which only act inside atoms), and **electromagnetism**. The attraction between electrons and the nucleus in [Conductors, Insulators, and Semiconductors](conductors_and_insulators.md#inside-the-atom) is electromagnetism, and so is the pull of a fridge magnet. They look like different forces, but they're two faces of one, and the second half of this article shows how they connect.

---

## Idea One: Magnets and Their Fields

The space around a magnet, where its force can be felt, is its **magnetic field**. The field can't be seen, but it can be mapped: iron filings sprinkled around a magnet line up into curves, and a small compass placed anywhere in the field points along them. Those curves are drawn as **field lines**.

<figure markdown>
  ![A 3D bar magnet, north end red and south end blue, with field lines leaving the north pole, curving around both sides, and entering the south pole; the lines crowd together near the poles where the field is strongest.](images/magnetism/bar_field.svg){ width="720" }
  <figcaption>Field lines leave the north pole and curve round to the south.</figcaption>
</figure>

Field lines follow a few rules:

- **They leave the north pole and enter the south pole** (outside the magnet), and run on through the magnet to form closed loops.
- **They never cross.**
- **They crowd together where the field is strong,** which is why a magnet is strongest at its poles.

Poles always come in pairs. Cut a bar magnet in half and you don't get a separate north and south: you get two smaller magnets, each with both poles.

### Like Poles Repel, Unlike Poles Attract

Bring two magnets together and their fields interact. A north pole facing a south pole pulls the magnets together; two of the same pole push them apart.

<figure markdown>
  ![Two pairs of bar magnets. Left: a north pole facing a south pole, with field lines running straight across the gap, pulling them together. Right: a south pole facing a south pole, with field lines bending away from each other, pushing them apart.](images/magnetism/poles.svg){ width="740" }
  <figcaption>Opposite poles attract; matching poles repel.</figcaption>
</figure>

That rule hides a twist. A compass needle is a small magnet, and the end marked N points north. Since unlike poles attract, the pole of the Earth near the geographic North Pole must be a magnetic *south* pole. The names are older than the physics.

### Kinds of Magnets

Magnets come in three broad kinds, defined by whether their magnetism lasts:

<div class="grid cards two-col" markdown>

-   :material-magnet: **Permanent magnets**

    ---

    Keep their magnetism indefinitely. **Ferrite** (ceramic) magnets are cheap and common in fridge magnets and loudspeakers; **alnico** (aluminium, nickel, cobalt) was common in older equipment; **neodymium** magnets are the strongest ordinary magnets made.

-   :material-nail: **Temporary magnets**

    ---

    Materials like soft iron and steel become magnetic while they sit in a field, then mostly lose it when the field is taken away. A nail stuck to a magnet can pick up a paper clip of its own.

-   :material-flash: **Electromagnets**

    ---

    A coil of wire carrying current, usually around an iron core. Their strength can be turned up, down, or off with the current. The second half of this article explains them.

</div>

### How Strong Is a Field?

Field strength is measured in **tesla** (T), a large unit: everyday fields are usually given in millitesla (mT) or microtesla (µT), using the prefixes from [Metric Prefixes and Units](metric_prefixes.md).

<figure markdown>
  ![A log scale of magnetic field strength from 10 microtesla to 10 tesla: Earth's field at 31 to 58 microtesla, a fridge magnet at 1 to 10 millitesla, a small neodymium magnet near 0.1 tesla, a loudspeaker's magnet gap at 1 to 2.4 tesla, and an MRI scanner at 1.5 to 7 tesla.](images/magnetism/field_scale.svg){ width="740" }
  <figcaption>From the Earth's gentle field to a hospital scanner, a range of about a hundred thousand times.</figcaption>
</figure>

---

## Idea Two: Electricity and Magnetism Are One Force

The connection between electricity and magnetism was found by accident. In 1820, the Danish physicist Hans Christian Ørsted noticed that a compass needle swung when he switched on a current in a nearby wire. A current makes a magnetic field.

### A Current Makes a Field

The field around a straight wire forms rings centred on the wire. Its direction follows the **right-hand rule**: point your right thumb along the conventional current ([Current](current.md#which-way-does-current-flow)), and your fingers curl the way the field circles.

<figure markdown>
  ![Left: a copper wire carrying current upward, surrounded by rings of magnetic field, with the right-hand rule: thumb along the current, fingers curling with the field. Right: the same wire wound into a coil, whose rings add into a field like a bar magnet's, with a north and a south end.](images/magnetism/wire_field.svg){ width="760" }
  <figcaption>One wire makes rings; a coil adds them into a bar magnet's field.</figcaption>
</figure>

One wire's field is weak, but winding the wire into a coil adds every turn's rings together, and the result is a field shaped exactly like a bar magnet's, with a north end and a south end. Put an iron core inside and the iron's own magnetism lines up with the coil's field and multiplies it many times over. That's an **electromagnet**, and it's the nail puzzle solved.

<figure markdown>
  ![A steel nail wrapped in copper wire, wired to a battery through a switch. With the switch closed, current flows, the nail becomes a magnet, and paper clips cling to its tip. With the switch open, no current flows and the clips fall away.](images/magnetism/nail_electromagnet.svg){ width="760" }
  <figcaption>The coil makes the field; the steel nail concentrates it; the switch turns it on and off.</figcaption>
</figure>

The magnet was the current all along. The coil of wire made a field the moment current flowed, the steel nail concentrated it, and opening the switch stopped the current and the field together. More turns, more current, or a better iron core all make an electromagnet stronger.

Electromagnets are everywhere a magnet needs to be switched:

- **Relays** use a small current in a coil to pull a switch closed, so a small signal can control a large load.
- **Motors** use electromagnets pushing against permanent magnets (or each other) to turn a shaft.
- **Loudspeakers** push a coil back and forth against a permanent magnet in time with the audio signal.

### A Changing Field Makes a Voltage

In 1831, Michael Faraday found the reverse: a magnetic field can push a current, but only when it's *changing*. Move a magnet into a coil and a meter connected to the coil swings. Hold the magnet still and the meter reads zero. Pull it out and the meter swings the other way. This is **electromagnetic induction**.

<figure markdown>
  ![Three scenes of a magnet and a coil connected to a meter. Moving the magnet into the coil swings the needle one way. Holding the magnet still gives no reading. Pulling it out swings the needle the other way.](images/magnetism/induction.svg){ width="760" }
  <figcaption>Motion, not presence: only a changing field induces a voltage.</figcaption>
</figure>

Induction is what makes a generator work. [AC vs DC](ac_dc.md#where-ac-comes-from-the-generator) showed a loop turning between magnet poles: the field through the loop keeps changing as it turns, so a voltage keeps being induced, first one way and then the other. That's alternating current.

### Transformers

Induction also lets two coils share energy without touching. Wind two coils on one iron core and feed AC into the first (the **primary**). Its constantly changing field circulates through the core and induces a voltage in the second coil (the **secondary**).

<figure markdown>
  ![A transformer: a square iron core with a primary coil of many turns on the left, fed 120 volts AC, and a secondary coil of one tenth as many turns on the right, delivering 12 volts AC. The changing field circulates through the core.](images/magnetism/transformer.svg){ width="720" }
  <figcaption>The voltage ratio follows the turns ratio.</figcaption>
</figure>

Every turn of each coil sees the same changing field, so the voltages are in the same ratio as the number of turns:

\[ \frac{V_{\text{secondary}}}{V_{\text{primary}}} = \frac{N_{\text{secondary}}}{N_{\text{primary}}} \]

A transformer with ten times as many turns on its primary steps 120 V down to 12 V. Turn it around and it steps voltage up instead, which is how the grid reaches the high voltages that [Ohm's Law and Power](ohms_law.md#why-power-lines-run-at-such-high-voltages) showed are needed for long lines. A steady DC current makes a steady field, which induces nothing, which is why transformers only work on AC.

<figure markdown>
  ![Schematic: a 120 volt AC source connected to a transformer's primary winding, drawn as a coil, with two parallel lines marking an iron core and a smaller secondary coil on the other side, labelled 10 to 1, feeding a 12 volt load resistor.](images/schematics/transformer_step_down.svg){ width="420" }
  <figcaption>A transformer in a schematic: two coils, with two straight lines between them for the iron core.</figcaption>
</figure>

### From Fields to Radio

A current makes a magnetic field; a changing magnetic field makes a voltage. In 1865, James Clerk Maxwell worked out that changing electric and magnetic fields can keep generating each other and travel through space on their own, at the speed of light. In 1887, Heinrich Hertz, the man the unit of frequency is named after, made and detected those waves in his laboratory. They're radio waves: electromagnetism set loose from the wire.

---

## Safety: Strong Magnets

Small, powerful magnets, like the neodymium magnets used in craft projects and magnet sets, are a real hazard around children.

!!! danger "Swallowed Magnets Are a Medical Emergency"
    Health Canada warns that swallowing small, powerful magnets can cause severe injury or death, with children under 10 most at risk. Two or more swallowed magnets can attract each other through the walls of the intestines and tear them. Keep loose small magnets away from children, and get medical help immediately if one may have been swallowed.

Larger neodymium magnets carry their own risks.

!!! warning "Pinches, Shards, and Electronics"
    Strong magnets snap together hard enough to pinch skin painfully and can shatter into sharp shards when they collide. Magnet suppliers also warn to keep them away from pacemakers and other implanted medical devices, and from the magnetic stripes on cards.

---

## Practice

??? question "1. Which Way?"

    A magnet's north pole is brought near another magnet's north pole. What happens?

    ??? tip "Solution"
        They **repel**. Like poles push apart; only unlike poles (north and south) attract.

??? question "2. Cutting a Magnet"

    A bar magnet is cut in half across its middle. How many poles does each half have?

    ??? tip "Solution"
        **Two.** Each half is a complete magnet with its own north and south pole; poles always come in pairs.

??? question "3. A Stronger Electromagnet"

    Name three ways to make the nail electromagnet stronger.

    ??? tip "Solution"
        Use **more turns** of wire, **more current** (within what the wire and battery can safely handle), and a **better iron core**. Each one increases the field.

??? question "4. Still Magnet"

    A strong magnet sits motionless inside a coil connected to a meter. What does the meter read, and why?

    ??? tip "Solution"
        **Zero.** Induction needs a *changing* field. A stationary magnet makes a steady field, which induces no voltage.

??? question "5. Turns Ratio"

    A transformer has 600 turns on its primary and 30 on its secondary. With 120 V AC on the primary, what's the secondary voltage?

    ??? tip "Solution"
        \( 120 \times 30 / 600 = 6\ \text{V} \) AC. The ratio is 20 : 1, so the voltage steps down twenty times.

??? question "6. Why Not DC?"

    Why won't a transformer step down the 12 V DC from a car battery?

    ??? tip "Solution"
        Steady DC makes a steady magnetic field in the core, and a steady field induces no voltage in the secondary. A transformer needs a changing current, which is why it works on AC.

---

## Quick Recap

<div class="grid cards two-col" markdown>

-   **Fields and poles**

    ---

    Field lines leave north and enter south, never cross, and crowd where the field is strong.

-   **Attract and repel**

    ---

    Unlike poles attract; like poles repel. Poles always come in pairs.

-   **Kinds of magnets**

    ---

    Permanent (ferrite, alnico, neodymium), temporary (soft iron), and electromagnets.

-   **Current makes a field**

    ---

    Ørsted, 1820. A coil with an iron core is an electromagnet.

-   **Changing field makes a voltage**

    ---

    Faraday, 1831. Induction runs generators and transformers.

-   **Transformers**

    ---

    Voltage ratio = turns ratio. AC only.

</div>

---

## What's Next

With electricity and magnetism joined, **[Series and Parallel Circuits](series_and_parallel.md)** returns to building real circuits from several components.

---

## Further Reading

**Reference**

- [Orders of Magnitude (Magnetic Field) — Wikipedia](https://en.wikipedia.org/wiki/Orders_of_magnitude_(magnetic_field)) — the field strengths used in this article
- [Magnet Safety — Health Canada](https://www.canada.ca/en/health-canada/services/toy-safety/magnets.html) — the risks of swallowed magnets

**Deep Dives**

- [Electromagnetic Induction — Wikipedia](https://en.wikipedia.org/wiki/Electromagnetic_induction) — Faraday's law and how generators and transformers use it
- [Transformer — Wikipedia](https://en.wikipedia.org/wiki/Transformer) — cores, windings, and the turns ratio

**Related Articles**

- [AC vs DC](ac_dc.md) — the generator that induction makes possible
- [Ohm's Law and Power](ohms_law.md) — why transformers step the grid up to high voltage
- [Current](current.md) — the conventional current direction the right-hand rule uses
