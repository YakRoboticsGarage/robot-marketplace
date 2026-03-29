# QA Assessment Report -- v0.51

**Date:** 2026-03-27
**Assessor:** Claude (automated QA review)
**Scope:** All 9 source files, all 10 test files, 146 passing tests + 4 known failures

---

## Executive Summary

The test suite is solid for a v0.5/v1.0 codebase: 146 tests pass, covering the happy-path lifecycle, wallet operations, reputation tracking, SQLite persistence, Stripe integration, Ed25519 signing, and the discovery bridge. Estimated line-level coverage is **~70-75%** across the auction package.

**Findings by classification:**

| Type | Count |
|------|-------|
| BUG | 5 |
| COVERAGE_GAP | 14 |
| EDGE_CASE | 9 |
| FLAKY | 2 |
| QUALITY | 4 |
| **Total** | **34** |

The most critical issues are: (1) the `confirm_delivery` plausibility check rejects `None` temperature values with a misleading error path instead of catching them cleanly, (2) the `cancel_task` transition uses an illegal shortcut that will crash for certain states, (3) no test covers the `cancel_task` path at all, and (4) wallet balance consistency is not verified end-to-end after re-pool cycles.

---

## Bugs Found

### BUG-1: `cancel_task` transitions directly to WITHDRAWN from states not in VALID_TRANSITIONS

**File:** `auction/engine.py:1120`

The `cancel_task` method calls `_transition(record, TaskState.WITHDRAWN, ...)` regardless of current state. However, `VALID_TRANSITIONS` only allows WITHDRAWN from: `POSTED`, `BIDDING`, `BID_ACCEPTED`, `IN_PROGRESS`, `DELIVERED`, `RE_POOLED`. If the task is in state `REJECTED`, `ABANDONED`, or `PROVIDER_CANCELLED`, the `_transition` call will raise `ValueError("Invalid transition: rejected -> withdrawn")`.

**Expected:** cancel_task should work from any non-terminal state.
**Actual:** Crashes for REJECTED, ABANDONED, PROVIDER_CANCELLED states.
**Suggested fix:** Either add WITHDRAWN to the valid targets for those intermediate states, or transition through RE_POOLED first, or handle the `_transition` exception.

### BUG-2: `confirm_delivery` plausibility check does not catch `None` temperature correctly

**File:** `auction/engine.py:846`

```python
if temp is not None and not (-40 <= temp <= 85):
```

When `BadPayloadRobot` delivers `{"temperature_celsius": None}`, `temp is not None` evaluates to `False`, so the check is skipped. The test `test_bad_payload_rejected` passes only because `confirm_delivery` raises *some* ValueError, but actually for the wrong reason -- the `None` value passes plausibility but may fail elsewhere or slip through entirely if the payload structure changes. A `None` temperature from a sensor is clearly invalid data and should be explicitly rejected.

**Expected:** `None` values for numeric sensor fields should be rejected.
**Actual:** `None` passes the plausibility check silently.
**Suggested fix:** Add an explicit None check: `if temp is None and "temperature_celsius" in required_fields: raise ValueError(...)`.

### BUG-3: `confirm_delivery` humidity check allows `humidity_percent = -1`

**File:** `auction/engine.py:848-849`

```python
if humidity is not None and not (0 <= humidity <= 100):
```

`BadPayloadRobot` delivers `humidity_percent: -1`. The check `not (0 <= -1 <= 100)` evaluates to `True`, so this is caught. However, this is only because the test uses `-1`. If `BadPayloadRobot` returned `humidity_percent: 0` (edge case -- potentially valid or invalid depending on context), the check would pass. More importantly, the `temperature_celsius: None` issue (BUG-2) means the test catches the wrong field's error.

### BUG-4: `accept_bid` balance check uses full `bid.price` instead of 25% reservation amount

**File:** `auction/engine.py:671`

```python
if not self.wallet.check_balance("buyer", bid.price):
    raise InsufficientBalance("buyer", bid.price, self.wallet.get_balance("buyer"))
```

The check verifies whether the buyer can cover the *full bid price*, but only debits 25%. This means a buyer with $0.40 balance cannot accept a $0.50 bid even though the reservation is only $0.13. The debit on line 673 correctly debits only the 25% reservation.

**Expected:** Balance check should compare against the 25% reservation amount.
**Actual:** Compares against full price, which is overly restrictive.
**Suggested fix:** Change `bid.price` to `reservation` in the `check_balance` call.

### BUG-5: `_start_auto_accept_timer` is called during `accept_bid` (line 692), not after delivery

**File:** `auction/engine.py:692`

The auto-accept timer is started when a bid is accepted (BID_ACCEPTED state), but the `_auto_accept_callback` checks `if record.state == TaskState.DELIVERED`. This means the timer starts ticking from bid acceptance, not from delivery. If execution takes a long time, the auto-accept could fire before the buyer even sees the delivery. The timer should start in the `execute` method after transitioning to DELIVERED.

**Expected:** Auto-accept timer starts after delivery is received.
**Actual:** Timer starts at bid acceptance. If `auto_accept_seconds=3600` and execution takes 3500s, buyer gets only 100s to review.
**Note:** The test `test_auto_accept_timer` passes because execution is near-instant (mocked). This bug would only manifest with real execution delays.

---

## Coverage Gaps

### COVERAGE_GAP-1: `cancel_task` has ZERO test coverage

**Risk: HIGH** -- This is a recovery tool for stuck tasks with real money implications (refund path). Not a single test calls `engine.cancel_task()`.

**Suggested tests:**
- Cancel from BIDDING state (no refund needed)
- Cancel from BID_ACCEPTED state (25% refund)
- Cancel from DELIVERED state (25% refund)
- Cancel from SETTLED state (should raise ValueError)
- Cancel from WITHDRAWN state (should raise ValueError)

### COVERAGE_GAP-2: `abandon_task` has ZERO test coverage

**Risk: HIGH** -- The manual abandonment path (both default and `provider_cancelled` variants) is untested.

**Suggested tests:**
- `abandon_task(request_id)` from IN_PROGRESS state
- `abandon_task(request_id, reason="provider_cancelled")` from BID_ACCEPTED state
- Wallet refund on abandonment
- Reputation recording on abandonment

### COVERAGE_GAP-3: `get_task_status` has ZERO test coverage

**Risk: MEDIUM** -- The status tool is agent-facing and returns complex state. The `available_actions` and `hint` logic could have errors.

### COVERAGE_GAP-4: MCP tools `auction_fund_wallet`, `auction_get_wallet_balance` not tested via the MCP layer

Only the underlying `WalletLedger` and `StripeWalletService` are tested. The MCP wrappers (with their error handling and fallback paths) are not.

### COVERAGE_GAP-5: MCP tools `auction_onboard_operator`, `auction_get_operator_status` not tested

These wrap StripeService calls with error handling that is unique to the MCP layer.

### COVERAGE_GAP-6: MCP tool `auction_quick_hire` not tested

**Risk: HIGH** -- This is a multi-step orchestration tool that handles 5 failure modes. None are tested.

### COVERAGE_GAP-7: MCP tool `auction_accept_and_execute` not tested

### COVERAGE_GAP-8: `_error_response` mapping logic in `mcp_tools.py` not tested

The error-to-structured-response mapping has complex conditional logic (lines 53-101) with no dedicated tests.

### COVERAGE_GAP-9: `SyncTaskStore` not tested independently

Only `TaskStore` (async) has tests. `SyncTaskStore` is tested implicitly through the engine integration tests, but its individual methods (`save_task`, `load_task`, `load_active_tasks`, `close`) have no direct tests.

### COVERAGE_GAP-10: `_load_from_store` restart recovery for DELIVERED state (auto-accept timer restart)

**File:** `auction/engine.py:234`

When restoring from store, if a task is in DELIVERED state, `_start_auto_accept_timer` is called. But the timer is based on `auto_accept_seconds` from task creation, not from the original delivery time. After restart, the full timer restarts, giving the buyer extra time. No test covers this.

### COVERAGE_GAP-11: `validate_task_spec` -- only tested indirectly through `post_task`

The function returns a list of all errors at once, but no test verifies that multiple validation errors are returned simultaneously.

### COVERAGE_GAP-12: Wallet `fund_wallet` method (distinct from `create_wallet` + manual balance setting)

While `WalletLedger.fund_wallet` is tested, the negative paths are not: funding a non-existent wallet, funding with zero/negative amount.

### COVERAGE_GAP-13: `_decimals_to_strings` in mcp_tools.py -- no test for nested structures

### COVERAGE_GAP-14: `infer_task_category` only tested indirectly

The function handles several branches (rgb_camera, lidar, temperature, etc.) but only the temperature path is exercised through Task creation tests.

---

## Edge Cases Missing

### EDGE_CASE-1: Concurrent task acceptance on the same auction

**Scenario:** Two agents call `accept_bid` simultaneously for different robots on the same request_id.
**Why it matters:** In-memory dict mutation is not thread-safe. If the MCP server handles concurrent requests, both could pass the state check.
**Suggested test:** Use threading to call `accept_bid` twice simultaneously; assert exactly one succeeds.

### EDGE_CASE-2: Exactly $0.50 budget with $0.50 bid (boundary)

**Scenario:** `budget_ceiling = $0.50`, robot bids exactly `$0.50`.
**Why it matters:** `score_bids` computes `price_score = 1 - (0.50 / 0.50) = 0.0`. The bid is not excluded (only `>` budget is excluded), but gets a zero price score. The bid may still win if other scores are high enough, but the edge is worth validating.
**Suggested test:** Post a task with `budget_ceiling=0.50`, have a robot bid exactly `0.50`, verify it is scored and eligible.

### EDGE_CASE-3: Zero eligible bids (all over budget)

**Scenario:** All robots bid above budget_ceiling.
**Why it matters:** `score_bids` returns empty list, `recommended_winner` is None. The `quick_hire` tool has a path for this, but it's untested.

### EDGE_CASE-4: Re-pool exhaustion (all robots excluded)

**Scenario:** 2-robot fleet. Robot A wins round 1, gets rejected. Robot B wins round 2, gets rejected. Round 3 has 0 eligible robots.
**Why it matters:** The task should transition to WITHDRAWN, not hang in BIDDING with no robots.
**Suggested test:** Verify task transitions to WITHDRAWN when all robots have been previous winners.

### EDGE_CASE-5: Negative wallet balance protection under concurrent debits

**Scenario:** Two tasks accepted simultaneously, both try to debit from the same buyer wallet.
**Why it matters:** Real money. The `check_balance` + `debit` is not atomic -- a TOCTOU race could allow overdraft.
**Suggested test:** Verify InsufficientBalance is raised if balance drops between check and debit (requires mocking or threading).

### EDGE_CASE-6: Float-to-Decimal conversion precision in MCP tools

**Scenario:** `auction_fund_wallet(amount=10.1)` -- the float `10.1` cannot be represented exactly.
**Why it matters:** `Decimal(str(10.1))` produces `Decimal('10.1')` which is correct. But if anyone passes `Decimal(10.1)` directly (without str conversion), they get `Decimal('10.09999999999999964472863211994990706443786621093750')`.
**Note:** The code consistently uses `Decimal(str(amount))`, which is correct. But the MCP tool signatures accept `float`, so this boundary should be tested.

### EDGE_CASE-7: SLA exactly met (elapsed == sla_seconds)

**Scenario:** Robot delivers at exactly the SLA deadline.
**Why it matters:** `sla_met = elapsed_seconds <= task.sla_seconds` uses `<=`, so exactly-at-deadline is "met". This is correct but should have a test documenting the boundary.

### EDGE_CASE-8: Task with no `payload` in capability_requirements

**Scenario:** `capability_requirements = {"hard": {"sensors_required": ["temperature"]}}` with no `payload` key.
**Why it matters:** `confirm_delivery` does `payload_spec = task.capability_requirements.get("payload", {})` and then `required_fields = payload_spec.get("fields", [])`. This means no fields are required, so any delivery passes. This is by design but should be tested to document the behavior.

### EDGE_CASE-9: Duplicate wallet creation

**Scenario:** Calling `create_wallet("buyer")` twice.
**Why it matters:** The `fund_wallet` MCP tool creates the wallet if it doesn't exist (line 436), but if it already exists, `create_wallet` raises ValueError. The try/except on line 434-436 handles this, but the path is untested.

---

## Existing Test Issues

### test_fakerover_bid.py -- 4 failures (root cause analysis)

**Root cause:** The `FakeRoverPlugin` class in `yakrover-8004-mcp/src/robots/fakerover/__init__.py` does NOT implement a `bid()` method. It inherits from `RobotPlugin`, whose default `bid()` returns `None`. The test file imports the real plugin from the sibling repo and expects it to have a working `bid()` implementation, but no one has added that method to `FakeRoverPlugin` yet.

**Affected tests (4):**
- `test_bid_returns_dict_when_capable` -- asserts `isinstance(result, dict)` but gets `None`
- `test_bid_has_required_fields` -- `None.keys()` -> AttributeError
- `test_bid_price_is_decimal_string` -- `None["price"]` -> TypeError
- `test_bid_capability_metadata_sensors` -- `None["capability_metadata"]` -> TypeError

**Passing tests (2):**
- `test_bid_returns_none_when_incapable` -- correctly expects `None`
- `test_bid_returns_none_when_simulator_offline` -- correctly expects `None`

**Fix:** Implement `async def bid(self, task_spec: dict) -> dict | None` on `FakeRoverPlugin` in the yakrover-8004-mcp repo. The method should check if the task requires sensors the fakerover has (temperature, humidity), call `/info` and `/sensor/ht` to verify the simulator is online, and return a bid dict with the standard fields.

### FLAKY-1: `test_auto_accept_timer` relies on `asyncio.sleep(1.5)`

**File:** `auction/tests/test_engine.py:732`

This test sets `auto_accept_seconds=1`, then sleeps 1.5s. Under CI load, the event loop may not fire the callback within 1.5s. The test has already been made as tight as possible (1s timeout + 0.5s buffer), but this is inherently flaky.

**Suggested fix:** Use a manual event loop tick or `asyncio.Event` to synchronize instead of wall-clock sleep.

### FLAKY-2: `test_execute_timeout_abandons` uses `sla_seconds=1`

**File:** `auction/tests/test_engine.py:493`

The TimeoutRobot sleeps for 999999s, so the `asyncio.wait_for(timeout=1)` will always fire. But the 1-second timeout means the test takes at least 1 second. Under extreme CI load, even this could be flaky if the test runner's event loop is delayed.

### QUALITY-1: `test_bad_payload_rejected` -- asserts wrong thing

**File:** `auction/tests/test_engine.py:669`

```python
with pytest.raises(ValueError):
    engine.confirm_delivery(request_id)
```

This asserts *some* ValueError but doesn't check which validation failed. Due to BUG-2, the `None` temperature passes the plausibility check, and the error comes from a different path. The test gives false confidence.

**Suggested fix:** Assert the specific error message, e.g., `match="temperature.*plausible"` or `match="Payload verification failed"`.

### QUALITY-2: `test_wraps_discovered_robots` -- mocks the function under test

**File:** `auction/tests/test_discovery_bridge.py:284-305`

This test patches `discover_and_adapt` itself and then calls the mock. It does NOT test the actual `discover_and_adapt` function logic at all. It only tests that the mock returns what it was told to return.

**Suggested fix:** Patch `core.discovery.discover_robots` and `_instantiate_plugin` at the correct level, then call the real `discover_and_adapt`.

### QUALITY-3: `test_returns_empty_when_import_fails` -- fragile patching

**File:** `auction/tests/test_discovery_bridge.py:271-280`

The test patches `sys.modules` to simulate ImportError, but the import of `core.discovery` inside `discover_and_adapt` may already be cached. The test passes because `core.discovery` genuinely isn't importable in this environment, not because of the patch.

### QUALITY-4: Property-based tests skip silently if hypothesis is not installed

**File:** `auction/tests/test_core.py:425`

`pytest.importorskip("hypothesis")` causes the entire `TestPropertyBased` class to be skipped if hypothesis is not installed. This is correct behavior, but the 5 skips in the test output correspond to Ed25519 tests (eth_account not installed), not hypothesis. The hypothesis tests are actually running. This is not a bug, but the skip reason could confuse developers.

---

## Test Infrastructure Recommendations

### 1. Add `cancel_task` and `abandon_task` test coverage (HIGH PRIORITY)

These are recovery paths for stuck tasks with real money implications. They should have at least 8 tests between them.

### 2. Add MCP tool-level tests for all 15 tools

Currently only `test_new_mcp_tools_registered` verifies the tools exist. None of the tools are called through the MCP layer. At minimum, test:
- `auction_quick_hire` happy path + each failure mode
- `auction_fund_wallet` with and without Stripe
- `auction_cancel_task` through MCP layer
- Error response structure for each error type

### 3. Replace `asyncio.sleep` in auto-accept test

Use `asyncio.Event` or manually advance the event loop clock to avoid wall-clock dependencies.

### 4. Add wallet balance invariant assertion

After every test that runs a full lifecycle (post -> bid -> accept -> execute -> confirm), assert:
```python
assert buyer_initial - buyer_final == agreed_price
assert operator_final == agreed_price
```

### 5. Add a concurrent operations test harness

Use `threading` or `asyncio.gather` to test race conditions in wallet operations and state transitions.

### 6. Implement FakeRoverPlugin.bid()

Unblock the 4 failing fakerover tests by implementing `bid()` on the plugin class.

### 7. Add SyncTaskStore unit tests

Mirror the async `TaskStore` tests for the sync variant.

---

## Recommended v0.51 Fixes

**Priority 1 -- Bugs (fix before any demo with real money):**

1. **BUG-4:** Fix `accept_bid` balance check to use 25% reservation instead of full price (engine.py:671)
2. **BUG-5:** Move `_start_auto_accept_timer` call from `accept_bid` to `execute` (after DELIVERED transition)
3. **BUG-1:** Add WITHDRAWN to valid transitions from REJECTED, ABANDONED, PROVIDER_CANCELLED states
4. **BUG-2:** Add explicit None check for sensor values in `confirm_delivery`

**Priority 2 -- Critical coverage gaps (needed for production confidence):**

5. Add `cancel_task` tests (COVERAGE_GAP-1)
6. Add `abandon_task` tests (COVERAGE_GAP-2)
7. Add `auction_quick_hire` MCP tool tests (COVERAGE_GAP-6)
8. Fix `accept_bid` balance check test to verify the 25% logic (tests currently pass despite the bug because buyer has ample balance)

**Priority 3 -- Edge cases:**

9. Test re-pool exhaustion (EDGE_CASE-4)
10. Test exactly-$0.50 budget boundary (EDGE_CASE-2)
11. Test wallet balance consistency after reject -> re-pool -> accept -> settle cycle

**Priority 4 -- Test quality:**

12. Fix `test_bad_payload_rejected` to assert specific error (QUALITY-1)
13. Fix `test_wraps_discovered_robots` to test real function (QUALITY-2)
14. Replace sleep-based auto-accept test (FLAKY-1)
15. Implement `FakeRoverPlugin.bid()` to unblock 4 failing tests
