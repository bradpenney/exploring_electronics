"""Second reference chart: the symbols the Circuit Foundations articles add
beyond the first dozen (meters, sources, protection, magnetics), plus the IEC
rectangle resistor that European and many Canadian drawings use. Same grid
layout as symbol_reference.py. Used in docs/reading_schematics.md.
"""

import schemdraw.elements as elm

from style import dark_drawing, LABEL

SYMBOLS = [
    (lambda: elm.ResistorIEC().right().length(1.8), "Resistor (IEC style)"),
    (lambda: elm.ResistorVar().right().length(1.8), "Variable resistor"),
    (lambda: elm.Fuse().right().length(1.8), "Fuse"),
    (lambda: elm.BatteryCell().right().length(1.8), "Single cell"),
    (lambda: elm.SourceSin().right().length(1.8), "AC source"),
    (lambda: elm.Lamp().right().length(1.8), "Lamp"),
    (lambda: elm.MeterV().right().length(1.8), "Voltmeter"),
    (lambda: elm.MeterA().right().length(1.8), "Ammeter"),
    (lambda: elm.MeterOhm().right().length(1.8), "Ohmmeter"),
]

COLS = 3
CELL_W = 5.5
CELL_H = 3.2


def build(path):
    with dark_drawing(file=str(path)) as d:
        for i, (factory, name) in enumerate(SYMBOLS):
            col = i % COLS
            row = i // COLS
            cx = col * CELL_W
            cy = -row * CELL_H
            d.add(factory().at((cx - 0.9, cy)))
            d.add(elm.Label().at((cx, cy - 1.1)).label(name, color=LABEL, fontsize=12))
        # The transformer is wider than one cell, so it gets its own centred row.
        cy = -3 * CELL_H - 0.4
        d.add(elm.Transformer(t1=4, t2=4, core=True).at((CELL_W - 0.6, cy - 0.2)))
        d.add(elm.Label().at((CELL_W, cy - 1.0)).label("Transformer (iron core)", color=LABEL, fontsize=12))
