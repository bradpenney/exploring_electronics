"""A first power-up on a bench supply: the supply, drawn as a voltage source
labelled with its settings (5 V, current limit 100 mA), feeds a new circuit
through its own built-in ammeter readback. The limit, not the circuit, sets
the worst-case current. Used in docs/tools/bench_power_supply.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        d.config(margin=0.8)  # the long labels sit past the wires
        src = d.add(elm.SourceV().up().label("bench supply\nset: 5 V\nlimit: 100 mA", loc="top", ofst=0.3))
        d.add(elm.Line().right(1))
        d.add(elm.MeterA().right().label("readback", loc="top"))
        d.add(elm.Line().right(1))
        box = d.add(elm.Resistor().down().toy(src.start).label("new circuit\n(the load)", loc="bottom"))
        d.add(elm.Line().left().tox(src.start))
