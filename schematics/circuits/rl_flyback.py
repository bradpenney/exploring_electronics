"""An RL circuit with a flyback diode: a 12 V battery and a switch feed a
100 mH coil whose winding has 20 ohms of resistance (drawn as a separate
resistor). The diode across the coil, cathode to the positive side, gives the
coil's current somewhere to go when the switch opens. Used in docs/inductors.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        bat = d.add(elm.Battery().up().reverse().label("12 V"))
        d.add(elm.Switch().right().label("switch"))
        d.add(elm.Line().right(0.6))
        top = d.add(elm.Dot())
        d.add(elm.Inductor2(loops=4).down().label("100 mH", loc="top"))
        d.add(elm.Resistor().down().label("20 Ω (winding)", loc="top"))
        bot = d.add(elm.Dot())
        d.add(elm.Line().left().tox(bat.start))
        d.add(elm.Line().toy(bat.start))
        d.add(elm.Line().at(top.center).right(2.0))
        d.add(elm.Diode().down().toy(bot.center).reverse().label("flyback diode", loc="bottom"))
        d.add(elm.Line().left().tox(bot.center))
