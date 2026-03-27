---
name: rfp-to-robot-spec
description: Process construction RFP documents into structured robot task specifications. Use this skill when the user uploads, pastes, or references a construction RFP, bid document, survey scope, or project specification and wants to extract the survey/inspection requirements into a machine-readable format for the robot marketplace. Also trigger when the user says "parse this RFP", "extract specs", "what robots do we need for this project", or references MDOT, DOT, highway, bridge, or construction survey documents.
---

# RFP to Robot Task Spec

Convert construction RFP documents into structured JSON task specifications that can be posted directly to the YAK ROBOTICS marketplace auction engine.

## Input

The user provides one of:
- A pasted RFP document or excerpt
- A file path to a PDF or text document
- A URL to a public bid document
- A project description with survey requirements

## Process

### Step 1: Extract Survey Requirements

Read the entire document and identify ALL survey, inspection, measurement, and data collection requirements. Look for:

- **Survey types**: topographic, as-built, control, alignment, hydraulic, photogrammetric, bridge/structure
- **Accuracy requirements**: horizontal, vertical, point density (in feet, cm, or metric)
- **Deliverable formats**: LandXML, DXF, DWG, GeoTIFF, LAS/LAZ, CSV, PDF reports
- **Area/scope**: acreage, linear feet, number of structures
- **Coordinate systems**: NAD83, state plane zones, datums (NAVD88, IGLD85)
- **Certifications required**: FAA Part 107, licensed surveyor, OSHA, confined space
- **Standards referenced**: MDOT sections, AASHTO, NCHRP, USGS QL levels, FEMA
- **Timeline constraints**: letting date, completion deadline, seasonal restrictions
- **Special conditions**: traffic control, environmental restrictions, utility conflicts

### Step 2: Map to Michigan Standards (when applicable)

Cross-reference extracted requirements against these MDOT standards:

**MDOT Accuracy Standards (95% confidence):**
| Control Type | Horizontal | Vertical |
|---|---|---|
| Primary Control | ±0.05 ft | ±0.05 ft closure |
| Intermediate Control | ±0.07 ft avg; ±0.10 ft max | ±0.10 ft accumulated |
| Design Survey Hard Surfaces | ±0.05 ft | ±0.01 ft; ±0.02 ft relative |
| Topographic Ground | N/A | ±0.10 ft accumulated |

**MDOT LiDAR Standards:**
- Static TLS: 0.1 ft point spacing on structures, 0.3 ft on roads, validation within 0.05 ft
- Mobile TLS: NCHRP 748 Category 1A for design projects
- Deliverables: e57, LAS, or LAZ with NSSDA accuracy reports

**MDOT Cross-Section Requirements (Section 104.09):**
- Every 50 feet for quantity determination
- Hard surfaces to nearest 0.01 foot
- Ground to nearest 0.1 foot

### Step 3: Determine Robot/Sensor Requirements

Map survey needs to specific robot capabilities:

| Survey Need | Robot Type | Sensor | Typical Platform |
|---|---|---|---|
| Topographic survey | Aerial drone | LiDAR + RTK-GPS | DJI Matrice 350 RTK + Zenmuse L2 |
| Photogrammetry | Aerial drone | High-res camera | DJI Matrice 350 + Zenmuse P1 |
| Subsurface/GPR | Ground robot | Ground-penetrating radar | Spot + GSSI StructureScan |
| Bridge inspection | Inspection drone/crawler | Visual + thermal | Skydio X10 / Flyability ELIOS 3 |
| 3D scanning | Ground robot | Terrestrial LiDAR | Spot + Leica BLK ARC |
| Progress monitoring | Aerial drone | Camera + LiDAR | DJI Matrice 350 / Skydio X10 |
| Structural inspection | Crawler/drone | Visual + crack detection | Gecko TOKA / Flyability ELIOS 3 |
| Environmental survey | Multi-platform | Water quality / air / soil | Custom sensor platforms |

### Step 4: Generate Task Spec JSON

Output one or more task specs in this exact format:

```json
{
  "description": "Pre-bid topographic survey for I-94 reconstruction, 15-acre corridor",
  "task_category": "site_survey",
  "capability_requirements": {
    "hard": {
      "sensors_required": ["aerial_lidar", "rtk_gps", "photogrammetry"],
      "accuracy_required": {
        "vertical_ft": 0.05,
        "horizontal_ft": 0.05,
        "point_density_ft": 0.3
      },
      "certifications_required": ["faa_part_107", "licensed_surveyor"],
      "area_acres": 15,
      "terrain": "highway_corridor",
      "standards_compliance": ["MDOT_104.09", "NCHRP_748_Cat1A", "NSSDA"]
    },
    "soft": {
      "preferred_deliverables": ["LAS", "LandXML", "DXF", "GeoTIFF", "CSV"],
      "preferred_coordinate_system": "NAD83 Michigan South Zone",
      "preferred_datum": "NAVD88",
      "cross_section_interval_ft": 50,
      "contour_interval_ft": 1
    },
    "payload": {
      "type": "survey_data",
      "fields": ["point_cloud", "topo_surface", "ortho_mosaic", "cross_sections", "control_report", "survey_report"],
      "format": "multi_file"
    }
  },
  "budget_ceiling": "5000.00",
  "sla_seconds": 259200,
  "payment_method": "auto",
  "project_metadata": {
    "project_name": "I-94 Reconstruction Phase 2",
    "agency": "MDOT",
    "control_section": "82XXX",
    "job_number": "XXXXXX",
    "location": "Wayne County, MI",
    "letting_date": "2026-06-15",
    "reference_standards": ["MDOT 2020 Std Specs Sec 104.09", "MDOT Survey Standards 2014", "NCHRP 748"],
    "special_conditions": ["traffic_control_required", "night_work_preferred", "utility_conflicts_present"]
  }
}
```

**Task category values:**
- `site_survey` — topographic, design survey, general site mapping
- `bridge_inspection` — structural condition, under-deck, crack detection
- `progress_monitoring` — construction progress documentation
- `as_built` — final condition survey for project closeout
- `subsurface_scan` — GPR, utility locating
- `environmental_survey` — water quality, habitat, emissions
- `control_survey` — primary/intermediate control establishment

### Step 5: Multi-Task Decomposition

If the RFP requires multiple survey types (common), decompose into separate task specs — one per robot type needed. For example, a highway project might produce:
1. Aerial LiDAR topo survey (drone)
2. GPR subsurface scan (ground robot)
3. Bridge condition inspection (inspection drone)

Each is a separate auction task so different operators can bid on each.

## Output Format

Present:
1. **Summary** — one paragraph describing the project and survey needs
2. **Extracted Requirements** — bulleted list of every survey requirement found
3. **Standards Referenced** — which MDOT/AASHTO/federal standards apply
4. **Task Specs** — one or more JSON blocks ready for the auction engine
5. **Estimated Cost Range** — based on area, complexity, and market rates
6. **Robot Recommendations** — which specific platforms would fulfill each task

## Notes

- Convert all imperial measurements to both feet and metric in the output
- Flag any requirements that no current marketplace robot can fulfill
- If accuracy requirements are ambiguous, default to MDOT design survey standards
- Always include NSSDA accuracy reporting in deliverables for MDOT projects
- Budget estimates use $150-300/acre for aerial topo, $3,000-6,000 for GPR, $500-1,500 for visual inspection
