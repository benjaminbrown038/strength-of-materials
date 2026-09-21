# Intro to Mechanics of Materials

Build the physical foundations behind machine components, aerospace structures,
and finite element analysis. Start with equilibrium, learn how loads produce
stress and deformation, and finish by verifying a small assembled FEA model.

**All nine tiers contain runnable Python code, editable inputs, equations,
expected behavior, and experiments.** No placeholder modules are required to
complete the path.

## Start here

Python 3.9 or newer. All calculations and tests use the Python standard library.
From the extracted repository folder:

```bash
python3 fundamentals/tier-0/main.py
python3 advanced/tier-1/main.py
python3 run_all.py
python3 -m unittest discover -s tests -v
```

Open `results/tier-0/report.md`. Read its lesson, predict the effect of moving
the load, edit the case JSON, and rerun. You do not need a notebook or a package
installation to start. `python3 main.py` also works from within any tier folder.

## Learning progression

| Tier | Topic | Runnable study | Main question |
|---|---|---|---|
| [0](fundamentals/tier-0/README.md) | Units and equilibrium | Supported beam reactions, shear, and moment | Where does the load go? |
| [1](advanced/tier-1/README.md) | Axial stress, strain, temperature | Round tie rod | How much does it stretch? |
| [2](advanced/tier-2/README.md) | Torsion, direct shear, bearing | Shaft and pin connection | How do twisting and connection loads differ? |
| [3](advanced/tier-3/README.md) | Bending, shear, deflection | Cantilever equipment support | How does geometry control stress and flexibility? |
| [4](advanced/tier-4/README.md) | Combined loading, principal stress, yielding | Shaft surface stress and axis rotation | Which stress measure answers the question? |
| [5](advanced/tier-5/README.md) | Compatibility and energy | Two rods with thermal mismatch | How do redundant members share load? |
| [6](advanced/tier-6/README.md) | Buckling | Slender rectangular strut | Does instability happen before yield? |
| [7](advanced/tier-7/README.md) | Concentrations, fatigue, fracture | Notch screening and crack growth | What changes when loading repeats or a crack exists? |
| [8](advanced/tier-8/README.md) | Analytical-to-numerical bridge | Tapered-bar stiffness assembly and convergence | How do you verify an FEA result? |

Study Tiers 0–4 first for the machine-design fundamentals. Tiers 5–6 add
compatibility and stability. Tier 7 is an introduction to durability; Tier 8
connects the whole workflow to FEA. Tier numbers are local to this repo and do
not correspond one-for-one to tiers in your other projects.

## Optional plots

Use a virtual environment if you want PNG figures:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-plot.txt
python3 run_all.py --plot
```

On Windows, use `.venv\Scripts\activate` to activate the environment.
Plots are written alongside CSV files; no graphical window is required.
See the included [baseline plot gallery](docs/plots.md) for examples.
The [baseline result tables](docs/baseline-results.md) give reference values;
[verification notes](docs/verification.md) describe the checks and runtime used.

## Change a case

```bash
cp advanced/tier-3/cases/baseline.json advanced/tier-3/cases/my-support.json
python3 advanced/tier-3/main.py \
  --case advanced/tier-3/cases/my-support.json \
  --output results/my-support
```

Edit the copied JSON before running it. Inputs are SI and key names include
units. Unknown keys, nonfinite values, and invalid geometric inputs produce a
clear error. Reusing an output folder overwrites matching result files; use a
new folder to preserve a comparison. A non-plot run does not refresh old PNGs.

## Repository map

| Location | Purpose |
|---|---|
| `fundamentals/tier-0/` | Units, statics, and free-body reasoning |
| `advanced/tier-1/` through `tier-8/` | Consistently structured lessons, main.py, and baseline JSON |
| `momlab/common.py` | Input validation, reports, CSV output, optional plotting |
| `momlab/fea.py` | Bar stiffness assembly, boundary condition, solver, stress recovery |
| `tests/` | Analytical benchmarks, scaling, limiting cases, conservation, convergence |
| `docs/` | Units, materials, equations, continuum bridge, project links, references |
| `templates/study-note.md` | Predict–run–explain record for your experiments |
| `results/` | Generated files, ignored by Git |

Read the formulas in each tier's `main.py`: the mechanics remain visible there.
The shared library handles repeated bookkeeping and the small FEA solver.

## How this supports your other projects

This repo teaches the mechanics. The machine/aerospace design repo uses them to
size components and make design decisions. Your FEA repo explores more detailed
geometry and boundary conditions. See [project connections](docs/project-connections.md)
for matched shaft and support cases, and the [continuum bridge](docs/continuum-bridge.md)
for how axial stress and strain generalize to 2D/3D elasticity.

Every lesson uses the same `$$` display-equation format and symbol table.
See [equation style](docs/equation-style.md). Baseline material properties are
illustrative teaching values; these examples are not component qualification
calculations. More detailed material and model limits are in [materials](docs/materials.md).

## Add it to GitHub

This archive contains source files, without Git history or a remote. Create an
empty GitHub repository named `intro-to-mechanics-of-materials`, then run from
this folder (replace `YOUR_USERNAME`):

```bash
git init -b main
git add .
git commit -m "Add progressive mechanics of materials learning examples"
git remote add origin https://github.com/YOUR_USERNAME/intro-to-mechanics-of-materials.git
git push -u origin main
```

If you already initialized this folder with Git, keep its existing history and
remote instead. No open-source license is selected; choose one before inviting
reuse or external contributions.

## Next extensions

Future work, not implemented here: thin-wall pressure vessels, unsymmetric
bending, shear flow, beam energy methods, 2D truss/frame elements, plasticity,
composites, contact, creep, and temperature-dependent properties. Start with the
implemented experiments before adding more tiers.
