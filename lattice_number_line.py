#!/usr/bin/env python3
"""
Number-line visualization of pseudocubic lattice constants for PLD.

Substrates point up at the line from below; film materials point down at it
from above, in the style of the classic figure in Schlom et al.,
"Strain Tuning of Ferroelectric Thin Films", Annu. Rev. Mater. Res. 37, 589 (2007).

Data provenance
---------------
All values are room-temperature *experimental* pseudocubic lattice constants
taken from the crystal-growth / thin-film literature (references per entry
below). For strain engineering, prefer experimental values over DFT databases
(Materials Project, OQMD, AFLOW): PBE/PBEsol-relaxed lattice constants carry
~0.5-1 % systematic error, i.e. 0.02-0.04 Angstrom -- larger than the entire
spacing between neighboring scandate substrates. Good primary sources:
  * R. Uecker et al., J. Cryst. Growth 310, 2649 (2008)  (REScO3 series)
  * D. Klimm et al., Cryst. Res. Technol. 55, 1900111 (2020)  (REScO3 review)
  * D. G. Schlom et al., Annu. Rev. Mater. Res. 37, 589 (2007)  (Table 1)
  * ICSD / Crystallography Open Database (COD) for individual refinements.

Usage
-----
    python lattice_number_line.py            # prints the data table, then
                                             # opens an interactive window
                                             # (save via the toolbar's disk icon)
    python lattice_number_line.py --save     # additionally writes PNG + SVG
Edit RANGE, BST_Y, or the MATERIALS list to customize.
"""

from dataclasses import dataclass

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

RANGE = (3.80, 4.01)          # Angstrom window (4.01 keeps BaRuO3 and NdScO3 in)
MIN_LABEL_SEP = 0.0065        # Angstrom; closer neighbors get staggered tiers

# Category -> side of the line and legend label.
CATEGORIES = {
    "substrate":  dict(side="below", label="Substrates (standard)"),
    "scandate":   dict(side="below", label="Substrates (REScO$_3$ series)"),
    "film_fe":    dict(side="above", label="Films: ferroelectric / dielectric"),
    "film_cond":  dict(side="above", label="Films: conducting / magnetic"),
}

# Pick the color scheme here.  "category" colors the four categories
# separately; "simple" uses one color for all substrates and one for all
# films (the solid-solution bar keeps RANGE_COLOR in both).  Colors are a
# colorblind-safe Okabe-Ito subset (validated: adjacent-pair CVD dE >= 8.5).
COLOR_SCHEME = "category"     # "category" or "simple"

COLOR_SCHEMES = {
    "category": {"substrate": "#0072B2", "scandate": "#009E73",
                 "film_fe": "#E69F00", "film_cond": "#CC79A7"},
    "simple":   {"substrate": "#0072B2", "scandate": "#0072B2",
                 "film_fe": "#009E73", "film_cond": "#009E73"},
}
RANGE_COLOR = "#D55E00"       # solid-solution range arrows


def category_color(category):
    return COLOR_SCHEMES[COLOR_SCHEME][category]


def legend_entries():
    """(label, color) pairs matching the active color scheme."""
    if COLOR_SCHEME == "simple":
        entries = [("Substrates", COLOR_SCHEMES["simple"]["substrate"]),
                   ("Films", COLOR_SCHEMES["simple"]["film_fe"])]
    else:
        entries = [(v["label"], category_color(k))
                   for k, v in CATEGORIES.items()]
    entries.append(("Solid-solution range", RANGE_COLOR))
    return entries


@dataclass
class Material:
    label: str        # mathtext label
    a: float          # pseudocubic lattice constant, Angstrom (RT)
    category: str
    note: str = ""    # provenance / caveat


# --------------------------------------------------------------------------
# Curated data (pseudocubic a, room temperature, Angstrom)
# --------------------------------------------------------------------------

MATERIALS = [
    # -- Substrates: standard perovskites ----------------------------------
    Material("LaAlO$_3$",      3.790, "substrate", "Schlom 2007; outside default range"),
    Material("NSAT",           3.840, "substrate", "(NdAlO3)0.39(SrAl1/2Ta1/2O3)0.61; 3.835-3.85 depending on composition (IUCr Acta Cryst B 2026)"),
    Material("NdGaO$_3$",      3.858, "substrate", "orthorhombic, avg pseudocubic (Schmidbauer high-precision)"),
    Material("LSAT",           3.868, "substrate", "(LaAlO3)0.29(SrAl1/2Ta1/2O3)0.71"),
    Material("LaGaO$_3$",      3.892, "substrate", "orthorhombic, avg pseudocubic"),
    Material("SrTiO$_3$",      3.905, "substrate", "cubic"),
    Material("SAGT",           3.925, "substrate", "Sr(Al,Ga,Ta)O3 double perovskite (arXiv:2310.12573)"),
    Material("KTaO$_3$",       3.989, "substrate", "cubic"),
    # -- Substrates: rare-earth scandates (Uecker 2008 / Klimm 2020) -------
    Material("DyScO$_3$",      3.944, "scandate"),
    Material("TbScO$_3$",      3.958, "scandate"),
    Material("GdScO$_3$",      3.968, "scandate"),
    Material("EuScO$_3$",      3.978, "scandate", "not sold commercially; (Sm,Gd)ScO3 mixed crystals substitute (Klimm 2020)"),
    Material("SmScO$_3$",      3.987, "scandate"),
    Material("NdScO$_3$",      4.008, "scandate"),
    Material("PrScO$_3$",      4.020, "scandate", "outside default range"),
    # -- Films: ferroelectric / dielectric (from the Schlom figure) --------
    Material("Bi$_4$Ti$_3$O$_{12}$",    3.85,  "film_fe", "Aurivillius, avg in-plane pseudo-perovskite"),
    Material("PbTiO$_3$",               3.904, "film_fe", "tetragonal a (c = 4.152)"),
    Material("EuTiO$_3$",               3.905, "film_fe", "cubic; magnetic quantum paraelectric"),
    Material("SrBi$_2$Ta$_2$O$_9$",     3.912, "film_fe", "Aurivillius, a,b/sqrt(2)"),
    Material("BiFeO$_3$",               3.965, "film_fe", "rhombohedral pseudocubic; multiferroic"),
    Material("BiMnO$_3$",               3.99,  "film_fe", "highly distorted monoclinic, approx. pseudocubic"),
    Material("BaTiO$_3$",               3.992, "film_fe", "tetragonal a (c = 4.036)"),
    # -- Films: other titanates ---------------------------------------------
    Material("CaTiO$_3$",               3.824, "film_fe", "orthorhombic, (V/4)^(1/3); incipient ferroelectric"),
    # -- Films: conducting / magnetic oxides (electrodes, manganites, ...) -
    # Manganites La(1-x)Sr(x)MnO3 -- a_pc shrinks with Sr doping
    Material("LaMnO$_3$",               3.935, "film_cond", "Jahn-Teller orthorhombic, (V/4)^(1/3); parent manganite"),
    Material("LSMO $x$=0.2",            3.88,  "film_cond", "La0.8Sr0.2MnO3, rhombohedral pseudocubic (approx.)"),
    Material("LSMO $x$=0.3",            3.876, "film_cond", "La0.67Sr0.33MnO3, rhombohedral pseudocubic (~3.87-3.88)"),
    Material("LSMO $x$=0.5",            3.86,  "film_cond", "La0.5Sr0.5MnO3, tetragonal (approx.; ~3.85-3.87 in lit.)"),
    Material("SrMnO$_3$",               3.805, "film_cond", "cubic perovskite polymorph (4H hexagonal ambient-stable)"),
    Material("LCMO",                    3.858, "film_cond", "La0.67Ca0.33MnO3, orthorhombic pseudocubic; CMR manganite"),
    # Nickelates
    Material("LaNiO$_3$",               3.838, "film_cond", "rhombohedral pseudocubic; metallic electrode"),
    Material("PrNiO$_3$",               3.820, "film_cond", "orthorhombic pseudocubic; MIT nickelate"),
    Material("NdNiO$_3$",               3.807, "film_cond", "orthorhombic pseudocubic; MIT nickelate"),
    # Ruthenates
    Material("SrRuO$_3$",               3.93,  "film_cond", "orthorhombic pseudocubic; metallic electrode"),
    Material("CaRuO$_3$",               3.84,  "film_cond", "orthorhombic, (V/4)^(1/3) (3.84-3.85 in lit.)"),
    Material("BaRuO$_3$",               4.006, "film_cond", "cubic perovskite polymorph (high-pressure phase; 4H/9R ambient-stable)"),
    # Iridates
    Material("SrIrO$_3$",               3.96,  "film_cond", "orthorhombic perovskite polymorph, pseudocubic; semimetal"),
    # Other conductors
    Material("SrVO$_3$",                3.842, "film_cond", "cubic; correlated metal / transparent conductor"),
    Material("YBa$_2$Cu$_3$O$_7$",      3.855, "film_cond", "avg of a = 3.82, b = 3.89"),
    Material("SrMoO$_3$",               3.976, "film_cond", "cubic; lowest-resistivity oxide metal"),
]

# Solid-solution films drawn as horizontal range arrows above the film labels.
# BST_Y sets the height of the (Ba,Sr)TiO3 bar in axis data units: the number
# line sits at y = 0 and the film label tips reach up to about y = 0.9, so
# values around 1.0-1.25 float the bar above the labels; smaller values pull
# it down toward the line.
BST_Y = 1.06

# (label, a_min, a_max, open_ended_right, y_position)
RANGES = [
    ("(Ba,Sr)TiO$_3$",  3.905, 3.994, False, BST_Y),  # SrTiO3 -> BaTiO3
]


# --------------------------------------------------------------------------
# Layout: stagger near-coincident labels onto tiers (pure logic, testable)
# --------------------------------------------------------------------------

def assign_tiers(xs, min_sep=MIN_LABEL_SEP, n_tiers=4):
    """Greedy tier assignment for one side of the line.

    xs: sorted list of x positions. Returns a list of tier indices (0 = closest
    to the line) such that any two labels on the same tier are >= min_sep apart.
    """
    last_x = [-1e9] * n_tiers
    tiers = []
    for x in xs:
        for t in range(n_tiers):
            if x - last_x[t] >= min_sep:
                tiers.append(t)
                last_x[t] = x
                break
        else:  # more than n_tiers collisions; stack on the outermost tier
            tiers.append(n_tiers - 1)
            last_x[n_tiers - 1] = x
    return tiers


def in_range(m, lo=RANGE[0], hi=RANGE[1]):
    return lo <= m.a <= hi


def compute_layout():
    """Split materials by side, sort, and assign tiers. Returns dict."""
    shown = [m for m in MATERIALS if in_range(m)]
    layout = {}
    for side in ("below", "above"):
        ms = sorted((m for m in shown
                     if CATEGORIES[m.category]["side"] == side),
                    key=lambda m: m.a)
        layout[side] = list(zip(ms, assign_tiers([m.a for m in ms])))
    return layout


# --------------------------------------------------------------------------
# Plot
# --------------------------------------------------------------------------

def make_figure():
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    lo, hi = RANGE
    fig, ax = plt.subplots(figsize=(15, 7.5))
    ax.set_xlim(lo - 0.006, hi + 0.006)
    y_top = max([1.35] + [r[4] + 0.15 for r in RANGES])
    ax.set_ylim(-1.0, y_top)
    ax.axis("off")

    # ---- The number line with major/minor ticks --------------------------
    # Integer loop: np.arange floats accumulate rounding error, which made
    # `(x*100) % 5` misclassify every major tick except the first, so only
    # "3.80" was ever labeled. i is exact hundredths of an Angstrom.
    ax.hlines(0, lo, hi, color="black", lw=1.8, zorder=3)
    for i in range(round(lo * 100), round(hi * 100) + 1):
        x = i / 100
        major = i % 5 == 0                          # labeled mark every 0.05 A
        ax.vlines(x, -0.035 if major else -0.02, 0.035 if major else 0.02,
                  color="black", lw=1.2 if major else 0.7, zorder=3)
        if major:
            ax.text(x, -0.055, f"{x:.2f}", ha="center", va="top",
                    fontsize=11, zorder=3)

    # ---- Arrows + labels, staggered by tier ------------------------------
    base, step = 0.16, 0.24                          # arrow lengths per tier
    for side, sign in (("below", -1), ("above", +1)):
        for m, tier in compute_layout()[side]:
            c = category_color(m.category)
            y_tip = sign * (base + tier * step)
            ax.annotate("", xy=(m.a, 0), xytext=(m.a, y_tip), zorder=2,
                        arrowprops=dict(arrowstyle="-|>", color=c, lw=1.6,
                                        mutation_scale=14, shrinkA=0, shrinkB=2))
            ax.text(m.a, y_tip + sign * 0.02, m.label, rotation=90,
                    ha="center", va="bottom" if sign > 0 else "top",
                    fontsize=10.5, color=c, zorder=4)

    # ---- Solid-solution range arrows -------------------------------------
    for label, a0, a1, open_right, y in RANGES:
        x0, x1 = max(a0, lo), min(a1, hi)
        style = "-|>" if (open_right and a1 > hi) else "|-|,widthA=0.35,widthB=0.35"
        ax.annotate("", xy=(x1, y), xytext=(x0, y),
                    arrowprops=dict(arrowstyle=style, color=RANGE_COLOR,
                                    lw=1.8, mutation_scale=12))
        ax.text(x0 + 0.004, y + 0.025, label, ha="left", va="bottom",
                fontsize=10.5, color=RANGE_COLOR)

    # ---- Axis titles and legend ------------------------------------------
    ax.text(lo - 0.004, -0.30, "Substrates", ha="left", va="center",
            fontsize=12, style="italic", color="0.25")
    ax.text(lo - 0.004, 0.30, "Films", ha="left", va="center",
            fontsize=12, style="italic", color="0.25")
    ax.set_title("Pseudocubic lattice constants of perovskite films and "
                 f"substrates, {lo:.2f}–{hi:.2f} Å",
                 fontsize=14, pad=18)
    fig.text(0.5, 0.015, "Pseudocubic lattice constant $a$ (Å)",
             ha="center", fontsize=12)
    handles = [Line2D([], [], color=color, lw=3, label=label)
               for label, color in legend_entries()]
    ax.legend(handles=handles, loc="lower right", frameon=False, fontsize=10,
              bbox_to_anchor=(1.0, -0.04))

    fig.tight_layout()
    return fig


# --------------------------------------------------------------------------
# Convenience: misfit strain of a film on a substrate
# --------------------------------------------------------------------------

def misfit(film_a, substrate_a):
    """Biaxial misfit strain (%) of a film clamped to a substrate."""
    return 100.0 * (substrate_a - film_a) / film_a


def _plain(label):
    return (label.replace("$", "").replace("_", "").replace("{", "")
            .replace("}", ""))


def print_table():
    """Table of every lattice constant drawn on the number line."""
    shown = sorted((m for m in MATERIALS if in_range(m)), key=lambda m: m.a)
    w = ("material", "a_pc (Å)", "category", "note")
    print(f"Lattice constants on the line ({RANGE[0]:.2f}-{RANGE[1]:.2f} Å)")
    print(f"{w[0]:<14}{w[1]:>10}  {w[2]:<11}{w[3]}")
    print("-" * 78)
    for m in shown:
        print(f"{_plain(m.label):<14}{m.a:>10.3f}  {m.category:<11}{m.note}")
    for label, a0, a1, _open, _y in RANGES:
        print(f"{_plain(label):<14}{a0:>6.3f}-{a1:.3f}  {'range':<11}"
              "solid-solution span")
    omitted = [m for m in MATERIALS if not in_range(m)]
    if omitted:
        names = ", ".join(f"{_plain(m.label)} ({m.a:.3f})" for m in omitted)
        print(f"\nIn the data set but outside the plotted range: {names}")


if __name__ == "__main__":
    import sys
    print_table()
    fig = make_figure()
    if "--save" in sys.argv:
        for ext in ("png", "svg"):
            fig.savefig(f"lattice_number_line.{ext}", dpi=300,
                        bbox_inches="tight")
            print(f"wrote lattice_number_line.{ext}")
    # Interactive window; save any view via the toolbar's disk icon.
    import matplotlib.pyplot as plt
    plt.show()
