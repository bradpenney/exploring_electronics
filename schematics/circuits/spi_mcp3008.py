"""An MCP3008 analog-to-digital converter on an Arduino Uno's SPI pins:
13 (SCK) to CLK, 11 (COPI) to DIN, 12 (CIPO) from DOUT, 10 (CS) to CS/SHDN.
A 10 kilohm potentiometer between 5 V and ground feeds channel 0; VDD and
VREF are 5 V. Used in docs/spi.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        uno = d.add(elm.Ic(pins=[elm.IcPin(name="13 SCK", side="right", slot="4/4"),
                                 elm.IcPin(name="11 COPI", side="right", slot="3/4"),
                                 elm.IcPin(name="12 CIPO", side="right", slot="2/4"),
                                 elm.IcPin(name="10 CS", side="right", slot="1/4")],
                           size=(2.6, 4)).label("Arduino Uno", loc="top"))
        adc = d.add(elm.Ic(pins=[elm.IcPin(name="CLK", side="left", slot="4/4"),
                                 elm.IcPin(name="DIN", side="left", slot="3/4"),
                                 elm.IcPin(name="DOUT", side="left", slot="2/4"),
                                 elm.IcPin(name="CS", side="left", slot="1/4"),
                                 elm.IcPin(name="CH0", side="right", slot="3/4")],
                           size=(2.6, 4)).label("MCP3008", loc="top")
                    .at((uno["13 SCK"][0] + 5, uno["13 SCK"][1])).anchor("CLK"))
        for a, b in (("13 SCK", "CLK"), ("11 COPI", "DIN"), ("12 CIPO", "DOUT"), ("10 CS", "CS")):
            d.add(elm.Line().at(uno[a]).right().tox(adc[b]))
        # potentiometer divider into CH0
        d.add(elm.Line().at(adc.CH0).right(1.2))
        tap = d.add(elm.Dot())
        pot = d.add(elm.Potentiometer().at((tap.center[0] + 1.6, tap.center[1] + 1.5)).down().flip().label("10 kΩ", loc="bottom").anchor("start"))
        d.add(elm.Vdd().at(pot.start).label("5 V"))
        d.add(elm.Ground().at(pot.end))
        d.add(elm.Line().at(pot.tap).left().tox(tap.center))
