"""Combined series + parallel circuit: a 5V supply feeds two parallel branches,
each branch a current-limiting resistor in series with its own LED. The resistor
and LED in a branch are in series; the two branches are in parallel. Mirrors the
"Real Circuits Use Both" example in docs/essential/series_and_parallel.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        # .reverse() puts the long (+) plate at the top so the positive terminal
        # feeds the top wire, forward-biasing the downward-drawn LEDs.
        bat = d.add(elm.Battery().up().reverse().label("5V"))
        # Top rail, with a branch-point dot above each branch.
        d.add(elm.Line().right().length(3))
        top1 = d.add(elm.Dot())
        d.add(elm.Line().right().length(3))
        top2 = d.add(elm.Dot())

        # Branch 1: resistor in series with LED 1.
        d.add(elm.Resistor().down().at(top1.center).label("220 Ω"))
        d.add(elm.LED().down().label("LED 1", loc="bottom"))
        bot1 = d.add(elm.Dot())

        # Branch 2: resistor in series with LED 2.
        d.add(elm.Resistor().down().at(top2.center).label("220 Ω"))
        d.add(elm.LED().down().label("LED 2", loc="bottom"))
        bot2 = d.add(elm.Dot())

        # Bottom rail back to the battery.
        d.add(elm.Line().at(bot2.center).left().tox(bot1.center))
        d.add(elm.Line().left().tox(bat.start))
        d.add(elm.Line().toy(bat.start))
