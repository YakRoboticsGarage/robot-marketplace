---
name: rfp-to-site-recon
description: Generate a site reconnaissance and execution context report from construction RFP data and public information sources. Run in parallel with rfp-to-robot-spec. Use whenever robot task specs have been generated and need execution-level detail before a robot can mobilize. Also trigger when someone asks "what does the robot need to know before going to the site", "site recon", "execution planning", "pre-mobilization", or "flight planning."
---

# RFP → Site Reconnaissance Report

Generate the physical execution context a robot needs to actually perform a survey task. This skill runs AFTER or IN PARALLEL with rfp-to-robot-spec. It takes the same RFP input but produces operational intelligence, not auction specs.

Every field in the output is tagged with its source confidence:

- `RFP` — value is explicitly stated in the RFP document
- `LOOKUP` — value derived from a specific public data source (URL required)
- `INFERRED` — value estimated from context (reasoning required, confidence percentage)
- `UNKNOWN` — value cannot be determined without site visit or client confirmation

Fields tagged `INFERRED` or `UNKNOWN` are presented to the operator as a pre-mobilization checklist. The robot does NOT assume these values are correct.

## Workflow

### 1. Accept input

Same input as rfp-to-robot-spec: RFP text, file, URL, or description. If task specs from rfp-to-robot-spec are also available, reference them to avoid re-extracting what's already known.

### 2. Extract location and scope

From the RFP, identify:
- Project location (address, highway mile markers, coordinates if given)
- Geographic extent (acreage, corridor length, structure count)
- Agency and jurisdiction

### 3. Look up site data from public sources

For each category below, query the specified public data source. If the source is unavailable or doesn't cover the area, tag as `UNKNOWN`.

Read `references/public-data-sources.md` for the full source list and query methods.

**Airspace:**
- FAA UAS Facility Map / LAANC grid → airspace class, max AGL per grid cell
- FAA Digital Obstacle File → towers, antennas, power lines near site
- TFRs (Temporary Flight Restrictions) → active NOTAMs for area

**Site geometry:**
- County GIS / parcel data → site boundary polygon (WKT or GeoJSON)
- USGS National Map / NED → terrain elevation, slope, land cover
- Google Earth / satellite imagery → recent aerial view, visible obstructions

**Infrastructure:**
- State DOT road network → active road classifications, speed limits, traffic volumes
- National Bridge Inventory → bridge locations, condition ratings, inspection history
- NPDES / state environmental GIS → wetlands, floodplains, protected areas

**Weather:**
- NOAA climate normals → temperature, precipitation, wind averages for the project timeline
- Historical wind data → P90 wind speed for the site (drone flight planning)

**Utilities:**
- State 811 / Miss Dig / Call Before You Dig → utility locate requirements
- FCC antenna database → communication tower locations

### 4. Classify each field

For every field in the output, attach exactly one tag:

```json
{
  "value": "Class G airspace, max 400ft AGL",
  "source": "LOOKUP",
  "source_url": "https://faa.maps.arcgis.com/apps/webappviewer/...",
  "queried_date": "2026-03-28"
}
```

For `INFERRED`:
```json
{
  "value": "Asphalt surface, based on satellite imagery showing parking lot",
  "source": "INFERRED",
  "confidence": 0.75,
  "reasoning": "Google Earth imagery from 2025-11 shows paved surface, but construction activity visible — surface may have changed"
}
```

For `UNKNOWN`:
```json
{
  "value": null,
  "source": "UNKNOWN",
  "required_from": "client",
  "question": "Is the outlet conduit dewatered or under flow? What is current water level?"
}
```

### 5. Generate site recon report

Output structure:

```json
{
  "project_reference": "links to rfp-to-robot-spec task ID if available",
  "site_boundary": { "value": "POLYGON((...))", "source": "LOOKUP", "source_url": "..." },
  "access_points": [
    { "value": {"lat": 42.96, "lon": -85.67, "description": "..."}, "source": "INFERRED|LOOKUP|UNKNOWN" }
  ],
  "airspace": {
    "class": { "value": "G", "source": "LOOKUP", "source_url": "..." },
    "max_altitude_agl_ft": { "value": 400, "source": "LOOKUP" },
    "laanc_required": { "value": false, "source": "LOOKUP" },
    "coa_required": { "value": false, "source": "RFP|LOOKUP" },
    "active_tfrs": { "value": [], "source": "LOOKUP" },
    "obstacles_within_1nm": { "value": [...], "source": "LOOKUP", "source_url": "..." }
  },
  "terrain": {
    "elevation_range_ft": { "value": [620, 645], "source": "LOOKUP" },
    "max_slope_pct": { "value": 8, "source": "LOOKUP" },
    "land_cover": { "value": "developed/paved + undeveloped grassland", "source": "LOOKUP" }
  },
  "surface_conditions": {
    "materials": { "value": ["asphalt", "concrete", "grass"], "source": "INFERRED", "confidence": 0.7 },
    "current_state": { "value": null, "source": "UNKNOWN", "question": "Is there active construction on site? Mud, stockpiles, equipment?" }
  },
  "access_and_safety": {
    "access_hours": { "value": null, "source": "UNKNOWN", "question": "What are site access hours? Is escort required?" },
    "safety_requirements_from_rfp": { "value": ["hard_hat", "high_vis"], "source": "RFP" },
    "traffic_control_required": { "value": true, "source": "RFP|INFERRED" },
    "active_operations": { "value": null, "source": "UNKNOWN", "question": "Is the site active during survey window?" }
  },
  "weather_window": {
    "avg_temp_f": { "value": [45, 72], "source": "LOOKUP", "source_url": "NOAA" },
    "avg_wind_mph": { "value": 8, "source": "LOOKUP" },
    "p90_wind_mph": { "value": 18, "source": "LOOKUP" },
    "rain_days_per_month": { "value": 9, "source": "LOOKUP" },
    "recommended_months": { "value": ["May", "Jun", "Jul", "Aug", "Sep"], "source": "INFERRED" }
  },
  "utilities": {
    "dig_notification_required": { "value": true, "source": "LOOKUP" },
    "dig_notification_service": { "value": "Michigan 811 (Miss Dig)", "source": "LOOKUP", "source_url": "https://missdig811.org" },
    "known_utilities_from_rfp": { "value": ["storm sewer", "sanitary", "water main", "gas", "electric"], "source": "RFP" }
  },
  "prior_data": {
    "nbi_bridges_on_site": { "value": [], "source": "LOOKUP" },
    "existing_lidar_available": { "value": "USGS 3DEP QL2 2019", "source": "LOOKUP" },
    "existing_ortho_available": { "value": "NAIP 2023 60cm", "source": "LOOKUP" }
  },
  "pre_mobilization_checklist": [
    "Confirm site access hours and escort requirements with client",
    "Verify current surface conditions (active construction may have altered site)",
    "Place ground control points (30 panels at 1000-ft intervals) — confirm GCP placement crew",
    "File LAANC authorization for flight area",
    "Notify Michigan 811 for utility locates (72-hour lead time)",
    "Check NOTAM/TFR status day-of-flight"
  ]
}
```

### 6. Validate

Run the validation script to ensure all fields have source tags:

```bash
python scripts/validate_site_recon.py < recon.json
```

This checks: every field has a `source` tag, every `LOOKUP` has a `source_url`, every `INFERRED` has `confidence` and `reasoning`, every `UNKNOWN` has a `question`.

## References

- `references/public-data-sources.md` — comprehensive list of public APIs and GIS portals for each data category, with query methods
- Shares references with rfp-to-robot-spec: `../rfp-to-robot-spec/references/` for standards and robot mapping

## Relationship to rfp-to-robot-spec

These skills serve different consumers:
- **rfp-to-robot-spec** → consumed by the **auction engine** (what to bid on)
- **rfp-to-site-recon** → consumed by the **winning operator** (how to execute)

They can run in parallel on the same RFP. The site recon report is delivered to the operator after they win the auction, not before — it's execution intelligence, not bidding information.
