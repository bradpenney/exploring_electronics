"""Measuring power: the 9 V / 330 Ω / LED loop with an ammeter in series and a
voltmeter across the LED. Multiply the two readings to get the LED's power.
Used in docs/ohms_law.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        bat = d.add(elm.Battery().up().reverse().label("9 V"))
        d.add(elm.MeterA().right())
        d.add(elm.Resistor().right().label("330 Ω"))
        top = d.add(elm.Line().right(1))
        led = d.add(elm.LED().down().label("LED", loc="top"))
        d.add(elm.Line().left().tox(bat.start))
        d.add(elm.Line().toy(bat.start))
        # voltmeter across the LED
        d.add(elm.Line().at(led.start).right(3))
        d.add(elm.MeterV().down().toy(led.end))
        d.add(elm.Line().left().tox(led.end))
