# Coverage map: AVARC Basic course, Chapter 4A "Inductance"

Source: Annapolis Valley Amateur Radio Club online Basic course, Chapter 4A
(Al Penney, VO1NO), 130 slides incl. 20 review questions:
https://avarc.ca/wp-content/uploads/online-basic-course/Ch4A-Inductance.pdf
(read 2026-10-08; slide numbers refer to that PDF).

Same rules as the chapter 2 and 3 maps. Electronics owns magnetism, inductors,
and transformers as power components; radio owns reactance, RF chokes, and
antenna impedance matching (marked "radio").

## Status

| Slides | Chapter topic | Status | Where it lives |
|---|---|---|---|
| 2–3 | Review: Ohm's law triangle, power | ✅ | ohms_law.md |
| 6–10 | Current makes a field; field strength ∝ current; conventional vs electron flow; force on a wire | ✅ | magnetism.md, current.md |
| 11–13 | Elementary generator | ✅ | ac_dc.md, magnetism.md |
| 14–19 | Counter EMF; inductor in a DC circuit; switch-off spike damages electronics | ✅ | inductors.md (flyback diode) |
| 20–22 | Inductor in an AC circuit | ✅ qualitative | inductors.md "Inductors and AC"; X_L formula is radio |
| 23–25 | Field around a coil; the henry | ✅ | magnetism.md, inductors.md |
| 26–28 | Types of inductor; roller inductor; loopstick (ferrite rod) | ✅ | inductors.md (roller coil + slug-tuned card added 2026-10-08) |
| 29–32 | Factors affecting inductance; core materials | ✅ | inductors.md (Wheeler, permeability) |
| 33–36 | Inductors in series and parallel (12 mH, 20 mH examples) | ✅ | inductors.md |
| 37–46 | Reactance, X_L = 2πfL, worked examples (8 H at 120 Hz and 2 kHz), energy stored not dissipated | radio | not written: Radio Fundamentals (B-005-010); inductors.md has the qualitative rise with frequency |
| RQ 8–9 | Ferrite cores and RF chokes: high reactance at RF, low at audio (B-008) | radio + ✅ | inductors.md ferrite bead card; RF framing belongs in radio's interference article |
| 47–63 | Transformers: induced EMF, isolation, step up/down, turns ratio = voltage ratio, worked examples | ✅ | magnetism.md Transformers |
| 70–74 | Power in = power out; current ratio inverse; VA rating | ✅ | magnetism.md "Current and Power" (added 2026-10-08) |
| 64–69 | Impedance matching with transformers; audio; antenna 300–75 Ω balun | ✅ / radio | magnetism.md states the turns-ratio-squared rule; baluns and antenna matching belong on radio (B-006) |
| 75–82 | Losses: eddy currents and laminations, winding resistance, leakage, hysteresis | ✅ | magnetism.md "Where the Losses Go" (added 2026-10-08) |
| 83–88 | Multiple windings, autotransformer, variac, toroids | ✅ | magnetism.md "Kinds of Transformer" + transformer_kinds schematic (added 2026-10-08) |
| RQ 19 | Coupling strongest when wires are close and parallel | ✅ | inductors.md |
| RQ 20 | Permanent magnets made of steel (hard magnetic material) | ✅ | magnetism.md permanent magnets card (added 2026-10-08) |
