# R-031: State Plane Zone Auto-Detection from Project Address or Coordinates

**Date:** 2026-04-05
**Topic ID:** R-031
**Module:** M1_rfp_processor
**Priority:** High
**Depends on:** R-001

---

## Executive Summary

- The `stateplane` Python library (pip-installable, pyproj wrapper) can reliably convert `(lon, lat)` to the correct State Plane EPSG code with a single call — `stateplane.identify(lon, lat)`. This is the lowest-friction path to correct zone assignment.
- The existing `standards-reference.md` EPSG table contains **incorrect EPSG codes for Michigan and Ohio** — the codes listed (2111-2113, 3401-3402) are wrong and will produce coordinate system errors in any downstream CRS operation. Correct values are 2251/2252/2253 (MI) and 3734/3735 (OH).
- The full pipeline — address → county FIPS → State Plane EPSG — can be assembled from three free components: Census Geocoder API / `censusgeocode` library (address → lat/lon + county FIPS), `stateplane.identify()` (lat/lon → EPSG), and a static county-FIPS-to-EPSG lookup as a zero-API-call fallback.
- `stateplane` 0.5.0 (released November 2022) is the latest version and Python 3.7–3.9 is listed in metadata, but it installs and runs on Python 3.12 in practice. It is a thin pyproj wrapper and unlikely to break.
- The `rfp_processor.py` currently falls back to `"State Plane"` (no EPSG) for MI and `"UTM"` for all other states — both are incorrect for production use. The fix is a two-line call.

---

## Findings

### 1. `stateplane` Library — Primary Recommended Tool

**Source:** https://pypi.org/project/stateplane/ | https://github.com/fitnr/stateplane

- `pip install stateplane` — no C++ dependency, pure Python wrapper over pyproj
- Latest release: 0.5.0, November 25, 2022. GPLv3. Author: Neil Freeman (fitnr).
- Status: beta, no recent commits, but stable because it is a thin wrapper. The underlying data (FIPS-to-EPSG county mapping) is static reference data that does not change.

**Key API:**
```python
import stateplane

# From coordinates (lon, lat) — returns EPSG int
epsg = stateplane.identify(-84.0, 42.3)          # → 2253 (MI South)
epsg = stateplane.identify(-95.3, 29.7)          # → 2278 (TX South Central)
epsg = stateplane.identify(-118.2, 34.0)         # → 2229 (CA Zone 5 — LA area)

# With state FIPS for faster lookup (avoids scanning all counties)
epsg = stateplane.identify(-84.0, 42.3, statefp="26")  # Michigan FIPS = 26

# With county FIPS (5-digit) — fastest, zero ambiguity
epsg = stateplane.identify(-84.0, 42.3, countyfp="26163")  # Wayne County, MI

# Short-name format (e.g., 'MI_S')
name = stateplane.identify(-84.0, 42.3, fmt='short')  # → 'MI_S'

# FIPS format (State Plane FIPS code, not county FIPS)
fips = stateplane.identify(-84.0, 42.3, fmt='fips')   # → '2113' (State Plane FIPS)
```

**Coverage:** All 50 states + DC, Puerto Rico, American Samoa, Guam, US Virgin Islands.

**Limitation:** Last release Nov 2022. No active maintenance. No Python 3.10+ classifiers, but works in practice. GPLv3 license may conflict with commercial code — check with counsel if distributing. Alternative: inline the county-FIPS-to-EPSG static table (free of license constraint, zero runtime dependency).

---

### 2. State Plane EPSG Reference — Correct Codes for Target Markets

All codes below are NAD83, US Survey Feet (ftUS), as required by state DOTs.

**Michigan (3 zones) — State FIPS: 26**

| Zone | EPSG (correct) | EPSG (in standards-reference.md — WRONG) | Counties |
|------|---------------|------------------------------------------|---------|
| Michigan North | **2251** | 2111 (wrong) | UP: Alger, Baraga, Chippewa, Delta, Dickinson, Gogebic, Houghton, Iron, Keweenaw, Luce, Mackinac, Marquette, Menominee, Ontonagon, Schoolcraft |
| Michigan Central | **2252** | 2112 (wrong) | Northern LP: Alcona, Alpena, Antrim, Arenac, Benzie, Charlevoix, Cheboygan, Clare, Crawford, Emmet, Gladwin, Grand Traverse, Iosco, Kalkaska, Lake, Leelanau, Manistee, Mason, Missaukee, Montmorency, Ogemaw, Osceola, Oscoda, Otsego, Presque Isle, Roscommon, Wexford |
| Michigan South | **2253** | 2113 (wrong) | Southern LP: most populated — Wayne (Detroit), Kent (Grand Rapids), Oakland, Washtenaw, Ingham, Kalamazoo, etc. |

Source: https://epsg.io/2251 | https://epsg.io/2252 | https://epsg.io/2253

**Ohio (2 zones) — State FIPS: 39**

| Zone | EPSG (correct) | EPSG (in standards-reference.md — WRONG) | Counties |
|------|---------------|------------------------------------------|---------|
| Ohio North | **3734** | 3401 (wrong) | 45 counties including Cuyahoga (Cleveland), Franklin (Columbus), Summit (Akron), Lorain, Medina |
| Ohio South | **3735** | 3402 (wrong) | 37 counties including Hamilton (Cincinnati), Montgomery (Dayton), Butler |

Source: https://epsg.io/3734 | https://epsg.io/3735

**Texas (5 zones) — State FIPS: 48**

| Zone | EPSG | FIPS | Key Counties |
|------|------|------|-------------|
| TX North | 2275 | 4201 | Amarillo area — Armstrong, Carson, Potter, Randall, etc. |
| TX North Central | 2276 | 4202 | Dallas/Fort Worth — Dallas, Tarrant, Collin, Denton, etc. |
| TX Central | 2277 | 4203 | Austin/San Antonio metro — Travis, Williamson, Bell, McLennan |
| TX South Central | 2278 | 4204 | Houston/San Antonio — Harris, Bexar, Fort Bend, Galveston |
| TX South | 2279 | 4205 | Rio Grande Valley — Hidalgo, Cameron, Webb, Nueces |

Source: https://epsg.io/2275 through 2279 | https://www.eye4software.com/hydromagic/documentation/state-plane-coordinate-systems/Texas

**California (6 zones) — State FIPS: 06**

| Zone | EPSG (ftUS) | EPSG (meters) | Counties |
|------|------------|---------------|---------|
| CA Zone 1 | 2225 | 26941 | Del Norte, Humboldt, Siskiyou, Trinity, Shasta, Tehama, Modoc, Lassen, Plumas |
| CA Zone 2 | 2226 | 26942 | Alpine, Amador, Butte, Colusa, El Dorado, Glenn, Lake, Mendocino, Napa, Nevada, Placer, Sacramento, Sierra, Solano, Sonoma, Sutter, Yolo, Yuba |
| CA Zone 3 | 2227 | 26943 | Alameda, Calaveras, Contra Costa, Madera, Marin, Mariposa, Merced, Mono, San Francisco, San Joaquin, San Mateo, Santa Clara, Santa Cruz, Stanislaus, Tuolumne |
| CA Zone 4 | 2228 | 26944 | Fresno, Inyo, Kings, Tulare |
| CA Zone 5 | 2229 | 26945 | Kern, Los Angeles, San Bernardino, San Luis Obispo, Santa Barbara, Ventura |
| CA Zone 6 | 2230 | 26946 | Imperial, Orange, Riverside, San Diego |

Source: https://epsg.io/2225 through 2230 | https://www.conservation.ca.gov/cgs/rgm/state-plane-coordinate-system

---

### 3. Address-to-EPSG Pipeline: Full Chain

When `site_info.coordinates` is not provided, the RFP processor must derive the zone from other inputs. The full chain:

**Step 1: Address or RFP text → lat/lon + county FIPS**

Option A — `censusgeocode` (free, no API key, US Census Bureau):
```python
import censusgeocode as cg
result = cg.address("1 Woodward Ave", city="Detroit", state="MI", zip="48226")
county_fips = result[0]["geographies"]["Counties"][0]["GEOID"]  # "26163" (Wayne)
lat = float(result[0]["coordinates"]["y"])
lon = float(result[0]["coordinates"]["x"])
```
Source: https://pypi.org/project/censusgeocode/ | https://github.com/fitnr/censusgeocode

Option B — FCC Area API (free, no key, REST only):
```
GET https://geo.fcc.gov/api/census/block/find?latitude={lat}&longitude={lon}&format=json
→ returns county FIPS, state FIPS, county name
```
Source: https://www.fcc.gov/general/census-block-conversions-api-v100 | https://gist.github.com/ramhiser/f09a71d96a4dec80994c

**Step 2: lat/lon → State Plane EPSG**

```python
import stateplane
epsg = stateplane.identify(lon, lat)  # returns int EPSG code
```

**Step 3 (fallback, no network): county FIPS → EPSG via static table**

The `stateplane` package ships `stateplane/counties.json` — a county-FIPS-to-EPSG mapping. This table can be bundled directly into the rfp_processor module as a ~5KB dict constant. Zero API calls, zero dependencies, deterministic.

---

### 4. pyproj `query_crs_info` — Programmatic Alternative

pyproj 3.x (already in our stack as stateplane's dependency) exposes:

```python
from pyproj.database import query_crs_info, CRSInfo
from pyproj.enums import PJType

# Expensive but dependency-free from stateplane
results = query_crs_info(
    auth_name="EPSG",
    pj_types=PJType.PROJECTED_CRS,
    area_of_interest=(lon_min, lat_min, lon_max, lat_max)
)
# Filter for "State Plane" in name
sp_results = [r for r in results if "State Plane" in r.name]
```

This works but returns multiple candidates (both meters and feet variants) requiring additional filtering. It is more flexible than `stateplane` but also more verbose. Use `stateplane` for the 50-state common case; use `query_crs_info` for unusual territories or when you need the NAD83(2011) realization (EPSG 6416–6426 for CA).

Source: https://pyproj4.github.io/pyproj/stable/api/database.html

---

### 5. NAD83 vs. NAD83(2011) — Which Realization?

TxDOT (March 2025 manual) and newer Caltrans projects specify NAD83(2011) — the updated realization using NATRF2022. For existing projects, "NAD83" (original 1986 realization) is still standard.

| Realization | TX Example | CA Example | Notes |
|-------------|-----------|-----------|-------|
| NAD83 (original) | 2275–2279 | 2225–2230 | Standard for existing work |
| NAD83(2011) | 6584–6588 | 6416–6426 | Required for some new TxDOT/Caltrans contracts |

For v1 rfp_processor, default to NAD83 original (2275–2279, 2225–2230). Add a `use_nad83_2011=True` flag for future TxDOT/Caltrans compliance.

---

### 6. Current Code Gap in rfp_processor.py

In `_build_task_spec()` (line ~306), the coordinate system is set as:
```python
"preferred_coordinate_system": "State Plane" if jurisdiction == "MI" else "UTM",
```

This has two problems:
1. No EPSG code is assigned — "State Plane" is a human label, not a CRS specification
2. Non-Michigan states default to "UTM" — incorrect for TX, CA, OH which use State Plane

The correct fix is to:
1. Detect the zone from `site_info.get("coordinates")` if provided
2. Fall back to `_infer_state_plane_epsg(jurisdiction, site_info)` using a static county table
3. Emit `"crs_epsg": 2253` (not a string label) in the soft constraints

---

## Implications for the Product

1. **The existing EPSG table in standards-reference.md is wrong.** Michigan codes 2111/2112/2113 and Ohio codes 3401/3402 will silently produce incorrect projections. Any GC or surveyor who checks the task spec's CRS will see incorrect values and lose trust in the platform. This must be fixed before any live tasks are posted.

2. **`stateplane.identify()` is the right default tool.** pip-installable, no compilation, 50-state coverage, single-call API. The GPLv3 license requires legal review if distributing, but the alternative (inline static county table) avoids the issue entirely.

3. **The address → EPSG pipeline is viable with zero paid APIs.** Census Geocoder (free, no key) + stateplane covers the full chain. FCC API is a backup for coordinate-only input.

4. **The rfp_processor coordinate system field must emit an EPSG integer, not a string label.** Downstream operators and deliverable QA (M35) need a machine-readable CRS.

5. **NAD83(2011) variants may be needed for TxDOT contracts by 2026.** The 2025 TxDOT manual update (found in R-001) emphasizes GEOID18/NGS OPUS workflows that imply NAD83(2011). Add a flag now, activate later.

---

## Improvement Proposals

### IMP-021: Fix incorrect EPSG codes in standards-reference.md
- **What:** Replace 2111→2251 (MI North), 2112→2252 (MI Central), 2113→2253 (MI South), 3401→3734 (OH North), 3402→3735 (OH South) in `standards-reference.md`. These are silent data errors in a reference file read by LLM during RFP parsing.
- **Module:** M1_rfp_processor
- **Effort:** small
- **Priority:** critical (silent error, active reference file)

### IMP-022: Add `stateplane` dependency + `_infer_state_plane_epsg()` helper to rfp_processor.py
- **What:** Add `pip install stateplane` to pyproject.toml extras. Implement `_infer_state_plane_epsg(jurisdiction, site_info) -> int` that: (1) uses `site_info["coordinates"]` if present → `stateplane.identify(lon, lat)`; (2) falls back to jurisdiction→default-zone static dict; (3) returns EPSG int. Replace the `"preferred_coordinate_system"` string field with `"crs_epsg": <int>` in task spec soft constraints.
- **Module:** M1_rfp_processor
- **Effort:** medium
- **Priority:** high

### IMP-023: Add complete EPSG table for 4-state target markets to standards-reference.md
- **What:** Replace the partial/incorrect EPSG table in `standards-reference.md` with a complete table covering all zones for MI (3), OH (2), TX (5), and CA (6) — 16 entries total. Include both ftUS EPSG and NAD83(2011) EPSG for each zone. Add a county-to-zone assignment note for multi-zone states.
- **Module:** M1_rfp_processor
- **Effort:** small
- **Priority:** high

---

## New Questions Spawned

- **R-032:** For addresses in the RFP that lack coordinates, which geocoder is most reliable for DOT project descriptions (e.g., "SR-89A between Petoskey and Cheboygan")? Route-based geocoding may require TIGER/Line road network lookup rather than address matching.
- **R-033:** TxDOT March 2025 manual specifies GEOID18 for vertical. Should the rfp_processor set `vertical_datum_epsg: 5703` (NAVD88) always, or detect state and select GEOID18/GEOID12B? What is the EPSG for GEOID18-realized heights?

---

## Sources

- stateplane PyPI: https://pypi.org/project/stateplane/
- stateplane GitHub: https://github.com/fitnr/stateplane
- stateplane README (fitnr): https://github.com/fitnr/stateplane/blob/master/README.md
- EPSG MI South (2253): https://epsg.io/2253
- EPSG MI Central (2252): https://epsg.io/2252
- EPSG MI North (2251): https://epsg.io/2251
- EPSG OH North (3734): https://epsg.io/3734
- EPSG OH South (3735): https://epsg.io/3735
- EPSG TX zones: https://epsg.io/2275 through https://epsg.io/2279
- EPSG CA zones: https://epsg.io/2225 through https://epsg.io/2230
- TX State Plane county map: https://www.eye4software.com/hydromagic/documentation/state-plane-coordinate-systems/Texas
- CA State Plane zones: https://www.conservation.ca.gov/cgs/rgm/state-plane-coordinate-system
- Caltrans Type A/B: https://spatialreference.org/ref/?search=california
- censusgeocode PyPI: https://pypi.org/project/censusgeocode/
- censusgeocode GitHub: https://github.com/fitnr/censusgeocode
- FCC Census Block API: https://www.fcc.gov/general/census-block-conversions-api-v100
- FCC lat/lon to FIPS gist: https://gist.github.com/ramhiser/f09a71d96a4dec80994c
- pyproj database API: https://pyproj4.github.io/pyproj/stable/api/database.html
- pyproj CRS docs: https://pyproj4.github.io/pyproj/stable/api/crs/crs.html
- State Plane FIPS/EPSG master list: https://gist.github.com/fitnr/10795511
- ArcGIS USA State Plane Zones NAD83: https://hub.arcgis.com/maps/esri::usa-state-plane-zones-nad83
- NOAA SPCS overview: https://geodesy.noaa.gov/SPCS/
