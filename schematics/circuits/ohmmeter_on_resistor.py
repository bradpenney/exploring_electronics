"""Measuring resistance: an ohmmeter connected across a single resistor that
has been removed from its circuit (no battery anywhere). The meter supplies its
own small test current. Used in docs/resistance.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        r = d.add(elm.Resistor().right().label("330 Ω"))
        d.add(elm.Line().down(1.5))
        d.add(elm.MeterOhm().left().tox(r.start))
        d.add(elm.Line().up().toy(r.start))
