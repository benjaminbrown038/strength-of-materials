# Tier 8: analytical mechanics to assembled 1D FEA

| Quantity | Value |
|---|---:|
| exact_tip_mm | 0.251140283 |
| fea_tip_64_elements_mm | 0.251137519 |
| relative_tip_error_64_elements | 1.10063019e-05 |
| support_reaction_N | -10000 |
| equilibrium_residual_N | 3.27418093e-11 |
| strain_energy_J | 1.25568759 |
| external_work_J | 1.25568759 |
| energy_residual_J | -3.99680289e-15 |

## Interpretation

- Linear elements integrate linear area exactly; displacement is piecewise linear and element strain is constant.
- For this tip-loaded bar, midpoint stress happens to be exact even while displacement error remains.
- A uniform bar is reproduced exactly (up to rounding); the tapered baseline makes mesh convergence visible.

Inputs and full numerical tables are preserved in `result.json`.
