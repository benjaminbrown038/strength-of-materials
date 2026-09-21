"""Read the adjacent README, change a case JSON, then run this file."""
import math
import sys
from pathlib import Path

# Permit direct execution from either this folder or the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from momlab.common import inputs, linspace, table, result, run_cli, capacity_ratio


def solve(case):
    """Compare Euler buckling with uniform compressive yielding for a strut."""
    c = inputs(case, positive=("length_m", "width_m", "height_m", "E_Pa", "yield_strength_Pa", "effective_length_factor"),
               nonnegative=("compression_N",))
    P, L, b, h, E, Sy, K = (c[k] for k in ("compression_N", "length_m", "width_m", "height_m",
                                          "E_Pa", "yield_strength_Pa", "effective_length_factor"))
    A = b * h
    I = min(b * h ** 3 / 12, h * b ** 3 / 12)
    r = math.sqrt(I / A)
    slenderness = K * L / r
    euler_load = math.pi ** 2 * E * I / (K * L) ** 2
    yield_load = A * Sy
    rows = [dict(length_m=length, euler_load_N=math.pi ** 2 * E * I / (K * length) ** 2,
                 uniform_yield_load_N=yield_load) for length in linspace(0.25 * L, 2 * L)]
    screen = "Euler stress below yield; also check proportional limit and imperfections"
    if euler_load >= yield_load:
        screen = "Euler elastic result outside yield screen; use an inelastic column model"
    return result("Tier 6: elastic column buckling", {
        "weak_axis_second_moment_m4": I, "radius_of_gyration_mm": r * 1000,
        "slenderness_KL_over_r": slenderness, "euler_load_N": euler_load,
        "euler_stress_MPa": euler_load / A / 1e6, "uniform_yield_load_N": yield_load,
        "euler_load_to_applied_load": capacity_ratio(euler_load, P),
        "yield_load_to_applied_load": capacity_ratio(yield_load, P), "applicability": screen,
    }, [table("column_capacity", rows, "length_m", ["euler_load_N", "uniform_yield_load_N"],
              "Unsupported length (m)", "Idealized load (N)")],
       ["Compression is entered as a nonnegative magnitude; bending uses the weaker section axis.",
        "The baseline Euler curve assumes a straight, centered, elastic column with ideal supports.",
        "The yield line is a comparison, not a combined inelastic column design curve."])


if __name__ == "__main__":
    run_cli(solve, __file__)
