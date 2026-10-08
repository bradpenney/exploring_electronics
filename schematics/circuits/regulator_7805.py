"""A 7805 fixed regulator: 12 V in, 5 V out, with the 0.22 uF input and
0.1 uF output capacitors TI's LM340/LM7805 datasheet specifies for its
measurements, driving a load. Used in docs/voltage_regulators.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        bat = d.add(elm.Battery().up().reverse().label("12 V"))
        d.add(elm.Line().right(1.5))
        cin = d.add(elm.Dot())
        d.add(elm.Line().right(1))
        reg = d.add(elm.VoltageRegulator().right().anchor("in").label("7805", loc="top", ofst=0.6))
        d.add(elm.Line().at(reg.out).right(1))
        cout = d.add(elm.Dot().label("5 V", loc="top"))
        d.add(elm.Line().right(2.5))
        load = d.add(elm.Resistor().down().toy(bat.start).label("load", loc="bottom"))
        d.add(elm.Line().left().tox(bat.start))
        d.add(elm.Capacitor().at(cin.center).down().toy(bat.start).label("0.22 µF", loc="bottom"))
        d.add(elm.Capacitor().at(cout.center).down().toy(bat.start).label("0.1 µF", loc="bottom"))
        d.add(elm.Line().at(reg.gnd).toy(bat.start))
        d.add(elm.Dot().at((reg.gnd[0], bat.start[1])))
