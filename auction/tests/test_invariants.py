"""Tier 2: Property-based invariant tests.

Uses Hypothesis to verify that financial and state machine invariants
hold under random inputs. These catch edge cases that example-based
tests miss: overflow, boundary conditions, unexpected input combos.
"""

from __future__ import annotations

from decimal import Decimal

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st

from auction.core import (
    Bid,
    Task,
    check_hard_constraints,
    compute_commitment_hash,
    score_bids,
    verify_commitment,
)
from auction.wallet import WalletLedger


# ---------------------------------------------------------------------------
# Score invariants
# ---------------------------------------------------------------------------

def _make_task(budget="10.00"):
    return Task(
        request_id="inv-001",
        description="Invariant test",
        task_category="env_sensing",
        capability_requirements={},
        budget_ceiling=Decimal(budget),
        sla_seconds=600,
    )


def _make_bid(price, sla=300, confidence=0.9, robot_id="bot"):
    return Bid(
        robot_id=robot_id,
        request_id="inv-001",
        price=Decimal(str(price)),
        sla_commitment_seconds=sla,
        ai_confidence=confidence,
        capability_metadata={"sensors": ["temperature"]},
        reputation_metadata={"completion_rate": 0.95},
        bid_hash="test_hash",
    )


@given(
    price_low=st.decimals(min_value=Decimal("0.01"), max_value=Decimal("5.00"), places=2),
    price_high=st.decimals(min_value=Decimal("5.01"), max_value=Decimal("9.99"), places=2),
)
@settings(max_examples=50)
def test_score_monotonic_price(price_low, price_high):
    """Lower price (all else equal) never decreases score."""
    task = _make_task()
    bid_cheap = _make_bid(price_low, robot_id="cheap")
    bid_expensive = _make_bid(price_high, robot_id="expensive")
    scored = score_bids(task, [bid_cheap, bid_expensive])
    cheap_score = next(score for bid, score in scored if bid.robot_id == "cheap")
    expensive_score = next(score for bid, score in scored if bid.robot_id == "expensive")
    assert cheap_score >= expensive_score


@given(
    sla_fast=st.integers(min_value=60, max_value=300),
    sla_slow=st.integers(min_value=301, max_value=600),
)
@settings(max_examples=50)
def test_score_monotonic_sla(sla_fast, sla_slow):
    """Faster SLA commitment (all else equal) never decreases score."""
    task = _make_task()
    bid_fast = _make_bid(price=5.0, sla=sla_fast, robot_id="fast")
    bid_slow = _make_bid(price=5.0, sla=sla_slow, robot_id="slow")
    scored = score_bids(task, [bid_fast, bid_slow])
    fast_score = next(score for bid, score in scored if bid.robot_id == "fast")
    slow_score = next(score for bid, score in scored if bid.robot_id == "slow")
    assert fast_score >= slow_score


@given(conf=st.floats(min_value=0.01, max_value=1.0))
@settings(max_examples=50)
def test_score_bounded(conf):
    """Composite score is always in [0.0, 1.0]."""
    task = _make_task()
    bid = _make_bid(price=3.0, sla=300, confidence=conf)
    scored = score_bids(task, [bid])
    _, composite = scored[0]
    assert 0.0 <= composite <= 1.0


# ---------------------------------------------------------------------------
# Hard constraint determinism
# ---------------------------------------------------------------------------

@given(
    has_sensor=st.booleans(),
    indoor=st.booleans(),
    battery=st.integers(min_value=0, max_value=100),
)
@settings(max_examples=50)
def test_hard_constraints_deterministic(has_sensor, indoor, battery):
    """Same inputs always produce the same eligibility result."""
    task = Task(
        request_id="det-001",
        description="det",
        task_category="env_sensing",
        capability_requirements={
            "hard": {
                "sensors_required": ["temperature"],
                "indoor_capable": True,
                "min_battery_percent": 50,
            }
        },
        budget_ceiling=Decimal("1.00"),
        sla_seconds=60,
    )
    robot = {
        "sensors": ["temperature"] if has_sensor else ["photogrammetry"],
        "indoor_capable": indoor,
        "battery_percent": battery,
    }
    r1 = check_hard_constraints(task, robot)
    r2 = check_hard_constraints(task, robot)
    assert r1 == r2


# ---------------------------------------------------------------------------
# Commitment hash invariants
# ---------------------------------------------------------------------------

@given(
    rid=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=("L", "N"))),
    salt=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=("L", "N"))),
)
@settings(max_examples=50)
def test_commitment_hash_roundtrip(rid, salt):
    """compute then verify always succeeds."""
    h = compute_commitment_hash(rid, salt)
    assert verify_commitment(rid, salt, h)


@given(
    rid1=st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=("L", "N"))),
    rid2=st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=("L", "N"))),
    salt=st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=("L", "N"))),
)
@settings(max_examples=50)
def test_commitment_hash_unique(rid1, rid2, salt):
    """Different request_ids produce different hashes."""
    assume(rid1 != rid2)
    h1 = compute_commitment_hash(rid1, salt)
    h2 = compute_commitment_hash(rid2, salt)
    assert h1 != h2


# ---------------------------------------------------------------------------
# Wallet invariants
# ---------------------------------------------------------------------------

@given(
    amounts=st.lists(
        st.decimals(min_value=Decimal("0.01"), max_value=Decimal("10.00"), places=2),
        min_size=1,
        max_size=20,
    )
)
@settings(max_examples=30)
def test_wallet_balance_non_negative(amounts):
    """After any sequence of fund/debit, balance never goes negative."""
    w = WalletLedger()
    w.create_wallet("test")
    total_funded = Decimal("0")
    total_debited = Decimal("0")

    for i, amt in enumerate(amounts):
        # Alternate fund and debit
        if i % 2 == 0:
            w.fund_wallet("test", amt, f"fund_{i}")
            total_funded += amt
        else:
            try:
                w.debit("test", amt, f"debit_{i}", "escrow")
                total_debited += amt
            except (ValueError, Exception):
                pass  # Insufficient funds — that's correct behavior

    balance = w.get_balance("test")
    assert balance >= 0
