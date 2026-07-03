"""Input-pin circuit for docs/essential/digital_io.md: a pushbutton read by a
microcontroller digital pin set to INPUT, with a pull-down resistor. Pressing
the button connects the pin to 5V (reads HIGH); the pull-down resistor ties the
pin to ground when the button is open so it reads a definite LOW instead of
floating.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        d.add(elm.Dot(open=True).label("5 V", loc="top"))
        d.add(elm.Button().down().label("Pushbutton", loc="left"))
        node = d.add(elm.Dot())
        # Pull-down leg: straight down from the node through the resistor to ground.
        d.add(elm.Resistor().down().at(node.center).label("10 kΩ pull-down"))
        d.add(elm.Ground())
        # Sense leg: branch right from the node to the input pin.
        d.add(elm.Line().right().length(3).at(node.center))
        d.add(elm.Dot(open=True).label("Pin D2 (INPUT)", loc="right"))
