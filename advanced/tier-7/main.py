"""Read the adjacent README, change a case JSON, then run this file."""
import math
import sys
from pathlib import Path

# Permit direct execution from either this folder or the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from momlab.common import inputs, linspace, table, result, run_cli, capacity_ratio


def paris_cycles(a0, a1, C, m, Y, stress_range):
    """Exact constant-geometry Paris integral; SI stress intensity is Pa sqrt(m)."""
    coefficient = C * (Y * stress_range * math.sqrt(math.pi)) ** m
    exponent = 1 - m / 2
    if abs(exponent) < 1e-12:
        return math.log(a1 / a0) / coefficient
    return (a1 ** exponent - a0 ** exponent) / (exponent * coefficient)


def solve(case):
    """Separate a notched-part fatigue screen from a pre-existing crack exercise."""
    c = inputs(case, positive=("nominal_max_stress_Pa", "Kt", "fatigue_strength_Pa", "target_cycles",
                               "ultimate_strength_Pa", "yield_strength_Pa", "crack_start_m", "crack_end_m",
                               "geometry_factor", "toughness_Pa_sqrt_m", "paris_C_SI", "paris_m"),
               nonnegative=("nominal_min_stress_Pa", "notch_sensitivity"))
    smax, smin = c["nominal_max_stress_Pa"], c["nominal_min_stress_Pa"]
    if smin >= smax:
        raise ValueError("require 0 <= minimum stress < maximum stress for this tensile-cycle model")
    if c["Kt"] < 1 or c["notch_sensitivity"] > 1:
        raise ValueError("require Kt >= 1 and notch_sensitivity in [0, 1]")
    if c["yield_strength_Pa"] > c["ultimate_strength_Pa"]:
        raise ValueError("yield strength cannot exceed ultimate strength in this teaching model")
    sa, sm = (smax - smin) / 2, (smax + smin) / 2
    Kf = 1 + c["notch_sensitivity"] * (c["Kt"] - 1)
    # Elastic notch assumption: Kt for mean, Kf for fatigue amplitude.
    goodman = Kf * sa / c["fatigue_strength_Pa"] + c["Kt"] * sm / c["ultimate_strength_Pa"]
    peak = c["Kt"] * smax
    a0, a1, Y = c["crack_start_m"], c["crack_end_m"], c["geometry_factor"]
    critical_a = (c["toughness_Pa_sqrt_m"] / (Y * smax)) ** 2 / math.pi
    if not a0 < a1 < critical_a:
        raise ValueError("require 0 < crack_start < crack_end < fracture critical size")
    delta_s = smax - smin
    cycles = paris_cycles(a0, a1, c["paris_C_SI"], c["paris_m"], Y, delta_s)
    rows = [dict(crack_mm=a * 1000,
                 elapsed_cycles=paris_cycles(a0, a, c["paris_C_SI"], c["paris_m"], Y, delta_s),
                 Kmax_MPa_sqrt_m=Y * smax * math.sqrt(math.pi * a) / 1e6)
            for a in linspace(a0, a1)]
    return result("Tier 7: stress concentration, fatigue, and fracture", {
        "nominal_amplitude_MPa": sa / 1e6, "nominal_mean_MPa": sm / 1e6,
        "fatigue_notch_factor_Kf": Kf, "target_cycles_for_fatigue_strength": c["target_cycles"],
        "goodman_utilization": goodman, "goodman_proportional_load_factor": 1 / goodman,
        "elastic_notch_peak_MPa": peak / 1e6,
        "notch_elasticity_screen": "below yield" if peak < c["yield_strength_Pa"] else "at/above yield; elastic notch model invalid",
        "initial_Kmax_MPa_sqrt_m": Y * smax * math.sqrt(math.pi * a0) / 1e6,
        "final_Kmax_MPa_sqrt_m": Y * smax * math.sqrt(math.pi * a1) / 1e6,
        "fracture_critical_crack_mm": critical_a * 1000,
        "paris_cycles_between_sizes": cycles,
    }, [table("crack_growth", rows, "elapsed_cycles", ["crack_mm"], "Elapsed cycles", "Crack size a (mm)")],
       ["Synthetic teaching properties; fatigue strength belongs to the specified target cycles, not an assumed endurance limit.",
        "Notched-part screening and pre-existing-crack propagation are separate exercises; their lives are not added.",
        "The crack uses nominal far-field stress and Y; do not multiply by the notch Kt again.",
        "Paris C uses Pa sqrt(m), not MPa sqrt(m). Constant Y, tensile cycles, and mid-regime growth are assumed; no threshold or closure model is included."])


if __name__ == "__main__":
    run_cli(solve, __file__)
