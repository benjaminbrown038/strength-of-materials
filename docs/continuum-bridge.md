# From bars to 2D and 3D elasticity

Tier 8 implements a bar with one displacement component. Your 2D/3D FEA work
uses the same ingredients with more displacement components and a constitutive
matrix. This page is a derivation guide; a 2D/3D solver is not included here.

## Displacement and small strain

$$
\mathbf{u}(x,y)=
\begin{bmatrix}
u_x(x,y)\\
u_y(x,y)
\end{bmatrix},
\qquad \boldsymbol{\varepsilon}=\frac{1}{2}\left(\nabla\mathbf{u}+(\nabla\mathbf{u})^T\right).
$$

In the engineering-strain vector, use gamma xy (twice tensor epsilon xy):

$$
\boldsymbol{\varepsilon}_{\mathrm{eng}}=
\begin{bmatrix}
\partial u_x/\partial x\\
\partial u_y/\partial y\\
\partial u_x/\partial y+\partial u_y/\partial x
\end{bmatrix}.
$$

## Plane-stress constitutive law

For a thin body loaded in its plane with free faces normal to z:

$$
\begin{bmatrix}
\sigma_x\\
\sigma_y\\
\tau_{xy}
\end{bmatrix}
=\frac{E}{1-\nu^2}
\begin{bmatrix}
1 & \nu & 0\\
\nu & 1 & 0\\
0 & 0 & (1-\nu)/2
\end{bmatrix}
\begin{bmatrix}
\varepsilon_x\\
\varepsilon_y\\
\gamma_{xy}
\end{bmatrix}.
$$

Plane stress imposes sigma z = tau xz = tau yz = 0. Plane strain instead imposes
epsilon z = gamma xz = gamma yz = 0, which generally gives nonzero sigma z.
They use different constitutive matrices; choose by physical restraint.

## Equilibrium and boundary conditions

$$
\nabla\cdot\boldsymbol{\sigma}+\mathbf{b}=\mathbf{0},
\qquad \mathbf{u}=\bar{\mathbf{u}}\ \text{on }\Gamma_u,
\qquad \boldsymbol{\sigma}\mathbf{n}=\bar{\mathbf{t}}\ \text{on }\Gamma_t.
$$

Here b is body force per volume (N/m^3), n is an outward unit normal, and
traction t is force per area (Pa). Prescribed displacement and prescribed
traction act on the corresponding boundary components. Enough displacement
constraints must remove rigid-body motion without unintentionally restraining
physical deformation.

## Finite element form

$$
\mathbf{u}_h=\mathbf{N}\mathbf{d}_e,
\qquad \boldsymbol{\varepsilon}_{\mathrm{eng}}=\mathbf{B}\mathbf{d}_e,
\qquad \mathbf{k}_e=\int_{\Omega_e}\mathbf{B}^T\mathbf{D}\mathbf{B}\,dV.
$$

N interpolates nodal displacement, B differentiates the interpolation, and D
maps engineering strain to stress. For a 2D constant-thickness body, dV includes
thickness. Assemble ke and consistent load vectors, constrain the appropriate
degrees of freedom, solve, and recover stress. These are the same steps visible
in `momlab/fea.py`, generalized from one-dimensional area integration.

With isotropic thermal expansion, subtract free thermal strain before applying D:

$$
\boldsymbol{\sigma}_{\mathrm{vec}}
=\mathbf{D}\left(\boldsymbol{\varepsilon}_{\mathrm{eng}}-
\begin{bmatrix}
\alpha\Delta T\\
\alpha\Delta T\\
0
\end{bmatrix}\right)
\quad\text{for plane stress}.
$$

Check reactions, displacement convergence, stress away from singularities, and
whether the boundary conditions reproduce the intended analytical comparison.
