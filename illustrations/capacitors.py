#!/usr/bin/env python3
"""Figures for docs/capacitors.md.

Sources:
- Permittivity of free space e0 = 8.854e-12 F/m (CODATA).
- Wikipedia "Electrolytic capacitor": relative permittivity Al2O3 9.6, Ta2O5 27;
  oxide thickness 1.4 nm/V (aluminium).
- Wikipedia "Ceramic capacitor": class 1 er 6-200, class 2 (barium titanate) 200-14,000.
- Wikipedia "Flashtube": "a 330 microfarad capacitor charged to 300 volts (common
  ballpark values found in cameras) stores almost 15 joules".
- Rubycon FW photoflash capacitor datasheet: rated 330 Vdc; charge/discharge test
  through a xenon flash tube of 0.7-1.0 ohm.
- RC charging: V(t) = V0 (1 - e^(-t/RC)); every number below is computed.

Usage:
    python3 illustrations/capacitors.py
"""

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from style3d import (AMBER, AMBER_LIGHT, GREEN, MUTED, RED, TEXT, box3d,  # noqa: E402
                     common_defs, cyl_gradient, panel, pill, render_all, shade,
                     svg, text)
from ac_dc import axes, glow_line  # noqa: E402

OUT = HERE.parent / "docs" / "images" / "capacitors"
E0 = 8.854e-12
PLUS, MINUS, FIELD = "#fc8181", "#90cdf4", "#fbd38d"

# The camera flash used throughout the article.
C_FLASH, V_FLASH, R_TUBE = 330e-6, 300.0, 1.0
E_FLASH = 0.5 * C_FLASH * V_FLASH ** 2          # 14.85 J
TAU_FLASH = R_TUBE * C_FLASH                     # 330 us


def plate(x, y, w, d, color, label=None):
    """A thin 3D metal plate, front-bottom-left at (x, y)."""
    out = box3d(x, y, w, d, 8, color, shadow=False)
    if label:
        out.append(text(x - 12, y - 2, label, 13, TEXT, "end"))
    return out


def charge_dot(x, y, sign):
    col = PLUS if sign > 0 else MINUS
    return [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{col}" fill-opacity="0.9"/>',
            text(x, y + 4, "+" if sign > 0 else "−", 11, "#1a1a1a", weight="bold")]


# 1. Inside a capacitor ------------------------------------------------------------------
def inside():
    w, h = 820, 460
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Two plates, an insulator between, and charge parked on each side", 16, TEXT, weight="bold"))
    x, w_pl, d = 250, 300, 110
    top_y, bot_y = 170, 330
    # dielectric slab between the plates
    parts += box3d(x + 4, bot_y - 10, w_pl - 8, d - 6, bot_y - top_y - 20, "#2c5282", shadow=False)
    parts.append(f'<rect x="{x + 4}" y="{top_y + 10}" width="{w_pl - 8}" height="{bot_y - top_y - 20}" fill="#90cdf4" fill-opacity="0.12"/>')
    for k in range(6):
        fx = x + 30 + k * 48
        parts.append(f'<line x1="{fx}" y1="{top_y + 16}" x2="{fx}" y2="{bot_y - 22}" stroke="{FIELD}" stroke-width="2" '
                     f'stroke-dasharray="5 4" marker-end="url(#arrow)"/>')
    parts += plate(x, bot_y, w_pl, d, "#a0aec0")
    parts += plate(x, top_y, w_pl, d, "#a0aec0")
    for k in range(8):
        parts += charge_dot(x + 25 + k * 36 + 20, top_y - 14, +1)
        parts += charge_dot(x + 25 + k * 36 + 20, bot_y + 18, -1)
    # leads and battery
    parts.append(f'<path d="M{x},{top_y - 4} L150,{top_y - 4} L150,215" fill="none" stroke="#cbd5e0" stroke-width="4"/>')
    parts.append(f'<path d="M{x},{bot_y - 4} L150,{bot_y - 4} L150,285" fill="none" stroke="#cbd5e0" stroke-width="4"/>')
    parts.append(f'<rect x="126" y="215" width="48" height="70" rx="6" fill="url(#core)"/>')
    parts.append(text(150, 247, "9 V", 14, "#ffffff", weight="bold"))
    parts.append(text(150, 266, "+ top", 10, "#e2e8f0"))
    parts.append(text(x + w_pl + 95, top_y - 8, "plate: + charge", 13, PLUS, "start", "bold"))
    parts.append(text(x + w_pl + 95, (top_y + bot_y) / 2 - 8, "dielectric:", 13, "#90cdf4", "start", "bold"))
    parts.append(text(x + w_pl + 95, (top_y + bot_y) / 2 + 10, "an insulator; no charge", 12, TEXT, "start"))
    parts.append(text(x + w_pl + 95, (top_y + bot_y) / 2 + 26, "crosses it, only the field", 12, TEXT, "start"))
    parts.append(text(x + w_pl + 95, bot_y + 22, "plate: − charge", 13, MINUS, "start", "bold"))
    parts.append(text(w / 2, 418, "Equal and opposite: every + on one plate is matched by a − on the other.", 13, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "A 3D capacitor opened up: two metal plates with a blue insulating dielectric between them, connected to a 9 volt battery. The top plate carries positive charges and the bottom plate an equal number of negative charges; dashed field lines cross the dielectric, but no charge does.")


# 2. Q = CV as tanks --------------------------------------------------------------------
def tanks():
    w, h = 820, 440
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Same voltage, different capacitance: the wider tank holds more", 16, TEXT, weight="bold"))
    base, top = 350, 120
    level = 175  # both filled to the same height (9 V)
    for cx, width, cap in ((250, 70, 10), (560, 260, 100)):
        x0 = cx - width / 2
        q = cap * 9
        parts += box3d(x0, base, width, 60, base - level, "#3182ce", shadow=True)
        parts.append(f'<rect x="{x0:.1f}" y="{top}" width="{width}" height="{base - top}" fill="none" stroke="#cbd5e0" stroke-opacity="0.7" stroke-width="2"/>')
        parts.append(f'<line x1="{x0:.1f}" y1="{top}" x2="{x0 + 42:.1f}" y2="{top - 27}" stroke="#cbd5e0" stroke-opacity="0.5"/>')
        parts.append(f'<line x1="{x0 + width:.1f}" y1="{top}" x2="{x0 + width + 42:.1f}" y2="{top - 27}" stroke="#cbd5e0" stroke-opacity="0.5"/>')
        parts.append(text(cx, base + 34, f"{cap} µF at 9 V", 15, AMBER_LIGHT, weight="bold"))
        parts.append(text(cx, base + 54, f"Q = C × V = {q} µC", 13, TEXT))
    parts.append(f'<line x1="30" y1="{level}" x2="740" y2="{level}" stroke="{AMBER}" stroke-dasharray="6 5" stroke-width="2"/>')
    parts.append(text(35, level - 8, "height = voltage (9 V)", 12, AMBER_LIGHT, "start", "bold"))
    parts.append(text(35, 230, "width = capacitance", 12, "#90cdf4", "start", "bold"))
    parts.append(text(35, 248, "water = charge", 12, "#90cdf4", "start", "bold"))
    return svg(w, h, "\n".join(parts), "Two 3D tanks filled with water to the same height, marked 9 volts. The narrow tank is a 10 microfarad capacitor holding 90 microcoulombs; the tank ten times wider is a 100 microfarad capacitor holding 900 microcoulombs.")


# 3. What sets C ------------------------------------------------------------------------
def what_sets_c():
    w, h = 880, 420
    parts = [common_defs()]
    base = dict(area=0.01, gap=1e-3, er=1.0)
    cases = [("Starting point", base, "10 × 10 cm plates, 1 mm of air"),
             ("Double the area", dict(base, area=0.02), "twice the plate"),
             ("Halve the gap", dict(base, gap=0.5e-3), "plates twice as close"),
             ("Better dielectric", dict(base, er=9.6), "aluminium oxide, εr 9.6")]
    for i, (title, p, sub) in enumerate(cases):
        cx = 115 + i * 217
        parts.append(panel(cx - 100, 20, 200, 380))
        parts.append(text(cx, 52, title, 15, AMBER_LIGHT, weight="bold"))
        pw = 90 * (2 if p["area"] > base["area"] else 1) ** 0.5
        gap_px = 60 * p["gap"] / base["gap"]
        y_bot = 250
        y_top = y_bot - gap_px - 8
        if p["er"] > 1:
            parts += box3d(cx - pw / 2 - 10, y_bot - 8, pw, 50, gap_px, "#2c5282", shadow=False)
        parts += box3d(cx - pw / 2 - 10, y_bot, pw, 50, 8, "#a0aec0", shadow=True)
        parts += box3d(cx - pw / 2 - 10, y_top, pw, 50, 8, "#a0aec0", shadow=False)
        c = E0 * p["er"] * p["area"] / p["gap"]
        parts.append(text(cx, 315, f"{c * 1e12:.0f} pF", 22, TEXT, weight="bold"))
        parts.append(text(cx, 340, sub, 12, MUTED))
    return svg(w, h, "\n".join(parts), "Four parallel-plate capacitors. Two 10 by 10 centimetre plates 1 millimetre apart in air give 89 picofarads. Doubling the area gives 177 picofarads, halving the gap gives 177 picofarads, and filling the gap with aluminium oxide, relative permittivity 9.6, gives 850 picofarads.")


# 4. Energy = half QV ---------------------------------------------------------------------
def energy_triangle():
    w, h = 800, 440
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Each extra coulomb is pushed in against a higher voltage", 16, TEXT, weight="bold"))
    L, R, T, B = 110, 560, 90, 360
    q_max = C_FLASH * V_FLASH
    axes(parts, L, R, T, B, B, f"charge stored (0 to {q_max * 1000:.0f} mC)", [(T + 10, f"{V_FLASH:.0f} V"), ((T + 10 + B) / 2, f"{V_FLASH / 2:.0f} V")])
    parts.append(f'<polygon points="{L},{B} {R},{T + 10} {R},{B}" fill="{AMBER}" fill-opacity="0.28"/>')
    parts.append(glow_line([(L, B), (R, T + 10)], AMBER))
    parts.append(f'<line x1="{L}" y1="{(T + 10 + B) / 2}" x2="{R}" y2="{(T + 10 + B) / 2}" stroke="#90cdf4" stroke-dasharray="6 5"/>')
    parts.append(text(470, 300, "area = energy", 14, AMBER_LIGHT, weight="bold"))
    parts.append(text(470, 320, "= ½ × Q × V", 14, AMBER_LIGHT, weight="bold"))
    parts.append(text(L + 8, (T + 10 + B) / 2 - 8, "average: half the final voltage", 12, "#90cdf4", "start"))
    x0 = 590
    for k, line in enumerate([f"{C_FLASH * 1e6:.0f} µF at {V_FLASH:.0f} V", f"Q = {q_max * 1000:.0f} mC",
                              f"E = ½ C V²", f"  = {E_FLASH:.2f} J"]):
        parts.append(text(x0, 150 + k * 28, line, 15, TEXT if k < 2 else AMBER_LIGHT, "start", "bold" if k == 3 else "normal"))
    parts.append(text(x0, 280, "a camera flash", 12, MUTED, "start", italic=True))
    parts.append(text(x0, 296, "capacitor (Wikipedia,", 12, MUTED, "start", italic=True))
    parts.append(text(x0, 312, "\"Flashtube\")", 12, MUTED, "start", italic=True))
    return svg(w, h, "\n".join(parts), f"A graph of voltage against charge for a capacitor: a straight line from zero to 300 volts as 99 millicoulombs are stored. The shaded triangle under it is the stored energy, half of charge times voltage: {E_FLASH:.2f} joules for a 330 microfarad flash capacitor at 300 volts.")


# 5. RC charging and discharging ---------------------------------------------------------
def rc_curve():
    w, h = 880, 440
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "Fast at first, then slower and slower: the RC curve", 16, TEXT, weight="bold"))
    L, R, T, B = 90, 820, 90, 360
    span = 5.0
    axes(parts, L, R, T, B, B, "time, in time constants (τ = R × C)", [(T, "100%"), (B - 0.632 * (B - T), "63%")])
    xs = [k * span / 400 for k in range(401)]
    up = [(L + (R - L) * t / span, B - (B - T) * (1 - math.exp(-t))) for t in xs]
    dn = [(L + (R - L) * t / span, B - (B - T) * math.exp(-t)) for t in xs]
    parts.append(glow_line(up, AMBER))
    parts.append(glow_line(dn, "#90cdf4"))
    for n in range(1, 6):
        x = L + (R - L) * n / span
        pct = 100 * (1 - math.exp(-n))
        parts.append(f'<line x1="{x:.1f}" y1="{T}" x2="{x:.1f}" y2="{B}" stroke="#4a5568" stroke-opacity="0.5"/>')
        parts.append(text(x + 4, B - 6, f"{n}τ", 11, MUTED, "start"))
        y = B - (B - T) * (1 - math.exp(-n))
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{AMBER}"/>')
        parts.append(text(x - 4, y - 10, f"{pct:.1f}%", 11, AMBER_LIGHT, "end", "bold"))
    parts.append(text(R - 120, T + 40, "charging", 14, AMBER_LIGHT, weight="bold"))
    parts.append(text(R - 120, B - 30, "discharging", 14, "#90cdf4", weight="bold"))
    parts.append(text(L + 110, 405, "10 kΩ × 100 µF: τ = 1 s, full (99%) in about 5 s", 12, MUTED, "start", italic=True))
    return svg(w, h, "\n".join(parts), "Two curves against time measured in time constants. Charging rises steeply then levels off: 63.2 percent after one time constant, 86.5 after two, 95.0 after three, 98.2 after four and 99.3 after five. Discharging is the mirror image, falling to 36.8 percent after one time constant.")


# 6. The flash: slow in, fast out ----------------------------------------------------------
def flash():
    w, h = 880, 440
    parts = [common_defs(cyl_gradient("cap", "#2b6cb0", vertical=True)), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "The same 15 joules, in slowly and out fast", 16, TEXT, weight="bold"))
    # two AA cells
    for k in range(2):
        parts.append(f'<rect x="{60 + k * 34}" y="190" width="28" height="80" rx="5" fill="url(#copperball)"/>')
    parts.append(text(94, 292, "2 × AA", 13, TEXT))
    parts.append(text(94, 310, "3 V", 13, MUTED))
    parts.append(f'<line x1="135" y1="230" x2="215" y2="230" stroke="#cbd5e0" stroke-width="4" marker-end="url(#arrow)"/>')
    parts += box3d(215, 270, 110, 50, 80, "#2d3748")
    parts.append(text(270, 225, "step-up", 13, "#ffffff", weight="bold"))
    parts.append(text(270, 243, "charger", 13, "#ffffff", weight="bold"))
    parts.append(f'<line x1="350" y1="230" x2="430" y2="230" stroke="#cbd5e0" stroke-width="4" marker-end="url(#arrow)"/>')
    parts.append(f'<rect x="440" y="160" width="70" height="140" rx="12" fill="url(#cap)"/>')
    parts.append(f'<rect x="440" y="160" width="14" height="140" fill="#cbd5e0" fill-opacity="0.35"/>')
    parts.append(text(475, 220, "330 µF", 12, "#ffffff", weight="bold"))
    parts.append(text(475, 238, "300 V", 12, "#ffffff", weight="bold"))
    parts.append(f'<line x1="520" y1="230" x2="610" y2="230" stroke="{AMBER}" stroke-width="7" marker-end="url(#arrow)"/>')
    parts.append(f'<ellipse cx="700" cy="230" rx="85" ry="38" fill="url(#glow)"/>')
    parts.append(f'<rect x="625" y="216" width="150" height="28" rx="14" fill="#fff7e0" filter="url(#softglow)"/>')
    parts.append(text(700, 290, "xenon flash tube, ~1 Ω", 13, TEXT))
    p_in = E_FLASH / 5
    p_out = E_FLASH / (3 * TAU_FLASH)
    parts += pill(230, 365, f"in: ~5 s, ~{p_in:.0f} W", "#2c5282", size=15, wpx=230)
    parts += pill(650, 365, f"out: ~{3 * TAU_FLASH * 1000:.0f} ms, ~{p_out / 1000:.0f} kW", "#b7791f", size=15, wpx=260)
    parts.append(text(w / 2, 410, f"τ = 1 Ω × 330 µF = {TAU_FLASH * 1e6:.0f} µs; three time constants empty 95% of the charge", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Two AA cells feed a step-up charger that fills a 330 microfarad, 300 volt capacitor over about 5 seconds, about 3 watts. The capacitor then dumps its 15 joules into a xenon flash tube of about 1 ohm in about a millisecond, about 15 kilowatts.")


# 7. Kinds of capacitors -------------------------------------------------------------------
def kinds():
    w, h = 900, 400
    grads = (cyl_gradient("alcan", "#2b6cb0") + cyl_gradient("supcap", "#2d3748") + cyl_gradient("tant", "#d69e2e"))
    parts = [common_defs(grads)]
    cards = [("Ceramic", "1 pF to ~10 µF", "no polarity"),
             ("Film", "1 nF to ~10 µF", "no polarity"),
             ("Electrolytic", "1 µF to 100,000 µF", "polarized: stripe = −"),
             ("Tantalum", "0.1 µF to ~1,000 µF", "polarized: stripe = +"),
             ("Supercapacitor", "0.1 F to thousands of F", "polarized, low voltage")]
    for i, (name, rng, pol) in enumerate(cards):
        cx = 95 + i * 177
        parts.append(panel(cx - 82, 20, 164, 360))
        cy = 160
        if i == 0:
            parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="38" ry="34" fill="#dd8a3c"/>')
            parts.append(f'<ellipse cx="{cx - 10}" cy="{cy - 12}" rx="16" ry="10" fill="#ffffff" fill-opacity="0.35"/>')
            parts.append(text(cx, cy + 6, "104", 14, "#1a1a1a", weight="bold"))
            legs = (-12, 12)
        elif i == 1:
            parts += box3d(cx - 34, cy + 30, 60, 26, 64, "#c53030")
            parts.append(text(cx - 4, cy + 4, ".1J", 13, "#ffffff", weight="bold"))
            legs = (-16, 16)
        elif i == 2:
            parts.append(f'<rect x="{cx - 30}" y="{cy - 60}" width="60" height="110" rx="8" fill="url(#alcan)"/>')
            parts.append(f'<rect x="{cx + 12}" y="{cy - 60}" width="14" height="110" fill="#e2e8f0" fill-opacity="0.85"/>')
            for k in range(4):
                parts.append(text(cx + 19, cy - 36 + k * 24, "−", 13, "#2b6cb0", weight="bold"))
            legs = (-12,)
            parts.append(f'<rect x="{cx + 10}" y="{cy + 50}" width="4" height="36" fill="#cbd5e0"/>')
        elif i == 3:
            parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="30" ry="38" fill="url(#tant)"/>')
            parts.append(text(cx, cy + 6, "+", 18, "#1a1a1a", weight="bold"))
            legs = (-10, 10)
        else:
            parts.append(f'<rect x="{cx - 42}" y="{cy - 40}" width="84" height="86" rx="10" fill="url(#supcap)"/>')
            parts.append(text(cx, cy, "1 F", 16, "#ffffff", weight="bold"))
            parts.append(text(cx, cy + 20, "5.5 V", 12, "#e2e8f0"))
            legs = (-18, 18)
        for dx in legs:
            parts.append(f'<rect x="{cx + dx - 2}" y="{cy + 50}" width="4" height="50" fill="#cbd5e0"/>')
        parts.append(text(cx, 290, name, 16, AMBER_LIGHT, weight="bold"))
        parts.append(text(cx, 314, rng, 12, TEXT))
        parts.append(text(cx, 336, pol, 12, MUTED))
    return svg(w, h, "\n".join(parts), "Five kinds of capacitor. Ceramic, an orange disc marked 104, 1 picofarad to about 10 microfarads, no polarity. Film, a red box, 1 nanofarad to about 10 microfarads, no polarity. Aluminium electrolytic, a blue can with a stripe of minus signs and a shorter negative lead, 1 to 100,000 microfarads. Tantalum, a yellow bead marked plus, polarized the other way. Supercapacitor, a dark block marked 1 farad 5.5 volts.")


# 8. Smoothing a rectified supply ---------------------------------------------------------
def smoothing():
    w, h = 880, 420
    parts = [common_defs(), panel(15, 15, w - 30, h - 30)]
    parts.append(text(w / 2, 48, "A capacitor fills on each peak and feeds the load in between", 16, TEXT, weight="bold"))
    L, R, T, B = 80, 830, 110, 350
    vpk, f = 17.0, 120.0  # full-wave rectified 60 Hz, 12 V RMS transformer, ~17 V peak
    cap, load = 2200e-6, 100.0
    t_end = 3 / 60
    axes(parts, L, R, T, B, B, "time: three cycles of 60 Hz mains (50 ms)", [(T, f"{vpk:.0f} V"), (B - (B - T) / 2, f"{vpk / 2:.1f} V")])
    n = 1200
    raw, smooth = [], []
    v = vpk
    for k in range(n + 1):
        t = t_end * k / n
        r = vpk * abs(math.sin(2 * math.pi * 60 * t))
        if k:
            v *= math.exp(-(t_end / n) / (load * cap))
        v = max(v, r)
        X = L + (R - L) * k / n
        raw.append((X, B - (B - T) * r / vpk))
        smooth.append((X, B - (B - T) * v / vpk))
    parts.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in raw)}" fill="none" stroke="#90cdf4" stroke-width="2" stroke-dasharray="5 4"/>')
    parts.append(glow_line(smooth, AMBER))
    ripple = vpk * (1 - math.exp(-1 / (f * load * cap)))
    parts.append(text(R, 84, f"with 2,200 µF across 100 Ω: ripple ≈ {ripple:.1f} V", 13, AMBER_LIGHT, "end", "bold"))
    parts.append(text(L, 84, "dashed: rectified, no capacitor", 13, "#90cdf4", "start", "bold"))
    return svg(w, h, "\n".join(parts), f"Two traces from a full-wave rectified 17 volt peak supply. Without a capacitor the voltage is a row of humps falling to zero 120 times a second. With 2,200 microfarads across a 100 ohm load, the capacitor charges at each peak and sags only about {ripple:.1f} volts between them.")


# 9. Series and parallel ----------------------------------------------------------------
def series_parallel():
    w, h = 860, 400
    parts = [common_defs(), panel(15, 15, 405, h - 30), panel(440, 15, 405, h - 30)]
    parts.append(text(217, 48, "Parallel: plate areas add", 16, AMBER_LIGHT, weight="bold"))
    for k in range(2):
        x = 75 + k * 150
        parts += plate(x, 250, 110, 50, "#a0aec0")
        parts += plate(x, 170, 110, 50, "#a0aec0")
        parts.append(text(x + 70, 122, "10 µF", 13, TEXT))
    parts.append(text(217, 310, "C = C₁ + C₂ = 20 µF", 16, TEXT, weight="bold"))
    parts.append(text(217, 334, "like more plate", 12, MUTED, italic=True))
    parts.append(text(642, 48, "Series: the gaps add", 16, AMBER_LIGHT, weight="bold"))
    parts += plate(585, 130, 110, 50, "#a0aec0")
    parts += plate(585, 195, 110, 50, "#718096")
    parts += plate(585, 260, 110, 50, "#a0aec0")
    parts.append(text(745, 150, "10 µF", 13, TEXT, "start"))
    parts.append(text(745, 192, "shared", 11, MUTED, "start"))
    parts.append(text(745, 215, "10 µF", 13, TEXT, "start"))
    parts.append(text(642, 310, "1/C = 1/C₁ + 1/C₂ → 5 µF", 16, TEXT, weight="bold"))
    parts.append(text(642, 334, "like a wider gap; voltage ratings add", 12, MUTED, italic=True))
    return svg(w, h, "\n".join(parts), "Left: two 10 microfarad capacitors side by side in parallel act like one capacitor with twice the plate area, 20 microfarads. Right: two 10 microfarad capacitors stacked in series act like one with a wider gap, 5 microfarads, with their voltage ratings adding.")


FIGURES = {"inside.svg": inside, "tanks.svg": tanks, "what_sets_c.svg": what_sets_c,
           "energy_triangle.svg": energy_triangle, "rc_curve.svg": rc_curve, "flash.svg": flash,
           "kinds.svg": kinds, "smoothing.svg": smoothing, "series_parallel.svg": series_parallel}

if __name__ == "__main__":
    render_all(FIGURES, OUT)
