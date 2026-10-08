"""A full-wave bridge rectifier with a smoothing capacitor: 12 V AC feeds the
bridge's two AC corners (top and bottom); the diodes' cathodes meet at the
right corner (DC +) and their anodes at the left corner (DC -). A 2,200 uF
electrolytic smooths the output across a 100 ohm load.
Used in docs/diodes_and_leds.md.
"""

import schemdraw.elements as elm

from style import STROKE, dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        br = d.add(elm.Rectifier(fill=STROKE).color(STROKE))
        # AC source on the far left, to the top and bottom corners
        d.add(elm.Line().at(br.N).up(0.8))
        top = d.add(elm.Line().left().tox(br.W.x - 2.5))
        src = d.add(elm.SourceSin().down().toy(br.S.y - 0.8).label("12 V AC", loc="top"))
        d.add(elm.Line().right().tox(br.S.x))
        d.add(elm.Line().toy(br.S))
        # DC output: + from the right corner, - from the left corner
        d.add(elm.Line().at(br.E).right(1.5))
        plus = d.add(elm.Dot().label("+", loc="top"))
        d.add(elm.Line().right(2.2))
        load = d.add(elm.Resistor().down(4.2).label("100 Ω load", loc="bottom"))
        bot = d.add(elm.Line().left().tox(plus.center))
        mid = d.add(elm.Dot())
        d.add(elm.Line().left().tox(br.W.x))
        d.add(elm.Line().toy(br.W))
        d.add(elm.Capacitor2(polar=True).at(plus.center).down().toy(mid.center).label("2,200 µF", loc="top"))
    # schemdraw draws the bridge's internal diode leads in black regardless of
    # the drawing colour; recolour them to match the dark theme.
    from pathlib import Path
    p = Path(path)
    p.write_text(p.read_text().replace("stroke:black", f"stroke:{STROKE}"))
