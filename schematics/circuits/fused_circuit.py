"""A protected circuit: battery, fuse, switch, lamp. The fuse sits right at the
battery's positive terminal so it protects all the wiring after it.
Used in docs/open_short_fuses.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        bat = d.add(elm.Battery().up().reverse().label("12 V"))
        d.add(elm.Fuse().right().label("fuse"))
        d.add(elm.Switch().right().label("switch"))
        d.add(elm.Lamp().down().label("lamp", loc="bottom"))
        d.add(elm.Line().left().tox(bat.start))
        d.add(elm.Line().toy(bat.start))
