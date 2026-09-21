# Verification record

All nine baseline examples ran successfully during preparation. All 23 automated
checks passed. These cover analytical benchmarks, load/geometry scaling,
equilibrium, rotation invariance, compatibility, energy, mesh convergence,
invalid input handling, consistent lesson headings, and equation formatting.

The core calculations were also run with Python's site-package loading disabled,
confirming that the baseline numerical workflow does not need installed packages.
Optional plots were generated separately with Matplotlib.

## Reproduce the checks

From the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 run_all.py
```

For optional PNG plots:

```bash
python3 -m pip install -r requirements-plot.txt
python3 run_all.py --plot
```

## Runtime and scope

Execution was verified with Python 3.12.14; plots used Matplotlib 3.10.8.
Source syntax was checked against Python 3.9 grammar. Python 3.9 is the intended
minimum, but a separate Python 3.9 interpreter was not used for these runs.

These checks establish consistency with the stated teaching models. They do not
validate material datasets or replace experimental validation of a component.
The fully restrained thermal-rod exercise and the 2D/3D continuum bridge are
documented extensions, not additional implemented solvers.
