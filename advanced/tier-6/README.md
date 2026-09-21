# Tier 6 — Column buckling and stability

[Previous tier](../../advanced/tier-5/README.md) · [Next tier](../../advanced/tier-7/README.md)

## Learning goal

See how a member can become unstable far below material yield stress.

## Model and assumptions

A straight rectangular strut carries centered compression. Use Euler elastic buckling about the weaker centroidal axis and an effective-length factor for ideal end restraint. Ignore eccentricity, initial curvature, residual stress, local plate buckling, and inelasticity.

## Inputs

The baseline uses a 1 m long, 25 mm by 12 mm strut with E = 69 GPa, Sy = 276 MPa, K = 1, and 3,000 N applied compression. It deliberately exceeds the ideal Euler load while staying far below the uniform-yield load.

Edit [cases/baseline.json](cases/baseline.json), or copy it to a new JSON file.
See [units and signs](../../docs/units-and-signs.md) and
[material-property conventions](../../docs/materials.md).

## Equations

Choose the weaker bending axis:

$$
A=bh,
\qquad I_{\min}=\min\left(\frac{bh^3}{12},\frac{hb^3}{12}\right),
\qquad r_g=\sqrt{\frac{I_{\min}}{A}}.
$$

Euler load and the associated slenderness ratio are:

$$
\lambda=\frac{KL}{r_g},
\qquad P_{\mathrm{cr}}=\frac{\pi^2EI_{\min}}{(KL)^2},
\qquad \sigma_{\mathrm{cr}}=\frac{\pi^2E}{\lambda^2}.
$$

Compare the ideal instability load with uniform compressive yielding:

$$
P_y=A S_y,
\qquad n_b=\frac{P_{\mathrm{cr}}}{P},
\qquad n_y=\frac{P_y}{P}.
$$

| Ideal end conditions | Effective-length factor K |
|---|---:|
| Pin–pin | 1.0 |
| Fixed–free | 2.0 |
| Fixed–fixed, no lateral translation | 0.5 |
| Fixed–pin, no lateral translation | Approximately 0.699 |

Euler requires elastic behavior up to buckling. Comparing its stress to yield
is only an initial screen; the proportional limit may be lower. The plotted
yield line is not an inelastic buckling formula or a code-based column curve.

## Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| P, Pcr, Py | Applied compression, Euler load, uniform-yield load | N |
| E, Sy | Young modulus, compressive yield reference | Pa |
| K, lambda | Effective-length factor, slenderness | 1 |
| L, rg | Unsupported length, radius of gyration | m |
| Imin, A | Weak-axis second moment, area | m^4; m^2 |

## Run

From the repository root:

```bash
python3 advanced/tier-6/main.py
```

Optional plots (after installing `requirements-plot.txt`):

```bash
python3 advanced/tier-6/main.py --plot
```

The run writes `report.md`, `result.json`, and CSV tables to
`results/tier-6/`. Add `--case path/to/my-case.json` and
`--output results/my-study` to preserve a separate case. Running again into the
same folder replaces files with matching names. PNG plots are produced only
when `--plot` is present; an old PNG is not updated by a CSV-only run.

## Expected behavior

Euler load is 2,451.61 N; uniform-yield load is 82,800 N. The Euler/applied-load ratio is 0.817203, which is below one: the baseline exceeds the ideal stability limit.

## Experiments

Predict before running. Change one input at a time and record the units, result,
and physical reason in the [study template](../../templates/study-note.md).

1. Halve length: Euler load increases fourfold, but uniform-yield load does not change.
2. Change K from 1 to 2. The Euler load falls to one quarter.
3. Make the column short enough that Euler stress exceeds yield; explain why the elastic result becomes inapplicable.

## Project connections

Useful for slender equipment supports and actuator rods. A later FEA comparison can distinguish eigenvalue buckling from an imperfect nonlinear load-deflection analysis.
