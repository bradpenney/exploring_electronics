"""Shared 3D figure style for Exploring Radio (copied from exploring_electronics'
illustrations/conductors_and_insulators.py so both sites look like one family).

Lit spheres via radial gradients, glassy panels, gloss overlays, glow, and a
perspective projector. Every page generator imports from here.
"""

import math
from xml.sax.saxutils import escape

TEXT = "#e6e6e6"
MUTED = "#a0aec0"
AMBER = "#f59e0b"
AMBER_LIGHT = "#fbbf24"
SLATE = "#2d3748"
SLATE_DARK = "#1a202c"
GREEN = "#48bb78"
RED = "#fc8181"
FONT = "IBM Plex Sans, Helvetica, Arial, sans-serif"

def svg(width, height, body, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" role="img" font-family="{FONT}">\n'
        f"<title>{title}</title>\n{body}\n</svg>\n"
    )


def text(x, y, s, size=15, fill=TEXT, anchor="middle", weight="normal", italic=False):
    style = ' font-style="italic"' if italic else ""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
        f'text-anchor="{anchor}" font-weight="{weight}"{style}>{escape(s)}</text>'
    )


def _ball(gid, light, mid, dark):
    return (f'<radialGradient id="{gid}" cx="35%" cy="32%" r="70%">'
            f'<stop offset="0" stop-color="{light}"/><stop offset="0.45" stop-color="{mid}"/>'
            f'<stop offset="1" stop-color="{dark}"/></radialGradient>')


def common_defs(extra=""):
    """Gradients and filters shared by every 3D-styled figure."""
    return (
        "<defs>"
        + _ball("eball", "#ffffff", "#cbd5e0", "#4a5568")
        + _ball("vball", "#fff7e0", "#f59e0b", "#92400e")
        + _ball("core", "#e2e8f0", "#718096", "#1a202c")
        + _ball("silverball", "#ffffff", "#c0c6cf", "#5a6270")
        + _ball("copperball", "#ffd2b0", "#c8733c", "#5e2b10")
        + _ball("goldball", "#fff3b0", "#e6b422", "#7a5a00")
        + _ball("alball", "#f0f6ff", "#a8b8cc", "#4a5868")
        + '<radialGradient id="glow" r="50%"><stop offset="0" stop-color="#f59e0b" stop-opacity="0.55"/>'
          '<stop offset="1" stop-color="#f59e0b" stop-opacity="0"/></radialGradient>'
        + '<linearGradient id="panel" x1="0" y1="0" x2="0" y2="1">'
          '<stop offset="0" stop-color="#2d3748" stop-opacity="0.45"/>'
          '<stop offset="1" stop-color="#1a202c" stop-opacity="0.15"/></linearGradient>'
        + '<linearGradient id="gloss" x1="0" y1="0" x2="0" y2="1">'
          '<stop offset="0" stop-color="#ffffff" stop-opacity="0.45"/>'
          '<stop offset="0.45" stop-color="#ffffff" stop-opacity="0.05"/>'
          '<stop offset="0.55" stop-color="#000000" stop-opacity="0"/>'
          '<stop offset="1" stop-color="#000000" stop-opacity="0.35"/></linearGradient>'
        + '<filter id="softglow" x="-50%" y="-50%" width="200%" height="200%">'
          '<feGaussianBlur stdDeviation="4" result="b"/>'
          '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        + f'<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
          f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{AMBER}"/></marker>'
        + extra
        + "</defs>"
    )


def panel(x, y, w, h):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="url(#panel)" '
            f'stroke="#4a5568" stroke-opacity="0.6"/>')


def _project(x, y, z, cx, cy, yaw=-0.55, pitch=0.42, focal=900.0):
    """Rotate a 3D point (yaw about y, pitch about x) and perspective-project it."""
    x, z = x * math.cos(yaw) + z * math.sin(yaw), -x * math.sin(yaw) + z * math.cos(yaw)
    y, z = y * math.cos(pitch) - z * math.sin(pitch), y * math.sin(pitch) + z * math.cos(pitch)
    s = focal / (focal + z)
    return cx + x * s, cy + y * s, z, s


# --- Building blocks (added 2026-09-30 for the electronics figure set) -----------
def shade(hex_color, f):
    """Lighten (f > 0) or darken (f < 0) a #rrggbb colour by fraction f."""
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    if f >= 0:
        r, g, b = (int(c + (255 - c) * f) for c in (r, g, b))
    else:
        r, g, b = (int(c * (1 + f)) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def cyl_gradient(gid, color, vertical=False):
    """Gradient that makes a rect read as a lit cylinder (light from above)."""
    x2, y2 = ("1", "0") if vertical else ("0", "1")
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}">'
            f'<stop offset="0" stop-color="{shade(color, -0.35)}"/>'
            f'<stop offset="0.22" stop-color="{shade(color, 0.45)}"/>'
            f'<stop offset="0.5" stop-color="{color}"/>'
            f'<stop offset="1" stop-color="{shade(color, -0.6)}"/></linearGradient>')


def box3d(x, y, w, d, h, color, shadow=True):
    """Isometric box; (x, y) is the front-bottom-left corner. Returns SVG parts."""
    dx, dy = d * 0.7, -d * 0.45
    out = []
    if shadow:
        out.append(f'<ellipse cx="{x + w / 2 + dx / 2:.1f}" cy="{y + 5:.1f}" rx="{w / 2 + dx / 2 + 6:.1f}" '
                   f'ry="{max(5, d * 0.18):.1f}" fill="#000" fill-opacity="0.4"/>')
    out += [
        f'<polygon points="{x:.1f},{y - h:.1f} {x + w:.1f},{y - h:.1f} {x + w + dx:.1f},{y - h + dy:.1f} '
        f'{x + dx:.1f},{y - h + dy:.1f}" fill="{shade(color, 0.3)}"/>',
        f'<rect x="{x:.1f}" y="{y - h:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{color}"/>',
        f'<rect x="{x:.1f}" y="{y - h:.1f}" width="{w:.1f}" height="{h:.1f}" fill="url(#gloss)" opacity="0.6"/>',
        f'<polygon points="{x + w:.1f},{y:.1f} {x + w:.1f},{y - h:.1f} {x + w + dx:.1f},{y - h + dy:.1f} '
        f'{x + w + dx:.1f},{y + dy:.1f}" fill="{shade(color, -0.45)}"/>',
    ]
    return out


def led(x, y, color="#fc8181", lit=True, r=13, glow=1.0):
    """A 5 mm LED seen from the front: dome, rim, two legs. (x, y) = dome centre."""
    gid = f"led{abs(hash((x, y, color, lit))) % 10**8}"
    body = color if lit else shade(color, -0.65)
    out = [f'<radialGradient id="{gid}" cx="38%" cy="30%" r="75%"><stop offset="0" stop-color="#ffffff" '
           f'stop-opacity="{0.95 if lit else 0.4}"/><stop offset="0.35" stop-color="{body}"/>'
           f'<stop offset="1" stop-color="{shade(body, -0.55)}"/></radialGradient>']
    if lit:
        out.append(f'<circle cx="{x}" cy="{y}" r="{r * 3.2 * glow:.1f}" fill="{color}" fill-opacity="0.18"/>')
        out.append(f'<circle cx="{x}" cy="{y}" r="{r * 2 * glow:.1f}" fill="{color}" fill-opacity="0.22"/>')
    out += [f'<line x1="{x - r * 0.35:.1f}" y1="{y + r}" x2="{x - r * 0.35:.1f}" y2="{y + r * 2.6:.1f}" stroke="#a0aec0" stroke-width="2.4"/>',
            f'<line x1="{x + r * 0.35:.1f}" y1="{y + r}" x2="{x + r * 0.35:.1f}" y2="{y + r * 2.3:.1f}" stroke="#a0aec0" stroke-width="2.4"/>',
            f'<rect x="{x - r * 1.15:.1f}" y="{y + r * 0.55:.1f}" width="{r * 2.3:.1f}" height="{r * 0.5:.1f}" rx="2" fill="url(#{gid})"/>',
            f'<path d="M{x - r:.1f},{y + r * 0.6:.1f} L{x - r:.1f},{y:.1f} A{r},{r} 0 0 1 {x + r:.1f},{y:.1f} '
            f'L{x + r:.1f},{y + r * 0.6:.1f} Z" fill="url(#{gid})"/>']
    return out


def pill(x, y, label, fill, fg="#ffffff", wpx=None, size=14, h=40):
    """Glossy rounded label centred at (x, y)."""
    wpx = wpx or int(size * 0.62 * len(label)) + 32
    return [f'<rect x="{x - wpx / 2:.1f}" y="{y - h / 2:.1f}" width="{wpx}" height="{h}" rx="{h / 2}" fill="{fill}"/>',
            f'<rect x="{x - wpx / 2:.1f}" y="{y - h / 2:.1f}" width="{wpx}" height="{h}" rx="{h / 2}" fill="url(#gloss)"/>',
            text(x, y + size * 0.36, label, size, fg, weight="bold")]


def render_all(figures, out_dir):
    """Write every figure in {name: fn} to out_dir."""
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, fn in figures.items():
        (out_dir / name).write_text(fn())
        print("wrote", out_dir / name)
