# Security Audit Report -- v0.51

**Auditor:** Security research agent (Claude Opus 4.6)
**Date:** 2026-03-27
**Scope:** All source files in `auction/` (core.py, engine.py, mcp_tools.py, stripe_service.py, wallet.py, store.py, discovery_bridge.py, reputation.py, mock_fleet.py)
**Codebase version:** v1.0 (~11,400 LOC, 15 MCP tools)

---

## Executive Summary

The codebase demonstrates solid foundational design -- parameterized SQL queries, timing-safe HMAC comparison, clear state machine transitions, and disciplined Decimal handling for money. However, the audit identified **3 critical**, **5 high**, **7 medium**, and **6 low** findings. The critical issues center on the absence of authentication/authorization on MCP tools, a race condition between wallet balance checks and debits, and the HMAC shared-secret signing model that allows the platform to forge bids on behalf of any robot. These must be resolved before handling real money.

---

## Critical Findings

### C-1: No Authentication or Authorization on MCP Tools

**File:** `auction/mcp_tools.py` (all tool registrations, lines 129-631)

**Description:** None of the 15 MCP tools perform any authentication or authorization checks. Any MCP client that can connect to the server can call any tool -- including `auction_fund_wallet` (create money from nothing), `auction_confirm_delivery` (release payments), `auction_cancel_task` (refund to attacker), and `auction_reject_delivery` (deny payment to operators).

**Exploit scenario:**
1. Attacker connects to the MCP server.
2. Calls `auction_fund_wallet(wallet_id="buyer", amount=1000000)` to credit $1M to a wallet.
3. Posts tasks, accepts bids, confirms deliveries -- all payments flow to attacker-controlled operator accounts.
4. Alternatively: calls `auction_cancel_task` on another buyer's in-progress task, causing a refund to the "buyer" wallet (which is shared -- see C-3).

**Recommended fix:** Implement MCP bearer token authentication (the `MCP_BEARER_TOKEN` env var is defined in CLAUDE.md but never enforced). Add per-tool authorization with wallet ownership checks. Each wallet operation must verify the caller owns the wallet_id.

---

### C-2: Race Condition in Wallet Balance Check and Debit (TOCTOU)

**File:** `auction/engine.py:670-674`, `auction/wallet.py:151-183`

**Description:** In `accept_bid()`, the wallet balance is checked (`check_balance`) and then debited (`debit`) in two separate, non-atomic operations. In a concurrent environment (multiple async tasks or MCP tool calls), a buyer could pass the balance check for two tasks simultaneously, then both debits succeed, driving the balance negative.

```python
# engine.py:670-674 -- NOT ATOMIC
if not self.wallet.check_balance("buyer", bid.price):   # Step 1: check
    raise InsufficientBalance(...)
self.wallet.debit("buyer", reservation, ...)              # Step 2: debit
```

The `debit()` method in `wallet.py:170` does its own balance check, but `WalletLedger` has no locking mechanism. Two concurrent `accept_bid` calls for different tasks can both pass line 170 before either subtracts from the balance.

**Exploit scenario:**
1. Buyer has $1.00 in wallet.
2. Two tasks are posted with `budget_ceiling=$1.00` each.
3. Two concurrent `accept_bid` calls both read balance as $1.00 before either debit completes.
4. Both debits of $0.25 succeed, and later both delivery payments of $0.75 succeed.
5. Total debited: $2.00 from a $1.00 wallet. Balance goes to -$1.00.

**Recommended fix:** Add a threading lock (or asyncio lock) around all wallet mutations. Alternatively, make `check_and_debit` an atomic operation. If using SQLite persistence, wrap balance check + debit in a single transaction with `SELECT ... FOR UPDATE` semantics (or use SQLite's single-writer lock).

---

### C-3: Single Shared "buyer" Wallet -- No Multi-Tenancy

**File:** `auction/engine.py:671`, `auction/mcp_tools.py:415-459`

**Description:** The entire system uses a single hardcoded wallet ID `"buyer"` for all buyer operations. The `accept_bid` method always debits from `"buyer"` (line 671). The `auction_fund_wallet` tool defaults to `wallet_id="buyer"`. There is no concept of per-user wallets.

**Exploit scenario:**
1. Buyer A funds the "buyer" wallet with $100.
2. Buyer B (different MCP client, no auth -- see C-1) posts a task and accepts a bid.
3. The 25% reservation is debited from the shared "buyer" wallet -- spending Buyer A's money.
4. On delivery, Buyer B confirms and the remaining 75% is also debited from Buyer A's funds.

**Recommended fix:** Associate each MCP session with an authenticated user identity. Map users to wallet IDs. Pass `wallet_id` through the task lifecycle rather than hardcoding `"buyer"`. Enforce that only the wallet owner can debit their wallet.

---

## High Findings

### H-1: HMAC Shared Secret Allows Platform to Forge Bids

**File:** `auction/core.py:395-408`, `auction/mock_fleet.py:133` (signing keys)

**Description:** In HMAC mode (the default, `SIGNING_MODE="hmac"`), bid signing uses a shared secret between the robot and the platform. The platform (AuctionEngine) has access to every robot's `signing_key` via `robot.signing_key`. This means the platform can forge bids on behalf of any robot -- the signature is indistinguishable from a genuine robot signature.

The signing keys are also hardcoded plaintext strings in `mock_fleet.py` (e.g., `"bay3_secret_key_v01"`, line 133) and `discovery_bridge.py` (`"default_hmac_key"`, line 174).

**Impact:** The bid signing mechanism provides no real non-repudiation in HMAC mode. A compromised or malicious platform operator could create fake bids to manipulate auction outcomes.

**Recommended fix:** Migrate to Ed25519 signing mode (`SIGNING_MODE="ed25519"`) where robots hold private keys and the platform only knows public addresses. The infrastructure for this exists in `core.py:411-449` but is not the default. Remove all hardcoded signing keys from source code.

---

### H-2: Bids with Invalid Signatures Are Still Accepted

**File:** `auction/engine.py:573-588`

**Description:** In `get_bids()`, bid signatures are verified and the result is logged and included in the response as `signature_valid`, but bids with invalid signatures are **not rejected**. They remain in the bid list and can be accepted. The only check at acceptance time (line 665) does verify, but the initial collection does not filter.

```python
# engine.py:573-574 -- verification result is logged but not enforced
sig_valid = verify_bid(bid, robot.signing_key)
log("VERIFY", f"{bid.robot_id} bid signature: {'VALID' if sig_valid else 'INVALID'}")
# bid is still added to bid_details regardless of sig_valid
```

While `accept_bid` does re-verify (line 665), a compromised robot could submit a bid, have it scored and recommended, and only fail at acceptance time -- wasting system resources and potentially causing the agent to select a robot that cannot actually fulfill.

**Impact:** A malicious actor that can inject a robot into the fleet can submit bids with forged signatures. These bids will be scored and potentially recommended. The acceptance-time check catches it, but the damage to the auction flow is already done.

**Recommended fix:** Filter out bids with invalid signatures in `get_bids()` before scoring. Do not include them in `bid_details` or in scoring.

---

### H-3: Stripe API Key Set as Global Module State

**File:** `auction/stripe_service.py:39-40`

**Description:** When a `StripeService` is initialized with an API key, it sets `stripe.api_key = api_key` as a module-level global. This means:
1. The API key is accessible to any code in the process via `stripe.api_key`.
2. If multiple `StripeService` instances are created (e.g., in tests), they clobber each other's keys.
3. The key persists in memory for the lifetime of the process.

**Recommended fix:** Use per-request API key passing: `stripe.PaymentIntent.create(..., api_key=self.api_key)` instead of setting the global. This is supported by the Stripe SDK and is the recommended pattern for multi-tenant applications.

---

### H-4: No Idempotency Keys on Stripe Mutations

**File:** `auction/stripe_service.py:68-76`, `auction/stripe_service.py:151-160`

**Description:** `create_wallet_topup()`, `create_connect_account()`, and `create_transfer()` do not pass idempotency keys to Stripe API calls. The CLAUDE.md explicitly states: "ALL payment operations must be idempotent -- handle retries safely. Use idempotency keys for Stripe mutations."

**Exploit scenario:** A network timeout during `create_transfer()` causes the caller to retry. Without an idempotency key, Stripe creates a second transfer -- the operator receives double payment.

**Recommended fix:** Generate deterministic idempotency keys from the `request_id` + operation type (e.g., `f"transfer_{request_id}"`) and pass them as `idempotency_key` to every Stripe mutation.

---

### H-5: StripeWalletService Credits Wallet Before Payment Confirmation

**File:** `auction/wallet.py:276-285`

**Description:** `StripeWalletService.fund_wallet()` calls `stripe.create_wallet_topup()` (which creates a PaymentIntent) and then immediately credits the internal ledger. A PaymentIntent creation does not mean the money has been collected -- it needs to be confirmed/captured. The code even has a comment acknowledging this:

```python
# (In live mode you would wait for webhook confirmation; for v1.0
# we credit immediately for simplicity.)
```

**Impact:** In live mode, a buyer could create a PaymentIntent with a card that will be declined, but the internal ledger is already credited. The buyer now has phantom balance they can spend.

**Recommended fix:** In live mode, only credit the ledger upon receiving a `payment_intent.succeeded` webhook from Stripe. In stub/test mode, the current behavior is acceptable.

---

## Medium Findings

### M-1: No Rate Limiting or Resource Limits on Task/Bid Creation

**File:** `auction/engine.py:449-535`, `auction/mcp_tools.py:130-186`

**Description:** There are no limits on:
- Number of tasks a single buyer can post
- Number of concurrent active tasks
- Number of re-pool rounds for a single task
- Frequency of MCP tool calls

**Impact:** An attacker (or misbehaving agent) could flood the system with thousands of tasks, exhausting memory (all tasks are held in `_tasks` dict) and CPU (each task triggers bid collection from all robots).

**Recommended fix:** Add per-wallet rate limits (e.g., max 100 active tasks). Add a maximum re-pool round count (e.g., 5). Consider memory bounds on `_tasks`.

---

### M-2: Operator Payment Credits Full Agreed Price Instead of Agreed Price Minus Platform Fee

**File:** `auction/engine.py:866-874`

**Description:** In `confirm_delivery()`, the buyer is debited 25% (reservation) + 75% (delivery) = 100% of the agreed price. But the operator is credited the **full agreed price**:

```python
# engine.py:866 -- credits full agreed_price, not delivery_payment
self.wallet.credit(record.winning_bid.robot_id, agreed_price, ...)
```

The buyer pays 25% + 75% = 100%. The operator receives 100%. There is no platform fee retained. This is internally consistent but means the platform has no revenue model in the ledger. More importantly, the Stripe transfer (line 892) also sends `agreed_price * 100` cents -- the full amount. If platform fees are intended, this is a financial leak.

**Recommended fix:** Clarify whether the 25%/75% split is meant to include a platform fee. If so, deduct the fee before crediting the operator. If not, document that the platform operates at zero margin in v1.

---

### M-3: cancel_task Allows Transition from States Not in VALID_TRANSITIONS

**File:** `auction/engine.py:1086-1128`

**Description:** `cancel_task()` transitions any non-terminal task to `WITHDRAWN` by calling `_transition()`. However, `VALID_TRANSITIONS` only allows `WITHDRAWN` from specific states: `POSTED`, `BIDDING`, `BID_ACCEPTED`, `IN_PROGRESS`, `DELIVERED`, `RE_POOLED`. It does **not** allow `WITHDRAWN` from `REJECTED`, `ABANDONED`, or `PROVIDER_CANCELLED`.

If a task is in state `REJECTED` (between rejection and re-pooling, though this is typically fast), calling `cancel_task` would raise a `ValueError` from `_transition`. This is actually correct behavior, but the MCP tool description says "Works in any state except settled and withdrawn" which is misleading.

**Recommended fix:** Either update `VALID_TRANSITIONS` to allow `WITHDRAWN` from all non-terminal states, or update the tool description to accurately list which states support cancellation.

---

### M-4: Task Description and Capability Requirements Not Sanitized

**File:** `auction/core.py:105-194`, `auction/engine.py:449-470`

**Description:** Task descriptions are arbitrary strings with no length limit or content validation. `capability_requirements` is an arbitrary dict that is serialized to JSON and stored in SQLite. While SQLite parameterized queries prevent SQL injection, there is no protection against:
- Extremely large task descriptions consuming memory
- Deeply nested `capability_requirements` dicts causing stack overflow during JSON serialization
- Task descriptions containing control characters or encoding attacks

**Recommended fix:** Add maximum length limits for `description` (e.g., 10,000 chars). Add maximum depth/size limits for `capability_requirements`. Sanitize or reject control characters in string fields.

---

### M-5: SIGNING_MODE Read Once at Import Time -- Cannot Be Changed Securely

**File:** `auction/core.py:39`

**Description:** `SIGNING_MODE = os.environ.get("SIGNING_MODE", "hmac")` is read once at module import time. If the environment variable is changed after import, the signing mode does not update. The comment says "Tests override via monkeypatch on the module attr" -- meaning test code directly mutates `core.SIGNING_MODE`, which is a fragile pattern.

More concerning: the default is `"hmac"` (the weaker mode). If `SIGNING_MODE` is not explicitly set in the environment, the system silently uses the less secure HMAC signing.

**Recommended fix:** Default to `"ed25519"` when `eth_account` is available. Log a warning when falling back to HMAC mode. Consider reading the signing mode from a configuration object rather than a module-level constant.

---

### M-6: Ed25519 Fallback Silently Downgrades to HMAC

**File:** `auction/core.py:417-423`, `auction/core.py:437-442`

**Description:** When `SIGNING_MODE="ed25519"` but `eth_account` is not installed, `_sign_bid_ed25519` and `_verify_bid_ed25519` silently fall back to HMAC with only a `RuntimeWarning`. This means a deployment could believe it is using Ed25519 signing while actually using HMAC -- a significant security downgrade.

**Recommended fix:** Raise an error instead of silently falling back when `SIGNING_MODE="ed25519"` but `eth_account` is not installed. A silent downgrade of cryptographic security is dangerous.

---

### M-7: Auto-Accept Timer Creates Unguarded Background Task

**File:** `auction/engine.py:414-443`

**Description:** `_start_auto_accept_timer` creates an `asyncio.Task` that sleeps for `auto_accept_seconds` and then calls `confirm_delivery`. This background task:
1. Has no error handling -- if `confirm_delivery` raises, the exception is silently swallowed by asyncio.
2. Holds a reference to `request_id` but not the record -- if the record is somehow removed from `_tasks`, the callback will raise `KeyError`.
3. Can fire even if the engine is shutting down, potentially causing operations on a half-torn-down system.

**Recommended fix:** Add exception handling in `_auto_accept_callback`. Register a done-callback to log failures. Consider using a more robust scheduling mechanism.

---

## Low Findings

### L-1: Signing Keys Hardcoded in Source Code

**File:** `auction/mock_fleet.py:133,166,192,219,248`, `auction/discovery_bridge.py:174,215`

**Description:** HMAC signing keys like `"bay3_secret_key_v01"`, `"default_hmac_key"` are hardcoded in source files. While these are for mock/demo robots, the pattern could be copied to production code. The `discovery_bridge.py` default key `"default_hmac_key"` is particularly dangerous as it is the default for all on-chain discovered robots.

**Recommended fix:** Load signing keys from environment variables or a secrets manager. Document that mock fleet keys must never be used in production.

---

### L-2: Stripe Error Responses Leak Error Type Class Names

**File:** `auction/stripe_service.py:76,107,125,160,180`

**Description:** Stripe error handlers return `"error_type": type(exc).__name__`, which leaks Python Stripe SDK exception class names (e.g., `"CardError"`, `"InvalidRequestError"`). While the MCP tools in `mcp_tools.py` are careful to not expose Python class names, the Stripe service returns them directly.

**Recommended fix:** Map Stripe exception types to stable, documented error codes (e.g., `"CARD_DECLINED"`, `"INVALID_REQUEST"`).

---

### L-3: Wallet Balance and Bid Amounts Logged to stdout

**File:** `auction/engine.py:675,756,863,901`

**Description:** Payment amounts, reservation amounts, and wallet operations are logged via `log()` which writes to stdout. In a production environment, these logs could be captured by log aggregation systems, exposing financial details.

**Recommended fix:** Use structured logging with appropriate log levels. Mark financial log lines as sensitive or ensure log aggregation applies PII/financial data masking.

---

### L-4: No Input Validation on wallet_id Parameter

**File:** `auction/mcp_tools.py:415-459`, `auction/wallet.py:117-123`

**Description:** `wallet_id` is an arbitrary string with no validation. Callers can create wallets with names like `""`, `"../../etc/passwd"`, or very long strings. While this does not cause injection (SQLite parameterized queries are used), it could cause confusion in the ledger or be used for social engineering.

**Recommended fix:** Validate `wallet_id` against a pattern (e.g., alphanumeric + underscore, max 64 chars).

---

### L-5: auction_get_operator_status Uses Predictable Account ID Convention

**File:** `auction/mcp_tools.py:522`

**Description:** The operator status tool constructs the Stripe account ID as `f"acct_{robot_id}"`. This is a predictable mapping that leaks information about the Stripe Connect account structure. An attacker who knows a robot_id can derive the Stripe account ID.

**Recommended fix:** Use an opaque mapping (e.g., a lookup table) between `robot_id` and Stripe account ID rather than a predictable convention.

---

### L-6: SQLite Database File Permissions Not Set

**File:** `auction/store.py:88-102`, `auction/store.py:563-577`

**Description:** When creating a SQLite database on disk (non-`:memory:`), neither `TaskStore` nor `SyncTaskStore` sets restrictive file permissions. The database file inherits the default umask, which may be world-readable, exposing task data, wallet balances, and bid details.

**Recommended fix:** Set file permissions to `0o600` (owner-only read/write) when creating the database file. Check permissions on startup if the file already exists.

---

## Positive Observations

1. **Parameterized SQL queries throughout.** Both `TaskStore` and `SyncTaskStore` use parameterized queries (`?` placeholders) consistently. No string interpolation of user input into SQL. This effectively prevents SQL injection.

2. **Timing-safe HMAC comparison.** `_verify_bid_hmac` (core.py:408) uses `hmac.compare_digest()` for signature verification, preventing timing side-channel attacks.

3. **Decimal for all money.** All monetary values use `Decimal` rather than `float`, preventing floating-point precision errors in financial calculations. The `quantize()` calls for 25%/75% splits ensure consistent rounding.

4. **Explicit state machine with validated transitions.** `VALID_TRANSITIONS` (engine.py:72-87) defines a clear adjacency list, and `_transition()` enforces it. Tasks cannot skip states arbitrarily.

5. **Structured error responses.** The `_error_response` pattern in `mcp_tools.py` maps exceptions to agent-friendly error dicts with `error_code`, `message`, and `hint` -- never exposing Python internals to MCP consumers.

6. **Stub mode for Stripe.** The `StripeService` gracefully degrades to stub mode when no API key is provided, preventing accidental real-money operations during development.

7. **WAL journal mode for SQLite.** Both stores set `PRAGMA journal_mode=WAL`, enabling concurrent readers during writes and reducing corruption risk.

8. **Bid re-verification at acceptance time.** `accept_bid()` re-verifies the bid signature (engine.py:665) as a defense-in-depth measure.

---

## Recommended v0.51 Fixes

Prioritized by severity and implementation effort:

1. **[C-1] Add MCP authentication.** Enforce `MCP_BEARER_TOKEN` on all tool calls. This is the single highest-impact fix -- without it, all other controls are bypassable. *Effort: 1-2 hours.*

2. **[C-2] Add wallet locking.** Wrap `check_balance` + `debit` in a `threading.Lock` (or `asyncio.Lock` for async callers). Alternatively, make `debit()` the sole balance-check point (it already checks, just ensure atomicity). *Effort: 1 hour.*

3. **[C-3] Add wallet ownership.** Pass `wallet_id` through the task lifecycle. Each task should record which wallet is being charged. Verify ownership before debit operations. *Effort: 4-8 hours (requires schema change).*

4. **[H-2] Reject invalid-signature bids in get_bids().** Add a `if not sig_valid: continue` after verification, or at minimum mark them ineligible. *Effort: 15 minutes.*

5. **[H-4] Add Stripe idempotency keys.** Pass `idempotency_key=f"{operation}_{request_id}"` to all Stripe mutations. *Effort: 30 minutes.*

6. **[H-3] Use per-request Stripe API keys.** Replace `stripe.api_key = api_key` with per-call `api_key=` parameter. *Effort: 30 minutes.*

7. **[H-5] Defer wallet credit until Stripe webhook.** In live mode, only credit the ledger on `payment_intent.succeeded` webhook. *Effort: 2-4 hours (requires webhook handler).*

8. **[M-6] Fail hard on Ed25519 fallback.** Replace silent HMAC fallback with `RuntimeError` when `SIGNING_MODE="ed25519"` and `eth_account` is missing. *Effort: 15 minutes.*

9. **[M-1] Add rate limits.** Max active tasks per wallet, max re-pool rounds per task. *Effort: 1-2 hours.*

10. **[M-4] Add input size limits.** Max description length, max capability_requirements depth/size. *Effort: 1 hour.*
