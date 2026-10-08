"""An RC charging circuit: a 9 V battery charges a 100 uF electrolytic
capacitor through a 10 kilohm resistor when the switch closes; a voltmeter
across the capacitor watches it rise. Time constant 10 k x 100 u = 1 s.
Used in docs/capacitors.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        bat = d.add(elm.Battery().up().reverse().label("9 V"))
        d.add(elm.Switch().right().label("switch"))
        d.add(elm.Resistor().right().label("10 kΩ"))
        top = d.add(elm.Dot())
        cap = d.add(elm.Capacitor2(polar=True).down().label("100 µF", loc="top", ofst=0.3))
        bot = d.add(elm.Dot())
        d.add(elm.Line().left().tox(bat.start))
        d.add(elm.Line().toy(bat.start))
        d.add(elm.Line().at(top.center).right(2.5))
        d.add(elm.MeterV().down())
        d.add(elm.Line().left().tox(bot.center))
