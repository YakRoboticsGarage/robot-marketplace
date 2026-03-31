# Tracking & Observability: Three Dashboard Surfaces

**Date:** 2026-03-31
**Status:** Requirements analysis, ready for design
**Context:** The marketplace has no real-time tracking beyond point queries. This doc specs three observability surfaces needed for production.

---

## The Problem

Today, a buyer posts a task and has no visibility until delivery. An operator wins a bid and has no central view of their work queue. We (admins) have no operational dashboard. The engine logs to stdout — nothing is queryable, alertable, or visualizable.

This is the equivalent of ordering food on UberEats and seeing a blank screen until the doorbell rings.

---

## Three Surfaces

```
+-------------------+    +---------------------+    +--------------------+
| BUYER DASHBOARD   |    | OPERATOR DASHBOARD  |    | ADMIN CONSOLE      |
| "Where's my       |    | "What's on my       |    | "How's the         |
|  survey?"          |    |  plate?"             |    |  platform?"         |
+-------------------+    +---------------------+    +--------------------+
        |                         |                          |
        +------------+------------+-----------+--------------+
                     |                        |
              [Event Stream]          [Metrics Aggregator]
                     |                        |
              [Auction Engine]         [SQLite / Store]
```

---

## Surface 1: Buyer/Agent Dashboard

**User:** GC estimator (Marco), AI agent orchestrating tasks
**Mental model:** UberEats order tracker — real-time status with visual progress

### What the buyer needs to see

#### Per-Task View
| Data Point | Source Today | Gap |
|------------|-------------|-----|
| Current state (posted, bidding, in progress...) | `auction_get_status` | None — exists |
| Time in current state | `posted_at` + clock | Missing: no per-state timestamps |
| SLA countdown | `sla_seconds` - elapsed | Exists in `auction_track_execution` |
| Bid count + top bid | `bid_count`, `winning_bid` | Exists |
| Operator identity + profile | `winning_bid.robot_id` → registry | Exists but requires separate query |
| Execution progress (%) | None | **Critical gap** — no milestones |
| Operator location | None | **Critical gap** — no GPS data |
| ETA to completion | None | **Gap** — no historical duration data |
| Deliverable preview | `delivery.data` | Only available after delivery |
| Payment status | `wallet_entries` | Exists but raw ledger format |

#### Multi-Task Project View (RFP-level)
| Data Point | Source Today | Gap |
|------------|-------------|-----|
| All tasks from this RFP | `auction_list_tasks(rfp_id=X)` | Exists |
| Per-task state summary | List of states | Exists but no aggregate view |
| Overall project progress | None | **Gap** — no rollup logic |
| Total spend vs budget | Wallet entries per request_id | Exists but needs aggregation |
| Dependency tracking | `task_decomposition.dependencies` | Exists in schema, not visualized |

#### Event Feed (Buyer)
What the buyer should see as a timeline:
```
10:14 AM  Task posted — "Topographic LiDAR survey, US-131"
10:16 AM  3 bids received — top bid: $38,500 (Apex Aerial Surveys)
10:18 AM  You awarded to Apex Aerial Surveys — $38,500
10:18 AM  25% escrow reserved ($9,625)
10:19 AM  Operator confirmed — mobilizing to site
11:45 AM  Operator on-site — flight planning
12:30 PM  Data capture in progress — 40% complete
 2:15 PM  Data capture complete — processing
 3:00 PM  Deliverables uploaded — pending your review
 3:00 PM  Auto-accept in 60 minutes if no action
 3:22 PM  You accepted delivery — payment released ($38,500)
```

**What exists today:** States and timestamps for posted_at, delivered_at. Everything in between is a black box.

---

## Surface 2: Operator Dashboard

**User:** Drone operator (Alex), robot fleet manager
**Mental model:** Uber driver app — task queue, active jobs, earnings

### What the operator needs to see

#### Task Discovery
| Data Point | Source Today | Gap |
|------------|-------------|-----|
| Available tasks matching my capabilities | Hard constraint filter in engine | Exists in engine, no operator-facing query |
| Task location + distance from me | `project_metadata.location` | Location exists, distance calculation missing |
| Budget range | `budget_ceiling` | Exists |
| Deadline urgency | `sla_seconds` | Exists |
| Required equipment/certs | `capability_requirements.hard` | Exists |
| Competition (bid count) | `bid_count` | Exists but not exposed to operators pre-bid |

#### Active Jobs
| Data Point | Source Today | Gap |
|------------|-------------|-----|
| My won tasks | `auction_list_tasks(robot_id=X)` | Exists |
| Current task status | Task state | Exists |
| Deadline countdown | SLA | Exists |
| Payment status | Wallet entries | Exists |
| Deliverable upload status | Delivery payload | Exists for completed, nothing for in-progress |

#### Progress Reporting (operator pushes updates)
| Data Point | Exists? | Notes |
|------------|---------|-------|
| Mark "en route to site" | No | New state or event needed |
| Mark "on site" | No | GPS could auto-detect |
| Upload progress % | No | New endpoint needed |
| Report delay/issue | No | No escalation mechanism |
| Upload partial deliverables | No | All-or-nothing delivery today |

#### Earnings & Performance
| Data Point | Source Today | Gap |
|------------|-------------|-----|
| Completed tasks | Reputation records | Exists |
| Total earnings | Wallet credit entries | Exists but needs aggregation |
| On-time rate | `reputation.on_time_rate` | Exists |
| Completion rate | `reputation.completion_rate` | Exists |
| Average bid win rate | None | **Gap** — no bid history per operator |
| Monthly/weekly earnings | Ledger entries with timestamps | Exists, needs aggregation |

#### Event Feed (Operator)
```
 9:00 AM  New task available — "Topo survey, Kalamazoo County" ($45,000, 14 days)
 9:05 AM  You placed bid — $38,500, 10-day delivery
10:18 AM  You won! — "Topo survey, Kalamazoo County"
10:18 AM  Escrow funded — $9,625 reserved by buyer
10:30 AM  → You marked: "Reviewing task specs"
11:00 AM  → You marked: "En route to site"
11:45 AM  → You marked: "On site — flight planning"
12:30 PM  → You uploaded: progress update (40%)
 3:00 PM  → You uploaded: deliverables (4 files)
 3:22 PM  Buyer accepted — $38,500 released to your wallet
```

---

## Surface 3: Admin Console

**User:** Us (platform operators)
**Mental model:** Stripe Dashboard / Cloudflare Analytics — operational health + business metrics

### Real-Time Operations
| Metric | Source Today | Gap |
|--------|-------------|-----|
| Active tasks by state | `auction_list_tasks` by state | Exists but no aggregate |
| Tasks posted today/week/month | `tasks.created_at` | Exists in SQLite, no rollup |
| Bids per task (avg) | Bid count per task | Exists, needs aggregation |
| Time from post to first bid | `posted_at` vs first bid timestamp | **Gap** — no bid timestamp in store |
| Time from post to award | `posted_at` vs `awarded_at` | `awarded_at` exists on TaskRecord but not persisted |
| Time from award to delivery | `awarded_at` vs `delivered_at` | Same gap |
| SLA violation rate | `reputation.on_time_rate` inverse | Exists |
| Re-pool rate | `bid_round > 1` count | Exists in TaskRecord |
| Withdrawal rate | Tasks in WITHDRAWN state | Exists |

### Financial
| Metric | Source Today | Gap |
|--------|-------------|-----|
| GMV (gross merchandise value) | Sum of winning bid prices | Needs aggregation over ledger |
| Platform revenue (12% commission) | None | **Gap** — commission not tracked separately |
| Escrow outstanding | Sum of `reservation_25` entries without matching `delivery_75` | Computable from ledger |
| Refund volume | Sum of `refund` entries | Computable from ledger |
| Average task value | Mean of winning bid prices | Needs aggregation |
| Operator payout volume | Sum of `credit` entries | Computable from ledger |

### Operator Health
| Metric | Source Today | Gap |
|--------|-------------|-----|
| Registered operators | `operator_registry.list_operators()` | Exists |
| Active (with tasks) vs idle | None | **Gap** — no active task count per operator |
| Compliance status | `compliance.verify_operator()` | Exists per operator, no aggregate |
| Operators with expiring certs | `compliance_record.expires_at` | Exists but no alert/query |
| Top operators by volume | None | **Gap** — needs reputation + ledger join |
| Operator churn | None | **Gap** — no deactivation tracking |

### Platform Health
| Metric | Source Today | Gap |
|--------|-------------|-----|
| API request volume | None | **Gap** — no request logging |
| MCP tool invocation counts | None | **Gap** — no tool telemetry |
| Error rates by tool | `_error_response` calls | Logged to stdout only |
| Worker rate limit hits | KV counters in Cloudflare | Exists in KV, not queryable |
| Tunnel/MCP server uptime | `/health` endpoint | Exists, no monitoring |

### Dispute & Escalation
| Metric | Source Today | Gap |
|--------|-------------|-----|
| Rejected deliveries | Tasks in REJECTED state | Exists |
| Rejection reasons | None | **Gap** — reason string in `reject_delivery` not persisted |
| Dispute resolution time | None | **Gap** — no dispute workflow |
| Escalation queue | None | **Gap** — no escalation mechanism |

---

## What Exists Today vs What's Needed

### Data Infrastructure Score Card

| Capability | Score | Notes |
|------------|-------|-------|
| Task lifecycle states | 9/10 | Comprehensive state machine, missing only per-state timestamps |
| Financial audit trail | 8/10 | Full ledger with timestamps. Missing: commission tracking, aggregate views |
| Operator profiles | 7/10 | Good registration + compliance. Missing: capacity, workload, bid history |
| Reputation tracking | 7/10 | Rolling 30-day window. Missing: category-specific, trend data |
| Execution visibility | 2/10 | Only "in_progress" → "delivered". No progress, location, milestones |
| Event streaming | 1/10 | Console logs only. No structured events, no pub/sub, no queryable log |
| Aggregation/analytics | 1/10 | Raw data exists but no rollup queries, no time-series, no dashboards |

### The Critical Gap: Event Log

Every surface needs a queryable event stream. Today, `log()` prints to stdout and disappears. The single highest-leverage change is:

**An `events` table that captures every meaningful state change with timestamp, actor, and context.**

---

## Proposed: Event Log Schema

```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,      -- 'task.posted', 'bid.received', 'task.awarded', etc.
    request_id TEXT,               -- task context (nullable for system events)
    actor_id TEXT,                 -- who caused this: buyer wallet_id, robot_id, 'system'
    actor_role TEXT,               -- 'buyer', 'operator', 'system', 'admin'
    data_json TEXT DEFAULT '{}',   -- event-specific payload
    timestamp TEXT NOT NULL,       -- ISO 8601
    INDEX idx_events_request (request_id),
    INDEX idx_events_type (event_type),
    INDEX idx_events_actor (actor_id),
    INDEX idx_events_ts (timestamp)
);
```

### Event Types

#### Task Lifecycle
| Event Type | Emitted When | Data Payload |
|------------|-------------|--------------|
| `task.posted` | Task enters POSTED state | `{task_category, budget_ceiling, sla_seconds, rfp_id}` |
| `task.bidding_opened` | Eligible robots notified | `{eligible_count, filter_reasons_summary}` |
| `task.bid_received` | Operator submits bid | `{robot_id, price, sla_commitment}` |
| `task.awarded` | Buyer accepts bid | `{robot_id, price, buyer_notes}` |
| `task.execution_started` | Operator begins work | `{robot_id}` |
| `task.progress_update` | Operator reports progress | `{percent_complete, status_text, location}` |
| `task.delivered` | Operator uploads deliverables | `{robot_id, sla_met, file_count}` |
| `task.accepted` | Buyer confirms delivery | `{robot_id}` |
| `task.rejected` | Buyer rejects delivery | `{robot_id, reason}` |
| `task.settled` | Payment finalized | `{amount, settlement_mode}` |
| `task.withdrawn` | No eligible bidders | `{reason}` |
| `task.re_pooled` | Re-opened after rejection | `{bid_round, excluded_robots}` |
| `task.expired` | SLA timeout | `{elapsed_seconds}` |

#### Payment
| Event Type | Emitted When | Data Payload |
|------------|-------------|--------------|
| `payment.escrow_reserved` | 25% debited from buyer | `{amount, wallet_id}` |
| `payment.delivery_charged` | 75% debited from buyer | `{amount, wallet_id}` |
| `payment.operator_paid` | Credited to operator | `{amount, wallet_id, stripe_transfer_id}` |
| `payment.refund_issued` | Refund on rejection/timeout | `{amount, wallet_id, reason}` |
| `wallet.funded` | Buyer tops up wallet | `{amount, wallet_id, payment_method}` |

#### Operator
| Event Type | Emitted When | Data Payload |
|------------|-------------|--------------|
| `operator.registered` | New operator signs up | `{company_name, location, equipment_count}` |
| `operator.activated` | Compliance verified | `{operator_id}` |
| `operator.suspended` | Compliance lapsed | `{operator_id, reason}` |
| `operator.compliance_expiring` | Cert expires within 30 days | `{doc_type, expires_at}` |
| `operator.heartbeat` | Periodic status ping | `{status, location, battery_pct, active_tasks}` |

#### System
| Event Type | Emitted When | Data Payload |
|------------|-------------|--------------|
| `system.auto_accept` | Timer fires | `{request_id, elapsed_seconds}` |
| `system.sla_warning` | 80% of SLA elapsed | `{request_id, remaining_seconds}` |
| `system.rate_limit_hit` | IP exceeds limit | `{ip_hash, endpoint, limit}` |

---

## Proposed: Execution Progress Model

The biggest UX gap is between "in_progress" and "delivered." For the UberEats experience, operators need to push progress updates.

### Progress States (operator-reported)

```
AWARDED
  → MOBILIZING       — "Reviewing specs, planning flight"
  → EN_ROUTE         — "Traveling to site"
  → ON_SITE          — "Arrived, setting up equipment"
  → CAPTURING        — "Data capture in progress" (with % if available)
  → PROCESSING       — "Post-processing data"
  → UPLOADING        — "Preparing deliverables"
DELIVERED
```

These are **soft states** — operator-reported via a new MCP tool, not engine-enforced. The engine state machine stays unchanged (BID_ACCEPTED → IN_PROGRESS → DELIVERED). Progress states live in the event stream.

### New MCP Tool

```
auction_update_progress(
    request_id: str,
    progress_state: str,    -- "mobilizing" | "en_route" | "on_site" | "capturing" | "processing" | "uploading"
    percent_complete: int,  -- 0-100 (optional)
    status_text: str,       -- free-text update (optional)
    location: dict,         -- {lat, lng} (optional)
)
```

### New MCP Tool: Task Feed

```
auction_get_task_feed(
    request_id: str,        -- events for one task
    -- OR --
    actor_id: str,          -- events for one buyer/operator
    since: str,             -- ISO timestamp (pagination)
    limit: int,             -- max events (default 50)
) → {events: [...], has_more: bool}
```

---

## Proposed: Dashboard Queries

These are the aggregation queries each surface needs, built on the event log + existing tables.

### Buyer Dashboard Queries

| Query | SQL/Logic | Frequency |
|-------|-----------|-----------|
| My active tasks | `SELECT * FROM tasks WHERE state NOT IN ('settled','withdrawn','expired') AND wallet_id = ?` | On load |
| Task timeline | `SELECT * FROM events WHERE request_id = ? ORDER BY timestamp` | Per task, real-time |
| Project rollup | `SELECT state, COUNT(*) FROM tasks WHERE rfp_id = ? GROUP BY state` | On load |
| Spend summary | `SELECT SUM(amount) FROM ledger_entries WHERE wallet_id = ? AND entry_type IN ('reservation_25','delivery_75')` | On load |

### Operator Dashboard Queries

| Query | SQL/Logic | Frequency |
|-------|-----------|-----------|
| Available tasks for me | Hard constraint filter + `state = 'BIDDING'` | Polling (30s) |
| My active jobs | `SELECT * FROM tasks WHERE winning_bid_json LIKE '%robot_id%' AND state IN ('bid_accepted','in_progress','delivered')` | On load |
| My earnings (period) | `SELECT SUM(amount) FROM ledger_entries WHERE wallet_id = ? AND entry_type = 'credit' AND timestamp >= ?` | On load |
| My bid history | `SELECT * FROM bids WHERE robot_id = ? ORDER BY created_at DESC` | On load |
| My compliance status | `compliance.verify_operator(robot_id)` | On load |

### Admin Console Queries

| Query | SQL/Logic | Frequency |
|-------|-----------|-----------|
| Tasks by state | `SELECT state, COUNT(*) FROM tasks GROUP BY state` | Polling (60s) |
| GMV (period) | `SELECT SUM(amount) FROM ledger_entries WHERE entry_type = 'credit' AND timestamp >= ?` | On load |
| Time to award (avg) | `SELECT AVG(julianday(awarded_ts) - julianday(posted_ts)) FROM ...` | Needs event log |
| SLA violation rate | `SELECT COUNT(*) FILTER (WHERE sla_met = 0) / COUNT(*) FROM reputation_records` | On load |
| Operator leaderboard | `SELECT robot_id, COUNT(*), AVG(completion_rate) FROM reputation GROUP BY robot_id` | On load |
| Expiring compliance | `SELECT * FROM compliance WHERE expires_at < datetime('now', '+30 days')` | Daily |
| Revenue (period) | Needs commission tracking added to settlement | Not yet possible |

---

## Implementation Phases

### Phase 1: Event Infrastructure (foundation for all three surfaces)
- Add `events` table to `store.py`
- Add `emit_event()` method to `AuctionEngine`
- Wire all state transitions to emit events
- Wire wallet operations to emit events
- Add `auction_get_task_feed` MCP tool
- **Effort:** 2-3 days
- **Unlocks:** Task timeline for buyer, event feed for operator, basic admin metrics

### Phase 2: Execution Progress
- Add `auction_update_progress` MCP tool
- Add progress states (mobilizing → en_route → on_site → capturing → processing → uploading)
- Emit `task.progress_update` events from operator
- Add progress % and status text to `auction_track_execution` response
- **Effort:** 1-2 days
- **Unlocks:** UberEats-style tracking for buyer, progress reporting for operator

### Phase 3: Buyer Dashboard
- Aggregate queries: project rollup, spend summary, SLA countdown
- Task timeline component (event feed → visual timeline)
- Multi-task project view (RFP grouping)
- Delivery preview/download
- **Effort:** 3-4 days (includes frontend if building UI)
- **Unlocks:** "Where's my survey?" experience

### Phase 4: Operator Dashboard
- Task discovery query (available tasks matching my capabilities)
- Active jobs view with deadline countdown
- Earnings aggregation (weekly/monthly)
- Bid history and win rate
- Compliance status + renewal alerts
- **Effort:** 3-4 days
- **Unlocks:** "What's on my plate?" experience

### Phase 5: Admin Console
- Platform metrics aggregation (GMV, task volume, SLA rates)
- Operator health overview (compliance, capacity, performance)
- Financial summary (escrow outstanding, refunds, revenue proxy)
- Dispute/rejection queue
- Expiring compliance alerts
- **Effort:** 2-3 days
- **Unlocks:** "How's the platform?" experience

---

## What Already Works (No Changes Needed)

These data points are already available via existing MCP tools and just need frontend/dashboard wiring:

- Task state and lifecycle (`auction_get_status`)
- SLA countdown (`auction_track_execution`)
- Bid count and winning bid details
- Full wallet ledger with timestamps (`auction_get_wallet_balance` + entries)
- Operator compliance checklist (`auction_verify_operator_compliance`)
- Operator profile and equipment (`auction_get_operator_status`)
- Reputation metrics (completion rate, on-time, rejection)
- Task filtering by state, rfp_id, robot_id, category (`auction_list_tasks`)
- Multi-task project linking via `task_decomposition.rfp_id`

**Bottom line:** ~60% of the data for all three dashboards already exists in the engine. The critical missing piece is the event log (Phase 1) and execution progress (Phase 2). Everything else is aggregation and presentation.
