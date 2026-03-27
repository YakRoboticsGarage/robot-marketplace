# Robot Task Auction Marketplace

## Project Overview

A marketplace where AI agents post tasks, physical robots bid autonomously, and winners are paid via Stripe (fiat) or USDC on Base (crypto). This project handles real money — payment code requires extreme care.

**v1.0 status:** Built. 151 tests, 15 MCP tools, ~11,400 LOC.
**Next:** v1.5 (crypto rail + privacy-aware foundation). See `docs/FEATURE_REQUIREMENTS_v15.md`.

## Architecture

- **Auction engine:** `auction/` — Task, Bid, AuctionResult, score_bids(), state machine
- **Payment:** Stripe Connect (fiat) + USDC on Base via x402 (crypto, v1.5)
- **Escrow:** `RobotTaskEscrow.sol` on Base with settlement abstraction (v1.5)
- **Fleet:** Robot discovery via ERC-8004, MCP tools for agent interaction
- **Persistence:** SQLite via `SyncTaskStore`
- **Robots:** tumbller (real hardware), tello (drone), fakerover (simulator)

## Key Commands

```bash
uv sync --all-extras                                    # Install everything
uv run pytest auction/tests/ -q --tb=short              # Unit tests (fast, no keys needed)
uv run pytest auction/tests/integration/ -m stripe      # Stripe integration (needs STRIPE_SECRET_KEY)
uv run pytest auction/tests/integration/ -m blockchain  # On-chain tests (needs BASE_SEPOLIA_RPC_URL)
uv run pytest auction/tests/integration/ -m fleet       # Fleet e2e (needs running fleet server)
uv run ruff check auction/ src/                         # Lint (includes security rules)
uv run mypy auction/                                    # Type check
uv run pytest --cov=auction auction/tests/              # Coverage report
```

## Payment Code Rules

- **NEVER** hardcode Stripe API keys, wallet private keys, or USDC addresses in source code. Use `.env` with `python-dotenv`.
- **ALL** payment operations must be idempotent — handle retries safely. Use idempotency keys for Stripe mutations.
- Stripe test mode (`sk_test_*`) for all development. Live keys only in production environment variables.
- **EVERY** payment state change must be logged to the audit trail in SQLite.
- Webhook handlers **MUST** verify Stripe signatures before processing.
- On-chain transactions **MUST** use commitment hash `H(request_id || salt)` per FD-4, never raw `request_id`.
- Robot wallet addresses must **NEVER** appear in API responses per PP-2. Use platform-internal `robot_id`.
- The settlement abstraction (FD-1) routes payments — do not add chain-specific logic outside the settlement layer.

## Testing Requirements

- Run `uv run pytest auction/tests/ -q` before committing any payment-related code change.
- Run `uv run ruff check` before committing any change.
- New payment features require both happy-path and failure-path tests.
- Property-based tests (hypothesis) for cryptographic operations and financial calculations.
- Wallet/escrow balances must never go negative under any test scenario.

## Decision Reference

Decisions live in `docs/DECISIONS.md` with IDs:
- **AD-X** = Architectural decisions
- **TC-X** = Technical constraints
- **PD-X** = Product decisions
- **FD-X** = Foundational design (cross-track, v1.5+)
- **PP-X** = Privacy-specific
- **LD-X** = Lunar-specific

Key decisions for v1.5: FD-1 (settlement abstraction), FD-4 (commitment hash), FD-5 (Horizen L3 eval), PP-2 (hidden wallet addresses).

## Project Structure

```
auction/
├── core.py              # Task, Bid, AuctionResult, signing
├── engine.py            # AuctionEngine, state machine, scoring
├── wallet.py            # WalletLedger
├── reputation.py        # ReputationTracker
├── stripe_service.py    # Stripe SDK integration
├── store.py             # SQLite persistence (SyncTaskStore)
├── discovery_bridge.py  # ERC-8004 robot discovery
├── mock_fleet.py        # Simulated robots for testing
├── demo.py              # Demo script
└── tests/
    ├── test_*.py        # Unit tests (mocked, fast)
    └── integration/     # Integration tests (need real services)
src/
├── core/
│   ├── plugin.py        # RobotPlugin base class
│   └── server.py        # Fleet MCP server
└── robots/
    ├── tumbller/        # Real hardware (ESP32-S3)
    ├── tello/           # DJI Tello drone
    └── fakerover/       # Simulator
docs/
├── FEATURE_REQUIREMENTS_v15.md  # v1.5 build spec
├── ROADMAP_v2.md                # 3-track roadmap
├── DECISIONS.md                 # All decisions (single source of truth)
├── DEVELOPMENT_STRATEGY.md      # Testing & code safety strategy
└── research/                    # Research synthesis documents
```

## Environment Variables

```
STRIPE_SECRET_KEY=sk_test_...     # Stripe test mode only
STRIPE_OPERATOR_ACCOUNT=acct_...  # Connect Express test account
AUCTION_DB_PATH=:memory:          # SQLite path (:memory: for tests)
SIGNING_MODE=ed25519              # or hmac for Phase 0
MCP_BEARER_TOKEN=                 # Fleet server auth
BASE_SEPOLIA_RPC_URL=             # For on-chain tests (v1.5)
FAKEROVER_URL=http://localhost:8080
```
