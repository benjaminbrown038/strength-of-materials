# Tier 7 — Stress concentration, fatigue, and fracture

[Previous tier](../../advanced/tier-6/README.md) · [Next tier](../../advanced/tier-8/README.md)

## Learning goal

Separate yielding, repeated-load fatigue screening, and growth of an existing crack.

## Model and assumptions

Two independent teaching studies use the same tensile stress cycle: an elastic notched-part fatigue screen, and a pre-existing crack with a constant geometry factor. Material values are synthetic. Fatigue strength is defined at a chosen cycle count; the model does not fit an S-N curve. Paris growth is restricted to an assumed mid-growth regime with no threshold, closure, overload, or environmental model.

## Inputs

The cycle ranges from 20 to 70 MPa. Kt = 2, notch sensitivity q = 0.8, Sf = 140 MPa at one million cycles, Su = 500 MPa, and Sy = 350 MPa. The crack grows from 1 to 3 mm with Y = 1.12, Kc = 30 MPa sqrt(m), Paris exponent 3, and C = 1e-30 in the SI convention below.

Edit [cases/baseline.json](cases/baseline.json), or copy it to a new JSON file.
See [units and signs](../../docs/units-and-signs.md) and
[material-property conventions](../../docs/materials.md).

## Equations

For the notched, initially uncracked part:

$$
\sigma_a=\frac{\sigma_{\max}-\sigma_{\min}}{2},
\qquad \sigma_m=\frac{\sigma_{\max}+\sigma_{\min}}{2},
\qquad K_f=1+q(K_t-1).
$$

This elastic-mean-stress convention uses Kf on alternating stress and Kt on mean
stress. Modified Goodman utilization at the selected target life is:

$$
U_G=\frac{K_f\sigma_a}{S_f(N_*)}+\frac{K_t\sigma_m}{S_u},
\qquad n_G=\frac{1}{U_G},
\qquad \sigma_{\mathrm{peak,elastic}}=K_t\sigma_{\max}.
$$

Here nG is a proportional load multiplier for this criterion, not a predicted
number of cycles. Check the peak elastic stress against yield before trusting
this notch model.

For the separate pre-existing crack under nominal far-field stress:

$$
K_{\max}=Y\sigma_{\max}\sqrt{\pi a},
\qquad \Delta K=Y(\sigma_{\max}-\sigma_{\min})\sqrt{\pi a},
\qquad a_c=\frac{1}{\pi}\left(\frac{K_c}{Y\sigma_{\max}}\right)^2.
$$

The Paris relation gives cycles between two specified crack sizes:

$$
\frac{da}{dN_c}=C(\Delta K)^m,
\qquad \Delta N_c=\int_{a_0}^{a_1}\frac{da}{C[Y\Delta\sigma\sqrt{\pi a}]^m}.
$$

For constant Y and stress range, the integral is evaluated exactly:

$$
\Delta N_c=\frac{1}{C(Y\Delta\sigma\sqrt{\pi})^m}
\begin{cases}
\dfrac{a_1^{1-m/2}-a_0^{1-m/2}}{1-m/2},&m\ne2,\\
\ln(a_1/a_0),&m=2.
\end{cases}
$$

The code uses Pa sqrt(m) for stress intensity; therefore C has units
m/cycle divided by (Pa sqrt(m)) to power m. The crack dimension a must match the
selected geometry convention (for an ideal edge crack, it is depth). The critical
size is a constant-Y extrapolation; geometry and small-scale-yielding limits may
invalidate that extrapolation before reaching it. The run stops at a1 below ac.

## Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| sigma max/min/a/m | Nominal maximum, minimum, alternating, mean stresses | Pa |
| Kt, Kf, q | Elastic concentration factor, fatigue notch factor, notch sensitivity | 1 |
| Sf(N*), Su, Sy | Fatigue strength at target life, ultimate strength, yield strength | Pa |
| a, a0, a1, ac | Crack size, start, end, idealized critical size | m |
| Y, Kc, delta K | Geometry factor, toughness, stress-intensity range | 1; Pa sqrt(m); Pa sqrt(m) |
| C, m, Nc | Paris coefficient, exponent, elapsed load cycles | See above; 1; cycles |

## Run

From the repository root:

```bash
python3 advanced/tier-7/main.py
```

Optional plots (after installing `requirements-plot.txt`):

```bash
python3 advanced/tier-7/main.py --plot
```

The run writes `report.md`, `result.json`, and CSV tables to
`results/tier-7/`. Add `--case path/to/my-case.json` and
`--output results/my-study` to preserve a separate case. Running again into the
same folder replaces files with matching names. PNG plots are produced only
when `--plot` is present; an old PNG is not updated by a CSV-only run.

## Expected behavior

Goodman utilization is 0.501429 and the load multiplier is 1.99430. Peak notch stress is 140 MPa. The synthetic Paris model gives about 27.3352 million cycles from 1 to 3 mm; this is not total part life and is not the one-million-cycle fatigue target.

## Experiments

Predict before running. Change one input at a time and record the units, result,
and physical reason in the [study template](../../templates/study-note.md).

1. Set q to zero and then one to see Kf range from 1 to Kt.
2. Set paris_m to 2 to exercise the logarithmic integral, with a coefficient appropriate to the new exponent.
3. Double C at fixed m: propagation cycles halve.
4. Double both nominal stress limits while remaining below the critical size: for m = 3, propagation cycles fall by eight.

## Project connections

Introduces the different questions behind fatigue-resistant design and damage tolerance. A local stress concentration, a crack stress intensity, and a von Mises contour are different quantities.
