"""Three kinds of transformer as schematics. Left: an isolation transformer,
1:1, two separate windings on an iron core. Middle: a centre-tapped secondary,
giving two equal voltages either side of the tap. Right: an autotransformer,
one winding with a tap, so input and output share a connection (no isolation).
Used in docs/magnetism.md.
"""

import schemdraw.elements as elm

from style import dark_drawing


def _leads(d, t, right_pins):
    d.add(elm.Line().at(t.p1).left(1.0))
    d.add(elm.Dot(open=True))
    d.add(elm.Line().at(t.p2).left(1.0))
    d.add(elm.Dot(open=True))
    for pin in right_pins:
        d.add(elm.Line().at(pin).right(1.0))
        d.add(elm.Dot(open=True))


def build(path):
    with dark_drawing(file=str(path)) as d:
        d.config(margin=0.6)
        iso = d.add(elm.Transformer(t1=4, t2=4, core=True).at((0, 0)))
        _leads(d, iso, (iso.s1, iso.s2))
        d.add(elm.Label().at(((iso.p2[0] + iso.s2[0]) / 2, iso.p2[1] - 1.0)).label("isolation, 1:1"))

        ct = d.add(elm.Transformer(t1=4, t2=[2, 2], core=True).at((6, 0)))
        _leads(d, ct, (ct.s3, ct.s2))
        d.add(elm.Line().at(ct.s1).to(ct.s4))
        mid = ((ct.s1[0] + ct.s4[0]) / 2, (ct.s1[1] + ct.s4[1]) / 2)
        d.add(elm.Dot().at(mid))
        d.add(elm.Line().at(mid).right(1.0))
        d.add(elm.Dot(open=True).label("tap", loc="right"))
        d.add(elm.Label().at(((ct.p2[0] + ct.s2[0]) / 2, ct.p2[1] - 1.0)).label("centre-tapped"))

        coil = d.add(elm.Inductor2(loops=6).at((14, 2.2)).down().toy(-0.6))
        d.add(elm.Line().at(coil.start).left(1.4))
        d.add(elm.Dot(open=True).label("in", loc="left"))
        d.add(elm.Line().at(coil.end).left(1.4))
        d.add(elm.Dot(open=True))
        tap_y = (coil.start[1] + coil.end[1]) / 2
        d.add(elm.Dot().at((coil.start[0], tap_y)))
        d.add(elm.Line().at((coil.start[0], tap_y)).right(1.4))
        d.add(elm.Dot(open=True).label("out", loc="right"))
        d.add(elm.Dot().at(coil.end))
        d.add(elm.Line().at(coil.end).right(1.4))
        d.add(elm.Dot(open=True))
        d.add(elm.Label().at((coil.start[0], coil.end[1] - 1.0)).label("autotransformer"))
