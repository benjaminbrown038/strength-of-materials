"""Read the adjacent README, change a case JSON, then run this file."""
import math
import sys
from pathlib import Path

# Permit direct execution from either this folder or the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from momlab.common import inputs, linspace, table, result, run_cli, capacity_ratio


def plane_stress(sx, sy, tau):
    """Return in-plane principal stresses, von Mises, and 3D maximum shear."""
    center = (sx + sy) / 2
    radius = math.hypot((sx - sy) / 2, tau)
    principal = sorted([center + radius, center - radius, 0.0], reverse=True)
    vm = math.sqrt(sx * sx - sx * sy + sy * sy + 3 * tau * tau)
    return center + radius, center - radius, vm, (principal[0] - principal[2]) / 2


def solve(case):
    """Resolve a shaft surface stress state and rotate its coordinate axes."""
    c = inputs(case, positive=("diameter_m", "E_Pa", "yield_strength_Pa"),
               finite=("axial_force_N", "bending_moment_Nm", "torque_Nm", "poisson"))
    d, E, nu = c["diameter_m"], c["E_Pa"], c["poisson"]
    if not -1 < nu < 0.5:
        raise ValueError("isotropic elastic poisson must be between -1 and 0.5")
    A, I, J = math.pi * d ** 2 / 4, math.pi * d ** 4 / 64, math.pi * d ** 4 / 32
    axial = c["axial_force_N"] / A
    bending = c["bending_moment_Nm"] * (d / 2) / I
    # Check both bending extremes. Torsional shear has the same magnitude there.
    sx = max((axial + bending, axial - bending), key=abs)
    sy, tau = 0.0, c["torque_Nm"] * (d / 2) / J
    sp, sm, vm, max_shear = plane_stress(sx, sy, tau)
    G = E / (2 * (1 + nu))
    rows = []
    for angle in linspace(0, 180, 181):
        t = math.radians(angle)
        normal = (sx + sy) / 2 + (sx - sy) / 2 * math.cos(2 * t) + tau * math.sin(2 * t)
        shear = -(sx - sy) / 2 * math.sin(2 * t) + tau * math.cos(2 * t)
        rows.append(dict(angle_deg=angle, normal_MPa=normal / 1e6, shear_MPa=shear / 1e6))
    return result("Tier 4: combined loading and stress transformation", {
        "selected_normal_MPa": sx / 1e6, "torsional_shear_MPa": tau / 1e6,
        "in_plane_principal_plus_MPa": sp / 1e6, "in_plane_principal_minus_MPa": sm / 1e6,
        "out_of_plane_principal_MPa": 0, "von_mises_MPa": vm / 1e6,
        "maximum_3D_shear_MPa": max_shear / 1e6,
        "yield_strength_to_demand": capacity_ratio(c["yield_strength_Pa"], vm),
        "axial_strain": (sx - nu * sy) / E,
        "transverse_strain": (sy - nu * sx) / E,
        "out_of_plane_strain": -nu * (sx + sy) / E,
        "engineering_shear_strain": tau / G,
    }, [table("stress_rotation", rows, "angle_deg", ["normal_MPa", "shear_MPa"],
              "Counterclockwise axis rotation (deg)", "Transformed stress (MPa)")],
       ["The reported surface is the bending extreme with the largest absolute axial normal stress.",
        "Plane stress sets the third normal stress to zero, not the third normal strain.",
        "Von Mises is a ductile-yield indicator; it is not a fatigue or brittle-fracture criterion."])


if __name__ == "__main__":
    run_cli(solve, __file__)
