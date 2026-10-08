"""Left: the vacuum diode and triode symbols, with their electrodes labelled.
Right: a common-cathode triode amplifier stage: plate resistor up to the
high-voltage supply (B+), grid resistor and input on the grid, cathode resistor
to ground. Heaters are omitted, as on most schematics. Values are left off:
the point is the shape. Used in docs/vacuum_tubes.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        # symbol reference
        dio = d.add(elm.TubeDiode(heater=True).at((0, 0)).label("diode", loc="bottom", ofst=0.6))
        d.add(elm.Label().at(dio.anode).label("plate", loc="top"))
        tri = d.add(elm.Triode(heater=True).at((3.2, 0)).label("triode", loc="bottom", ofst=0.6))
        d.add(elm.Label().at(tri.anode).label("plate", loc="top"))
        d.add(elm.Line().at(tri.grid).left(0.4))
        d.add(elm.Label().label("grid", loc="left"))
        # common-cathode stage
        t = d.add(elm.Triode().at((12, 0)))
        d.add(elm.Resistor().at(t.anode).up().label("plate\nresistor"))
        d.add(elm.Vdd().label("B+ (hundreds of volts)"))
        d.add(elm.Line().at(t.anode).right(1.5))
        d.add(elm.Dot(open=True).label("output", loc="right"))
        d.add(elm.Line().at(t.grid).left(2.8))
        gd = d.add(elm.Dot())
        d.add(elm.Line().left(1))
        d.add(elm.Dot(open=True).label("input", loc="left"))
        d.add(elm.Resistor().at(gd.center).down().label("grid\nresistor", loc="top"))
        d.add(elm.Ground())
        d.add(elm.Resistor().at(t.cathode).down().label("cathode\nresistor"))
        d.add(elm.Ground())
