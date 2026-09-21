# Units and sign conventions

All JSON inputs use SI: meters, newtons, pascals, kelvin differences, and radians
where angles are used internally. Output names include display units.

| Quantity | Conversion to SI |
|---|---|
| Length | 1 mm = 0.001 m; 1 in = 0.0254 m |
| Area | 1 mm$^2$ = $10^{-6}$ m$^2$ |
| Second moment of area | 1 mm$^4$ = $10^{-12}$ m$^4$ |
| Stress/modulus | 1 MPa = $10^6$ Pa; 1 GPa = $10^9$ Pa |
| Force | 1 lbf = 4.4482216152605 N |
| Torque | 1 N mm = 0.001 N m |
| Temperature change | 1 degree Celsius change = 1 K change |

Dimensional checks catch many bugs:

$$
[\sigma]=\frac{\mathrm{N}}{\mathrm{m}^2},
\qquad [I]=[J]=\mathrm{m}^4,
\qquad \left[\frac{PL}{EA}\right]=\mathrm{m}.
$$

| Case | Sign convention |
|---|---|
| Axial rods / FEA | Positive axial force is tension; positive displacement increases x |
| Simply supported beam | P is downward magnitude; reactions upward; positive M is sagging; V = dM/dx away from jumps |
| Cantilever | P and downward deflection are positive magnitudes; y is positive downward; root moment is reported as magnitude |
| Torsion | Torque sign sets twist and shear sign about the chosen shaft axis |
| Plane stress | Tensile normal stress is positive; positive shear acts +y on the +x face; rotation is counterclockwise |
| Buckling | Applied compression is a positive magnitude |
| Fatigue/fracture | Baseline cycles are tensile with $0\leq\sigma_{\min}<\sigma_{\max}$ |

Use internal resultants at a cut before calculating stress. $P/A$ is an average
normal stress, $V/A$ an average shear stress, $My/I$ a bending normal stress, and
$Tr/J$ a circular-shaft torsional shear stress. A point load or perfectly sharp
constraint in a continuum FEA model can create a local singularity that these
nominal formulas do not represent.

Engineering shear strain is twice tensor shear strain:

$$
\gamma_{xy}=2\varepsilon_{xy},
\qquad \tau_{xy}=G\gamma_{xy}.
$$

For a homogeneous rectangle with width b and vertical height h, bending about
the centroidal horizontal axis uses $I=bh^3/12$. Rotate the section by 90 degrees
and the roles of b and h exchange. Neither I nor polar area moment J is a mass
moment of inertia.
