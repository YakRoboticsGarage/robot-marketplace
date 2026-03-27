"""
Shared fixtures for integration tests.

These tests hit real external services (Stripe test mode, Base Sepolia, fleet servers).
They require environment variables to be set — see markers in pyproject.toml.

Run with:
    uv run pytest auction/tests/integration/ -m stripe      # Stripe only
    uv run pytest auction/tests/integration/ -m blockchain   # On-chain only
    uv run pytest auction/tests/integration/ -m fleet        # Fleet e2e only
"""

from __future__ import annotations

import os

import pytest


def _require_env(var: str) -> str:
    """Get required env var or skip test."""
    val = os.environ.get(var)
    if not val:
        pytest.skip(f"{var} not set — skipping integration test")
    return val


# ---------------------------------------------------------------------------
# Stripe fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def stripe_api_key() -> str:
    """Real Stripe test-mode API key (sk_test_...)."""
    key = _require_env("STRIPE_SECRET_KEY")
    if not key.startswith("sk_test_"):
        pytest.fail("STRIPE_SECRET_KEY must be a test-mode key (sk_test_...), not live")
    return key


@pytest.fixture
def stripe_operator_account() -> str:
    """Stripe Connect Express test operator account ID."""
    return _require_env("STRIPE_OPERATOR_ACCOUNT")


# ---------------------------------------------------------------------------
# Blockchain fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def base_sepolia_rpc() -> str:
    """Base Sepolia RPC URL for on-chain tests."""
    return _require_env("BASE_SEPOLIA_RPC_URL")


@pytest.fixture
def test_wallet_key() -> str:
    """Private key for a funded Base Sepolia test wallet."""
    return _require_env("TEST_WALLET_PRIVATE_KEY")


# ---------------------------------------------------------------------------
# Fleet fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def fleet_url() -> str:
    """URL of a running fleet server with at least one robot."""
    return _require_env("FLEET_URL")


@pytest.fixture
def fleet_bearer_token() -> str:
    """Bearer token for fleet server auth."""
    return _require_env("MCP_BEARER_TOKEN")
