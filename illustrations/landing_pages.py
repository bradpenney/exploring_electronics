#!/usr/bin/env python3
"""Clickable transit maps for the four topic landing pages (circuit_foundations,
components, microcontrollers, practical_tools). Stops and stages mirror each
page's numbered lists: keep them in sync when an article is added.

Hrefs are written as built URLs relative to the landing page (`../voltage/`),
because inlined HTML isn't rewritten by MkDocs; htmlproofer checks them.

Usage:
    python3 illustrations/landing_pages.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from transit import transit_map  # noqa: E402
from style3d import render_all  # noqa: E402

OUT = HERE.parent / "docs" / "images" / "landing"

AMBER, TEAL, PURPLE, BLUE, GREEN = "#f59e0b", "#38b2ac", "#9f7aea", "#4299e1", "#48bb78"


def _desc(intro, stages):
    parts = [f"{name}: " + ", ".join(" ".join(lines) for lines, _ in stops) for name, _, stops in stages]
    return intro + " " + "; ".join(parts) + ". Every stop is a link to its article."


CF = [
    ("What electricity is made of", AMBER, [
        (["Conductors"], "../conductors_and_insulators/"),
        (["What Is", "Electricity?"], "../what_is_electricity/"),
        (["Prefixes"], "../metric_prefixes/")]),
    ("The three quantities", TEAL, [
        (["Voltage"], "../voltage/"),
        (["Current"], "../current/"),
        (["Resistance"], "../resistance/")]),
    ("Putting them to work", PURPLE, [
        (["Ohm's Law", "and Power"], "../ohms_law/"),
        (["Opens, Shorts,", "and Fuses"], "../open_short_fuses/")]),
    ("Beyond steady DC", BLUE, [
        (["AC vs DC"], "../ac_dc/"),
        (["Magnetism"], "../magnetism/")]),
    ("Combining and storing", GREEN, [
        (["Series and", "Parallel"], "../series_and_parallel/"),
        (["Voltage", "Dividers"], "../voltage_divider/"),
        (["Capacitors"], "../capacitors/"),
        (["Inductors"], "../inductors/")]),
]

COMPONENTS = [
    ("Resistors", AMBER, [
        (["Color Codes"], "../resistor_color_codes/"),
        (["Resistor Types"], "../resistor_types/")]),
    ("Valves for current", PURPLE, [
        (["Diodes", "and LEDs"], "../diodes_and_leds/"),
        (["Transistors"], "../transistors/"),
        (["Vacuum Tubes"], "../vacuum_tubes/")]),
    ("Sensors and packages", GREEN, [
        (["Temperature", "Sensors"], "../temperature_sensors/"),
        (["Package Types"], "../package_types/")]),
]

MICRO = [
    ("Meet the board", AMBER, [
        (["What Is an", "Arduino?"], "../what_is_an_arduino/"),
        (["Digital Pins"], "../digital_io/")]),
    ("Outputs and inputs", TEAL, [
        (["Blink an LED"], "../blink_an_led/"),
        (["Pull-up and", "Pull-down"], "../pull_resistors/")]),
    ("Measuring the world", PURPLE, [
        (["Analog Sensor"], "../analog_input/"),
        (["Threshold", "Ladder"], "../threshold_output/")]),
]

COMMS = [
    ("Point to point", AMBER, [
        (["Serial"], "../serial_communication/")]),
    ("Shared buses", TEAL, [
        (["I²C"], "../i2c/"),
        (["SPI"], "../spi/")]),
]

POWER = [
    ("Storing it", AMBER, [
        (["Cells and", "Batteries"], "../batteries/")]),
    ("Steadying it", GREEN, [
        (["Voltage", "Regulators"], "../voltage_regulators/")]),
]

TOOLS = [
    ("On the shelf", AMBER, [
        (["Breadboards"], "../tools/breadboards/"),
        (["arduino-cli"], "../tools/arduino_cli/"),
        (["Multimeter"], "../tools/multimeter/"),
        (["Bench", "Supply"], "../tools/bench_power_supply/"),
        (["Soldering"], "../tools/soldering/")]),
    ("Multimeter settings, taught in Circuit Foundations", TEAL, [
        (["Voltage"], "../voltage/#measuring-voltage"),
        (["Current"], "../current/#measuring-current"),
        (["Resistance"], "../resistance/#measuring-resistance"),
        (["Continuity"], "../open_short_fuses/#continuity-testing-for-a-complete-path")]),
]


def circuit_foundations():
    return transit_map("cf", "Circuit Foundations reading order, as a transit map",
                       _desc("One line snaking through fourteen stops in five stages.", CF), CF, [6, 4, 4])


def components():
    return transit_map("co", "Components reading order, as a transit map",
                       _desc("One line through seven stops in three stages.", COMPONENTS), COMPONENTS, [7])


def microcontrollers():
    return transit_map("mc", "Microcontrollers reading order, as a transit map",
                       _desc("One line through six stops in three stages.", MICRO), MICRO, [6])


def communication():
    return transit_map("cm", "Communication reading order, as a transit map",
                       _desc("One line through three stops.", COMMS), COMMS, [3])


def power():
    return transit_map("pw", "Power reading order, as a transit map",
                       _desc("One line through two stops.", POWER), POWER, [2])


def practical_tools():
    return transit_map("pt", "Practical Tools and multimeter settings, as a transit map",
                       _desc("Two separate lines: the tool articles, and the multimeter settings.", TOOLS),
                       TOOLS, [5, 4], connected=False, numbered=False,
                       hint="Click any stop to open it")


FIGURES = {"circuit_foundations.svg": circuit_foundations, "components.svg": components,
           "microcontrollers.svg": microcontrollers, "power.svg": power, "communication.svg": communication, "practical_tools.svg": practical_tools}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
