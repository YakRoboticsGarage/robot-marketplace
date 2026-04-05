# Multi-State DOT Survey Manual Comparison

**Topic ID:** R-001  
**Date:** 2026-04-05  
**Module:** M1_rfp_processor  
**Status:** Complete  
**Researcher:** Automated daily research agent

---

## Executive Summary

- MI, OH, TX, and CA DOTs have meaningfully different LiDAR accuracy requirements, point density minimums, cross-section intervals, deliverable formats, and coordinate system conventions — the current RFP processor defaulting to Michigan standards will produce incorrect specs for out-of-state work.
- Ohio DOT (ODOT, January 2024) specifies 40 pts/m² minimum point density — 5x higher than USGS QL1 (8 pts/m²) and 20x higher than QL2 — a significant differentiator that will affect operator bid pricing.
- TxDOT has a dedicated UAS Aerial Mapping spec document (design-grade, ASPRS Class 1) with 5cm GSD minimum and Level 3 accuracy for ground control, plus a March 2025 revised Survey Manual — the most recently updated of the four state manuals reviewed.
- Caltrans uses a Type A / Type B classification for laser scanning surveys (not USGS QL levels), with Type A requiring Hz ≤ 0.03 ft and Z ≤ 0.02 ft local positional accuracy — stricter than MDOT default.
- NCDOT uses USGS QL-based standards for statewide LiDAR (QL2 baseline) but its drone photogrammetry unit runs its own internal specs, adding a fifth distinct standards regime to track.

---

## Findings

### 1. Michigan DOT (MDOT)

**Source:** [MDOT Design Survey Manual — Chapter 9 Remote Sensing](https://mdotwiki.state.mi.us/design/index.php/Chapter_9_-_Remote_Sensing) | [MDOT Survey Manual](https://mdotjboss.state.mi.us/stdplan/surveymanual.htm)

**Accuracy Standards:**
| Control Type | Horizontal | Vertical |
|---|---|---|
| Primary Control | ±0.05 ft | ±0.05 ft closure |
| Intermediate Control | ±0.07 ft avg; ±0.10 ft max | ±0.10 ft accumulated |
| Design Survey Hard Surfaces | ±0.05 ft | ±0.01 ft; ±0.02 ft relative |
| Topographic Ground | N/A | ±0.10 ft accumulated |

**LiDAR / Remote Sensing (Chapter 9):**
- Mobile Terrestrial LiDAR (MTL): must meet NCHRP Report 748 Category 1A for design projects
- Point density: max 0.1 ft spacing on structures; max 0.3 ft on roads (terrestrial)
- Minimum 4 control points per project; minimum 20% scan overlap
- Validation within 0.05 ft of adjusted point cloud
- Deliverables: e57, LAS, or LAZ format
- NSSDA-formatted accuracy reports required
- LiDAR point cloud files: two copies to MDOT Lansing Survey Support Unit + one to region surveyor
- Chapter 9 focused primarily on Mobile Terrestrial LiDAR; aerial/drone LiDAR treated as research integration (UAV Phase III project)

**Cross-Section Standards (Section 104.09):**
- Cross-sections every **50 feet** for quantity determination
- Hard surfaces to nearest 0.01 foot; ground to nearest 0.1 foot
- Horizontal control points max 1,000 feet apart on tangent
- Bench marks every 1,000 feet

**Coordinate System:** Michigan State Plane (South most common), NAD83(2011), NAVD88; IGLD85 for Great Lakes projects

**CAD Format:** MDOT does not mandate a specific CAD format in Chapter 9 (e57/LAS/LAZ for point clouds; DXF/DWG common for design output)

**PLS Requirement:** Michigan requires licensed professional surveyor oversight for design surveys. No specific provisions found for electronic seals on drone deliverables in the current manual.

---

### 2. Ohio DOT (ODOT)

**Source:** [ODOT Aerial LiDAR Acquisition & Mapping Specifications January 2024](https://www.odot.org/survey/surveyInternet/conventional-survey-specs/Aerial%20LIDAR%20Acquisition%20&%20Mapping%20Specifications%20January%202024.pdf) | [ODOT Survey and Mapping Specifications](https://www.transportation.ohio.gov/working/engineering/cadd-mapping/survey-mapping-specs)

**LiDAR Accuracy and Density — Key Differentiator:**
- **Minimum point density: 40 pts/m²** — this is 5× USGS QL1 (8 pts/m²) and 20× QL2 (2 pts/m²)
- Horizontal datum: NAD83(2011)
- Image files: GSD < 2 inches (< 5.1 cm) — similar to TxDOT
- LAS format (not LAZ mentioned)

**Required Deliverables:**
- Raw LiDAR files in LAS format at 40+ pts/m²
- Trajectory file: SBET.OUT format
- Tiled GeoTIFF imagery with ABGPS text file (Imagestation-compatible)
- Ground Control File: Target #, X, Y, Z in .txt or .xls + KMZ file
- Open Roads Designer terrain file (Aerial Topo.dgn) containing all terrain/topographic data in ORD field book
- Final ground point / bare earth LAS file

**Notable Difference from Federal Standards:** ODOT's 40 pts/m² minimum is significantly more stringent than both USGS QL1 (8 pts/m²) and QL0 (20 pts/m²). This would require a dedicated high-density acquisition pass. The use of OpenRoads Designer (.dgn) as a required deliverable format distinguishes ODOT from other states using AutoCAD/DWG.

**Software Stack:** ODOT is standardized on Bentley OpenRoads Designer — deliverables must be in .dgn format, which is uncommon in other states. This is a material difference for robot operators who typically deliver DXF/DWG.

---

### 3. Texas DOT (TxDOT)

**Source:** [TxDOT Survey Manual (ESS), Revised March 2025](https://www.txdot.gov/content/dam/txdotoms/row/ess/ess.pdf) | [TxDOT UAS Aerial Mapping Specifications](https://www.txdot.gov/content/dam/docs/division/row/survey/uas-aerial-mapping-for-design.pdf) | [TxDOT Airborne LiDAR Specifications](https://www.txdot.gov/content/dam/docs/division/row/survey/airborne-lidar-for-design.pdf)

**Survey Manual Last Updated:** March 2025 (most current of all four states reviewed)

**UAS / Drone-Specific Specifications (dedicated document):**
- Targets ASPRS Class 1 accuracy for UAS aerial mapping
- GCP accuracy: TxDOT Level 3 specifications
- Aerial photography: minimum **5cm GSD** for 2D planimetric compilation
- UAS operations must comply with TxDOT UAS Flight Operations and User's Manual
- Integrated LiDAR + photogrammetry workflow (both sensors required together)
- Lidar ground-truthing report required as final deliverable

**Airborne LiDAR Specifications:**
- Vertical RMSEV: **±0.15 ft** (design-grade) to **±0.33 ft** (preliminary)
- Point density: **20-25 pts/m²** minimum for design-grade (higher than USGS QL0/QL1, lower than ODOT)
- Flight height: 1,500–4,000 ft AGL depending on coverage requirements
- ASPRS 1.2 (or above) classification required
- LAS/LAZ format (LAS 1.4 implied by current ASPRS standards)

**Cross-Sections / Design Survey:**
- Feature measurement intervals: 25 ft maximum for manmade features; 50 ft for natural features
- Cross-section precision: <0.2 ft for PS&E surveys; <1 ft for schematic surveys
- This is effectively **25-50 ft intervals** (similar to MDOT 50 ft default)

**CAD Format:** AutoCAD DGN/DWG per TxDOT CAD Standards (both formats; note: TxDOT historically uses MicroStation DGN but also accepts AutoCAD DWG)

**Coordinate System:** NAD83(2011) Texas State Plane (5 zones — North, North Central, Central, South Central, South); NAVD88 via GEOID18

**PLS Requirement:** Texas requires RPLS (Registered Professional Land Surveyor) oversight. Electronic seals regulated by Texas Board of Professional Engineers and Land Surveyors.

---

### 4. California DOT (Caltrans)

**Source:** [Caltrans Survey Manual — Chapter 15 Terrestrial Laser Scanning](https://dot.ca.gov/-/media/dot-media/programs/right-of-way/documents/ls-manual/15-surveys-a11y.pdf) | [Caltrans Surveys Manual main page](https://dot.ca.gov/programs/right-of-way/surveys-manual-and-interim-guidelines) | [Chapter 5 — Classifications of Accuracy](https://dot.ca.gov/-/media/dot-media/programs/right-of-way/documents/ls-manual/05-surveys-a11y.pdf)

**Type A / Type B Classification (not USGS QL):**
- **Type A** = high-accuracy hard surface survey for engineering/forensics
  - Hz ≤ 0.03 ft; Z ≤ 0.02 ft local positional accuracy
  - All horizontal project control: minimum 2 cm network accuracy
- **Type B** = lower-accuracy topographic survey for asset inventory, environmental, earthwork
  - Local registration point targets at max 3,000-ft spacing (both sides of roadway)
  - Vertical local registration points between painted targets at 1,500 ft intervals

**Notable:** Caltrans does not use USGS Quality Levels in their primary standards framework. They use their own Type A/B classification. RFPs from Caltrans districts may reference NVA/VVA (federal) but the primary accuracy language is in feet with Type A/B classification.

**Deliverables:**
- Point cloud specified as deliverable from LiDAR surveys
- Survey narrative report required (geospatial metadata conforming to current Caltrans standard)
- NAD83 coordinate system (specific zone determined by project location — 6 zones in CA)
- NAVD88 vertical datum

**UAS/Drone:** Caltrans has a Mobile Terrestrial Laser Scanning (MTLS) Guidelines document supporting a statewide MTLS system. Aerial/drone LiDAR for design-grade is an evolving area; Chapter 15 covers TLS but drone LiDAR accuracy testing has been conducted (GeoCue article references Caltrans true-view accuracy testing).

**Coordinate System:** NAD83 State Plane California Zones 1–6 (EPSG 2225–2230); NAVD88 vertical

**PLS Requirement:** California requires a Licensed Land Surveyor (LLS, equivalent to PLS in other states) in responsible charge. Electronic seal provisions exist but are subject to California BPC Section 8726.

---

### 5. North Carolina DOT (NCDOT) — Supplementary

**Source:** [NCDOT Aerial Surveying with Drones page](https://connect.ncdot.gov/resources/Photogrammetry/Pages/Aerial-Surveying-With-Drones.aspx) | [NCDOT LiDAR Applications in Transportation (NGAC presentation, April 2024)](https://www.fgdc.gov/ngac/meetings/april-2024/ncdot-lidar-applications-in-transportation-ngac.pdf)

- Uses USGS QL framework as primary reference
- Statewide LiDAR baseline: 19.6 cm (0.64 ft) NVA at 95% confidence (QL2 equivalent)
- Photogrammetry Unit operates DJI Inspire 2 + Zenmuse X4s 20MP camera; uses SfM for orthophotos and DEMs
- PLS oversight required for survey-grade products
- NCDOT uses its own internal photogrammetry specs for drone mapping (no single published standard found)

---

### 6. Federal / Baseline Standards (Reference)

**USGS LiDAR Base Specification (LBS) 2025 rev. A:**

| QL | NVA (cm) | VVA (cm) | Min Density (pts/m²) | Typical DOT Use |
|---|---|---|---|---|
| QL0 | ≤5.0 | ≤7.6 | ≥20 | Bridge/airport, corridor |
| QL1 | ≤10.0 | ≤15.0 | ≥8 | Design-grade highway |
| QL2 | ≤10.0 | ≤15.0 | ≥2 | Standard topographic |
| QL3 | ≤20.0 | N/A | ≥0.5 | Reconnaissance |

All deliverables: LAS 1.4-R15, Point Data Record Format 6, 7, 8, 9, or 10. Minimum 3 returns per pulse.

**ASPRS 2024 Edition 2 updates (relevant for bid scoring):**
- Renamed RMSE terms (RMSEX, RMSEY, RMSEZ)
- VVA changes: projects can no longer fail solely for VVA
- Minimum checkpoint count raised from 20 to 30 (max 120 for large projects)

---

## Multi-State Comparison Table

| Dimension | MDOT (MI) | ODOT (OH) | TxDOT (TX) | Caltrans (CA) |
|---|---|---|---|---|
| Accuracy framework | Ft-based (design manual) | USGS QL + state density req | ASPRS Class 1 / Level 3 | Type A / Type B |
| LiDAR min density | ~0.3 ft spacing (terrestrial) | **40 pts/m²** | 20–25 pts/m² | N/A (TLS-focused) |
| USGS QL equivalent | QL1 (implied) | Super-QL0 (5× QL1) | ~QL0 | Type A ≈ QL0 |
| Vertical accuracy (design) | ±0.01–0.05 ft | Not specified separately | ±0.15 ft RMSEV | Z ≤ 0.02 ft |
| Cross-section interval | 50 ft | Not specified (aerial topo) | 25–50 ft | Not specified in manual |
| Primary LAS format | LAS/LAZ 1.4 | LAS (not LAZ specified) | LAS/LAZ 1.4 | LAS (implied) |
| Required CAD format | e57/LAS/DXF | .dgn (OpenRoads) | DGN/DWG (TxDOT CAD Std) | Not mandated |
| Coordinate system | NAD83(2011) MI State Plane | NAD83(2011) | NAD83(2011) TX State Plane | NAD83 CA State Plane |
| Vertical datum | NAVD88 (IGLD85 for lakes) | NAVD88 | NAVD88 (GEOID18) | NAVD88 |
| PLS/RPLS/LLS req | Yes | Yes | Yes (RPLS) | Yes (LLS) |
| UAS-specific spec | Research phase | Not found | Dedicated UAS document | TLS-focused; evolving |
| Manual last updated | 2014 (standards) / wiki current | Jan 2024 | March 2025 | Chapter 15 (2015+) |

---

## Implications for the Product

### 1. The Current RFP Processor Defaults are Michigan-Only

The `rfp_processor.py` module loads `michigan-standards.md` and `aashto-federal-standards.md`. For ODOT projects, the defaults will produce incorrect specs because:
- MDOT defaults 50 ft cross-section intervals; ODOT uses aerial topo with OpenRoads deliverables
- No state detection logic exists in the current processor for ODOT-specific requirements (40 pts/m², .dgn)

### 2. ODOT's 40 pts/m² Requirement Affects Bid Pricing Significantly

At 40 pts/m², operators need specialized high-density airborne LiDAR systems (not consumer drones). A DJI Matrice 350 + Zenmuse L2 at standard flight altitude achieves ~8–15 pts/m² — below ODOT minimums. Operators would need manned aircraft or specialized UAV LiDAR setups. This creates a distinct operator tier for Ohio work that the current bid scoring doesn't account for.

### 3. ODOT's .dgn Deliverable Requirement is a Material Constraint

Most drone operators deliver DXF/DWG/LAS. ODOT requires Bentley OpenRoads Designer (.dgn) terrain models — software that costs ~$5,000/seat. This is a filter on which operators can legally fulfill Ohio work. The compliance module should check this.

### 4. TxDOT Has the Most RFP-Ready Standards

TxDOT's dedicated UAS document (ASPRS Class 1, 5cm GSD, 20-25 pts/m²) is well-suited for automated parsing. The March 2025 Survey Manual revision makes TxDOT the most current reference. Adding a `txdot-standards.md` reference file to the rfp-to-robot-spec skill would improve accuracy for the large Texas market.

### 5. Caltrans Type A/B ≠ USGS QL — Mapping Required

An RFP from Caltrans that says "Type A survey" means Z ≤ 0.02 ft (≈0.6 cm), which is stricter than USGS QL0. The current parser has no mapping for Caltrans Type A/B terminology. Misinterpreting "Type B" as a lower-accuracy standard could cause incorrect ASPRS class assignment.

### 6. State Plane Zone Auto-Detection

All four states use different State Plane coordinate system zones. The existing `standards-reference.md` has EPSG codes for major zones, but the RFP processor has no logic to auto-detect the correct zone from project location. For Texas (5 zones) and California (6 zones), using the wrong EPSG code is a material error in the task spec.

---

## Improvement Proposals

**IMP-017:** Add state-detection logic to `rfp_processor.py` — extract state/agency from RFP header and load the appropriate standards reference.

**IMP-018:** Create `txdot-standards.md` reference file for the rfp-to-robot-spec skill, mirroring `michigan-standards.md` structure.

**IMP-019:** Add ODOT-specific constraints to the compliance module — flag tasks requiring 40+ pts/m² and .dgn deliverables as requiring specialized operator capabilities.

**IMP-020:** Add Caltrans Type A/B → ASPRS class mapping to `standards-reference.md` and the RFP processor keyword extraction logic.

---

## New Questions Spawned

- **R-029:** ODOT OpenRoads Designer operator capability survey — how many drone survey operators in Ohio can deliver .dgn terrain models? Is this a market gap or a deal-breaker?
- **R-030:** TxDOT UAS operator approval process — does TxDOT require operator pre-approval or just Part 107? Their dedicated UAS manual implies tighter controls.
- **R-031:** State Plane zone auto-detection from project address — what's the best open-source library or API for converting a project address to the correct EPSG code?

---

## Sources

- [MDOT Design Survey Manual Wiki — Chapter 9 Remote Sensing](https://mdotwiki.state.mi.us/design/index.php/Chapter_9_-_Remote_Sensing)
- [MDOT Design Survey Manual (TC.1)](https://mdotjboss.state.mi.us/stdplan/surveymanual.htm)
- [MDOT Standards of Practice, May 2014](https://mdotjboss.state.mi.us/SpecProv/getPubDoc.htm?docGuid=0d2aa85b-f99d-4c1a-9c03-0121f7d6a321&fileName=%22MDOT_Survey_Standards_2014.pdf%22)
- [ODOT Aerial LiDAR Acquisition & Mapping Specifications January 2024](https://www.odot.org/survey/surveyInternet/conventional-survey-specs/Aerial%20LIDAR%20Acquisition%20&%20Mapping%20Specifications%20January%202024.pdf)
- [ODOT Survey and Mapping Specifications page](https://www.transportation.ohio.gov/working/engineering/cadd-mapping/survey-mapping-specs)
- [TxDOT Survey Manual (ESS) Revised March 2025](https://www.txdot.gov/content/dam/txdotoms/row/ess/ess.pdf)
- [TxDOT UAS Aerial Mapping Specifications for Design-Grade](https://www.txdot.gov/content/dam/docs/division/row/survey/uas-aerial-mapping-for-design.pdf)
- [TxDOT Airborne LiDAR Specifications for Design-Grade](https://www.txdot.gov/content/dam/docs/division/row/survey/airborne-lidar-for-design.pdf)
- [TxDOT Surveyors' Toolkit](https://www.txdot.gov/business/resources/surveyor-toolkit.html)
- [Caltrans Surveys Manual — main page](https://dot.ca.gov/programs/right-of-way/surveys-manual-and-interim-guidelines)
- [Caltrans Survey Manual Chapter 15 — Terrestrial Laser Scanning](https://dot.ca.gov/-/media/dot-media/programs/right-of-way/documents/ls-manual/15-surveys-a11y.pdf)
- [Caltrans Survey Manual Chapter 5 — Classifications of Accuracy](https://dot.ca.gov/-/media/dot-media/programs/right-of-way/documents/ls-manual/05-surveys-a11y.pdf)
- [NCDOT Aerial Surveying with Drones](https://connect.ncdot.gov/resources/Photogrammetry/Pages/Aerial-Surveying-With-Drones.aspx)
- [NCDOT LiDAR Applications in Transportation — NGAC April 2024](https://www.fgdc.gov/ngac/meetings/april-2024/ncdot-lidar-applications-in-transportation-ngac.pdf)
- [USGS LiDAR Base Specification (LBS) — Topographic Data Quality Levels](https://www.usgs.gov/3d-elevation-program/topographic-data-quality-levels-qls)
- [USGS LBS Tables](https://www.usgs.gov/ngp-standards-and-specifications/lidar-base-specification-tables)
- [Mobile LiDAR DOT Digital Delivery Guide 2025](https://iscano.com/real-world-applications-laser-scanning-lidar/mobile-lidar-services-dot-digital-delivery-guide/)
