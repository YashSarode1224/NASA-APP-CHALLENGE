# AnalogAtlas — Adversarial Review and Corrected Implementation Decision

**Review date:** 5 October 2026  
**Reviewed file:** `AnalogAtlas_Blueprint (1).md`  
**Verdict type:** independent red-team review, not an endorsement of the original blueprint.

## Evidence status

I checked the current NASA Space Apps 2026 site, its 2026 participant terms, NASA Moon Base and Artemis material, the NASA/USGS PDS product pages, GEBCO, WorldClim, Protected Planet, and NASA Earthdata product documentation on 5 October 2026. The 2026 challenge statement is published and says to use open Earth, Moon, and Mars data to identify and characterize new terrestrial analogs. The official event page gives 14–15 November 2026 and a submission window of 14 November 09:00 to 15 November 23:59 local time. The complete challenge resources are scheduled for 28 October, so any data requirement or partner-dataset list not yet published remains **CHECKED/VERIFY**, not settled.

The sources most relevant to corrections are the [2026 Space Apps event page](https://www.spaceappschallenge.org/2026/), [2026 Participant Terms](https://www.spaceappschallenge.org/legal/), [official challenge description](https://www.spaceappschallenge.org/2026/find-a-team/lunar-terra/), [NASA Moon Base overview](https://www.nasa.gov/reference/moonbase-about/), [NASA Artemis landing-region update](https://ntrs.nasa.gov/citations/20250011660), [GEBCO 2025 documentation](https://www.gebco.net/data-products-gridded-bathymetry-data/gebco2025-grid), [MOLA PDS documentation](https://pds-geosciences.wustl.edu/missions/mgs/megdr.html), [LOLA GDRDEM documentation](https://ode.rsl.wustl.edu/mars/pagehelp/Content/Missions_Instruments/LRO/LOLA/GDR/GDRDEM.htm), [WorldClim licensing](https://worldclim.org/about.html), and [Protected Planet licensing](https://www.protectedplanet.net/en/legal).

## A. Executive verdict

**Decision: MODIFY, then build a much smaller terrain-first product.**

The proposal is a credible concept but not yet a scientifically defensible MVP. A four-person student team can build a strong Space Apps submission for ₹0 external cost if it ships:

1. one lunar target and one Mars target;
2. three mission views at most;
3. a common, explicitly benchmarked terrain representation;
4. Earth gates and contextual environmental descriptors;
5. a transparent score with missing-data penalties;
6. a real validation table with honest failure cases;
7. a static offline map and datasheet.

The original plan should **not** score Earth aridity, WorldClim temperature, thermal amplitude, Earth ice potential, cross-sensor albedo, or a “mafic-volcanic fraction” as if they were commensurate planetary measurements. Those are useful evidence layers or operational context, but their current cross-body formulations are proxies with weak physical equivalence. The highest-risk phrase in the original is “relative-regime matching”: percentile position in two unrelated planetary distributions is not a physical analog relationship.

The final product should be called an **evidence-backed terrain analog index**, not a mission-site selector. It should answer: “Which Earth regions share the measured terrain morphology of this selected lunar or Martian reference region, and what contextual Earth conditions make them useful or unsuitable for a stated training use?” It must not answer: “This place is Moon-like,” “this is a suitable base,” or “NASA recommends this site.”

The original blueprint’s best decisions are retained: NASA PDS data, local-first operation, precomputation, explicit proxy labels, deterministic explanations, no deep learning, no claim of scientific novelty, and a reproducible datasheet. FastAPI, DuckDB at runtime, k-means, the LLM, most climate/resource features, global 0.5 km processing, and the elaborate confidence machinery are cut from the MVP.

## B. Critical issues — ranked

| Rank | Issue | Severity | Corrective decision |
|---|---|---:|---|
| 1 | Climate/thermal/aridity/ice variables are treated as cross-planet similarity features even though their measurements and physical regimes are different. | Critical | Remove them from the core similarity score. Keep them as Earth context, gates, or separately labelled operational evidence. |
| 2 | “~0.5 km baseline” is not what the stated Horn 3×3 implementation actually measures. A central difference across a 3×3 grid spans about two pixels, roughly 0.9–1.0 km at the cited nominal spacing. | Critical | Define the effective filter and derivative baseline mathematically; benchmark a common 1 km analysis scale, or use a one-pixel adjacent-slope estimator if a 0.5 km baseline is truly required. |
| 3 | Nominal grid spacing is mistaken for comparable effective resolution. GEBCO land is heterogeneous and largely derived from SRTM15+/other sources; MOLA is binned altimetry; LOLA is binned/interpolated altimetry. | Critical | Say “common nominal analysis scale,” include source-quality flags, and avoid trafficability claims. Use terrain morphology, not landing safety. |
| 4 | Missing-data renormalization can reward cells missing difficult proxy features. The family-cap redistribution can also make the score unintuitive. | High | Use fixed family weights, availability penalties, and no cross-family reallocation in the browser. |
| 5 | Validation is circular and the proposed AUC is based on unlabeled random “negatives.” The blueprint calls that conservative, but the bias direction is not guaranteed. | High | Use pre-registered leave-site-out rank recovery and hard-negative comparisons as primary evidence. Make AUC exploratory only. |
| 6 | The pre-event plan risks violating the 2026 local guidance that teams may not begin developing the intended competition solution before the event. | High | Before 14 November, only research, account setup, data-access tests, generic learning, and a blank scaffold. Do not develop the intended engine or exports. Recheck the official global guidance on 28 October. |
| 7 | WorldClim is free for academic/non-commercial use but does not permit unrestricted redistribution or commercial use. WDPA has stronger no-redistribution terms. Both are incorrectly treated as uncomplicated Class A resources. | High | Classify both as restricted Class B; omit WDPA from the core. Do not commit raw WorldClim or WDPA data. |
| 8 | The core dataset plan is too large and the 10–15 GB estimate is unproven, especially if several MOD44B years are downloaded. | High | Use targeted regional downloads and one frozen MOD44B year, or replace the bare-ground gate with a lighter, documented land-cover/vegetation product. Measure storage on the weakest laptop. |
| 9 | The proposed “novel candidate” thresholds are presentation heuristics, not evidence of novelty. A Google Scholar search cannot establish that a site is unused. | High | Use “new to this registry” and publish the registry, query date, and search scope. Do not present novelty as a scientific discovery. |
| 10 | FastAPI, runtime DuckDB, optional Ollama, k-means, PCA, five profiles, seven targets, and multiple optional layers compete with the only judge-critical path: data → score → explanation → validation. | High | Ship a static app with one export bundle and a deterministic template explainer. |

## C. Scientific corrections

### Cross-planet comparison

There are three different kinds of comparison and the blueprint must name them separately:

| Type | Defensible examples | Not defensible as currently written |
|---|---|---|
| Direct morphology | Elevation-derived slope, relief, and a defined roughness statistic at a common effective scale | Calling the resulting values “trafficability” or “landing safety” |
| Surface/context proxy | Earth bare-ground fraction, lithology label, aridity, permafrost, protected status | Treating the proxy as a lunar/Martian physical equivalent |
| Operational context | Earth access, permits, roads, field logistics, climate stress | Folding accessibility into analog similarity |

The Moon and Mars do not share Earth’s atmosphere, gravity, radiation environment, dust behavior, thermal boundary conditions, or hydrologic cycle. Terrain morphology is the strongest common denominator in this proposal. Every other feature must carry a `proxy` or `context` label and must not silently enter the headline score.

### Scale-matching replacement

The claim that all three native products “happen to align well” is too strong. MOLA 128 pixels/degree has a nominal latitude spacing near 463 m; LOLA LDEM_64 is documented at 473.8 m; GEBCO is on a 15-arcsecond grid, but its land values have heterogeneous source lineage and effective resolution. At high latitude, longitude spacing contracts. A 3×3 Horn derivative does not have a 0.5 km gradient baseline; its central difference is approximately two pixel spacings.

Use this replacement:

1. Choose a frozen analysis scale after a benchmark, preferably a **1 km effective terrain scale** for a laptop MVP.
2. Reproject each local DEM crop to a local metric CRS: UTM or an azimuthal/polar stereographic projection appropriate to the body and latitude. Do not repair high-latitude anisotropy by merely block-averaging columns in longitude.
3. Resample to a common grid spacing, preserving the DEM’s native uncertainty and recording the resampling kernel.
4. Compute slope with a documented finite-difference stencil and call the result “slope at the stated effective scale.” If a 3×3 Horn stencil is used, state its effective support and derivative baseline explicitly.
5. Report a source-quality flag and run a scale sensitivity test at one coarser setting. A 30 m Earth product is not a refinement of a 1 km lunar/Mars comparison unless the planetary reference is recomputed at the same scale.
6. For lunar polar targets, use the polar stereographic LOLA product. For Mars polar targets, use the documented polar MOLA product where available. For Earth polar areas, use an appropriate polar projection and source-quality flag.

Equal physical support area is a reasonable design choice, but matching an H3 resolution-5 average area is a **heuristic**, not a planetary law. Define the common support as “approximately 250 km²” and use equal-area tiles or a fixed-area zonal statistic. A 25 km-radius disc is approximately 1,963 km², so it contains about 7.8 such units; edge clipping, overlap, and small-sample quantiles must be specified. Do not claim that a target with seven cells has a stable P90 merely because the number is above seven.

### Feature audit

| Feature | Keep? | Scientific validity | Dataset validity | Proxy risk | Cost | Recommendation |
|---|---|---|---|---|---|---|
| Mean slope | Yes | Direct morphology if scale is fixed | GEBCO/MOLA/LOLA available | Medium: source resolution and vertical error | Medium | **KEEP IN MVP**, label as terrain morphology |
| Slope P90 | Yes, cautiously | Useful tail descriptor, but unstable in small/heterogeneous cells | Same DEM issue | Medium | Medium | **KEEP IN MVP** only with quantile/sample diagnostics |
| Roughness = σ(slope) | Modify | A reproducible statistic, not a universal roughness or trafficability measure | Available from DEM | High for rover claims | Low | **KEEP IN MVP** as “slope variability”; test one alternative |
| Relief P95−P5 | Yes | Defensible regional morphology statistic | Available from DEM | Medium | Low | **KEEP IN MVP** |
| Broadband albedo | No in core | Cross-sensor bands, photometry, atmosphere, illumination, and surface materials differ | Products exist | High | High | **MOVE TO SHOULD HAVE** as contextual evidence; do not score by default |
| Aridity | No in core | Earth AI/PET is not a Martian or lunar dryness measurement | WorldClim/Global AI available | Very high | Low-medium | **MOVE TO CONTEXT/GATE**, not analog similarity |
| Thermal level | No in core | Air climatology vs planetary surface temperature are not equivalent | WorldClim, Diviner/MCD products differ | Very high | High | **REMOVE FROM MVP SCORE** |
| Thermal amplitude | No in core | Diurnal/seasonal meanings differ fundamentally | Products differ | Very high | High | **REMOVE FROM MVP SCORE**; display only if a specialist interprets it |
| Mafic/volcanic fraction | No numeric score | Map legends, scale, unit definitions and mapping confidence differ | GLiM and planetary maps exist | High | Medium-high | **MOVE TO CONTEXT** as lithology tags |
| Ice potential | No numeric score | Earth permafrost/climate is not PSR ice or Mars subsurface hydrogen | Data are indirect and heterogeneous | Very high | High | **REMOVE FROM MVP SCORE**; retain target-specific resource evidence |
| Bare-ground gate | Yes, with better name | Earth land-cover gate, not a planetary analog variable | MOD44B exists; product resolution/version must be pinned | Medium | Medium-high | **KEEP IN MVP** as an eligibility mask, not a scored feature |
| Ice/water mask | Yes | Necessary to avoid calling ice sheets “bare ground” analogs | Natural Earth is coarse; use a documented mask | Medium | Low | **KEEP IN MVP**, validate edge cases |
| Urban mask | Yes | Reasonable operational exclusion, not science similarity | Natural Earth is coarse | Low-medium | Low | **KEEP IN MVP** if explicitly an operational filter |
| Accessibility | Yes, separate | Operational suitability, not analog similarity | Roads/protected-area data have restrictions | Low | Medium | **KEEP as separate axis**, not headline score |
| Protected areas | Optional | Relevant for field feasibility, not analogity | WDPA terms restrict redistribution | Low | Medium | **CUT from MVP**; use an external link or manually curated note |
| Cave information | Optional | Valuable mission context but an inventory, not a derived discovery | Curated lists are possible | Medium | Medium | **SHOULD HAVE/advanced overlay**, never claim discovered caves |
| Geology | Optional | Important, but current numeric fraction is weak | GLiM/USGS maps vary in scale and legend | High | Medium-high | **SHOULD HAVE** as categorical evidence |
| Mineralogy | No in MVP | Directly useful but patchy and hard to match | CRISM/M3/ASTER are not a global student-laptop stack | Very high | Very high | **REMOVE from MVP** |

### Thermal, aridity, albedo, ice, geology, and accessibility decisions

*Thermal:* The relative-percentile method is not a valid physical replacement for direct temperature matching. A percentile is a rank within a body-specific distribution; it does not preserve radiative balance, atmospheric pressure, thermal inertia, insolation, or diurnal cycling. Replace it with a separate “thermal stress context” panel. If the team wants one scored environmental variable, use an Earth-only operational score and clearly state that it is not part of cross-body similarity.

*Aridity:* Earth AI = precipitation/PET is meaningful for terrestrial water limitation. It is not the same thing as the absence of atmosphere or liquid water on the Moon/Mars. Use aridity to enforce “terrestrial dry field site” eligibility and to describe the Earth candidate; do not match it to a hyper-arid planetary reference.

*Albedo:* MCD43’s broadband/spectral products and lunar/Mars reflectance products are not automatically comparable. Photometric correction, viewing geometry, spectral response, atmosphere, soil, dust, and snow contamination matter. Use as a contextual chart or cut it.

*Ice:* Keep “resource evidence” separate from “terrain analog score.” A lunar candidate may be near a permanently shadowed region, while an Earth analog may be cold/permafrost; that supports training logistics or field instrumentation, not a claim that the Earth site analogs lunar ice.

*Geology:* A mapped “basic volcanic” fraction is not an equivalent mafic fraction across GLiM and planetary map legends. Use a categorical tag: basaltic/volcanic, sedimentary, mixed/unknown, with source and map scale. Do not let it dominate the score.

*Accessibility:* It should be a separate operational suitability axis and possibly a user-selected constraint. Keep the analog score scientific and the logistics score practical. Show both, never combine them into one “best site” without exposing the tradeoff.

## D. Dataset corrections

| Dataset | Current finding | Decision |
|---|---|---|
| GEBCO 2025 | Official documentation describes a global 15-arcsecond grid, a 4 GB NetCDF global file and about 7.5 GB uncompressed; land source lineage is heterogeneous and not simply “SRTM everywhere.” | **Use for coarse global terrain screening**, pin DOI/version, and do not claim uniform 463 m effective resolution. |
| MOLA MEGDR | PDS documents 4/16/32/64/128 pixels/degree and polar products; the archive was moved to a maintained PDS4 bundle on 25 August 2026. | **Use**, but update scripts to the maintained PDS4 bundle and keep counts/source metadata. |
| LOLA LDEM_64 | Official documentation gives 0.4738 km latitude pixel size; polar products use polar stereographic grids from 100 m down to 5 m. | **Use LDEM_64 globally and polar products for south-pole crops**, resampling to the frozen common scale. |
| WorldClim 2.1 | 1 km climate surfaces exist, but the official license allows academic and other non-commercial use and disallows unrestricted redistribution/commercial use. | **Class B**. Use only if the team accepts the restriction, never commit raw files, and keep it contextual. A NASA-only fallback may simplify the license story. |
| Global Aridity Index/PET v3 | The database and paper are available; current license/redistribution terms must be read from the exact Figshare release before publication. | **Class B until confirmed**; context/gate only. |
| MOD44B v061 | NASA Earthdata lists the current collection as MODIS/Terra Vegetation Continuous Fields Yearly 250 m SIN Grid V061; older technical material describes related VCF processing at 500 m, so the exact band/grid metadata must be read from the downloaded product. | **Use one pinned year only**, verify band and scale from the product metadata, and benchmark download volume. Do not claim a five-year global median in the MVP. |
| MCD43 | Current v061 products include 0.05-degree CMG and 30-arcsecond products, with QA requirements. | **Cut from core score**; if used, use QA-filtered context only. |
| Natural Earth | Appropriate for lightweight global masks and a static basemap, but not a high-resolution urban or glacier truth layer. | **Use for coarse display/masks**, label limitations. |
| GLiM | Useful global lithology context, not a directly equivalent planetary material fraction. | **Should-have categorical layer**. |
| WDPA/Protected Planet | Terms prohibit commercial use and redistribution, including redistribution through interactive maps, and require current-version attribution and a source link. | **Do not ship raw or downloadable derived WDPA data in the MVP**. Omit or use only a manually recorded external-link flag after a terms review. |
| Diviner | Useful for lunar thermal/rock-abundance context, but not an Earth-comparable thermal feature. | **Context/target evidence only**. |
| THEMIS/TES | Useful Mars thermal inertia/albedo context, but not an Earth equivalent without a carefully defined physical model. | **Advanced only**. |
| USGS planetary geology maps | Good target context if legends and map scale are preserved. | **Should-have categorical evidence**, not numeric cross-body fraction. |
| Copernicus GLO-30 | Free/open Copernicus data, but current access paths and user categories can change; the 2026 view service introduced registration requirements for some access. | **Optional targeted refinement**, never a core dependency. |
| JAXA/ISRO products | Potential partner-data value, but the exact product, license, coverage and download workflow are not pinned. | **Do not make these required before the 28 October resources are released.** |

The data-size claim is not proven. A global GEBCO file alone is multi-gigabyte; MOLA and LOLA global products are also large; several annual MOD44B downloads can dominate the estimate. The team must run a capacity script that records compressed size, uncompressed size, peak RAM, processing time and output size. The corrected MVP should process a bounded set of dry-land bands or a deliberately chosen continental study set rather than promise an immediate global scan.

## E. Scoring corrections

### Decision on the tolerance-kernel method

**MODIFY.** A Gaussian tolerance kernel is acceptable as a transparent similarity primitive, but the original aggregation is too permissive. The kernel should be a descriptive index, not a probability. Keep it for terrain features only, with tolerances frozen before validation.

Use:

```text
s_k = exp(-0.5 * ((x_k - target_k) / tau_k)^2)
```

where `tau_k` is a pre-registered tolerance plus a documented target heterogeneity term. Do not call target IQR divided by 1.349 “measurement uncertainty”; call it **target heterogeneity**.

Use fixed family weights, for example:

```text
terrain = 0.75
surface/context = 0.25
```

For the headline score, surface/context can be zero in the first build. Within a family, average available feature similarities but apply an explicit completeness penalty. Do not redistribute missing-feature weight into other families. A conservative form is:

```text
family_score = family_weight * mean(available_similarity) * fraction_of_family_weight_available
score = 100 * sum(family_score)
```

The app separately displays `coverage = available_weight / total_weight`. A missing value cannot improve the score. If the team prefers to renormalize for exploratory sliders, show both “raw score with missing penalty” and “available-feature agreement”; never use the latter as the only ranking.

Replace the `min(score, 50)` critical-feature gate. It introduces an arbitrary discontinuity and can hide why the score changed. Use hard eligibility gates only for non-comparable Earth cells—water, urban, permanent ice, or insufficient data. Let terrain mismatch lower the continuous score, and show a warning when slope or slope-tail similarity is below a pre-registered threshold.

Do not perform cross-body percentile matching for thermal, aridity, or ice. If sliders are kept, constrain them to documented ranges, retain a “defaults” reset, and label custom results **scenario rankings, not validated rankings**. The sliders have scientific value as sensitivity exploration, not as evidence that users can tune a correct mission score.

## F. Validation corrections

The original validation plan has good instincts but overstates what its data can establish.

### Problems

* Known analogs were selected partly because they resemble the same terrain/climate variables. This is face validity, not independent validation.
* A 1-ring “best of seven” rule can choose the most favorable cell after seeing the results and inflate recovery.
* Random gate-passing cells are unlabeled, not true negatives. AUC against them is exploratory and can be biased in either direction.
* Ten to fifteen positives cannot support precise bootstrap intervals. Resampling 1,000 times does not create more independent sites.
* Tuning tolerances, gates, or weights after inspecting positives invalidates the advertised test.
* “Below the 50th percentile” for hard negatives and “median ≥ 90th percentile” for positives are heuristics, not scientific pass standards.

### MINIMUM VALIDATION

1. Freeze the terrain feature definitions, target ROIs, tolerances and weights in a config hash before scoring.
2. Use 5–8 documented analog sites with a short citation and mission-use label. Do not mix geological analogs such as Rio Tinto into a terrain-only positive set; report them as out-of-scope or a separate qualitative category.
3. Use a fixed positive-cell rule: the cell containing the site centroid, plus a predeclared buffer only if the physical site is smaller than the analysis cell. Do not use “best of seven” as the primary result; show it as sensitivity.
4. Choose 3–5 hard negatives before running the score. Each must pass the Earth gates and have a written expected mismatch.
5. Report percentile rank, top-5% recovery, gate-only baseline, terrain-only baseline, and a table of false positives/false negatives.
6. Run leave-one-site-out sensitivity: the site being evaluated must not influence target choice, tolerance choice, or narrative claims.
7. Treat AUC as optional exploratory context. Do not set AUC ≥ 0.8 as an acceptance criterion.

### IDEAL VALIDATION

Add independently sourced sites, region-level spatial blocking, bootstrap at the **site** level with wide intervals, scale sensitivity, missing-data stress tests, rank correlation under bounded weight perturbations, and an ablation showing the result with contextual features removed. Pre-register the test and maintain a post-hoc change log. The ideal report should say “consistent with face validity under this registry” rather than “validated for mission use.”

The judge-facing validation figure should contain one rank plot, one baseline comparison, and one honest failure. This has more value than a polished AUC number with weak labels.

## G. AI corrections

The deterministic engine → evidence card → optional explainer architecture is sound, but the LLM is not a must-have. Exact-string number checks catch some hallucinations but fail on unit conversions, rounded paraphrases, negation, and unsupported qualitative claims. Banned-phrase detection is a secondary guard, not a scientific validator.

Final decision:

* **Keep:** deterministic template explanation generated directly from evidence JSON.
* **Optional:** an LLM that rewrites the template for readability, with output discarded on any schema, field, number, unit, or claim-policy failure.
* **Remove from MVP:** Ollama, RAG, live network inference, and pre-generated top-100 explanations.
* **Require:** an AI-use disclosure for any AI-assisted code/text that the team submits, consistent with the terms and the team’s own provenance log.

The app must work identically with the LLM disabled. AI is meaningful here only as a constrained communication aid: it translates computed evidence into plain language and never chooses features, weights, candidates, or scientific claims.

## H. Architecture corrections

The simplest reliable architecture is:

```text
Pinned source data
  → offline Python preprocessing
  → compact Parquet/JSON/GeoJSON exports
  → static React/MapLibre app
  → deterministic datasheet and explanation
```

Remove FastAPI from the required architecture. Remove PostGIS entirely. DuckDB may be used by the offline build scripts, but it is not a runtime dependency. Do not ship a microservice, Docker Compose stack, remote database, API calls during the demo, or a hosted LLM.

Use a self-contained basemap made from Natural Earth or another license-cleared local vector package. MapLibre is a renderer, not a basemap provider. Do not rely on commercial Mapbox tokens or public OSM tile servers during the demo. If an online backup is published, use a static host and disclose its availability is not required for the product.

The runtime package should contain only the top candidate polygons, a low-resolution global context layer, target locations, per-candidate evidence JSON, validation results, and the score slabs needed for the slider. A complete global cell-by-feature-by-target matrix is not automatically a problem—the 41 MB raw uint8 estimate is arithmetically plausible for 0.59 million cells × 10 features × 7 targets—but browser top-k selection, JSON overhead, geometry, and mobile/weak-laptop behavior still need a benchmark.

## I. Cost corrections

The ₹0 claim is achievable only if all required paths are local and no paid quota is needed. “Free” and “unrestricted” are not synonyms.

* Class A: NASA PDS, NASA Earthdata data access with a free account, GEBCO with attribution, Natural Earth, Python/Node open-source tooling, local laptop, and static local serving.
* Class B: WorldClim, Global Aridity Index until its exact license is confirmed, WDPA, Copernicus access paths that require registration, GitHub/static hosts requiring accounts, and any optional free hosted backend. These have restrictions or operational dependencies.
* Class C: paid APIs, required billing accounts, commercial basemaps, cloud storage/compute required for operation, paid LLM APIs, and any service whose free tier cannot support the demo. The corrected architecture uses none.

Internet data usage is a household/resource cost, not an external project charge, but it is still a practical risk. Do not promise “₹0” while requiring a credit card, trial, paid API key, or fragile free backend.

## J. Contradictions found

| Section | Contradiction or defect | Correct interpretation | Fix |
|---|---|---|---|
| Part 1 / Part 26 | Blueprint encourages extensive pre-event downloads and preparation, while 2026 event guidance says teams may not begin developing the intended competition solution before the event. | Data-access preparation may be allowed, but solution development is a rules question. | Do not pre-build the intended engine/exports; recheck official guidance on 28 October and retain a provenance log. |
| Part 3 / Part 7 | A 3×3 Horn kernel is described as a ~0.5 km baseline. | The central difference spans about two pixels; support and baseline differ. | State effective scale and benchmark it; default to 1 km effective terrain scale. |
| Part 3 / Part 7 | Native 15″, MOLA 128 ppd, and LOLA LDEM_64 are treated as equally resolved. | Nominal grid spacing is similar; effective resolution/source error is not. | Add source-quality metadata and weaken claims. |
| Part 3 / Part 5 | Equal H3 resolution-5 area is presented as the uniquely correct planetary support. | It is a reasonable heuristic support choice. | Call it a common ~250 km² analysis support and test sensitivity. |
| Part 4 / Part 9 | Family caps are said to control correlation, but family caps do not estimate correlation. | They are a heuristic weight constraint. | Rename “correlation handling” to “weight constraint”; use fixed family weights. |
| Part 9 / Part 12 | Missing-data renormalization is paired with confidence coverage, but missing proxy features can increase the available-feature score. | Agreement and evidence quality are conflated. | Apply missing penalties to the headline score; show coverage separately. |
| Part 9 | A score cap of 50 at `s < 0.2` is called a critical-feature gate. | It is an arbitrary discontinuous penalty, not an eligibility gate. | Use eligibility masks and continuous terrain mismatch warnings. |
| Parts 3, 4, 9 | Thermal, aridity and ice are marked proxies but still take substantial default weight. | Proxy labels do not make unlike measurements physically comparable. | Remove from core cross-body score. |
| Part 10 | AUC against random gate-passing cells is described as conservative. | Random cells are unlabeled and may contain valid analogs; bias is unknown. | Make AUC exploratory and prioritize blocked rank recovery. |
| Part 10 / Part 38 | Bootstrap intervals and hard thresholds suggest stronger statistical validation than the small registry supports. | The result is face-validity evidence. | Drop mandatory AUC/90th/0.8 targets; retain honest rank and baseline tests. |
| Part 11 | A 30-site registry is required for novelty, but the 48-hour plan also requires five targets, features, validation, UI and documentation. | Thirty-site curation is a separate research task. | Use 8–15 documented sites in MVP; call outputs new to this registry. |
| Part 11 / Part 34 | “Prior-use check passed” could be read as evidence a site is new. | A web search cannot establish absence. | Use “no prior use found within our stated search scope.” |
| Part 12 | “Reference uncertainty” is computed from target spread, but spread is not measurement uncertainty. | It is target heterogeneity. | Rename the component. |
| Part 12 / Part 19 | Stability is precomputed for defaults while sliders change ranking and confidence. | Custom ranking is not covered by the default stability result. | Label sliders exploratory and do not show default stability as custom confidence. |
| Part 13 / Part 32 | PCA/k-means are called MVP/supporting analytics while ML is otherwise cut. | They are not needed for the core result. | Remove k-means and make PCA optional after the vertical slice. |
| Part 15 / Part 23 | MapLibre is described as having a free basemap. | MapLibre is a renderer; tiles/style/glyphs are separate. | Package a local basemap and test with the network disabled. |
| Part 17 / Part 24 | FastAPI is optional, but local primary operation depends on `uvicorn`. | A static server is sufficient. | Remove FastAPI from the required build. |
| Part 18 | DuckDB is proposed as runtime storage while Part 23 says static offline exports are the demo path. | DuckDB is build-time only. | Move DuckDB to preprocessing and ship static exports. |
| Part 6 / Cost audit | WorldClim is listed as Class A even though official terms restrict redistribution and commercial use. | It is restricted Class B. | Do not commit raw data; keep it contextual or replace it. |
| Part 6 / Cost audit | WDPA is listed as optional approved while its terms prohibit redistribution through interactive maps. | It is legally awkward for a downloadable/static app. | Omit from MVP. |
| Part 6 | MOD44B is described as 250 m in one place and related VCF documentation uses 500 m. | Exact current product metadata must govern. | Pin the downloaded product’s grid/resolution and use a single year. |
| Part 1 / Part 5 | Current Artemis information is mixed with Moon Base representation and an older 2022 candidate list. | Nine updated Artemis III regions and Connecting Ridge are different reference concepts. | Label each as Artemis candidate, Moon Base representative, or historical Apollo/rover target. |
| Part 38 | “Clean checkout offline in <10 minutes” includes large data processing in some wording. | A clean demo checkout should use precomputed exports; raw preprocessing can be much longer. | Split demo startup and data-build benchmarks. |

## K. Overengineering to remove

### CUT

* Global processing of every proposed optional dataset.
* Cross-planet thermal, aridity, albedo and ice similarity.
* FastAPI, PostGIS, Docker Compose, runtime DuckDB, and hosted backend.
* k-means cluster naming, Isolation Forest, Mahalanobis distance, RAG, and deep learning.
* Five mission profiles and seven planetary targets in the first vertical slice.
* A 30-site novelty registry as a hard acceptance criterion.
* PDF generation, 3D globe, live NASA APIs, live LLM calls, and full global heatmap geometry.

### OPTIONAL

* A single categorical geology tag.
* One QA-filtered albedo context chart.
* PCA after the score and validation work.
* A manually curated cave/pit overlay.
* A separate operational-accessibility panel.
* One targeted 30 m Earth refinement shown explicitly as “not scored.”

### MUST KEEP

* NASA PDS terrain data and source citations.
* A common metric analysis scale with a reproducible method.
* Earth eligibility masks.
* A transparent terrain score with per-feature evidence.
* Missing-data penalties and coverage reporting.
* At least one real positive and one hard negative validation comparison.
* Offline static operation.
* Deterministic explanation and a claims banner.
* A candidate datasheet and a short methods/limitations page.

## L. First vertical slice

Build this before adding any second-order feature:

1. **One lunar target:** Connecting Ridge/Shackleton region, explicitly labelled as a representative lunar south-pole target rather than a final NASA base site.
2. **One mission view:** lunar rover/EVA terrain analog.
3. **Three scored features:** slope summary, slope-tail summary, and relief/roughness at one frozen effective scale.
4. **Three Earth gates:** land, non-urban, sufficiently non-vegetated/dry; all gates shown as operational filters, not planetary physics.
5. **One compact Earth study set:** a preselected set of dry volcanic/polar/desert regions large enough to demonstrate discovery, processed using the same code as the final run.
6. **One deterministic score:** fixed terrain weights, tolerance config, missing-data penalty, and per-feature similarities.
7. **Five known/negative locations:** at least three documented analog positives and two gate-passing hard negatives, all frozen before the validation run.
8. **One map:** candidate polygons/hexes, target marker, score legend and no external tile dependency.
9. **One datasheet:** Earth value, target value, similarity, source, proxy/context label, coverage, and limitations.
10. **One validation panel:** positive ranks, hard-negative ranks, terrain-only baseline, and one failure.

The vertical slice is complete only when a user can select the target, see the ranked Earth cells, open a datasheet, understand why the winner ranked highly, and inspect a failure without network access.

## M. Corrected MVP

The corrected MVP has two bodies, two targets, one terrain-first score, three mission views at most, and no required LLM.

**Scored:** mean/median slope, slope P90 or a clearly defined slope-tail statistic, local relief, and slope variability. Use only features that survive the common-scale benchmark.

**Context/gates:** bare-ground/vegetation, water/ice, urban, Earth aridity, surface temperature context, geology tag, access notes. They are visible and can be filters, but not silently mixed into the analog score.

**Outputs:** top 20 candidates per target/profile, per-site datasheet, feature bar chart, score decomposition, coverage/evidence-quality badge, validation page, claims banner, local basemap, static exports, README, source registry, and AI disclosure.

**Profiles:** default terrain analog, lunar rover/EVA terrain, Mars rover terrain. The profile names are use cases, not NASA mission requirements. A base-siting profile can be added only if its resource/illumination inputs are present and clearly separated from terrain similarity.

## N. Corrected final architecture

### FINAL ARCHITECTURE

Offline, single-repository, build-time Python pipeline producing static frontend exports.

### FINAL DATASETS

GEBCO 2025 for bounded Earth terrain screening; MOLA MEGDR PDS4 for Mars; LOLA LDEM_64 plus polar LOLA crop for the lunar target; Natural Earth for lightweight masks/basemap; one pinned NASA Earthdata vegetation/bare-ground product only if the capacity and metadata checks pass. WorldClim/Aridity/GLiM are optional, restricted/contextual, and not required for the vertical slice.

### FINAL SCIENTIFIC FEATURES

Terrain morphology at one common metric scale: slope, slope-tail, relief, slope variability. Contextual evidence: vegetation/bare ground, aridity, geology, thermal/illumination/resource notes. No cross-body temperature, aridity, albedo, ice or mineralogy score in MVP.

### FINAL SCORING METHOD

Tolerance-kernel terrain similarities with fixed weights, explicit missing-data penalties, eligibility masks, no family redistribution, and no arbitrary score cap. Custom weights are scenario exploration. Default validation is the only one called validated/assessed.

### FINAL VALIDATION

Pre-registered positive/hard-negative set, site-level ranks, terrain-only and gate-only baselines, fixed cell rule, false-positive/false-negative review, and scale/missing-data sensitivity. AUC is optional and clearly exploratory.

### FINAL AI ROLE

Template explanation is primary. Optional LLM rewrites validated evidence only and is disabled by default. It cannot score, select, cite new sources, or make mission claims.

### FINAL FRONTEND

React + Vite + MapLibre GL JS, with local Natural Earth-style basemap and packaged glyphs/sprites if needed. GeoJSON only for the top candidate set; no live tile dependency.

### FINAL BACKEND

None required at runtime. A local static server is enough. Python build scripts are the backend in the reproducibility sense; FastAPI is not required.

### FINAL STORAGE

Raw data and intermediate rasters gitignored; build metadata and checksums tracked; compact Parquet/JSON/GeoJSON exports committed only when licenses permit. No raw WDPA or restricted WorldClim data in the repository.

### FINAL DEPLOYMENT

Primary: offline local static server. Backup: a static host if the team wants a public URL and the host’s terms are checked. Recorded demo is the last-resort artifact, not the product’s runtime dependency.

### FINAL ₹0 COST

No paid API, cloud, commercial basemap, paid LLM, billing account, required hosted backend, or required cloud storage. Free accounts may be needed for NASA Earthdata and a public static host, but they are not runtime dependencies.

## O. Corrected dataset stack

### Required for the first slice

* MOLA MEGDR PDS4 terrain crop around the selected Mars target.
* LOLA LDEM_64 and an appropriate polar LOLA product for the lunar target.
* GEBCO or a bounded Earth DEM study set, pinned by DOI/version.
* Natural Earth land/coastline and coarse ice/urban display masks.
* A small, hand-curated registry of analog sites with citations.

### Conditional

* MOD44B v061, one frozen year, if the product metadata and download size pass.
* WorldClim or Global AI/PET for contextual Earth descriptions only, with restrictions documented.
* GLiM or USGS lithology tags after terrain scoring works.
* Copernicus GLO-30 only for a few finalists and only as unscored context.

### Excluded from MVP

MCD43 as a scored feature, Diviner/TES as cross-body temperature features, Earth permafrost versus lunar/Mars ice matching, CRISM/M3/ASTER global mineralogy, raw WDPA, full LROC/HiRISE/CTX imagery, and any partner product whose current terms or access path are not pinned.

## P. Corrected 48-hour plan

The 48-hour event plan assumes no intended solution code or computed result was prepared beforehand. Before the event, the team may learn the tools, read the challenge, establish accounts, check available disk, and document a blank repository/provenance plan only as permitted by the official rules. Do not rely on a prebuilt six-week implementation without explicit confirmation.

| Event time | Deliverable | Cut rule |
|---:|---|---|
| 0–3 h | Confirm challenge/resources, freeze one target, one profile, source registry, JSON contract and claims policy | If data access fails, use the pre-approved small study set |
| 3–10 h | Load two terrain products and one bounded Earth DEM; compute one common-scale terrain feature | If global processing fails, stay regional |
| 10–15 h | Build target vector, Earth cell features, gates and deterministic score | No climate/geology/LLM yet |
| 15–20 h | Build validation set and run baseline/false-positive checks | Do not tune weights after seeing ranks |
| 20–28 h | Export top candidates, datasheets and validation JSON | Static exports beat API work |
| 28–35 h | React/MapLibre map, ranking, detail drawer and local basemap | Use points if polygon performance fails |
| 35–39 h | JS/Python parity, missing-data tests, clean offline run | Fix correctness before polish |
| 39–43 h | Add second target/profile only if the first slice is stable | Otherwise polish first slice |
| 43–46 h | Record a short demo and assemble README/source/AI disclosure | Never invent validation numbers |
| 46–48 h | Rehearse, submit with buffer, save source manifest and final commit | Submission is final; reserve time |

### Pre-event preparation that is safe only after rules confirmation

Create accounts, confirm storage/bandwidth, read licenses, learn raster reprojection, test a generic MapLibre sample, and prepare an empty repository template. Do not download a complete intended solution result, tune AnalogAtlas weights, precompute final exports, or write the competition-specific engine if the official rules prohibit pre-development.

## Q. Change log from Claude’s blueprint

| Original decision | Keep/Modify/Remove | Reason | Replacement |
|---|---|---|---|
| Open-data Earth/Moon/Mars atlas | Keep | Directly answers the challenge | Terrain-first evidence atlas |
| GEBCO + MOLA + LOLA | Modify | Good access, unequal effective resolution | Pin versions; bounded processing; source-quality flags |
| Common ~0.5 km baseline | Modify | Stated stencil does not have that baseline | Benchmark and freeze a common metric effective scale, default 1 km |
| Area-matched planetary cells | Modify | Reasonable but heuristic and small-N sensitive | Common ~250 km² support, equal-area tiling, sensitivity |
| Slope/relief/roughness core | Keep/modify | Strongest comparable variables | Keep with scale and interpretation caveats |
| Aridity as scored feature | Remove from core | Earth AI/PET is not planetary dryness | Earth context/gate only |
| Thermal level/amplitude as percentile features | Remove from core | Percentiles do not create physical comparability | Context panel or omit |
| Albedo as scored cross-sensor feature | Move | Sensor/photometric mismatch | Optional context only |
| Ice potential as scored proxy | Remove from core | Earth permafrost, lunar PSR, Mars H are different | Separate resource evidence |
| Mafic-volcanic fraction | Move | Map legend/scale mismatch | Categorical geology tag |
| Accessibility separate axis | Keep | Correct conceptual separation | Separate operational suitability panel |
| Family caps with redistribution | Modify | Not genuine correlation handling; can be unintuitive | Fixed family weights and missing penalties |
| Gaussian tolerance kernel | Keep/modify | Transparent and easy to explain | Terrain-only, pre-registered tolerances |
| Critical feature score cap at 50 | Remove | Arbitrary discontinuity | Eligibility gates plus continuous mismatch warnings |
| Live sliders | Keep with warning | Useful scenario exploration | Default profile remains reference; custom output unvalidated |
| Known positives/hard negatives | Keep/modify | Good idea, but circular/unlabeled | Site-level rank validation and written controls |
| ROC-AUC as acceptance target | Remove as requirement | Too few and unlabeled negatives | Exploratory metric only |
| Bootstrap intervals with 10–15 sites | Modify | Intervals will be wide and unstable | Site-level intervals, report uncertainty honestly |
| “Novel” = top 1%, >200 km, stability ≥0.8 | Modify | Heuristics cannot establish novelty | “New to our registry under stated search scope” |
| Confidence High/Medium/Low | Modify | Sounds probabilistic; target spread is not uncertainty | “Evidence quality” with completeness/robustness components |
| PCA | Optional | Judge-visible but not core | Add only after first slice |
| k-means/Isolation Forest | Remove | No judge-critical value; unlabeled semantics | Geographic diversity NMS only |
| LLM explainer | Modify | Useful only as constrained prose | Template first; optional offline rewrite |
| RAG/Ollama | Remove from MVP | Hardware and setup risk | No runtime LLM dependency |
| React/Vite/MapLibre | Keep | Good static frontend choice | Package local basemap/assets |
| FastAPI | Remove from final architecture | Static export covers demo | Local static server only |
| DuckDB | Modify | Good build-time tool, not necessary at runtime | Build-time only or Parquet scripts |
| PostGIS/microservices/Docker | Remove | Unnecessary setup and failure modes | Single repo, single build pipeline |
| GitHub/static host backup | Keep cautiously | Useful public link | Optional; no dependency and terms checked |
| 10–15 GB and <10-minute estimates | Modify | Not benchmarked and likely optimistic with multiple MODIS years | Capacity benchmark; separate build-time/demo-time budgets |
| Six-week pre-event code/data preparation | Modify | May conflict with event rules | Research/setup only until rules are confirmed |

## R. Final ₹0 audit

| Resource | Required? | Class | Decision |
|---|---:|---:|---|
| NASA PDS MOLA/LOLA | Yes | A | Use locally with citation |
| GEBCO | Yes/conditional | A | Use bounded/pinned data with attribution |
| NASA Earthdata account | Conditional | B | Use only if MOD44B passes capacity check |
| MOD44B | Conditional | B | One pinned year; no runtime network |
| WorldClim | No | B | Context only; no raw redistribution |
| Global AI/PET | No | B until license confirmed | Context only or omit |
| Natural Earth | Yes | A | Basemap/coarse masks |
| GLiM/USGS maps | No | A/B by exact terms | Optional categorical context |
| WDPA | No | B/restricted | Omit from MVP |
| Copernicus GLO-30 | No | A/B access-dependent | Targeted unscored refinement only |
| Python, NumPy, rasterio/GDAL, Parquet, React, Vite, MapLibre | Yes | A | Pin versions; local install |
| Map tiles | No external service | A if locally packaged | Use Natural Earth/local assets; no commercial tiles |
| FastAPI/PostGIS/Docker | No | — | Removed |
| LLM API/Ollama | No | C risk if hosted/billed | Removed from required path |
| Cloud compute/storage/database | No | C if required | Removed |
| GitHub/static host | Optional | B | Backup only; local demo remains complete |
| Laptop/internet | Yes | Personal resource | No external project charge, but capacity/bandwidth risk |

**Required external cash cost: ₹0**, provided the team uses its existing laptop/internet and no paid service is made mandatory. The project’s legal/open-source compliance still requires preserving third-party terms; an MIT/Apache license on the code does not relicense restricted datasets.

## S. NASA judge score — before vs after

These are strict review estimates, not predictions and not official NASA scores.

| Dimension | Original blueprint | Corrected MVP | Reason for corrected score |
|---|---:|---:|---|
| NASA relevance | 8.5 | 8.5 | Strong direct response to analog characterization |
| Scientific validity | 5.5 | 7.5 | Removes misleading cross-body climate/resource score and fixes scale language |
| Creativity | 7.5 | 7.0 | Less feature novelty, but the evidence/datasheet concept remains distinctive |
| Meaningful NASA data usage | 8.0 | 8.5 | MOLA/LOLA/PDS are central rather than decorative |
| Technical depth | 8.0 | 7.5 | Less infrastructure, more auditable science |
| AI usefulness | 5.5 | 5.5 | Modest by design; AI is constrained communication, not a scoring gimmick |
| Usability | 7.0 | 8.0 | Smaller scope, static/offline flow, clearer evidence |
| Visual impact | 8.0 | 7.5 | A polished map and datasheet remain; no need for a 3D globe |
| Validation | 5.5 | 7.0 | Honest site-level ranks and baselines replace inflated acceptance targets |
| Feasibility | 5.5 | 8.5 | One vertical slice can actually finish in 48 hours |
| Originality | 7.0 | 7.0 | Registry novelty is carefully worded; reproducibility differentiates |
| Presentation potential | 7.0 | 8.0 | Simple story: same terrain scale, evidence, rank, limitation |

**Approximate averages:** original **6.9/10** after deducting for scientific overclaim and scope risk; corrected **7.6/10** if the team demonstrates real outputs and honest validation. A completed, visually polished original could score well, but the current blueprint is not itself evidence that those features will be completed or scientifically defended.

## T. Final “BUILD THIS”

If I were one of the four students, I would ship this exact product:

> **AnalogAtlas Terrain Edition:** an offline, open-data map that compares the terrain morphology of a lunar south-pole reference region and one Mars rover region with dry, volcanic, polar and desert Earth regions at one documented metric scale. It ranks candidates using four transparent DEM-derived features, applies visible Earth eligibility gates, shows an evidence-quality badge and per-feature explanation, and includes a validation page with three known analogs, two hard negatives, a terrain-only baseline and one failure. Every candidate exports a one-page datasheet. The app contains no paid API, no live tiles, no required backend, no LLM, no “NASA-approved” claim, and no claim that a site is new to science.

Build order:

1. Make the terrain pipeline correct and benchmarked.
2. Produce one target vector and one Earth ranking.
3. Add validation before adding features.
4. Add the second target and static map.
5. Add datasheet, claims policy, citations and offline test.
6. Only then add one context layer or constrained AI rewrite if it cannot endanger the core demo.

The winning pitch is not “we found Mars on Earth.” It is: **“We made the analog claim inspectable: same stated terrain scale, same computation, per-feature evidence, known failures, and no hidden scientific authority.”**

### Source notes

* [NASA Space Apps 2026 homepage and submission window](https://www.spaceappschallenge.org/2026/)
* [NASA Space Apps 2026 challenge description](https://www.spaceappschallenge.org/2026/find-a-team/lunar-terra/)
* [NASA Space Apps 2026 Participant Terms and Conditions](https://www.spaceappschallenge.org/legal/)
* [NASA Moon Base overview](https://www.nasa.gov/reference/moonbase-about/)
* [NASA/Artemis updated candidate-region record](https://ntrs.nasa.gov/citations/20250011660)
* [GEBCO 2025 grid documentation](https://www.gebco.net/data-products-gridded-bathymetry-data/gebco2025-grid)
* [MOLA MEGDR PDS documentation](https://pds-geosciences.wustl.edu/missions/mgs/megdr.html)
* [LOLA GDRDEM PDS documentation](https://ode.rsl.wustl.edu/mars/pagehelp/Content/Missions_Instruments/LRO/LOLA/GDR/GDRDEM.htm)
* [NASA Earthdata MODIS collection index](https://cmr.earthdata.nasa.gov/search/site/collections/directory/LPCLOUD/gov.nasa.eosdis)
* [WorldClim license](https://worldclim.org/about.html)
* [Global Aridity Index and PET database](https://www.global-ai-pet.org/global-aridity-index-pet-database)
* [Protected Planet legal terms](https://www.protectedplanet.net/en/legal)
* [Copernicus access terms](https://www.copernicus.eu/en/terms-use/how-access-data)

