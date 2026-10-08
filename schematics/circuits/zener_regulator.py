"""A Zener shunt regulator: 9 V through a 390 ohm resistor to a 1N4733A
(5.1 V) Zener, connected in reverse, holding the output near 5.1 V.
Used in docs/diodes_and_leds.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        bat = d.add(elm.Battery().up().reverse().label("9 V"))
        d.add(elm.Resistor().right().label("390 Ω"))
        top = d.add(elm.Dot())
        d.add(elm.Zener().down().reverse().label("5.1 V", loc="bottom"))
        bot = d.add(elm.Dot())
        d.add(elm.Line().left().tox(bat.start))
        d.add(elm.Line().at(top.center).right(1.5))
        d.add(elm.Dot(open=True).label("5.1 V out", loc="right"))
        d.add(elm.Line().at(bot.center).right(1.5))
        d.add(elm.Dot(open=True).label("0 V", loc="right"))
