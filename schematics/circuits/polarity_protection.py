"""Reverse-polarity protection: a diode in series with the positive lead from
a 13.8 V supply to a transceiver. Connected the right way it conducts (and
drops about 0.9 V); reversed, it blocks. Used in docs/diodes_and_leds.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        bat = d.add(elm.Battery().up().reverse().label("13.8 V"))
        d.add(elm.Diode().right().label("1N5400"))
        d.add(elm.Line().right(1))
        d.add(elm.Resistor().down().label("radio", loc="bottom"))
        d.add(elm.Line().left().tox(bat.start))
