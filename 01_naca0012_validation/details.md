# NACA 0012 validation: detailed set-up and results

This page complements the [stage README](README.md) with the full set-up and result tables.

Warm-up validation of the CFD chain (geometry, mesh, physics, force coefficients, post-processing) used later for the NACA 65-(12)10 compressor cascade. The case follows the NASA Turbulence Modeling Resource (TMR) "2D NACA 0012 Airfoil Validation" set-up.

**Summary.** With a 400-chord domain and the finest mesh, Cl is within 1.6 % of the TMR SST reference at α = 10° and 15° (at 10° it lies inside the spread of the reference codes). Cd is 3.4–3.5 % below the reference at 0°, and +3.3 to +4.7 % (10°) and +8 to +13 % (15°) above it. Two sensitivity studies explain most of the early discrepancy: enlarging the far-field radius from 50 to 400 chords lowers Cd by about 4 % at 10° and 15°, and grid refinement (3 meshes per angle) lowers it further. After Richardson extrapolation, Cd is +0.3 to +1.7 % (10°) and +1 to +5 % (15°) above the reference. At 15° the fine-mesh GCI is still 8 %, so Cd is not fully mesh-converged there.

## 1. Set-up

| Item | Value |
|---|---|
| Solver | Simcenter STAR-CCM+ 2210 (build 17.06.008), 2D, steady, coupled implicit, 2nd-order convection |
| Fluid | ideal gas, T = 300 K, ρ_ref = 1.1766 kg/m³, μ = 1.0214×10⁻⁵ Pa·s, p_ref = 101 325 Pa |
| Flow | M = 0.15, V = 52.08 m/s, Re = 6×10⁶ (chord = 1 m) |
| Turbulence | k-ω SST (Menter), all-y⁺ wall treatment; freestream Tu = 0.05 %, μt/μ = 0.009 |
| Geometry | NACA 0012, sharp trailing edge at x/c = 1 (classic formula with last coefficient −0.1036, maximum thickness 12.0 %), chord 1 m, 201 points per surface imported as a spline. The TMR grids use the −0.1015 formula scaled to close at c = 1 (maximum thickness 11.894 %). |
| Domain | circle of radius 400 c centred at (0.5, 0), free-stream boundary (a first series used 50 c, see section 3) |
| Mesh | polygonal mesher + prism layer mesher, 35 prism layers, total thickness 0.015 m, first layer 4.5×10⁻⁶ m (3×10⁻⁶ m at 15°), wake refinement 1.5 m long aligned with the flow direction; airfoil and wake cell size 3.5 / 2.5 / 1.8 mm for the coarse / medium / fine meshes |
| Force coefficients | ρ_ref = 1.1766 kg/m³, V_ref = 52.08 m/s, S_ref = 1 m²; lift direction (−sin α, cos α), drag direction (cos α, sin α) |
| Convergence | Cl and Cd averaged over the last 300 iterations; relative standard deviation < 0.01 % in most cases (coarse 15° mesh: 0.07 %) |

Reference values (TMR SST results, CFL3D / FUN3D / NTS): Cd(0°) = 0.00808–0.00809; Cl(10°) = 1.0765–1.0840, Cd(10°) = 0.01236–0.01253; Cl(15°) = 1.5068–1.5110, Cd(15°) = 0.02187–0.02275.

## 2. Results (finest mesh, 400 c)

| α | Cells | Cl | Cd | Cd pressure | Cd friction | y⁺ max |
|---|---|---|---|---|---|---|
| 0° | 266 424 | −2.5×10⁻⁴ | 0.007809 | 0.001388 | 0.006421 | 0.73 |
| 10° | 332 499 | 1.0804 | 0.012941 | 0.007133 | 0.005809 | 1.59 |
| 15° | 369 075 | 1.4875 | 0.024629 | 0.019665 | 0.004964 | 1.31 |

Comparison with the TMR SST reference:

| α | Cl error | Cd error (fine mesh) | Cd error (Richardson-extrapolated) |
|---|---|---|---|
| 0° | \|Cl\| < 3×10⁻⁴ | −3.4 to −3.5 % | – |
| 10° | +0.4 to −0.3 % (inside the reference spread) | +3.3 to +4.7 % | +0.3 to +1.7 % |
| 15° | −1.3 to −1.6 % | +8.3 to +12.6 % | +1.3 to +5.4 % (+0.3 to −3.6 % if p = 2 is imposed, see section 4) |

## 3. Far-field sensitivity

The same meshes were run with a far-field radius of 50 c and 400 c (cell counts differ by less than 3 %, except at 0°).

| α | Mesh | Cd (50 c) | Cd (400 c) | Change | Cl change |
|---|---|---|---|---|---|
| 10° | medium | 0.013942 | 0.013358 | −4.2 % | +0.05 % |
| 10° | fine | 0.013517 | 0.012941 | −4.3 % | +0.3 % |
| 15° | coarse | 0.03214 | 0.03118 | −3.0 % | – |
| 15° | medium | 0.02764 | 0.02653 | −4.0 % | – |
| 15° | fine | 0.02577 | 0.02463 | −4.4 % | +0.3 % |
| 0° | fine | 0.007836 | 0.007809 | −0.35 % | – |

The change comes almost entirely from the pressure part of the drag (−7.1 % at 10°, medium mesh). It is as large as one mesh refinement, and it is similar at 10° and 15°. The grid sensitivity is nearly the same at 50 c and 400 c (10° medium to fine: −3.05 % and −3.1 %), so both effects add up. At 0°, the fine mesh has 14 % fewer cells at 400 c (266 424) than at 50 c (310 910) with identical mesh settings.

## 4. Mesh sensitivity (GCI, 400 c)

Three systematically refined meshes per angle. Refinement ratios are computed from the cell counts (h = N^(-1/2) in 2D), ordered coarse / medium / fine; apparent order and GCI follow Celik et al. (2008) with a safety factor of 1.25 (`scripts/gci.py`).

| α | Cells (coarse / medium / fine) | Cd (coarse / medium / fine) | Apparent order p | Extrapolated Cd | GCI (fine) |
|---|---|---|---|---|---|
| 10° | 112 033 / 194 679 / 332 499 | 0.01428 / 0.01336 / 0.01294 | 2.8 | 0.01257 | 3.6 % |
| 15° | 121 664 / 216 349 / 369 075 | 0.03118 / 0.02653 / 0.02463 | 2.9 | 0.02305 | 8.0 % |

Cl: extrapolated 1.0855 with a GCI of 0.6 % at 10°; extrapolated 1.5105 with a GCI of 1.9 % at 15°. The pressure part of the drag carries most of the uncertainty (GCI of Cd,p: 7.8 % at 10°, 10.8 % at 15°); the friction part is almost converged (1.6 % and 3.6 %).

At 15° the apparent order (2.9) is higher than the formal order of the scheme (2), which makes the extrapolation somewhat optimistic. Imposing p = 2 gives an extrapolated Cd of 0.02194 and a GCI of 13.6 %. The extrapolated Cd at 15° therefore lies between 0.0219 and 0.0231, to be compared with the reference range 0.0219–0.0228.

Wall-resolution check at 15° (50 c, 221k cells): first prism layer 4.5×10⁻⁶ m → 3×10⁻⁶ m (y⁺ max 1.97 → 1.33) changes Cd by +1.5 % and Cl by −0.3 %, so the 15° meshes use 3×10⁻⁶ m.

## 5. Pressure distributions (finest mesh, 400 c)

Figures in `figures/`: `cp_alpha0_R400.png`, `cp_alpha10_R400.png`, `cp_alpha15_R400.png`.

| α | RMSE, all points | RMSE, x/c ≥ 0.02 | Cp,min CFD / experiment | Cp at stagnation |
|---|---|---|---|---|
| 0° | 0.062 (n = 25) | 0.013 (n = 20) | −0.414 / −0.419 | 1.008 |
| 10° | 0.127 (n = 24) | 0.021 (n = 19) | −5.56 / −5.24 | 1.006 |
| 15° | 0.319 (n = 24) | 0.045 (n = 18) | −10.62 / −10.18 | 1.007 |

The stagnation Cp of an isentropic compressible flow at M = 0.15 is 1.0056, which the computed values reproduce within 0.3 %. The RMSE over all points is dominated by the first experimental points (x/c < 0.02), where Cp varies by several units over a few thousandths of a chord and the digitized data are the least reliable; both values are therefore reported.

## 6. Limitations

- The experimental pressures (Gregory & O'Reilly, NASA R&M 3726) were measured at Re = 2.88×10⁶, about half of the computed Reynolds number, and the available data are digitized, suction side only.
- Force references come from other RANS codes (structured grids, far field at about 500 chords), not from experiment. They are not directly comparable to a polygonal-mesh result, and the remaining gap in Cd is not attributed to a single demonstrated cause.
- The far-field radius was raised from 50 to 400 chords, still smaller than the TMR grids (about 500 chords); the remaining far-field effect is not quantified. The mesh uncertainty (GCI) was computed at 400 c only.
- At 15° the trailing-edge separation makes steady RANS the least reliable, and the fine-mesh GCI (8 %, 13.6 % with p = 2) shows that Cd is not fully mesh-converged. A finer mesh would be needed to narrow it.
- The coarse 15° mesh oscillates slightly (0.07 % standard deviation); the mean is used in the GCI.
- At 0° the fine mesh at 400 c has 14 % fewer cells than at 50 c with identical settings; no GCI was computed at this angle.
- The airfoil thickness (12.0 %) differs slightly from the TMR geometry (11.894 %); the effect on Cd was not quantified.
- Only one turbulence model (k-ω SST) and no transition model were used.

## 7. Reproducing the figures

See the [stage README](README.md): `python 01_naca0012_validation/scripts/make_figures.py` (run from the repository root). Cp is computed in Star-CCM+ as `${Pressure}/(0.5*1.1766*52.08*52.08)` (gauge pressure, free-stream gauge pressure = 0). The `.sim` files are not included in the repository.

## References

- NASA Turbulence Modeling Resource, "2D NACA 0012 Airfoil Validation Case", SST results (CFL3D, FUN3D, NTS).
- Gregory, N. and O'Reilly, C. L., "Low-speed aerodynamic characteristics of NACA 0012 aerofoil section, including the effects of upper-surface roughness simulating hoar frost", NASA R&M 3726, 1970.
- Celik, I. B. et al., "Procedure for Estimation and Reporting of Uncertainty Due to Discretization in CFD Applications", J. Fluids Eng. 130(7), 2008.
