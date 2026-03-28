#!/usr/bin/env python3
"""Validate a site recon JSON report.

Checks that every field has a source tag and that each source type
includes the required metadata (URL for LOOKUP, confidence for INFERRED,
question for UNKNOWN).

Usage: python validate_site_recon.py < recon.json
       python validate_site_recon.py recon.json

Exits 0 if valid, 1 if invalid.
"""
import json
import sys

VALID_SOURCES = {"RFP", "LOOKUP", "INFERRED", "UNKNOWN"}


def validate_field(path: str, field: dict, errors: list) -> None:
    """Validate a single tagged field."""
    if not isinstance(field, dict):
        return  # Primitive value, not a tagged field — skip

    source = field.get("source")

    # If it has a "source" key, it's a tagged field — validate it
    if source is not None:
        if source not in VALID_SOURCES:
            errors.append(f"{path}: invalid source '{source}'. Valid: {sorted(VALID_SOURCES)}")

        if source == "LOOKUP" and not field.get("source_url"):
            errors.append(f"{path}: LOOKUP field missing 'source_url'")

        if source == "INFERRED":
            if "confidence" not in field:
                errors.append(f"{path}: INFERRED field missing 'confidence' (0.0-1.0)")
            elif not (0 <= field["confidence"] <= 1):
                errors.append(f"{path}: confidence must be 0.0-1.0, got {field['confidence']}")
            if not field.get("reasoning"):
                errors.append(f"{path}: INFERRED field missing 'reasoning'")

        if source == "UNKNOWN" and not field.get("question"):
            errors.append(f"{path}: UNKNOWN field missing 'question' (what to ask client)")

        return

    # If no "source" key, recurse into sub-fields
    if isinstance(field, dict):
        for key, val in field.items():
            if isinstance(val, dict):
                validate_field(f"{path}.{key}", val, errors)
            elif isinstance(val, list):
                for i, item in enumerate(val):
                    if isinstance(item, dict):
                        validate_field(f"{path}.{key}[{i}]", item, errors)


def validate(recon: dict) -> list[str]:
    errors = []

    # Must have pre_mobilization_checklist
    if "pre_mobilization_checklist" not in recon:
        errors.append("Missing 'pre_mobilization_checklist' — every recon must produce action items")
    elif not isinstance(recon["pre_mobilization_checklist"], list):
        errors.append("'pre_mobilization_checklist' must be a list of strings")
    elif len(recon["pre_mobilization_checklist"]) == 0:
        errors.append("'pre_mobilization_checklist' is empty — there are always unknowns")

    # Count source types for summary
    source_counts = {"RFP": 0, "LOOKUP": 0, "INFERRED": 0, "UNKNOWN": 0}

    def count_sources(obj):
        if isinstance(obj, dict):
            s = obj.get("source")
            if s in source_counts:
                source_counts[s] += 1
            for v in obj.values():
                count_sources(v)
        elif isinstance(obj, list):
            for item in obj:
                count_sources(item)

    count_sources(recon)

    # Validate all tagged fields
    for key, val in recon.items():
        if key == "pre_mobilization_checklist":
            continue
        if isinstance(val, dict):
            validate_field(key, val, errors)
        elif isinstance(val, list):
            for i, item in enumerate(val):
                if isinstance(item, dict):
                    validate_field(f"{key}[{i}]", item, errors)

    # Warn if no UNKNOWN fields — suspicious (there are always unknowns in site recon)
    if source_counts["UNKNOWN"] == 0:
        errors.append("WARNING: zero UNKNOWN fields — every real site has unknowns. Did you forget to flag client-dependent information?")

    return errors, source_counts


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    errors, counts = validate(data)

    # Print source distribution
    total = sum(counts.values())
    print(f"Source distribution ({total} tagged fields):")
    for src, n in sorted(counts.items()):
        pct = (n / total * 100) if total > 0 else 0
        print(f"  {src}: {n} ({pct:.0f}%)")

    if errors:
        print(f"\n{len(errors)} issue(s):", file=sys.stderr)
        for e in errors:
            print(f"  ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    else:
        print("\nOK: all fields properly tagged")
        sys.exit(0)


if __name__ == "__main__":
    main()
