#!/usr/bin/env python3
"""Generate the SVG illustrations for docs/conductors_and_insulators.md.

Hand-built SVG (no dependencies) in the site's dark slate/amber palette, with
a transparent background so every figure blends into the Material slate theme.
Every plotted number comes from the same sources the article cites:

- resistivity at 20 C: Wikipedia "Electrical resistivity and conductivity"
  (silver 1.59e-8, copper 1.68e-8, gold 2.44e-8, aluminum 2.82e-8 ohm-m)
- free-electron densities: HyperPhysics, data from Ashcroft & Mermin
  (Cu 8.47, Ag 5.86, Au 5.90, Al 18.1 x 10^28 per m^3)
- insulator/semiconductor ranges and copper's temperature coefficient
  (0.00386 /C): HyperPhysics resistivity table
- the NTC curve is a typical B = 3950 K thermistor, labelled as such

Usage:
    python3 illustrations/conductors_and_insulators.py
"""

import math
from xml.sax.saxutils import escape
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "docs" / "images" / "conductors"

TEXT = "#e6e6e6"
MUTED = "#a0aec0"
AMBER = "#f59e0b"
AMBER_LIGHT = "#fbbf24"
SLATE = "#2d3748"
SLATE_DARK = "#1a202c"
GREEN = "#48bb78"
RED = "#fc8181"
FONT = "IBM Plex Sans, Helvetica, Arial, sans-serif"

# Measured values (see module docstring for sources).
RHO = {"Silver": 1.59e-8, "Copper": 1.68e-8, "Gold": 2.44e-8, "Aluminum": 2.82e-8}
N_FREE = {"Silver": 5.86e28, "Copper": 8.47e28, "Gold": 5.90e28, "Aluminum": 18.1e28}
ALPHA_CU = 0.00386


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


def arrow_defs(color=AMBER, name="arrow"):
    return (
        f'<defs><marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker></defs>'
    )


# 1. Copper atom (3D) ----------------------------------------------------------
def _fibonacci_sphere(n, rot):
    """n roughly even points on a unit sphere, rotated by (rx, ry) radians."""
    pts = []
    golden = math.pi * (3 - math.sqrt(5))
    for i in range(n):
        y = 1 - 2 * (i + 0.5) / n
        r = math.sqrt(1 - y * y)
        th = golden * i
        x, z = math.cos(th) * r, math.sin(th) * r
        rx, ry = rot
        y, z = y * math.cos(rx) - z * math.sin(rx), y * math.sin(rx) + z * math.cos(rx)
        x, z = x * math.cos(ry) + z * math.sin(ry), -x * math.sin(ry) + z * math.cos(ry)
        pts.append((x, y, z))
    return pts


def copper_atom():
    w, h = 720, 460
    cx, cy = 245, 230
    focal = 900.0  # perspective distance, in px
    radii = [52, 92, 138, 192]
    counts = [2, 8, 18, 1]
    rots = [(0.9, 0.4), (0.5, 1.1), (0.25, 0.7), (0, 0)]
    defs = [
        '<defs>',
        '<radialGradient id="shell" cx="38%" cy="32%" r="70%">'
        '<stop offset="0" stop-color="#e2e8f0" stop-opacity="0.16"/>'
        '<stop offset="0.75" stop-color="#2d3748" stop-opacity="0.05"/>'
        '<stop offset="1" stop-color="#a0aec0" stop-opacity="0.28"/></radialGradient>',
        '<radialGradient id="eball" cx="35%" cy="32%" r="70%">'
        '<stop offset="0" stop-color="#ffffff"/><stop offset="0.45" stop-color="#cbd5e0"/>'
        '<stop offset="1" stop-color="#4a5568"/></radialGradient>',
        '<radialGradient id="vball" cx="35%" cy="32%" r="70%">'
        '<stop offset="0" stop-color="#fff7e0"/><stop offset="0.45" stop-color="#f59e0b"/>'
        '<stop offset="1" stop-color="#92400e"/></radialGradient>',
        '<radialGradient id="proton" cx="35%" cy="32%" r="70%">'
        '<stop offset="0" stop-color="#fde68a"/><stop offset="0.5" stop-color="#d97706"/>'
        '<stop offset="1" stop-color="#78350f"/></radialGradient>',
        '<radialGradient id="neutron" cx="35%" cy="32%" r="70%">'
        '<stop offset="0" stop-color="#e2e8f0"/><stop offset="0.5" stop-color="#718096"/>'
        '<stop offset="1" stop-color="#1a202c"/></radialGradient>',
        '<radialGradient id="glow" r="50%"><stop offset="0" stop-color="#f59e0b" stop-opacity="0.55"/>'
        '<stop offset="1" stop-color="#f59e0b" stop-opacity="0"/></radialGradient>',
        f'<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{AMBER}"/></marker>',
        '</defs>',
    ]

    def project(x, y, z):
        s = focal / (focal - z)
        return cx + x * s, cy + y * s, s

    electrons = []  # (z, svg)
    valence_xy = None
    for r, n, rot in zip(radii, counts, rots):
        if n == 1:
            d = (-0.55, -0.62, 0.56)
            norm = math.sqrt(sum(c * c for c in d))
            pts = [tuple(c / norm for c in d)]
        else:
            pts = _fibonacci_sphere(n, rot)
        for ux, uy, uz in pts:
            x, y, s = project(ux * r, uy * r, uz * r)
            z = uz * r
            if n == 1:
                rad = 11 * s
                body = (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad * 2.4:.1f}" fill="url(#glow)"/>'
                        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad:.1f}" fill="url(#vball)"/>')
                valence_xy = (x, y, rad)
            else:
                rad = 6.2 * s
                op = 1.0 if z >= 0 else 0.45
                body = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad:.1f}" fill="url(#eball)" opacity="{op}"/>'
            electrons.append((z, body))

    parts = defs[:]
    back = sorted((e for e in electrons if e[0] < 0), key=lambda e: e[0])
    front = sorted((e for e in electrons if e[0] >= 0), key=lambda e: e[0])
    parts += [b for _, b in back]
    for r in reversed(radii):  # translucent shells, outer first
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#shell)" stroke="{MUTED}" '
                     f'stroke-opacity="0.45" stroke-width="1"/>')
        parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r * 0.3:.1f}" fill="none" '
                     f'stroke="{MUTED}" stroke-opacity="0.3" stroke-dasharray="3 5" '
                     f'transform="rotate(-18 {cx} {cy})"/>')
    # nucleus: 29 protons + 35 neutrons (copper-63), packed as a shaded cluster
    rnd = random.Random(29)
    nucleons = ["proton"] * 29 + ["neutron"] * 35
    rnd.shuffle(nucleons)
    nuc = []
    for i, kind in enumerate(nucleons):
        ux, uy, uz = _fibonacci_sphere(len(nucleons), (0.3, 0.2))[i]
        k = rnd.uniform(0.25, 1.0) ** (1 / 3) * 17
        nuc.append((uz * k, cx + ux * k, cy + uy * k, kind))
    for z, x, y, kind in sorted(nuc):
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.2" fill="url(#{kind})"/>')
    parts += [b for _, b in front]

    vx, vy, vr = valence_xy
    parts.append(f'<line x1="{vx + vr + 4:.1f}" y1="{vy - 2:.1f}" x2="478" y2="66" stroke="{AMBER}" '
                 f'stroke-width="1.5" marker-start="url(#arrow)"/>')
    parts.append(text(484, 62, "1 valence electron", 17, AMBER_LIGHT, "start", "bold"))
    parts.append(text(484, 84, "far from the nucleus,", 14, TEXT, "start"))
    parts.append(text(484, 103, "screened by 28 others,", 14, TEXT, "start"))
    parts.append(text(484, 122, "loosely held", 14, TEXT, "start"))
    parts.append(text(484, 168, "Nucleus: 29 protons", 14, MUTED, "start"))
    parts.append(text(484, 187, "and 35 neutrons", 14, MUTED, "start"))
    parts.append(text(484, 260, "The same ending, three metals:", 15, TEXT, "start", "bold"))
    rows = [("Copper (29)", "2 · 8 · 18 · ", "1"),
            ("Silver (47)", "2 · 8 · 18 · 18 · ", "1"),
            ("Gold (79)", "2 · 8 · 18 · 32 · 18 · ", "1")]
    for i, (name, shells, last) in enumerate(rows):
        y = 292 + i * 30
        parts.append(text(484, y, name, 14, MUTED, "start"))
        parts.append(
            f'<text x="574" y="{y}" font-size="14" fill="{TEXT}">{shells}'
            f'<tspan fill="{AMBER_LIGHT}" font-weight="bold">{last}</tspan></text>'
        )
    parts.append(text(cx, h - 10, "Shells, nucleus outward: 2, 8, 18, 1 electrons (not to scale)", 13, MUTED))
    return svg(w, h, "\n".join(parts), "A copper atom in 3D: 29 electrons on nested shells of 2, 8, 18 and 1 around a nucleus")


# Shared 3D styling -------------------------------------------------------------
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


# 2. Electron sea vs locked bonds (3D lattices) ----------------------------------------
def electron_sea():
    w, h = 780, 440
    rnd = random.Random(7)
    nx, ny, nz, step = 4, 3, 2, 70
    grid = [((i - (nx - 1) / 2) * step, (j - (ny - 1) / 2) * step, (k - (nz - 1) / 2) * step)
            for i in range(nx) for j in range(ny) for k in range(nz)]
    parts = [common_defs(), panel(10, 10, 375, 420), panel(395, 10, 375, 420)]

    # left: metal cores in a sea of free electrons
    lcx, lcy = 197, 205
    items = []
    for gx, gy, gz in grid:
        x, y, z, s = _project(gx, gy, gz, lcx, lcy)
        r = 13 * s
        items.append((z, f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="url(#core)"/>'
                         f'<text x="{x:.1f}" y="{y + 4.5 * s:.1f}" font-size="{13 * s:.1f}" fill="#f7fafc" '
                         f'text-anchor="middle" font-weight="bold">+</text>'))
    placed = []
    while len(placed) < len(grid):  # one free electron per atom core
        p = (rnd.uniform(-1.6, 1.6) * step, rnd.uniform(-1.1, 1.1) * step, rnd.uniform(-1.1, 1.1) * step)
        if min(math.dist(p, g) for g in grid) < 24 or any(math.dist(p, q) < 18 for q in placed):
            continue
        placed.append(p)
        x, y, z, s = _project(*p, lcx, lcy)
        r = 5.2 * s
        items.append((z, f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * 2.6:.1f}" fill="url(#glow)"/>'
                         f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="url(#vball)"/>'))
    parts += [b for _, b in sorted(items, key=lambda t: -t[0])]
    parts.append(text(197, 40, "Conductor (copper)", 18, AMBER_LIGHT, weight="bold"))
    parts.append(text(197, 60, "fixed atom cores in a sea of free electrons", 13, MUTED))
    # glow drawn as a soft rect: a blur filter on a horizontal line has a zero-height box
    parts.append(f'<rect x="80" y="364" width="228" height="16" rx="8" fill="{AMBER}" fill-opacity="0.18"/>')
    parts.append(f'<line x1="80" y1="372" x2="314" y2="372" stroke="{AMBER}" stroke-width="3" '
                 f'marker-end="url(#arrow)"/>')
    parts.append(text(197, 400, "apply a voltage: the whole sea drifts", 14, TEXT))

    # right: insulator lattice with an electron pair on every bond
    rcx, rcy = 583, 205
    items = []
    idx = {}
    for n, (gx, gy, gz) in enumerate(grid):
        idx[(round(gx), round(gy), round(gz))] = n
    for gx, gy, gz in grid:
        for dx, dy, dz in ((step, 0, 0), (0, step, 0), (0, 0, step)):
            nb = (round(gx + dx), round(gy + dy), round(gz + dz))
            if nb not in idx:
                continue
            x1, y1, z1, s1 = _project(gx, gy, gz, rcx, rcy)
            x2, y2, z2, s2 = _project(gx + dx, gy + dy, gz + dz, rcx, rcy)
            zm = (z1 + z2) / 2 + 0.1
            bond = (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#1a202c" '
                    f'stroke-width="{5 * (s1 + s2) / 2:.1f}" stroke-linecap="round"/>'
                    f'<line x1="{x1:.1f}" y1="{y1 - 1:.1f}" x2="{x2:.1f}" y2="{y2 - 1:.1f}" stroke="#718096" '
                    f'stroke-width="{2 * (s1 + s2) / 2:.1f}" stroke-linecap="round"/>')
            items.append((zm, bond))
            for f in (0.42, 0.58):
                px, py, pz, ps = _project(gx + dx * f, gy + dy * f, gz + dz * f, rcx, rcy)
                items.append((pz - 0.2, f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{3.6 * ps:.1f}" fill="url(#vball)"/>'))
        x, y, z, s = _project(gx, gy, gz, rcx, rcy)
        items.append((z, f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{12 * s:.1f}" fill="url(#core)"/>'))
    parts += [b for _, b in sorted(items, key=lambda t: -t[0])]
    parts.append(text(583, 40, "Insulator (glass)", 18, TEXT, weight="bold"))
    parts.append(text(583, 60, "every outer electron locked in a bond", 13, MUTED))
    parts.append(text(583, 384, "apply a voltage: nothing free to move", 14, TEXT))
    parts.append(text(583, 404, "(an electron pair sits on every bond)", 12, MUTED))
    return svg(w, h, "\n".join(parts), "Conductor versus insulator as 3D lattices: a sea of free electrons versus electrons locked in bonds")


# 3. The two factors -----------------------------------------------------------------
def two_factors():
    w, h = 720, 520
    L, R, T, B = 95, 650, 60, 430
    xmax, ymax = 2.4, 1.8
    X = lambda v: L + (R - L) * v / xmax
    Y = lambda v: B - (B - T) * v / ymax
    clip = f'<clipPath id="plot"><rect x="{L}" y="{T}" width="{R - L}" height="{B - T}"/></clipPath>'
    parts = [common_defs(clip), panel(L - 10, T - 10, R - L + 20, B - T + 20)]
    for v in (0.5, 1.0, 1.5, 2.0):
        parts.append(f'<line x1="{X(v):.1f}" y1="{T}" x2="{X(v):.1f}" y2="{B}" stroke="#4a5568" stroke-opacity="0.35"/>')
    for v in (0.5, 1.0, 1.5):
        parts.append(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{R}" y2="{Y(v):.1f}" stroke="#4a5568" stroke-opacity="0.35"/>')

    def curve(k):
        pts, x = [], k / ymax
        while x <= xmax + 0.001:
            pts.append((X(x), Y(k / x)))
            x += 0.01
        return pts

    cu = curve(1.0)
    above = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in cu) + f" L{X(xmax):.1f},{Y(ymax):.1f} L{cu[0][0]:.1f},{Y(ymax):.1f} Z"
    parts.append(f'<path d="{above}" fill="{AMBER}" fill-opacity="0.09" clip-path="url(#plot)"/>')
    parts.append(text(X(1.75), Y(1.45), "conducts better than copper", 13, AMBER_LIGHT, italic=True))
    for k, lab, lx, dy, anc in ((1.0, "same conductivity as copper", 1.45, -12, "start"),
                                (0.6, "60% of copper", 1.05, 22, "end")):
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in curve(k))
        color = AMBER if k == 1.0 else MUTED
        parts.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="1.8" '
                     f'stroke-dasharray="7 5" clip-path="url(#plot)"/>')
        parts.append(text(X(lx), Y(k / lx) + dy, lab, 12, color, anc, italic=True))
    parts.append(f'<line x1="{L}" y1="{B}" x2="{R}" y2="{B}" stroke="{MUTED}" stroke-width="1.5"/>')
    parts.append(f'<line x1="{L}" y1="{B}" x2="{L}" y2="{T}" stroke="{MUTED}" stroke-width="1.5"/>')
    for v in (0, 0.5, 1.0, 1.5, 2.0):
        parts.append(text(X(v), B + 22, f"{v:g}×", 13, MUTED))
    for v in (0, 0.5, 1.0, 1.5):
        parts.append(text(L - 10, Y(v) + 4, f"{v:g}×", 13, MUTED, "end"))
    parts.append(text((L + R) / 2, B + 54, "Question one: free electrons per cubic metre (relative to copper)", 14))
    parts.append(
        f'<text x="30" y="{(T + B) / 2}" font-size="14" fill="{TEXT}" text-anchor="middle" '
        f'transform="rotate(-90 30 {(T + B) / 2})">Question two: time between collisions (relative to copper)</text>')
    m, e = 9.1093837e-31, 1.602176634e-19
    tau = {k: m / (RHO[k] * N_FREE[k] * e * e) for k in RHO}
    style = {"Silver": ("silverball", (16, -12, "start")), "Copper": ("copperball", (16, -10, "start")),
             "Gold": ("goldball", (-16, 22, "end")), "Aluminum": ("alball", (0, 34, "middle"))}
    for k in RHO:
        xv, yv = N_FREE[k] / N_FREE["Copper"], tau[k] / tau["Copper"]
        cond = RHO["Copper"] / RHO[k]
        r = 8 + 6 * cond
        x, y = X(xv), Y(yv)
        grad, (dx, dy, anc) = style[k]
        parts.append(f'<ellipse cx="{x:.1f}" cy="{y + r + 3:.1f}" rx="{r:.1f}" ry="{r * 0.28:.1f}" fill="#000" fill-opacity="0.35"/>')
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="url(#{grad})"/>')
        parts.append(text(x + dx, y + dy, f"{k} ({cond * 100:.0f}%)", 14,
                          AMBER_LIGHT if k == "Copper" else TEXT, anc, "bold"))
    parts.append(text((L + R) / 2, 30, "Conductivity = how many electrons are free × how far each one gets", 15, TEXT, weight="bold"))
    parts.append(text(R - 8, B - 12, "sphere size shows conductivity", 12, MUTED, "end", italic=True))
    return svg(w, h, "\n".join(parts), "Free electrons against time between collisions for silver, copper, gold and aluminum, each drawn as a sphere in its own colour")


# 4. Resistivity scale ------------------------------------------------------------
def resistivity_scale():
    w, h = 780, 330
    L, R = 50, 730
    lo, hi = -9, 19
    X = lambda v: L + (R - L) * (math.log10(v) - lo) / (hi - lo)
    ty, th = 140, 30
    # Band edges are approximate: the families shade into each other, and graphite is a
    # (poor) conductor, so the conductor band runs to 1e-3.
    bands = [(1e-9, 1e-3, GREEN, "Conductors"), (1e-3, 1e5, AMBER, "Semiconductors"), (1e5, 1e19, RED, "Insulators")]
    stops = []
    for a, b, color, _ in bands:
        stops.append(f'<stop offset="{(X(a) - L) / (R - L):.3f}" stop-color="{color}"/>')
        stops.append(f'<stop offset="{(X(b) - L) / (R - L):.3f}" stop-color="{color}"/>')
    tube = f'<linearGradient id="bands" x1="0" y1="0" x2="1" y2="0">{"".join(stops)}</linearGradient>'
    parts = [common_defs(tube), panel(15, 15, w - 30, h - 30)]
    parts.append(f'<rect x="{L}" y="{ty + th - 2}" width="{R - L}" height="10" rx="5" fill="#000" fill-opacity="0.35"/>')
    parts.append(f'<rect x="{L}" y="{ty}" width="{R - L}" height="{th}" rx="{th / 2}" fill="url(#bands)" fill-opacity="0.55"/>')
    parts.append(f'<rect x="{L}" y="{ty}" width="{R - L}" height="{th}" rx="{th / 2}" fill="url(#gloss)" stroke="#e2e8f0" stroke-opacity="0.35"/>')
    for a, b, color, lab in bands:
        parts.append(text((X(a) + X(b)) / 2, ty + th + 34, lab, 14, color, weight="bold"))
    for p in range(lo + 1, hi, 3):
        x = X(10 ** p)
        parts.append(f'<line x1="{x:.1f}" y1="{ty + th + 2}" x2="{x:.1f}" y2="{ty + th + 8}" stroke="{MUTED}"/>')
        parts.append(f'<text x="{x:.1f}" y="{ty + th + 58}" font-size="12" fill="{MUTED}" text-anchor="middle">10<tspan dy="-5" font-size="9">{p}</tspan></text>')
    items = [
        (1.59e-8, 2.82e-8, "silver · copper · gold · aluminum", True, "copperball"),
        (3e-5, 6e-4, "graphite", False, "core"),
        (0.1, 60, "silicon", False, "eball"),
        (1e9, 1e13, "glass", True, "eball"),
        (1e13, 1e15, "hard rubber", False, "core"),
        (7.5e17, 7.5e17, "fused quartz", True, "eball"),
    ]
    cy = ty + th / 2
    for a, b, lab, above, grad in items:
        x1, x2 = X(a), X(b)
        mid = (x1 + x2) / 2
        if b == a or x2 - x1 < 12:
            parts.append(f'<circle cx="{mid:.1f}" cy="{cy}" r="9" fill="url(#{grad})"/>')
        else:
            parts.append(f'<rect x="{x1:.1f}" y="{cy - 7}" width="{x2 - x1:.1f}" height="14" rx="7" fill="url(#{grad})"/>'
                         f'<rect x="{x1:.1f}" y="{cy - 7}" width="{x2 - x1:.1f}" height="14" rx="7" fill="url(#gloss)"/>')
        y = ty - 26 if above else ty + th + 92
        parts.append(f'<line x1="{mid:.1f}" y1="{ty - 3 if above else ty + th + 3}" x2="{mid:.1f}" '
                     f'y2="{y + (6 if above else -14)}" stroke="{MUTED}" stroke-width="1"/>')
        anchor = "start" if mid < 130 else ("end" if mid > 670 else "middle")
        parts.append(text(mid if anchor == "middle" else mid + (-6 if anchor == "start" else 6), y, lab, 14, TEXT, anchor))
    parts.append(text(w / 2, 50, "Resistivity at room temperature, ohm-metres (log scale: each tick is 1,000×)", 15, TEXT, weight="bold"))
    parts.append(text(w / 2, h - 30, "Copper to quartz spans about 25 powers of ten", 13, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Log-scale resistivity chart drawn as a glossy tube, from silver and copper through silicon to glass and quartz")


# 5. Marbles in a tube ------------------------------------------------------------
def marbles():
    w, h = 780, 300
    glass = ('<linearGradient id="tube" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#e2e8f0" stop-opacity="0.35"/>'
             '<stop offset="0.25" stop-color="#e2e8f0" stop-opacity="0.06"/>'
             '<stop offset="0.8" stop-color="#1a202c" stop-opacity="0.2"/>'
             '<stop offset="1" stop-color="#e2e8f0" stop-opacity="0.25"/></linearGradient>'
             '<linearGradient id="pulse" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0" stop-color="#f59e0b" stop-opacity="0"/>'
             '<stop offset="0.85" stop-color="#f59e0b" stop-opacity="0.9"/>'
             '<stop offset="1" stop-color="#fde68a" stop-opacity="1"/></linearGradient>'
             '<linearGradient id="trail" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0" stop-color="#f59e0b" stop-opacity="0"/>'
             '<stop offset="1" stop-color="#f59e0b" stop-opacity="0.6"/></linearGradient>')
    parts = [common_defs(glass), panel(15, 15, w - 30, h - 30)]
    tx, ty, tw, th = 130, 110, 520, 48
    # pulse riding along the top of the tube
    parts.append(f'<rect x="{tx}" y="{ty - 30}" width="{tw}" height="8" rx="4" fill="url(#pulse)" filter="url(#softglow)"/>')
    parts.append(text(tx + tw / 2, ty - 40, "the push: a large fraction of the speed of light", 14, AMBER_LIGHT, weight="bold"))
    parts.append(f'<ellipse cx="{tx + tw / 2}" cy="{ty + th + 10}" rx="{tw / 2}" ry="7" fill="#000" fill-opacity="0.35"/>')
    r = 20
    n = int((tw - 8) // (2 * r))
    for i in range(n):
        cx = tx + 4 + r + i * 2 * r
        parts.append(f'<circle cx="{cx}" cy="{ty + th / 2}" r="{r - 2}" fill="url(#eball)"/>')
    parts.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="{th / 2}" fill="url(#tube)" stroke="#e2e8f0" stroke-opacity="0.55" stroke-width="1.5"/>')
    parts.append(f'<rect x="{tx + 14}" y="{ty + 5}" width="{tw - 28}" height="5" rx="2.5" fill="#ffffff" fill-opacity="0.35"/>')
    yin = ty + th / 2
    parts.append(f'<rect x="{tx - 105}" y="{yin - 8}" width="60" height="16" rx="8" fill="url(#trail)"/>')
    parts.append(f'<circle cx="{tx - 38}" cy="{yin}" r="{(r - 2) * 2.4}" fill="url(#glow)"/>')
    parts.append(f'<circle cx="{tx - 38}" cy="{yin}" r="{r - 2}" fill="url(#vball)"/>')
    parts.append(text(tx - 38, ty + th + 32, "one in", 15, AMBER_LIGHT, weight="bold"))
    ox = tx + tw + 38
    parts.append(f'<rect x="{ox + 4}" y="{yin - 8}" width="60" height="16" rx="8" fill="url(#trail)" transform="rotate(180 {ox + 34} {yin})"/>')
    parts.append(f'<circle cx="{ox}" cy="{yin}" r="{(r - 2) * 2.4}" fill="url(#glow)"/>')
    parts.append(f'<circle cx="{ox}" cy="{yin}" r="{r - 2}" fill="url(#vball)"/>')
    parts.append(text(ox, ty + th + 32, "one out, at once", 15, AMBER_LIGHT, weight="bold"))
    parts.append(text(w / 2, ty + th + 32, "a wire already full of electrons", 13, MUTED, italic=True))
    parts.append(text(w / 2, 236, "Each electron drifts about 0.07 mm per second (1 A in a 1 mm² copper wire):", 14, TEXT))
    parts.append(text(w / 2, 258, "almost four hours to travel one metre.", 14, TEXT))
    return svg(w, h, "\n".join(parts), "Marbles packed in a glass tube: pushing one in pushes one out the far end immediately")


# 6. Temperature: metal up, semiconductor down --------------------------------------
def temperature_curves():
    w, h = 720, 480
    L, R, T, B = 95, 560, 60, 400
    tmin, tmax, ymax = 0, 100, 3.0
    X = lambda t: L + (R - L) * (t - tmin) / (tmax - tmin)
    Y = lambda v: B - (B - T) * v / ymax
    fills = ('<linearGradient id="semifill" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#e2e8f0" stop-opacity="0.28"/>'
             '<stop offset="1" stop-color="#e2e8f0" stop-opacity="0"/></linearGradient>'
             '<linearGradient id="cufill" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#f59e0b" stop-opacity="0.3"/>'
             '<stop offset="1" stop-color="#f59e0b" stop-opacity="0"/></linearGradient>')
    parts = [common_defs(fills), panel(L - 10, T - 10, R - L + 20, B - T + 20)]
    for t in range(20, 101, 20):
        parts.append(f'<line x1="{X(t):.1f}" y1="{T}" x2="{X(t):.1f}" y2="{B}" stroke="#4a5568" stroke-opacity="0.35"/>')
    for v in (0.5, 1.0, 1.5, 2.0, 2.5):
        parts.append(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{R}" y2="{Y(v):.1f}" stroke="#4a5568" stroke-opacity="0.35"/>')
    parts.append(f'<line x1="{L}" y1="{B}" x2="{R}" y2="{B}" stroke="{MUTED}" stroke-width="1.5"/>')
    parts.append(f'<line x1="{L}" y1="{B}" x2="{L}" y2="{T}" stroke="{MUTED}" stroke-width="1.5"/>')
    for t in range(0, 101, 20):
        parts.append(text(X(t), B + 22, f"{t} °C", 13, MUTED))
    for v in (0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0):
        parts.append(text(L - 10, Y(v) + 4, f"{v:g}×", 13, MUTED, "end"))
    parts.append(text((L + R) / 2, B + 50, "Temperature", 14))
    parts.append(
        f'<text x="30" y="{(T + B) / 2}" font-size="14" fill="{TEXT}" text-anchor="middle" '
        f'transform="rotate(-90 30 {(T + B) / 2})">Resistance (relative to 20 °C)</text>')
    bval = 3950.0
    ntc = lambda t: math.exp(bval * (1 / (t + 273.15) - 1 / 293.15))
    sc_pts = [(X(t), Y(ntc(t))) for t in range(0, 101, 2) if ntc(t) <= ymax]
    cu_pts = [(X(t), Y(1 + ALPHA_CU * (t - 20))) for t in range(0, 101, 2)]
    for pts, fill in ((sc_pts, "semifill"), (cu_pts, "cufill")):
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f" L{pts[-1][0]:.1f},{B} L{pts[0][0]:.1f},{B} Z"
        parts.append(f'<path d="{d}" fill="url(#{fill})"/>')
    for pts, color in ((sc_pts, "#f7fafc"), (cu_pts, AMBER)):
        line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        parts.append(f'<polyline points="{line}" fill="none" stroke="{color}" stroke-width="3.5" '
                     f'stroke-linejoin="round" filter="url(#softglow)"/>')
    x20, y20 = X(20), Y(1)
    parts.append(f'<circle cx="{x20:.1f}" cy="{y20:.1f}" r="7" fill="url(#vball)"/>')
    parts.append(text(x20 + 14, y20 - 14, "both equal at 20 °C", 12, MUTED, "start", italic=True))
    cx_end, cy_end = cu_pts[-1]
    parts.append(f'<circle cx="{cx_end:.1f}" cy="{cy_end:.1f}" r="8" fill="url(#copperball)"/>')
    sx_end, sy_end = sc_pts[-1]
    parts.append(f'<circle cx="{sx_end:.1f}" cy="{sy_end:.1f}" r="8" fill="url(#eball)"/>')
    parts.append(text(R + 18, cy_end + 5, "Copper", 15, AMBER_LIGHT, "start", "bold"))
    parts.append(text(R + 18, cy_end + 24, "rises ~0.39%/°C", 13, AMBER_LIGHT, "start"))
    parts.append(text(X(14), Y(2.55), "Semiconductor", 15, TEXT, "start", "bold"))
    parts.append(text(X(14), Y(2.55) + 19, "(typical NTC thermistor) falls steeply", 13, TEXT, "start"))
    parts.append(text(w / 2, 30, "Heat pushes metals and semiconductors in opposite directions", 15, TEXT, weight="bold"))
    return svg(w, h, "\n".join(parts), "Resistance against temperature: copper rises gently, a semiconductor thermistor falls steeply")



# 7. Material families: how tightly the atom holds its valence electrons ---------------
def _mini_atom(cx, cy, n_val, mode):
    """A small 3D atom: core sphere, glassy valence shell, n_val valence electrons.

    mode: "loose" (one electron leaving with a trail), "bonded" (electrons paired
    toward neighbours), "heat" (all bonded but one shaken loose).
    """
    out = [f'<ellipse cx="{cx}" cy="{cy + 78}" rx="60" ry="10" fill="#000" fill-opacity="0.35"/>',
           f'<circle cx="{cx}" cy="{cy}" r="62" fill="url(#shellg)" stroke="#a0aec0" stroke-opacity="0.45"/>',
           f'<ellipse cx="{cx}" cy="{cy}" rx="62" ry="18" fill="none" stroke="#a0aec0" stroke-opacity="0.3" '
           f'stroke-dasharray="3 5" transform="rotate(-18 {cx} {cy})"/>',
           f'<circle cx="{cx}" cy="{cy}" r="22" fill="url(#core)"/>']
    for i in range(n_val):
        a = -math.pi / 2 + 2 * math.pi * i / n_val + 0.3
        x, y = cx + 62 * math.cos(a), cy + 62 * math.sin(a) * 0.9
        if mode == "loose" and i == 0:
            x2, y2 = cx + 112, cy - 52
            out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x2}" y2="{y2}" stroke="{AMBER}" '
                       f'stroke-opacity="0.45" stroke-width="5" stroke-linecap="round" stroke-dasharray="2 7"/>')
            out.append(f'<circle cx="{x2}" cy="{y2}" r="22" fill="url(#glow)"/>'
                       f'<circle cx="{x2}" cy="{y2}" r="9" fill="url(#vball)"/>')
            continue
        if mode == "heat" and i == 0:
            x2, y2 = cx + 104, cy - 58
            out.append(f'<circle cx="{(x + x2) / 2:.1f}" cy="{(y + y2) / 2:.1f}" r="16" fill="url(#heat)"/>')
            out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x2}" y2="{y2}" stroke="#fc8181" '
                       f'stroke-opacity="0.6" stroke-width="3" stroke-dasharray="2 6"/>')
            out.append(f'<circle cx="{x2}" cy="{y2}" r="8" fill="url(#vball)"/>')
            continue
        if mode in ("bonded", "heat"):
            # pair each electron with a partner from the neighbouring atom (stub bond)
            bx, by = cx + 92 * math.cos(a), cy + 92 * math.sin(a) * 0.9
            out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="#718096" '
                       f'stroke-width="3" stroke-linecap="round"/>')
            out.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="6" fill="url(#eball)" opacity="0.8"/>')
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7.5" fill="url(#vball)"/>')
    return out


def material_families():
    w, h = 780, 470
    extra = ('<radialGradient id="shellg" cx="38%" cy="32%" r="70%">'
             '<stop offset="0" stop-color="#e2e8f0" stop-opacity="0.18"/>'
             '<stop offset="0.75" stop-color="#2d3748" stop-opacity="0.05"/>'
             '<stop offset="1" stop-color="#a0aec0" stop-opacity="0.3"/></radialGradient>'
             '<radialGradient id="heat" r="50%"><stop offset="0" stop-color="#fc8181" stop-opacity="0.7"/>'
             '<stop offset="1" stop-color="#fc8181" stop-opacity="0"/></radialGradient>')
    parts = [common_defs(extra)]
    cols = [
        (135, 1, "loose", "1 to 3 valence electrons", "held loosely: they leave", "and join a shared sea",
         "Conductor", "copper, silver, gold, aluminum", GREEN),
        (390, 4, "heat", "4 valence electrons", "all bonded, but heat", "shakes a few loose",
         "Semiconductor", "silicon, germanium", AMBER_LIGHT),
        (645, 6, "bonded", "5 to 8 valence electrons", "held tightly: every one", "locked into a bond",
         "Insulator", "glass, porcelain, rubber, plastic", RED),
    ]
    for cx, n, mode, l1, l2, l3, fam, ex, color in cols:
        parts.append(panel(cx - 120, 15, 240, 440))
        parts.append(text(cx, 48, l1, 15, TEXT, weight="bold"))
        parts += _mini_atom(cx, 160, n, mode)
        parts.append(text(cx, 278, l2, 13, MUTED))
        parts.append(text(cx, 296, l3, 13, MUTED))
        # glossy pedestal with the family name
        parts.append(f'<rect x="{cx - 95}" y="330" width="190" height="64" rx="14" fill="{color}" fill-opacity="0.22" '
                     f'stroke="{color}" stroke-opacity="0.7"/>')
        parts.append(f'<rect x="{cx - 95}" y="330" width="190" height="64" rx="14" fill="url(#gloss)"/>')
        parts.append(text(cx, 360, fam, 18, color, weight="bold"))
        parts.append(text(cx, 382, ex, 12, TEXT))
        parts.append(text(cx, 430, "→ resistance falls when heated" if mode == "heat" else
                          ("→ resistance rises when heated" if mode == "loose" else "→ blocks current"), 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Three atoms: loosely held valence electrons make a conductor, four bonded electrons a semiconductor, tightly held electrons an insulator")


# 8. Heat feedback loop ------------------------------------------------------------
def heat_feedback():
    w, h = 760, 420
    cx, cy, rx, ry = 330, 215, 205, 120
    parts = [common_defs('<linearGradient id="ring" x1="0" y1="0" x2="1" y2="1">'
                         '<stop offset="0" stop-color="#f59e0b"/><stop offset="1" stop-color="#c53030"/></linearGradient>'),
             panel(15, 15, w - 30, h - 30)]
    parts.append(f'<ellipse cx="{cx}" cy="{cy + 10}" rx="{rx}" ry="{ry}" fill="none" stroke="#000" stroke-opacity="0.35" stroke-width="16"/>')
    parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="url(#ring)" stroke-width="12" stroke-opacity="0.85"/>')
    parts.append(f'<ellipse cx="{cx}" cy="{cy - 3}" rx="{rx}" ry="{ry}" fill="none" stroke="#fff" stroke-opacity="0.25" stroke-width="3"/>')
    # direction chevrons around the ring (clockwise)
    for deg in (45, 135, 225, 315):
        a = math.radians(deg)
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        tx, ty = -rx * math.sin(a), ry * math.cos(a)
        ang = math.degrees(math.atan2(ty, tx))
        parts.append(f'<path d="M-9,-9 L5,0 L-9,9" fill="none" stroke="#fff" stroke-width="3.5" '
                     f'stroke-linecap="round" stroke-linejoin="round" transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f})"/>')
    nodes = [(270, "Wire heats up"), (0, "Atoms vibrate harder"), (90, "More collisions"), (180, "Resistance rises")]
    for deg, lab in nodes:
        a = math.radians(deg)
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        wpx = 9 * len(lab) + 28
        parts.append(f'<rect x="{x - wpx / 2:.1f}" y="{y - 20:.1f}" width="{wpx}" height="40" rx="20" fill="#2d3748" stroke="#cbd5e0" stroke-opacity="0.6"/>')
        parts.append(f'<rect x="{x - wpx / 2:.1f}" y="{y - 20:.1f}" width="{wpx}" height="40" rx="20" fill="url(#gloss)"/>')
        parts.append(text(x, y + 5, lab, 14, TEXT, weight="bold"))
    # entry: too much current
    parts.append(f'<rect x="{cx - 90}" y="{cy - 22}" width="180" height="44" rx="22" fill="{AMBER}" fill-opacity="0.85"/>')
    parts.append(f'<rect x="{cx - 90}" y="{cy - 22}" width="180" height="44" rx="22" fill="url(#gloss)"/>')
    parts.append(text(cx, cy + 6, "Too much current", 15, "#1a1a1a", weight="bold"))
    parts.append(f'<line x1="{cx}" y1="{cy - 24}" x2="{cx}" y2="{cy - ry + 26}" stroke="{AMBER}" stroke-width="3" marker-end="url(#arrow)"/>')
    parts.append(text(cx + 10, cy - 50, "starts it", 12, MUTED, "start", italic=True))
    # exit: insulation fails
    ex, ey = 640, 120
    parts.append(f'<path d="M{cx + 80},{cy - ry - 4} Q{ex - 40},{ey - 70} {ex},{ey - 34}" fill="none" stroke="#fc8181" '
                 f'stroke-width="3" stroke-dasharray="6 5" marker-end="url(#arrowred)"/>')
    parts.append(f'<circle cx="{ex}" cy="{ey + 10}" r="58" fill="url(#heatglow)"/>')
    parts.append(f'<rect x="{ex - 78}" y="{ey - 28}" width="156" height="72" rx="16" fill="#c53030" fill-opacity="0.85"/>')
    parts.append(f'<rect x="{ex - 78}" y="{ey - 28}" width="156" height="72" rx="16" fill="url(#gloss)"/>')
    parts.append(text(ex, ey + 2, "Insulation melts", 14, "#fff", weight="bold"))
    parts.append(text(ex, ey + 22, "or ignites", 14, "#fff", weight="bold"))
    parts.append(text(ex, ey + 70, "if nothing stops it", 12, "#fc8181", italic=True))
    parts.append(text(cx, h - 32, "Each lap turns more of the current into heat", 14, MUTED, italic=True))
    s_ = svg(w, h, "\n".join(parts), "A glowing feedback loop: too much current heats the wire, atoms vibrate harder, collisions increase, resistance rises, which heats the wire further")
    return s_.replace("</defs>",
                      '<marker id="arrowred" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                      'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#fc8181"/></marker>'
                      '<radialGradient id="heatglow" r="50%"><stop offset="0" stop-color="#fc8181" stop-opacity="0.45"/>'
                      '<stop offset="1" stop-color="#fc8181" stop-opacity="0"/></radialGradient></defs>', 1)


# 9. Doping ----------------------------------------------------------------------
def _si_patch(cx, cy, special=None):
    """3x3 silicon lattice in perspective; the centre atom may be P (extra e-) or B (hole)."""
    out = []
    pts = {}
    for i in range(3):
        for j in range(3):
            x, y, z, s = _project((i - 1) * 52, 0, (j - 1) * 52, cx, cy, yaw=-0.5, pitch=0.9)
            pts[(i, j)] = (x, y, z, s)
    items = []
    for (i, j), (x, y, z, s) in pts.items():
        for di, dj in ((1, 0), (0, 1)):
            if (i + di, j + dj) in pts:
                x2, y2, z2, s2 = pts[(i + di, j + dj)]
                missing = special == "B" and (i, j) == (1, 1) and (di, dj) == (1, 0)
                items.append(((z + z2) / 2 + 0.1,
                              f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#718096" stroke-width="3"/>'))
                for f in (0.4, 0.6):
                    px, py = x + (x2 - x) * f, y + (y2 - y) * f
                    if missing and f == 0.4:
                        items.append(((z + z2) / 2 - 0.1,
                                      f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="none" stroke="#fc8181" '
                                      f'stroke-width="2" stroke-dasharray="2 2"/>'))
                    else:
                        items.append(((z + z2) / 2 - 0.1, f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.6" fill="url(#vball)"/>'))
    for (i, j), (x, y, z, s) in pts.items():
        grad = "core"
        if (i, j) == (1, 1) and special == "P":
            grad = "pball"
        if (i, j) == (1, 1) and special == "B":
            grad = "bball"
        items.append((z, f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{13 * s:.1f}" fill="url(#{grad})"/>'))
    out += [b for _, b in sorted(items, key=lambda t: -t[0])]
    if special == "P":
        x, y, _, _ = pts[(1, 1)]
        out.append(f'<circle cx="{x + 26:.1f}" cy="{y - 34:.1f}" r="20" fill="url(#glow)"/>'
                   f'<circle cx="{x + 26:.1f}" cy="{y - 34:.1f}" r="7" fill="url(#vball)"/>')
    return out, pts


def doping():
    w, h = 780, 500
    extra = (_ball("pball", "#c3dafe", "#4c6ef5", "#1e2a78") + _ball("bball", "#fed7d7", "#e05656", "#5c1a1a")
             + '<linearGradient id="nface" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a78f0"/>'
               '<stop offset="1" stop-color="#26357a"/></linearGradient>'
               '<linearGradient id="pface" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e86a6a"/>'
               '<stop offset="1" stop-color="#7a2626"/></linearGradient>')
    parts = [common_defs(extra)]
    specs = [(130, None, "Pure silicon", "4 valence electrons, all bonded", TEXT),
             (390, "P", "N-type: add phosphorus", "5 valence electrons: one spare", "#7f9cf5"),
             (650, "B", "P-type: add boron", "3 valence electrons: one gap", "#fc8181")]
    for cx, sp, t1, t2, color in specs:
        parts.append(panel(cx - 120, 15, 240, 250))
        parts.append(text(cx, 45, t1, 15, color, weight="bold"))
        parts.append(text(cx, 65, t2, 12, MUTED))
        patch, _ = _si_patch(cx, 160, sp)
        parts += patch
    parts.append(text(455, 92, "free electron", 12, AMBER_LIGHT, italic=True))
    parts.append(text(650, 248, "dashed ring: the missing electron (a hole)", 11, "#fc8181", italic=True))
    # arrows from N and P down to the junction block
    for sx in (390, 650):
        parts.append(f'<path d="M{sx},{272} Q{sx},{320} {520 + (sx - 520) * 0.35:.1f},{345}" fill="none" stroke="{AMBER}" '
                     f'stroke-width="3" marker-end="url(#arrow)"/>')
    # 3D junction block: N half and P half
    bx, by, bw, bh, bd = 400, 360, 120, 56, 34
    for i, (face, lab) in enumerate((("nface", "N"), ("pface", "P"))):
        x0 = bx + i * bw
        parts.append(f'<polygon points="{x0},{by} {x0 + bw},{by} {x0 + bw + bd},{by - bd * 0.6} {x0 + bd},{by - bd * 0.6}" '
                     f'fill="url(#{face})" opacity="0.75"/>')
        parts.append(f'<rect x="{x0}" y="{by}" width="{bw}" height="{bh}" fill="url(#{face})"/>')
        parts.append(f'<rect x="{x0}" y="{by}" width="{bw}" height="{bh}" fill="url(#gloss)"/>')
        parts.append(text(x0 + bw / 2, by + 36, lab, 22, "#fff", weight="bold"))
    parts.append(f'<polygon points="{bx + 2 * bw},{by} {bx + 2 * bw + bd},{by - bd * 0.6} {bx + 2 * bw + bd},{by + bh - bd * 0.6} {bx + 2 * bw},{by + bh}" '
                 f'fill="#3a1414"/>')
    parts.append(f'<line x1="{bx + bw}" y1="{by - 4}" x2="{bx + bw}" y2="{by + bh + 4}" stroke="{AMBER_LIGHT}" stroke-width="3"/>')
    parts.append(text(bx + bw, by + bh + 26, "the junction", 13, AMBER_LIGHT, weight="bold"))
    parts.append(text(bx + bw, by + bh + 52, "Join the two kinds: diodes, transistors, every chip", 15, TEXT, weight="bold"))
    return svg(w, h, "\n".join(parts), "Pure silicon, phosphorus-doped N-type with a spare electron, boron-doped P-type with a hole, and the two joined into a P-N junction")


# 10. Choosing a conductor: four ingots -----------------------------------------------
def _ingot(x, y, wid, dep, hgt, top, front, side):
    """Isometric metal bar: front-bottom-left corner at (x, y)."""
    dx, dy = dep * 0.7, -dep * 0.45
    return [
        f'<ellipse cx="{x + wid / 2 + dx / 2:.1f}" cy="{y + 6:.1f}" rx="{wid / 2 + dx / 2 + 8:.1f}" ry="9" fill="#000" fill-opacity="0.4"/>',
        f'<polygon points="{x},{y - hgt} {x + wid},{y - hgt} {x + wid + dx},{y - hgt + dy} {x + dx},{y - hgt + dy}" fill="{top}"/>',
        f'<rect x="{x}" y="{y - hgt}" width="{wid}" height="{hgt}" fill="{front}"/>',
        f'<rect x="{x}" y="{y - hgt}" width="{wid}" height="{hgt}" fill="url(#gloss)"/>',
        f'<polygon points="{x + wid},{y} {x + wid},{y - hgt} {x + wid + dx},{y - hgt + dy} {x + wid + dx},{y + dy}" fill="{side}"/>',
    ]


def choosing_conductor():
    w, h = 780, 400
    parts = [common_defs()]
    metals = [
        ("Copper", "conductivity per dollar", "wire, cable, circuit boards", "#e8a07a", "#b8673a", "#6e3417"),
        ("Gold", "a surface that never corrodes", "plating on contacts", "#ffe58a", "#d4a514", "#7a5c00"),
        ("Aluminum", "conductivity per kilogram", "overhead power lines", "#eef3f9", "#a9b6c6", "#5c6878"),
        ("Silver", "the last few percent, any price", "specialty plating", "#ffffff", "#c9ced6", "#6b7280"),
    ]
    for i, (name, need, use, top, front, side) in enumerate(metals):
        cx = 100 + i * 193
        parts.append(panel(cx - 88, 15, 176, 370))
        parts.append(text(cx, 48, "When you need", 12, MUTED))
        words = need.split(" ")
        half = (len(words) + 1) // 2
        parts.append(text(cx, 70, " ".join(words[:half]), 14, TEXT, weight="bold"))
        parts.append(text(cx, 89, " ".join(words[half:]), 14, TEXT, weight="bold"))
        parts += _ingot(cx - 62, 250, 104, 40, 70, top, front, side)
        parts.append(text(cx, 300, name, 19, front, weight="bold"))
        parts.append(text(cx, 324, use, 12, TEXT))
    return svg(w, h, "\n".join(parts), "Four metal ingots, copper, gold, aluminum and silver, each labelled with the need that makes it the right choice")


FIGURES = {
    "copper_atom.svg": copper_atom,
    "electron_sea.svg": electron_sea,
    "two_factors.svg": two_factors,
    "resistivity_scale.svg": resistivity_scale,
    "marbles.svg": marbles,
    "temperature_curves.svg": temperature_curves,
    "material_families.svg": material_families,
    "heat_feedback.svg": heat_feedback,
    "doping.svg": doping,
    "choosing_conductor.svg": choosing_conductor,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in FIGURES.items():
        (OUT / name).write_text(fn())
        print("wrote", OUT / name)


if __name__ == "__main__":
    main()
