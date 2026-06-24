"""Reference chart of the schematic symbols a beginner meets first. A labelled
grid — each cell shows one component's standard symbol with its name beneath.
Used in docs/essential/reading_schematics.md.
"""

import schemdraw.elements as elm

from style import dark_drawing, LABEL

# (element factory, label) in reading order, laid out in a 3-column grid.
SYMBOLS = [
    (lambda: elm.Resistor().right().length(1.8), "Resistor"),
    (lambda: elm.Capacitor().right().length(1.8), "Capacitor"),
    (lambda: elm.Capacitor2().right().length(1.8), "Capacitor (polarized)"),
    (lambda: elm.LED().right().length(1.8), "LED"),
    (lambda: elm.Diode().right().length(1.8), "Diode"),
    (lambda: elm.Battery().right().length(1.8), "Battery"),
    (lambda: elm.Switch().right().length(1.8), "Switch"),
    (lambda: elm.Button().right().length(1.8), "Pushbutton"),
    (lambda: elm.Potentiometer().right().length(1.8), "Potentiometer"),
    (lambda: elm.Inductor2().right().length(1.8), "Inductor"),
    (lambda: elm.BjtNpn(), "Transistor (NPN)"),
    (lambda: elm.Ground(), "Ground"),
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
            # Centre two-terminal symbols (length 1.8) on the cell.
            start_x = cx - 0.9
            d.add(factory().at((start_x, cy)))
            d.add(elm.Label().at((cx, cy - 1.1)).label(name, color=LABEL, fontsize=12))
