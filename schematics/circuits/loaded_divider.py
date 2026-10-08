"""The same 9 V, 10k/10k divider with a 1 kilohm load connected across its
output: the load sits in parallel with R2, so the output falls to 0.75 V.
Used in docs/voltage_divider.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        bat = d.add(elm.Battery().up().reverse().label("9 V"))
        d.add(elm.Line().right(3))
        d.add(elm.Resistor().down().label("R1\n10 kΩ"))
        mid = d.add(elm.Dot().label("0.75 V", loc="left"))
        d.add(elm.Resistor().down().label("R2\n10 kΩ"))
        bot = d.add(elm.Dot())
        d.add(elm.Line().left().tox(bat.start))
        d.add(elm.Line().toy(bat.start))
        d.add(elm.Line().at(mid.center).right(3))
        d.add(elm.Resistor().down().label("load\n1 kΩ"))
        d.add(elm.Line().left().tox(bot.center))
