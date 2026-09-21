# Tier 5 — Compatibility, thermal mismatch, and energy

[Previous tier](../../advanced/tier-4/README.md) · [Next tier](../../advanced/tier-6/README.md)

## Learning goal

Solve a statically indeterminate load split by adding displacement compatibility.

## Model and assumptions

Two parallel rods have equal initial length. Their left ends are fixed; their right ends share a rigid plate guided to translate without rotation. A total axial force acts on that plate. Both rods experience the same uniform temperature change. Ignore guide friction, bending, buckling, and plasticity.

## Inputs

The 0.5 m rods use E1 = 200 GPa, A1 = 200 mm^2, alpha1 = 12e-6/K and E2 = 69 GPa, A2 = 300 mm^2, alpha2 = 23e-6/K. The applied total force is 10,000 N and heating is 50 K.

Edit [cases/baseline.json](cases/baseline.json), or copy it to a new JSON file.
See [units and signs](../../docs/units-and-signs.md) and
[material-property conventions](../../docs/materials.md).

## Equations

Equilibrium and compatibility must both hold:

$$
N_1+N_2=P,
\qquad \delta_1=\delta_2=\delta,
\qquad \varepsilon=\frac{\delta}{L}.
$$

Each rod's force depends on how far its shared strain is from its own free
thermal strain:

$$
N_i=E_iA_i(\varepsilon-\alpha_i\Delta T).
$$

Substitution into equilibrium gives the common strain directly:

$$
\varepsilon=\frac{P+\Delta T(E_1A_1\alpha_1+E_2A_2\alpha_2)}{E_1A_1+E_2A_2}.
$$

Elastic strain energy and equivalent mechanical stiffness are:

$$
U=\sum_{i=1}^{2}\frac{N_i^2L}{2E_iA_i},
\qquad k_{\mathrm{eq}}=\frac{E_1A_1+E_2A_2}{L}.
$$

With zero temperature change, Castigliano's relation recovers displacement:

$$
U=\frac{P^2}{2k_{\mathrm{eq}}},
\qquad \delta=\frac{\partial U}{\partial P}=\frac{P}{k_{\mathrm{eq}}}.
$$

When thermal strain is present, differentiating stored elastic energy alone does
not recover the free thermal part of total displacement. Use the compatibility
equation above; do not apply the last zero-temperature formula blindly.

## Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| N1, N2, P | Rod forces and applied total force; tension positive | N |
| Ei, Ai, alpha i | Each rod’s modulus, area, expansion coefficient | Pa; m^2; 1/K |
| L, delta, epsilon | Common initial length, extension, total strain | m; m; 1 |
| delta T, U, keq | Temperature change, stored elastic energy, equivalent stiffness | K; J; N/m |

## Run

From the repository root:

```bash
python3 advanced/tier-5/main.py
```

Optional plots (after installing `requirements-plot.txt`):

```bash
python3 advanced/tier-5/main.py --plot
```

The run writes `report.md`, `result.json`, and CSV tables to
`results/tier-5/`. Add `--case path/to/my-case.json` and
`--output results/my-study` to preserve a separate case. Running again into the
same folder replaces files with matching names. PNG plots are produced only
when `--plot` is present; an old PNG is not updated by a CSV-only run.

## Expected behavior

The common extension is 0.476153 mm. Rod 1 carries +14,092.3 N and rod 2 carries -4,092.26 N. One rod is compressed even though the total applied force is tensile. The force sum remains 10,000 N.

## Experiments

Predict before running. Change one input at a time and record the units, result,
and physical reason in the [study template](../../templates/study-note.md).

1. Set the temperature change to zero. Load shares in proportion to EA.
2. Set P to zero but keep unequal expansion coefficients. The rods develop equal-and-opposite self-equilibrated forces.
3. Set equal expansion coefficients and zero applied force. Both rods expand freely with zero internal force.
4. At zero temperature change, numerically differentiate U with respect to P and compare with delta.

## Project connections

Stiffness governs load sharing through redundant supports and mixed-material assemblies. FEA uses compatibility and constitutive laws to resolve the same kind of indeterminacy.
