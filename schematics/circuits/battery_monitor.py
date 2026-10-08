"""A battery monitor: a 20 kilohm / 10 kilohm divider scales a 12.6 V battery
(15 V at most) down to one third, 4.2 V (5 V at most), for an Arduino's A0.
Used in docs/voltage_divider.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        bat = d.add(elm.Battery().up().reverse().label("12.6 V\nbattery"))
        d.add(elm.Line().right(3))
        d.add(elm.Resistor().down().label("R1\n20 kΩ"))
        mid = d.add(elm.Dot())
        d.add(elm.Resistor().down().label("R2\n10 kΩ"))
        bot = d.add(elm.Dot())
        d.add(elm.Line().left().tox(bat.start))
        d.add(elm.Line().toy(bat.start))
        d.add(elm.Line().at(mid.center).right(2.5))
        d.add(elm.Dot(open=True).label("Arduino A0\n(4.2 V)", loc="right"))
        d.add(elm.Line().at(bot.center).right(2.5))
        d.add(elm.Dot(open=True).label("Arduino GND", loc="right"))
