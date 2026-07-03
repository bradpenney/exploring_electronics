"""Output-pin circuit for docs/essential/digital_io.md: a microcontroller
digital pin set to OUTPUT drives an LED through a current-limiting resistor to
ground. Driving the pin HIGH lights the LED; LOW turns it off.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        # The pin is the source: an open terminal labelled as the GPIO pin.
        d.add(elm.Dot(open=True).label("Pin D3 (OUTPUT)", loc="left"))
        d.add(elm.Resistor().down().label("220 Ω"))
        # LED drawn downward so it is forward-biased from the HIGH pin to ground.
        d.add(elm.LED().down().label("LED", loc="right"))
        d.add(elm.Ground())
