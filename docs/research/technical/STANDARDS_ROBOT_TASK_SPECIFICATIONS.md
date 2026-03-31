# Standards Analysis: Robot Task Specification Formats

**Date:** 2026-03-31
**Status:** Research complete, recommendations ready for implementation planning
**Scope:** Standards that should inform the RFP → structured robot task request conversion

## Context

The marketplace converts natural-language RFPs into structured task specs that robots bid on. The current schema (`auction/core.py` Task dataclass + `.claude/skills/rfp-to-robot-spec/` output) uses a custom format. This document evaluates existing standards to identify what we should adopt, adapt, or reference.

## Current Task Spec Schema (Baseline)

```
Task:
  request_id          UUID
  description         free text
  task_category       enum (15 values: site_survey, bridge_inspection, ...)
  capability_requirements:
    hard:
      sensors_required        string list
      accuracy_required       dict {vertical_ft, horizontal_ft}
      certifications_required string list
      area_acres              number
      terrain                 string
    soft:
      preferred_deliverables  string list ("LAS", "DXF", ...)
      preferred_coordinate_system  string
      preferred_datum              string
    payload:
      type    string
      fields  string list
      format  string
  budget_ceiling      Decimal
  sla_seconds         int
  payment_method      "stripe" | "usdc" | "auto"
  task_decomposition  dict (rfp_id, task_index, dependencies, bundling)
  project_metadata    dict (project_name, agency, location, ...)
```

## Standards Evaluation

### Tier 1 — Directly Adoptable (should incorporate into schema)

#### ASPRS Positional Accuracy Standards (Ed. 2, 2024)
- **Body:** American Society for Photogrammetry and Remote Sensing
- **What:** Defines accuracy classes using RMSE as sole metric. Horizontal/vertical classes with numeric thresholds.
- **Current gap:** We use `accuracy_required: {vertical_ft: 0.05, horizontal_ft: 0.05}` — correct concept but no reference to the standard's accuracy class system.
- **Recommendation:** Add `asprs_accuracy_class` field mapping to the standard's class system. Continue supporting raw RMSE values for custom requirements.
- **Effort:** Low. Lookup table mapping class names to RMSE thresholds.

#### USGS LiDAR Base Specification (2025 rev. A)
- **Body:** U.S. Geological Survey
- **What:** Detailed requirements for LiDAR data acquisition and deliverables for 3DEP. Specifies point density, accuracy (aligned with ASPRS), classification, LAS 1.4 format, tiling, projection, metadata.
- **Current gap:** Our `payload.fields` is a flat string list. USGS LBS defines a structured deliverable checklist: classified point cloud, bare-earth DEM, breaklines, metadata, reports.
- **Recommendation:** Create a `deliverables` array where each item has `format`, `version`, `classification_standard`, `crs_epsg`, and `accuracy_spec`. Model after the USGS deliverable checklist structure.
- **Effort:** Medium. Schema expansion + rfp-to-robot-spec skill update.

#### LAS 1.4 / E57 / LandXML Format Specifications
- **Body:** ASPRS (LAS), ASTM E57, LandXML.org
- **What:** Standard file formats for point clouds (LAS/LAZ, E57) and civil engineering data (LandXML).
- **Current gap:** We list format names as strings but don't specify versions or parameters.
- **Recommendation:** When a deliverable specifies LAS, include `las_version: "1.4"` and `point_record_format: 6` (or equivalent). For E57, reference ASTM E2807. Already partially implemented — just formalize.
- **Effort:** Low. Enum expansion.

#### EPSG Codes for Coordinate Systems
- **Body:** OGC / IOGP (maintains EPSG registry)
- **What:** Numeric codes for coordinate reference systems (e.g., EPSG:2113 = NAD83 Michigan South).
- **Current gap:** We use `preferred_coordinate_system: "NAD83 Michigan South Zone"` — human-readable but not machine-parseable.
- **Recommendation:** Add `crs_epsg: 2113` alongside the human-readable string. EPSG codes are universally supported by GIS software.
- **Effort:** Very low. Single field addition.

### Tier 2 — Conceptually Aligned (should inform design)

#### IEEE 1872 CORA — Ontology for Robotics and Automation
- **Body:** IEEE Robotics and Automation Society
- **Version:** 1872-2015 (core), 1872.2-2021 (autonomous extension)
- **What:** Formal ontology (OWL) defining concepts: Robot, RoboticSystem, Task, Capability, Environment. The 1872.2 extension adds Mission, Plan, and GoalSpecification.
- **Current alignment:** Our Task/Bid/AuctionResult model is conceptually compatible but doesn't use IEEE 1872 terminology.
- **Recommendation:** Align vocabulary where possible. Our `task_category` maps to IEEE 1872's task taxonomy. Our `capability_requirements.hard` maps to CORA's `Capability` concept. No need to adopt OWL — just use compatible naming.
- **Effort:** Low. Documentation/naming alignment, not code change.

#### ROS 2 Action Interface (.action IDL)
- **Body:** Open Robotics
- **What:** Defines long-running robot tasks as Goal (request) → Feedback (progress) → Result (outcome). The .action file format is the production standard for commanding robots.
- **Current alignment:** Our Task lifecycle (POSTED → BIDDING → IN_PROGRESS → DELIVERED) maps cleanly to ROS 2 Action states. Our `DeliveryPayload` maps to Action Result.
- **Recommendation:** Ensure our task spec can be translated to a ROS 2 Action goal. This means structured, typed fields rather than free-form dicts. Don't adopt .action IDL directly — it's a robot-side concern — but document the mapping.
- **Effort:** Low. Design documentation.

#### A2A Protocol (Google/Linux Foundation)
- **Body:** Google, now Linux Foundation
- **Version:** 0.3
- **What:** Agent-to-agent task delegation with Task lifecycle (submitted → working → completed → failed), Agent Cards for discovery, and structured status updates.
- **Current alignment:** High. Our auction lifecycle closely mirrors A2A's Task lifecycle. ERC-8004 agent cards already overlap with A2A Agent Cards.
- **Recommendation:** Consider A2A compatibility for the agent-facing API. An A2A-compatible wrapper would let external AI agents discover and use our marketplace without MCP. Low priority but strategically valuable.
- **Effort:** Medium. New API layer.

#### MRTA iTax Taxonomy (Korsah-Stentz-Dias, 2013)
- **Body:** Academic (CMU/Ashesi)
- **What:** Classifies multi-robot task allocation problems along 4 axes: ST/MT (single/multi-task robots), SR/MR (single/multi-robot tasks), IA/TA (instantaneous/time-extended), ND/ID/XD/CD (dependency type).
- **Current alignment:** Our current model is [ST-SR-IA-ND] — single-task robots, single-robot tasks, instantaneous allocation, no dependencies. The `task_decomposition.dependencies` field hints at future [ST-SR-TA-ID] support.
- **Recommendation:** Tag task specs with MRTA classification. This helps the scoring engine select appropriate allocation algorithms when we support compound tasks (v2.0).
- **Effort:** Very low. Metadata field.

#### OGC SensorML 2.1
- **Body:** Open Geospatial Consortium
- **What:** XML-based description of sensors, actuators, and measurement processes — identifiers, capabilities, characteristics, inputs/outputs.
- **Current alignment:** Our `capability_requirements.hard.sensors_required` is a flat string list. SensorML provides a richer sensor description (measurement range, accuracy, resolution, wavelength).
- **Recommendation:** For the operator/equipment registry, consider SensorML-aligned sensor descriptions. For the task spec itself, the flat list is sufficient — the matching engine handles the mapping.
- **Effort:** Medium. Equipment registry schema expansion.

#### OGC SensorThings API Part 2 (Tasking)
- **Body:** Open Geospatial Consortium
- **What:** REST-based API for tasking sensors and actuators. Defines TaskingCapabilities, Tasks, and ActuationParameters.
- **Current alignment:** Conceptually similar — our POST /api/tool/auction_post_task is functionally equivalent to creating a SensorThings Task.
- **Recommendation:** Monitor for adoption. If SensorThings Tasking gains traction in the drone survey industry, we should offer a compatible endpoint.
- **Effort:** Medium. New API endpoint wrapper.

### Tier 3 — Reference Standards (context, not schema changes)

#### ASTM F3411 (Remote ID) / F3548 (UTM)
- **Relevance:** Regulatory prerequisites for drone operations. A task spec should include a boolean `remote_id_required: true` and potentially reference an operational volume (F3548). Not schema-structural — just constraint fields.

#### IFC / ISO 16739 (BIM)
- **Relevance:** Construction context. If the project has a BIM model, the task spec could reference it via `project_metadata.ifc_model_url`. Future concern for v2.0+.

#### 2026 ALTA/NSPS Land Title Survey Standards
- **Relevance:** For land/property survey tasks. The Table A optional items (20 items, yes/no) could be encoded as a checklist within `capability_requirements`. Niche — only applies to ALTA surveys.

#### ISO 19115 (Geographic Metadata)
- **Relevance:** Deliverable metadata compliance. Task specs should be able to require ISO 19115-compliant metadata with output. Add as a deliverable attribute, not a core schema change.

#### ConsensusDocs / AIA Contract Standards
- **Relevance:** Already integrated — we generate ConsensusDocs 750 subcontracts. The contract standards inform deliverable requirements but aren't schema-structural.

## Recommended Schema Changes

### Priority 1 — Quick Wins (this sprint)

```yaml
# Add to capability_requirements.hard
accuracy_standard: "asprs_ed2"           # Reference standard
asprs_horizontal_class: "5cm"            # ASPRS horizontal accuracy class
asprs_vertical_class: "5cm"              # ASPRS vertical accuracy class
crs_epsg: 2113                           # Machine-readable CRS (EPSG code)
vertical_datum_epsg: 5703                # NAVD88 = EPSG:5703

# Replace payload with structured deliverables
deliverables:
  - format: "LAS"
    version: "1.4"
    point_record_format: 6
    classification_standard: "asprs"
    min_point_density_ppsm: 8            # points per sq meter
  - format: "GeoTIFF"
    type: "orthomosaic"
    gsd_cm: 2.5
  - format: "LandXML"
    version: "1.2"
    content: ["surface", "alignments"]
  - format: "DXF"
    content: ["contours", "breaklines"]
```

### Priority 2 — Structural Improvements (next sprint)

```yaml
# MRTA classification metadata
mrta_class:
  robot_type: ST                         # single-task robot
  task_type: SR                          # single-robot task
  allocation: IA                         # instantaneous
  dependency: ND                         # no dependency

# Regulatory constraints
regulatory:
  faa_remote_id_required: true
  faa_part_107_required: true
  airspace_class: "G"
  laanc_authorization: "required"        # required | not_required | pre_approved
  state_pls_required: true
  pls_jurisdiction: "MI"
```

### Priority 3 — Future Interop (v2.0+)

```yaml
# A2A-compatible agent discovery metadata
interop:
  a2a_task_type: "survey.construction.topographic"
  a2a_capabilities_required: ["lidar", "rtk_gps", "photogrammetry"]
  ros2_action_type: "survey_interfaces/action/TopographicSurvey"

# BIM/IFC reference
project_context:
  ifc_model_url: "https://..."           # Optional BIM model
  citygml_lod: 2                         # Target LOD for 3D deliverables
```

## Standards Not Adopted (With Rationale)

| Standard | Why Not |
|----------|---------|
| Full OWL/IEEE 1872 ontology | Overkill for our use case. Align vocabulary, don't adopt the format. |
| ROS 2 .action IDL as task format | Robot-side concern, not marketplace-side. We produce JSON task specs; the robot translates to ROS 2 internally. |
| Full SensorML sensor descriptions | Too verbose for task requests. Keep flat sensor lists for matching; rich descriptions live in the equipment registry. |
| GML/XML-based geospatial standards | Our stack is JSON-first. Reference the standards, use JSON encodings where available. |
| ANP (Agent Network Protocol) | Too early. Monitor for W3C standardization progress. |
| Full SensorThings API | Would require a separate API layer. Our MCP tools serve the same function. Monitor adoption. |

## Implementation Plan

| Phase | Changes | Files Affected | Effort |
|-------|---------|----------------|--------|
| **1. Quick wins** | Add EPSG codes, ASPRS accuracy classes, structured deliverables | `auction/core.py`, `rfp-to-robot-spec/SKILL.md`, `rfp-to-robot-spec/references/` | 1-2 days |
| **2. Schema expansion** | MRTA classification, regulatory constraints, deliverable versioning | `auction/core.py`, `auction/mcp_tools.py`, `mcp_server.py` | 2-3 days |
| **3. Validation** | Validate EPSG codes, ASPRS classes, LAS versions against known-good lists | `auction/core.py` validate_task_spec() | 1 day |
| **4. Skill update** | Update rfp-to-robot-spec to emit new fields | `.claude/skills/rfp-to-robot-spec/` | 1 day |
| **5. Documentation** | Update PRODUCT_DSL, DECISIONS.md with new standards references | `docs/` | 0.5 day |

## Sources

### Accuracy & Quality
- ASPRS Positional Accuracy Standards, Edition 2, Version 2 (2024) — asprs.org
- USGS LiDAR Base Specification, 2025 rev. A — usgs.gov/ngp-standards-and-specifications
- FGDC Content Standard for Digital Geospatial Metadata (CSDGM) — fgdc.gov

### File Formats
- ASPRS LAS 1.4 Specification, Revision 15 (2019) — asprs.org
- ASTM E2807 / E57 3D Imaging Data Exchange — astm.org
- LandXML 1.2 — landxmlproject.org
- ISO 19115-1:2014 Geographic Metadata — iso.org

### Robotics Ontology
- IEEE 1872-2015 Core Ontology for Robotics and Automation — ieee.org
- IEEE 1872.2-2021 Autonomous Robotics Ontology Extension — ieee.org
- Gerkey & Mataric, "A Formal Analysis of Multi-Robot Task Allocation" (2004)
- Korsah, Stentz & Dias, "A Comprehensive Taxonomy for MRTA" (2013) — IJRR

### Agent Protocols
- Google A2A Protocol v0.3 — a2a-protocol.org
- MCP Specification (2025-11-25) — modelcontextprotocol.io
- ERC-8004 Trustless Agents — eips.ethereum.org
- x402 Payment Protocol v2 — x402.org

### Geospatial Standards
- OGC SensorML 2.1 — ogc.org
- OGC SensorThings API Part 2 Tasking — ogc.org
- OGC CityGML 3.0 — ogc.org
- EPSG Registry — epsg.org

### Construction Industry
- 2026 ALTA/NSPS Land Title Survey Standards (11th ed.) — nsps.us.com
- IFC 4.3 / ISO 16739-1:2024 — buildingsmart.org
- Michigan MDOT Survey Standards of Practice (2014) — michigan.gov
- ASTM F3411-22a Remote ID / F3548-21 UTM — astm.org

### Existing Project References
- `.claude/skills/rfp-to-robot-spec/references/michigan-standards.md`
- `.claude/skills/rfp-to-robot-spec/references/aashto-federal-standards.md`
- `.claude/skills/rfp-to-robot-spec/references/robot-sensor-mapping.md`
- `docs/research/technical/FOUNDATIONAL_TECH_ANALYSIS.md` (WoT TD, A2A references)
