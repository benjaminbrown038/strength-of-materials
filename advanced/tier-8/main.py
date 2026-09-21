"""Read the adjacent README, change a case JSON, then run this file."""
import math
import sys
from pathlib import Path

# Permit direct execution from either this folder or the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from momlab.common import inputs, linspace, table, result, run_cli, capacity_ratio


from momlab.fea import bar, exact_displacement


def solve(case):
    """Assemble a tapered-bar FEA model and measure convergence to an exact solution."""
    c = inputs(case, positive=("length_m", "root_area_m2", "E_Pa"), finite=("force_N", "taper_ratio"))
    P, L, A0, E, beta = (c[k] for k in ("force_N", "length_m", "root_area_m2", "E_Pa", "taper_ratio"))
    if beta <= -1:
        raise ValueError("taper_ratio must be greater than -1 so the area stays positive")
    exact_tip = exact_displacement(L, E, A0, L, beta, P)
    convergence = []
    for n in (1, 2, 4, 8, 16, 32, 64):
        model = bar(E, A0, L, beta, P, n)
        error = abs(model["u"][-1] - exact_tip)
        # Absolute error is meaningful even when the exact displacement is zero.
        convergence.append(dict(elements=n, tip_mm=model["u"][-1] * 1000,
                                exact_tip_mm=exact_tip * 1000, absolute_error_mm=error * 1000,
                                relative_error=error / abs(exact_tip) if exact_tip else 0.0))
    nodes = [dict(x_m=x, fea_mm=u * 1000,
                  exact_mm=exact_displacement(x, E, A0, L, beta, P) * 1000)
             for x, u in zip(model["nodes"], model["u"])]
    n, h = 64, L / 64
    stresses = [dict(midpoint_m=(i + 0.5) * h, fea_MPa=s / 1e6,
                     exact_midpoint_MPa=P / (A0 * (1 + beta * (i + 0.5) * h / L)) / 1e6)
                for i, s in enumerate(model["stress"])]
    return result("Tier 8: analytical mechanics to assembled 1D FEA", {
        "exact_tip_mm": exact_tip * 1000, "fea_tip_64_elements_mm": model["u"][-1] * 1000,
        "relative_tip_error_64_elements": convergence[-1]["relative_error"],
        "support_reaction_N": model["reaction"], "equilibrium_residual_N": model["reaction"] + P,
        "strain_energy_J": model["energy"], "external_work_J": 0.5 * P * model["u"][-1],
        "energy_residual_J": model["energy"] - 0.5 * P * model["u"][-1],
    }, [table("mesh_convergence", convergence, "elements", ["absolute_error_mm"], "Number of elements", "Absolute tip error (mm)",
              log=all(row["absolute_error_mm"] > 0 for row in convergence)),
        table("displacement_comparison", nodes, "x_m", ["fea_mm", "exact_mm"], "Position x (m)", "Displacement (mm)"),
        table("element_stress", stresses, "midpoint_m", ["fea_MPa", "exact_midpoint_MPa"], "Element midpoint (m)", "Axial stress (MPa)")],
       ["Linear elements integrate linear area exactly; displacement is piecewise linear and element strain is constant.",
        "For this tip-loaded bar, midpoint stress happens to be exact even while displacement error remains.",
        "A uniform bar is reproduced exactly (up to rounding); the tapered baseline makes mesh convergence visible."])


if __name__ == "__main__":
    run_cli(solve, __file__)
