# MS-01 University Valley material/control check

**Disposition: missing co-located material calibration, not a verified ice/no-ice classifier.** Temperature records constrain diffusivity, not conductivity and volumetric heat capacity separately. No independent co-located University Valley k, density and heat-capacity measurements were found in the primary papers checked. Do not relabel imported Linnaeus Terrace properties as University Valley measurements.

## Source ledger and values

| Primary source / exact geography | Value or control | Measurement status / limitation |
|---|---|---|
| [Marinova et al. 2022](https://doi.org/10.1017/S0954102022000025), University Valley weather-station subsurface; Appendix, Fig. 9 | Dry-ground diffusivity 6.9e-7 m²/s (-5 to -25°C), increasing toward 1e-6 at -45°C | Inferred from temperature profiles. Authors explicitly lack independent k, density, Cp. Frost cementation is proposed, not measured. |
| Same UV model | Dry density 1630 kg/m³; Cp 800 J/kg/K; k 0.9–1.3 W/m/K | Density/Cp imported from McKay 1998; k derived, not measured locally. |
| Same UV model, ice-cemented layer | Density 2022; Cp 1200; k 2.5; diffusivity approximately 1e-6 | Assigned from McKay 1998; icy UV data insufficient to improve it. |
| McKay 1998 as explicitly traced in Marinova Appendix | Linnaeus Terrace, elevation 1625 m, NOT University Valley | Returned-sample density/Cp measured in laboratory; k inferred from field diffusivity. |
| [McKay et al. 2019 snow/salt model](https://pmc.ncbi.nlm.nih.gov/articles/PMC7430506/), UV scenarios | Cp 837; density 1630; porosity 0.41; pore-ice occupancy 90%; k endpoints 0.6–2.5 | Model inputs / semi-empirical ice-dependent k, not local paired material tests. Shallow/medium/deep dry-cover scenarios: 8/22/36 cm. |
| [Fisher et al. 2016](https://doi.org/10.1002/2016JF004054), UV valley floor | 17 shallow cores (<1 m), 11 sites: volumetric ice 28–93%, mean 53.4±17.4%, excluding two massive-ice bodies | Physical ice evidence, not a k/Cv calibration. Medium sand, <8% fines. Ice-table variation within polygon is cm to tens of cm. |
| [Lapalme et al. 2017 distribution/origin](https://www.cambridge.org/core/journals/antarctic-science/article/abs/distribution-and-origin-of-ground-ice-in-university-valley-mcmurdo-dry-valleys-antarctica/399F4CEA9C4B2BE4954B8B0DA038C023), UV | 18 sampled sites; ground ice ubiquitous in upper 2 m; distribution differs within polygons and along valley | Does not establish a deep ice-absent matched control. Multiple origins: vapour, refrozen snowmelt, buried glacier ice. |
| [Lapalme et al. 2017 cryostratigraphy](https://pmc.ncbi.nlm.nih.gov/articles/PMC7380095/), UV polygons | Five CT-selected cores P1-C1, P6-C5, P7-C1, P8-C3, P8-C6; sampling removed dry cover first | Icy-core study, not same-soil paired dry/icy k/Cv experiment. P8-C3 is polygon centre in perennially cryotic zone. |

## Bounded identifiability calculation (our calculation, not an observed classifier result)

Using the 2022 assigned material values:
- Dry Cv = 1630 × 800 = **1.304 MJ/m³/K**.
- Icy Cv = 2022 × 1200 = **2.4264 MJ/m³/K**.
- Thermal inertia I = sqrt(k Cv): dry warm **1083**, dry cold **1302**, assigned icy **2463 J/m²/K/s^0.5**. These are conditional model values, not local truth labels.
- At the cold endpoint, dry apparent diffusivity reaches ~1e-6, the same rounded value assigned to icy ground. Exact k/Cv from listed icy parameters is 1.030e-6. Thus phase/amplitude propagation under a prescribed surface-temperature boundary cannot uniquely separate these states even though their assumed inertia differs by ~1.89×.
- A 1-day sinusoidal skin depth sqrt(alpha*86400/pi) is **0.138 m** at 6.9e-7 versus **0.166 m** at 1e-6. At z=0.20 m the amplitude transmission exp(-z/delta) is **0.234 versus 0.299**, and phase delay **5.55 versus 4.61 h**. Cold dry and assigned icy endpoints coincide at the rounded alpha. This is a conditional identifiability counterexample, not an instrument uncertainty assessment.

Important distinction: infrared surface-energy-balance retrieval can involve thermal inertia and fluxes, so the temperature-diffusion degeneracy alone does NOT prove all remote sensing cannot discriminate ice. It proves temperature-profile fitting cannot independently validate the assumed k and Cv or an ice label.

## Missing target record / next minimum evidence

A same-station, same-depth/time, same-mineral/texture pair with measured k and Cv (or measured density and Cp), independently quantified ice fraction, dry/icy sample-state preservation, uncertainty and temperature dependence; plus physical verification that the no-ice control is genuinely ice-absent through the thermal sensing depth. The reported UV dry-over-icy stratigraphy is not that no-ice control. Prefer metadata linking core/polygon coordinates to thermistor intervals, not merely the valley name. No verified station-to-core join was recovered in this short pass.

Checked 2026-11-14. No repository changes, outreach, credentials, or new full report.
