"""
Tests for functions in class SolveDiffusion2D
"""

import unittest
import numpy as np
from diffusion2d import SolveDiffusion2D


class TestDiffusion2D(unittest.TestCase):
    def setUp(self):
        self.solver = SolveDiffusion2D()

    def test_initialize_domain(self):
        # Manually pick domain parameters
        w = 12.0
        h = 10.0
        dx = 0.2
        dy = 0.1

        # Expected nx, ny
        nx_expected = int(w / dx)  # 12 / 0.2 = 60
        ny_expected = int(h / dy)  # 10 / 0.1 = 100

        # Call the function
        self.solver.initialize_domain(w=w, h=h, dx=dx, dy=dy)

        # Check using unittest's self.assertEqual
        self.assertEqual(
            self.solver.nx,
            nx_expected,
            f"nx should be {nx_expected} but got {self.solver.nx}",
        )
        self.assertEqual(
            self.solver.ny,
            ny_expected,
            f"ny should be {ny_expected} but got {self.solver.ny}",
        )

    def test_initialize_physical_parameters(self):
        # We must define dx, dy first
        self.solver.dx = 0.1
        self.solver.dy = 0.1

        d = 5.0
        T_cold = 300.0
        T_hot = 600.0

        # Manually compute dt
        # dx^2=0.01, dy^2=0.01 => sum=0.02
        # => numerator=1e-4
        # => denominator=2*5.0*0.02=0.2
        # => dt=1e-4/0.2=5.e-4=0.0005
        dt_expected = 0.0005

        # Call the function
        self.solver.initialize_physical_parameters(d=d, T_cold=T_cold, T_hot=T_hot)

        # Check
        self.assertEqual(self.solver.D, d, f"D should be {d} but got {self.solver.D}")
        self.assertEqual(
            self.solver.T_cold,
            T_cold,
            f"T_cold should be {T_cold} but got {self.solver.T_cold}",
        )
        self.assertEqual(
            self.solver.T_hot,
            T_hot,
            f"T_hot should be {T_hot} but got {self.solver.T_hot}",
        )
        self.assertTrue(
            np.isclose(self.solver.dt, dt_expected, rtol=1e-12),
            f"dt should be {dt_expected}, got {self.solver.dt}",
        )

    def test_set_initial_condition(self):
        self.solver.nx = 100
        self.solver.ny = 200
        self.solver.dx = 0.1
        self.solver.dy = 0.1
        self.solver.T_cold = 300.0
        self.solver.T_hot = 700.0

        # Call the function
        u = self.solver.set_initial_condition()

        # Check shape
        self.assertEqual(
            u.shape, (100, 200), f"Expected array shape (100, 200), got {u.shape}"
        )

        # The center is index [50, 50]
        self.assertTrue(
            np.isclose(u[50, 50], self.solver.T_hot),
            "Center of hot disc should be T_hot.",
        )

        # Outside circle at [0, 0]
        self.assertTrue(
            np.isclose(u[0, 0], self.solver.T_cold),
            "Point (0,0) should remain at T_cold.",
        )
        self.assertEqual(1, 2)


if __name__ == "__main__":
    unittest.main()
