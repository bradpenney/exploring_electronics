"""The idea of a buck (step-down) switching regulator: a switch chops 12 V on
and off; while it's on, current builds in the inductor; while it's off, the
diode gives that current a path; the capacitor smooths the result to 5 V.
The real controller (LM2596 etc.) that times the switch is left out.
Used in docs/voltage_regulators.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        bat = d.add(elm.Battery().up().reverse().label("12 V"))
        d.add(elm.Line().right(0.5))
        d.add(elm.Switch().right().label("switch\n150 kHz"))
        sw = d.add(elm.Dot())
        d.add(elm.Inductor2().right().label("inductor"))
        out = d.add(elm.Dot().label("5 V", loc="top"))
        d.add(elm.Line().right(3))
        d.add(elm.Resistor().down().toy(bat.start).label("load", loc="bottom"))
        d.add(elm.Line().left().tox(bat.start))
        d.add(elm.Diode().at(sw.center).down().toy(bat.start).reverse().label("diode", loc="top"))
        d.add(elm.Capacitor2(polar=True).at(out.center).down().toy(bat.start).label("capacitor", loc="bottom"))
