# Tier 8 — From analytical mechanics to assembled 1D FEA

[Previous tier](../../advanced/tier-7/README.md) · [Continuum bridge](../../docs/continuum-bridge.md)

## Learning goal

Assemble a stiffness system, apply a boundary condition, recover stress, and measure numerical error.

## Model and assumptions

A bar has linearly varying area A(x) = A0(1 + beta x/L), constant Young modulus, a fixed left end, and a right-end axial force. There is no distributed axial load. Linear two-node elements use the exact integrated area for each element. This is a one-dimensional axial model, not a 3D tapered-solid stress solution.

## Inputs

The baseline uses P = 10,000 N, L = 0.5 m, A0 = 200 mm^2, E = 69 GPa, and beta = 1 (tip area twice root area). Meshes contain 1, 2, 4, 8, 16, 32, and 64 elements.

Edit [cases/baseline.json](cases/baseline.json), or copy it to a new JSON file.
See [units and signs](../../docs/units-and-signs.md) and
[material-property conventions](../../docs/materials.md).

## Equations

Equilibrium, strain-displacement, and constitutive response give:

$$
\frac{d}{dx}\left(EA(x)\frac{du}{dx}\right)=0,
\qquad u(0)=0,
\qquad EA(L)u'(L)=P.
$$

Integrate du/dx = P/(EA) for an exact benchmark:

$$
u(x)=\begin{cases}
\dfrac{PL}{EA_0\beta}\ln\left(1+\dfrac{\beta x}{L}\right),&\beta\ne0,\\
\dfrac{Px}{EA_0},&\beta=0.
\end{cases}
$$

For a two-node element of length h with local coordinate xi in [0, 1]:

$$
u_h=(1-\xi)u_i+\xi u_j,
\qquad \mathbf{B}=\begin{bmatrix}-1/h & 1/h\end{bmatrix}.
$$

Integrate the stiffness matrix; a linear area function makes the midpoint area
exact for this integral:

$$
\mathbf{k}_e=\int_{x_i}^{x_j}\mathbf{B}^{T}EA(x)\mathbf{B}\,dx
=\frac{EA(x_{\mathrm{mid}})}{h}
\begin{bmatrix}
1 & -1\\
-1 & 1
\end{bmatrix}.
$$

Assemble shared-node contributions, impose the fixed degree of freedom, and
solve the reduced system:

$$
\mathbf{K}_{ff}\mathbf{u}_f=\mathbf{f}_f,
\qquad \sigma_e=E\frac{u_j-u_i}{h},
\qquad \sigma_{\mathrm{exact}}(x)=\frac{P}{A(x)}.
$$

Recover reaction and check work under a gradually applied mechanical load:

$$
R_0+P=0,
\qquad U_h=\frac{1}{2}\sum_e\mathbf{u}_e^T\mathbf{k}_e\mathbf{u}_e
=\frac{1}{2}P u_h(L).
$$

$$
e_u=\frac{|u_h(L)-u(L)|}{|u(L)|}.
$$

For zero load, the implementation reports zero relative error and zero absolute
error. A uniform bar is reproduced exactly apart from rounding, so use nonzero
beta when studying convergence. Stress happens to be exact at element midpoints
for this special load case; that does not make the piecewise-constant stress
field exact everywhere.

## Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| P, E, A0, L | Tip force, modulus, root area, length | N; Pa; m^2; m |
| beta, xi | Area taper parameter, local element coordinate | 1 |
| h, u, uh | Element length, exact displacement, approximate displacement | m |
| B, ke, K | Strain-displacement matrix, element/global stiffness | 1/m; N/m; N/m |
| R0, Uh, eu | Support reaction, elastic energy, relative tip error | N; J; 1 |

## Run

From the repository root:

```bash
python3 advanced/tier-8/main.py
```

Optional plots (after installing `requirements-plot.txt`):

```bash
python3 advanced/tier-8/main.py --plot
```

The run writes `report.md`, `result.json`, and CSV tables to
`results/tier-8/`. Add `--case path/to/my-case.json` and
`--output results/my-study` to preserve a separate case. Running again into the
same folder replaces files with matching names. PNG plots are produced only
when `--plot` is present; an old PNG is not updated by a CSV-only run.

## Expected behavior

The exact tip extension is 0.251140 mm. With 64 elements it is 0.251138 mm, with relative error about 1.10063e-5 (0.00110063%). The reaction is -10,000 N; equilibrium and energy residuals are near floating-point zero.

## Experiments

Predict before running. Change one input at a time and record the units, result,
and physical reason in the [study template](../../templates/study-note.md).

1. Set taper_ratio to 0. Even one element reproduces the exact uniform-bar displacement.
2. Keep beta = 1 and compare error after each mesh doubling. It should fall by roughly a factor of four once the mesh is sufficiently fine.
3. Set taper_ratio to -0.5. The tip is now narrower; stress rises toward the tip.
4. Compare midpoint stress with endpoint stress in a coarse element; explain why one can be exact while the other is not.

## Project connections

The assembly, constraints, stress recovery, and verification steps generalize to your 2D/3D FEA project. Read momlab/fea.py to inspect the stiffness assembly and tridiagonal solve.
