# Exploring Electronics — Planning Document

Last updated: 2026-05-10

---

## What This Site Is

**Conceptual electronics education for software engineers.** Not a tutorial site — no "follow these steps." Every article explains WHY things work the way they do, grounded in real-world context and cross-linked to actual projects.

**The unique angle:** Electronics taught from a software engineer's mental model. Every concept gets a software parallel:
- Voltage = pressure, current = flow rate
- Pull-up resistor = default parameter value
- I2C handshake = TCP connection setup
- Filter = moving average
- MOSFET gate = boolean switch in code

This framing is genuinely underserved. Most electronics tutorials either ignore your coding background or assume you have none.

---

## What This Site Is NOT

- Not a how-to tutorial site
- Not a step-by-step project guide
- No wiring diagrams, no "connect pin 4 to ground"

The actual projects live on **projects.bradpenney.io** (separate site, to be built). This site provides the theory; the projects site shows it applied.

---

## Relationship with projects.bradpenney.io

These two sites are designed to cross-link deeply:

- Each electronics article has a **"See It In Action"** section linking to relevant projects
- Each project page on projects.bradpenney.io tags which electronics concepts it uses
- Readers bounce between sites: theory → application → deeper theory

**Action item:** When designing projects.bradpenney.io, build a tag/category system that maps to the electronics concept taxonomy on this site.

---

## Site Structure — Three Tiers

### 📦 Essential — Building Blocks and First Principles
*Audience: Software developer, zero electronics background, safety-first, heavy software analogies*

~8 articles. Every article references real objects (phone chargers, USB ports, LEDs) and cross-links to projects. No circuit steps, but illustrative circuits as examples are fine (not instructions).

Planned topics:
1. **What Is Electricity?** — charge, voltage, current, resistance for someone who thinks in code
2. **Resistors** — what they do, why they're everywhere, Ohm's Law, real-world uses
3. **Capacitors** — energy storage, filtering, decoupling; "why is there a cap on every power pin?"
4. **Inductors** — the third passive, energy in magnetic fields, why they fight change
5. **Diodes and LEDs** — the simplest semiconductor story, the p-n junction
6. **Reading Schematics** — the language of electronics; how to decode any circuit diagram
7. **Power Fundamentals** — batteries, voltage rails, regulators, why stable power matters
8. **Safety** — what actually injures you (mains), what doesn't (3.3V), what destroys components

### ⚡ Efficient — Design Thinking
*Audience: Maker/developer who can follow tutorials but wants to go off-script; peer-to-peer tone; "Where You've Seen This" required in every article*

~12 articles. Enough depth to design a circuit from scratch rather than copy one.

Planned topics:
1. **Transistors** — BJT and MOSFET as switch and amplifier; the most important component in existence
2. **Op-Amps** — the Swiss Army knife of analog electronics
3. **Filters** — low-pass, high-pass, band-pass; the software parallel (weighted moving average)
4. **Digital Logic** — gates, flip-flops, registers; the bridge from analog to digital
5. **UART** — serial communication at the physical layer; bits as voltage transitions
6. **SPI** — synchronous serial; why it's faster than UART
7. **I2C** — multi-device bus; the handshake that looks like TCP
8. **Microcontrollers** — where everything above meets programmable logic; convergence point
9. **Reading Datasheets** — the skill that unlocks every component ever made
10. **Analog-to-Digital Conversion** — how the physical world becomes numbers
11. **PWM** — fake analog from digital pins; duty cycle, frequency, applications
12. **Power Supply Design** — linear vs. switching regulators, efficiency, ripple

### 🎯 Mastery — Professional Depth *(Paywalled)*
*Audience: IoT developer, embedded systems engineer, hardware-responsible professional*

~15+ articles. Production-grade concerns.

Planned topics:
- PCB design fundamentals — why layout matters as much as schematic
- Grounding and ground planes — the most misunderstood topic in electronics
- Signal integrity — why your circuit works on a bench but not in a box
- Switching power supply design — efficiency, EMI, compensation
- RF basics — antennas, impedance matching, why WiFi antennas are the length they are
- EMC — conducted and radiated emissions, why your product needs to pass testing
- Component selection for production — tolerances, alternatives, lifecycle, sourcing
- Analog design: feedback and stability — the math behind why op-amp circuits work
- Testing and debugging techniques — oscilloscope, logic analyzer, bench power supply
- Regulatory basics — FCC, CE, RoHS; what "certification" actually means

---

## Platform Strategy

**Primary platform: ESP32** (most searched, has WiFi/Bluetooth — developers care about connectivity)

**Code approach:** MicroPython first, Arduino C as a tab alongside it. Platform-agnostic at the concept level; platform-specific in code examples.

**Raspberry Pi:** Covered only where clearly hardware-relevant (GPIO, HATs, physical computing) — not as "Linux on small hardware" (that's linux.bradpenney.io's territory).

---

## Real-World Grounding — How to Do It

Every article needs grounding from at least one of these:

1. **Everyday objects** — "This is the circuit inside your phone charger." "Every USB port has this protection diode."
2. **Software parallels** — "Where You've Seen This" (Efficient+ required section)
3. **Project cross-links** — "See It In Action" section pointing to projects.bradpenney.io
4. **Industry context** — "This is why engineers do X instead of Y in production"

Dry = failure. The site dies if it reads like a physics textbook.

---

## Open Questions to Resolve

1. **Essential tier depth** — Should Essential articles include illustrative circuits (not tutorials, just "here's what this looks like")? Current thinking: yes, as long as framing is "this demonstrates the concept" not "build this."

2. **projects.bradpenney.io scope** — Needs its own planning session. The cross-link architecture between these two sites should be designed together.

3. **Scope boundary: pure analog vs. digital-only** — Committing to full electronics (analog, digital, power, RF, embedded). Confirm this scope is right before writing Mastery articles.

---

## Site Setup Status

### Done ✅
- `CLAUDE.md` — full AI instructions (persona, tone, safety, writing standards, quality checklist)
- `mkdocs.yaml` — site name, URL, metadata, plugins (search, meta, exclude, social, htmlproofer), correct markdown extensions
- `pyproject.toml` — correct dependencies including `mkdocs-material[imaging]`, `mkdocs-exclude`, `mkdocs-htmlproofer-plugin`
- `docs/CNAME` — `electronics.bradpenney.io`
- `docs/index.md` — electronics-specific homepage
- `docs/robots.txt` — created
- `.github/workflows/ci.yaml` — disabled (workflow_dispatch only until ready to deploy)
- Stale software-dev-tools content removed (old git tutorial, wrong logo image)

### Still Needed Before First Article ⚠️
- `CLAUDE.md` needs updating — currently describes the site as a tutorial/how-to site; needs to reflect the conceptual education approach and projects.bradpenney.io relationship
- Replace `REPLACE_WITH_GA_TRACKING_ID` in `mkdocs.yaml` with actual Google Analytics property ID
- Run `poetry lock && poetry install` inside this directory (pyproject.toml changed)
- Logo image — `docs/images/exploring_electronics.png` (when ready, uncomment logo/favicon in mkdocs.yaml)

### When Ready to Deploy
- Re-enable CI: change `workflow_dispatch` back to `push: branches: [main]` in `.github/workflows/ci.yaml`

---

## Next Session Checklist

1. Update `CLAUDE.md` to reflect non-tutorial, conceptual education approach
2. Confirm open questions (especially Essential tier depth and illustrative circuits)
3. Draft first Essential article outline — "What Is Electricity?" from a software engineer's POV
4. Decide: start planning projects.bradpenney.io in parallel?
