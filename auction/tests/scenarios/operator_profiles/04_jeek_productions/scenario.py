"""Operator 04: Jeek Productions — Small drone team, photogrammetry focus.

Minimal compliance profile. Tests the lower bound of what an operator
needs to participate in the marketplace. No PLS, no E&O, limited to
photogrammetry and progress monitoring tasks.

Scenario flow:
    1. Upload Part 107 and insurance COI (minimal docs)
    2. System verifies:
       - Part 107: VALID
       - Insurance: VALID (flags E&O MISSING)
       - PLS: MISSING
    3. Jeek bids on photogrammetry / progress monitoring task
    4. If task requires PLS stamp, PLS-as-a-service recommended
    5. Scoring: lower compliance score than PLS-holding operators

Key assertions:
    - Minimal docs accepted (Part 107 + CGL + aviation)
    - PLS MISSING flagged
    - E&O MISSING flagged
    - Can bid on progress monitoring without PLS
    - Cannot bid on tasks requiring PLS stamp without PLS-as-a-service
"""

from pathlib import Path

SCENARIO_DIR = Path(__file__).parent

OPERATOR_PROFILE = {
    "id": "04_jeek_productions",
    "name": "Jeek Productions, LLC",
    "location": "Grand Rapids, MI",
    "contact": "Jake Eekema, Owner/Pilot",
    "has_pls": False,
    "has_part_107": True,
    "has_insurance": True,  # Partial — no E&O
    "has_confined_space": False,
    "operator_type": "small_drone_team",
}

COMPLIANCE_DOCS = {
    "faa_part_107": SCENARIO_DIR / "faa_part_107.txt",
    "insurance_coi": SCENARIO_DIR / "insurance_coi.txt",
}

EXPECTED_COMPLIANCE = {
    "pls_license": "MISSING",
    "faa_part_107": "VALID",
    "insurance_coi": "VALID",
    "insurance_eo": "MISSING",
    "overall": "PARTIAL",
}

ELIGIBLE_TASK_TYPES = [
    "progress_monitoring",
    "photogrammetry",
]
