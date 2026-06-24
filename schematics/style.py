"""Shared dark-theme styling for every Exploring Electronics schematic.

The site uses the Material "slate" (dark) theme. schemdraw's defaults render
black-on-white, which looks broken against a dark page. Build EVERY schematic
through ``dark_drawing()`` so the whole site stays visually consistent and no
diagram ever ships with the wrong colours.

This is the single file a future tool migration would need to re-implement —
keep all colour/weight decisions here, never inline them in individual circuit
scripts.
"""

import schemdraw

# Palette — tuned to read cleanly on the slate background.
STROKE = "#e6e6e6"   # lines and component bodies (light grey)
LABEL = "#e6e6e6"    # label text
ACCENT = "#ffb300"   # amber, matches the theme accent — use sparingly for emphasis
LINE_WIDTH = 2.2
FONT_SIZE = 14


def dark_drawing(**kwargs):
    """Return a ``schemdraw.Drawing`` pre-styled for the dark site theme.

    The native SVG backend writes a transparent background, so the schematic
    blends straight into the page. Pass any normal ``Drawing`` kwargs through.
    """
    kwargs.setdefault("show", False)  # never try to pop open a viewer at build time
    d = schemdraw.Drawing(**kwargs)
    d.config(color=STROKE, lw=LINE_WIDTH, fontsize=FONT_SIZE)
    return d
