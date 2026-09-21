# Tier 6: elastic column buckling

| Quantity | Value |
|---|---:|
| weak_axis_second_moment_m4 | 3.6e-09 |
| radius_of_gyration_mm | 3.46410162 |
| slenderness_KL_over_r | 288.675135 |
| euler_load_N | 2451.60973 |
| euler_stress_MPa | 8.17203244 |
| uniform_yield_load_N | 82800 |
| euler_load_to_applied_load | 0.817203244 |
| yield_load_to_applied_load | 27.6 |
| applicability | Euler stress below yield; also check proportional limit and imperfections |

## Interpretation

- Compression is entered as a nonnegative magnitude; bending uses the weaker section axis.
- The baseline Euler curve assumes a straight, centered, elastic column with ideal supports.
- The yield line is a comparison, not a combined inelastic column design curve.

Inputs and full numerical tables are preserved in `result.json`.
