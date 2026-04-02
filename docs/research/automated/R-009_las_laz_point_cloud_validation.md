# R-009: LAS/LAZ Point Cloud Validation Tools and Libraries

**Date:** 2026-04-02
**Topic ID:** R-009
**Module:** M35_deliverable_qa
**Priority:** Critical
**Researcher:** Automated daily research agent

---

## Executive Summary

- **PDAL (Point Data Abstraction Library)** is the leading open-source tool for automated LAS/LAZ point cloud QA, with mature Python bindings (`pip install pdal`) that can be integrated into the marketplace's deliverable acceptance workflow.
- **laspy 2.x** (Python, pure-Python, pip-installable) provides lightweight, fast header validation, point count checks, CRS inspection, and classification auditing without C++ build dependencies — ideal as a first-pass check before heavier PDAL pipelines.
- **USGS Lidar Base Specification v2.1 (LBS 2025 rev. A)** defines a precise, automatable acceptance checklist: no Class 0 points, ≥90% cell coverage at twice the ANPS, no duplicate points, CRS required, accuracy validated against ≥30 checkpoints, swath Δz ≤ 8 cm.
- **ASPRS Positional Accuracy Standards Edition 2 (2024)** updated accuracy classes to require RMSE reporting against 30+ checkpoints and eliminated VVA pass/fail — the automated QA module should align to these updated standards.
- There is **no existing deliverable QA layer** in the current codebase — `DeliveryPayload.data` is an open `dict` with no structural or quality validation. This is the highest-impact gap in the M35_deliverable_qa module.

---

## Findings

### 1. Core Python Libraries for LAS/LAZ QA

#### laspy 2.x (Pure Python — easiest to integrate)
- **Source:** https://laspy.readthedocs.io/en/latest/index.html
- **PyPI:** `pip install laspy[lazrs]`
- **What it does:** Read/write LAS 1.0–1.4 files, inspect header metadata, access point arrays as NumPy arrays, check CRS via pyproj, validate classification codes.
- **Key checks available:**
  - `las.header.point_count` — total point count
  - `las.header.version` — LAS version (1.4 required for ASPRS compliance)
  - `las.classification` — array of all classification codes; check for Class 0 presence
  - `las.header.mins` / `las.header.maxs` — bounding box extents
  - CRS inspection via `las.header.parse_crs()` (pyproj integration)
- **Limitation:** No density computation, no swath alignment check.

#### PDAL (C++ library with Python bindings — full QA)
- **Source:** https://pdal.io/, https://pypi.org/project/pdal/
- **Install:** `conda install -c conda-forge python-pdal` (recommended) or build from source
- **Key QA filters:**
  - `filters.hexbin` — realistic point density using hexagonal binning (more accurate than bounding-box estimate)
  - `filters.stats` — min/max/mean/stddev for all dimensions
  - `filters.range` — filter/check classification codes
  - `readers.las` + `pdal info --metadata` → JSON output for CRS, point count, bounds
  - `pdal info --boundary` → hexbin density estimate
- **Python integration:** Pipeline as JSON dict, execute, get NumPy arrays back
- **Caveat:** Conda install is easiest; pip from source requires PDAL base library.

#### CloudComPy (Python wrapper for CloudCompare — advanced C2C distance)
- **Source:** https://github.com/CloudCompare/CloudComPy
- **Use case:** Cloud-to-cloud distance computation (C2C) for swath alignment validation and change detection QA
- **Verdict:** Too heavy for automated pipeline checks; better suited for manual review of flagged deliverables. Not recommended for first integration sprint.

#### lidR (R package — forestry/research focus)
- **Source:** https://github.com/r-lidar/lidR
- **Verdict:** Excellent for research but R dependency is a non-starter for this Python-based stack. Python PDAL covers the same checks.

### 2. USGS Lidar Base Specification — Automatable Acceptance Criteria

The USGS LBS v2.1 (latest: LBS 2025 rev. A) defines the federal standard for LiDAR deliverable acceptance. Key automatable checks:

| Check | Criterion | Automatable? | Tool |
|-------|-----------|-------------|------|
| Point format | LAS 1.4-R15, PDR format 6/7/8/9/10 | Yes | laspy |
| Duplicate points | None allowed (same x,y,z,timestamp) | Yes | PDAL/laspy |
| Class 0 points | None allowed in classified deliverable | Yes | laspy `classification` array |
| Point density | ≥90% of cells contain ≥1 point (cell = 2× ANPS) | Yes | PDAL `filters.hexbin` |
| Horizontal CRS | Must be present and valid WKT | Yes | PDAL metadata / laspy+pyproj |
| Vertical CRS | Must be present | Yes | PDAL metadata |
| Swath Δz | ≤8 cm in overlap areas | Partial | CloudComPy (heavy) |
| Intensity normalization | 16-bit normalized | Yes | laspy header check |
| Withheld bit flag | Proof of performance required | Partial | Metadata inspection |
| Duplicate tiles | No overlap between adjacent tiles | Yes | Bounding box comparison |

- **Source:** https://www.usgs.gov/ngp-standards-and-specifications/lidar-base-specification-deliverables
- **Source:** https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/Lidar-Base-Specification-version-2-1.pdf

### 3. ASPRS Accuracy Standards Edition 2 (2024)

- **Source:** https://lidarmag.com/2023/10/06/the-asprs-positional-accuracy-standards-edition-2/
- **Source:** https://lidarvisor.com/lidar-accuracy/
- Key updates relevant to automated QA:
  - Minimum **30 checkpoints** required (up from 20) to validate vertical accuracy
  - **RMSE-based** accuracy reporting (eliminated 95% confidence level phrasing)
  - VVA pass/fail removed — but VVA still reported
  - Accuracy form: "Meets ASPRS Edition 2 (2024) for XX cm RMSEH horizontal accuracy class"
- **Quality Levels:**
  - **QL0:** Highest accuracy, specialized engineering (RMSE ≤ 5 cm vertical)
  - **QL1:** RMSE ≤ 10 cm vertical, ≥8 pulses/m²
  - **QL2:** RMSE ≤ 10 cm vertical, ≥2 pulses/m² — minimum for USGS 3DEP and most DOT work
  - **QL3:** RMSE ≤ 20 cm vertical, ≥0.5 pulses/m²
- Current codebase has `VALID_USGS_QUALITY_LEVELS = frozenset(["QL0", "QL1", "QL2", "QL3"])` in `core.py` — validation of the QL label is already gated at task creation, but not at delivery.

### 4. Current Codebase Gap Analysis

The current `DeliveryPayload` in `auction/core.py` (line 427):
```python
@dataclass
class DeliveryPayload:
    request_id: str
    robot_id: str
    data: dict        # ← open dict, no structural validation
    delivered_at: datetime
    sla_met: bool
```

There is no module at `auction/deliverable_qa.py` or any similar file. The `engine.py` transitions the task from `IN_PROGRESS` → `DELIVERED` without any check on `delivery.data` contents. Settlement and payment release happen via `confirm_delivery()` with no QA gate.

**This means escrow funds can be released for deliverables that:**
- Contain no LAS/LAZ file reference at all
- Have no CRS defined
- Contain Class 0 (unclassified) points
- Have point density below the spec required by the task

### 5. Practical Integration Path

A minimal `check_las_deliverable()` function using **laspy** (pure Python, fast) would provide:
1. Header validity check (LAS 1.4, correct PDR format)
2. Point count > 0
3. CRS present (horizontal + vertical)
4. Class 0 percentage below threshold (reject if > X%)
5. Bounding box sanity check against task site GeoJSON

A second-tier **PDAL pipeline** (heavier, optional) would add:
1. Hexbin density check against task's required QL (QL2 = ≥2 pts/m²)
2. Duplicate point detection
3. Classification completeness (required classes present for task type)

The pattern should follow the existing `check_sam_exclusion()` pattern in `auction/compliance.py` — a pure-Python function that returns `(status, issues_list)` where status is `PASS | WARN | FAIL`.

### 6. Open-Source Blog Reference

The "Open lidar QA with PDAL" series at spatialised.net (updated May 2025) is a practical implementation reference for the exact QA patterns described above:
- **Source:** https://www.spatialised.net/lidar-qa-with-pdal-part-1/

---

## Implications for the Product

1. **Payment gating risk:** The current system can release escrow for zero-quality deliverables. A QA layer must gate `confirm_delivery()` before payment settles — especially at construction task scale ($1K–$200K).

2. **laspy is the right first integration:** Pure Python, pip-installable, no build dependencies. Can be added to `pyproject.toml` immediately. Provides sufficient coverage for header, CRS, and classification checks.

3. **PDAL is the right second integration:** Conda-installable but heavier. Use for density checks (QL validation) and duplicate point detection. May be deferred to a separate worker or async validation job.

4. **USGS LBS acceptance criteria should be the baseline:** Tasks specifying `usgs_quality_level: QL2` (already in core.py) should automatically trigger the corresponding density check at delivery time.

5. **ASPRS Edition 2 (2024)** is now the accuracy standard — QA reports generated for GC buyers should cite this version and include RMSE against checkpoint data if provided by the operator.

6. **New research spawned:** R-010 (State DOT deliverable checklists) is unblocked by this finding — proceed.

---

## Improvement Proposals

### IMP-004: Add `check_las_deliverable()` to compliance module using laspy

Implement a pure-Python LAS/LAZ validation function in `auction/compliance.py` (or new `auction/deliverable_qa.py`) using laspy. Gate `AuctionEngine.confirm_delivery()` on a PASS or WARN result. Block escrow settlement on FAIL. Follow the `(status, issues)` pattern of `check_sam_exclusion()`.

- **Effort:** medium
- **Module:** M35_deliverable_qa
- **Research source:** R-009

### IMP-005: Add PDAL-based point density check for QL-gated tasks

For tasks specifying `usgs_quality_level` in hard constraints, run a PDAL hexbin density check at delivery time. Verify ≥2 pts/m² for QL2 tasks, ≥8 pts/m² for QL1. Return FAIL if density is below threshold. Can run async post-delivery with a configurable timeout before payment settlement.

- **Effort:** large
- **Module:** M35_deliverable_qa
- **Research source:** R-009

### IMP-006: Add `deliverable_qa_result` field to `DeliveryPayload`

Extend `DeliveryPayload` to carry QA results (`status`, `issues`, `point_count`, `density_pts_per_m2`, `crs_detected`, `class_0_pct`). Store in SQLite audit trail. Surface in buyer dashboard and GC reporting.

- **Effort:** medium
- **Module:** M35_deliverable_qa, M32_buyer_dashboard
- **Research source:** R-009

---

## New Questions Spawned

- **R-010** (already in roadmap): State DOT deliverable acceptance criteria → now unblocked
- **R-011** (already in roadmap): Orthomosaic/DEM QA metrics → now unblocked
- **R-009a** (new): What is the Python packaging strategy for PDAL — conda env, Docker sidecar, or subprocess call to pdal CLI? Evaluate trade-offs for Cloudflare Worker + Railway deployment.

---

## Sources

- [PDAL Point Data Abstraction Library](https://pdal.io/)
- [PDAL Python bindings on PyPI](https://pypi.org/project/pdal/)
- [laspy 2.5.0 documentation](https://laspy.readthedocs.io/en/latest/index.html)
- [laspy on PyPI](https://pypi.org/project/laspy/)
- [Open lidar QA with PDAL part 1 — Spatialised.net](https://www.spatialised.net/lidar-qa-with-pdal-part-1/)
- [PDAL Wrench — parallel point cloud processing](https://github.com/PDAL/wrench)
- [USGS Lidar Base Specification Deliverables](https://www.usgs.gov/ngp-standards-and-specifications/lidar-base-specification-deliverables)
- [USGS Lidar Base Specification v2.1 PDF](https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/Lidar-Base-Specification-version-2-1.pdf)
- [USGS LBS Data Processing and Handling Requirements](https://www.usgs.gov/ngp-standards-and-specifications/lidar-base-specification-data-processing-and-handling-requirements)
- [ASPRS Positional Accuracy Standards Edition 2 — LIDAR Magazine](https://lidarmag.com/2023/10/06/the-asprs-positional-accuracy-standards-edition-2/)
- [LiDAR Accuracy: ASPRS Standards & Quality Levels](https://lidarvisor.com/lidar-accuracy/)
- [CloudComPy Python wrapper for CloudCompare](https://github.com/CloudCompare/CloudComPy)
- [LAStools — GitHub](https://github.com/LAStools/LAStools)
- [lidR R package — CRAN](https://cran.r-project.org/web/packages/lidR/index.html)
- [COPC — Cloud Optimized Point Cloud Specification](https://copc.io/)
- [Propeller Aero LiDAR QA/QC](https://www.propelleraero.com/lidar-survey-processing/)
