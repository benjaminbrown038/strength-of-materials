# Tier 7: stress concentration, fatigue, and fracture

| Quantity | Value |
|---|---:|
| nominal_amplitude_MPa | 25 |
| nominal_mean_MPa | 45 |
| fatigue_notch_factor_Kf | 1.8 |
| target_cycles_for_fatigue_strength | 1000000 |
| goodman_utilization | 0.501428571 |
| goodman_proportional_load_factor | 1.99430199 |
| elastic_notch_peak_MPa | 140 |
| notch_elasticity_screen | below yield |
| initial_Kmax_MPa_sqrt_m | 4.39431311 |
| final_Kmax_MPa_sqrt_m | 7.61117358 |
| fracture_critical_crack_mm | 46.6080047 |
| paris_cycles_between_sizes | 27335165.2 |

## Interpretation

- Synthetic teaching properties; fatigue strength belongs to the specified target cycles, not an assumed endurance limit.
- Notched-part screening and pre-existing-crack propagation are separate exercises; their lives are not added.
- The crack uses nominal far-field stress and Y; do not multiply by the notch Kt again.
- Paris C uses Pa sqrt(m), not MPa sqrt(m). Constant Y, tensile cycles, and mid-regime growth are assumed; no threshold or closure model is included.

Inputs and full numerical tables are preserved in `result.json`.
