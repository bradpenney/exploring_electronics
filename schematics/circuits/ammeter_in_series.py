"""Measuring current: the same 9 V / 330 Ω / LED loop as
voltmeter_across_resistor.py, with an ammeter inserted IN SERIES so the loop's
whole current flows through it. Used in docs/current.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        bat = d.add(elm.Battery().up().reverse().label("9 V"))
        d.add(elm.MeterA().right())
        d.add(elm.Resistor().right().label("330 Ω"))
        d.add(elm.LED().down().label("LED", loc="bottom"))
        d.add(elm.Line().left().tox(bat.start))
        d.add(elm.Line().toy(bat.start))
