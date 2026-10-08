# Coverage map: AVARC Basic course, Chapter 3 "Ohm's Law and Power"

Source: Annapolis Valley Amateur Radio Club online Basic course, Chapter 3
(Al Penney, VO1NO), 188 slides incl. 38 review questions:
https://avarc.ca/wp-content/uploads/online-basic-course/Ch3-Ohms-Law-and-Power.pdf
(read 2026-10-04; slide numbers below refer to that PDF).

Same rules as `avarc_basic_ch2.md`: cover everything, in our own words, from
primary sources. exploring_electronics owns the circuit theory; exploring_radio
owns the transmitter-specific applications (marked "radio").

## Status

| Slides | Chapter topic | Status | Where it lives |
|---|---|---|---|
| 2 | Beware cheap battery packs | ✅ | batteries.md, Charging, Storage, and Care (Health Canada source) |
| 4–7 | Current, voltage (EMF, potential difference, symbol E), resistance, conductance, siemens, resistivity, size/shape | ✅ | current.md, voltage.md, resistance.md; E notation in ohms_law.md |
| 6 | Superconductors | ✅ | resistance.md, temperature bullet (added 2026-10-04) |
| 8–9 | Ohm's law, Georg Ohm 1827, Cavendish | ✅ | ohms_law.md (Cavendish added 2026-10-04) |
| 11–12 | Ohm's law triangle | ✅ | ohms_law.md (V on top; notes E for the exam) |
| 13–36 | Worked problems with mV, mA, kΩ conversions | ✅ | ohms_law.md practice + metric_prefixes.md |
| 37–41 | Series resistance adds | ✅ | series_and_parallel.md |
| 42–50 | Parallel reciprocal formula, identical resistors R ÷ n | ✅ | series_and_parallel.md |
| 51–60 | Series current same, voltage drops sum, step-by-step drops | ✅ | series_and_parallel.md (300/600 Ω worked example), voltage.md, current.md |
| 61–64 | Battery internal resistance, terminal voltage under load, voltmeter draws no current, rises as discharged | ✅ | batteries.md (rise with discharge + cold added 2026-10-04, Energizer IR guide) |
| 65–81 | Parallel: same voltage, branch currents sum, worked | ✅ | series_and_parallel.md, current.md (Kirchhoff) |
| 82–92 | Series-parallel combination reduction | ✅ | series_and_parallel.md "Reducing a Network Step by Step" (added 2026-10-04) |
| 93 | Energy, kinetic/potential, joule | ✅ | voltage.md (energy per coulomb, height picture), ohms_law.md (joules per second, kWh) |
| 94–104 | Power, watt, P = IE = E²/R = I²R | ✅ | ohms_law.md |
| 105–106 | Resistor power ratings, physical size, safety margin | ✅ | ohms_law.md Power Ratings (half-rating rule); series_and_parallel.md "Bigger Bodies, Bigger Ratings" |
| 107–109 | Power ratings in series/parallel combinations; two resistors of twice R for more dissipation | ✅ | series_and_parallel.md "Sharing the Heat" (added 2026-10-04) |
| RQ 2 | Heavy-gauge DC leads for a 100 W transceiver (B-003-017-007, -009) | radio | not written: Station & Safety; electronics resistance.md has the wire physics to link |
| RQ 31 | Transmitter DC input power (B-005-006-003); DC input vs RF output (B-003-011-011, B-004-001-010) | radio | not written: P = V × I is in ohms_law.md; transmitter framing belongs on radio |
| RQ 35 | 50 Ω dummy load (B-005-006-007; purpose B-002-004-005) | ✅ / radio | resistor combination in series_and_parallel.md; what a dummy load is for belongs on radio |
