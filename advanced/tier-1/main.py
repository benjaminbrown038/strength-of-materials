"""Read the adjacent README, change a case JSON, then run this file."""
import math
import sys
from pathlib import Path

# Permit direct execution from either this folder or the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from momlab.common import inputs, linspace, table, result, run_cli, capacity_ratio


def solve(case):
    """Stretch a round tie rod and add unrestrained thermal expansion."""
    c = inputs(case, positive=("length_m", "diameter_m", "E_Pa"),
               finite=("force_N", "poisson", "alpha_per_K", "temperature_change_K"))
    P, L, d, E = c["force_N"], c["length_m"], c["diameter_m"], c["E_Pa"]
    nu, alpha, dT = c["poisson"], c["alpha_per_K"], c["temperature_change_K"]
    if not -1 < nu < 0.5:
        raise ValueError("isotropic elastic poisson must be between -1 and 0.5")
    A = math.pi * d ** 2 / 4
    sigma = P / A
    mechanical_strain = sigma / E
    thermal_strain = alpha * dT
    axial_strain = mechanical_strain + thermal_strain
    lateral_strain = -nu * mechanical_strain + thermal_strain
    rows = [dict(x_m=x, mechanical_mm=1000 * mechanical_strain * x,
                 thermal_mm=1000 * thermal_strain * x, total_mm=1000 * axial_strain * x)
            for x in linspace(0, L)]
    return result("Tier 1: axial stress, strain, and temperature", {
        "area_mm2": A * 1e6, "stress_MPa": sigma / 1e6,
        "mechanical_strain": mechanical_strain, "thermal_strain": thermal_strain,
        "total_axial_strain": axial_strain,
        "mechanical_extension_mm": mechanical_strain * L * 1000,
        "thermal_extension_mm": thermal_strain * L * 1000,
        "total_extension_mm": axial_strain * L * 1000,
        "diameter_change_um": lateral_strain * d * 1e6,
        "axial_stiffness_N_per_m": E * A / L,
    }, [table("axial_displacement", rows, "x_m", ["mechanical_mm", "thermal_mm", "total_mm"],
              "Position x (m)", "Axial displacement (mm)")],
       ["Left end fixed; right end can move under prescribed axial force.",
        "Uniform heating alone creates extension but no axial stress in this model.",
        "Negative force gives compressive stress; buckling is evaluated separately in Tier 6."])


if __name__ == "__main__":
    run_cli(solve, __file__)
