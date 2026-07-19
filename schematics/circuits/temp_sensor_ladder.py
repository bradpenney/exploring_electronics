"""Full threshold-ladder circuit for docs/threshold_output.md: the same
MCP9700A from temp_sensor_wiring.py feeding A0, plus three LEDs on digital
pins 4, 5, and 6, each through its own 220 Ω resistor to ground. The sketch
lights zero, one, two, or three of them depending on how far the temperature
has climbed.
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
                size=(2.6, 2.2),
            ).label("MCP9700A", loc="left", ofst=(-1.8, 0))
        )
        d.add(elm.Line().up().at(ic.VDD).length(1))
        d.add(elm.Dot(open=True).label("5 V", loc="top"))
        d.add(elm.Line().down().at(ic.GND).length(1))
        d.add(elm.Ground())
        d.add(elm.Line().right().at(ic.VOUT).length(1.5))
        d.add(elm.Dot(open=True).label("A0", loc="top"))

        # Three LED branches, one per digital pin, laid out left to right.
        pins = ["D4", "D5", "D6"]
        for i, pin in enumerate(pins):
            x = 6 + i * 3
            d.add(elm.Dot(open=True).at((x, 2)).label(f"Pin {pin}", loc="top"))
            d.add(elm.Resistor().down().at((x, 2)).label("220 Ω"))
            d.add(elm.LED().down().label(f"LED {i + 1}", loc="right"))
            d.add(elm.Ground())
