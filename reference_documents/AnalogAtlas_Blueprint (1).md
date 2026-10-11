# AnalogAtlas: Master Implementation Blueprint

*NASA Space Apps 2026: "Identify Earth Locations that Analog the Permanent Moon Base Locations and Mars"*

> **Version.** v2, revised 4 Oct 2026. **Event dates (CHECKED):** hackathon 14–15 Nov 2026; full challenge statements and partner datasets released 28 Oct 2026; judging begins 16 Nov. You have about six weeks of preparation time. Use it (Part 26).
>
> **Verification status.** v1 was written without live searches. For v2, items confirmed against dated official sources on 4 Oct 2026 are tagged **CHECKED**. Anything still tagged **VERIFY** needs a ~10-minute check before you commit. The official challenge page blocks automated fetching, so its text was confirmed only through search snippets: re-read the page by hand, and again after 28 Oct. Sources are listed in the Revision notes at the end.
>
> **Labels used throughout:** **VERIFIED** (stable, well known) · **CHECKED** (confirmed on a dated official source) · **ASSUMPTION** · **HEURISTIC** · **PROXY** · **NEEDS VALIDATION** · **VERIFY** (open check)
>
> **Access classes (used in Part 6, Part 24 and the cost audit):** **A** = free, no account · **B** = free, but needs an account, login or terms acceptance · **C** = paid or billing required (not allowed in this blueprint).

---

## Table of Contents

1. [The challenge](#part-1-the-challenge)
2. [Product definition](#part-2-product-definition)
3. [Scientific definition of "analog"](#part-3-scientific-definition-of-analog)
4. [Mission profiles](#part-4-mission-profiles)
5. [Planetary reference locations](#part-5-planetary-reference-locations)
6. [Dataset research](#part-6-dataset-research)
7. [Data preparation](#part-7-data-preparation)
8. [Earth candidate discovery](#part-8-earth-candidate-discovery)
9. [Similarity engine](#part-9-similarity-engine)
10. [Validation](#part-10-validation)
11. [Novel analog discovery](#part-11-novel-analog-discovery)
12. [Uncertainty and confidence](#part-12-uncertainty-and-confidence)
13. [Machine learning](#part-13-machine-learning)
14. [LLM](#part-14-llm)
15. [GIS / map](#part-15-gis--map)
16. [UI/UX](#part-16-uiux)
17. [Architecture](#part-17-architecture)
18. [Database](#part-18-database)
19. [API](#part-19-api-rest)
20. [Repository](#part-20-repository)
21. [Security](#part-21-security-baseline)
22. [Performance](#part-22-performance)
23. [Offline-resilient demo](#part-23-offline-resilient-demo)
24. [₹0 deployment](#part-24-0-deployment-verify-all-hosting-terms)
25. [MVP definition](#part-25-mvp-definition)
26. [24-hour plan](#part-26-24-hour-plan-survival-cut)
27. [36-hour plan](#part-27-36-hour-plan)
28. [48-hour plan](#part-28-48-hour-plan)
29. [Team of 4](#part-29-team-of-4)
30. [Backlog](#part-30-backlog-condensed-effort-in-hours)
31. [Risks](#part-31-risks)
32. [Do NOT build](#part-32-do-not-build)
33. [Judge review](#part-33-judge-review-honest-pre-validation)
34. [3-minute demo](#part-34-3-minute-demo)
35. [Innovation scorecard](#part-35-innovation-scorecard)
36. [Final architecture decision](#part-36-final-architecture-decision)
37. [Final data flow](#part-37-final-data-flow)
38. [Acceptance criteria](#part-38-acceptance-criteria)
39. [Scientific claims policy](#part-39-scientific-claims-policy)
40. [Executive blueprint](#part-40-executive-blueprint)
41. [Final cost audit](#final-cost-audit)
42. [Final technical sanity check](#final-technical-sanity-check)
43. [Revision notes](#revision-notes)

---

## PART 1: The challenge

**1.1 Objective.** Use open Earth, Moon and Mars data from NASA and other space agencies to *identify and characterize new* terrestrial analogs for future bases or landing sites. The statement names deserts, polar regions, volcanic and arid terrain, caves, and "other environments that share conditions with the lunar or Martian surface."

**1.2 What NASA is asking.** The statement says site selection depends on topography, geology, environment and available resources, and that known analogs (Atacama, Haughton, Death Valley) "are not entirely well characterized." Three things follow:

- **Discover:** find sites beyond the famous ones.
- **Characterize:** quantify why a site is analogous, per dimension.
- **Do it with open data:** the method must be reproducible by anyone.

**1.3 Deliverables.** The challenge text lists none. What the program requires:

- **CHECKED (Space Apps submission guide):** a **Project Demo** is mandatory. You cannot upload video or slides to the Space Apps site, so host them elsewhere and link them. The description should show how NASA and Space Agency partner open data made the project possible. **Submission is final**, so submit with a time buffer.
- **CHECKED (2026 Participant Terms and Conditions):** original content must be freely available or licensed under an OSI-approved open-source licence, and you must **cite every source** used, even open or free ones.
- **ASSUMPTION:** also provide a public GitHub repo, a list of the NASA and partner data used, and an AI-use disclosure (put it in the README and the submission text regardless of whether the form asks).
- **VERIFY:** demo length or format limits and the exact AI-disclosure wording, once the 28 Oct pages are live.

**1.4 Constraints and interpretation.**

*Stated by the challenge:*

- Use open data from NASA and other space agencies.
- Find *new* terrestrial analogs; re-ranking the famous ones is not enough.
- *Characterize* them, not just list them.

*Our interpretation (ASSUMPTION, state it in the pitch):*

- Cover the Moon *and* Mars. The title names both.
- Treat topography, geology, environment and resources as the dimensions to characterize. The statement lists them as factors in site selection, not as scoring requirements.
- "Permanent base" means operational suitability matters, not just resemblance.

**1.5 Hidden opportunities.**

- "Characterize" means each site gets a reproducible **analog datasheet**. Many entries will stop at a map.
- "Caves" invites a small lava-tube/pit module.
- **CHECKED:** NASA states the Moon Base will be established in the lunar south-pole region, so the lunar profiles should be south-pole oriented.
- "Other space agencies" is explicit. **CHECKED:** the 2026 partners include ESA, JAXA, ISRO and CSA. Include at least one non-NASA agency dataset in the data list (Part 6).
- Validation is no longer unique. **Observed 4 Oct 2026:** at least one public repo for this challenge already reports ROC-AUC against known analogs and negative controls. Differentiate on *rigor*: gate-aware baselines, hard negatives, bootstrap intervals, pre-registered config, and per-site stability (Part 10).
- The six-week preparation window is a real advantage for teams that plan data acquisition and science decisions early.

**1.6 What judges likely want.** **CHECKED:** the official Judging & Awards Guide (2024) lists five criteria: Impact, Creativity, Validity, Relevance, Presentation. It says presentation deserves the same attention as the other four. **VERIFY** the 2026 guide, because one 2026 local-event listing words the criteria slightly differently.

| Criterion | How this blueprint answers it |
|---|---|
| Impact | A reproducible, open-data shortlist and method that analog fieldwork teams can rerun |
| Creativity | Scale-matched, profile-weighted similarity with live reweighting and per-site stability |
| Validity | Validation harness with hard negatives and baselines, sensitivity analysis, claims policy |
| Relevance | Directly answers "identify and characterize new analogs": Moon and Mars, datasheet per site |
| Presentation | 3-minute demo narrative (Part 34) with the validation figure up front |

Optimize for all five. Spend the extra effort on *Validity* (rigor is where this design is strongest) and *Presentation* (the guide says teams under-invest in it).

**1.7 Weak solution.**

- A satellite-image → LLM → "looks like Mars" pipeline.
- One global "Mars similarity %".
- A map of the three famous sites.
- A coarse grid (≥ 0.5°, ~55 km) where "slope" is a regional gradient, not a trafficability-scale quantity.
- No validation, or validation that mostly measures a vegetation filter.

**1.8 Exceptional solution.**

- A transparent, scale-matched, multi-feature method.
- Mission-profile weights you can change live.
- Validation against known analogs, with hard negatives, baselines and confidence intervals.
- Honest confidence, including a stated ceiling when a profile leans on proxies.
- A few defensible new candidates, each with a datasheet and a prior-use check.
- An LLM that only narrates computed evidence.

**1.9 Key scientific questions.**

1. What can be compared *directly* across bodies, and what is only a proxy?
2. How do we avoid scale artifacts, especially in slope, roughness and relief (baseline *and* support area)?
3. Do the known analogs score highly under a method that was not tuned to them?
4. Which candidates survive weight perturbation?
5. Does the score do work beyond the barren-ground gate? (Compare against gate-only and single-family baselines.)

---

## PART 2: Product definition

**Names:** **AnalogAtlas** (recommended), TerraTwin, ProvingGround, AnalogScope, Selene-Ares Atlas.

**One-liner:** An open-data atlas that finds, ranks and explains Earth sites resembling lunar and Martian mission targets, with evidence and honest uncertainty, under mission-specific priorities.

**Problem.** Analog sites are chosen by tradition and are poorly quantified. No transparent, reproducible, mission-specific way exists to search the planet for alternatives.

**Solution.** Scale-matched feature extraction for Earth, Moon and Mars, then profile-weighted similarity, a confidence model, and a validation harness. Outputs are ranked sites, datasheets and a grounded explanation.

**Users.** Analog researchers (primary), rover/habitat testers, mission planners, educators and students.

**Differentiators.**

- It is not a map: every ranked site carries quantified, sourced evidence.
- It is not a chatbot: the LLM never produces or edits a score.
- It is not one Earth/Mars number: there is one profile per mission use, plus a separate **operational accessibility** axis.
- It is scale-matched: terrain features share baseline and support area across the three bodies.
- It is validated, with hard negatives, baselines, intervals and sensitivity analysis.
- It is honest about proxies: each is flagged and its share of the score is shown.

**Success test.** A judge can pick any ranked site, see per-feature evidence for both bodies, and trace every number to a dataset and a line of config.

---

## PART 3: Scientific definition of "analog"

**Definition.** An analog is purpose-specific: a site is analogous *for stated dimensions and a stated mission use*, with fidelity varying by dimension. Earth cannot reproduce vacuum, lunar gravity (~0.17 g), Martian gravity (~0.38 g), lunar radiation or the thin Martian CO₂ atmosphere (~0.6 kPa). **Our analogy is therefore limited to terrain, surface, thermal regime, arid/cold environment, geology and logistics.** This limit appears in the app.

**Key design principle (scale matching).** Slope and roughness depend on measurement baseline, and relief and tail statistics depend on the *area* they are computed over. Native DEM resolutions happen to align well:

| Body | Product | Native sampling | Effective-resolution caveat |
|---|---|---|---|
| Earth | GEBCO 15″ (latest release) | ~463 m at equator | **CHECKED:** land elevation is taken from SRTM15+ V2.8, so it is a smoothed, SRTM-derived product |
| Mars | MOLA MEGDR 128 ppd | ~463 m | Gridded between laser tracks, so it is interpolated at low latitudes. **NEEDS VALIDATION** against published MOLA km-scale slope statistics (e.g., Kreslavsky and Head, 1999) |
| Moon | LOLA LDEM_64 | ~474 m | Dense laser coverage; the best-constrained of the three |

Four scale rules apply to every feature:

1. **Same baseline, in metres.** Compute slope from local metric spacing, never from degrees. All terrain features use a **~0.5 km baseline** (native pixel ≈ 0.46–0.47 km; a 3×3 Horn kernel spans ~1 km, identically for all three bodies). The tool must never compare a 20 m lunar slope with a 450 m Earth slope.
2. **Keep the baseline isotropic at high latitude.** East-west pixel spacing shrinks with cos(latitude): about 232 m at 60°, 120 m at 75°, 40 m at 85°. For |lat| > 60°, block-average columns by ⌈1/cos φ⌉ before differencing, or reproject to polar stereographic at 500 m. Lunar polar targets must use polar stereographic crops.
3. **Same support area.** Earth cells are H3 resolution 5 (~253 km²). Planetary reference ROIs are tessellated into cells of the same physical area (Part 5). Relief and P90 grow with area, so unequal areas would bias every comparison.
4. **Same statistic, area-weighted.** Medians, P90 and P5–P95 ranges use the same definitions and cos(latitude) pixel weights on every body.

**Second principle (two comparison modes).**

- **Absolute match** for physically comparable quantities: slope, roughness, relief, albedo.
- **Relative-regime match** for quantities where Earth cannot reach the extreme: temperature level, thermal amplitude, aridity. Here we match the *position within each body's own distribution*, or an ordinal regime. **HEURISTIC.**

**Feature table (★ = scored in the engine; the MVP column is build priority).**

| Feature | Scientific relevance | Earth data | Moon/Mars data | Direct/Proxy | Comparison method | Confidence | MVP |
|---|---|---|---|---|---|---|---|
| ★ T1 Mean slope @0.5 km | Landing, trafficability, base siting | GEBCO (latest) | LOLA LDEM_64 / MOLA 128ppd | Direct (derived) | Absolute, tolerance kernel | High | Must |
| ★ T2 Slope P90 | Steep tail (crater walls) | GEBCO | same | Direct | Absolute | High | Must |
| ★ T3 Roughness = σ(slope), 3×3 | Rover mobility | GEBCO | same | Direct | Absolute | Med-High (Mars: Medium, see interpolation caveat) | Must |
| ★ T4 Local relief = P95 − P5 elevation per cell | Massifs, crater rims; robust to single outlier pixels | GEBCO | same | Direct | Absolute (area-matched) | High | Must |
| ★ S1 Broadband albedo | Surface reflectance, thermal budget. The Moon is dark (Bond albedo ≈ 0.1) and bright deserts are ≈ 0.25–0.4 (**VERIFY**), so expect dark basaltic terrain to be favored for lunar profiles | MODIS MCD43 (CMG 0.05°) | MOLA/TES albedo (Mars); LROC WAC reflectance (Moon) | Proxy (different bands) | Absolute, wide tolerance | Medium | Should |
| ★ E1 Aridity | Dryness, dust, no vegetation | Global Aridity Index v3 | Reference = hyper-arid | Proxy/regime | Ordinal regime | Med | Must |
| ★ E2 Thermal level | Cold-desert character | WorldClim 2.1 mean annual temp | Mars: Mars Climate Database (MCD) value; Moon: Diviner | Proxy | Relative percentile | Low-Med | Must |
| ★ E3 Thermal amplitude | Thermal cycling stress | WorldClim BIO2 (diurnal range) | MCD / Diviner | Proxy | Relative percentile | Low-Med | Should |
| ★ G1 Mafic-volcanic fraction | Basaltic substrate, ISRU testing | GLiM (basic volcanics) | USGS Astrogeology maps (Unified Geologic Map of the Moon; Mars global geologic map) | Proxy | Fraction match | Medium | Should |
| ★ R1 Cold/ground-ice potential | ISRU-relevant ice | Climate-based index (+ permafrost map if time) | Mars GRS hydrogen/ice-rich EZ literature; Moon PSR/LEND literature | **Proxy** | Regime match; profile-specific | Low | Should |
| Barrenness (gate) | Moon/Mars are ~100% bare | MODIS MOD44B Percent_NonVegetated | by definition | Direct (Earth) | **Hard filter**, not scored | High | Must |
| Ice and water mask (gate) | MOD44B counts snow/ice as non-vegetated, so an ice mask is required | Natural Earth glaciated areas; GEBCO elevation ≤ 0 | n/a | Direct | **Hard filter**, not scored | High | Must |
| Operational axis: remoteness, protected area, traversable fraction (<15°) | Logistics, permitting | Natural Earth, WDPA, derived slope | n/a | Heuristic | Separate index | Medium | Should |
| Rock abundance | Hazard | none on Earth | Diviner | n/a | **Reference-only, not compared** | n/a | Cut |
| Hydrated minerals | ISRU | ASTER (coarse) | CRISM/M3 | Proxy | Too heavy | Low | Optional |
| Lava tubes/pits | Habitat shelter | Curated literature list | Wagner & Robinson lunar pits; USGS Mars cave candidate catalog | Direct (inventory) | Overlay, not scored | Med | Advanced |

Every row has the same columns on purpose. Your "analog datasheet" lists, per feature: the Earth value, the target value, the mode used, the proxy flag and the source.

---


## PART 4: Mission profiles

Scoring is a per-feature similarity `s_k ∈ [0,1]`, combined with profile weights `w` (sums to 1). **HEURISTIC expert priors**, to be refined by Person 1, documented, and then frozen before the first validation run (Part 10).

| Feature | A Lunar S-Pole base | B Mars base | C Mars rover test | D Lunar rover/EVA | E General |
|---|---|---|---|---|---|
| T1 slope mean | .12 | .10 | .16 | .16 | .10 |
| T2 slope P90 | .12 | .06 | .12 | .12 | .10 |
| T3 roughness | .10 | .08 | .20 | .22 | .10 |
| T4 relief | .12 | .06 | .08 | .10 | .10 |
| S1 albedo | .06 | .08 | .06 | .10 | .10 |
| E1 aridity | .04 | .18 | .12 | .06 | .10 |
| E2 thermal level | .12 | .12 | .04 | .06 | .10 |
| E3 thermal amplitude | .08 | .10 | .06 | .10 | .10 |
| G1 mafic volcanic | .04 | .10 | .16 | .08 | .10 |
| R1 ice potential | .20 | .12 | 0 | 0 | .10 |

**Feature families** (used for correlation handling in Part 9):

- **Terrain:** T1, T2, T3, T4
- **Surface-climate:** S1, E1, E2, E3
- **Geology-resource:** G1, R1

**Family weight totals at default weights, and the proxy share** (every feature except T1–T4 is a proxy):

| | A | B | C | D | E |
|---|---|---|---|---|---|
| Terrain | .46 | .30 | .56 | .60 | .40 |
| Surface-climate | .30 | .48 | .28 | .32 | .40 |
| Geology-resource | .24 | .22 | .16 | .08 | .20 |
| **Proxy share** | **.54** | **.70** | **.44** | **.40** | **.60** |

**Family cap.** Each family's total weight is capped at **0.5**, with one documented exception: the two rover/EVA profiles (C and D) use **0.6** for Terrain, because mobility testing is terrain-dominated by design. *(v1 stated a 0.5 cap but profiles C and D exceeded it at 0.56 and 0.60.)* The proxy shares above feed the confidence ceiling in Part 12.

**Hard constraints per profile (gates, never scored, never removable by sliders).**

- Bare ground ≥ ~80% (MOD44B Percent_NonVegetated).
- Not urban, not open water, not permanent ice-sheet interior (ice-free polar terrain stays in).
- Profile A also requires a **cold-climate flag**: mean annual temperature ≤ 0 °C. **HEURISTIC**, set by physical reasoning only.

**Weighting methods compared.**

- **Expert-defined:** simple and defensible. **Use as default.**
- **User-defined sliders:** the demo feature.
- **AHP:** principled, but the pairwise matrices are tedious for 10 features. Use "AHP-lite" (pairwise only between the 3 feature *families*) if time allows.
- **Sensitivity analysis:** mandatory (Dirichlet perturbation, Parts 10 and 12).
- **Data-driven:** circular without labels; skip.

**Recommendation:** expert defaults + live sliders + Dirichlet stability. **"Change priorities → rankings change" is worth building**, and it is cheap, because the engine precomputes `s_k` and the browser only recomputes a weighted sum. The browser must replicate the gate, family caps and missing-data renormalization exactly (Part 17 parity test).

**Explanation requirement per profile:** top 3 contributing features, weakest feature, and proxy share.

---

## PART 5: Planetary reference locations

**Status of the lunar targets (CHECKED, 4 Oct 2026).** NASA lists **nine** Artemis candidate landing regions near the south pole: a peak near Cabeus B, Haworth, Malapert Massif, Mons Mouton Plateau, Mons Mouton, Nobile Rim 1, Nobile Rim 2, de Gerlache Rim 2 and Slater Plain. They were narrowed from 13 regions announced in 2022. 2026 reporting says the first landing moved from Artemis III to Artemis IV or later. NASA states the Moon Base will be in the south-pole region and uses a Connecting Ridge region (from the 2022 list, not among the nine) as its representative south-pole site.

**Representation (MVP): area-matched cell vectors.**

1. Tile a ~25 km-radius neighbourhood around the target centre (≈ 1,960 km², about 8 cells) with hexagons of the *same physical area as an Earth H3 resolution-5 cell (≈ 253 km²)*, in a local equal-area projection. Use up to 40 km radius (≈ 20 cells) where terrain allows.
2. Compute every feature per hexagon exactly as for Earth (Part 7).
3. Summarize across hexagons: `μ_k` = median, `σ_k` = IQR / 1.349 (a robust standard deviation), and record `n_cells`.

Why not reuse H3 on the Moon or Mars: H3 is defined on Earth's geometry, so a resolution-5 cell mapped onto the Moon would cover only ~19 km² (Mars ~72 km²). That is a factor of 13 (Moon) smaller than an Earth cell, which would silently break scale matching. The old plan of a "15–25 km-radius ROI aggregated like an Earth cell" had a different area (700–1,960 km²) from an Earth cell, which biases relief and P90.

A single point is too noisy, a raster ROI is too heavy, and a multi-scale approach is the Advanced version. For narrow targets (e.g., the Taurus-Littrow valley), `σ_k` reflects the neighbourhood rather than the site. Document this per target.

**Proposed MVP targets (7 rows; Haworth and Malapert count separately if you want 8). VERIFY every coordinate and the current NASA candidate list.**

| Target | Why useful | Variables | Data | Limits |
|---|---|---|---|---|
| Lunar S-Pole: Shackleton rim / Connecting Ridge | NASA's representative south-pole site; illumination, ice proximity | Slope, relief, thermal (Diviner), PSR | LOLA polar DEMs (polar stereographic, resampled to 500 m), Diviner | Extreme thermal/illumination has no Earth match |
| Lunar S-Pole: Haworth or Malapert Massif | Two of NASA's nine current candidate regions | Same | Same | Same; Malapert is a massif, Haworth a crater, so choose by mission use |
| Lunar: Taurus-Littrow (Apollo 17), ~20.2°N, 30.8°E | Mare basalt valley, an EVA/rover baseline with real ground truth | Terrain, basalt | LOLA, LROC | Equatorial; no ice; narrow valley, so `σ_k` is neighbourhood-dominated |
| Mars: Jezero, ~18.4°N, 77.5°E | Perseverance site; delta, basaltic floor | Terrain, geology | MOLA, THEMIS, CRISM | Crater floor and delta are only a few cells wide; no ice |
| Mars: Gale, ~4.6°S, 137.4°E | Curiosity; mound, layered | Terrain | MOLA | Mound relief is extreme, so floor-versus-mound ROI choice changes the vector; document the choice |
| Mars: Oxia Planum, ~18.2°N, 335.4°E | Rover-friendly, clay-bearing | Terrain, mineralogy | MOLA, CRISM | Clay mineralogy is not matched (no hydrated-mineral feature in the MVP) |
| Mars: Arcadia Planitia (or other ice-rich human-landing candidate) | Subsurface ice for base ISRU (**VERIFY** current exploration-zone literature) | Ice proxy, mid-latitude cold | GRS/SHARAD literature | Ice not measured on Earth side; relies on the R1 proxy |

Selection criterion: each target must stand for a distinct mission use, not for fame. If time allows, add one more of NASA's nine regions (e.g., Nobile Rim 2 or de Gerlache Rim 2) to show the method generalizes.

---

## PART 6: Dataset research

**Dataset decision matrix (sizes approximate; VERIFY).** Cost/access class A/B/C is defined at the top of this document.

| Dataset | Planet | Variable | Resolution | Coverage | Format | Access | Download | Cost | MVP? |
|---|---|---|---|---|---|---|---|---|---|
| GEBCO latest grid (**CHECKED:** GEBCO_2025 released Aug 2025, 43200 × 86400; a 2026 release appears in GEBCO documentation, so pin the exact version and DOI) | Earth | Elevation | 15″ (~463 m) | Global | Global file is NetCDF; GeoTIFF only for user-defined areas via the download app | Direct, no login | GBs (≈ 7.5 GB if unpacked as int16) | Free, incl. commercial use, acknowledge source (A) | **Must** |
| WorldClim 2.1 | Earth | Temp, BIO2, precip | 30″–10′ | Global | GeoTIFF | Direct | Small | Free, academic/non-commercial licence (A) | **Must** |
| Global Aridity Index & PET v3 / v3.1 (**CHECKED:** 30″, 1970–2000 means, AI stored as integers × 10,000; read the Figshare release notes, which mention a bias in some affected outputs) | Earth | Aridity | 30″ | Global | GeoTIFF | Figshare, direct | Small | Free, non-commercial (A; **VERIFY** licence text) | **Must** |
| MODIS MOD44B VCF v061 (**CHECKED:** yearly, 250 m, band Percent_NonVegetated, 2000–2024; LP DAAC data carry no use or redistribution restrictions) | Earth | Bare-ground % | 250 m | Global | HDF tiles | NASA Earthdata (free login) | Medium | Free (B: login) | **Must** (fallback: MOD13C2 NDVI CMG) |
| MODIS MCD43 CMG | Earth | Albedo | 0.05° | Global | HDF | Earthdata | Small | Free (B) | Should |
| Natural Earth glaciated areas, urban areas, populated places | Earth | Ice mask, urban mask, places | vector | Global | shp | Direct | Small | Free (A) | **Must** (masks) |
| GLiM | Earth | Lithology | polygons | Global | Geodatabase/shp | Univ. Hamburg | Medium | Free (A) | Should |
| Natural Earth roads, WDPA | Earth | Roads, protected areas | vector | Global | shp | Direct | Small | Free (A; WDPA terms: do not redistribute raw polygons, ship only derived per-cell fractions; **VERIFY**) | Should |
| Smithsonian GVP, Earth Impact Database | Earth | Volcanoes, craters | points | Global | CSV | Direct | Tiny | Free (A) | Should (tags) |
| MOLA MEGDR 128 ppd | Mars | Elevation | ~463 m | Global | PDS IMG | PDS Geosciences Node | ~2 GB | Free (A) | **Must** |
| LOLA LDEM_64 | Moon | Elevation | ~474 m | Global | PDS IMG | PDS Geosciences Node | ~0.5 GB | Free (A) | **Must** |
| LOLA polar stereographic DEMs | Moon | Elevation | 20–120 m (coarser variants exist) | Poles | GeoTIFF/IMG | PDS | Per-ROI crops | Free (A) | Should (targets only; resample to ~500 m by averaging) |
| LRO Diviner global products | Moon | Temp, rock abundance | ~240 m | Global | PDS | PDS | Medium | Free (A) | Should (reference values) |
| LROC WAC mosaic | Moon | Reflectance | 100 m | Global | tiles | LROC/PDS | Large | Free (A) | Optional (use coarse version) |
| THEMIS / TES | Mars | Thermal inertia, albedo | 100 m–3 km | Global | PDS/USGS | PDS/USGS | Medium | Free (A) | Optional |
| Mars Climate Database | Mars | Temperature | model | Global | Web tool | Free, academic | Tiny (per-target queries) | Free (A; VERIFY terms) | Should |
| USGS Astrogeology geologic maps (Unified Geologic Map of the Moon; Mars global geologic map) | Mars/Moon | Units | vector | Global | GIS | USGS | Small | Free (A) | Should |
| Copernicus GLO-30 (ESA/European Commission) | Earth | 30 m DEM | 30 m | Global | COG | AWS open data | Large | Free (A) | Optional (Stage 2 context; also a non-NASA agency dataset for the submission) |
| JAXA AW3D30 or SELENE/Kaguya products, ISRO Chandrayaan-2 products | Earth/Moon | DEM / terrain | 30 m or finer | Global/patchy | Varies | Agency portals | Varies | Free (B likely; **VERIFY**) | Optional (agency diversity) |
| NASA POWER or MERRA-2 climatology | Earth | Temp, climate | 0.5°–0.625° | Global | NetCDF/API | NASA | Small | Free, NASA-open (A/B; **VERIFY**) | Fallback if a climate licence is a problem (Risk 20) |
| Northern-Hemisphere permafrost map (e.g., Obu et al. 2019) | Earth | Ground-ice proxy | ~1 km | N. Hemisphere | GeoTIFF | PANGAEA | Small | Free (A; **VERIFY**) | Optional (improves R1) |
| CRISM, M3, HiRISE, CTX, LROC NAC | Both | Mineralogy, imagery | m-scale | Patchy | Huge | PDS | **Huge** | Free but unsuitable | **Do not use** |
| ERA5 / CDS | Earth | Climate | 0.25° | Global | NetCDF | Account required | Medium | Free but login (B) | Do not use (WorldClim suffices) |

**Categories.**

- **Must:** GEBCO, MOLA, LDEM_64, WorldClim, Aridity, MOD44B (or fallback), Natural Earth ice/urban masks.
- **Should:** GLiM, MCD43, Natural Earth/WDPA, MCD values, USGS maps, Diviner reference values.
- **Optional:** Copernicus GLO-30, THEMIS, GVP and impact DB tags, curated cave list, permafrost map, JAXA/ISRO products.
- **Do not use:** HiRISE, CTX, CRISM, M3, NAC. They are too heavy, patchy and mineral-specific for a global screen.

**Data volume.** The Must tier is roughly 10–15 GB raw on disk (**VERIFY** after downloading), and the derived store is under 1 GB. Allow at least 30 GB of free disk for intermediates. Because the event is six weeks away, download now: bandwidth caps are the most common hidden blocker.

**NASA-versus-other-agency note for the submission.** NASA data here: MOLA, LOLA, Diviner, MODIS (and SRTM underneath GEBCO's land layer, **VERIFY**). Non-NASA agency data: Copernicus GLO-30 (ESA/EC) and, optionally, JAXA or ISRO products. The submission must state this explicitly.

---

## PART 7: Data preparation

**Strategy: global coarse screening → targeted refinement.**

1. **Download** the Must tier to `data/raw/` (scripted, resumable, checksummed). Record version, DOI and retrieval date per file in `data_sources`.
2. **Metric spacing and reprojection.** The planetary DEMs are global lat-lon grids. Compute `dx = R·cos φ·Δλ` and `dy = R·Δφ` per row with each body's reference radius (Moon 1737.4 km, Mars 3396.19 km equatorial, which is the MOLA reference, Earth WGS84). Apply scale rule 2 from Part 3 for |lat| > 60°. For lunar polar targets, use the polar stereographic crop resampled to 500 m by averaging.
3. **Terrain features:** slope by Horn's method (the standard 3×3 finite-difference slope algorithm) on the ~0.5 km grid. Roughness is σ(slope) in a 3×3 window (freeze the choice in `tolerances.yaml`; run TRI as a sensitivity check only). Per cell: mean slope, slope P90, and relief = P95 − P5 of elevation.
4. **Cell aggregation.** Earth grid: **H3 resolution 5** (~253 km², ~15–17 km across, 2,016,842 cells globally; **VERIFIED**). Per cell: area-weighted (cos φ) median and P90 of pixel values. Compute tile-by-tile in 10° blocks to keep memory low, but note that **cells split across blocks cannot be combined from per-block medians**. Accumulate fixed-bin histograms per cell (mergeable across tiles) and read quantiles from the merged histograms. Assign pixels to H3 cells on land pixels only, and benchmark one tile in hour 1.
5. **Resampling.** Climate rasters (1–5 km) are sampled at the cell centroid or mean-aggregated. This is documented, not hidden.
6. **Tolerances.** The per-feature expert tolerance `δ_k` is set at feature-definition time in `config/tolerances.yaml`. The effective `τ_k` adds the target's own dispersion (`τ_k = sqrt(σ_k² + δ_k²)`, Part 9). No z-scoring across Earth is applied to absolute features.
7. **Missing data.** Store `NaN` plus a mask. The score renormalizes over available features, and coverage feeds confidence.
8. **Temporal mismatch.** Climate is climatological (30-year means); MODIS products are annual composites, so use a multi-year median (e.g., the latest 5 available years) for MOD44B. Document this. The Moon and Mars are static.
9. **Cloud/noise.** Use product quality flags; drop cells with >30% missing pixels.
10. **Masks.** Ocean: exclude cells with ≥ 50% of pixels at or below 0 m, and use land pixels only in coastal cells. Ice: Natural Earth glaciated areas. Urban: Natural Earth urban areas. Record the mask reason per cell.
11. **Caching.** Every stage writes Parquet to `data/processed/`, is idempotent, and writes a `manifest.json` with input hashes, versions and the config hash.

**Refinement (Stage 2).** For the top ~30 candidates only, optionally re-derive slope at 30 m from Copernicus GLO-30 to produce a finer datasheet. This is precomputed, not live. **Scale caveat:** a 30 m Earth slope is *not comparable* to a 0.5 km target value. Display Stage 2 numbers as "fine-scale context, not scored" unless the target is re-derived at the same baseline (e.g., LOLA 20–60 m polar DEMs, or CTX/HiRISE DTMs for a specific Mars site).

---

## PART 8: Earth candidate discovery

Pipeline: **Earth → H3 res-5 cells → exclusion masks → feature extraction → per-target similarity → profile-weighted score → greedy diversity selection → candidates.**

- **Cells:** 2,016,842 globally, ≈ 0.59 M land (≈ 0.53 M excluding Antarctica). Computation is trivial after zonal stats. The expensive part is the DEM pass (roughly tens of minutes on a laptop, tile-wise, **NEEDS VALIDATION** by the hour-1 benchmark).
- **Exclusions:** ocean, urban, permanent ice-sheet interior (**MVP choice**; ice-free Antarctic regions stay in), cells with bare-ground < ~80%.
- **No hard-coded sites.** Famous sites enter only as *validation positives* and as a "known analog registry."
- **Spatial indexing:** H3 ids are the key. Neighbours and diversity filtering use H3 rings (adjacent resolution-5 centres are ~14.8 km apart, so 300 km ≈ 20 rings, about 1,261 cells per disk). Use great-circle distance for the final distance checks.
- **Missing data:** the score is computed on available features only, and confidence drops.
- **Discovery vs feasibility balance:** discovery is global but at coarse resolution. Depth (datasheets) is reserved for the top ~30.
- **Reproducibility:** fixed random seeds, pinned versions, and a config hash stored with every output.

---


## PART 9: Similarity engine

| Method | Strengths | Weaknesses | Interpretability | Feasibility |
|---|---|---|---|---|
| A Weighted normalized distance | Transparent, per-feature breakdown | Ignores correlations | High | High |
| B Cosine | Scale-free | Ignores magnitude; wrong for absolute match | Medium | High |
| C Euclidean | Simple | Unit-dependent | Medium | High |
| D Mahalanobis | Handles correlation | Needs stable covariance; ref ROI too small | Low-Med | Medium |
| E PCA + distance | Decorrelates | Axes lose meaning | Low | Medium |
| F Clustering | Regimes, diversity | Not a ranking | Medium | High |
| G Supervised ML | Learns from labels | We have only ~10–15 labels; circular | Low | Low |
| H Hybrid | Best coverage | Complex | Medium | Medium |

**FINAL MVP METHOD: tolerance-kernel weighted similarity (a Gower-style weighted average of per-feature Gaussian similarities), with family caps and a critical-feature gate.**

Definitions, for Earth cell `c`, target `t` and profile `p`:

- `x_k` is the Earth cell value of feature `k` (NaN if missing).
- `μ_k`, `σ_k` are the target's median and robust SD from area-matched cells (Part 5).
- `δ_k` is the expert tolerance, "what counts as equivalent" (`config/tolerances.yaml`).
- `w_k` are the profile weights; families and caps are defined in Part 4.

```text
1. τ_k   = sqrt(σ_k² + δ_k²)
2. s_k   = exp( −½ · ((x_k − μ_k) / τ_k)² )      # in [0, 1]; s = 0.61 at |z| = 1, s = 0.2 at |z| ≈ 1.8
3. A     = { k : x_k is not NaN }                # available features
4. w'_k  = w_k / Σ_{j∈A} w_j                     # renormalize over available features
5. Family cap: for each family F, if Σ_{k∈F∩A} w'_k > cap_F, scale that family down to cap_F
   and redistribute the excess pro rata to the other families. Repeat until stable (max 5 passes).
   If only one family remains available, skip the cap and let coverage carry the penalty.
6. Score = round( 100 · Σ_{k∈A} w'_k · s_k )     # integer 0–100
7. Gate: if any critical feature k ∈ A has s_k < 0.2 (|z| > ~1.8), then Score = min(Score, 50) and flag "gated by <feature>"
```

- **Critical features (HEURISTIC):** T1 and T2 for every profile, plus T3 for the rover/EVA profiles C and D. A proxy feature is never critical.
- **Family caps:** 0.5 by default; Terrain 0.6 for profiles C and D (Part 4). This is a pragmatic substitute for Mahalanobis. **HEURISTIC.**
- **Relative-regime features (E1–E3, R1):** replace `x_k` and `μ_k` with a within-body percentile before applying the kernel. The Earth percentile is taken among *eligible* (gate-passing) Earth cells, and the target percentile within its own body's global distribution. `δ_k` is in percentile points (default 10). **HEURISTIC.**
- **Aridity (E1) is ordinal:** use the UNEP classes of the aridity index (hyper-arid < 0.05, arid 0.05–0.20, semi-arid 0.20–0.50, other). Default step similarity against a hyper-arid reference: 1.0, 0.6, 0.2, 0. **HEURISTIC.**
- **Quantization for export:** store `s_k` as `uint8` values 0–254 (`round(254·s)`), with **255 meaning missing**, because 0 is a valid similarity.

**ADVANCED:** Mahalanobis with Ledoit–Wolf shrinkage (a regularized covariance estimator), plus PCA for visualization. Not for the MVP.

**What the score means:** "weighted agreement across the *selected, available* features, under the chosen profile."

**What it does NOT mean:** probability of being Mars-like, a mission suitability certification, or anything about the factors Earth cannot reproduce (vacuum, radiation, gravity). We present it as a **0–100 index**, rounded to integers, never to decimals.

---

## PART 10: Validation

**Positive set** (from literature; confirm each against an authoritative source and record the citation. **NEEDS VALIDATION** before use).

- *Mars-oriented:* Atacama (Yungay), Utah MDRS, Rio Tinto (Spain), Antarctic Dry Valleys, Haughton crater (Devon Island).
- *Moon-oriented:* Craters of the Moon (Idaho), SP Crater / Black Point lava flow (Arizona), Mauna Kea/Kilauea (Hawaii), Askja (Iceland), Meteor Crater (Arizona).
- *Other agencies (optional, VERIFY):* ESA PANGAEA training sites such as Lanzarote and the Ries crater.
- Only use sites with documented NASA/ESA/agency analog or training use. Do not include Death Valley blindly; check which mission use is documented.
- **Expected false negatives.** Rio Tinto's analog value is geochemical (acidic, iron-rich), which our terrain and climate features barely capture. Report such sites separately rather than hiding them.

**Positive-cell rule.** Analog sites are often smaller than a 16 km cell. Assign each positive to the H3 cell containing its centroid plus its 1-ring (7 cells) and use the best percentile of the seven. Declare the rule before the first run.

**Negative controls.**

- *Easy negatives* (Amazon basin, Congo basin, Ganges plain, Netherlands). These are removed by the barren-ground, ice and urban gates, so they only prove the gate works. Report them as "gated", not as score evidence.
- *Hard negatives (≥ 3, chosen by P1 with a written rationale before the first run).* Barren cells that pass the gates but should mismatch one profile, for example a hot, low-relief sand sea for the cold polar Profile A. These test the kernel itself. Require them to rank below the 50th percentile of gate-passing cells.

**Which target and profile.** Evaluate each positive against its body's profiles using one **default target per profile** (Connecting Ridge for A, Arcadia for B, Jezero for C, Taurus-Littrow for D). Also report the "best of the body's targets" variant, and say clearly that it is more generous.

**Tests.**

1. **Percentile rank** of each positive's cell among **gate-passing cells** (primary) and among all land cells (secondary), per relevant profile. Pass: median ≥ 90th percentile. Stretch: ≥ 95th. Without the gate-aware baseline, the barren-ground filter alone would carry the result.
2. **Top-k recovery:** fraction of positives in the top 1% / 5% of gate-passing cells.
3. **ROC-AUC** of positives vs random gate-passing cells. These are *unlabeled* rather than true negatives (many other places would also be good analogs), so AUC is conservative. Say so.
4. **Negative-control check:** easy negatives are gated; hard negatives are below the 50th percentile.
5. **Baselines.** Compare the full score against (a) a random gate-passing cell, (b) aridity only, (c) terrain only, (d) climate only. This shows what each family contributes and that the kernel adds value beyond the gate.
6. **False positives:** manually inspect the top 30. Are there obvious mismatches (e.g., ice sheets that slip through)? Document each and add a gate if justified.
7. **False negatives:** positives that rank low. Diagnose the feature (e.g., Haughton's ice/cold).
8. **Weight sensitivity:** 500 Dirichlet-perturbed weight vectors around each profile (`w' ~ Dirichlet(α·w)`, α = 100 default, α = 20 stress case; zero weights stay zero). Report Spearman ρ between rankings and top-k stability.
9. **Ablation:** leave one feature family out.
10. **Missing data:** randomly mask 20% of feature values; report rank change.
11. **Scale sensitivity:** repeat at H3 res 4 and 6 (re-tile the reference ROIs to the matching area).
12. **Uncertainty on the metrics:** with only ~10–15 positives, report 95% bootstrap intervals (1,000 resamples over positives) for median percentile and AUC.

**Circularity caveat.** Analog sites were chosen partly *because* of terrain and climate we also measure. Weights and tolerances are fixed a priori and not tuned on the positives. **Pre-register:** git-tag the config hash before the first validation run, and log every later change (bug fixes, new gates) in `docs/VALIDATION.md` with its justification. State the result as "face validity and consistency," not proof.

**Acceptable hackathon evidence:** a one-page validation figure (percentile ranks of positives vs hard negatives with intervals, AUC vs baselines, a stability plot) plus an honest list of failures.

---

## PART 11: Novel analog discovery

A candidate is **"novel to our registry"** when it meets all of these:

- top 1% of gate-passing cells for the profile;
- >200 km (great-circle) from every registry site;
- evidence coverage ≥ 80%;
- stability ≥ 0.8 (the same threshold as "High" confidence in Part 12);
- **prior-use check passed:** a documented search (agency pages, Google Scholar, NASA/ESA/ISRO/JAXA analog lists) found no known analog or training use. The datasheet records the query, the date and the result. If prior use is found, label the site "known (not in registry)" and add it to the registry.

We say "not previously listed in our analog registry," never "new to science."

**Registry.** Aim for at least 30 agency-documented analog sites (NASA, ESA, CSA, JAXA, ISRO and others, **VERIFY** each). The validation positives (~10–15) are a subset. The rest are used only for the novelty distance check and for "nearest known analog."

**Diversity.** Greedy non-maximum suppression (NMS): take the highest-scoring cell, suppress cells within 300 km, and repeat. Optionally cap at 2 per country. Regime clusters (Part 13) label each result's type.

**Per-site output:** location, score, profile, feature breakdown, top contributors, weakest feature, evidence and data sources, confidence, coverage, stability, proxy share, nearest known analog *in feature space*, prior-use check result, and an analog datasheet (a frozen JSON schema, so the frontend and exports never drift). For the lava-tube module, overlay a curated cave list and **do not claim discovered caves.**

---

## PART 12: Uncertainty and confidence

Output format:

> **Analog Score 82 / 100 · Confidence Medium · Evidence Coverage 90% · Proxy reliance 40% · Rank stability 72% · Primary uncertainty: thermal regime (proxy).**

**MVP confidence (HEURISTIC, documented):**

- **Coverage** = Σw(available) / Σw.
- **Proxy share** = Σ(w × is_proxy) / Σw over the *available* features. Shown on every score as its own badge. The confidence ceiling below uses the *active-weights* version over all features instead.
- **Stability** = share of 500 Dirichlet-perturbed weight vectors (`w' ~ Dirichlet(α·w)`, α = 100 default, zero weights stay zero) that keep the cell in the profile's top 5% of gate-passing cells.
- **Reference uncertainty** = mean σ_k/τ_k over the target's scored features. A value near 1 means the target's own spread dominates the tolerance, so the kernel is wide and less discriminating.

**Rule:**

- **High** requires all of: coverage ≥ 0.85, stability ≥ 0.8, reference uncertainty ≤ 0.8, **and** an active-weights proxy share ≤ 0.5.
- **Low** if coverage < 0.6 or stability < 0.4.
- Otherwise **Medium.**

Thresholds are labeled as heuristic in the app, and a tooltip explains each component.

**Proxy ceiling (changed from v1).** v1 required a per-site proxy share ≤ 0.4. At default weights the proxy share is 0.54, 0.70, 0.44, 0.40 and 0.60 for profiles A–E (Part 4), so that rule made High unreachable for four of five profiles, and it perversely rewarded sites whose proxy data were *missing*. v2 computes the proxy share from the **active weights** (defaults or slider values), not per-site missingness. Consequences: profiles A, B and E are "proxy-heavy" and capped at Medium by design, and the UI says so. Profiles C and D can reach High. Moving sliders to reduce proxy weight lifts the ceiling live, which is a good demo moment.

**Custom weights.** Stability is precomputed for the default weights. Under custom sliders the UI keeps showing the default-weight stability with a "not recomputed" badge, and confidence is capped at Medium.

---

## PART 13: Machine learning

**ML is not required for the core score, and we say so.** Use it only where it adds value, and label it "supporting analytics, not part of the score" in the app.

- **MVP ML:**
  - *PCA* on the standardized Earth feature matrix, computed on gate-passing cells: check feature redundancy and drive a 2D "feature space" plot with the targets overlaid (good for the demo).
  - *k-means (k≈8–12, fixed seed, k chosen by silhouette or elbow)* to define terrain-climate regimes for diversity and naming. Name each cluster from its centroid features.
  - *Isolation Forest* is optional, to flag cells with unusual feature combinations; use only if time permits.
- **Advanced ML:** shrinkage Mahalanobis; a learned metric only if you obtain a larger labeled analog set. **Avoid** deep learning: there are no labels, and it would hurt explainability.

---

## PART 14: LLM

**Architecture:** Engine → `evidence_card.json` → prompt → LLM → explanation → **validator** → UI.

- **Roles:** explain a ranking, compare two sites, translate "why not X" questions, draft a report. It never computes or edits scores.
- **Evidence card:** all numbers are **pre-formatted strings** with units (e.g., `"slope_mean": "2.1°"`), so the validator can check exact text rather than guess at rounding.
- **Prompt rules:** "Use only the JSON provided. Quote numbers exactly. If a field is null, say it is unavailable. Do not state anything about the site that is not in the JSON." Use temperature 0 and a JSON-schema response format where the runtime supports it.
- **Output:** structured JSON `{summary, strengths[], weaknesses[], caveats[], cited_fields[]}`.
- **Guardrails:** a post-check confirms every number in the text appears in the JSON as an exact string, every cited field exists, and no banned phrase from the claims policy appears (e.g., "proven", "equivalent", "NASA-approved", "probability"). Failures fall back to the template. User free text is treated as untrusted data and not instructions. The UI renders LLM text as plain text, never as HTML.
- **Failure behavior / fallback (mandatory):** a deterministic **template explainer** generates the same card with no LLM. The LLM output is an upgrade, never a dependency.
- **LLM source:** a local model via Ollama (a ~7–8B instruct model such as Qwen or Llama, if laptops have ≥ 8–16 GB RAM; **VERIFY** which models the Ollama library currently offers) **or** pre-generate explanations for the top ~100 sites using your existing subscriptions through the web UI and cache them as JSON. No API billing.
- **AI-use disclosure.** Record the tool, version, date and purpose for every AI-assisted artifact (explanations and any AI-assisted code or text) in `docs/AI_DISCLOSURE.md`. This follows NASA's own guidance on acknowledging generative-AI content and the Space Apps "cite every source" rule. **VERIFY** the exact 2026 wording.
- **RAG:** **not needed in the MVP.** Instead, a small curated `knowledge_cards.yaml` (~30 entries with citations on features, targets and caveats) is injected by key. **Advanced:** local embeddings plus FAISS over NASA documentation.

---


## PART 15: GIS / map

| Option | License | 2D/3D | Fit |
|---|---|---|---|
| **MapLibre GL JS** | BSD-3 | 2D + globe (recent versions), terrain | **Choose.** Free, vector tiles, no token. |
| Leaflet | BSD-2 | 2D | Simple, weak for many features |
| Cesium | Apache-2 (CesiumJS) | 3D globe | Heavy; ion terrain needs account |
| deck.gl | MIT | GPU layers (H3 hex) | Optional overlay if rendering struggles |

**Primary: MapLibre GL JS with a free basemap (self-hosted/pmtiles or Natural Earth), and no commercial tile API.** Top ~2,000 candidate hexes render as GeoJSON polygons. A full land-cell heatmap (≈ 0.59 M cells, fewer after the gates) is optional (pre-rendered raster at low zoom).

**Map edge cases to test explicitly:** hexes that cross the antimeridian or contain a pole produce broken polygons unless split, so keep a test fixture for each. Use a colour-blind-safe sequential ramp for scores, and never rely on colour alone to show confidence.

---

## PART 16: UI/UX

- **Main screen:** left control panel (Moon/Mars selector → target → mission profile → weight sliders → filters); centre map; right ranking panel.
- **Ranking list:** rank, score, confidence badge, proxy-share badge, region name.
- **Site detail drawer:** feature bars (Earth vs target), evidence and data sources, uncertainty breakdown, operational accessibility, nearest known analog, prior-use check, and a **"Why ranked high?"** AI panel.
- **Comparison view:** Earth candidate vs planetary reference, side by side, with a radar chart and feature table.
- **Journey:** choose mission → choose target → see ranked map → click a site → read evidence → compare with a known analog → move sliders → ranking re-sorts → export datasheet (Markdown or HTML, print to PDF from the browser).
- **Persistent claims banner on every screen:** "Index of agreement on selected terrain, surface and climate variables. Not a mission-suitability certification. Not endorsed by NASA."
- **States to design, not leave to chance:** loading, empty ranking (all candidates gated), LLM unavailable (show the template card without an error), and "custom weights: stability not recomputed."
- **Accessibility basics:** keyboard-reachable sliders and ranking rows, visible focus, text alternatives for charts, and a contrast check on badges.

---

## PART 17: Architecture

**Smallest reliable stack:**

- **Offline engine (Python):** NumPy, rasterio/GDAL, xarray (optional), GeoPandas, h3, scikit-learn, DuckDB/Parquet.
- **Serving:** FastAPI (optional layer).
- **Frontend:** React + Vite + MapLibre.

**Key trick:** the engine precomputes a `similarity_matrix` (gate-passing cells × features × targets, `uint8`, 0–254 with 255 = missing). The browser applies weights. The demo therefore works with **no live backend**, and FastAPI adds only datasheets, comparison and LLM explanations.

- **Size:** at most ~0.59 M cells × 10 features × 7 targets ≈ 41 MB, and far less after the gates. The browser loads one target's slab (a few MB).
- **Speed:** a weighted re-score is ~6 M multiply-adds plus a top-k selection on typed arrays, well inside the 300 ms budget. **NEEDS VALIDATION** on the weakest demo laptop.
- **Parity (required):** the JavaScript scorer must implement steps 3–7 of Part 9 (renormalize, family caps, gate). A golden test compares it with the Python engine on 1,000 sampled cells × 5 profiles and must agree to ±1 point.
- **Custom weights:** stability is not recomputed (Part 12), and confidence is capped at Medium.

**Why not microservices:** a single FastAPI process and static assets are enough.

---

## PART 18: Database

**Recommendation:** DuckDB + Parquet (a single file, no server, zero setup). The schema below is portable to PostGIS if the team prefers (add `geom GEOMETRY(Polygon,4326)` with GiST indexes). H3 ids remove most spatial joins. This is a schema sketch, not runnable DDL.

```text
data_sources(id PK, name, body, variable, url, doi, license, access_class, retrieved_at, version, sha256)
planetary_targets(id PK, body, name, lat, lon, radius_km, notes, citation)
planetary_features(target_id FK, feature_key, median, iqr, sigma, mode, n_cells, n_pixels, source_id FK)
mission_profiles(id PK, name, body, weights_json, constraints_json, family_caps_json, version)
earth_cells(h3 BIGINT PK, lat, lon, country, region_name, regime_cluster, masked BOOL, mask_reason)
earth_features(h3 FK, feature_key, value, is_missing, source_id FK)   -- idx (feature_key, h3)
cell_similarity(h3 FK, target_id FK, feature_key, s UTINYINT)         -- idx (target_id, h3); 255 = missing
analysis_runs(id PK, profile_id, target_id, weights_json, created_at, engine_version, config_hash)
candidate_sites(run_id FK, h3 FK, rank, score, confidence, coverage, proxy_share, stability, novel BOOL, prior_use_check)
evidence(run_id, h3, feature_key, earth_value, target_value, s, is_proxy, source_id)
known_analogs(id PK, name, lat, lon, h3, label, agency, documented_use, profile_tags, citation)
```

`known_analogs.label` takes the values `positive`, `negative_easy`, `negative_hard` or `registry_only`, so validation and novelty use one table. `config_hash` ties every run to the exact profiles, tolerances and code version.

---

## PART 19: API (REST)

All paths are prefixed `/api/v1`.

| Endpoint | Method | Purpose |
|---|---|---|
| `/profiles` | GET | List mission profiles, default weights, family caps and proxy shares |
| `/targets?body=mars` | GET | List reference targets |
| `/analysis` | POST `{target_id, profile_id, weights?, filters?, top_n}` | Run or re-score → `{run_id, candidates[]}` |
| `/candidates/{run_id}` | GET | Paged ranking |
| `/sites/{h3}?run_id=` | GET | Datasheet: features, evidence, confidence |
| `/sites/{h3}/datasheet?run_id=&format=json\|md\|html` | GET | Exportable datasheet |
| `/compare` | POST `{h3_a, h3_b or target_id}` | Side-by-side table |
| `/explain` | POST `{run_id, h3}` | Template or LLM explanation (validated) |
| `/validation` | GET | Validation metrics and plots data |
| `/health` | GET | Liveness |

**Static-mode equivalents.** Each endpoint has a pre-built JSON file under `data/exports/` (profiles, targets, per-target similarity slabs, top-N candidates, datasheets, validation, cached explanations), so the frontend works with no server.

**Validation:** weights must be finite and ≥ 0, at least one must be > 0, and they are renormalized; `top_n` ≤ 500; `h3` must be a valid resolution-5 index; `profile_id` and `target_id` must belong to the same body.

**Errors:** 400 invalid input, 404 unknown id, 422 schema. `/explain` always returns 200 with `explanation_source: "llm" | "cache" | "template"`. An unavailable LLM falls back to the template and is never surfaced to the UI as an error.

---

## PART 20: Repository

```text
analogatlas/
├─ README.md            # what it is, offline run in < 10 min, AI-use disclosure, data credits
├─ LICENSE              # OSI-approved licence (e.g., MIT or Apache-2.0), required by the 2026 terms
├─ Makefile             # make data | features | similarity | validate | export | demo
├─ environment.yml      # pinned conda env (GDAL/rasterio/h3 install issues, Risk 8)
├─ frontend/            # React+Vite+MapLibre; src/{components,map,state,api}
├─ backend/             # FastAPI: routers/, schemas/, services/ (thin)
├─ engine/              # scientific engine (pure Python, no web deps)
│  ├─ features/         # slope.py, roughness.py, climate.py, ...
│  ├─ similarity/       # kernel.py, confidence.py, diversity.py
│  ├─ validation/       # known_analogs.py, metrics.py, sensitivity.py
│  └─ explain/          # template.py, llm.py, validator.py
├─ schemas/             # JSON Schemas: evidence_card, datasheet, export manifest (Risk 15)
├─ config/              # profiles.yaml, targets.yaml, tolerances.yaml, knowledge_cards.yaml
├─ data/{raw,processed,exports}/   # raw and processed gitignored; data/exports committed (small)
├─ scripts/             # download_*.py, build_features.py, build_similarity.py, export_static.py
├─ tests/               # unit tests, JS-vs-Python parity test, antimeridian/polar hex fixtures
├─ docs/                # METHODOLOGY.md, CLAIMS_POLICY.md, VALIDATION.md, DATA_SOURCES.md, AI_DISCLOSURE.md
├─ .github/workflows/   # CI: lint + tests
└─ docker-compose.yml   # optional
```

The key boundary: `engine/` has no web dependency, so science and web work do not collide.

---

## PART 21: Security (baseline)

- **Secrets:** none required at demo time. Earthdata credentials are needed only to download data; keep them in `~/.netrc` or environment variables, never in the repo. Any other config goes in `.env`, which is gitignored.
- **CORS:** allow only the frontend origin.
- **Input validation:** Pydantic schemas with bounds (Part 19).
- **Rate limiting:** a simple in-memory limiter on `/explain`.
- **Uploads:** none in the MVP.
- **Prompt injection:** the LLM receives only engine JSON plus a short user question inside a delimited block; output is validated. Never include raw web or document text.
- **Output handling:** render LLM text as plain text. Never use `dangerouslySetInnerHTML` (or equivalent) with it.
- **DB:** read-only DuckDB connection in the API.
- **Dependencies:** pin versions; run `pip-audit` and `npm audit` once before the demo.
- **Network binding:** bind to `127.0.0.1` unless you deliberately demo over a LAN.
- **Logging:** log request ids and errors, never full prompts with user content beyond what is needed.

---

## PART 22: Performance

| Bottleneck | MVP strategy | Future |
|---|---|---|
| Raster processing | Tile-wise (10° blocks) with mergeable per-cell histograms, precomputed once | Dask / COG streaming |
| Zonal stats | Pixel→H3 aggregation on land pixels only | Parallelism |
| Candidate search | Precomputed uint8 similarity matrix; weighted sum in browser | Server-side vectorized scoring |
| Map rendering | Top-2k hexes only | PMTiles / deck.gl H3 layer |
| LLM | Cached explanations; template fallback | Batch |

**Budgets:** slider re-rank < 300 ms; first map render < 3 s on the demo laptop; site drawer < 200 ms from cache; `make demo` from a clean checkout < 10 minutes.

---

## PART 23: Offline-resilient demo

- **Precompute and ship in the repo (`data/exports/`):** similarity matrix, top-N candidates per profile × target, datasheets, validation figures, cached LLM explanations, and a basemap (Natural Earth vectors or a local pmtiles file).
- **Dynamic:** only weight re-scoring (in the browser) and optionally `/explain`.
- **No dependency on NASA APIs at demo time.** All NASA data is downloaded in advance.
- **Self-host everything the page loads:** fonts, MapLibre glyphs and sprites (a vector style with labels fails offline without them), icons and chart libraries. Test with the network disabled.
- **Fallback chain:** live LLM → cached LLM text → template text.
- **Last resort:** a recorded 3-minute screen capture and a PDF datasheet pack.
- **Demo-day checklist:** clean-checkout run on the demo laptop, power and display adapters, screen resolution and zoom level set, notifications off, video and slides hosted at a public link (the Space Apps site takes links, not uploads).

---

## PART 24: ₹0 deployment (**VERIFY all hosting terms**)

- **PRIMARY:** demo from a team laptop: `uvicorn` serving the built frontend and API. This is the most reliable option and has no network dependency.
- **BACKUP:** a **static build** (no backend; precomputed JSON, client-side scoring, template explanations) on GitHub Pages or a similar free static host (e.g., Cloudflare Pages or Netlify; compare each host's per-file and site-size limits). Class A-B: free, no billing for public repos, with size limits (keep files well under ~100 MB each and the site under ~1 GB on GitHub Pages). **VERIFY.**
- **Optional backend hosting:** free CPU tiers (e.g., Render free, Hugging Face Spaces) exist but **sleep or have quotas, so class B**, and some may ask for billing details. **Never make them necessary.**
- **LOCAL DEMO FALLBACK:** the recorded video plus offline exports.
- **Licensing of what you publish:** the repo carries an OSI-approved licence (Part 20). Do not commit raw third-party data whose terms restrict redistribution (e.g., WDPA); ship derived per-cell values and cite the source.

---

## PART 25: MVP definition

- **MUST:** the Must-tier data → features → similarity engine → ≥ 3 profiles and ≥ 5 targets → ranked map → site datasheet → live weight sliders → confidence → validation page (known analogs, hard negatives and baselines) → template explainer → claims policy → **submission package** (hosted demo link, README with AI disclosure and data credits, OSI licence, citations).
- **SHOULD:** all 5 profiles, GLiM geology, albedo, operational axis, LLM explainer (cached), comparison view, PCA plot.
- **ADVANCED:** Stage-2 30 m refinement, lava-tube overlay, Mahalanobis, local RAG, PDF report export.
- **CUT FIRST:** RAG, 3D globe, Stage-2 refinement, THEMIS/LROC layers, supervised ML, PostGIS, hosted backend.

---


## PART 26: 24-hour plan (survival cut)

**Pre-event window (4 Oct → 13 Nov; dates CHECKED).** The hackathon is 14–15 Nov, so the first hours of every plan below should start *ready*:

- **Do now:** create the Earthdata account, build the pinned environment (`environment.yml`), download the Must-tier data (DATA-0 to DATA-2), re-read the challenge page after 28 Oct, and decide targets, tolerances, weights and hard negatives on paper (SCI-1 to SCI-3).
- **Rules check (VERIFY):** the terms cover original content "created for" the challenge and ask you to cite every source. To stay safe, write the core engine during the event and openly declare anything written earlier. Data acquisition, environment setup and science decisions are preparation, not code.
- **Capacity check.** Four people at ~60% productive time give about 58 person-hours in 24 h and about 115 in 48 h. The P0 backlog is about 88 hours (Part 30). It fits the 48-hour plan with slack. It does **not** fit 24 hours without the cuts below *and* the pre-event preparation above.

| Hours | Objective | Owner | Output / acceptance |
|---|---|---|---|
| 0–2 | Setup check, scope freeze, JSON/Parquet contracts; confirm pre-event downloads (else start them now) | All | Repo + data present |
| 2–8 | Terrain features for 3 bodies at ~0.5 km (metric spacing, area-matched targets); H3 cells; climate + aridity + masks join | P2, P3 | `earth_features.parquet` for ≥ 6 features |
| 2–8 | Targets YAML (5 targets), profiles, tolerances; config frozen | P1 | Citations recorded |
| 2–8 | Frontend shell + map with fake data | P4 | Map shows hexes |
| 8–14 | Similarity + ranking + diversity; API stub; JS scorer | P2, P3 | Top-20 per profile |
| 8–14 | Positives/hard negatives list, validation script (v0) | P1 | AUC + percentile table |
| 14–19 | Integrate real results; sliders; site panel | P3, P4 | End-to-end demo |
| 19–22 | Template explainer, confidence, claims text | P1, P2 | Datasheet card |
| 22–24 | Rehearse, record fallback video, submit | All | Submission |

**Cuts for 24 h:** drop the LLM, geology, albedo, comparison view and PCA plot; use 3 profiles; defer the Dirichlet stability panel (SCI-6); shrink TEST-1 to percentile + AUC with the gate-aware baseline; reduce DOC-1 to the README.

---

## PART 27: 36-hour plan

Same as the 24 h plan, plus:

- **Hours 24–30:** GLiM geology, albedo, all 5 profiles, sensitivity analysis and the confidence model (including stability), comparison view.
- **Hours 30–36:** cached LLM explanations, validation figures, UI polish, demo rehearsal, video.

---

## PART 28: 48-hour plan

| Hours | Block |
|---|---|
| 0–4 | Setup check, scope freeze, contracts; confirm pre-event downloads |
| 4–12 | Terrain features, cells, climate, aridity, masks (bare-ground, ice, ocean), area-matched targets |
| 12–18 | Similarity engine, profiles, diversity, API. **Tag the pre-registered config at ~hour 14, then run validation v0 (a smoke test) at ~hour 18.** Early failures are cheaper to diagnose. Fix bugs, do not tune weights. |
| 18–24 | Map, ranking panel, sliders, datasheet, JS-vs-Python parity test |
| 24–30 | Geology, albedo, operational axis, confidence |
| 30–36 | **Validation and sensitivity** (dedicated), LLM explainer + guardrails |
| 36–40 | Integration testing, bug bash, offline export build |
| 40–44 | UI polish, documentation (METHODOLOGY, CLAIMS, VALIDATION) |
| 44–46 | Demo rehearsal, fallback video recording, host the video |
| 46–48 | Presentation prep, submission, buffer. Submit at least 2 h before the deadline, because submission is final (**VERIFY** the deadline). |

---

## PART 29: Team of 4

| Person | Responsibilities | Deliverables | Backup for |
|---|---|---|---|
| **P1 Planetary Science/Data** | Targets, tolerances, weights, analog registry, hard negatives, citations, claims policy, validation interpretation, knowledge cards | `targets.yaml`, `profiles.yaml`, `known_analogs`, `VALIDATION.md` | P2 (feature checks) |
| **P2 Geospatial/ML** | Terrain features, zonal stats, H3, similarity, confidence, sensitivity, PCA/k-means | `engine/` | P3 |
| **P3 Backend/Data Infra** | Download scripts, Parquet/DuckDB, API, export builder, template/LLM service | `scripts/`, `backend/` | P4 |
| **P4 Frontend/UX** | Map, panels, sliders, comparison, charts, polish, demo flow | `frontend/` | P1 (docs) |

**Minimizing conflicts:** agree on the JSON/Parquet contracts in hour 1, and P4 develops against a mock export from hour 2. Directory ownership matches the table.

**Checkpoints (24 h plan; scale proportionally for 36 and 48 h):** hour 8 features exist; hour 14 a ranking exists; hour 19 end-to-end demo works; hour 22 feature freeze. At each checkpoint, apply the cut list rather than slipping.

---

## PART 30: Backlog (condensed; effort in hours)

| ID | Title | Pri | Owner | Deps | Acceptance | Est |
|---|---|---|---|---|---|---|
| DATA-0 | Earthdata account, pinned environment, disk and bandwidth check | P0 | P3 | – | `make data` dry run passes | 1 |
| DATA-1 | Download GEBCO, LDEM_64, MOLA | P0 | P3 | DATA-0 | Files + checksums + version/DOI recorded | 3 |
| DATA-2 | Download WorldClim, Aridity, MOD44B, Natural Earth ice/urban masks | P0 | P3 | DATA-0 | Files present | 3 |
| DATA-3 | GLiM, Natural Earth roads/places, WDPA | P1 | P3 | DATA-0 | Loaded | 2 |
| DATA-4 | Data source registry table | P1 | P3 | DATA-1, DATA-2 | All sources have licence + URL + access class | 1 |
| SCI-1 | Targets YAML (≥5) with citations | P0 | P1 | – | Reviewed; centres and ROI radii recorded | 4 |
| SCI-2 | Profiles + tolerances + weights + family caps | P0 | P1 | – | YAML valid; family totals and proxy shares computed by script | 3 |
| SCI-3 | Known analogs, hard negatives, registry (≥ 30 sites) | P0 | P1 | – | Each with citation; hard negatives justified before first run | 3 |
| SCI-4 | Claims policy doc | P1 | P1 | – | Published | 1 |
| SCI-8 | Pre-registration tag + change log | P0 | P1 | SCI-2, SCI-3 | Config hash tagged before first validation run | 1 |
| GIS-1 | Slope/roughness/relief for 3 bodies at ~0.5 km (metric spacing, high-latitude fix) | P0 | P2 | DATA-1 | Spot-check vs known values; cross-body slope histograms | 6 |
| GIS-2 | H3 grid + zonal stats (mergeable histograms) | P0 | P2 | GIS-1 | `earth_features.parquet` | 5 |
| GIS-3 | Climate/aridity/bare-ground join + ice/urban/ocean masks | P0 | P2 | DATA-2 | Coverage report | 4 |
| GIS-4 | Target feature vectors (area-matched tessellation) | P0 | P2 | GIS-1, SCI-1 | `planetary_features` with `n_cells` ≥ 7 | 3 |
| GIS-5 | Geology + albedo features | P1 | P2 | DATA-3 | Joined | 4 |
| SCI-5 | Similarity kernel + family caps + gating | P0 | P2 | GIS-2, GIS-4 | Unit tests pass | 4 |
| SCI-6 | Confidence + Dirichlet stability | P0 | P2 | SCI-5 | Output per cell | 4 |
| SCI-7 | Diversity NMS + prior-use check template | P1 | P2 | SCI-5 | Min distance verified | 2 |
| TEST-1 | Validation harness (gate-aware percentile, AUC, hard negatives, baselines, bootstrap intervals) | P0 | P1/P2 | SCI-5, SCI-8 | Report generated | 6 |
| TEST-2 | Sensitivity + ablation + missing-data tests | P1 | P2 | SCI-6 | Figures | 4 |
| TEST-3 | Scale sensitivity (res 4/6) | P2 | P2 | GIS-2 | Table | 3 |
| BE-1 | Export builder (uint8 matrix, top-N JSON) | P0 | P3 | SCI-5 | Files < size limit | 3 |
| BE-2 | FastAPI endpoints | P1 | P3 | BE-1 | OpenAPI works | 5 |
| BE-3 | DuckDB loaders | P1 | P3 | GIS-2 | Queries < 1 s | 3 |
| AI-1 | Template explainer | P0 | P1/P3 | SCI-5 | Deterministic card | 3 |
| AI-2 | LLM explainer + validator | P2 | P3 | AI-1 | Number-check passes | 5 |
| AI-3 | Pre-generated explanation cache | P2 | P3 | AI-2 | Top-100 cached | 2 |
| FE-1 | Map + hex layer (antimeridian and polar fixtures) | P0 | P4 | mock | Renders 2k hexes | 5 |
| FE-2 | Target/profile selectors + sliders (client scoring) | P0 | P4 | BE-1 | Ranking updates < 300 ms | 6 |
| QA-1 | JS-vs-Python parity test | P0 | P3/P4 | FE-2, SCI-5 | Agrees to ±1 point on 1,000 cells × 5 profiles | 2 |
| FE-3 | Site drawer + datasheet (claims banner, proxy badges) | P0 | P4 | BE-1 | Features, confidence, sources | 6 |
| FE-4 | Comparison view | P1 | P4 | FE-3 | Side-by-side | 4 |
| FE-5 | Validation page + PCA plot | P1 | P4 | TEST-1 | Charts | 4 |
| DEP-1 | Static build + local run script | P0 | P3 | FE-2 | Opens offline (network disabled) | 3 |
| DEP-2 | Static hosting | P2 | P3 | DEP-1 | Public URL | 2 |
| DOC-1 | METHODOLOGY + DATA_SOURCES | P0 | P1 | – | Complete | 3 |
| DOC-2 | Demo script + video | P0 | All | all | Recorded and hosted at a public link | 4 |
| DOC-3 | Submission package: README, OSI LICENSE, AI disclosure, NASA/partner data list, citations | P0 | All | DOC-1 | Matches the Space Apps form fields | 3 |

**Effort totals:** 38 items, **130 h** in total: **P0 88 h**, P1 30 h, P2 12 h. At ~60% productive time a team of four has about 115 h in 48 h, so P0 fits the 48-hour plan with slack but not a 24-hour plan without the cuts in Part 26.

---

## PART 31: Risks

**Legend.** P = probability, I = impact (L low, M medium, H high).

| # | Risk | P | I | Detection | Mitigation | Backup |
|---|---|---|---|---|---|---|
| 1 | Slope scale mismatch | M | H | Cross-body slope histograms | Matched ~0.5 km baseline, isotropic at high latitude | Report scale caveat |
| 2 | Thermal comparison not physical | H | M | Review | Relative-regime mode, labeled proxy | Down-weight |
| 3 | Known analogs rank poorly | M | H | Validation | Diagnose features; honest report | Reframe as a limitation |
| 4 | Circular validation attacked | M | M | Review | State caveat; fixed weights; pre-registered config | Add hard negatives and baselines |
| 5 | Downloads slow/blocked | M | H | Early check | Download in the pre-event window | Coarser alternatives |
| 6 | Earthdata login friction | M | L | Setup | Create accounts early (DATA-0) | MOD13C2 / skip MODIS |
| 7 | Laptop memory limits | M | M | Crashes | Tile-wise, mergeable histograms | Coarser grid |
| 8 | H3/GDAL install problems | M | M | Setup | Pin versions early | Conda env |
| 9 | Lunar polar geometry errors | M | M | Spot-check | Polar stereographic crops | Use lat-lon with caveat |
| 10 | Target coordinates wrong | L | H | Peer check | Cite sources | Remove target |
| 11 | Weights seen as arbitrary | H | M | Judge Q&A | Sensitivity + sliders | Equal weights profile |
| 12 | Proxy shown as fact | M | H | Review | Flags, proxy-share badge, claims policy | Label all |
| 13 | LLM hallucination | M | H | Validator | Grounded JSON, exact-string number check | Template |
| 14 | LLM unavailable | M | L | Test | Cache + template | Template |
| 15 | Frontend–engine contract drift | H | M | Integration | JSON schemas, mock, parity test | Freeze by hr 12 |
| 16 | Map performance | M | M | Test | Top-2k only | Points not polygons |
| 17 | Hosting free tier changes | M | L | Check | Local primary | Video |
| 18 | Time overrun | H | H | Checkpoints | Cut list | MVP-Lite |
| 19 | Judges say "just Earth/Mars matching" | M | M | Pitch review | Emphasize profiles, validation, datasheets | Demo emphasis |
| 20 | Licence misuse or terms conflict (e.g., WorldClim and Aridity are non-commercial; the 2026 terms ask for freely available or open-source materials) | L | M | Read the "solution materials" wording of the 2026 terms | Cite, use non-commercially, commit only derived values | Replace the layer (e.g., NASA POWER or MERRA-2) |
| 21 | Unsupported "NASA-approved" claims | L | H | Review | Claims policy | Edit copy |
| 22 | Event-rule non-compliance (pre-existing code, licence, AI disclosure, deadline) | L | H | Read the 28 Oct pages and submission guide | OSI licence, cite everything, disclose AI use, submit early | Fix and resubmit before the deadline |
| 23 | Support-area mismatch between targets and Earth cells biases relief and P90 | M | H | Recompute one target at two ROI radii | Area-matched tessellation (Part 5) | Report the sensitivity |
| 24 | Validation dominated by the gate (inflated AUC) | H | M | Compare against gate-only baseline | Gate-aware percentile and AUC; report both | State the limitation |
| 25 | MOLA interpolation artifacts distort Mars roughness | M | M | Compare with published MOLA slope statistics | Robust statistics; wider tolerance on Mars T3 | Down-weight T3 for Mars profiles |
| 26 | Crowded field: similar public entries exist | H | M | Check public repos and the 28 Oct statements | Differentiate on rigor, datasheets, stability | Demo emphasis |

---

## PART 32: Do NOT build

- Image-to-LLM "looks like Mars" classifier.
- CNN on HiRISE/CTX/CRISM imagery (huge data, no labels).
- Global high-resolution (<100 m) processing.
- Kubernetes, microservices, vector DB, mandatory RAG.
- A 3D Cesium globe as a core dependency.
- A "probability Mars-like" output.
- Live NASA API calls during the demo.
- Autonomous LLM agents with tool use.
- Mineralogy matching with M3/CRISM at global scale.
- Supervised learning on ~10–15 labels.
- A coarse (≥ 0.5°) grid with regional-gradient "slope" as the terrain feature.

---


## PART 33: Judge review (honest, pre-validation)

Self-assessed, not a prediction. Scores are out of 10.

| Criterion | Score | Criterion | Score |
|---|---|---|---|
| NASA relevance | 9 | Validation | 7 (9 if done well) |
| Scientific depth | 8 | Feasibility | 7 |
| Innovation | 7 | Originality | 7 |
| NASA data usage | 8 | Storytelling | 8 |
| Technical implementation | 8 | UX | 8 |
| AI usefulness | 6 | Visual impact | 8 |

Average: 91 / 12 ≈ **7.6** pre-validation, and ≈ 7.8 if Validation reaches 9.

**Mapping to the five official criteria (CHECKED for 2024; VERIFY for 2026):** Impact ← NASA relevance, feasibility. Creativity ← innovation, originality. Validity ← scientific depth, validation. Relevance ← NASA relevance, NASA data usage. Presentation ← storytelling, UX, visual impact. AI usefulness and technical implementation support all five.

**10 reasons to lose:**

1. Known analogs rank poorly and no explanation exists.
2. Thermal/aridity proxies attacked.
3. Weights seen as arbitrary.
4. Results look like "just deserts and poles."
5. Too much data prep, so an unfinished demo.
6. Lunar results feel weak since Earth cannot match polar lighting.
7. LLM seen as decoration.
8. The UI is cluttered.
9. The circular-validation criticism lands, or the AUC is shown to be mostly the barren-ground gate.
10. "Novel" candidates turn out to be already known sites.

**10 reasons to win:**

1. Matched-scale methodology (baseline *and* support area).
2. Mission profiles with live reweighting.
3. Separate operational axis.
4. Validation with hard negatives, baselines and intervals.
5. Honest confidence, including a stated proxy ceiling.
6. Reproducible datasheets for "characterize."
7. A grounded, validated LLM with fallback.
8. Works fully offline at ₹0.
9. Clear separation of direct vs proxy.
10. A strong, clean demo narrative.

**Highest-ROI changes:**

1. Validation figure on the first slide.
2. Weight-stability visual.
3. A datasheet export per candidate.
4. Feature-space (PCA) plot with targets.
5. Lava-tube overlay if time remains.

---

## PART 34: 3-minute demo

1. **0:00–0:15 Challenge and hook:** "Analog sites aren't well characterized; we quantify them. Our validation: *N of M* known analogs land in the top *X%*, and hard negatives do not." (Fill in the real numbers.)
2. **0:15–0:35** Pick **Lunar South Pole base → Connecting Ridge / Shackleton region**.
3. **0:35–1:00** Map lights up; the ranking panel shows scores, confidence, coverage and proxy share.
4. **1:00–1:30** Click the top candidate: feature bars, Earth vs target, proxy badges, nearest known analog.
5. **1:30–1:50** "Why ranked high?" shows the grounded explanation (note the evidence links).
6. **1:50–2:15** Move sliders (ice potential ↓, roughness ↑) → ranking re-sorts and the proxy-share badge updates.
7. **2:15–2:35** Show a **novel candidate** (not in the registry, >200 km from known analogs, prior-use check recorded) and its stability plot.
8. **2:35–2:50** Validation panel: known analogs in the top percentile, hard negatives low, and one honest failure.
9. **2:50–3:00** Impact statement: a reproducible, open-data shortlist for analog fieldwork. State what the score does *not* claim.

**Rules for the demo:** rehearse three times with a timer; keep the fallback video ready (Part 23); host the video or slides at a public link, because the Space Apps site does not take uploads. **VERIFY** the official demo length or format limits, which may differ from 3 minutes.

---

## PART 35: Innovation scorecard

| Feature | Scientific value | Judge impact | Difficulty | Cost | Priority |
|---|---|---|---|---|---|
| Live profile reweighting | M | High | Low | ₹0 | **Build** |
| Weight-stability (Dirichlet) visual | High | High | Low | ₹0 | **Build** |
| Analog datasheet export | High | High | Low | ₹0 | **Build** |
| Validation vs baselines with hard negatives and intervals | High | High | Low | ₹0 | **Build** |
| Pre-registered config + change log | High | M | Low | ₹0 | **Build** |
| Feature-space PCA plot | M | M | Low | ₹0 | Should |
| Operational accessibility axis | M | M | Low | ₹0 | Should |
| Nearest-known-analog finder | M | M | Low | ₹0 | Should |
| Lava-tube/pit overlay | M | M | Med | ₹0 | Advanced |
| Stage-2 30 m refinement | M | M | Med | ₹0 | Advanced |
| Local RAG over NASA docs | Low | M | Med | ₹0 | Cut |
| 3D globe | Low | M | High | ₹0 | Cut |

**Best 3:** live reweighting, weight-stability visual, analog datasheet export.

---

## PART 36: Final architecture decision

**FINAL STACK**

- **Frontend:** React + Vite + MapLibre GL JS
- **Backend:** FastAPI (optional; static mode works without it)
- **Database:** DuckDB + Parquet (PostGIS schema documented as an optional alternative)
- **GIS:** rasterio/GDAL, GeoPandas, H3
- **Scientific engine:** NumPy/SciPy tolerance-kernel similarity (pure Python module)
- **ML:** PCA + k-means (supporting only)
- **LLM:** local Ollama model or cached subscription-generated text; template fallback
- **Data:** the Must-tier datasets above
- **Storage:** local disk, exports in repo
- **Licence:** OSI-approved (e.g., MIT or Apache-2.0)
- **Deployment:** local primary; static host backup

```text
        RAW OPEN DATA (GEBCO, LOLA, MOLA, WorldClim, MODIS, GLiM)
                         │
                   [Ingestion scripts]
                         │
         [Preprocessing: tile-wise, matched ~0.5 km baseline, equal support area]
                         │
        [Feature extraction → H3 cells + target ROI vectors]
                         │
   ┌─────────────────────┴─────────────────────┐
   │ SCIENTIFIC ENGINE: kernel similarity,     │
   │ gating, confidence, stability, diversity  │
   └─────────────────────┬─────────────────────┘
                         │
          Parquet / DuckDB + static exports
                         │
                 FastAPI (optional)  ──→ static JSON mode
                         │
              React + MapLibre frontend
                         │
        Evidence JSON → template / LLM explanation → validator
```

---

## PART 37: Final data flow

```text
RAW OPEN DATA → INGESTION → PREPROCESSING (scale-matched: metric baseline, equal support area, masks)
→ FEATURE EXTRACTION → PLANETARY REFERENCE VECTOR (area-matched cells) + EARTH CELL VECTORS
→ TOLERANCE-KERNEL NORMALIZATION (absolute / relative-regime)
→ SIMILARITY ENGINE (family caps, gate) → PER-CELL SENSITIVITY (stability, confidence)
→ RANKING + DIVERSITY → GIS → EVIDENCE JSON → TEMPLATE / LLM EXPLANATION → VALIDATOR → UI

OFFLINE GATE (reads the same outputs; never feeds back into the weights):
VALIDATION HARNESS (positives, hard negatives, baselines, bootstrap intervals)
```

Change from the original draft flow: per-cell sensitivity sits *inside* the engine loop, so every result carries its stability. The validation harness is a separate offline gate on the same outputs and is never used to tune weights.

---

## PART 38: Acceptance criteria

- All Must datasets load, pass checksum, and have version and DOI recorded.
- Features exist for ≥ 95% of unmasked land cells (coverage report), with cross-body slope histograms and a spot check against published values.
- Each of ≥ 3 profiles and ≥ 5 targets produces a ranking, and every target vector is area-matched (`n_cells` ≥ 7).
- Validation report: median positive percentile among gate-passing cells ≥ 90 (stretch ≥ 95), AUC ≥ 0.8, and hard negatives below the 50th percentile, with baselines and 95% bootstrap intervals. If missed, document why.
- The config was tagged before the first validation run, and every later change is logged.
- Weight perturbation produces stability values for every candidate (default weights).
- Map shows candidates; sliders re-rank in < 300 ms; the JS scorer matches the Python engine to ±1 point (parity test).
- Every displayed score shows confidence, coverage, proxy share and proxy flags, and the claims banner is visible on every screen.
- Every LLM sentence passes the number/field/banned-phrase validator; the template fallback works with the LLM disabled.
- The app runs offline (network disabled) from a clean checkout in < 10 minutes.
- The submission package is complete: public demo link, README, OSI licence, AI disclosure, NASA and partner data list, citations.
- Every **VERIFY** item is resolved, or listed as open in `docs/DATA_SOURCES.md`.
- Total required external cost is ₹0.

*(The 90 / 0.8 thresholds are **HEURISTIC** targets, not published standards.)*

---

## PART 39: Scientific claims policy

**Allowed:**

- "high-scoring candidate analog under profile X"
- "strong similarity across the selected, available variables"
- "candidate not previously in our registry (prior-use check: <result, date>)"

**Not allowed:**

- "scientifically proven Mars/Moon equivalent"
- "NASA-approved/recommended site"
- "guaranteed habitat location"
- "probability of being Mars-like"
- any claim of equivalence for radiation, gravity, vacuum or atmosphere

**Always state:**

- The score is a transparent index.
- Proxies are flagged, and the proxy share is shown.
- Validation is limited by the small analog list and potential circularity.
- Coarse (~0.5 km, ~16 km-cell) data cannot replace field surveys.

**Branding.** Say the project is not affiliated with or endorsed by NASA, and do not use NASA logos or insignia (**VERIFY** NASA's media-usage guidelines). The persistent banner text is in Part 16.

---

## PART 40: Executive blueprint

1. **Overview:** AnalogAtlas, a validated, open-data tool to find and characterize Earth analogs for Moon/Mars missions.
2. **Hypothesis:** scale-matched terrain, surface and environmental features combined under mission-specific weights can recover known analogs and surface defensible new candidates.
3. **Exact MVP:** the Must-tier features and masks, ≥ 3 profiles, ≥ 5 targets, ranked map, datasheets, live sliders, confidence, validation page, submission package.
4. **Architecture:** offline Python engine → Parquet/DuckDB + static exports → optional FastAPI → React/MapLibre → validated explanations.
5. **Stack:** as in Part 36.
6. **Datasets:** GEBCO, LOLA LDEM_64, MOLA 128 ppd, WorldClim, Aridity Index, MOD44B, Natural Earth masks (+ GLiM, MCD43, WDPA as Should; Copernicus GLO-30 as the non-NASA agency dataset).
7. **Method:** tolerance-kernel weighted similarity with family caps, critical-feature gating and relative-regime handling for environment.
8. **Validation:** positives vs hard negatives and baselines, percentile/AUC/top-k with bootstrap intervals, Dirichlet stability, ablation, missing-data and scale tests, pre-registered config.
9. **AI:** deterministic engine; LLM explains validated JSON; template fallback; no RAG in the MVP.
10. **Database:** DuckDB/Parquet (Part 18 schema).
11. **API:** Part 19.
12. **Repo:** Part 20.
13. **Team:** Part 29.
14. **48-hour plan:** Part 28 (event 14–15 Nov 2026, with pre-event preparation in Part 26).
15. **Backlog:** Part 30.
16. **Risks:** Part 31.
17. **Cost audit:** below.
18. **Judge score:** ≈ 7.6 / 10 self-assessed average pre-validation; ≈ 7.8 if validation reaches 9.
19. **Demo:** Part 34.
20. **Decision:** **Build** the engine, validation, sliders, datasheets and fallback. **Don't build** imagery ML, RAG, 3D globe, or hosted-backend dependence.

---

## FINAL COST AUDIT

| Resource | Purpose | Cost | Required Account? | Usage Limitation | Primary/Backup | Approved? |
|---|---|---|---|---|---|---|
| GEBCO, WorldClim, Aridity, GLiM, Natural Earth | Earth data | ₹0 | No | Cite licences; WorldClim and Aridity are non-commercial; GEBCO needs acknowledgement | Primary | ✅ |
| NASA PDS (LOLA, MOLA, Diviner) | Moon/Mars data | ₹0 | No | Large files | Primary | ✅ |
| NASA Earthdata (MODIS) | Bare ground, albedo | ₹0 | Free login (no billing) | Login friction | Primary (fallback layer exists) | ✅ |
| WDPA | Protected areas | ₹0 | Accept terms | Do not redistribute raw polygons | Optional | ✅ |
| Copernicus GLO-30 (AWS open data) | Stage 2 context; non-NASA agency data | ₹0 | No | Large files | Optional | ✅ |
| Python OSS stack, H3, DuckDB | Engine | ₹0 | No | None | Primary | ✅ |
| React, Vite, MapLibre | Frontend | ₹0 | No | None | Primary | ✅ |
| Local laptop | Demo hosting | ₹0 | No | None | **Primary** | ✅ |
| GitHub (repo, Pages) / free static host | Public repo; backup demo | ₹0 | Free account | Size limits (**VERIFY**) | Backup | ✅ |
| Public video or slides link | Required Project Demo | ₹0 | Free account | Must be publicly viewable | Primary | ✅ |
| Ollama + local model | LLM | ₹0 | No | Needs RAM | Optional | ✅ |
| Existing LLM subscription (web UI) | Pre-generate cached text | ₹0 extra | Existing | Manual | Optional | ✅ |
| Internet bandwidth for ~15 GB of downloads | Data acquisition | ₹0 external | No | May exhaust a capped plan, so download early | Primary | ⚠️ plan ahead |
| Free CPU backend hosting | Optional | ₹0 | Possibly | Sleeps/quotas (**VERIFY**) | Optional, never required | ⚠️ not relied on |
| ERA5/CDS | Climate | ₹0 | Account | Unneeded | Not used | ❌ (unnecessary) |

**Total required external cost: ₹0** (your own internet plan aside).

---

## FINAL TECHNICAL SANITY CHECK

1. **Four students can build it?** Yes, if the LLM and the Should-tier items are cut-able. Validation is never cut.
2. **Datasets acquirable?** Yes. Versions and several licences were CHECKED on 4 Oct 2026; exact URLs are still **VERIFY**.
3. **Genuinely free?** Yes; Earthdata and WDPA need free accounts or terms acceptance. WorldClim and Aridity are non-commercial, so check them against the 2026 terms (Risk 20).
4. **Laptop-processable?** Yes, tile-wise with mergeable histograms; raw data ~10–15 GB, so allow ≥ 30 GB free disk. 16 GB RAM is comfortable and 8 GB is feasible.
5. **Score explainable?** Yes, a per-feature kernel and weights, with the renormalize → cap → gate order written down (Part 9).
6. **Comparable?** Terrain yes, scale-matched in baseline and support area; environment only by relative regime (flagged).
7. **Proxy confusion?** Controlled via flags, the proxy-share badge, the confidence ceiling and the claims policy.
8. **Validatable?** Face validity only, with gate-aware baselines and hard negatives; honest about circularity.
9. **New candidates?** Yes, "novel to registry" only, after a prior-use check.
10. **LLM adds value?** Modest; it is explanatory, and the system works without it.
11. **Works without the LLM?** Yes.
12. **Works without cloud?** Yes.
13. **Too much data?** No: matched ~0.5 km, 10–15 GB.
14. **Too complicated?** The static mode keeps it small.
15. **Major claim challengeable?** Thermal/ice proxies; mitigated by labeling and the ablation.
16. **Unsupported "NASA approval"?** Banned by policy.
17. **Compelling demo?** Yes (Part 34).
18. **Meaningful NASA data?** MOLA, LOLA, Diviner, MODIS, PDS/USGS maps, plus ESA/EC Copernicus as non-NASA agency data.
19. **Differentiation?** Scale matching, validation rigor, profiles, stability, datasheets, in a crowded field (Risk 26).
20. **24-hour cuts:** the LLM, geology, albedo, comparison view, the PCA plot and the stability panel. Three profiles stay.

**One weakness I revised for:** the original instinct was absolute temperature matching, which would just reward Antarctica. The relative-regime mode fixes this but remains the most attackable part. Have P1 prepare a clear defense. **Draft three-sentence defense:** "We do not claim Earth reaches lunar or Martian temperatures. We ask which Earth places sit at the same *relative* position in Earth's distribution as the target does in its own body's, as one flagged proxy component (default weight 0.10–0.22 across the thermal features, settable to zero with a slider). Our ablation shows how the rankings change when the whole thermal family is removed."

---

### Before you start, verify

**Already checked on 4 Oct 2026 (re-confirm if a long time has passed):** event dates; challenge text (through search snippets only); judging criteria (2024 guide); 2026 terms (open-source content, cite every source); the mandatory Project Demo; GEBCO release and format; Aridity v3 details; MOD44B v061; the nine Artemis candidate regions and the south-pole Moon Base statement.

**Still open:**

- The full challenge statement and partner datasets (due 28 Oct), read by hand on the official page
- The 2026 judging guide wording, AI-disclosure rules, demo length and submission deadline
- Exact download URLs and sizes (including GEBCO 2026 vs 2025)
- Target coordinates, and the current Mars exploration-zone literature for the Arcadia target
- Licence texts (Aridity, WorldClim, WDPA, MCD) against the 2026 terms, and the rule on pre-existing code
- Typical albedo values, and published MOLA slope statistics for the Mars scale check
- Free-hosting limits

---

## Revision notes

**What changed from v1 to v2, and why.**

*Contradictions and errors fixed*

1. The family cap of 0.5 was exceeded by Profile C (Terrain 0.56) and Profile D (0.60). Families are now explicit (S1 joins Surface-climate), and C and D carry a documented 0.6 Terrain cap.
2. The confidence rule (per-site proxy share ≤ 0.4) made "High" unreachable for four of five profiles at default weights (proxy shares 0.54, 0.70, 0.44, 0.40, 0.60) and rewarded missing proxy data. It is now a proxy ceiling computed from the active weights. The example output now shows stability, and reference uncertainty is used.
3. Validation targets disagreed (median ≥ 95th in Part 10, ≥ 90 in Part 38). Now: pass at 90, stretch at 95.
4. The 24-hour cuts said "two profiles" while Parts 25, 26 and 38 require at least three.
5. The judge average was stated as 7.7; the table gives 91/12 = 7.6.
6. The sanity check said validation was cut-able, while Part 25 makes it a MUST.
7. `exports/` and `data/exports/` are now one path. "~20 labels" is now ~10–15. The target count (~8) now matches the 7 rows, and the empty "Limits" cells are filled.
8. Undefined labels are now defined: cost classes A/B/C, risk P/I, VERIFY, CHECKED.
9. Part 7 mixed up `τ_k` and `δ_k`. AHP-lite said four families; there are three. "Secrets: none" ignored Earthdata credentials. The API said 503 for an unavailable LLM and also said it is not an error. The DB sketch was labeled `sql` but is not DDL. Land cells were 0.6–0.7 M and are ≈ 0.59 M.

*Scientific and technical rigor added*

10. Reference ROIs now match the Earth cell *area* (H3 cannot be reused on the Moon or Mars), and relief is a robust P95 − P5.
11. The baseline is kept isotropic at high latitude; cells split across tiles use mergeable histograms; an ice mask is required because MOD44B counts ice as non-vegetated.
12. Validation is gate-aware (the barren-ground gate would otherwise inflate AUC), adds hard negatives, baseline comparisons, bootstrap intervals, a positive-cell rule, default targets per profile and a pre-registered config.
13. The kernel is written as ordered pseudo-code (renormalize → cap → gate), with critical features, ordinal aridity steps, Dirichlet α and the uint8 missing sentinel specified, plus a JS-vs-Python parity test.
14. Stage-2 30 m numbers are context only unless the target is re-derived at the same baseline. Novelty now needs a stability threshold, a prior-use check and a registry of at least 30 sites.
15. The LLM evidence card uses pre-formatted number strings, a banned-phrase check, plain-text rendering and an AI-use disclosure log.

*Facts updated (CHECKED 4 Oct 2026)*

16. Event dates, the six-week preparation window, the Project Demo requirement, the open-source and cite-every-source terms, and the judging criteria.
17. Nine current Artemis candidate regions, the shift of the first landing to Artemis IV or later, and NASA's statement that the Moon Base will be at the south pole.
18. GEBCO (2025 release and a 2026 release; global file is NetCDF; land from SRTM15+), Aridity v3/v3.1, MOD44B v061, and the note that other public repos already tackle this challenge.

*Process and submission*

19. Added a pre-event window, a capacity check, early validation v0, checkpoints, four backlog items (DATA-0, SCI-8, QA-1, DOC-3) and five risks (22–26). The demo timing now puts validation up front, and the submission package is part of the MVP.

**Sources consulted on 4 Oct 2026.**

- 2026 NASA Space Apps registration and dates: https://astrobiology.com/2026/09/04/registration-is-now-open-for-the-2026-nasa-space-apps-challenge/
- Challenge page (search snippet only; the page blocks automated fetch): https://www.spaceappschallenge.org/2026/challenges/identify-earth-locations-that-analog-the-permanent-moon-base-locations-and-mars/
- Judging & Awards Guide: https://spaceappschallenge.org/resources/judging-awards-guide
- Project Submission Guide: https://www.spaceappschallenge.org/resources/project-submission-guide/
- 2026 Participant Terms and Conditions: https://www.spaceappschallenge.org/legal/
- GEBCO_2025 grid: https://www.gebco.net/data-products-gridded-bathymetry-data/gebco2025-grid
- Aridity Index v3 paper: https://doi.org/10.1038/s41597-022-01493-1 and the Figshare record (DOI 10.6084/m9.figshare.7504448)
- MOD44B v061: https://www.earthdata.nasa.gov/data/catalog/lpcloud-mod44b-061
- Artemis candidate regions (Sky & Telescope), NASA Moon Base environment page: https://www.nasa.gov/moonbase-environment-visualization/
