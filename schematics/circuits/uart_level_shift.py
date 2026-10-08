"""Serial between a 5 V Arduino Uno and a 3.3 V device: TX crosses to RX each
way, grounds joined. The Uno's 5 V TX passes through a 1 k / 2 k divider
(3.33 V) into the device's RX; the device's 3.3 V TX goes straight to the
Uno's RX (above the ATmega328P's 3 V input-high threshold).
Used in docs/serial_communication.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        uno = d.add(elm.Ic(pins=[elm.IcPin(name="TX", side="right", slot="3/3"),
                                 elm.IcPin(name="GND", side="right", slot="2/3"),
                                 elm.IcPin(name="RX", side="right", slot="1/3")],
                           size=(2.4, 4)).label("Arduino Uno (5 V)", loc="top"))
        dev = d.add(elm.Ic(pins=[elm.IcPin(name="RX", side="left", slot="3/3"),
                                 elm.IcPin(name="GND", side="left", slot="2/3"),
                                 elm.IcPin(name="TX", side="left", slot="1/3")],
                           size=(2.4, 4)).label("3.3 V device", loc="top")
                    .at((uno.TX[0] + 8, uno.TX[1])).anchor("RX"))
        d.add(elm.Line().at(uno.TX).right(1))
        d.add(elm.Resistor().right().label("1 kΩ"))
        mid = d.add(elm.Dot())
        d.add(elm.Line().right().tox(dev.RX))
        d.add(elm.Line().at(dev.TX).left().tox(uno.RX))
        d.add(elm.Line().at(uno.GND).right().tox(dev.GND))
        d.add(elm.Dot().at((mid.center[0], uno.GND[1])))
        d.add(elm.Resistor().at(mid.center).down().toy(uno.GND).label("2 kΩ", loc="bottom"))
