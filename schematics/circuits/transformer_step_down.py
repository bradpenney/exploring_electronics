"""A step-down transformer: a 120 V AC source on the primary, a 12 V load on
the secondary. Turns ratio 10:1. Used in docs/magnetism.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        xf = d.add(elm.Transformer(t1=10, t2=4, core=True).label("10 : 1", loc="top"))
        d.add(elm.Line().at(xf.p1).left(1.5))
        src = d.add(elm.SourceSin().down().toy(xf.p2).label("120 V AC", loc="top"))
        d.add(elm.Line().right().tox(xf.p2))
        d.add(elm.Line().at(xf.s1).right(1.5))
        load = d.add(elm.Resistor().down().toy(xf.s2).label("12 V load", loc="bottom"))
        d.add(elm.Line().left().tox(xf.s2))
