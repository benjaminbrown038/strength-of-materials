# Tier 3: beam bending, transverse shear, and deflection

| Quantity | Value |
|---|---:|
| second_moment_m4 | 4.32e-09 |
| root_moment_magnitude_Nm | 30 |
| max_bending_stress_MPa | 41.6666667 |
| max_transverse_shear_MPa | 0.833333333 |
| tip_deflection_mm | 0.754830918 |
| tip_slope_rad | 0.00754830918 |
| span_to_height | 12.5 |
| deflection_to_span | 0.00503220612 |

## Interpretation

- y is positive downward; the top surface is in tension and the bottom in compression.
- Bending and transverse-shear maxima occur at different section locations; do not combine both maxima at one point.
- Euler-Bernoulli theory neglects shear deflection, clamp details, root fillets, and large rotations.

Inputs and full numerical tables are preserved in `result.json`.
