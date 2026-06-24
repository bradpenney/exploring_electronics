"""A minimal, complete circuit used as the worked "read this schematic" example
in docs/essential/reading_schematics.md: a 5V battery drives current through a
330 ohm resistor and an LED, back to the battery.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        # .reverse() puts the long (+) plate at the top so the positive terminal
        # feeds the top wire — forward-biasing the LED, which is drawn pointing down.
        bat = d.add(elm.Battery().up().reverse().label("5V"))
        d.add(elm.Line().right().length(1))
        d.add(elm.Resistor().right().label("330 Ω"))
        d.add(elm.Line().right().length(1))
        d.add(elm.LED().down().label("LED", loc="bottom"))
        d.add(elm.Line().left().tox(bat.start))
        d.add(elm.Line().toy(bat.start))
