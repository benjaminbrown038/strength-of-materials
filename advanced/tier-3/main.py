"""Read the adjacent README, change a case JSON, then run this file."""
import math
import sys
from pathlib import Path

# Permit direct execution from either this folder or the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from momlab.common import inputs, linspace, table, result, run_cli, capacity_ratio


def solve(case):
    """Calculate the stress and deflection of a cantilever equipment support."""
    c = inputs(case, positive=("length_m", "width_m", "height_m", "E_Pa"),
               nonnegative=("tip_force_N",))
    P, L, b, h, E = (c[k] for k in ("tip_force_N", "length_m", "width_m", "height_m", "E_Pa"))
    A, I = b * h, b * h ** 3 / 12
    # Downward deflection and root moment magnitude are positive for this lesson.
    delta = P * L ** 3 / (3 * E * I)
    rows = [dict(x_m=x, deflection_mm=1000 * P * x ** 2 * (3 * L - x) / (6 * E * I),
                 moment_magnitude_Nm=P * (L - x)) for x in linspace(0, L)]
    section = [dict(y_mm=y * 1000, bending_MPa=-P * L * y / I / 1e6,
                    transverse_shear_MPa=1.5 * P / A * (1 - (2 * y / h) ** 2) / 1e6)
               for y in linspace(-h / 2, h / 2)]
    return result("Tier 3: beam bending, transverse shear, and deflection", {
        "second_moment_m4": I, "root_moment_magnitude_Nm": P * L,
        "max_bending_stress_MPa": P * L * h / (2 * I) / 1e6,
        "max_transverse_shear_MPa": 1.5 * P / A / 1e6,
        "tip_deflection_mm": delta * 1000, "tip_slope_rad": P * L ** 2 / (2 * E * I),
        "span_to_height": L / h, "deflection_to_span": delta / L,
    }, [table("beam_deflection", rows, "x_m", ["deflection_mm"], "Position x (m)", "Downward deflection (mm)"),
        table("section_stress", section, "y_mm", ["bending_MPa", "transverse_shear_MPa"],
              "Section coordinate y, positive downward (mm)", "Stress (MPa)")],
       ["y is positive downward; the top surface is in tension and the bottom in compression.",
        "Bending and transverse-shear maxima occur at different section locations; do not combine both maxima at one point.",
        "Euler-Bernoulli theory neglects shear deflection, clamp details, root fillets, and large rotations."])


if __name__ == "__main__":
    run_cli(solve, __file__)
