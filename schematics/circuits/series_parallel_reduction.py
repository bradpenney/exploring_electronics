"""A series-parallel network to reduce step by step: a 9 V battery feeds a
100 ohm resistor in series with a 300 ohm and a 600 ohm resistor in parallel.
Total 300 ohms, 30 mA; 3 V across the 100 ohm, 6 V across the pair.
Used in docs/series_and_parallel.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        bat = d.add(elm.Battery().up().reverse().label("9 V"))
        d.add(elm.Resistor().right().label("R1\n100 Ω"))
        top = d.add(elm.Dot())
        r2 = d.add(elm.Resistor().down().label("R2\n300 Ω", loc="bottom"))
        bot = d.add(elm.Dot())
        d.add(elm.Line().left().tox(bat.start))
        d.add(elm.Line().toy(bat.start))
        d.add(elm.Line().at(top.center).right(3))
        d.add(elm.Resistor().down().label("R3\n600 Ω"))
        d.add(elm.Line().left().tox(bot.center))
