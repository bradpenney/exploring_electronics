"""Two 1.5 V cells in series (left loop, 3 V across the load) and two in
parallel (right loop, 1.5 V across the load, double the capacity).
Used in docs/batteries.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        # series: cells stacked + to -, total 3 V
        b1 = d.add(elm.BatteryCell().up().reverse().label("1.5 V", loc="bottom"))
        d.add(elm.BatteryCell().up().reverse().label("1.5 V", loc="bottom"))
        top = d.add(elm.Line().right(2))
        d.add(elm.Resistor().down().toy(b1.start).label("load: 3 V", loc="bottom"))
        d.add(elm.Line().left().tox(b1.start))
        # parallel: two cells side by side, tops joined (+ to +), bottoms joined (- to -)
        p1 = d.add(elm.BatteryCell().at((6, 0)).up().reverse().label("1.5 V", loc="bottom"))
        p2 = d.add(elm.BatteryCell().at((8.5, 0)).up().reverse().label("1.5 V", loc="bottom"))
        d.add(elm.Line().at(p1.end).to(p2.end))
        d.add(elm.Line().at(p2.end).right(2))
        d.add(elm.Resistor().down().toy(p1.start).label("load: 1.5 V", loc="bottom"))
        d.add(elm.Line().left().tox(p1.start))
