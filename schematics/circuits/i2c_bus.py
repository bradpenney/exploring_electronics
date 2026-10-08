"""An I2C bus on an Arduino Uno: SDA (A4) and SCL (A5) each pulled up to 5 V
through 4.7 kilohms, shared by two MCP9808 temperature sensors at addresses
0x18 and 0x19 (set by their A0 pins). Used in docs/i2c.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def _sensor(d, x, y, label):
    return d.add(elm.Ic(pins=[elm.IcPin(name="SDA", side="top", slot="1/2"),
                              elm.IcPin(name="SCL", side="top", slot="2/2")],
                        size=(2.2, 1.4)).theta(0).label(label, loc="bottom").at((x, y)).anchor("SDA"))


def build(path):
    with dark_drawing(file=str(path)) as d:
        uno = d.add(elm.Ic(pins=[elm.IcPin(name="SDA (A4)", side="right", slot="2/2"),
                                 elm.IcPin(name="SCL (A5)", side="right", slot="1/2")],
                           size=(2.6, 2.4)).label("Arduino Uno", loc="top"))
        sda_y, scl_y = uno["SDA (A4)"][1], uno["SCL (A5)"][1]
        x0 = uno["SDA (A4)"][0]
        # bus lines
        d.add(elm.Line().at(uno["SDA (A4)"]).right(9))
        d.add(elm.Label().label("SDA", loc="right"))
        d.add(elm.Line().at(uno["SCL (A5)"]).right(9))
        d.add(elm.Label().label("SCL", loc="right"))
        # pull-ups to 5 V
        for k, y in enumerate((sda_y, scl_y)):
            x = x0 + 1.4 + k * 1.2
            d.add(elm.Dot().at((x, y)))
            d.add(elm.Resistor().at((x, y)).up().toy(sda_y + 3.0).label("4.7 kΩ", loc="top" if k == 0 else "bottom"))
        d.add(elm.Line().at((x0 + 1.4, sda_y + 3.0)).right(1.2))
        d.add(elm.Vdd().at((x0 + 2.0, sda_y + 3.0)).label("5 V"))
        # two sensors hanging off the bus
        for k, (x, lab) in enumerate(((x0 + 4.6, "MCP9808\n0x18"), (x0 + 7.4, "MCP9808\n0x19"))):
            s = _sensor(d, x, scl_y - 1.6, lab)
            d.add(elm.Line().at(s.SDA).toy(sda_y))
            d.add(elm.Dot())
            d.add(elm.Line().at(s.SCL).toy(scl_y))
            d.add(elm.Dot())
