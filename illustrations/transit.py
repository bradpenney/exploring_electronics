"""Clickable transit-map figures for the topic landing pages.

Each stop is an <a> link, so these SVGs are inlined into the page with
pymdownx.snippets (`--8<-- "docs/images/landing/<page>.svg"` inside a raw
<figure>) rather than placed as an <img>, where links are dead. Because the
SVG shares the page's id namespace, every id carries the figure's prefix, and
the output has no blank lines so Markdown keeps it a single raw HTML block.

A map is a list of stages, each (name, colour, [(label lines, href), ...]),
laid out in rows: either one snaking line (connected=True, for a reading
order) or one separate line per row (connected=False, for a reference shelf).
"""

from xml.sax.saxutils import escape, quoteattr

from style3d import FONT, MUTED, TEXT, shade, text

LEFT, RIGHT, STEP = 112, 888, 160
TOP, ROW_H = 120, 150
BALL_R = 15


def _style():
    return ("<style>"
            ".tm-stop .tm-ring{stroke:#1a202c;stroke-width:3;transition:stroke .15s}"
            ".tm-stop:hover .tm-ring,.tm-stop:focus-visible .tm-ring{stroke:#ffffff;stroke-width:4}"
            ".tm-stop:hover .tm-lbl,.tm-stop:focus-visible .tm-lbl{fill:#ffffff;text-decoration:underline}"
            ".tm-stop:focus{outline:none}"
            "</style>")


def _ink(color):
    """Dark numerals on light balls, white on dark ones."""
    r, g, b = (int(color[i:i + 2], 16) for i in (1, 3, 5))
    return "#1a1a1a" if 0.299 * r + 0.587 * g + 0.114 * b > 150 else "#ffffff"


def _tube(d, color):
    common = 'fill="none" stroke-linecap="round" stroke-linejoin="round"'
    return [f'<path d="{d}" {common} stroke="#000000" stroke-opacity="0.45" stroke-width="12" transform="translate(2,4)"/>',
            f'<path d="{d}" {common} stroke="{color}" stroke-width="10"/>',
            f'<path d="{d}" {common} stroke="{shade(color, 0.5)}" stroke-opacity="0.55" stroke-width="3" transform="translate(-1,-2)"/>']


def _layout(stages, rows, connected):
    """Place every stop: returns [(num, lines, href, stage_index, x, y, row)]."""
    flat = [(lines, href, si) for si, (_, _, stops) in enumerate(stages) for lines, href in stops]
    assert sum(rows) == len(flat), (sum(rows), len(flat))
    placed, k = [], 0
    for r, n in enumerate(rows):
        y = TOP + r * ROW_H
        last = r == len(rows) - 1
        full = connected and not last and n > 1
        step = (RIGHT - LEFT) / (n - 1) if full else min(STEP, (RIGHT - LEFT) / max(n - 1, 1))
        rtl = connected and r % 2 == 1
        # A separate line per row is centred; a snaking line starts at its edge.
        start = LEFT if connected else (LEFT + RIGHT) / 2 - (n - 1) * step / 2
        for i in range(n):
            x = RIGHT - i * step if rtl else start + i * step
            lines, href, si = flat[k]
            placed.append((k + 1, lines, href, si, x, y, r))
            k += 1
    return placed


def _tracks(stages, placed, rows, connected):
    out = []
    for a, b in zip(placed, placed[1:]):
        color = stages[a[3]][1]
        if a[6] == b[6]:
            out += _tube(f"M{a[4]:.1f},{a[5]} L{b[4]:.1f},{b[5]}", color)
        elif connected:
            # U-turn at the row's end: carry on to the edge, arc down, come back.
            edge = RIGHT if a[6] % 2 == 0 else LEFT
            sweep = 1 if edge == RIGHT else 0
            r = ROW_H / 2
            out += _tube(f"M{a[4]:.1f},{a[5]} L{edge},{a[5]} A{r},{r} 0 0 {sweep} {edge},{b[5]} "
                         f"L{b[4]:.1f},{b[5]}", color)
    return out


def _stop(prefix, num, lines, href, color, x, y, numbered):
    name = " ".join(lines)
    aria = f"{num}. {name}" if numbered else name
    out = [f'<a class="tm-stop" href={quoteattr(href)} aria-label={quoteattr(aria)}>',
           f"<title>{escape(aria)}</title>",
           f'<circle cx="{x + 2:.1f}" cy="{y + 4}" r="{BALL_R}" fill="#000000" fill-opacity="0.4"/>',
           f'<circle class="tm-ring" cx="{x:.1f}" cy="{y}" r="{BALL_R}" fill="url(#{prefix}-ball-{color[1:]})"/>']
    if numbered:
        out.append(f'<text x="{x:.1f}" y="{y + 5}" font-size="13" fill="{_ink(color)}" text-anchor="middle" '
                   f'font-weight="bold">{num}</text>')
    for i, s in enumerate(lines):
        out.append(f'<text class="tm-lbl" x="{x:.1f}" y="{y + 38 + 18 * i}" font-size="15" fill="{TEXT}" '
                   f'text-anchor="middle" font-weight="bold">{escape(s)}</text>')
    out.append("</a>")
    return out


def _headers(stages, placed):
    """Each stage's name above its stops, once per row it occupies."""
    out, groups = [], {}
    for _, _, _, si, x, y, r in placed:
        groups.setdefault((si, r), []).append((x, y))
    for (si, _), pts in groups.items():
        xs = [p[0] for p in pts]
        cx, y = (min(xs) + max(xs)) / 2, pts[0][1]
        out.append(text(cx, y - 32, stages[si][0], 13, shade(stages[si][1], 0.25), weight="bold"))
    return out


def transit_map(prefix, title, desc, stages, rows, connected=True, numbered=True, hint="Click any stop to open its article"):
    placed = _layout(stages, rows, connected)
    w = 1000
    h = TOP + (len(rows) - 1) * ROW_H + 90
    colors = sorted({c for _, c, _ in stages})
    defs = ["<defs>",
            f'<linearGradient id="{prefix}-panel" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#2d3748" stop-opacity="0.45"/>'
            '<stop offset="1" stop-color="#1a202c" stop-opacity="0.15"/></linearGradient>']
    for c in colors:
        defs.append(f'<radialGradient id="{prefix}-ball-{c[1:]}" cx="35%" cy="32%" r="70%">'
                    f'<stop offset="0" stop-color="{shade(c, 0.6)}"/><stop offset="0.45" stop-color="{c}"/>'
                    f'<stop offset="1" stop-color="{shade(c, -0.55)}"/></radialGradient>')
    defs.append("</defs>")
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
             f'style="max-width:100%;height:auto" role="group" aria-labelledby="{prefix}-title {prefix}-desc" '
             f'font-family="{FONT}">',
             f'<title id="{prefix}-title">{escape(title)}</title>',
             f'<desc id="{prefix}-desc">{escape(desc)}</desc>',
             _style()] + defs
    parts.append(f'<rect x="15" y="15" width="{w - 30}" height="{h - 30}" rx="14" fill="url(#{prefix}-panel)" '
                 f'stroke="#4a5568" stroke-opacity="0.6"/>')
    parts.append(text(w / 2, 46, hint, 13, MUTED, italic=True))
    parts += _tracks(stages, placed, rows, connected)
    parts += _headers(stages, placed)
    for num, lines, href, si, x, y, _ in placed:
        parts += _stop(prefix, num, lines, href, stages[si][1], x, y, numbered)
    parts.append("</svg>")
    return "\n".join(parts) + "\n"
