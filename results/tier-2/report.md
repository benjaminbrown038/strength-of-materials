# Tier 2: circular-shaft torsion and direct shear

| Quantity | Value |
|---|---:|
| polar_moment_m4 | 3.83495197e-08 |
| surface_shear_MPa | 16.2974662 |
| twist_rad | 0.0200584199 |
| twist_deg | 1.1492628 |
| surface_shear_strain | 0.000626825622 |
| pin_average_shear_MPa | 9.94718394 |
| plate_bearing_MPa | 31.25 |

## Interpretation

- Torsion formulas apply to circular annular or solid shafts, not arbitrary open sections.
- The pin example is a separate load case; its average shear is not the shaft's torsional shear.
- Bearing uses the full force on the central loaded plate; in symmetric double shear each outer plate carries half.

Inputs and full numerical tables are preserved in `result.json`.
