"""Physics-based checks: benchmarks, invariants, limits, and convergence."""
import json
import math
from pathlib import Path
import runpy
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from momlab.fea import bar, exact_displacement


def load_tier(n):
    folder = ROOT / ("fundamentals" if n == 0 else "advanced") / ("tier-" + str(n))
    return runpy.run_path(str(folder / "main.py")), json.loads((folder / "cases/baseline.json").read_text())


class MechanicsTests(unittest.TestCase):
    def setUp(self):
        self.tiers = [load_tier(n) for n in range(9)]

    def solve(self, n, **overrides):
        module, baseline = self.tiers[n]
        return module["solve"](dict(baseline, **overrides))["metrics"]

    def test_equilibrium_and_support_limits(self):
        for position in (0, 0.2, 0.5, 1):
            m = self.solve(0, load_position_m=position)
            self.assertAlmostEqual(m["force_residual_N"], 0)
            self.assertAlmostEqual(m["moment_residual_Nm"], 0)
        m = self.solve(0, load_position_m=0.5)
        self.assertEqual(m["reaction_A_N"], 500)
        self.assertEqual(m["max_moment_Nm"], 250)

    def test_axial_hand_calculation(self):
        # A=1 m^2, E=100 Pa, P=10 N, L=2 m -> sigma=10 Pa, delta=0.2 m.
        m = self.solve(1, diameter_m=math.sqrt(4 / math.pi), E_Pa=100,
                       force_N=10, length_m=2, temperature_change_K=0)
        self.assertAlmostEqual(m["stress_MPa"] * 1e6, 10)
        self.assertAlmostEqual(m["total_extension_mm"], 200)

    def test_axial_stiffness_does_not_change_force_controlled_stress(self):
        a, b = self.solve(1), self.solve(1, E_Pa=138e9)
        self.assertEqual(a["stress_MPa"], b["stress_MPa"])
        self.assertAlmostEqual(a["mechanical_extension_mm"], 2 * b["mechanical_extension_mm"])

    def test_free_thermal_expansion_has_no_stress(self):
        m = self.solve(1, force_N=0)
        self.assertEqual(m["stress_MPa"], 0)
        self.assertAlmostEqual(m["total_extension_mm"], 0.46)

    def test_torsion_scaling_and_double_shear(self):
        a, b = self.solve(2), self.solve(2, outer_diameter_m=0.05, shear_planes=1)
        self.assertAlmostEqual(a["surface_shear_MPa"] / b["surface_shear_MPa"], 8)
        self.assertAlmostEqual(a["twist_rad"] / b["twist_rad"], 16)
        self.assertAlmostEqual(b["pin_average_shear_MPa"] / a["pin_average_shear_MPa"], 2)
        self.assertEqual(a["plate_bearing_MPa"], b["plate_bearing_MPa"])

    def test_beam_benchmark_and_boundary_conditions(self):
        m = self.solve(3)
        self.assertAlmostEqual(m["max_bending_stress_MPa"], 125 / 3)
        self.assertAlmostEqual(m["tip_deflection_mm"], 0.754830917874396, places=10)
        module, case = self.tiers[3]
        rows = module["solve"](case)["tables"][0]["rows"]
        self.assertEqual(rows[0]["deflection_mm"], 0)
        self.assertEqual(rows[-1]["moment_magnitude_Nm"], 0)

    def test_beam_height_scaling(self):
        a, b = self.solve(3), self.solve(3, height_m=0.024)
        self.assertAlmostEqual(a["max_bending_stress_MPa"] / b["max_bending_stress_MPa"], 4)
        self.assertAlmostEqual(a["tip_deflection_mm"] / b["tip_deflection_mm"], 8)

    def test_plane_stress_known_states_and_third_principal(self):
        stress = self.tiers[4][0]["plane_stress"]
        plus, minus, vm, shear = stress(0, 0, 10)
        self.assertEqual((plus, minus, shear), (10, -10, 10))
        self.assertAlmostEqual(vm, math.sqrt(3) * 10)
        # Equibiaxial tension has zero in-plane shear, but nonzero 3D maximum shear.
        self.assertEqual(stress(10, 10, 0), (10, 10, 10, 5))

    def test_von_mises_is_rotation_invariant(self):
        module, case = self.tiers[4]
        data = module["solve"](case)
        sx = data["metrics"]["selected_normal_MPa"]
        vm = data["metrics"]["von_mises_MPa"]
        for row in data["tables"][0]["rows"][::13]:
            rotated = module["plane_stress"](row["normal_MPa"], sx - row["normal_MPa"], row["shear_MPa"])
            self.assertAlmostEqual(rotated[2], vm, places=10)

    def test_compressive_force_selects_opposite_bending_fiber(self):
        a, b = self.solve(4), self.solve(4, axial_force_N=-4000)
        self.assertAlmostEqual(a["selected_normal_MPa"], -b["selected_normal_MPa"])
        self.assertAlmostEqual(a["von_mises_MPa"], b["von_mises_MPa"])

    def test_compatibility_and_equilibrium(self):
        m = self.solve(5)
        self.assertAlmostEqual(m["rod1_force_N"] + m["rod2_force_N"], 10000)
        # Recover each extension independently from constitutive response.
        delta1 = 0.5 * (m["rod1_stress_MPa"] * 1e6 / 200e9 + 12e-6 * 50)
        delta2 = 0.5 * (m["rod2_stress_MPa"] * 1e6 / 69e9 + 23e-6 * 50)
        self.assertAlmostEqual(delta1, delta2)
        self.assertAlmostEqual(delta1 * 1000, m["common_extension_mm"])

    def test_thermal_self_stress_and_equal_expansion_limit(self):
        m = self.solve(5, force_N=0)
        self.assertAlmostEqual(m["rod1_force_N"], -m["rod2_force_N"])
        self.assertGreater(abs(m["rod1_force_N"]), 0)
        equal = self.solve(5, force_N=0, alpha2_per_K=12e-6)
        self.assertAlmostEqual(equal["rod1_force_N"], 0)
        self.assertAlmostEqual(equal["rod2_force_N"], 0)

    def test_castigliano_at_zero_temperature_change(self):
        step = 1.0
        a = self.solve(5, force_N=10000 - step, temperature_change_K=0)
        b = self.solve(5, force_N=10000 + step, temperature_change_K=0)
        displacement = (b["elastic_strain_energy_J"] - a["elastic_strain_energy_J"]) / (2 * step)
        expected = self.solve(5, temperature_change_K=0)["common_extension_mm"] / 1000
        self.assertAlmostEqual(displacement, expected, places=12)

    def test_buckling_length_and_restraint_scaling(self):
        a, b, c = self.solve(6), self.solve(6, length_m=0.5), self.solve(6, effective_length_factor=2)
        self.assertAlmostEqual(b["euler_load_N"] / a["euler_load_N"], 4)
        self.assertAlmostEqual(a["euler_load_N"] / c["euler_load_N"], 4)
        self.assertEqual(a["uniform_yield_load_N"], b["uniform_yield_load_N"])
        self.assertIn("outside yield", self.solve(6, length_m=0.01)["applicability"])

    def test_paris_known_integrals(self):
        cycles = self.tiers[7][0]["paris_cycles"]
        # Y*stress_range*sqrt(pi)=1 makes the integral directly hand-checkable.
        self.assertAlmostEqual(cycles(1, 4, 1, 2, 1, 1 / math.sqrt(math.pi)), math.log(4))
        self.assertAlmostEqual(cycles(1, 4, 1, 3, 1, 1 / math.sqrt(math.pi)), 1)

    def test_paris_load_scaling_and_coefficient_units(self):
        a = self.solve(7)
        b = self.solve(7, nominal_max_stress_Pa=140e6, nominal_min_stress_Pa=40e6)
        self.assertAlmostEqual(a["paris_cycles_between_sizes"] / b["paris_cycles_between_sizes"], 8)
        cycles = self.tiers[7][0]["paris_cycles"]
        # Consistent conversion of both stress units AND the coefficient preserves cycles.
        si = cycles(0.001, 0.003, 1e-30, 3, 1.12, 50e6)
        mpa = cycles(0.001, 0.003, 1e-12, 3, 1.12, 50)
        self.assertAlmostEqual(si / mpa, 1)

    def test_fea_uniform_bar_patch_test(self):
        for n in (1, 2, 8, 64):
            model = bar(200e9, 1e-4, 2, 0, 1000, n)
            for x, displacement in zip(model["nodes"], model["u"]):
                self.assertAlmostEqual(displacement, 1000 * x / (200e9 * 1e-4), places=13)
            self.assertAlmostEqual(model["reaction"], -1000, places=7)
            for sigma in model["stress"]:
                self.assertAlmostEqual(sigma / 1e6, 10, places=8)

    def test_fea_convergence_energy_and_force_balance(self):
        errors = []
        E, A, L, beta, P = 69e9, 2e-4, 0.5, 1, 10000
        exact = exact_displacement(L, E, A, L, beta, P)
        for n in (2, 4, 8, 16, 32):
            model = bar(E, A, L, beta, P, n)
            errors.append(abs(model["u"][-1] - exact))
            self.assertAlmostEqual(model["reaction"] + P, 0, places=6)
            self.assertAlmostEqual(model["energy"], P * model["u"][-1] / 2, places=10)
        self.assertTrue(all(a > b for a, b in zip(errors, errors[1:])))
        self.assertTrue(3.9 < errors[-2] / errors[-1] < 4.1)

    def test_zero_loads_are_finite_and_serializable(self):
        variants = [(0, dict(load_N=0)), (1, dict(force_N=0, temperature_change_K=0)),
                    (2, dict(torque_Nm=0, pin_force_N=0)), (3, dict(tip_force_N=0)),
                    (4, dict(axial_force_N=0, bending_moment_Nm=0, torque_Nm=0)),
                    (5, dict(force_N=0, temperature_change_K=0)), (6, dict(compression_N=0)),
                    (8, dict(force_N=0))]
        for n, overrides in variants:
            module, case = self.tiers[n]
            json.dumps(module["solve"](dict(case, **overrides)), allow_nan=False)

    def test_invalid_inputs_are_rejected(self):
        variants = [(0, dict(load_position_m=2)), (1, dict(E_Pa=0)), (1, dict(poisson=0.5)),
                    (2, dict(inner_diameter_m=0.03)), (2, dict(shear_planes=1.5)),
                    (3, dict(height_m=-1)), (4, dict(diameter_m=float("nan"))),
                    (5, dict(area1_m2=True)), (6, dict(effective_length_factor=0)),
                    (7, dict(crack_end_m=1)), (7, dict(notch_sensitivity=1.1)),
                    (7, dict(nominal_min_stress_Pa=80e6)), (8, dict(taper_ratio=-1))]
        for n, overrides in variants:
            with self.subTest(tier=n, overrides=overrides):
                with self.assertRaises(ValueError):
                    self.solve(n, **overrides)
        with self.assertRaises(ValueError):
            self.solve(3, misspelled_input=1)


if __name__ == "__main__":
    unittest.main()
