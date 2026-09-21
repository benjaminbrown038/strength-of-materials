# Tier 4 — Combined loading and stress transformation

[Previous tier](../../advanced/tier-3/README.md) · [Next tier](../../advanced/tier-5/README.md)

## Learning goal

Combine stresses at the same material point and distinguish components, principal stresses, and von Mises stress.

## Model and assumptions

A solid round shaft section carries axial force N, bending moment M, and torque T. Evaluate both bending extreme surfaces and select the larger absolute axial normal stress. At that surface, x is axial and y is tangent to the circumference. Assume plane stress, isotropic elasticity, and no transverse-force shear or notch effects.

## Inputs

The baseline uses N = 4,000 N, M = 60 N m, T = 50 N m, d = 25 mm, E = 200 GPa, Poisson ratio 0.3, and an illustrative yield strength of 350 MPa.

Edit [cases/baseline.json](cases/baseline.json), or copy it to a new JSON file.
See [units and signs](../../docs/units-and-signs.md) and
[material-property conventions](../../docs/materials.md).

## Equations

Build the local stress state from resultants at the same section:

$$
A=\frac{\pi d^2}{4},
\qquad I=\frac{\pi d^4}{64},
\qquad J=\frac{\pi d^4}{32}.
$$

$$
\sigma_x=\frac{N}{A}\pm\frac{M(d/2)}{I},
\qquad \sigma_y=0,
\qquad \tau_{xy}=\frac{T(d/2)}{J}.
$$

For a counterclockwise rotation of the coordinate axes:

$$
\sigma_{x'}=\frac{\sigma_x+\sigma_y}{2}+\frac{\sigma_x-\sigma_y}{2}\cos(2\theta)+\tau_{xy}\sin(2\theta),
$$

$$
\tau_{x'y'}=-\frac{\sigma_x-\sigma_y}{2}\sin(2\theta)+\tau_{xy}\cos(2\theta).
$$

The in-plane principal stresses and plane-stress von Mises value are:

$$
\sigma_{\pm}=\frac{\sigma_x+\sigma_y}{2}\pm\sqrt{\left(\frac{\sigma_x-\sigma_y}{2}\right)^2+\tau_{xy}^2},
$$

$$
\sigma_{\mathrm{vm}}=\sqrt{\sigma_x^2-\sigma_x\sigma_y+\sigma_y^2+3\tau_{xy}^2},
\qquad n_y=\frac{S_y}{\sigma_{\mathrm{vm}}}.
$$

Include the third principal stress (zero) before finding 3D maximum shear:

$$
\tau_{\max,3D}=\frac{\max(\sigma_+,\sigma_-,0)-\min(\sigma_+,\sigma_-,0)}{2}.
$$

Constitutive response under plane stress:

$$
\varepsilon_x=\frac{\sigma_x-\nu\sigma_y}{E},
\quad \varepsilon_y=\frac{\sigma_y-\nu\sigma_x}{E},
\quad \varepsilon_z=-\frac{\nu(\sigma_x+\sigma_y)}{E},
\quad \gamma_{xy}=\frac{\tau_{xy}}{G}.
$$

The code checks both bending extremes even if the axial force is compressive.
For this shaft, surface shear magnitude is constant around the circumference;
the extreme absolute normal stress therefore also controls surface von Mises.

## Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| N, M, T | Axial force, bending moment, torque | N; N m; N m |
| sigma x, sigma y, tau xy | Local stress components | Pa |
| theta | Counterclockwise rotation of axes | rad |
| sigma +, sigma - | In-plane principal stresses | Pa |
| Sy, ny | Yield strength, strength/demand ratio | Pa; 1 |
| epsilon, gamma | Normal strain, engineering shear strain | 1 |

## Run

From the repository root:

```bash
python3 advanced/tier-4/main.py
```

Optional plots (after installing `requirements-plot.txt`):

```bash
python3 advanced/tier-4/main.py --plot
```

The run writes `report.md`, `result.json`, and CSV tables to
`results/tier-4/`. Add `--case path/to/my-case.json` and
`--output results/my-study` to preserve a separate case. Running again into the
same folder replaces files with matching names. PNG plots are produced only
when `--plot` is present; an old PNG is not updated by a CSV-only run.

## Expected behavior

Selected normal stress is 47.2627 MPa, shear is 16.2975 MPa, and von Mises stress is 55.0507 MPa. In-plane principal values are approximately 52.3375 and -5.07489 MPa. The reported yield ratio is about 6.35777.

## Experiments

Predict before running. Change one input at a time and record the units, result,
and physical reason in the [study template](../../templates/study-note.md).

1. Set N and M to zero. Pure shear gives principal stresses +tau and -tau, and von Mises = sqrt(3)*abs(tau).
2. Set T to zero. Von Mises becomes the absolute uniaxial stress at the selected surface.
3. Change axial force to compression and verify that the other bending extreme controls.
4. Use the rotation CSV to locate an angle with zero transformed shear.

## Project connections

Compare stress components at the same point in your shaft FEA before comparing equivalent stress. See the continuum bridge for the constitutive matrix used in 2D elements.
