"""Measuring voltage: a 9 V battery drives a 330 Ω resistor and an LED; a
voltmeter sits in PARALLEL across the resistor, probes on either side of it.
Used in docs/voltage.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        bat = d.add(elm.Battery().up().reverse().label("9 V"))
        d.add(elm.Line().right(1))
        r1 = d.add(elm.Resistor().right().label("330 Ω"))
        d.add(elm.Line().right(1))
        d.add(elm.LED().down().label("LED", loc="bottom"))
        d.add(elm.Line().left().tox(bat.start))
        d.add(elm.Line().toy(bat.start))
        # voltmeter across the resistor (parallel)
        d.add(elm.Line().at(r1.start).up(1.6))
        m = d.add(elm.MeterV().right().tox(r1.end))
        d.add(elm.Line().down().toy(r1.end))
