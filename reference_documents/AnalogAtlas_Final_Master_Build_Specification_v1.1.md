# AnalogAtlas — Final Master Build Specification

**Version:** 1.1 (frozen build plan)  
**Decision date:** 5 October 2026  
**Purpose:** implementation-ready specification for a four-person NASA Space Apps team.  
**Supersedes:** v1.0 for implementation decisions; v1.0 is retained unchanged as the decision history.  
**Status:** scientific rules below are frozen. Event-provided datasets/requirements may replace sources or extents only through the change-absorption process in §24 and a versioned config change before validation.

## 1. FINAL DECISION

**Modify v1.0 with targeted patches; do not redesign or expand the product.** The terrain-first, deterministic, offline atlas remains the right 48-hour scope. V1.1 makes the statistical unit, scale, tolerances, validation separation, window-selection rule, and data-volume assumptions explicit. It also corrects the source mapping: LOLA is the lunar altimeter; MOLA is the Mars altimeter. No probability, trafficability, safety, resource, mission-certification, NASA-approval, global-exhaustiveness, or scientific-novelty claim is permitted.

Core claim: **“AnalogAtlas identifies Earth regions with measurable terrain-morphology agreement with selected lunar and Martian reference regions at a declared analysis scale.”**

## 2. WHAT CHANGED FROM v1.0

| v1.0 decision | v1.1 decision | Reason | Impact |
|---|---|---|---|
| Target median and IQR over an ROI | One fixed 16 × 16 km target support per body; no target heterogeneity parameter | One support cannot yield a meaningful distribution/IQR | Simple, honest reference vector; no invented target uncertainty |
| Approximately 250 km² supports | Exactly 256 km² square supports, 16 × 16 km | Exact integer grid geometry at 500 m | Each support is 32 × 32 analysis cells |
| Fixed tolerances without a reproducible derivation | `δk = 0.25 × IQR` across eligible discovery supports, balanced by window | Robust, reproducible, independent of validation positives | Freeze before validation; report sensitivity, never optimize |
| Andes, Namib, Ladakh discovery windows | East African Rift/Afar, Namib, Ladakh; Atacama, Haughton and Death Valley held out | Avoid selecting search areas around known positives and improve geographic/terrain diversity | Andes is replaced; validation cannot set tolerances or rank-search choices |
| “~1 km effective scale” with ambiguous grid/stencil wording | 500 m metric analysis cells; Horn 3×3; 1 km center-to-center derivative baseline; 1.5 km stencil footprint | Separates grid interval from derivative and support scales | UI says “~1 km derivative baseline; 500 m analysis grid” |
| Four features implicitly equal | Four retained and grouped into two equally weighted families | Slope metrics and variability metrics can be redundant | Prevents one family dominating solely by having two members |
| Small, loosely defined registry | Minimum 12, target 20 documented entries; validation examples explicitly held out | Better documentation and traceability, not a novelty claim | Registry does not train/tune the score |
| Extensive governance without priority levels | P0 correctness, P1 if time, P2 polish, plus explicit cuts | Protect scientific validity under 48-hour constraints | Scientific freeze and source traceability remain mandatory |
| Event datasets treated as relatively static | Configuration-driven adapters and event-time source freeze | Challenge materials may change before the event | Replacing a source need not rewrite scoring or UI contracts |

## 3. FINAL SCIENTIFIC MODEL

### Question and unit

For each body, compare the terrain-morphology feature vector of a fixed reference support with vectors from equal-area Earth candidate supports. A support is the unit of analysis, ranking and map display. The map may aggregate or downsample for rendering, but the science table remains support-level.

### Shared processing

1. Read a version-pinned DEM and validity/source-quality masks.
2. Reproject to a local metric equal-area CRS appropriate to each target/window.
3. Resample elevations by area-weighted averaging to a 500 m square-cell analysis grid. Do not imply resampling creates information finer than the source.
4. Compute Horn slope on the common grid. Derivatives use physical x/y spacing and elevation in metres.
5. Partition eligible cells into non-overlapping 32 × 32 supports anchored at a deterministic origin in each projected window. Use a fixed origin in the frozen config; do not shift it to improve results.
6. Calculate four support summaries: median slope, 90th percentile slope, elevation P95−P5, and population SD of slope. Slope is in degrees; relief is metres; slope SD is degrees.
7. Compare support vectors with the fixed tolerance score in §11; apply pre-score eligibility gates and missingness rules.

### Interpretation boundary

This is a terrain-statistics comparison, not physical equivalence between worlds. Equal projected area and an identical analysis method aid comparability but cannot equalize sensor point-spread, DEM interpolation, vertical datum, landform genesis, gravity, atmosphere, regolith, or sub-grid roughness. It does not provide site suitability or safety advice.

## 4. FINAL SCALE DEFINITION

| Term | Frozen meaning |
|---|---|
| Source grid spacing | Earth: GEBCO_2026, nominal 15 arcsec (roughly 0.46 km north-south; east-west varies with latitude), unless official event resources require another source. Moon: LOLA LDEM_45S_100M polar product (100 m nominal posting), subject to coverage/label verification. Mars: MOLA MEGDR 128 pixels/degree (~0.44–0.46 km near Jezero). Nominal interval is not effective resolution. |
| Analysis grid spacing | 500 m × 500 m in a local metric equal-area projection for all scored bodies/windows. |
| Derivative operator | Horn 3 × 3 finite-difference slope; center-to-center derivative baseline is 2 cells = 1,000 m. |
| Kernel footprint | 3 × 3 cell stencil spans 1.5 km edge-to-edge on the 500 m grid. |
| Candidate support | 16 km × 16 km square = exactly 256 km² = 32 × 32 analysis cells. |
| Effective terrain scale label | “~1 km derivative baseline on a 500 m analysis grid; 16 km support.” Never shorten this to “1 km DEM resolution.” |

Use a one-cell minimum DEM halo around each support before slope calculation, preferably a tile halo of two cells to simplify block reads; discard halo outputs. Use local Lambert azimuthal equal-area (LAEA) grids: WGS84 ellipsoid for Earth; body-specific Moon/Mars radii and coordinate conventions read from the selected PDS product labels for the planetary grids. Do not project Moon/Mars data on the WGS84 ellipsoid. Center each LAEA at its target/window center and record its full PROJ definition. Pin longitude convention, planetocentric/planetographic conversion, resampling method, vertical units, edge handling and software versions. Resampling/CRS transformations are part of the reproducible run record.

## 5. FINAL TARGET-STATISTICS METHOD

Choose **one-support method (option C)**. The target ROI for each body is one team-defined 16 × 16 km equal-area square centered on the representative coordinate below. It is not described as an official mission boundary. The support’s four cell-derived summaries are the target vector. “Target median” means the median of pixel-level slope values for median slope; the other three vector entries are the P90 of pixel-level slopes, the within-support elevation P95−P5, and population SD of pixel-level slopes.

There is one support per target (`n = 1`). The minimum is one support with at least 90% valid analysis cells and valid feature computations. If that test fails, that target cannot be scored and the app must show “reference unavailable”; it must not silently substitute a different footprint. **Target spatial heterogeneity is not estimated from n=1 and is not assumed to be zero.** It is omitted from the scoring model, so target tolerance `τk = δk`. This is not measurement uncertainty. Future multi-support target characterization would require a separately versioned study, not a hackathon-time change.

Frozen approximate centers: Moon south-polar Connecting Ridge study reference **89.46°S, 137.4°W** (team reference point; check LOLA coverage and coordinate convention), and Mars Jezero landing neighborhood **18.4446°N, 77.4509°E**. Verify the Moon support’s actual geometry, LAEA area, DEM coverage and placement against source metadata before freezing the target config. If the approximate lunar coordinate cannot support a valid 16 km square, report the reason and request a science-freeze amendment; do not move it by visual score inspection.

## 6. FINAL TOLERANCE METHOD

For feature `k`, calculate one tolerance from eligible discovery supports only:

`δk = α × IQR_Earth,k`, with `α = 0.25` for every feature; `IQR = Q75 − Q25`.

Rules:

- Apply fixed pre-score data-validity/coverage gates first. Do not apply analog/score labels or validation membership as selection criteria.
- Compute the empirical IQR separately in each frozen discovery window, then take their equally weighted mean: `IQR_Earth,k = (IQR_1,k + IQR_2,k + IQR_3,k) / 3`. Within each window, every eligible support has equal weight. This prevents the largest window from dominating the scale.
- Use the Hyndman–Fan type 7 linear-interpolation quantile, as implemented and fixture-tested in the pinned scientific runtime. Record eligible count/window and all three IQRs.
- IQR is robust to extreme tails but does not remove skew. Do not log-transform features; publish empirical quantiles and inspect histograms before freeze.
- `δk` must be finite and positive. If a feature’s pooled IQR is zero, mark that feature non-discriminating and exclude it before validation; redistribute its predeclared within-family weight equally among remaining features in that family. If the entire family is non-discriminating, redistribute its family weight to the other family and disclose the change. No arbitrary epsilon/minimum tolerance is permitted.
- Freeze `α = 0.25` as a heuristic before computing validation scores. Also report fixed sensitivity values `α = 0.10` and `0.50`; these are sensitivity runs, not model selection. Do not choose an alpha based on analog rank or validation performance.

Alternative tolerances (fixed domain thresholds, standard deviations, and validation-fitted thresholds) were rejected: domain thresholds lack a single defensible common physical interpretation for these regional summaries; standard deviation is more outlier-sensitive; validation fitting is circular. The IQR method is a transparent scale normalization heuristic, not a scientifically calibrated equivalence threshold.

## 7. FINAL FEATURE SET

| Feature | Definition / units | Interpretation | Correlation concern | Weight |
|---|---|---|---|---:|
| Median slope | Median Horn slope of valid support cells; degrees | Typical grid-scale inclination | Correlated with P90 and slope SD | 0.25 overall |
| Slope P90 | 90th percentile Horn slope; degrees | Upper-tail steepness, not a hazard threshold | Correlated with median slope and slope SD | 0.25 overall |
| Relief P95−P5 | 95th minus 5th percentile elevation within support; metres | Robust local elevation range | Correlates with slopes; depends on geomorphic wavelengths and DEM smoothing | 0.25 overall |
| Slope SD | Population standard deviation of support-cell slope; degrees | Within-support slope variability | Correlated with median and P90; outlier-sensitive | 0.25 overall |

Weights are grouped: **Slope distribution** = median slope + P90 slope, family weight 0.5; **Terrain variability** = relief + slope SD, family weight 0.5. Members split their family weight equally. This limits accidental double weight for slope-related variables while retaining interpretable measurements. We do not claim independence, and we do not use PCA in the MVP.

### Pre-rank feature correlation check

After discovery supports and fixed gates are finalized, but before any validation score/rank is produced, compute Spearman correlations for all four features on a deterministic sample or all eligible supports (use all if feasible). Report sample size, per-window and pooled matrices, and scatterplots. Flag `|ρ| ≥ 0.85` as high redundancy for disclosure. Do not remove/reweight features based on correlation in the MVP; do not inspect validation outcomes when making any scientific decision. Correlation findings may motivate a future version, not an unlogged event-time patch.

## 8. FINAL SEARCH-WINDOW PROTOCOL

Freeze three discovery windows by a written, score-blind protocol. A candidate region is eligible when it (1) spans a coherent, bounded physiographic setting; (2) contributes a different broad terrain process/landform context from the other windows; (3) is geographically separated from the other windows; (4) is not centered on or chosen to include a named validation site; (5) has full, permissible DEM coverage and usable source metadata; (6) fits the bounded regional processing budget; and (7) can provide a transparent land mask and deterministic support grid. Among eligible alternatives, choose using geographic diversity and coverage first, then terrain/analog relevance. No score, target similarity, or favorable candidate is a selection criterion.

Run this protocol once before calculating rankings. Save the short candidate-screening notes, selected bounds, rejected alternatives, config version and checksum. Named analog field sites are validation, not discovery-window selection anchors. Discovery windows are not asserted to be a global or representative sample of Earth.

## 9. FINAL EARTH WINDOWS

Three equal-area-projected discovery windows; bounds are WGS84 longitude/latitude and are fixed inclusively at the outer edge. The projected usable area excludes ocean and cells failing data gates.

| Discovery window | Fixed bounds | Approximate land area | Rationale / caveat |
|---|---|---:|---|
| East African Rift / Afar highlands | 36–42°E, 7–13°N | ~0.44 million km² | Rifted, volcanic and upland relief; broad physiographic diversity. Window is not a claim of direct environmental equivalence. |
| Namib margin and interior | 12–20°E, 20–28°S | ~0.76 million km² | Arid terrain and strong relief contrasts. GEBCO land source quality is heterogeneous; nominal 15″ is not local effective resolution. |
| Ladakh / western Himalaya | 75–82°E, 32–37°N | ~0.35 million km² | High-relief mountain/desert setting provides a contrasting terrain regime. Terrain variability and source interpolation must be disclosed. |

Area and computation estimates are rough planning calculations from geographic bounds, not GIS-measured final counts. **Validation set held outside these windows:** Atacama/Yungay, Haughton Crater, and Death Valley. If final coordinates fall within any window after source-backed site definition, resolve overlap before freeze by excluding a predeclared 16 km buffer around the entire validation support from discovery calibration and rankings; log it. Prefer no overlap. These locations can be discussed as known analog field environments; a label does not imply all their terrain is positive for both targets.

**Capacity estimate for the three windows:** total geographic area ~1.55 million km²; at 500 m cells, ~6.2 million analysis cells before masks. A 15″ source grid implies approximately 7–9 million sampled source cells depending on latitude/bounds. One int16 source array is ~14–18 MB raw, before metadata/compression; source downloads, GeoTIFF/COG conversion and tile padding may make actual files tens to a few hundred MB. A small streaming/tiled feature build should keep working arrays to roughly 0.5–1.5 GB peak RAM; an incautious whole-array implementation can exceed this. Temporary disk budget 2 GB. These are estimates, **not benchmark results**. The event-time Earth source release may differ; recalculate with actual raster dimensions.

## 10. FINAL TARGETS

1. **Moon:** one 256 km² support centered near Connecting Ridge, 89.46°S, 137.4°W; use LOLA LDEM_45S_100M as the named input candidate, and confirm coverage, labels, product version and coordinate convention before freeze. NASA has not fixed a permanent-base polygon at this location; this is a documented team-defined reference, not an official site boundary.
2. **Mars:** one 256 km² Jezero landing-neighborhood support centered at 18.4446°N, 77.4509°E; MOLA MEGDR at 128 ppd for global context/source consistency, with exact product/version pinned. The support is much broader than Perseverance’s landing ellipse and is not a landing-safety area.

One lunar and one Mars target selector is sufficient. If source resolution/coverage is inadequate for a valid support, show unavailable; do not substitute a high-resolution local product for only one body without a pre-validation freeze amendment and a comparable-processing rationale.

## 11. FINAL SCORE

For target `t` and candidate support `i`, feature distance and partial agreement are:

`dk,i = min(1, |xk,i − tk| / δk)`  
`ak,i = 1 − dk,i`

With four features and frozen weights `wk` summing to 1, score all features against their target values:

`Terrain Morphology Agreement(i,t) = 100 × Σk wk × ak,i`.

Do **not** renormalize over available features. A missing/invalid feature contributes agreement zero; therefore missingness can never improve the score. Pre-score eligibility requires at least 90% valid cells in a support and all four features present for ranked output. Supports failing that gate are not ranked and are shown as excluded with reason, rather than silently filled. If a feature is globally removed by the zero-IQR rule, use the frozen redistributed weights and record it.

The index is bounded 0–100, deterministic, and **not a probability**. A score is tolerance-dependent agreement, not a calibrated physical equivalence. Sort descending; ties use fixed stable `support_id` lexical order. UI wording: **Terrain Morphology Agreement (0–100 index)** and **Scenario Ranking** only.

## 12. FINAL VALIDATION

Use a small, pre-registered, site-level face-validity experiment; not a model-training set.

- **Held-out documented positives/examples:** Atacama/Yungay, Haughton Crater, Death Valley. Use one or more citations per site and specify each site’s analog domain. Do not assume one label is positive for both targets; before scoring, a planetary-science reviewer marks each site-target pair as relevant, contextual, or not assessed with a rationale.
- **Contrast controls:** select two recognizable terrain settings before score generation (e.g., Salar de Uyuni and Mauna Loa only if source-backed criteria support them). Call them contrast controls, not true negatives. Never use unlabeled random cells as negatives.
- Compute the exact 16 km support vectors at documented site centers using the same pipeline. No positive/control supports enter discovery IQR calculations. Keep sites spatially separate from discovery candidate supports, with fixed buffer/exclusion policy. Rank the site supports among discovery supports and publish rank/percentile only as descriptive. Include gate-only comparison, all failed/missing sites, and at least one false positive/false negative or low-ranking known analog if observed.
- No ROC-AUC, accuracy claim, supervised fit, threshold tuning or positive-driven window selection. Registry is too small and purposive for predictive validation. Pre-rank correlation check and scientific freeze precede this experiment.
- Publish site source, center coordinate, target/site label rationale, support polygon, all four feature values, coverage, source flags and resulting ranks. If site shape/center is uncertain, report sensitivity as a separately labeled descriptive check, not an optimization.

## 13. FINAL REGISTRY

Target **20 documented analog/environment entries**, with a hard minimum of **12** before describing the registry as a useful browseable product. If fewer than 12 are ready, ship fewer honestly and call it a pilot list. Build only from NASA/ESA/JAXA/ISRO/CSA sources, government geological/space-agency sources, mission publications and peer-reviewed field-analog papers. Avoid copying restricted maps/imagery; citations and factual metadata only unless terms permit redistribution.

Required fields: stable `site_id`; display name; coordinates and uncertainty/geometry source; country/region; analog domain(s); intended target association (if any); label (`validation_positive`, `contrast_control`, `context_only`, `registry_only`); rationale; citation title/DOI/URL; source organization; source date/retrieval date; license/redistribution note; registry version; reviewer and last-checked date. The registry does not train the score. Validation labels are not automatically inferred from appearance.

Freeze a versioned registry and dated prior-use search log. Search only stated public sources (agency analog-site catalogs, mission/field analog publications, papers/web sources named in the log) using location name and coordinates. Exact UI language: **“New to our registry (registry vX, dated YYYY-MM-DD). No prior analog or training use found within our stated search scope as of YYYY-MM-DD; this is not evidence of scientific novelty.”** “New” is registry-relative only.

## 14. FINAL EVIDENCE QUALITY

Display Evidence Quality separately from the morphology score. It is a transparent, non-probabilistic data-quality summary with components:

- **Coverage:** valid 500 m cells divided by 1,024 expected cells.
- **Source lineage:** source/product version and known source-quality/coverage flag, including GEBCO Type Identifier summary when available; mark unknown or mixed source honestly.
- **Sensitivity stability:** whether candidate score decile/top-50 membership is stable across predeclared alpha (0.10/0.25/0.50) and one grid-origin sensitivity, if time allows. If not computed, say “not assessed.”

Show components rather than one opaque confidence number. If a compact badge is needed, use “high / medium / limited evidence” only under published completeness/source rules; never describe it as probability, confidence of analogy, accuracy, safety, or suitability. Missing data cannot increase either the headline score or Evidence Quality.

## 15. FINAL AI ROLE

AI is optional and subordinate. It may generate a draft plain-language explanation from a deterministic evidence JSON object, but cannot select sites, alter scores, write scientific conclusions without citations, or override the displayed values. Default product must work without a model or network. If no fully local, free and tested model is already available, ship template-based explanations and no AI feature. Log any AI use in the competition submission. Validate generated text against source IDs and numeric values; on mismatch, render deterministic template text. Do not add RAG, hosted APIs, or AI-generated novelty claims.

## 16. FINAL ARCHITECTURE

```text
Versioned config + locally downloaded, licensed DEMs
                    ↓
Python build pipeline (NumPy, Rasterio/GDAL, pyproj, Shapely/GeoPandas)
                    ↓
Parquet science tables + compact GeoJSON/JSON + provenance manifest
                    ↓
React + Vite + MapLibre + local Natural Earth vectors
                    ↓
Offline static demo (local server or packaged static files)
```

DuckDB is optional at build time. No required API server, FastAPI, PostGIS, Docker, cloud, hosted tiles, external API, paid map, or LLM. Build products locally; bundle only the needed derived candidate products, not full global source datasets. Ship attribution and source records. Runtime remains network-independent.

## 17. FINAL DATA CONTRACTS

### `config/run.yaml` (version-controlled)

```yaml
schema_version: "1.1"
run_id: "event-YYYYMMDD-<short-hash>"
analysis_grid_m: 500
support_m: 16000
horn_kernel_cells: 3
support_cells: 32
min_valid_fraction: 0.90
tolerance_alpha: 0.25
quantile_method: "Hyndman-Fan-7"
feature_family_weights: {slope_distribution: 0.5, terrain_variability: 0.5}
validation_scored_after_freeze: true
```

Targets, windows, dataset adapters, CRS, support-grid origin, source versions, and validation site definitions live in separate `targets.yaml`, `windows.yaml`, `datasets.yaml`, and `validation.yaml`. Reject unknown schema versions.

### `features.parquet` (one row per support)

Columns: `schema_version` string; `run_id` string; `support_id` string; `region_id` string; `role` enum (`discovery|target|validation|control`); `target_id` nullable string; `geometry` projected polygon or WKB with CRS metadata; `center_lon`, `center_lat` float64; `valid_fraction` float32; `source_id` string; `source_quality_summary` string/JSON; `slope_median_deg`, `slope_p90_deg`, `relief_p95_p5_m`, `slope_sd_deg` float32 nullable; `excluded_reason` nullable string. No NaN/Infinity; null means unavailable.

### `scores.json` (UI payload, abridged)

```json
{
  "schema_version":"1.1",
  "run_id":"event-YYYYMMDD-abc123",
  "target_id":"mars_jezero_v1",
  "score_name":"Terrain Morphology Agreement",
  "score_scale":[0,100],
  "method":{"grid_m":500,"derivative_baseline_m":1000,"support_m":16000,"alpha":0.25},
  "items":[{
    "support_id":"EA_000001",
    "score":72.4,
    "rank":1,
    "features":{"slope_median_deg":null,"slope_p90_deg":null,"relief_p95_p5_m":null,"slope_sd_deg":null},
    "coverage":0.98,
    "evidence_quality":{"coverage":"high","source_lineage":"mixed","sensitivity":"not_assessed"},
    "source_ids":["earth_dem_release_id"]
  }]
}
```

Values above are illustrative schema examples, not measured results. Runtime validators enforce finite values, bounds, required keys and stable IDs. Include exact `scores.schema.json`, `features.schema.json` and fixtures in the repository.

## 18. FINAL REPOSITORY

```text
analogatlas/
├── README.md
├── LICENSE
├── CITATION.cff
├── config/
│   ├── run.yaml
│   ├── targets.yaml
│   ├── windows.yaml
│   ├── datasets.yaml
│   └── validation.yaml
├── schemas/
│   ├── features.schema.json
│   └── scores.schema.json
├── data/
│   ├── raw/                 # gitignored; local only
│   ├── interim/             # gitignored
│   ├── processed/           # compact derived products only
│   └── registry/sites.csv
├── manifests/
│   ├── sources.csv
│   └── run.json
├── science/
│   ├── README.md
│   ├── validation-results.csv
│   └── limitations.md
├── scripts/
│   ├── fetch_or_prepare.py
│   ├── build_features.py
│   ├── score_and_rank.py
│   ├── validate.py
│   └── benchmark.py
├── tests/
│   ├── fixtures/
│   ├── test_features.py
│   ├── test_scoring.py
│   └── test_contracts.py
└── app/
    ├── package.json
    ├── vite.config.js
    ├── public/data/
    └── src/{components,views,lib,styles}/
```

Do not commit raw DEMs, credentials, restricted data, or unneeded temporary rasters. Keep the team’s already-present blueprint/review materials and v1.0; this v1.1 file is a new versioned artifact.

## 19. FINAL TEAM OF 4

1. **Science/data lead:** source verification and license allowlist; target/window config; target and validation site definitions; review feature plausibility and caveats.
2. **Geospatial pipeline lead:** adapters, CRS/resampling, Horn features, masks, support IDs, Parquet; benchmark and unit tests.
3. **Scoring/validation lead:** tolerance freeze, grouped weights, deterministic scoring, held-out site ranks, sensitivity and validation report. Cannot change frozen methods after viewing validation results.
4. **Frontend/demo lead:** schema-driven map, target switcher, ranking/detail/datasheet, offline check, three-minute narrative.

All four review the P0 freeze before producing validation ranks. Agree schemas and fixture data in the first hour. Assign one integrator; avoid parallel edits to the scoring contract. If staff overlap is needed, science lead can help registry, and scoring lead can help tests; no one is sole owner of both validation labeling and post-result model changes.

## 20. FIRST VERTICAL SLICE

First slice: **Jezero MOLA target → Namib discovery window → four features → frozen IQR from all three windows only after all are built → score/rank → held-out site plumbing (fixture first, actual validation after freeze) → local map → one datasheet.** Use a small end-to-end Namib patch for pipeline proof; do not derive or publish the final tolerance from one window. After the full three-window eligible set is assembled, compute pooled tolerance as §6 specifies, freeze the manifest, then run validation.

Prove exactly:

```text
RAW DEM → METRIC PROJECTION → COMMON 500 m GRID → TERRAIN FEATURES
→ TARGET VECTOR → FROZEN TOLERANCE/SIMILARITY → RANKING
→ HELD-OUT VALIDATION → OFFLINE MAP → CANDIDATE DATASHEET
```

The first slice is pipeline proof, not final evidence or a validated result. If the Moon target data arrives first, use that as an additional test but do not block on it.

## 21. 24-HOUR EMERGENCY BUILD

Keep only one target (Jezero), all three bounded windows if feasible (otherwise explicitly publish the completed subset and do not call it the frozen three-window design), the exact four-feature pipeline, the predeclared formula, top-50 map/list, source manifest, one held-out validation example plus its limitations, and one datasheet. Keep offline local basemap, schema/score tests, and the scientific freeze. Cut optional contextual overlays, LLM, hosted deployment, full registry beyond minimum citations, animations, advanced sensitivity UI and elaborate benchmarks. Never cut data/source attribution, held-out separation, missingness gates, or score limitations. If the defined P0 science cannot finish, show a clearly labeled pipeline prototype rather than imply completed results.

## 22. 48-HOUR FULL BUILD

| Time from opening | Work and exit condition |
|---|---|
| 0–2 h | Confirm rules/challenge assets; assign owners; create repo and schemas/fixtures; verify exact selected source products/licenses; record run ID. |
| 2–6 h | Download/prepare bounded patches; build one Jezero→Namib end-to-end fixture; confirm CRS, units, masks, grid, support ID determinism. |
| 6–14 h | Stream/tile full three windows and both targets; compute feature tables and completeness; run tests and benchmark. |
| 14–18 h | P0 science freeze: windows/targets/source versions/gates/features/tolerance cohort/weights/validation labels; checksum config and outputs. |
| 18–24 h | Compute tolerance and discovery scores; run pre-rank correlation audit; save manifests and sensitivity. No validation results seen yet. |
| 24–31 h | Run held-out validation; inspect positives/controls and failures; populate transparent results table; prohibit parameter adjustment. |
| 31–39 h | Finish offline map, top-50 exploration, datasheet, evidence-quality components, source and caveat panels. |
| 39–44 h | Clean offline run, weakest-laptop benchmark, data license audit, schema/scoring tests, fix only implementation defects (not scientific tuning). |
| 44–48 h | Rehearse 3-minute demo including a failure; verify submission fields/permissions; record video/link if required; submit with buffer. |

Actual challenge instructions supersede this schedule. Reserve final hours for submission verification, not new scientific features.

## 23. P0 / P1 / P2 / CUT

| Tier | Items | Why / validity effect | Automate? | Cut? |
|---|---|---|---|---|
| **P0 — mandatory correctness** | Scientific freeze before validation; source/product/license table; exact target/window/config versions; schema contract; data gates/missingness; deterministic IDs/score; raw-data gitignore; provenance run ID; attribution; core tests; honest limitations | Directly protects reproducibility, licensing and circularity; freeze is essential to validity | Yes for schema, checksums, finite/range checks, gates and repeatability | No |
| **P1 — important if time** | Full eligible-support correlation matrices; complete performance and memory benchmark; alpha/grid-origin sensitivity; source TID summary; 20-site registry; browser size/timing; independent JS/Python score parity if scoring is duplicated | Improves auditability and robustness; core science can still be honestly reported if marked “not assessed” | Mostly | Some may be omitted with explicit disclosure; do not substitute post-hoc claims |
| **P2 — documentation polish** | PCA/scatterplot gallery (PCA descriptive only, never MVP score), polished lineage diagrams, full site essays, animation, extended metadata UX | Communicates context; does not establish validity | Partly | Yes |
| **CUT** | Model tuning from validation; random unlabeled negatives; probability language; cloud/API dependencies; paid data/tools; required AI; global exhaustive search; real-time remote tiles; safety/mobility claims | Creates circularity, scope/cost risk, or unsupported claims | N/A | Always |

Scientific freeze is P0 and cannot be cut. A frozen, immutable config checksum and a short decision table are sufficient governance; no elaborate approval workflow is required.

## 24. PRE-EVENT / EVENT BOUNDARY

Before the event, retain this architecture/specification, learn general tools, and prepare generic reusable skills only as permitted by the current official rules. Do not assume pre-event project-specific code, score results, derived datasets or submission material are allowed. At event opening, inspect the final challenge page, terms, partner/data resources and submission requirements; record URL, retrieval time, version and interpretation. If rules disallow pre-event preparation or data processing, perform those steps only after opening. Do not process restricted or credential-gated sources contrary to their terms.

Change absorption: `datasets.yaml` maps logical layers to a dataset adapter, product/version, license, nodata, vertical unit/datum, CRS and source-quality field. `targets.yaml`, `windows.yaml`, and `validation.yaml` hold bounds, sites and labels. `run.yaml` holds grid/scoring settings. Each adapter normalizes inputs into the same elevation/mask/quality interface; the feature engine consumes normalized rasters; scoring consumes feature rows and frozen `target_vector`; UI consumes stable JSON/GeoJSON schemas. NASA changing a recommended dataset should require adapter/config and source-manifest changes, not a scoring-engine rewrite.

If challenge wording/target definitions change, the science lead drafts a config amendment with rationale; all four review it before any validation score is produced. Increment `schema_version` only for interface changes; increment `run_id` for every scientific data/config change. If an amendment follows validation inspection, preserve prior outputs, label the run exploratory, and do not present it as confirmatory validation.

## 25. PERFORMANCE BENCHMARK

Benchmark script must run on the slowest team laptop and record OS, CPU, RAM, Python/GDAL/NumPy versions, dataset bytes/dimensions, cache state and run ID. Measure: source read and crop; reprojection/resampling; feature generation; supports/second; score/rank time; peak RSS; temporary disk peak; output sizes; offline browser initial usable render; map rendering at 50 and 2,000 supports; local re-rank latency if scenario sliders are included.

Initial estimates: ~6.2M Earth analysis cells; tiled arrays with elevation/mask and four working fields should ordinarily fit below 1.5 GB peak, but GDAL/cache and copies may raise this; budget 2 GB peak and 2 GB temporary disk. Typical processing time cannot be asserted without hardware/data benchmark; benchmark a representative patch and extrapolate with a clearly marked estimate only. Desired output budgets: top-50 JSON <5 MB; 2,000-support vector layer <20 MB or use simplified/aggregated map rendering. Browser initial usability <10 seconds from local server start and scenario re-rank <300 ms are targets, not facts. Record measured values; narrow extent or stream smaller blocks if over budget, then refreeze before validation.

## 26. ₹0 COST AUDIT

| Item | Required | Cost / access | Runtime or license decision |
|---|---:|---|---|
| NASA PDS MOLA / LOLA products | Yes | ₹0 public data access; verify selected product metadata | Local build input; cite exact bundle/release |
| GEBCO regional DEM | Yes, unless event dataset replaces it | Public domain/free with attribution; event-time grid selection and terms check | Local build input; never rely on remote service |
| Natural Earth | Yes | Public domain | Package local vectors |
| Python, NumPy, Rasterio/GDAL, pyproj, Shapely/GeoPandas, Parquet tooling | Yes | Open-source, no fee | Local build |
| React, Vite, MapLibre | Yes | Open-source, no fee | Local/offline app assets only |
| DuckDB | Optional | Free | Build-time only |
| NASA Earthdata / Copernicus account data | No | May require free account/acceptance/eligibility | Optional; exclude if access/license or redistribution is unclear |
| Hosting, cloud, database, map tiles, APIs, paid LLM | No | Not budgeted | Explicitly not required or used |

Required external project cost is **₹0**. No trial, billing account, paid dataset, paid API, cloud compute, paid hosting or paid LLM may become a dependency. Team internet/laptops are existing resources, not project purchases.

## 27. RISKS

1. **Source effective resolution differs from cell size:** source lineage and spatial scale caveats; remove any hazard interpretation.
2. **GEBCO land elevation is heterogeneous:** capture source/TID where possible; show it; replace only through a documented adapter/config amendment.
3. **One target support is sensitive to center choice:** freeze center/polygon; label it as a selected reference, not a distribution.
4. **Validation labels overgeneralize analogs:** label site-target pairs, not sites universally; publish rationale.
5. **Validation leakage into IQR/windows:** strict role field and run-order lock; compute tolerance before unmasking ranks.
6. **Feature redundancy:** family weights and pre-rank correlation disclosure; no post-result retuning.
7. **Grid origin changes candidate summaries:** deterministic origin; disclose origin sensitivity if measured.
8. **High latitude/polar projection errors:** polar CRS fixtures; area and orientation checks.
9. **Missing cells inflate apparent agreement:** fixed coverage gates; no available-feature renormalization.
10. **Downloads/disk exceed event capacity:** regional crops, tiled builds, benchmark early; publish reduced scope only with new freeze.
11. **Data license/redistribution violation:** source allowlist; keep raw data local; verify each derived output’s terms.
12. **Offline map requests remote glyphs/tiles:** package style/fonts/vector basemap; test networking disabled.
13. **Late challenge resource change:** adapter/config isolation and stable normalized input contract.
14. **Registry too small or outdated:** minimum 12; cite and date each; pilot wording if unmet.
15. **Scope/integration consumes time:** early schema freeze, vertical slice and cuts; protect submission buffer.

## 28. JUDGE QUESTIONS

1. **What does the score mean?** A weighted, tolerance-normalized comparison of four terrain summaries on equal-area 256 km² supports; it is not probability.
2. **Why terrain only?** Elevation-derived summaries have a comparatively clear operational definition on all three bodies; atmosphere, aridity, albedo, ice and resources are not like-for-like here.
3. **Is 500 m your DEM resolution?** No. It is the common analysis cell spacing. Horn derivatives use a 1 km center baseline, and inputs have different effective resolution.
4. **What area is compared?** One 16 × 16 km support per target/candidate, exactly 256 km².
5. **How is lunar target variability estimated?** It is not; one support does not establish a distribution. Target spatial heterogeneity is omitted, not declared zero.
6. **Why these Earth windows?** A predeclared geographic/physiographic/data-feasibility protocol; no ranking result chose them. Known examples are held out.
7. **Why these analog examples?** Publicly documented field environments; relevance is assigned per target and source-backed, not assumed for all metrics.
8. **Are these results predictive?** No. The small purposive site set is a face-validity experiment, not a statistically powered benchmark.
9. **Why not report AUC?** Unlabeled cells are not true negatives, and the registry is small and selected.
10. **How chosen are tolerances?** `0.25 ×` equally window-weighted discovery IQR, frozen without validation positives; it is explicitly a heuristic.
11. **Do four correlated features count ruggedness four times?** Two feature families receive equal total weight; within-family redundancy is disclosed by a pre-rank correlation audit.
12. **Can it identify safe rover routes or landing sites?** No. It lacks fine-scale hazards and is not a trafficability/engineering model.
13. **Is a location “new to science”?** No. At most “new to our dated registry/search scope”; absence is not proof of novelty.
14. **Is this NASA approved?** No. It is an independent challenge project; it must not imply NASA endorsement.
15. **Where is the AI?** Optional prose assistance only. Deterministic science, scores and offline operation do not depend on AI.

## 29. 3-MINUTE DEMO

**0:00–0:20:** State the narrow claim: inspectable terrain-morphology agreement at a declared scale, not planetary equivalence.  
**0:20–0:45:** Select Jezero; show 16 km support, MOLA source/version and 500 m grid / 1 km derivative baseline.  
**0:45–1:10:** Show offline Earth ranking and the three disclosed discovery windows; explain held-out validation examples.  
**1:10–1:40:** Open a candidate datasheet: four values, units, tolerance contributions, coverage, lineage and caveats.  
**1:40–2:05:** Show Atacama/Haughton/Death Valley site-target labels and ranks, emphasizing small face-validity scope.  
**2:05–2:30:** Show a failure or low-ranking known example and a high-ranking contrast control if observed. Do not hide it.  
**2:30–2:48:** Show “new to our registry” copy with version/search date, or omit if no eligible candidate.  
**2:48–3:00:** Close with offline operation, reproducible sources, and the explicit no-safety/no-certification boundary.

Never fabricate results, claim discovery/novelty, or imply the validation sites were all expected to score highly.

## 30. FINAL BUILD CHECKLIST

### Freeze and sources

- [ ] Recheck final 2026 challenge instructions, event terms and partner resources; record time/version.
- [ ] Verify exact NASA PDS LOLA lunar and MOLA Mars product, release, labels, dimensions, datum, license and source URL.
- [ ] Confirm GEBCO_2026 is still the appropriate permissible source at event-time; record exact release, DOI/URL, TID availability, download dimensions and attribution. If an official challenge source supersedes it, use the adapter/config change process.
- [ ] Check all third-party software/data redistribution terms; omit uncertain optional datasets.
- [ ] Freeze target centers/polygons, three WGS84 windows, support-grid origin, CRS and validation site/control list before validation.
- [ ] Save immutable config, source manifest, registry version, run ID and checksums.

### Science and computation

- [ ] Build 500 m metric equal-area grid; validate units, resampling and area.
- [ ] Compute Horn slope with 1 km baseline and 1.5 km stencil; preserve halo.
- [ ] Compute exactly four features over 16 km supports; test against fixtures.
- [ ] Apply 90% support-validity gate; fail closed for absent target reference.
- [ ] Calculate window-balanced IQR tolerances from discovery only; log counts/quantiles; freeze α=0.25.
- [ ] Run feature-correlation check before validation; disclose redundancy without tuning.
- [ ] Generate deterministic score with fixed weights and no missing-feature renormalization.
- [ ] Score held-out site-target pairs only after freeze; include failures/controls; no AUC.
- [ ] Report alpha sensitivity and grid-origin sensitivity if completed; otherwise mark not assessed.

### Product and release

- [ ] Validate Parquet/JSON/GeoJSON schemas; no NaN/Infinity; nulls explicit.
- [ ] Package a fully local Natural Earth basemap/style/fonts and pass network-disabled test.
- [ ] Show score, per-feature values, scale, coverage, source lineage, rank and limitations.
- [ ] Keep Evidence Quality separate from score and non-probabilistic.
- [ ] Include dated registry/search wording; no scientific novelty language.
- [ ] Ensure no raw/restricted datasets, credentials, secrets or temporary files enter version control.
- [ ] Run benchmark on weakest laptop; record measured values, not estimates as facts.
- [ ] Test clean startup, fixtures, offline browsing, source citations and 3-minute demo including a failure case.
- [ ] Verify submission fields, links, permissions and deadline buffer.

## 31. FINAL CTO DECISION

**Build AnalogAtlas Terrain Edition** as a deterministic, offline static atlas that compares three preselected Earth discovery windows with a single lunar south-polar reference support and a single Jezero reference support. Every comparison uses a 16 × 16 km equal-area support, a common 500 m analysis grid, Horn slope with a 1 km derivative baseline, and four transparent terrain summaries combined in two equally weighted feature families. Feature tolerances come only from the window-balanced IQR of eligible discovery supports and are frozen before separate, documented analog-site validation. The product exposes source lineage, missingness, scale, score contributions, validation failures and limitations; it requires no cloud, paid service or LLM, and makes no safety, mission-suitability, NASA-approval or scientific-novelty claim.

> If I were the CTO of this four-person team, this is exactly what I would build.

### Primary sources to recheck at event-time

- NASA Space Apps 2026 event and challenge pages: https://www.spaceappschallenge.org/2026/ and https://www.spaceappschallenge.org/2026/challenges/identify-earth-locations-that-analog-the-permanent-moon-base-locations-and-mars/
- Official participant terms: https://www.spaceappschallenge.org/legal/
- NASA Moon Base reference and Blue Origin Blue Moon Mark 1 / Connecting Ridge context: https://www.nasa.gov/reference/moonbase-about/ and https://www.nasa.gov/event/clps-flight-blue-origins-blue-moon-mark-1/
- Approximate lunar reference coordinate study: https://doi.org/10.3847/2041-8213/ac5a48
- Jezero landing ellipse and coordinate reference: https://science.nasa.gov/resource/perseverance-rover-landing-ellipse-in-jezero-crater/ and https://doi.org/10.1126/sciadv.abo4856
- GEBCO_2026 grid product page and current grid catalog (15″ nominal interval; check lineage/TID and attribution): https://www.gebco.net/data-products-gridded-bathymetry-data/gebco2026-grid and https://www.gebco.net/data-products/gridded-bathymetry-data
- MOLA MEGDR products: https://pds-geosciences.wustl.edu/missions/mgs/megdr.html
- LOLA lunar PDS products: https://pds-geosciences.wustl.edu/missions/lro/lola.htm
- NASA documented planetary analog and research-location material: https://science.nasa.gov/solar-system/planetary-analogs/ and https://astrobiology.nasa.gov/research-locations/
- Natural Earth terms: https://www.naturalearthdata.com/about/terms-of-use/
- Excluded-source license checks: https://worldclim.org/about.html and https://www.protectedplanet.net/en/legal

All product access, current version, license, challenge wording and event rules must be verified from the primary source before use; citations in this plan are not a substitute for recording the exact product actually processed.
