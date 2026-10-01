# Coverage map: AVARC Basic course, Chapter 2 "Basic Electricity"

Source: Annapolis Valley Amateur Radio Club online Basic course, Chapter 2
(Al Penney, VO1NO), 168 slides incl. 40 review questions:
https://avarc.ca/wp-content/uploads/online-basic-course/Ch2-Basic-Electricity.pdf
(read 2026-10-01; slide numbers below refer to that PDF).

Brad's requirement (2026-10-01): the electronics site (and the radio site, for
radio-specific items) must cover everything in this chapter. Write everything in
our own words from primary sources; never copy the slides. Where the slides are
imprecise, teach the precise version (noted below).

Ownership rule: exploring_electronics owns DC/AC circuit theory, components,
batteries, magnetism; exploring_radio owns operating, ethics, and RF.

## Status

| Slides | Chapter topic | Status | Where it lives |
|---|---|---|---|
| 2–3 | Code of Ethics (Bill Wilson VE3NR, 1997); The Radio Amateur's Code (Paul Segal W9EEA, 1928) | ✅ | exploring_radio amateurs_code.md (RAC + ARRL sources) |
| 5–10 | Structure of matter, atoms, electrostatic attraction | ✅ | conductors_and_insulators.md |
| 11 | Molecules, ions, isotopes | ✅ molecules + ions (isotopes skipped: not electrical) | conductors_and_insulators.md "Inside the Atom" |
| 12–18 | Valence electrons, conductors vs insulators, copper atom, band gap | ✅ | conductors_and_insulators.md |
| 17, 19–22 | Electric current, coulomb, ampere, ammeter, conventional current | ✅ | current.md |
| 23–26 | Voltage as "pressure", potential difference, voltmeter | ✅ | voltage.md |
| 27–29 | Resistance, ohm, ohmmeter | ✅ | resistance.md |
| 30 | Factors affecting resistance; PTC vs NTC; tempco in ppm/°C | ✅ | resistance.md (factors) + resistor_types.md (TCR, PTC/NTC, Yageo CFR/MFR worked example) |
| 31–36 | Resistors, symbol, colour code, mnemonic | ✅ | resistor_color_codes.md ("Better Be Right Or Your Great Big Venture Goes West") |
| 37–40 | Potentiometers, wirewound vs composition pots, trimmers, rheostat (+ tapped, tapers, fixed types, wire-wound vs composition) | ✅ | resistor_types.md + pot_and_rheostat schematic |
| 41 | Conductance | ✅ | resistance.md |
| 42–46 | Magnets, four fundamental forces, fields, lines of force, poles, types of magnets | ✅ | magnetism.md (+ electromagnets, induction, transformers: also ISED topic 5-11) + transformer_step_down schematic |
| 47–48 | Direct current | ✅ | current.md (DC/AC section) |
| 49 | Sources of DC: friction, heat, pressure (piezo), magnetism, light, chemical | ✅ | voltage.md "Where Voltage Comes From" (six sources + figure) |
| 50–70 | Cells and batteries: cell vs battery, EMF, electrochemistry, series vs parallel (capacity, not "current"), mAh and drain, primary vs secondary (storage), shelf life, self-discharge, internal resistance, cell voltages, 8 chemistries, Li-ion hazards (Health Canada + Canadian Forces Fire Marshal guidance, not the slide's extinguisher advice), lead-acid hydrogen, disposal (Call2Recycle) | ✅ | batteries.md (Power topic) + cells_series_parallel schematic |
| 71–73 | Closed, open, short circuits; continuity | ✅ | open_short_fuses.md |
| 74 | Fuses: current rating, voltage rating (interrupt without arcing), never up-rate | ✅ | open_short_fuses.md (Littelfuse-sourced ratings, derating, speed classes, breakers) |
| 75 | Schematic diagrams | ✅ | reading_schematics.md |
| 76–85 | AC: definition, 60 Hz, hertz, V and I in phase in a resistor, elementary generator, RMS (0.707 / 1.414), sine vs square (+ triangle), 120 V RMS = 170 V peak, mains frequencies (Niagara 25 Hz, Westinghouse 60 Hz, Europe 50 Hz) | ✅ | ac_dc.md + ac_resistor schematic |
| Q21, Q22, Q24 | Metric prefixes (mA ↔ A, mV ↔ V) | ✅ | metric_prefixes.md (all of ISED topic 5-1 incl. centi; RKM + capacitor codes) |
| Q1–Q40 | Review questions | maps to the rows above | — |

## Writing order

1. Metric Prefixes and Units (short; every later article leans on it)
2. Open Circuits, Short Circuits, and Fuses
3. Cells and Batteries
4. AC vs DC
5. Magnetism and Electromagnetism
6. Resistor Types (fixed, tapped, variable; carbon composition, film, wire-wound; potentiometers, trimmers, rheostats; tempco ppm/°C)
7. Small edits: piezo source (voltage.md), molecules/ions (conductors_and_insulators.md), colour-code mnemonic (resistor_color_codes.md)
8. Radio: Code of Ethics + The Radio Amateur's Code (radio On the Air topic)

Mark each row ✅ (with the article) as it lands.
