"""The basic voltage divider: a 9 V battery across two 10 kilohm resistors in
series, with the output taken from the point between them (4.5 V).
Used in docs/voltage_divider.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        bat = d.add(elm.Battery().up().reverse().label("9 V"))
        d.add(elm.Line().right(3))
        d.add(elm.Resistor().down().label("R1\n10 kΩ"))
        mid = d.add(elm.Dot())
        d.add(elm.Resistor().down().label("R2\n10 kΩ"))
        bot = d.add(elm.Dot())
        d.add(elm.Line().left().tox(bat.start))
        d.add(elm.Line().toy(bat.start))
        d.add(elm.Line().at(mid.center).right(2.5))
        d.add(elm.Dot(open=True).label("Vout = 4.5 V", loc="right"))
        d.add(elm.Line().at(bot.center).right(2.5))
        d.add(elm.Dot(open=True).label("0 V", loc="right"))
