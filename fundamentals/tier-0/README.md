# Tier 0 — Units, free-body diagrams, and equilibrium

[Repository overview](../../README.md) · [Next tier](../../advanced/tier-1/README.md)

## Learning goal

Turn an external load into support reactions and internal shear/bending before calculating stress.

## Model and assumptions

A beam spans from a pin at x = 0 to a roller at x = L. A downward point load P acts at x = a. Ignore beam weight. Draw upward reactions RA and RB; the pin horizontal reaction is zero. The pin fixes horizontal and vertical translation; the roller fixes vertical translation and permits axial motion.

## Inputs

The baseline uses a 1 m span, a 1,000 N point load, and a load position of 0.4 m. Move the point load to study the load path.

Edit [cases/baseline.json](cases/baseline.json), or copy it to a new JSON file.
See [units and signs](../../docs/units-and-signs.md) and
[material-property conventions](../../docs/materials.md).

## Equations

Equilibrium of the whole beam determines the reactions:

$$
\sum F_y=0:\quad R_A+R_B-P=0,
\qquad \sum M_A=0:\quad R_B L-Pa=0.
$$

$$
R_B=\frac{Pa}{L},
\qquad R_A=\frac{P(L-a)}{L}.
$$

Cut the beam at x to expose internal resultants. Away from the point load:

$$
V(x)=\begin{cases}
R_A,&0<x<a,\\
R_A-P,&a<x<L,
\end{cases}
\qquad M(x)=R_Ax-P\max(0,x-a).
$$

$$
M_{\max}=\frac{Pa(L-a)}{L},
\qquad \frac{dM}{dx}=V.
$$

Shear jumps by -P at the load while bending moment stays continuous. The CSV
includes both sides of that jump. Values at support locations are interior
limits, not an additional load outside the span.

## Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| P | Downward point-load magnitude | N |
| L, a, x | Span, load position, section position | m |
| RA, RB | Upward support reactions | N |
| V, M | Internal shear and bending moment | N; N m |

## Run

From the repository root:

```bash
python3 fundamentals/tier-0/main.py
```

Optional plots (after installing `requirements-plot.txt`):

```bash
python3 fundamentals/tier-0/main.py --plot
```

The run writes `report.md`, `result.json`, and CSV tables to
`results/tier-0/`. Add `--case path/to/my-case.json` and
`--output results/my-study` to preserve a separate case. Running again into the
same folder replaces files with matching names. PNG plots are produced only
when `--plot` is present; an old PNG is not updated by a CSV-only run.

## Expected behavior

Reactions are 600 N and 400 N; maximum moment is 240 N m. Both equilibrium residuals should be zero to floating-point precision.

## Experiments

Predict before running. Change one input at a time and record the units, result,
and physical reason in the [study template](../../templates/study-note.md).

1. Set a = L/2. Predict equal reactions and a larger maximum moment (250 N m).
2. Double P. Both reactions, shear, and moment double.
3. Place the force at a support. The other reaction and interior bending moment go to zero.

## Project connections

Use equilibrium to obtain loads for an equipment support, shaft bearing, or actuator attachment. In FEA, sum reactions before interpreting contours.
