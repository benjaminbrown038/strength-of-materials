"""Read the adjacent README, change a case JSON, then run this file."""
import math
import sys
from pathlib import Path

# Permit direct execution from either this folder or the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from momlab.common import inputs, linspace, table, result, run_cli, capacity_ratio


def solve(case):
    """Compare shaft torsion with average pin shear and plate bearing."""
    c = inputs(case, positive=("length_m", "outer_diameter_m", "G_Pa", "pin_diameter_m",
                               "loaded_plate_thickness_m", "shear_planes"),
               nonnegative=("inner_diameter_m", "pin_force_N"), finite=("torque_Nm",))
    T, L, D, d, G = (c[k] for k in ("torque_Nm", "length_m", "outer_diameter_m", "inner_diameter_m", "G_Pa"))
    if d >= D:
        raise ValueError("inner diameter must be smaller than outer diameter")
    planes = c["shear_planes"]
    if planes not in (1, 2):
        raise ValueError("shear_planes must be 1 or 2")
    J = math.pi * (D ** 4 - d ** 4) / 32
    tau = T * (D / 2) / J
    twist = T * L / (G * J)
    pin_area = math.pi * c["pin_diameter_m"] ** 2 / 4
    pin_tau = c["pin_force_N"] / (planes * pin_area)
    bearing = c["pin_force_N"] / (c["pin_diameter_m"] * c["loaded_plate_thickness_m"])
    rows = [dict(radius_mm=r * 1000, torsional_shear_MPa=T * r / J / 1e6)
            for r in linspace(d / 2, D / 2)]
    return result("Tier 2: circular-shaft torsion and direct shear", {
        "polar_moment_m4": J, "surface_shear_MPa": tau / 1e6,
        "twist_rad": twist, "twist_deg": math.degrees(twist),
        "surface_shear_strain": tau / G,
        "pin_average_shear_MPa": pin_tau / 1e6, "plate_bearing_MPa": bearing / 1e6,
    }, [table("torsional_shear", rows, "radius_mm", ["torsional_shear_MPa"],
              "Radius in shaft material (mm)", "Shear stress (MPa)")],
       ["Torsion formulas apply to circular annular or solid shafts, not arbitrary open sections.",
        "The pin example is a separate load case; its average shear is not the shaft's torsional shear.",
        "Bearing uses the full force on the central loaded plate; in symmetric double shear each outer plate carries half."])


if __name__ == "__main__":
    run_cli(solve, __file__)
