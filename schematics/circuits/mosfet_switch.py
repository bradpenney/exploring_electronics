"""An N-channel MOSFET low-side switch: an Arduino pin drives an IRLZ44N's
gate through 220 ohms, a 10 kilohm pull-down holds it off while the pin
floats, and the MOSFET switches a 12 V load with a flyback diode.
Used in docs/transistors.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        q = d.add(elm.NFet(bulk=False).reverse().label("IRLZ44N", loc="right"))
        d.add(elm.Line().at(q.gate).left(1.0))
        g = d.add(elm.Dot())
        d.add(elm.Resistor().left().label("220 Ω"))
        d.add(elm.Dot(open=True).label("Arduino pin", loc="left"))
        d.add(elm.Resistor().at(g.center).down().label("10 kΩ", loc="bottom"))
        d.add(elm.Ground())
        d.add(elm.Ground().at(q.source))
        d.add(elm.Line().at(q.drain).up(0.5))
        top = d.add(elm.Dot())
        d.add(elm.Motor().up().label("12 V load", loc="top"))
        sup = d.add(elm.Dot())
        d.add(elm.Line().up(0.5))
        d.add(elm.Vdd().label("+12 V"))
        d.add(elm.Line().at(top.center).right(1.8))
        d.add(elm.Diode().up().toy(sup.center).label("1N4001", loc="bottom"))
        d.add(elm.Line().left().tox(sup.center))
