"""An NPN low-side switch: an Arduino pin drives a P2N2222A's base through a
270 ohm resistor; the transistor switches a 12 V, 150 mA fan, with a
flyback diode across the fan. Used in docs/transistors.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        q = d.add(elm.BjtNpn(circle=True).label("P2N2222A", loc="right"))
        d.add(elm.Resistor().at(q.base).left().label("270 Ω"))
        d.add(elm.Dot(open=True).label("Arduino pin", loc="left"))
        d.add(elm.Ground().at(q.emitter))
        d.add(elm.Line().at(q.collector).up(0.5))
        top = d.add(elm.Dot())
        d.add(elm.Motor().up().label("12 V fan", loc="top"))
        sup = d.add(elm.Dot())
        d.add(elm.Line().up(0.5))
        d.add(elm.Vdd().label("+12 V"))
        d.add(elm.Line().at(top.center).right(1.8))
        d.add(elm.Diode().up().toy(sup.center).label("1N4001", loc="bottom"))
        d.add(elm.Line().left().tox(sup.center))
