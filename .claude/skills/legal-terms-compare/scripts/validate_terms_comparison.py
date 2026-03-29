#!/usr/bin/env python3
"""Validate a legal terms comparison report JSON.
Exits 0 if valid, 1 if invalid."""
import json, sys

VALID_STATUSES = {"COMPATIBLE", "CONFLICTS_FOUND", "REVIEW_REQUIRED"}
VALID_DIM_STATUSES = {"MATCH", "CONFLICT", "MISSING", "UNENFORCEABLE", "RISK_IMBALANCE"}
VALID_RISK_LEVELS = {"low", "medium", "high", "critical"}
DIMENSIONS_REQUIRED = 12

def validate(report):
    errors = []
    if report.get("comparison_status") not in VALID_STATUSES:
        errors.append(f"Invalid comparison_status: {report.get('comparison_status')}")
    if not report.get("project_state"):
        errors.append("Missing project_state")
    dims = report.get("dimensions", [])
    if len(dims) < DIMENSIONS_REQUIRED:
        errors.append(f"Expected {DIMENSIONS_REQUIRED} dimensions, got {len(dims)}")
    for d in dims:
        if d.get("status") not in VALID_DIM_STATUSES:
            errors.append(f"Invalid status '{d.get('status')}' for dimension '{d.get('dimension')}'")
        if d.get("risk_level") and d["risk_level"] not in VALID_RISK_LEVELS:
            errors.append(f"Invalid risk_level '{d['risk_level']}' for '{d.get('dimension')}'")
    if not report.get("disclaimer"):
        errors.append("Missing disclaimer — every report must include 'not legal advice' disclaimer")
    summary = report.get("summary", {})
    total = sum(summary.get(k, 0) for k in ["matches", "conflicts", "missing", "unenforceable", "risk_imbalances"])
    if total < DIMENSIONS_REQUIRED:
        errors.append(f"Summary counts ({total}) don't cover all {DIMENSIONS_REQUIRED} dimensions")
    return errors

def main():
    data = json.load(open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin)
    errors = validate(data)
    if errors:
        for e in errors: print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"OK: Terms comparison valid — status: {data['comparison_status']}, {len(data.get('dimensions',[]))} dimensions")

if __name__ == "__main__":
    main()
