"""Tier 3: Performance baseline tests.

Run with: uv run pytest auction/tests/test_benchmarks.py --benchmark-only
Skip in normal CI with: --benchmark-disable

These establish performance baselines for critical paths. If a code change
makes scoring 10x slower, it shows up here before it hits production.
"""

from __future__ import annotations

from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from auction.core import (
    Task,
    check_hard_constraints,
    compute_commitment_hash,
    score_bids,
    validate_task_spec,
)
from auction.engine import AuctionEngine
from auction.mock_fleet import create_demo_fleet
from auction.wallet import WalletLedger


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_task_and_bids(n_bids=100):
    """Create a task and N simulated bids for benchmarking."""
    from auction.core import Bid

    task = Task(
        request_id="bench-001",
        description="Benchmark task",
        task_category="topo_survey",
        capability_requirements={"hard": {"sensors_required": ["aerial_lidar"]}},
        budget_ceiling=Decimal("10.00"),
        sla_seconds=600,
    )
    bids = []
    for i in range(n_bids):
        bids.append(Bid(
            robot_id=f"robot_{i}",
            request_id="bench-001",
            price=Decimal(f"{1 + i * 0.05:.2f}"),
            sla_commitment_seconds=300 + i * 5,
            ai_confidence=max(0.01, 0.90 - (i * 0.005)),
            capability_metadata={"sensors": ["aerial_lidar"]},
            reputation_metadata={"completion_rate": 0.95},
            bid_hash="bench_hash",
        ))
    return task, bids


def _make_robot_capabilities(n=100):
    """Create N robot capability dicts for constraint checking."""
    caps = []
    for i in range(n):
        caps.append({
            "sensors": ["aerial_lidar", "rtk_gps"] if i % 3 != 0 else ["photogrammetry"],
            "indoor_capable": i % 5 == 0,
            "battery_percent": 40 + (i % 60),
            "distance_meters": 1000 + i * 100,
            "certifications": ["licensed_surveyor"] if i % 10 == 0 else [],
        })
    return caps


# ---------------------------------------------------------------------------
# Benchmarks
# ---------------------------------------------------------------------------

def test_score_bids_100(benchmark):
    """Score and rank 100 bids against a single task."""
    task, bids = _make_task_and_bids(100)
    benchmark(score_bids, task, bids)


def test_check_hard_constraints_100(benchmark):
    """Filter 100 robots through 3 hard constraints."""
    task = Task(
        request_id="bench-hc",
        description="Constraint benchmark",
        task_category="topo_survey",
        capability_requirements={
            "hard": {
                "sensors_required": ["aerial_lidar"],
                "indoor_capable": False,
                "min_battery_percent": 30,
            }
        },
        budget_ceiling=Decimal("5.00"),
        sla_seconds=300,
    )
    robots = _make_robot_capabilities(100)

    def check_all():
        return [check_hard_constraints(task, r) for r in robots]

    benchmark(check_all)


def test_validate_task_spec(benchmark):
    """Validate a complex construction task spec."""
    spec = {
        "description": "Aerial LiDAR topographic survey for 12-acre highway corridor",
        "task_category": "topo_survey",
        "budget_ceiling": 5000.0,
        "sla_seconds": 86400,
        "latitude": 42.2917,
        "longitude": -85.5872,
        "capability_requirements": {
            "hard": {
                "sensors_required": ["aerial_lidar", "rtk_gps"],
                "min_battery_percent": 50,
                "certifications_required": ["licensed_surveyor"],
            },
            "soft": {
                "preferred_deliverables": ["LAS 1.4", "GeoTIFF"],
            },
        },
    }
    benchmark(validate_task_spec, spec)


def test_commitment_hash_throughput(benchmark):
    """SHA-256 commitment hash: 1000 iterations."""
    def hash_1000():
        for i in range(1000):
            compute_commitment_hash(f"req_{i}", f"salt_{i}")

    benchmark(hash_1000)


def test_post_and_score_lifecycle(benchmark):
    """Post task → score bids lifecycle with demo fleet."""
    fleet = create_demo_fleet()

    def lifecycle():
        engine = AuctionEngine(fleet)
        result = engine.post_task({
            "description": "Benchmark lifecycle",
            "task_category": "env_sensing",
            "capability_requirements": {
                "hard": {"sensors_required": ["temperature", "humidity"], "indoor_capable": True},
                "payload": {"format": "json", "fields": ["temperature_celsius"]},
            },
            "budget_ceiling": 1.00,
            "sla_seconds": 600,
        })
        engine.get_bids(result["request_id"])

    benchmark(lifecycle)


def test_wallet_1000_operations(benchmark):
    """Fund/debit/credit cycle x 1000 on WalletLedger."""
    def ops():
        w = WalletLedger()
        w.create_wallet("bench")
        w.fund_wallet("bench", Decimal("10000.00"), "seed")
        for i in range(1000):
            w.debit("bench", Decimal("1.00"), f"task_{i}", "escrow")
            w.credit("bench", Decimal("0.50"), f"task_{i}", "refund")

    benchmark(ops)


def test_decimals_to_strings(benchmark):
    """Convert a nested dict with 50 Decimal values to JSON-safe strings."""
    from auction.mcp_tools import _decimals_to_strings

    data = {
        "tasks": [
            {
                "id": f"task_{i}",
                "price": Decimal(f"{i * 1.5:.2f}"),
                "budget": Decimal(f"{i * 10:.2f}"),
                "score": Decimal(f"0.{85 + i % 15}"),
            }
            for i in range(50)
        ],
        "total": Decimal("5000.00"),
        "nested": {"deep": {"value": Decimal("123.456")}},
    }
    benchmark(_decimals_to_strings, data)
