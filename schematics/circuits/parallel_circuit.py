"""Parallel switch circuit: 5V supply and a shared current-limiting resistor
feed two buttons on parallel branches into a single LED. Pressing either
button completes a path. Mirrors the breadboard build in
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
        # Top node where the two parallel branches split.
        split = d.add(elm.Dot())
        d.push()
        d.add(elm.Button().right().label("SW1"))
        merge_top = d.add(elm.Dot())
        d.pop()
        # Second branch below the first.
        d.add(elm.Line().down().length(2))
        d.add(elm.Button().right().label("SW2"))
        d.add(elm.Line().up().length(2))
        d.add(elm.Dot())
        # From the merge node, down through the LED and back to the battery.
        d.add(elm.LED().at(merge_top.center).down().label("LED", loc="bottom"))
        d.add(elm.Line().left().tox(bat.start))
        d.add(elm.Line().toy(bat.start))
        _ = split  # split dot kept for visual clarity of the branch point
