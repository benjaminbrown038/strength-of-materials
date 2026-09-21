"""Read the adjacent README, change a case JSON, then run this file."""
import math
import sys
from pathlib import Path

# Permit direct execution from either this folder or the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from momlab.common import inputs, linspace, table, result, run_cli, capacity_ratio


def solve(case):
    """Find reactions and internal forces for a simply supported beam."""
    c = inputs(case, positive=("length_m",), nonnegative=("load_N", "load_position_m"))
    P, L, a = c["load_N"], c["length_m"], c["load_position_m"]
    if a > L:
        raise ValueError("load_position_m must lie on the beam")
    RB = P * a / L
    RA = P - RB
    # Include both sides of the point-load jump; M stays continuous.
    stations = sorted(set(linspace(0, L) + [a]))
    rows = []
    for x in stations:
        if x == a:
            rows.append(dict(x_m=x, shear_N=RA, moment_Nm=RA * x))
        V = RA if x < a else RA - P
        M = RA * x - P * max(0, x - a)
        rows.append(dict(x_m=x, shear_N=V, moment_Nm=M))
    return result("Tier 0: units and equilibrium", {
        "reaction_A_N": RA, "reaction_B_N": RB,
        "force_residual_N": RA + RB - P,
        "moment_residual_Nm": RB * L - P * a,
        "max_moment_Nm": RA * a,
        "length_in": L / 0.0254,
    }, [table("shear", rows, "x_m", ["shear_N"], "Position x (m)", "Shear V (N)"),
        table("moment", rows, "x_m", ["moment_Nm"], "Position x (m)", "Bending moment M (N m)")],
        ["P is a downward magnitude; both reactions are positive upward.",
         "A pin at x=0 and roller at x=L remove rigid-body motion; no horizontal load is applied.",
         "Force and moment equilibrium determine reactions before stress can be calculated."])


if __name__ == "__main__":
    run_cli(solve, __file__)
