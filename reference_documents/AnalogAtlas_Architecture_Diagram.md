# AnalogAtlas - Architecture and Feature Map

**Companion to:** [AnalogAtlas Master Build Specification v1.1](AnalogAtlas_Final_Master_Build_Specification_v1.1.md)  
**Printable version:** [Architecture and Features PDF](output/pdf/AnalogAtlas_Architecture_and_Features.pdf)

This Markdown uses ordinary embedded PNG images - no Mermaid or special diagram renderer. Keep the `output/pdf/md-assets/` folder beside this file when uploading it to a Markdown-to-PDF service, so the image links resolve. The PDF above is standalone and does not need those assets.

## 1. System architecture

![AnalogAtlas system architecture: source datasets and configuration flow through the local Python science build into compact outputs and an offline React/MapLibre application.](output/pdf/md-assets/architecture-page-1.png)

## 2. Science engine, scale, features and score

![Shared 500 metre analysis grid, Horn slope scale, 256 square kilometre support, four terrain features, IQR tolerance and deterministic score.](output/pdf/md-assets/architecture-page-2.png)

## 3. User experience, validation and team build

![Offline application features, separated discovery and held-out validation, and responsibilities for the four-person team.](output/pdf/md-assets/architecture-page-3.png)

## Frozen implementation at a glance

- **Sources:** GEBCO for Earth, LOLA for the Moon, MOLA for Mars; exact product versions and coverage are recorded in the run manifest.
- **Scale:** 500 m metric analysis grid; Horn 3 x 3 slope with a 1 km derivative baseline; each target and candidate uses a 16 x 16 km (256 km2) support.
- **Features:** median slope, slope P90, elevation relief P95-P5, and population standard deviation of slope.
- **Score:** two equally weighted feature families; per-feature tolerance is 0.25 times the equally weighted mean of the three discovery-window IQRs.
- **Validation:** Atacama/Yungay, Haughton Crater and Death Valley remain held out until after the scientific configuration is frozen.
- **Runtime:** static React + Vite + MapLibre app using local JSON/GeoJSON and a local basemap; no required backend or network.
- **Limits:** a terrain agreement index, not probability, trafficability, safety, mission suitability, NASA certification, or scientific novelty.
