# Python code to solve the diffusion equation in 2D

Please follow the instructions in [python_testing_exercise.md](https://github.com/Simulation-Software-Engineering/Lecture-Material/blob/main/05_testing_and_ci/python_testing_exercise.md).

## Test logs (for submission)

### pytest log

```text
(venv) yonatan@Yonatans-MacBook-Pro testing-python-exercise-wt2425 % python -m pytest tests/unit/test_diffusion2d_functions.py
============================================================================================================= test session starts ==============================================================================================================
platform darwin -- Python 3.11.5, pytest-8.3.4, pluggy-1.5.0
rootdir: /Users/yonatan/Documents/SSE/testing-python-exercise-wt2425
collected 3 items

tests/unit/test_diffusion2d_functions.py FFF                                                                                                                                                                                             [100%]

=================================================================================================================== FAILURES ===================================================================================================================
____________________________________________________________________________________________________________ test_initialize_domain ____________________________________________________________________________________________________________

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

>       assert solver.nx == nx, f"nx should be {nx} but got {solver.nx}"
E       AssertionError: nx should be 60 but got 50
E       assert 50 == 60
E        +  where 50 = <diffusion2d.SolveDiffusion2D object at 0x103401750>.nx

tests/unit/test_diffusion2d_functions.py:25: AssertionError
_____________________________________________________________________________________________________ test_initialize_physical_parameters ______________________________________________________________________________________________________

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
>       assert solver.D == d, f"D should be {d} but got {solver.D}"
E       AssertionError: D should be 5.0 but got 15.0
E       assert 15.0 == 5.0
E        +  where 15.0 = <diffusion2d.SolveDiffusion2D object at 0x117640950>.D

tests/unit/test_diffusion2d_functions.py:55: AssertionError
------------------------------------------------------------------------------------------------------------- Captured stdout call -------------------------------------------------------------------------------------------------------------
dt = 0.00016666666666666672
__________________________________________________________________________________________________________ test_set_initial_condition __________________________________________________________________________________________________________

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
>       assert np.isclose(u[i_center, j_center], solver.T_hot), \
            "Center of hot disc should have temperature T_hot."
E       AssertionError: Center of hot disc should have temperature T_hot.
E       assert np.False_
E        +  where np.False_ = <function isclose at 0x1021d5cb0>(np.float64(300.0), 700.0)
E        +    where <function isclose at 0x1021d5cb0> = np.isclose
E        +    and   700.0 = <diffusion2d.SolveDiffusion2D object at 0x1178b6f10>.T_hot

tests/unit/test_diffusion2d_functions.py:87: AssertionError
=========================================================================================================== short test summary info ============================================================================================================
FAILED tests/unit/test_diffusion2d_functions.py::test_initialize_domain - AssertionError: nx should be 60 but got 50
FAILED tests/unit/test_diffusion2d_functions.py::test_initialize_physical_parameters - AssertionError: D should be 5.0 but got 15.0
FAILED tests/unit/test_diffusion2d_functions.py::test_set_initial_condition - AssertionError: Center of hot disc should have temperature T_hot.
============================================================================================================== 3 failed in 0.46s ===============================================================================================================
```

```text
(venv) yonatan@Yonatans-MacBook-Pro testing-python-exercise-wt2425 % python -m pytest tests/integration/test_diffusion2d.py

============================================================================================================= test session starts ==============================================================================================================
platform darwin -- Python 3.11.5, pytest-8.3.4, pluggy-1.5.0
rootdir: /Users/yonatan/Documents/SSE/testing-python-exercise-wt2425
collected 2 items

tests/integration/test_diffusion2d.py FF                                                                                                                                                                                                 [100%]

=================================================================================================================== FAILURES ===================================================================================================================
_____________________________________________________________________________________________________ test_initialize_physical_parameters ______________________________________________________________________________________________________

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

>       assert np.isclose(solver.dt, dt_expected, rtol=1e-12), \
            f"dt expected {dt_expected}, got {solver.dt}"
E       AssertionError: dt expected 0.0008, got 0.0005333333333333335
E       assert np.False_
E        +  where np.False_ = <function isclose at 0x105f655f0>(0.0005333333333333335, 0.0008, rtol=1e-12)
E        +    where <function isclose at 0x105f655f0> = np.isclose
E        +    and   0.0005333333333333335 = <diffusion2d.SolveDiffusion2D object at 0x10728d490>.dt

tests/integration/test_diffusion2d.py:34: AssertionError
------------------------------------------------------------------------------------------------------------- Captured stdout call -------------------------------------------------------------------------------------------------------------
dt = 0.0005333333333333335
__________________________________________________________________________________________________________ test_set_initial_condition __________________________________________________________________________________________________________

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
        nx = solver.nx   # 20
        ny = solver.ny   # 20
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
                distance_sq = (xcoord - cx)**2 + (ycoord - cy)**2
                if distance_sq < r**2:
                    u_expected[i, j] = solver.T_hot

        # Get the actual result from the solver
        u_computed = solver.set_initial_condition()

        # Compare the entire array
        assert u_computed.shape == u_expected.shape, (
            f"Shape mismatch: expected {u_expected.shape}, got {u_computed.shape}"
        )

        # Use np.allclose for a floating-point safe comparison of all elements
>       assert np.allclose(u_computed, u_expected), (
            "Computed 2D array does not match expected 2D array for set_initial_condition"
        )
E       AssertionError: Computed 2D array does not match expected 2D array for set_initial_condition
E       assert False
E        +  where False = <function allclose at 0x105f65470>(array([[400., 400., 400., 400., 400., 400., 400., 400., 400., 400., 400.,\n        400., 400., 400., 400., 400., 400., ..., 400., 400., 400., 400., 400., 400., 400., 400., 400.,\n        400., 400., 400., 400., 400., 400., 400., 400., 400.]]), array([[200., 200., 200., 200., 200., 200., 200., 200., 200., 200., 200.,\n        200., 200., 200., 200., 200., 200., ..., 200., 200., 200., 200., 200., 200., 200., 200., 200.,\n        200., 200., 200., 200., 200., 200., 200., 200., 200.]]))
E        +    where <function allclose at 0x105f65470> = np.allclose

tests/integration/test_diffusion2d.py:87: AssertionError
------------------------------------------------------------------------------------------------------------- Captured stdout call -------------------------------------------------------------------------------------------------------------
dt = 0.010416666666666666
=========================================================================================================== short test summary info ============================================================================================================
FAILED tests/integration/test_diffusion2d.py::test_initialize_physical_parameters - AssertionError: dt expected 0.0008, got 0.0005333333333333335
FAILED tests/integration/test_diffusion2d.py::test_set_initial_condition - AssertionError: Computed 2D array does not match expected 2D array for set_initial_condition
============================================================================================================== 2 failed in 0.43s ===============================================================================================================


```

### unittest log

```text
(venv) yonatan@Yonatans-MacBook-Pro testing-python-exercise-wt2425 %  python -m unittest tests/unit/test_diffusion2d_functions.py
Fdt = 0.00016666666666666672
FF
======================================================================
FAIL: test_initialize_domain (tests.unit.test_diffusion2d_functions.TestDiffusion2D.test_initialize_domain)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/yonatan/Documents/SSE/testing-python-exercise-wt2425/tests/unit/test_diffusion2d_functions.py", line 30, in test_initialize_domain
    self.assertEqual(
AssertionError: 50 != 60 : nx should be 60 but got 50

======================================================================
FAIL: test_initialize_physical_parameters (tests.unit.test_diffusion2d_functions.TestDiffusion2D.test_initialize_physical_parameters)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/yonatan/Documents/SSE/testing-python-exercise-wt2425/tests/unit/test_diffusion2d_functions.py", line 61, in test_initialize_physical_parameters
    self.assertEqual(self.solver.D, d, f"D should be {d} but got {self.solver.D}")
AssertionError: 15.0 != 5.0 : D should be 5.0 but got 15.0

======================================================================
FAIL: test_set_initial_condition (tests.unit.test_diffusion2d_functions.TestDiffusion2D.test_set_initial_condition)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/yonatan/Documents/SSE/testing-python-exercise-wt2425/tests/unit/test_diffusion2d_functions.py", line 90, in test_set_initial_condition
    self.assertTrue(
AssertionError: np.False_ is not true : Center of hot disc should be T_hot.

----------------------------------------------------------------------
Ran 3 tests in 0.004s

FAILED (failures=3)
```

## Citing

The code used in this exercise is based on [Chapter 7 of the book "Learning Scientific Programming with Python"](https://scipython.com/book/chapter-7-matplotlib/examples/the-two-dimensional-diffusion-equation/).
