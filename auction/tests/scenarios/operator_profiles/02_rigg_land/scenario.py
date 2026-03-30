"""Operator 02: Rigg Land Surveying — Traditional surveyor with drones.

Represents the typical small Michigan PLS firm that has added drone
capability. Has PLS license and Part 107, qualifies for standard
aerial topo and control survey tasks.

Scenario flow:
    1. Upload PLS license, Part 107, insurance COI
    2. System verifies all documents — all pass
    3. Rigg bids on control survey or small topo task
    4. Scoring considers: PLS (bonus), regional proximity, equipment match
    5. May win smaller tasks where SSI is overqualified/overpriced

Key assertions:
    - PLS license validates (MI #35214, not expired)
    - Part 107 validates
    - Insurance meets standard minimums (but not high-value thresholds)
    - No confined space cert — cannot bid tunnel tasks
    - Aviation coverage ($1M) may be below some GC requirements ($5M)
"""

from pathlib import Path

SCENARIO_DIR = Path(__file__).parent

OPERATOR_PROFILE = {
    "id": "02_rigg_land",
    "name": "Rigg Land Surveying, LLC",
    "location": "Tawas City, MI",
    "contact": "William Rigg, P.S.",
    "has_pls": True,
    "has_part_107": True,
    "has_insurance": True,
    "has_confined_space": False,
    "operator_type": "traditional_pls_with_drones",
}

COMPLIANCE_DOCS = {
    "pls_license": SCENARIO_DIR / "pls_license.txt",
    "faa_part_107": SCENARIO_DIR / "faa_part_107.txt",
    "insurance_coi": SCENARIO_DIR / "insurance_coi.txt",
}

EXPECTED_COMPLIANCE = {
    "pls_license": "VALID",
    "faa_part_107": "VALID",
    "insurance_coi": "VALID",
    "overall": "COMPLIANT",
}

ELIGIBLE_TASK_TYPES = [
    "aerial_lidar_topo",
    "photogrammetry",
    "control_survey",
]
