# Connecting the three learning projects

Mechanics of materials provides the physical model and hand checks. Machine and
aerospace design uses those checks to select components. FEA resolves geometry,
loading, and constraints that are too detailed for a simple formula.

| This repo | Machine/aerospace design link | FEA question to investigate |
|---|---|---|
| Tier 0: equilibrium | Loads at a support or actuator joint | Do reactions balance applied force and moment? |
| Tier 1: axial/thermal | Tie rods, spacers, thermal growth | Are extension and reaction consistent with restraint? |
| Tier 2: torsion/direct shear | Design Tier 2 shaft; Tier 3 bolted mount | Does a shaft's twist match? What changes with hole/contact detail? |
| Tier 3: beams | Design Tier 1 cantilever; Tier 5 lightweight support | Compare tip displacement and nominal section stress away from the clamp |
| Tier 4: combined stress | Design Tier 2 combined-load shaft | Compare stress components before comparing von Mises contours |
| Tier 5: compatibility | Parallel load paths, mixed-material supports | Does stiffness control load sharing and thermal self-stress? |
| Tier 6: buckling | Slender supports and actuator rods | How do restraint, imperfection, and mode shape change the prediction? |
| Tier 7: fatigue/fracture | Repeatedly loaded brackets and shafts | Is the needed quantity nominal stress, a notch stress, or stress intensity? |
| Tier 8: assembled FEA | Verification foundation for all components | Do displacement, equilibrium, and energy converge consistently? |

The Tier 3 baseline matches the existing design repo's 200 N, 150 mm long,
30 mm wide, 12 mm high support. The Tier 2 shaft uses the same 25 mm diameter,
400 mm torsion span, and 50 N m torque. These are convenient manual comparison
cases. This repo does not import or automatically synchronize either project.

## First comparison exercise

1. Run Tier 3 and record root bending stress and tip deflection.
2. Build the same idealized beam in your FEA project using identical units,
   modulus, dimensions, restraint, and resultant load.
3. Refine the mesh at least three times. Compare tip displacement first, then
   section stress away from the load/constraint details.
4. Explain differences from element formulation, shear deformation, load
   application, and clamp idealization before changing the analytical formula.

The new Tier 8 is a deliberately small 1D solver. Your more advanced 2D/3D FEA
work can reuse its verification habits: exact solutions, mesh refinement,
reaction balance, energy checks, and explicit boundary conditions.
