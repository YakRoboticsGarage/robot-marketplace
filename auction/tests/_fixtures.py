"""Shared fixtures for auction test suite."""

from __future__ import annotations

from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from auction.mock_fleet import create_demo_fleet
from auction.engine import AuctionEngine
from auction.reputation import ReputationTracker
from auction.wallet import WalletLedger


# ---------------------------------------------------------------------------
# Common task specs
# ---------------------------------------------------------------------------

VALID_TASK_SPEC = {
    "description": "Measure temperature and humidity in warehouse bay 3",
    "task_category": "env_sensing",
    "capability_requirements": {
        "hard": {
            "sensors_required": ["temperature", "humidity"],
            "indoor_capable": True,
        },
        "payload": {
            "format": "json",
            "fields": ["temperature_celsius", "humidity_percent"],
        },
    },
    "budget_ceiling": 1.00,
    "sla_seconds": 600,
}

WELDING_TASK_SPEC = {
    "description": "Inspect welding seam quality on assembly line",
    "task_category": "visual_inspection",
    "capability_requirements": {
        "hard": {
            "sensors_required": ["welding_sensor"],
        },
        "payload": {
            "format": "json",
            "fields": [],
        },
    },
    "budget_ceiling": 2.00,
    "sla_seconds": 300,
}

LIDAR_TASK_SPEC = {
    "description": "Aerial LiDAR topographic survey for highway corridor",
    "task_category": "topo_survey",
    "capability_requirements": {
        "hard": {
            "sensors_required": ["aerial_lidar"],
        },
    },
    "budget_ceiling": 5.00,
    "sla_seconds": 10,
}


# ---------------------------------------------------------------------------
# Mock httpx (used by any test that calls engine.execute())
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_httpx():
    """Patch httpx.AsyncClient with a canned sensor response."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"temperature": 22.5, "humidity": 45.0}
    mock_response.status_code = 200

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    mock_client_cls = MagicMock()
    mock_client_cls.return_value.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client_cls.return_value.__aexit__ = AsyncMock(return_value=False)

    with patch("auction.mock_fleet.httpx.AsyncClient", mock_client_cls):
        yield mock_client


# ---------------------------------------------------------------------------
# Engine fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def demo_fleet():
    """Create the standard demo fleet."""
    return create_demo_fleet()


@pytest.fixture
def engine(demo_fleet):
    """AuctionEngine with demo fleet, no wallet."""
    return AuctionEngine(demo_fleet)


@pytest.fixture
def funded_engine(demo_fleet):
    """AuctionEngine with demo fleet, funded wallet, and reputation tracker.

    Returns (engine, wallet, reputation).
    """
    wallet = WalletLedger()
    wallet.create_wallet("buyer")
    wallet.fund_wallet("buyer", Decimal("10.00"), "test_setup")
    rep = ReputationTracker()
    eng = AuctionEngine(demo_fleet, wallet=wallet, reputation=rep)
    return eng, wallet, rep
