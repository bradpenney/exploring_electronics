"""An AC source driving a lamp: the sine-wave source symbol (a circle with a
tilde) and a resistive load. Used in docs/ac_dc.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        src = d.add(elm.SourceSin().up().label("120 V\n60 Hz"))
        d.add(elm.Line().right(2))
        d.add(elm.Lamp().down().label("100 W lamp", loc="bottom"))
        d.add(elm.Line().left().tox(src.start))
