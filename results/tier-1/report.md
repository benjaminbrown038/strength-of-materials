# Tier 1: axial stress, strain, and temperature

| Quantity | Value |
|---|---:|
| area_mm2 | 113.097336 |
| stress_MPa | 88.4194128 |
| mechanical_strain | 0.00128144077 |
| thermal_strain | 0.00092 |
| total_axial_strain | 0.00220144077 |
| mechanical_extension_mm | 0.640720383 |
| thermal_extension_mm | 0.46 |
| total_extension_mm | 1.10072038 |
| diameter_change_um | 5.96549457 |
| axial_stiffness_N_per_m | 15607432.3 |

## Interpretation

- Left end fixed; right end can move under prescribed axial force.
- Uniform heating alone creates extension but no axial stress in this model.
- Negative force gives compressive stress; buckling is evaluated separately in Tier 6.

Inputs and full numerical tables are preserved in `result.json`.
