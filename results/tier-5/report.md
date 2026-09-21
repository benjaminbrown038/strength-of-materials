# Tier 5: compatibility, thermal mismatch, and strain energy

| Quantity | Value |
|---|---:|
| common_extension_mm | 0.476153213 |
| rod1_force_N | 14092.257 |
| rod2_force_N | -4092.257 |
| rod1_stress_MPa | 70.461285 |
| rod2_stress_MPa | -13.6408567 |
| equilibrium_residual_N | -1.8189894e-12 |
| elastic_strain_energy_J | 1.4434514 |
| mechanical_only_extension_mm | 0.0823723229 |
| equivalent_stiffness_N_per_m | 121400000 |

## Interpretation

- Both rods have the same initial length and share a rigid end plate guided against rotation.
- Compatibility requires equal extension, not equal stress or equal force.
- Stored energy uses elastic strain; dU/dP alone omits free thermal extension when temperature is nonzero.

Inputs and full numerical tables are preserved in `result.json`.
