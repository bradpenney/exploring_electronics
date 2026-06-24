"""Series switch circuit: 5V supply, current-limiting resistor, two buttons
wired in series, and an LED. Both buttons must be pressed to complete the
single current path. Mirrors the breadboard build in
docs/essential/series_and_parallel.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        # .reverse() puts the long (+) plate at the top so the positive terminal
        # feeds the top wire, forward-biasing the downward-drawn LED.
        bat = d.add(elm.Battery().up().reverse().label("5V"))
        d.add(elm.Resistor().right().label("220 Ω"))
        d.add(elm.Button().right().label("SW1"))
        d.add(elm.Button().right().label("SW2"))
        d.add(elm.LED().down().label("LED", loc="bottom"))
        d.add(elm.Line().left().tox(bat.start))
        d.add(elm.Line().toy(bat.start))
