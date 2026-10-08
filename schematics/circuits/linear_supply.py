"""A complete linear power supply: a transformer steps mains down and isolates
it, a bridge rectifier turns AC into humps, a filter capacitor smooths them,
and a regulator holds the output steady. Used in docs/voltage_regulators.md.
"""

from pathlib import Path

import schemdraw.elements as elm

from style import STROKE, dark_drawing


def build(path):
    with dark_drawing(file=str(path)) as d:
        br = d.add(elm.Rectifier(fill=STROKE).color(STROKE))
        # transformer secondary feeds the bridge's two AC corners
        d.add(elm.Line().at(br.N).up(0.8))
        d.add(elm.Line().left().tox(br.W.x - 1.5))
        t = d.add(elm.Transformer().right().anchor("s1").label("transformer", loc="top", ofst=0.3))
        d.add(elm.Line().at(t.s2).down().toy(br.S.y - 0.8))
        d.add(elm.Line().right().tox(br.S.x))
        d.add(elm.Line().toy(br.S))
        # mains into the primary
        d.add(elm.Line().at(t.p1).left(2.6))
        d.add(elm.SourceSin().down().toy(t.p2).label("120 V AC\nmains", loc="top", ofst=0.3))
        d.add(elm.Line().right().tox(t.p2.x))
        # DC side
        d.add(elm.Line().at(br.E).right(1.2))
        plus = d.add(elm.Dot())
        d.add(elm.Line().right(1.0))
        reg = d.add(elm.VoltageRegulator().right().anchor("in").label("regulator", loc="top", ofst=0.6))
        d.add(elm.Line().at(reg.out).right(1.2))
        outx = reg.out[0] + 1.2
        d.add(elm.Dot(open=True).label("steady DC", loc="right"))
        gnd_y = br.S.y - 1.8
        d.add(elm.Line().at(br.W).down().toy(gnd_y))
        d.add(elm.Line().right().tox(outx))
        d.add(elm.Dot(open=True).label("0 V", loc="right"))
        d.add(elm.Capacitor2(polar=True).at(plus.center).down().toy(gnd_y).label("filter", loc="bottom"))
        d.add(elm.Line().at(reg.gnd).toy(gnd_y))
        d.add(elm.Dot().at((reg.gnd[0], gnd_y)))
        d.add(elm.Dot().at((plus.center[0], gnd_y)))
    p = Path(path)
    p.write_text(p.read_text().replace("stroke:black", f"stroke:{STROKE}"))
