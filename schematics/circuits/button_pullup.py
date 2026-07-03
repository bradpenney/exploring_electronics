"""Input-pin circuit with a pull-up resistor for docs/essential/pull_resistors.md:
the resistor ties the pin to 5V so it rests HIGH; pressing the button connects
the pin to ground, so it reads LOW while held. The mirror image of the
pull-down arrangement in button_pulldown.py.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        d.add(elm.Dot(open=True).label("5 V", loc="top"))
        # Pull-up leg: the resistor sits between 5V and the pin's node.
        d.add(elm.Resistor().down().label("10 kΩ pull-up"))
        node = d.add(elm.Dot())
        # The button connects the node straight to ground when pressed.
        d.add(elm.Button().down().at(node.center).label("Pushbutton", loc="left"))
        d.add(elm.Ground())
        # Sense leg: branch right from the node to the input pin.
        d.add(elm.Line().right().length(3).at(node.center))
        d.add(elm.Dot(open=True).label("Pin D2 (INPUT)", loc="right"))
