# Tier 2 — Circular-shaft torsion, pin shear, and bearing

[Previous tier](../../advanced/tier-1/README.md) · [Next tier](../../advanced/tier-3/README.md)

## Learning goal

Understand shear stress from torque, then compare it with direct shear in a connection.

## Model and assumptions

A solid or hollow circular shaft has constant torque and a fixed torsional reference at one end. A separate pin example assumes equal force sharing across one or two shear planes. Bearing is averaged over the projected area of the loaded central plate. Ignore pin bending, clearance, friction, and preload.

## Inputs

The shaft baseline uses 50 N m torque, 400 mm length, 25 mm outer diameter, zero inner diameter, and G = 26 GPa. The separate connection uses a 1,000 N force, 8 mm pin, two shear planes, and a 4 mm loaded central plate.

Edit [cases/baseline.json](cases/baseline.json), or copy it to a new JSON file.
See [units and signs](../../docs/units-and-signs.md) and
[material-property conventions](../../docs/materials.md).

## Equations

For a circular annulus (set inner diameter d to zero for a solid shaft):

$$
J=\frac{\pi(D^4-d^4)}{32},
\qquad \tau(r)=\frac{Tr}{J},
\qquad \phi=\frac{TL}{GJ}.
$$

$$
\gamma(r)=\frac{\tau(r)}{G},
\qquad \tau_{\max}=\frac{|T|D}{2J}.
$$

For the separate pin and central loaded plate:

$$
A_{\mathrm{pin}}=\frac{\pi d_p^2}{4},
\qquad \tau_{\mathrm{avg}}=\frac{F}{n_s A_{\mathrm{pin}}},
\qquad \sigma_{\mathrm{bearing}}=\frac{F}{t d_p}.
$$

In symmetric double shear, each outer plate carries F/2. Its bearing stress
requires its own thickness and half the force. J is the polar **area** moment;
these torsion equations do not apply to a rectangular shaft by substituting its
polar area moment.

## Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| T, L, phi | Torque, shaft length, twist | N m; m; rad |
| D, d, r | Outer diameter, inner diameter, material radius | m |
| G, J | Shear modulus, polar area moment | Pa; m^4 |
| tau, gamma | Shear stress, engineering shear strain | Pa; 1 |
| F, dp, ns, t | Pin force, pin diameter, shear-plane count, plate thickness | N; m; 1; m |

## Run

From the repository root:

```bash
python3 advanced/tier-2/main.py
```

Optional plots (after installing `requirements-plot.txt`):

```bash
python3 advanced/tier-2/main.py --plot
```

The run writes `report.md`, `result.json`, and CSV tables to
`results/tier-2/`. Add `--case path/to/my-case.json` and
`--output results/my-study` to preserve a separate case. Running again into the
same folder replaces files with matching names. PNG plots are produced only
when `--plot` is present; an old PNG is not updated by a CSV-only run.

## Expected behavior

Shaft surface shear is 16.2975 MPa and twist is 1.14926 degrees. Pin average shear is 9.94718 MPa, while loaded-plate bearing is 31.25 MPa.

## Experiments

Predict before running. Change one input at a time and record the units, result,
and physical reason in the [study template](../../templates/study-note.md).

1. Double solid-shaft diameter: surface shear falls by eight and twist by sixteen.
2. Increase inner diameter at fixed outer diameter. Predict lower torsional stiffness.
3. Change shear_planes from 2 to 1. Pin average shear doubles; central plate bearing is unchanged.

## Project connections

Links to the design repo’s shaft and bolted-mount cases. Keep connection bearing, direct shear, and torsional shear as distinct stress calculations.
