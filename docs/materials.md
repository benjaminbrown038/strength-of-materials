# Material properties and model boundaries

The values in the baseline JSON files are **invented teaching inputs**. The
elastic constants resemble common metals so the magnitudes are familiar, but
they are not a verified alloy/temper dataset or aerospace design allowables.
Keep stiffness, yield strength, fatigue strength, and fracture toughness separate.

| Property | Symbol | SI unit | Controls |
|---|---|---|---|
| Young's modulus | $E$ | Pa | Axial and bending stiffness |
| Shear modulus | $G$ | Pa | Shear and torsional stiffness |
| Poisson ratio | $\nu$ | 1 | Lateral strain coupling |
| Expansion coefficient | $\alpha$ | K$^{-1}$ | Free thermal strain |
| Yield strength | $S_y$ | Pa | Onset of permanent deformation under a chosen yield criterion |
| Ultimate strength | $S_u$ | Pa | Tensile strength reference in the fatigue illustration |
| Fatigue strength at chosen life | $S_f(N_*)$ | Pa | Fully reversed strength at specified cycles and conditions |
| Fracture toughness | $K_c$ | Pa $\sqrt{\mathrm{m}}$ | Crack instability in the assumed geometry and constraint |

For homogeneous isotropic linear elasticity:

$$
G=\frac{E}{2(1+\nu)}.
$$

Material identity, temper, product form, orientation, temperature, surface finish,
size, environment, and statistical basis matter when replacing teaching values.
The Tier 7 coefficients are synthetic and deliberately not labeled as aluminum,
steel, or titanium. Its Paris coefficient is $10^{-30}$ in SI for exponent 3;
the equivalent numerical coefficient with MPa $\sqrt{\mathrm{m}}$ is $10^{-12}$.
Using the same coefficient with both unit systems produces a billion-fold error.

The implemented models assume small strain and elastic response. A reported
stress above yield means the elastic prediction needs a different material model;
it does not describe plastic redistribution. Thermal cases use uniform temperature
and constant properties. Anisotropic composites, plasticity, creep, contact, shell
buckling, and temperature-dependent material curves are future extensions.
