---
date: "2026-06-28 14:30"
title: "arduino-cli: Program an Arduino From the Command Line"
description: "Compile and upload Arduino sketches from the terminal with arduino-cli — one command, no IDE. Install it, find your board, and flash code from your own editor."
---

# arduino-cli

!!! abstract "Practical Tools"
    This article is part of the **Practical Tools** section. It assumes you have an Arduino-compatible board and a circuit to run code on — if you're still wiring that up, start with [Breadboards](breadboards.md). New to Arduino entirely? [What Is an Arduino?](../what_is_an_arduino.md) covers the board itself first.

The Arduino IDE is how most people meet a microcontroller: install it, pick your board from a menu, click the arrow, watch the LED blink. It's a smooth on-ramp — and it's also a curtain. Behind that one button, two real things happen: your code is **compiled from C++ into a binary**, and that binary is **uploaded to the chip**. The IDE is designed so you never have to think about either one.

That's comfortable until it isn't. The day the IDE won't see your board, or the upload dies with a cryptic error, the abstraction that shielded you becomes the thing in your way — and if you've never seen the machinery underneath, you're stuck with a button that just doesn't work.

`arduino-cli` is that same machinery, out in the open. One command compiles your sketch and flashes it to the board, and it hides none of what it's doing: you can see it is C++ being compiled and a binary being sent to a microcontroller. Build that mental model once and no broken IDE can strand you — which is exactly why it's worth starting here rather than arriving here later.

This article gets you from nothing to a board running your code, and explains every part of the command that does it.

---

## Why Start at the Command Line?

The usual advice is to start in the IDE and "graduate" to the command line later. That's backwards. The command line is where anyone doing this seriously ends up — so it's where it pays to begin, before a layer of abstraction has quietly taught you the wrong mental model.

- **You see what's actually happening.** The command names the operation out loud: compile this C++ sketch, send the result to that chip on that port. Nothing is implied or hidden, so the understanding you build is the real one — not "I pressed the arrow and it worked."
- **You can debug a failure.** When an upload fails from the command line, it tells you *which* step broke — compile or upload — and on which port. When the only interface is a button, a failure is just a button that doesn't work, with nowhere to look.
- **It composes with everything else.** A compile-and-upload is one line, so it drops straight into a `Makefile`, a shell alias, a git hook, or a CI run. It works over SSH to a board on a headless machine across the room or across the country. And because the whole command is text — board, core version, port — it's reproducible a year later.

!!! tip "Where the IDE still helps"
    The IDE's **Library Manager** and **Boards Manager** are handy for *browsing* what's available, and they share the same cores and libraries `arduino-cli` uses. Browse there if you like — then build here, where you can see the work being done.

---

## Installing arduino-cli

On macOS or Linux with Homebrew, the cleanest path is the package manager — it handles updates and your `PATH` for you:

```bash
brew install arduino-cli
```

Everywhere else, use the official install script — but **download it and look at it before you run it**:

```bash
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh -o install-arduino-cli.sh
less install-arduino-cli.sh   # read what you're about to execute
sh install-arduino-cli.sh
```

You'll see one-liners online that pipe that URL straight into `sh`. It works, but it's a habit worth never forming: piping the internet into your shell executes whatever the server sends, sight unseen. Downloading first costs ten seconds and lets you check.

By default the binary lands in `./bin` — move it onto your `PATH` (for example, `~/.local/bin` or `/usr/local/bin`) so you can run `arduino-cli` from anywhere.

Confirm it's working:

```bash
arduino-cli version
```

---

## One-Time Setup: Install a Core

`arduino-cli` ships with *no* board support out of the box. A **core** is the package that teaches it how to compile for and upload to a specific family of chips. An Arduino Uno uses the AVR core.

```bash
arduino-cli config init          # create the config file
arduino-cli core update-index    # fetch the list of available cores
arduino-cli core install arduino:avr   # install AVR support (Uno, Nano, Mega…)
```

You only do this once per machine (and again when you want to update). After the AVR core is installed, every AVR board you ever plug in is ready to go.

---

## A Sketch Is a Folder

Arduino has one firm rule about file layout: **a sketch lives in a folder, and the main `.ino` file must have the same name as that folder.**

```
BlinkTest/
└── BlinkTest.ino
```

`BlinkTest.ino` in a folder called `BlinkTest` is valid. The same file in a folder called `blink` is not — the upload will fail to find the sketch. This trips up everyone once. After that, you never forget it.

---

## Find Your Board

Plug the board in over USB and ask `arduino-cli` what it sees:

```bash
arduino-cli board list
```

```
Port         Protocol Type              Board Name  FQBN            Core
/dev/ttyACM0 serial   Serial Port (USB) Arduino Uno arduino:avr:uno arduino:avr
```

Two columns matter here: the **Port** (`/dev/ttyACM0`) and the **FQBN** (`arduino:avr:uno`). Those are the two things the upload command needs to know — where the board is, and what it is. If the board doesn't appear at all, jump to [Common Mistakes](#common-mistakes).

---

## The One Command

From *inside* the sketch folder:

```bash
arduino-cli compile --upload -p /dev/ttyACM0 --fqbn arduino:avr:uno .
```

That single line builds the sketch and flashes it to the board. Every piece:

| Part | What it does |
|---|---|
| `compile` | Builds the sketch — turns your code into a binary the chip can run |
| `--upload` | After a successful build, send the binary to the board |
| `-p /dev/ttyACM0` | The **port** the board is on (from `board list`) |
| `--fqbn arduino:avr:uno` | The **board** you're targeting (from `board list`) |
| `.` | The sketch to build — `.` means "the current directory" |

`compile` and `--upload` are deliberately separate. Run `compile` alone to catch errors without touching the board; add `--upload` once it builds clean. The `.` at the end is easy to forget — it tells `arduino-cli` *which* sketch to build, and the answer is almost always "the folder I'm standing in."

### Reading the FQBN

`FQBN` is the **Fully Qualified Board Name**, and it's structured as `vendor:architecture:board`:

```
arduino : avr : uno
  │        │     │
vendor   arch  board
```

- `arduino` — the vendor (who maintains the core)
- `avr` — the chip architecture (the Uno's ATmega328P is an AVR chip)
- `uno` — the specific board

Swap the last segment for a different AVR board (`arduino:avr:nano`, `arduino:avr:mega`) or the whole thing for another family entirely (`esp32:esp32:esp32`). The FQBN is how one tool targets thousands of different boards without guessing.

---

## The Edit–Compile–Upload Loop

The whole workflow is two steps on repeat: edit the `.ino` in your editor, run the one command. There's nothing to document about the editing half — write the code the way you write any other file. The point of the CLI is that the *build* half collapses into a single line you can re-run instantly.

To keep even that line out of the way, alias it once per project:

```bash
alias flash='arduino-cli compile --upload -p /dev/ttyACM0 --fqbn arduino:avr:uno .'
```

Now the loop is: save the file, type `flash`, watch the board. Every time you run it, the same two steps happen in full view — your C++ is recompiled and the fresh binary is sent to the chip — so the build is never a mystery you're trusting a button to handle.

---

## Watching Serial Output

When your sketch prints with `Serial.println()`, you need something on the other end to read it. That's the IDE's "Serial Monitor" — and `arduino-cli` has it too:

```bash
arduino-cli monitor -p /dev/ttyACM0
```

Match the baud rate your sketch sets in `Serial.begin()` with `-c baudrate=9600` if it isn't the default. This is the single most useful debugging tool you have on a microcontroller: there's no debugger and no `print` to a console, so a serial line is how the board tells you what it's thinking.

---

## What Language Is This, Really?

It's tempting to call Arduino code "C" — it looks like C, and a simple sketch is nearly indistinguishable from it. But the toolchain compiles your sketch as **C++**. ([What Is an Arduino?](../what_is_an_arduino.md) covers what a sketch's `setup()`/`loop()` skeleton means if you haven't seen it before.)

Behind the scenes, `arduino-cli` takes your `.ino` file, adds `#include <Arduino.h>`, generates function prototypes, and hands the result to [a C++ compiler](https://cs.bradpenney.io/efficiency/compilers_vs_interpreters/) (`avr-g++` for AVR boards) that translates it into the binary the chip runs. That's why features that aren't part of C — the `String` object, `Serial.println()`, libraries built around classes — work without complaint, and it's why `setup()` and `loop()` are the two functions the core calls for you rather than ordinary functions like `pinMode()` or `digitalWrite()` that you call yourself. Knowing it's C++ matters the moment you reach for a class, a library, or an error message that mentions C++ types.

---

## Common Mistakes

??? warning "`Permission denied` on the serial port"

    On Linux, the serial device (`/dev/ttyACM0`, `/dev/ttyUSB0`) is owned by a system group — usually `dialout`. If your user isn't [a member of that group](https://linux.bradpenney.io/essentials/users_and_groups/), the upload fails with a permission error. Add yourself once:

    ```bash
    sudo usermod -aG dialout $USER
    ```

    Then **log out and back in** for the group change to take effect. (On Arch-based systems the group is `uucp` instead.)

??? warning "Board doesn't appear in `board list`"

    Usually one of three things: a charge-only USB cable with no data lines (swap it for a known-good data cable), the board not fully seated, or — on some Uno clones — a missing CH340 driver. Genuine Unos enumerate as `/dev/ttyACM*`; many clones show up as `/dev/ttyUSB*` instead, which changes the `-p` value.

??? warning "Wrong port after replugging"

    The port number isn't permanent. Unplug and replug, or connect a second board, and `/dev/ttyACM0` can become `/dev/ttyACM1`. If an upload suddenly fails, re-run `arduino-cli board list` and check the port hasn't moved.

??? warning "`.ino` name doesn't match the folder"

    The main sketch file must share its folder's name. `blink.ino` inside a `BlinkTest/` folder won't be found. Rename one to match the other.

??? warning "Forgetting the core"

    `Platform 'arduino:avr' not found` means you skipped `arduino-cli core install arduino:avr`. No core, no compiler for that chip.

??? warning "Leaving off the `.`"

    `arduino-cli compile --upload -p … --fqbn …` with no path doesn't know which sketch to build. The trailing `.` (the current directory) is the sketch. Run the command from inside the sketch folder and don't drop it.

---

## Practice

??? question "Decode the FQBN"

    A tutorial tells you to upload with `--fqbn esp32:esp32:esp32`. Without looking anything up, what are the three parts telling you, and what would you need to install before this command could work?

    ??? tip "Solution"

        `esp32:esp32:esp32` is `vendor:architecture:board`. The vendor is `esp32` (Espressif), the architecture is `esp32`, and the board is a generic `esp32`. Before it works you'd need that core installed — `arduino-cli core install esp32:esp32` — because `arduino-cli` ships with no board support at all.

??? question "Compile without uploading"

    You've made a risky change and want to check it builds *before* it touches the board. What's the smallest change to the upload command, and why is the separation useful?

    ??? tip "Solution"

        Drop `--upload`:

        ```bash
        arduino-cli compile -p /dev/ttyACM0 --fqbn arduino:avr:uno .
        ```

        `compile` builds and reports errors without writing anything to the board. Keeping compile and upload separate lets you catch mistakes at your desk instead of pushing broken firmware to hardware.

??? question "The upload worked yesterday and fails today"

    Same board, same sketch, same command — but today the upload errors out before it starts. Nothing in the code changed. What's the first thing to check?

    ??? tip "Solution"

        The **port**. Replugging the board (or plugging in another) can shift `/dev/ttyACM0` to `/dev/ttyACM1`. Run `arduino-cli board list`, confirm where the board actually is, and update `-p`. A permission issue (`dialout` group) is the second thing to rule out if you're on a new machine.

---

## Quick Recap

<div class="grid cards two-col" markdown>

-   **Install Once**

    ---

    Drop the binary on your `PATH`, then `core update-index` and `core install arduino:avr`. `arduino-cli` ships with no board support until you add a core.

-   **The Command**

    ---

    `arduino-cli compile --upload -p PORT --fqbn BOARD .` — build and flash in one line. Run it from inside the sketch folder; the `.` is the sketch.

-   **Two Facts the Command Needs**

    ---

    The **port** (where the board is) and the **FQBN** (what the board is). Both come straight from `arduino-cli board list`.

-   **It's C++**

    ---

    Sketches compile as C++, not C. `setup()` runs once, `loop()` runs forever — the core calls them; everything else is an ordinary library function.

</div>

## What's Next

You have a board, a toolchain, and a one-line way to push code to it. The next step is making that code *do* something physical: **[Digital Pins](../digital_io.md)** — how a microcontroller reads a button and drives an LED, and why a pin is either fully on or fully off with nothing in between.

---

## Further Reading

**Official Documentation**

- [arduino-cli Documentation](https://arduino.github.io/arduino-cli/latest/) — the full command reference, including `board`, `core`, `sketch`, and `monitor`
- [arduino-cli Installation](https://arduino.github.io/arduino-cli/latest/installation/) — every install method for macOS, Linux, and Windows
- [Arduino Language Reference](https://docs.arduino.cc/language-reference/) — every core function, organised by category, including Digital I/O

**Related Articles**

- [What Is an Arduino?](../what_is_an_arduino.md) — the board itself, and what `setup()`/`loop()` actually mean
- [Breadboards](breadboards.md) — build the circuit your code runs on before you flash anything to it

