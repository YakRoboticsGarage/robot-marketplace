# Reject Recovery: From Declined Bid to Resolution

Research date: 2026-03-29. This document addresses the dead-end UX identified in `FEEDBACK_REJECT_DEAD_END.md` -- what happens after a user clicks "Reject" on a recommended winner, and how the system should recover.

---

## How DOTs Handle Rejection

When a state DOT rejects the apparent low bidder, the standard procedure is **award to the next lowest responsive and responsible bidder** -- not an automatic re-bid. Re-advertising is a last resort.

- **FHWA guidance**: The contracting agency may reject the low bid and award to the second-lowest bidder, provided that bidder is also responsive and responsible. The agency must document the rejection reason. Re-advertising is required only when all bids are rejected or the remaining bids exceed the engineer's estimate by an unacceptable margin.
- **TxDOT**: If the low bidder is found non-responsible (e.g., insufficient bonding, failed prequalification), TxDOT moves to bidder #2 and runs the same responsive/responsible checks. The process adds roughly 7-14 days per rejected bidder. TxDOT reserves the right to reject all bids and re-let the project at a future monthly letting.
- **MDOT**: The Contract Awards Unit reviews in order of bid rank. If the low bidder is rejected, the next bidder's responsibility is evaluated. MDOT's timeline is 14-30 days for straightforward awards; each rejection adds another review cycle. MDOT will reject all bids and re-advertise if the remaining bids are more than 10% over the engineer's estimate.
- **Key pattern**: DOTs walk down the ranked list sequentially. They do not skip to bidder #3 while #2 is under review. The process is linear, not parallel.

**Takeaway for the marketplace**: Walking the ranked list is the correct default. Re-posting is the fallback when the list is exhausted or all remaining bids are unacceptable.

---

## Marketplace Platform Patterns

### Upwork: Decline + Continue Reviewing
When a client clicks "Decline" on a proposal, the freelancer receives a generic notification ("The client has chosen to move forward with other candidates"). The client's proposal list remains intact -- they can review and hire any remaining candidate at any time. No automatic next-candidate promotion. The client stays in control.

### Thumbtack: Dismiss + Browse
Dismissing a pro's quote removes it from the active list. The customer continues browsing remaining quotes. If all quotes are dismissed, Thumbtack prompts: "Want to update your request to get more quotes?" This is the re-post equivalent.

### BuildingConnected: Reject Bid + Bid Leveling
The GC can mark a sub's bid as "not awarded" with an optional reason. The bid leveling view updates to show remaining candidates. The GC selects the next preferred sub. Rejected subs receive a notification. The platform does not auto-promote the next bidder -- the GC re-evaluates the leveling sheet.

### Uber/Lyft: Automatic Re-Match
When a driver cancels, the rider is automatically re-matched to the next available driver with no user action required. This works because rides are commodity services with interchangeable providers. Construction tasks are not commodities -- the GC needs to review each candidate. **Auto-match is the wrong model for this marketplace.**

### Pattern Summary
Every platform except ride-sharing preserves human selection after rejection. The correct UX is: reject current, surface the next candidate for review, let the human decide.

---

## State Machine Design

### New States Needed

The existing `TaskState` enum has `REJECTED` and `RE_POOLED` defined but unreachable. The reject-recovery flow needs these transitions added to `VALID_TRANSITIONS` in `engine.py`:

```
BID_ACCEPTED -----> AWARD_REVIEW (new: GC reviewing recommended winner)
AWARD_REVIEW -----> IN_PROGRESS  (GC confirms -- existing flow continues)
AWARD_REVIEW -----> WINNER_REJECTED (new: GC declines this bidder)
WINNER_REJECTED --> AWARD_REVIEW (next bidder promoted for review)
WINNER_REJECTED --> RE_POOLED    (no more bidders -- task goes back to market)
WINNER_REJECTED --> SKIPPED      (new: GC skips this task, proceeds with others)
RE_POOLED --------> BIDDING      (new auction round opens)
```

### How Many Rounds Before Re-Post?

- DOTs walk the entire ranked list (typically 3-8 bidders).
- For the marketplace, allow rejection of **all ranked bidders** before forcing a decision. After the last bidder is rejected, present three options: re-post, skip, or withdraw.
- Practical limit: if a task has been rejected 3+ times, the system should surface a warning: "Multiple rejections may indicate a scope or budget issue. Consider revising the task spec before re-posting."

### Should Rejected Bidders Be Notified?

Yes. Every platform studied notifies rejected candidates. The notification should include:
- That their bid was not selected (not the specific reason -- mirrors DOT practice where rejection reasons are documented internally but not always shared with the bidder).
- That they are free to bid on other tasks.
- Timeline: notification sent within 1 hour of rejection action.

---

## Partial Award Scenarios

### Multi-Task RFP: Award Some, Skip Others

This is the scenario from the feedback: the user rejects Task 2's winner but wants to proceed with Task 1.

- **DOT precedent**: DOTs can and do make partial awards on multi-line contracts. FHWA allows awarding individual line items when the solicitation permits it. Many state DOTs structure lettings so each project is a separate contract, but within a project, partial award of bid items is possible when specified.
- **Marketplace approach**: Each task in a multi-task RFP should be independently awardable. Rejecting Task 2's winner should not block Task 1's confirmation. The "Sign & Activate" button should work for confirmed tasks only, with skipped/pending tasks tracked separately.

### Valid Outcomes for a Multi-Task RFP

1. **All tasks confirmed** -- proceed to Sign & Activate for all.
2. **Some confirmed, some in review** -- Sign & Activate available tasks; others continue their reject-recovery flow independently.
3. **Some confirmed, some skipped** -- Sign & Activate confirmed tasks; skipped tasks can be re-posted later or abandoned.
4. **All rejected** -- return to RFP dashboard. Offer: revise and re-post, or withdraw.

---

## Recommended Flow for Demo

### After User Clicks "Reject" on a Task Winner

**Screen 1 -- Rejection Reason** (modal overlay):
- Radio buttons: "Insufficient qualifications," "Prior experience concern," "Price too high," "DBE non-compliance," "Conflict of interest," "Other (specify)."
- Required selection. "Other" shows a text field.
- Button: "Confirm Rejection."

**Screen 2 -- Next Bidder Card** (replaces the rejected bidder's card):
- If another bidder exists: show their card in the same format (compliance checks, profile, price, score). Header: "Next Ranked Bidder (2 of 3)."
- Same actions: "Confirm Award" / "Reject."
- If no more bidders: show Screen 3.

**Screen 3 -- No More Bidders** (replaces the task card):
- Message: "All bidders for [Task Name] have been reviewed."
- Three buttons: "Re-Post Task" (opens new auction), "Skip This Task" (proceed without it), "Revise Scope" (edit task spec and re-post).

### Multi-Task Proceed Logic
- The "Sign & Activate" button enables when **at least one task** is confirmed and **no tasks are in AWARD_REVIEW state** (all must be resolved: confirmed, skipped, or re-posted).
- Confirmed tasks show green check. Skipped tasks show gray "Skipped" badge. Re-posted tasks show orange "Re-Bidding" badge.

---

## Specific Screen Updates Needed

1. **Award Review Screen**: Add `AWARD_REVIEW` as a visible state. Current flow jumps from auction close to confirmed -- insert the review step.
2. **Task Card Component**: Support four visual states: Reviewing (blue), Confirmed (green), Rejected/Next (amber, with bidder counter "2 of 3"), Skipped (gray).
3. **Rejection Modal**: New component. Reason selector + confirm button. Reason is stored in the audit trail but not sent to the bidder.
4. **Next Bidder Transition**: Animate the card swap -- slide out rejected, slide in next bidder. Preserves spatial context so the user knows they are still on the same task.
5. **Sign & Activate Gate**: Change the enable condition from "all tasks confirmed" to "all tasks resolved (confirmed or skipped) and at least one confirmed."
6. **Engine State Transitions**: Add `AWARD_REVIEW`, `WINNER_REJECTED`, and `SKIPPED` to `TaskState` enum in `core.py`. Add corresponding transitions to `VALID_TRANSITIONS` in `engine.py`.
7. **Notification Stub**: On rejection, log a notification event (bidder_id, task_id, rejection_reason, timestamp). Actual delivery is a future feature, but the data model should capture it now.
