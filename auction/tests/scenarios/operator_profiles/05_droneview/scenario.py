"""Operator 05: DroneView Technologies — Premium operator, full compliance.

The highest-tier operator profile. Has all 6 compliance documents including
SAM registration for federal-adjacent work. ASPRS certified. Staff PLS.
Competes with SSI on high-value tasks.

Scenario flow:
    1. Upload all 6 compliance documents (PLS, Part 107, COI, SAM, etc.)
    2. System verifies all documents — all pass, SAM active
    3. DroneView bids on GC 05 Task 1 (I-94 topo, federal-adjacent)
    4. Federal requirements detected: DBE, Davis-Bacon, Buy America
    5. SAM registration validates — eligible for federal work
    6. Scoring: highest compliance score, competes with SSI on price/experience
    7. May win federal-adjacent tasks where SAM registration is preferred

Key assertions:
    - All 6 compliance docs upload and verify
    - PLS license validates (MI #41203, Rebecca Torres)
    - SAM registration active and NAICS codes match survey work
    - Insurance meets highest GC thresholds ($5M aviation, $5M umbrella)
    - ASPRS certification recognized as professional credential
    - Federal-adjacent eligibility confirmed
"""

from pathlib import Path

SCENARIO_DIR = Path(__file__).parent

OPERATOR_PROFILE = {
    "id": "05_droneview",
    "name": "DroneView Technologies, Inc.",
    "location": "Bloomfield Hills, MI",
    "contact": "Michael Singer, CEO",
    "has_pls": True,  # Staff PLS: Rebecca Torres
    "has_part_107": True,
    "has_insurance": True,  # Full coverage including umbrella
    "has_confined_space": False,
    "has_sam": True,
    "operator_type": "premium_full_service",
}

COMPLIANCE_DOCS = {
    "pls_license": SCENARIO_DIR / "pls_license.txt",
    "faa_part_107": SCENARIO_DIR / "faa_part_107.txt",
    "insurance_coi": SCENARIO_DIR / "insurance_coi.txt",
    "sam_registration": SCENARIO_DIR / "sam_registration.txt",
}

EXPECTED_COMPLIANCE = {
    "pls_license": "VALID",
    "faa_part_107": "VALID",
    "insurance_coi": "VALID",
    "insurance_eo": "VALID",
    "sam_registration": "ACTIVE",
    "overall": "FULLY_COMPLIANT",
}

ELIGIBLE_TASK_TYPES = [
    "aerial_lidar_topo",
    "photogrammetry",
    "control_survey",
    "progress_monitoring",
    # No confined space — cannot do tunnel work
]

FEDERAL_ELIGIBLE = True
