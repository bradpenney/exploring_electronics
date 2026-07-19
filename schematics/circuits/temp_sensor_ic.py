"""Generic analog temperature sensor IC for docs/temperature_sensors.md: a
three-pin package (VDD, VOUT, GND) — the same pinout shared by the MCP9700A
and most analog temperature ICs, shown on its own before any microcontroller
enters the picture.
"""

import schemdraw.elements as elm
from schemdraw.elements.intcircuits import IcPin

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        d.add(
            elm.Ic(
                pins=[
                    IcPin(name="VDD", side="top"),
                    IcPin(name="VOUT", side="right"),
                    IcPin(name="GND", side="bottom"),
                ],
                size=(3, 2.5),
            ).label("Analog Temp\nSensor", loc="left", ofst=(-2.6, 0))
        )
