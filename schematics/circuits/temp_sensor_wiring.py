"""MCP9700A wired to an Arduino for docs/analog_input.md: VDD to 5V, GND to
ground, and VOUT straight into analog pin A0 — no resistor needed, since the
pin is only measuring a voltage, not driving current through anything.
"""

import schemdraw.elements as elm
from schemdraw.elements.intcircuits import IcPin

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        ic = d.add(
            elm.Ic(
                pins=[
                    IcPin(name="VDD", side="top"),
                    IcPin(name="VOUT", side="right"),
                    IcPin(name="GND", side="bottom"),
                ],
                size=(3, 2.5),
            ).label("MCP9700A", loc="left", ofst=(-2.0, 0))
        )
        d.add(elm.Line().up().at(ic.VDD).length(1.2))
        d.add(elm.Dot(open=True).label("5 V", loc="top"))

        d.add(elm.Line().down().at(ic.GND).length(1.2))
        d.add(elm.Ground())

        d.add(elm.Line().right().at(ic.VOUT).length(2))
        d.add(elm.Dot(open=True).label("Pin A0 (analogRead)", loc="right"))
