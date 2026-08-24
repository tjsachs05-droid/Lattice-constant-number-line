# Lattice-constant number line for PLD

A number-line visualization of room-temperature **pseudocubic lattice constants**
of perovskite substrates and film materials in the 3.80–4.01 Å window, in the
style of the classic figure from Schlom *et al.*, *Annu. Rev. Mater. Res.* **37**,
589 (2007). Substrates point up at the line from below; films point down from
above; labeled marks every 0.05 Å. Beyond the materials in the original figure,
it adds PLD-relevant conducting/magnetic oxides: nickelates (LaNiO₃, PrNiO₃,
NdNiO₃), manganites across Sr doping (LaMnO₃, LSMO x = 0.2/0.3/0.5, SrMnO₃,
plus LCMO), ruthenates (CaRuO₃, SrRuO₃, cubic BaRuO₃), the iridate SrIrO₃,
titanates (CaTiO₃ alongside SrTiO₃/EuTiO₃/BaTiO₃/PbTiO₃), SrVO₃, SrMoO₃, and
the n = 2 Ruddlesden–Popper (327) bilayer phases La₃Ni₂O₇, Pr₃Ni₂O₇, Nd₃Ni₂O₇,
and Sr₃Ir₂O₇ — for these layered orthorhombic/tetragonal phases the plotted
value is the **in-plane pseudo-tetragonal lattice constant** (avg(a,b)/√2 of
the orthorhombic cell), the number that matters for epitaxy.
(The window ends at 4.01 rather than 4.00 so cubic BaRuO₃ at 4.006 Å and
NdScO₃ at 4.008 Å stay on the line.)

## Usage

```bash
pip install matplotlib numpy
python lattice_number_line.py          # prints the data table, then opens an
                                       # interactive window — save any view
                                       # via the toolbar's disk icon
python lattice_number_line.py --save   # additionally writes PNG + SVG files
```

Customize by editing the top of `lattice_number_line.py`:

- `RANGE` — the Å window to display (materials outside it are filtered out
  automatically; the dict already contains LaAlO₃ and PrScO₃ for a wider
  window).
- `COLOR_SCHEME` — `"category"` (default: four colors distinguishing standard
  substrates, scandates, ferroelectric films, and conducting films) or
  `"simple"` (two colors: one for all substrates, one for all films; the
  solid-solution bar keeps its own color in both schemes).
- `BST_Y` — vertical position of the (Ba,Sr)TiO₃ solid-solution bar (the
  number line is at y = 0; film labels reach up to about y = 0.9, so ~1.0–1.25
  floats the bar above them and smaller values pull it toward the line).
- `MATERIALS` — add a `Material(label, a, category, note)` entry; near-coincident
  entries are automatically staggered onto tiers so labels never collide.
- `misfit(film_a, substrate_a)` — helper returning the biaxial misfit strain (%).

## Where the numbers come from (and why not Materials Project)

All values are **experimental** room-temperature pseudocubic lattice constants
from the crystal-growth and thin-film literature. For strain engineering, avoid
taking lattice constants from DFT databases (Materials Project, OQMD, AFLOW):
PBE/PBEsol-relaxed values carry ~0.5–1 % systematic error — 0.02–0.04 Å, larger
than the entire spacing between neighboring scandate substrates. Use those
databases to *look up structures*, then take the lattice constants from
experimental refinements (ICSD, Crystallography Open Database) or from:

- R. Uecker *et al.*, [*J. Cryst. Growth* **310**, 2649 (2008)](https://www.sciencedirect.com/science/article/abs/pii/S0022024808000675) — REScO₃ series (Nd–Dy)
- D. Klimm *et al.*, [*Cryst. Res. Technol.* **55**, 1900111 (2020)](https://onlinelibrary.wiley.com/doi/full/10.1002/crat.201900111) — REScO₃ substrate review
- D. G. Schlom *et al.*, [*Annu. Rev. Mater. Res.* **37**, 589 (2007)](https://www.annualreviews.org/doi/10.1146/annurev.matsci.37.061206.113016) — Table 1, commercial perovskite substrates
- [(Nd,Sr)(Al,Ta)O₃ (NSAT) structure, *Acta Cryst.* B (2026)](https://pmc.ncbi.nlm.nih.gov/articles/PMC13058900/)

Per-entry provenance notes live in the `MATERIALS` list in the script. Values
for solid solutions (NSAT, LSAT, LSMO, LCMO…) shift with exact composition;
the notes flag the spread where it matters.

![Preview](preview.png)

*(Preview render; run the script for the full-resolution matplotlib figure.)*
