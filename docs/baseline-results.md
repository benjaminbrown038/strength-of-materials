# Baseline results

Generated from the included JSON cases. Units are part of each quantity name.
Small equilibrium/energy residuals near zero are floating-point roundoff.
Your last digits may vary slightly by Python/platform.

## Tier 0: units and equilibrium

| Quantity | Value |
|---|---:|
| reaction_A_N | 600 |
| reaction_B_N | 400 |
| force_residual_N | 0 |
| moment_residual_Nm | 0 |
| max_moment_Nm | 240 |
| length_in | 39.3700787 |

## Tier 1: axial stress, strain, and temperature

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

## Tier 2: circular-shaft torsion and direct shear

| Quantity | Value |
|---|---:|
| polar_moment_m4 | 3.83495197e-08 |
| surface_shear_MPa | 16.2974662 |
| twist_rad | 0.0200584199 |
| twist_deg | 1.1492628 |
| surface_shear_strain | 0.000626825622 |
| pin_average_shear_MPa | 9.94718394 |
| plate_bearing_MPa | 31.25 |

## Tier 3: beam bending, transverse shear, and deflection

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

## Tier 4: combined loading and stress transformation

| Quantity | Value |
|---|---:|
| selected_normal_MPa | 47.2626519 |
| torsional_shear_MPa | 16.2974662 |
| in_plane_principal_plus_MPa | 52.3375443 |
| in_plane_principal_minus_MPa | -5.07489236 |
| out_of_plane_principal_MPa | 0 |
| von_mises_MPa | 55.0507082 |
| maximum_3D_shear_MPa | 28.7062183 |
| yield_strength_to_demand | 6.3577747 |
| axial_strain | 0.00023631326 |
| transverse_strain | -7.08939779e-05 |
| out_of_plane_strain | -7.08939779e-05 |
| engineering_shear_strain | 0.00021186706 |

## Tier 5: compatibility, thermal mismatch, and strain energy

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

## Tier 6: elastic column buckling

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

## Tier 7: stress concentration, fatigue, and fracture

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

## Tier 8: analytical mechanics to assembled 1D FEA

| Quantity | Value |
|---|---:|
| exact_tip_mm | 0.251140283 |
| fea_tip_64_elements_mm | 0.251137519 |
| relative_tip_error_64_elements | 1.10063019e-05 |
| support_reaction_N | -10000 |
| equilibrium_residual_N | 3.27418093e-11 |
| strain_energy_J | 1.25568759 |
| external_work_J | 1.25568759 |
| energy_residual_J | -3.77475828e-15 |
