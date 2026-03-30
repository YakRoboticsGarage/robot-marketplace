#!/usr/bin/env python3
"""Scenario test runner — runs GC scenarios one at a time.

Usage:
    # Run all scenarios sequentially
    PYTHONPATH=. python auction/tests/scenarios/run_all.py

    # Run a specific scenario by number (1-5)
    PYTHONPATH=. python auction/tests/scenarios/run_all.py 1

    # Run with verbose output
    PYTHONPATH=. python auction/tests/scenarios/run_all.py --verbose

    # List available scenarios
    PYTHONPATH=. python auction/tests/scenarios/run_all.py --list
"""

import importlib.util
import sys
import time
from pathlib import Path

SCENARIOS_DIR = Path(__file__).parent / "gc_profiles"


def discover_scenarios() -> list[tuple[str, Path]]:
    """Find all scenario.py files, sorted by folder name."""
    scenarios = []
    for folder in sorted(SCENARIOS_DIR.iterdir()):
        script = folder / "scenario.py"
        if script.exists():
            scenarios.append((folder.name, script))
    return scenarios


def run_scenario(name: str, script_path: Path) -> dict:
    """Run a single scenario and return results."""
    print(f"\n{'=' * 70}")
    print(f"  RUNNING: {name}")
    print(f"  Script: {script_path.relative_to(script_path.parents[4])}")
    print(f"{'=' * 70}")

    # Load the module dynamically
    spec = importlib.util.spec_from_file_location(f"scenario_{name}", script_path)
    if spec is None or spec.loader is None:
        return {"name": name, "status": "ERROR", "message": "Could not load scenario", "gaps": []}

    module = importlib.util.module_from_spec(spec)

    start = time.time()
    try:
        spec.loader.exec_module(module)
        if hasattr(module, "main"):
            gap_count = module.main()
            elapsed = time.time() - start
            return {
                "name": name,
                "status": "PASS" if gap_count == 0 else "GAPS_FOUND",
                "gap_count": gap_count,
                "elapsed_s": round(elapsed, 2),
                "gaps": getattr(module, "gaps", []),
            }
        else:
            return {
                "name": name,
                "status": "SKIP",
                "message": "No main() function — scenario incomplete",
                "gaps": [],
            }
    except Exception as e:
        elapsed = time.time() - start
        return {
            "name": name,
            "status": "ERROR",
            "message": str(e),
            "elapsed_s": round(elapsed, 2),
            "gaps": [f"CRASH: {e}"],
        }


def print_report(results: list[dict]) -> int:
    """Print consolidated gap report. Returns total gap count."""
    print("\n")
    print("=" * 70)
    print("  SCENARIO RESULTS")
    print("=" * 70)

    total_gaps = 0
    all_gaps = []

    for r in results:
        status = r["status"]
        name = r["name"]
        elapsed = r.get("elapsed_s", 0)
        gap_count = r.get("gap_count", len(r.get("gaps", [])))
        total_gaps += gap_count

        icon = {"PASS": "OK", "GAPS_FOUND": "!!", "ERROR": "XX", "SKIP": "--"}[status]
        print(f"  [{icon}] {name:<30s} {status:<12s} {gap_count} gaps  ({elapsed}s)")

        for g in r.get("gaps", []):
            all_gaps.append(f"  {name}: {g}")

    print(f"\n  Total: {len(results)} scenarios, {total_gaps} gaps")

    if all_gaps:
        print(f"\n{'=' * 70}")
        print("  GAP DETAILS")
        print("=" * 70)
        for g in all_gaps:
            print(g)

    print("=" * 70)
    return total_gaps


def main():
    # Add project root to path
    project_root = str(Path(__file__).resolve().parents[3])
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    scenarios = discover_scenarios()

    if "--list" in sys.argv:
        print("Available scenarios:")
        for i, (name, path) in enumerate(scenarios, 1):
            has_main = "main" in (path.read_text())
            status = "ready" if has_main else "incomplete"
            print(f"  {i}. {name} ({status})")
        return 0

    # Run specific scenario by number
    specific = [a for a in sys.argv[1:] if a.isdigit()]
    if specific:
        idx = int(specific[0]) - 1
        if 0 <= idx < len(scenarios):
            name, path = scenarios[idx]
            result = run_scenario(name, path)
            return print_report([result])
        else:
            print(f"Scenario {specific[0]} not found. Use --list to see available.")
            return 1

    # Run all sequentially
    results = []
    for name, path in scenarios:
        result = run_scenario(name, path)
        results.append(result)
        # Stop on crash to make debugging easier
        if result["status"] == "ERROR":
            print(f"\n  Stopping: {name} crashed. Fix before continuing.")
            break

    return print_report(results)


if __name__ == "__main__":
    sys.exit(main())
