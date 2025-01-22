"""
Tests for functionality checks in class SolveDiffusion2D
"""

from diffusion2d import SolveDiffusion2D
import numpy as np


def test_initialize_physical_parameters():
    """
    Checks function SolveDiffusion2D.initialize_domain
    """
    solver = SolveDiffusion2D()
    # domain parameters
    w = 12.0
    h = 6.0
    dx = 0.2
    dy = 0.1

    solver.initialize_domain(w=w, h=h, dx=dx, dy=dy)

    # physical parameters
    d = 5.0
    T_cold = 300.0
    T_hot = 600.0
    solver.initialize_physical_parameters(d=d, T_cold=T_cold, T_hot=T_hot)

    # Manually compute dt
    # dx^2=0.04, dy^2=0.01 => sum=0.05
    # => numerator=0.04*0.01=0.0004
    # => denominator=2 * 5.0 * 0.05= 0.5
    # => dt= 0.0004/0.5= 0.0008
    dt_expected = 0.0008

    assert np.isclose(
        solver.dt, dt_expected, rtol=1e-12
    ), f"dt expected {dt_expected}, got {solver.dt}"


def test_set_initial_condition():
    """
    Checks function SolveDiffusion2D.get_initial_function
    """
    solver = SolveDiffusion2D()

    # domain parameters
    w = 10.0
    h = 10.0
    dx = 0.5
    dy = 0.5
    solver.initialize_domain(w, h, dx, dy)
    # => solver.nx = 20, solver.ny = 20

    # physical parameters
    solver.initialize_physical_parameters(d=4.0, T_cold=200.0, T_hot=400.0)

    # Now we manually compute the expected array
    nx = solver.nx  # 20
    ny = solver.ny  # 20
    r = 2.0
    cx = 5.0
    cy = 5.0

    # Initialize everything to T_cold
    u_expected = np.full((nx, ny), solver.T_cold)

    # For each grid point (i, j), check if it's inside the circle
    #   Circle of radius 2.0, centered at (cx, cy) = (5.0, 5.0)
    #   x-coordinate of index i: x_i = i * dx
    #   y-coordinate of index j: y_j = j * dy
    for i in range(nx):
        for j in range(ny):
            xcoord = i * dx
            ycoord = j * dy
            distance_sq = (xcoord - cx) ** 2 + (ycoord - cy) ** 2
            if distance_sq < r**2:
                u_expected[i, j] = solver.T_hot

    # Get the actual result from the solver
    u_computed = solver.set_initial_condition()

    # Compare the entire array
    assert (
        u_computed.shape == u_expected.shape
    ), f"Shape mismatch: expected {u_expected.shape}, got {u_computed.shape}"

    # Use np.allclose for a floating-point safe comparison of all elements
    assert np.allclose(
        u_computed, u_expected
    ), "Computed 2D array does not match expected 2D array for set_initial_condition"
