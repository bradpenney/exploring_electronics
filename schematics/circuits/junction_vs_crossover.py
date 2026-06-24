"""The single most important schematic-reading rule, drawn two ways: wires that
cross WITH a dot are connected; wires that cross WITHOUT a dot just pass over
each other. Used in docs/essential/reading_schematics.md.
"""

import schemdraw.elements as elm

from style import dark_drawing, LABEL


def _cross(d, cx, cy, connected):
    """Draw a + shaped wire crossing centred on (cx, cy)."""
    d.add(elm.Line().at((cx - 1.4, cy)).right().length(2.8))   # horizontal wire
    d.add(elm.Line().at((cx, cy - 1.4)).up().length(2.8))      # vertical wire
    if connected:
        d.add(elm.Dot().at((cx, cy)))


def build(path):
    with dark_drawing(file=str(path)) as d:
        _cross(d, 0, 0, connected=True)
        d.add(elm.Label().at((0, -2.4)).label("Connected", color=LABEL, fontsize=12))

        _cross(d, 5, 0, connected=False)
        d.add(elm.Label().at((5, -2.4)).label("Just crossing", color=LABEL, fontsize=12))
