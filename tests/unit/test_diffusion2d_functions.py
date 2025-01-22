"""
Tests for functions in class SolveDiffusion2D
"""

from diffusion2d import SolveDiffusion2D
import numpy as np

def test_initialize_domain():
    """
    Check function SolveDiffusion2D.initialize_domain
    """
    solver = SolveDiffusion2D()
    # domain parameters
    w = 12.0
    h = 10.0
    dx = 0.2
    dy = 0.1

    # Expected nx, ny
    nx = int(w / dx)  # 12 / 0.2 = 60
    ny = int(h / dy)  # 10 / 0.1 = 100

    solver.initialize_domain(w=w, h=h, dx=dx, dy=dy)

    assert solver.nx == nx, f"nx should be {nx} but got {solver.nx}"
    assert solver.ny == ny, f"ny should be {ny} but got {solver.ny}"



def test_initialize_physical_parameters():
    """
    Checks function SolveDiffusion2D.initialize_domain
    """
    solver = SolveDiffusion2D()

    solver.dx = 0.1
    solver.dy = 0.1

    # Set parameters
    d = 5.0
    T_cold = 300.0
    T_hot = 600.0

    # Expected dt = dx^2 * dy^2 / (2 * d * (dx^2 + dy^2))
    # dx^2 = 0.01, dy^2 = 0.01 => dx^2 + dy^2 = 0.02
    # => numerator= 0.01 * 0.01= 1.e-4
    # => denominator= 2 * 5.0 * 0.02= 0.2
    # => dt_expected= 1.e-4 / 0.2= 5.e-4=0.0005
    dt_expected = 0.0005

    # Call the function
    solver.initialize_physical_parameters(d=d, T_cold=T_cold, T_hot=T_hot)

    # Check
    assert solver.D == d, f"D should be {d} but got {solver.D}"
    assert solver.T_cold == T_cold, f"T_cold should be {T_cold} but got {solver.T_cold}"
    assert solver.T_hot == T_hot, f"T_hot should be {T_hot} but got {solver.T_hot}"
    assert np.isclose(solver.dt, dt_expected, rtol=1e-12), \
        f"dt should be {dt_expected} but got {solver.dt}"



def test_set_initial_condition():
    """
    Checks function SolveDiffusion2D.get_initial_function
    """
    solver = SolveDiffusion2D()

    # Define everything needed by set_initial_condition
    solver.nx = 100
    solver.ny = 200
    solver.dx = 0.1
    solver.dy = 0.1
    solver.T_cold = 300.0
    solver.T_hot = 700.0

    u = solver.set_initial_condition()

    # Check shape
    assert u.shape == (100, 200), \
        f"Expected array shape (100, 200), got {u.shape}"

    # The center is (cx, cy) = (5, 5), radius=2 => i_center= 5/0.1=50, j_center= 5/0.1=50
    # Check the center is T_hot
    i_center = 50
    j_center = 50
    assert np.isclose(u[i_center, j_center], solver.T_hot), \
        "Center of hot disc should have temperature T_hot."

    # (0,0) should be outside the center circle
    assert np.isclose(u[0, 0], solver.T_cold), \
        "Point (0,0) should remain at temperature T_cold."