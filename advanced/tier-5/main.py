"""Read the adjacent README, change a case JSON, then run this file."""
import math
import sys
from pathlib import Path

# Permit direct execution from either this folder or the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from momlab.common import inputs, linspace, table, result, run_cli, capacity_ratio


def solve(case):
    """Share axial load between two parallel rods with thermal mismatch."""
    c = inputs(case, positive=("length_m", "E1_Pa", "area1_m2", "E2_Pa", "area2_m2"),
               finite=("force_N", "alpha1_per_K", "alpha2_per_K", "temperature_change_K"))
    P, L, dT = c["force_N"], c["length_m"], c["temperature_change_K"]
    EA1, EA2 = c["E1_Pa"] * c["area1_m2"], c["E2_Pa"] * c["area2_m2"]
    a1, a2 = c["alpha1_per_K"], c["alpha2_per_K"]
    def state(temp):
        strain = (P + temp * (EA1 * a1 + EA2 * a2)) / (EA1 + EA2)
        n1 = EA1 * (strain - a1 * temp)
        n2 = EA2 * (strain - a2 * temp)
        return strain, n1, n2
    strain, n1, n2 = state(dT)
    energy = n1 ** 2 * L / (2 * EA1) + n2 ** 2 * L / (2 * EA2)
    rows = []
    for temp in linspace(min(0, dT), max(1, dT)):
        _, f1, f2 = state(temp)
        rows.append(dict(temperature_change_K=temp, rod1_force_N=f1, rod2_force_N=f2))
    # For dT=0, differentiating total strain energy w.r.t. P gives displacement.
    mechanical_extension = P * L / (EA1 + EA2)
    return result("Tier 5: compatibility, thermal mismatch, and strain energy", {
        "common_extension_mm": strain * L * 1000,
        "rod1_force_N": n1, "rod2_force_N": n2,
        "rod1_stress_MPa": n1 / c["area1_m2"] / 1e6,
        "rod2_stress_MPa": n2 / c["area2_m2"] / 1e6,
        "equilibrium_residual_N": n1 + n2 - P,
        "elastic_strain_energy_J": energy,
        "mechanical_only_extension_mm": mechanical_extension * 1000,
        "equivalent_stiffness_N_per_m": (EA1 + EA2) / L,
    }, [table("thermal_load_sharing", rows, "temperature_change_K", ["rod1_force_N", "rod2_force_N"],
              "Temperature change (K)", "Axial rod force, tension positive (N)")],
       ["Both rods have the same initial length and share a rigid end plate guided against rotation.",
        "Compatibility requires equal extension, not equal stress or equal force.",
        "Stored energy uses elastic strain; dU/dP alone omits free thermal extension when temperature is nonzero."])


if __name__ == "__main__":
    run_cli(solve, __file__)
