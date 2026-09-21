# Tier 3 — Beam bending, transverse shear, and deflection

[Previous tier](../../advanced/tier-2/README.md) · [Next tier](../../advanced/tier-4/README.md)

## Learning goal

Predict support stress and flexibility, and see why section height matters so much.

## Model and assumptions

A rectangular cantilever is clamped at x = 0 and carries a downward tip force at x = L. Use a prismatic Euler-Bernoulli beam with small deflection and linear elasticity. Width b is horizontal; height h is vertical. The section coordinate y is positive downward. Actual clamp, fillet, holes, and contact are omitted.

## Inputs

The 200 N load, 150 mm span, 30 mm width, 12 mm height, and 69 GPa modulus match the simple support comparison in the design project.

Edit [cases/baseline.json](cases/baseline.json), or copy it to a new JSON file.
See [units and signs](../../docs/units-and-signs.md) and
[material-property conventions](../../docs/materials.md).

## Equations

The area and centroidal second moment are:

$$
A=bh,
\qquad I=\frac{bh^3}{12},
\qquad c=\frac{h}{2}.
$$

Moment magnitude decreases from PL at the clamp to zero at the tip. With y
positive downward, the bending normal stress is:

$$
M_{\mathrm{mag}}(x)=P(L-x),
\qquad \sigma_x(x,y)=-\frac{M_{\mathrm{mag}}(x)y}{I}.
$$

The standard beam shear relation and its rectangular specialization are:

$$
\tau=\frac{VQ}{It},
\qquad \tau(y)=\frac{3P}{2A}\left[1-\left(\frac{2y}{h}\right)^2\right],
\qquad \tau_{\max}=\frac{3P}{2A}.
$$

Integrating curvature with zero displacement and slope at the clamp gives
downward displacement v:

$$
v(x)=\frac{Px^2(3L-x)}{6EI},
\qquad v(L)=\frac{PL^3}{3EI},
\qquad v'(L)=\frac{PL^2}{2EI}.
$$

The outer fibers have peak bending stress and zero transverse shear. The neutral
axis has zero bending stress and peak transverse shear. Section formulas describe
nominal beam fields; they do not resolve the clamp's local 3D stress distribution.

## Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| P, L, x | Downward force, span, axial position | N; m; m |
| b, h, y, c | Width, height, section coordinate, outer-fiber distance | m |
| A, I | Area, second moment about horizontal centroidal axis | m^2; m^4 |
| Q, t | First area moment above/below cut, local section width | m^3; m |
| E, v | Young modulus, downward deflection | Pa; m |

## Run

From the repository root:

```bash
python3 advanced/tier-3/main.py
```

Optional plots (after installing `requirements-plot.txt`):

```bash
python3 advanced/tier-3/main.py --plot
```

The run writes `report.md`, `result.json`, and CSV tables to
`results/tier-3/`. Add `--case path/to/my-case.json` and
`--output results/my-study` to preserve a separate case. Running again into the
same folder replaces files with matching names. PNG plots are produced only
when `--plot` is present; an old PNG is not updated by a CSV-only run.

## Expected behavior

Root bending magnitude is 41.6667 MPa; maximum transverse shear is 0.833333 MPa; tip deflection is 0.754831 mm. Span/height is 12.5 and deflection/span is about 0.00503.

## Experiments

Predict before running. Change one input at a time and record the units, result,
and physical reason in the [study template](../../templates/study-note.md).

1. Double height: bending stress falls by four, tip deflection by eight, and shear stress by two.
2. Double width: stress and deflection both halve.
3. Double length at fixed force and section: bending stress doubles, deflection increases eightfold.
4. Rotate the rectangular section by swapping width and height; explain the changed stiffness.

## Project connections

Use this as your first hand-calculation versus FEA comparison for equipment supports and bracket arms. The model establishes nominal behavior before adding fillets and fastener holes.
