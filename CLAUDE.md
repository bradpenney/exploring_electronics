# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Repository Overview

**Exploring Electronics** teaches electronics and physical computing to software developers and engineers through a progressive learning journey—from understanding a resistor to designing and building real circuits. It follows the same editorial standards and progressive structure as the other exploring_* sites.

**Target Audience:** Software developers, platform engineers, and DevOps professionals who want to understand the hardware side of computing—Arduino, Raspberry Pi, ESP32, sensors, circuits, and the electronics underlying IoT and embedded systems.

**Teaching Philosophy:** Every article starts with a software engineer's mental model (code, variables, functions, APIs) before introducing electronics theory. Hardware concepts are connected to things they already know: GPIO pins as function arguments, voltage dividers as analog data, serial protocols as network packets.

## Current Status: Site Setup

**CRITICAL**: This site is newly created. Content structure and article plans are not yet defined. The focus for now is establishing the editorial framework, AI instructions, and site configuration. Content will be developed separately.

- All navigation should be commented out in `mkdocs.yaml` until content is reviewed and ready
- The site is in draft state — no published articles yet
- Content will be developed in phases (Essential → Efficient → Mastery)

## Important Preferences

**Git Operations**: The user handles all git operations (commits, pushes, etc.) themselves. Do not commit or push changes.

**MkDocs Operations**: The user handles running `mkdocs serve` and `mkdocs build` themselves. Do not run these commands.

## Critical Persona Insight

**IMPORTANT**: This site has a unique audience assumption that differs from typical electronics tutorials:

### Essential: The Software Developer Picking Up Hardware

**Who they are:**
- Software developer, platform engineer, or SRE
- Has programmed professionally — comfortable with code, APIs, command lines
- Just bought their first Arduino, Raspberry Pi, or ESP32 kit
- Intimidated by hardware (fear of breaking things, "smoke means you've lost")
- Has no formal electronics training

**What they already know:**
- How to write code (Python, JavaScript, C — at least one)
- What variables, functions, loops, and conditionals are
- Networking concepts (TCP/IP, APIs, protocols)
- Version control and basic DevOps

**What they don't know:**
- Ohm's Law, voltage, current, resistance
- What a resistor, capacitor, or transistor actually does
- How to read a schematic or datasheet
- Why you can't just plug things in without checking the specs

**Tone and approach for Essential:**
- Mentorship voice — experienced guide, not authority lecturing
- **Safety-first**: Electronics can injure or destroy equipment; explain consequences before risky steps
- Use software analogies: GPIO pins as function I/O, voltage as "pressure", current as "flow rate"
- Reassuring: "You won't break it by reading a datasheet"
- Build confidence incrementally; never assume electronics familiarity

---

### Efficient: The Maker Who Wants to Go Off-Script

**Who they are:**
- Developer or hobbyist who can follow an Arduino tutorial
- Building real projects (IoT sensors, home automation, custom hardware)
- Wants to understand WHY things work, not just copy paste code
- Ready to read datasheets and design their own circuits

**What they already know:**
- Basic circuit concepts (voltage, current, resistance)
- How to wire a breadboard and use a multimeter
- Microcontroller basics (GPIO, PWM, serial communication)
- One microcontroller platform (Arduino, MicroPython, etc.)

**What they don't know:**
- Component selection and substitution
- Circuit analysis and design principles
- Communication protocols at the register level
- Power supply design and efficiency

**Tone and approach for Efficient:**
- **Peer-to-peer** — no hand-holding, treat them as engineers
- Connect electronics to their software engineering context
- Safety warnings still apply but are framed professionally, not reassuringly
- Required section: **"Where You've Seen This"** — bridges their software experience to electronics

---

### Mastery: The IoT Developer or Electronics Professional

**Who they are:**
- IoT developer, embedded systems engineer, or electronics-adjacent professional
- Designs and ships hardware products or infrastructure
- Responsible for production reliability of hardware-software systems
- Understands electronics at a professional level

**What they already know:**
- Circuit design, component selection, power electronics
- Communication protocols (I2C, SPI, UART, USB) at the register level
- PCB layout fundamentals
- Production concerns (EMI, thermal management, manufacturing tolerances)

**Tone and approach for Mastery:**
- Colleague-to-colleague — skip the basics, focus on professional concerns
- Production context: cost, reliability, regulatory compliance (CE, FCC, RoHS)
- Deep technical depth — no apologies for complexity

---

**The rule:** Read the section you're working on. Essential = developer persona, safety-first. Efficient = peer-to-peer, off-script maker. Mastery = professional, production-grade.

---

## SEO Strategy and Publication Process

**CRITICAL**: This site uses a draft/publish workflow to ensure only vetted content appears in search engines and the sitemap.

### SEO Configuration Overview

The site has comprehensive SEO optimization:

1. **Sitemap**: Auto-generated by MkDocs at `/sitemap.xml` when `site_url` is configured
2. **robots.txt**: Located at `docs/robots.txt`, points to sitemap
3. **Meta plugin**: Injects canonical URLs to prevent duplicate content
4. **Social cards**: Open Graph images auto-generated for social media sharing
5. **Google Analytics**: Configured with tracking ID
6. **Exclude plugin**: Prevents unpublished content from appearing in builds and sitemap

### Required Metadata for Every Article

**MANDATORY**: Every article MUST have frontmatter metadata before being published:

```yaml
---
title: "Title With a Colon: Must Be Quoted"
description: Compelling description for search results (150-160 chars ideal)
---
```

**CRITICAL**: If the title contains a colon (`:`) it **must** be quoted — unquoted colons cause PyYAML to misparse the frontmatter silently.

**Rules:**

- **Title**: Should be unique across the site, descriptive, include key terms
- **Description**: Summarize what the reader will learn, compelling call-to-action
- **No keywords needed**: Modern search engines don't rely on keyword meta tags
- **Check length**: Titles >60 chars and descriptions >160 chars get truncated in search results

### The Exclude Plugin Strategy

**Problem**: MkDocs by default includes ALL `.md` files in builds and sitemaps, even draft/unpublished content.

**Solution**: The `mkdocs-exclude` plugin configured in `mkdocs.yaml` excludes unpublished directories from:
- Site builds
- Sitemap generation
- Search indexing
- Navigation (even if accidentally uncommented)

**Current exclude configuration** (as of 2026-05-24):

```yaml
plugins:
  - search
  - meta
  - exclude:
      glob:
        - "efficient/*"
        - "mastery/*"
        - "tools/multimeter.md"
        - "tools/arduino_cli.md"
        - "tools/soldering.md"
        - "tools/bench_power_supply.md"
  # ... other plugins
```

**Published articles (not in exclude list):**
- `essential/what_is_electricity.md`
- `tools/breadboards.md`

**What this means:**
- Draft articles can exist in these directories without appearing in search results
- Articles can be worked on incrementally without affecting SEO
- Only vetted, published content appears in sitemap and builds

### How to Publish an Article

When an article is ready for publication (passes all quality checks), follow these steps **in order**:

#### 1. Pre-Publication Checklist

Complete the [Quality Standards Checklist](#quality-standards-checklist) below. Do NOT proceed until all items are checked.

#### 2. Remove from Exclude List

Edit `mkdocs.yaml` and remove the directory from the exclude plugin:

**Before (draft):**
```yaml
- exclude:
    glob:
      - "essential/*"  # Article is excluded
```

**After (published):**
```yaml
- exclude:
    glob:
      # essential/* is now published
```

**IMPORTANT**:
- Remove the ENTIRE line, don't just comment it
- If publishing individual files (not whole directories), use specific paths:
  ```yaml
  - "essential/intro_to_circuits.md"  # Still draft
  # essential/what_is_electronics.md is published (not in exclude list)
  ```

#### 3. Add to Navigation

Uncomment the article in the `nav:` section of `mkdocs.yaml`.

#### 4. Verify Publication

```bash
# Build the site
poetry run mkdocs build --strict

# Check sitemap includes the new article
grep -o '<loc>[^<]*</loc>' site/sitemap.xml | grep essential
```

#### 5. Update CLAUDE.md Exclude List

Update the "Current exclude configuration" section above to reflect what's NOW excluded.

### SEO Checklist for Published Articles

Before removing an article from the exclude list, verify:

- [ ] **Frontmatter metadata present** - Title and description in YAML frontmatter
- [ ] **Title is unique** - Not duplicated across other published articles
- [ ] **Description is compelling** - 150-160 chars, summarizes value
- [ ] **All images have alt text**
- [ ] **All links work** - Internal links point to published articles only
- [ ] **No "coming soon" dead links** - Replace with plain text or link to overview
- [ ] **External links are valid** - Use WebFetch to verify important URLs
- [ ] **Headings are hierarchical** - One H1, logical H2-H6 structure
- [ ] **No duplicate content** - Cross-link instead of repeating other articles

### Common SEO Mistakes to Avoid

1. **Linking to unpublished articles** - Always check if target article is in exclude list before linking
2. **Forgetting to update exclude list** - When publishing, remove from exclude glob
3. **Missing metadata** - Every article needs title and description
4. **Publishing incomplete articles** - Follow full quality checklist before publishing
5. **Leaving articles in navigation but excluded** - Navigation and exclude list must align

---

## CRITICAL: No Repetition - Respect Reader's Time

**This is an absolute deal-breaker for content quality.**

### The Principle

Avoid duplication and repetition at all costs. Every time we repeat information, we waste the reader's time and make the content feel bloated.

### The Rules

1. **Cross-link instead of repeating** - If a concept is explained elsewhere, link to it
2. **Only repeat for significantly different perspectives** - Brief intro vs. deep dive is acceptable; same explanation twice is not
3. **Progressive depth, not repetition** - Each article builds WITHOUT re-explaining previous articles
4. **Audit before publishing** - Search for repeated concepts across published articles

### Before Explaining Any Concept, Ask:

1. Have we explained this elsewhere in this section (Essential, Efficient, Mastery)?
2. If yes, is my perspective SIGNIFICANTLY different?
3. If no, add a cross-link: "Remember X from [Article]? Now let's see how..."
4. If yes, explicitly state the new angle: "Earlier we covered voltage conceptually — now let's measure it"

### Required: Pre-Publication Repetition Audit

Before marking any article complete, use the Explore agent to search for repeated concepts across published articles in the same section. If found, consolidate and cross-link.

---

## Project Structure

- `docs/` - Markdown content organized by learning tier
  - `essential/` - Getting started (complete beginner, first circuit, first microcontroller)
  - `efficient/` - Going deeper (circuit design, protocols, real projects)
  - `mastery/` - Professional level (PCB design, power electronics, production)
  - `images/` - Diagrams and circuit photos
  - `stylesheets/` - Custom CSS (`extra.css`)
- `mkdocs.yaml` - Site configuration and navigation
- `pyproject.toml` - Poetry dependencies

**Important:** Directory structure mirrors site navigation. Articles reference each other using relative paths (e.g., `../essential/filename.md`).

## Common Commands

```bash
# Install dependencies
poetry install

# Serve locally (http://localhost:8000)
poetry run mkdocs serve

# Build static site (ALWAYS use --strict for link validation)
poetry run mkdocs build --strict
```

**Link Validation:** The project uses `mkdocs-htmlproofer-plugin` to validate all internal links. Always build with `--strict` flag to catch broken links.

---

## Content Guidelines

### Tone and Style

Tone varies by tier. See **Critical Persona Insight** above. The key rule:

- **Essential** → mentorship voice, safety-first, software analogies, reassuring
- **Efficient** → peer-to-peer, no hand-holding, expects electronics literacy
- **Mastery** → colleague-to-colleague, production focus, full technical depth

**Core Principles (all tiers):**

- **Safety-first**: Electronics can injure (mains voltage), start fires (lithium batteries), destroy components. Never omit safety context.
- **Software analogies**: This audience codes for a living — use that. GPIO = function parameter. Voltage = pressure. Pull-up resistor = default parameter value.
- **Purpose-driven**: Always explain the "why" before the "how"
- **Practical focus**: Real components, real values, real circuits — not vague theory
- **No emoji spam**: limit to 1-3 per article, used strategically

**Essential tone specifically:**

- Empathetic openings: "You just plugged in your first Arduino. Now what?"
- Safety-first: explain what can go wrong and why, before any risky steps
- Mentorship voice: "I'll show you..." not "You must..."
- Software bridges: open with familiar code context, introduce hardware equivalent

**Efficient tone specifically:**

- Peer-to-peer: assume they've wired a breadboard and can use a multimeter
- Required: **"Where You've Seen This"** section — connects electronics concept to software engineering experience (e.g., I2C handshake → TCP connection setup)
- Safety warnings still apply, but framed professionally — not reassuringly

**Required Sections (all tiers):**

1. Opening hook with real-world context (Essential: empathetic; Efficient/Mastery: scenario-based)
2. **"Where You've Seen This"** — **(Efficient+ required)** bridges software knowledge to electronics concept
3. Core content with circuit examples, component values, and code snippets
4. Safety warnings where appropriate
5. Practice exercises with expandable solutions (`??? question`)
6. Quick Recap / Key Takeaways
7. What's Next — progression to next article
8. Further Reading — organized by category

---

### Electronics-Specific Writing Guidelines

#### Safety Warnings — NEVER Skip These

Use the `!!! danger` admonition for life-safety hazards:

```markdown
!!! danger "Mains Voltage (120V / 240V AC)"
    Never connect mains voltage to a breadboard or to any circuit without proper isolation and
    enclosures. Lethal current levels begin at 50mA. Always use a GFCI outlet and appropriate
    fusing when working near mains power.
```

Use `!!! warning` for equipment-destroying risks:

```markdown
!!! warning "Reverse Polarity"
    Connecting a component backwards can destroy it instantly. Always double-check polarity
    before powering a circuit. Electrolytic capacitors and diodes are polarized components.
```

**Safety escalation by context:**

- Essential: Full explanation with WHY it's dangerous, not just "be careful"
- Efficient: Professional callout — brief, assumes competence
- Mastery: Regulatory/standards context (IEC 60950, UL listing, etc.)

#### Component Values and Units

**ALWAYS use standard SI prefixes in prose:**

- Resistance: Ω, kΩ, MΩ (not "ohms" or "kohm" in value notation)
- Capacitance: pF, nF, µF (not "microfarads" inline; use µF symbol)
- Inductance: nH, µH, mH
- Voltage: mV, V
- Current: µA, mA, A
- Frequency: Hz, kHz, MHz, GHz
- Power: mW, W

**Component value formatting in prose:**

- ✅ Correct: "a 10 kΩ resistor", "a 100 µF capacitor", "3.3V supply rail"
- ❌ Wrong: "a 10k resistor", "a 100uf cap", "3.3 volts"

**Component names in prose:**

- ✅ Correct: "Use a `74HC595` shift register"
- ✅ Correct: "The `ESP32` module"
- ❌ Wrong: "Use a 74HC595 shift register" (chip names get backticks like command names)

#### Code Examples

Electronics articles include both **circuit diagrams** and **code**. Both must be treated as first-class teaching tools.

**Code formatting:**

```markdown
``` python title="Read a Temperature Sensor (MicroPython)" linenums="1"
from machine import I2C, Pin
import time

i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # (1)!
addr = 0x48  # (2)!

while True:
    raw = i2c.readfrom(addr, 2)
    temp = ((raw[0] << 8) | raw[1]) >> 4  # (3)!
    print(f"Temperature: {temp * 0.0625:.1f}°C")
    time.sleep(1)
```

1. I2C bus 0, with GPIO22 as clock and GPIO21 as data
2. Default I2C address for the TMP102 sensor
3. The 12-bit temperature value is left-aligned in the two bytes
```

**Code language priority for electronics articles:**

- **MicroPython** — default for microcontroller examples (most accessible, Python syntax)
- **Arduino C/C++** — when hardware library support is better or more common
- **Python (host-side)** — for data collection, serial communication, Raspberry Pi scripts
- Provide tabs when both MicroPython and Arduino C are relevant

**Tab format for multi-platform examples:**

```markdown
=== ":material-language-python: MicroPython"

    ```python title="Blink LED" linenums="1"
    from machine import Pin
    import time

    led = Pin(25, Pin.OUT)
    while True:
        led.toggle()
        time.sleep(0.5)
    ```

=== ":simple-arduino: Arduino C"

    ```cpp title="Blink LED" linenums="1"
    const int LED_PIN = 13;

    void setup() {
        pinMode(LED_PIN, OUTPUT);
    }

    void loop() {
        digitalWrite(LED_PIN, HIGH);
        delay(500);
        digitalWrite(LED_PIN, LOW);
        delay(500);
    }
    ```
```

#### Circuit Diagrams

Use **Mermaid diagrams** for logical circuit flow and block diagrams. For actual schematic symbols, reference external tools or images.

**Mermaid block diagrams for electronics:**

```markdown
``` mermaid
graph LR
    PWR["3.3V Power"] --> R["10 kΩ Pull-up"]
    R --> SDA["SDA Line"]
    SDA --> SENSOR["Temp Sensor\n(TMP102)"]
    SDA --> MCU["ESP32"]
```
```

**When to use images vs Mermaid:**
- Mermaid: block diagrams, architecture, data flow, protocol timing concepts
- Images: actual breadboard layouts, schematic fragments, oscilloscope screenshots

**Mermaid color scheme for this site (slate + amber accent):**

- Standard Node (Slate 800): `fill:#2d3748,stroke:#cbd5e0,stroke-width:2px,color:#fff`
- Highlighted Node (Amber 600): `fill:#d97706,stroke:#cbd5e0,stroke-width:2px,color:#fff`
- Darker Node (Slate 900): `fill:#1a202c,stroke:#cbd5e0,stroke-width:2px,color:#fff`
- Warning/Danger (Red 600): `fill:#c53030,stroke:#cbd5e0,stroke-width:2px,color:#fff`
- Success/Output (Green 700): `fill:#2f855a,stroke:#cbd5e0,stroke-width:2px,color:#fff`

#### Read-Only vs Risky Operations

Label every operation clearly for Essential-tier readers:

```markdown
- ✅ **Safe (Non-Destructive):** Reading voltages with a multimeter, measuring continuity, reading datasheets
- ⚠️ **Caution (Can Damage Components):** Applying voltage without checking polarity, exceeding GPIO current limits, hotplugging I2C devices
- 🚨 **DANGER (Can Injure or Destroy):** Mains voltage, lithium battery shorts, capacitor discharge
```

#### Datasheets and Official Sources

Always link to manufacturer datasheets when introducing a component:

```markdown
The `NE555` timer IC is one of the most produced chips in history.
([Datasheet](https://www.ti.com/lit/ds/symlink/ne555.pdf))
```

Validate all datasheet URLs with WebFetch before publishing — TI, Microchip, and others reorganize their documentation.

---

### Article Layout and Visual Structure

**CRITICAL**: Articles must not be simple circuit references. They must teach skills with context and serve multiple audiences through varied layout.

#### Visual Elements Required

1. **Mermaid Diagrams** (when circuit/protocol architecture exists)
   - Place at article top to show the big picture
   - Use for: block diagrams, protocol flows, power rails, signal paths
   - Follow the amber/slate color scheme above

2. **Card Grids** (for categorization)
   - Use `<div class="grid cards" markdown>` for grouping related components or concepts
   - Each card should explain "Why it matters" BEFORE showing circuit values or code
   - Format:
     ```markdown
     <div class="grid cards" markdown>

     -   :material-resistor: **Resistors**

         ---

         **Why it matters:** Every digital circuit uses resistors to limit current and set voltage levels.

         **Essential value:** Know Ohm's Law — `V = I × R`

         **Rule of thumb:** When in doubt, use 10 kΩ for pull-up resistors

     </div>
     ```

3. **Content Tabs** (for platforms, protocols, or complexity levels)
   - Use `=== "Tab Name"` for different microcontroller platforms or approaches
   - Examples:
     - "MicroPython" vs "Arduino C"
     - "ESP32" vs "Raspberry Pi"
     - "Breadboard Prototype" vs "Production Circuit"

#### Layout Patterns by Article Type

**Component Introduction Articles (like Resistors, Capacitors, LEDs):**

1. Opening — Software engineer's analogy hook
2. "Where You've Seen This" — connect to something they know
3. Mermaid Diagram — block diagram showing where this component fits
4. Card Grid — component types or common use cases
5. Core explanation with values and formulas
6. Code example (if component interfaces with a microcontroller)
7. Safety warnings
8. Practice Exercises
9. Quick Recap
10. Further Reading
11. What's Next

**Hands-On Project Articles (like "Blink an LED", "Read a Sensor"):**

1. Opening — "Here's what you'll build"
2. Parts list with exact component values
3. Wiring diagram (image or mermaid block diagram)
4. Step-by-step — wiring, then code
5. Verification — how to know it's working
6. Troubleshooting (collapsible)
7. Practice Exercises
8. Further Reading
9. What's Next

**Protocol/Communication Articles (like I2C, SPI, UART):**

1. Opening — Software bridge (protocols they already know: HTTP, TCP, serial)
2. "Where You've Seen This" — required
3. Mermaid Diagram — protocol timing or bus architecture
4. Technical details — addresses, timing, registers
5. Code Example — sending and receiving data
6. Common Issues and debugging
7. Practice Exercises
8. Further Reading
9. What's Next

#### Context Before Code

**NEVER start with code or circuit values.** Always provide context first:

- ❌ Bad: "Connect a 10 kΩ resistor between GPIO4 and 3.3V"
- ✅ Good: "GPIO inputs float to unpredictable values when disconnected. A pull-up resistor connects the pin to a known voltage (3.3V) through a high-resistance path, so the pin reads HIGH unless actively pulled LOW..."

---

### Cross-Linking Strategy

**Internal links:** Connect concepts progressively. Each article should link forward and backward in the learning path.

**Cross-link to cs.bradpenney.io** for computer science fundamentals:
- Serial protocols → How parsers work, FSMs
- Binary and hex → Computer science essentials

**Cross-link to other exploring_* sites:**
- Linux articles for Raspberry Pi GPIO via the command line
- Kubernetes articles when deploying IoT data pipelines
- Software Dev Tools articles for git workflows on embedded projects

---

## Quality Standards Checklist

Before uncommenting an article in `mkdocs.yaml`:

**✅ Content Quality:**

- [ ] **NO REPETITION AUDIT** - Searched for repeated concepts across published articles in this section (CRITICAL!)
- [ ] Opening hook with real-world relevance (Essential: empathetic dev persona; Efficient/Mastery: scenario-based)
- [ ] Clear learning objectives
- [ ] Circuit values and component specs are correct (verify against datasheets)
- [ ] Code examples tested (or clearly marked as illustrative)
- [ ] Safety considerations addressed (NEVER skip for Essential)
- [ ] Practice exercises with nested solutions (`??? tip "Solution"` inside question)
- [ ] Key takeaways or quick recap
- [ ] What's Next progression
- [ ] Further Reading organized into categories (Datasheets, Official Docs, Deep Dives, Related Articles)

**✅ Technical Accuracy:**

- [ ] Component values are correct and practical
- [ ] Code compiles/runs (or validated syntax)
- [ ] Safety warnings for hazardous operations
- [ ] Datasheet links verified with WebFetch
- [ ] Platform-specific differences noted (3.3V vs 5V logic, ESP32 vs Arduino pin numbering)

**✅ Tone and Style:**

- [ ] Correct persona for the tier (Essential vs Efficient vs Mastery)
- [ ] "Where You've Seen This" section present (Efficient+ only, required)
- [ ] Software analogies used for unfamiliar hardware concepts (Essential)
- [ ] Safety-conscious throughout
- [ ] Emoji usage limited (1-3 max, strategic)
- [ ] No over-the-top marketing language

**✅ Layout and Structure:**

- [ ] Article is NOT a simple parts list or command reference — teaches skills with context
- [ ] Uses visual elements appropriately (mermaid block diagrams, card grids, tabs)
- [ ] Mermaid diagram at top (if circuit/protocol architecture exists)
- [ ] Card grids explain "Why it matters" before values/code
- [ ] Platform tabs for multi-platform examples (MicroPython vs Arduino C)
- [ ] Context provided BEFORE circuit values or code (never starts with syntax)

**✅ Formatting:**

- [ ] All code blocks have `title=` attribute (and `linenums="1"`)
- [ ] Component chip names in backticks in prose (e.g., `NE555`, `ESP32`, `74HC595`)
- [ ] Component values use correct SI units (kΩ not "kohm", µF not "uf")
- [ ] **CRITICAL: Blank lines before ALL lists** (recurring MkDocs rendering issue)
- [ ] Mermaid diagrams follow slate/amber color scheme
- [ ] Internal links use relative paths
- [ ] **External/datasheet links validated with WebFetch before publishing**

**✅ Integration and Links:**

- [ ] Pre-publication link audit completed
- [ ] **NEVER link to unpublished articles** - only link to articles uncommented in mkdocs.yaml
- [ ] Cross-links added between published articles in the same tier
- [ ] "Part of [Tier]" callout with link to tier overview
- [ ] Referenced in "What's Next" from previous article
- [ ] Datasheet links included for every component introduced
- [ ] Cross-links to cs.bradpenney.io and other exploring_* sites where relevant

---

## Final Notes

This site teaches **electronics to software engineers**. Every concept must be grounded in something they already know from software, then expanded into hardware reality.

**Essential** — err on the side of:
- More safety context rather than less
- More software analogies rather than hardware-first explanations
- Simpler circuits before complex ones
- Reassurance that mistakes are recoverable (components are cheap; mains is not)

**Efficient** — err on the side of:
- Peer-to-peer directness
- Connecting hardware behavior to software engineering principles
- Datasheets and primary sources over simplified summaries

**Mastery** — err on the side of:
- Production realities (cost, tolerances, regulatory)
- Deep technical depth
- Referencing standards and specifications

The goal: software engineers who can **confidently design, build, and debug real electronic circuits** — and understand the hardware underneath the software they ship.
