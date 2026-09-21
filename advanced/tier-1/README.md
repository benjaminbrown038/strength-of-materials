# Tier 1 — Axial stress, strain, and thermal expansion

[Previous tier](../../fundamentals/tier-0/README.md) · [Next tier](../../advanced/tier-2/README.md)

## Learning goal

Distinguish force, stress, strain, displacement, and stiffness using a tie rod.

## Model and assumptions

A straight, uniform round rod is fixed at its left end and loaded axially at its movable right end. Temperature is uniform. The material is homogeneous, isotropic, and linear elastic. Ignore grip concentrations and compressive instability.

## Inputs

The baseline uses P = 10,000 N, L = 0.5 m, d = 12 mm, E = 69 GPa, Poisson ratio 0.33, expansion coefficient 23e-6/K, and a 40 K temperature increase. JSON dimensions are meters.

Edit [cases/baseline.json](cases/baseline.json), or copy it to a new JSON file.
See [units and signs](../../docs/units-and-signs.md) and
[material-property conventions](../../docs/materials.md).

## Equations

Average stress comes from equilibrium; strain describes local deformation:

$$
A=\frac{\pi d^2}{4},
\qquad \sigma=\frac{P}{A},
\qquad \varepsilon_{\mathrm{mech}}=\frac{\sigma}{E}.
$$

Elastic and thermal strains add in this small-strain model:

$$
\varepsilon_x=\frac{P}{EA}+\alpha\Delta T,
\qquad u(x)=\varepsilon_x x,
\qquad \delta=u(L)=\frac{PL}{EA}+\alpha\Delta T L.
$$

$$
k=\frac{EA}{L},
\qquad \varepsilon_{\mathrm{lateral}}=-\nu\frac{P}{EA}+\alpha\Delta T,
\qquad \Delta d=d\varepsilon_{\mathrm{lateral}}.
$$

Hooke's law relates stress to **mechanical** strain, not total thermal strain.
As a separate hand exercise, restrain both ends of an initially stress-free rod
and heat it with no prescribed tip force. Zero total axial strain gives:

$$
0=\frac{\sigma}{E}+\alpha\Delta T,
\qquad \sigma=-E\alpha\Delta T.
$$

That fully restrained boundary condition is a different model from the runnable
free-end case. Tier 5 implements a compatibility-driven thermal stress problem.

## Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| P, A | Axial force (tension positive), area | N; m^2 |
| L, d, u, delta | Length, diameter, axial displacement, extension | m |
| E, sigma | Young modulus, axial stress | Pa |
| nu, epsilon | Poisson ratio, strain | 1 |
| alpha, delta T | Expansion coefficient, temperature change | 1/K; K |
| k | Axial stiffness | N/m |

## Run

From the repository root:

```bash
python3 advanced/tier-1/main.py
```

Optional plots (after installing `requirements-plot.txt`):

```bash
python3 advanced/tier-1/main.py --plot
```

The run writes `report.md`, `result.json`, and CSV tables to
`results/tier-1/`. Add `--case path/to/my-case.json` and
`--output results/my-study` to preserve a separate case. Running again into the
same folder replaces files with matching names. PNG plots are produced only
when `--plot` is present; an old PNG is not updated by a CSV-only run.

## Expected behavior

Axial stress is 88.4194 MPa. Mechanical extension is 0.640720 mm, thermal extension is 0.460000 mm, and total extension is 1.100720 mm. The total diameter change is positive because thermal expansion exceeds Poisson contraction.

## Experiments

Predict before running. Change one input at a time and record the units, result,
and physical reason in the [study template](../../templates/study-note.md).

1. Set temperature_change_K to 0. The diameter should contract under tension.
2. Set force_N to 0. Thermal expansion remains, but mechanical stress becomes zero.
3. Double E with the other inputs fixed. Stress stays the same; mechanical extension halves.
4. Double diameter. Mechanical stress and extension fall by a factor of four.

## Project connections

Axial members are the simplest exact benchmarks for FEA. This separates stiffness requirements from strength requirements before sizing a tie rod or spacer.
