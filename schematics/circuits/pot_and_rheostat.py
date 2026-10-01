"""Left: a potentiometer as an adjustable voltage divider (all three terminals,
output taken from the wiper). Right: a variable resistor (rheostat, two
terminals) setting an LED's current, with a fixed 330 ohm resistor in series so
the LED is still protected when the rheostat is turned to zero.
Used in docs/resistor_types.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        # potentiometer divider
        bat = d.add(elm.Battery().up().reverse().label("5 V"))
        d.add(elm.Line().right(3.5))
        pot = d.add(elm.Potentiometer().down().label("10 kΩ pot", loc="top"))
        d.add(elm.Line().left().tox(bat.start))
        d.add(elm.Line().at(pot.tap).right(2))
        d.add(elm.Dot(open=True).label("adjustable\n0–5 V out", loc="right"))
        # rheostat (with a fixed minimum resistor) setting an LED's current
        bat2 = d.add(elm.Battery().at((10, 0)).up().reverse().label("9 V"))
        d.add(elm.Line().right(1))
        d.add(elm.ResistorVar().right().label("rheostat"))
        d.add(elm.Resistor().right().label("330 Ω"))
        d.add(elm.LED().down().toy(bat2.start).label("LED", loc="bottom"))
        d.add(elm.Line().left().tox(bat2.start))
