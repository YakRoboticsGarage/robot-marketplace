# Feedback: Reject Flow Dead End

**Date:** 2026-03-29
**Source:** Founder review of demo flow
**Severity:** UX dead end — blocks user from completing the flow

---

## The Problem

When a user clicks "Reject" on the award review screen and sends a decline:
1. The task card grays out with "Task X declined — notification sent"
2. But then... nothing. The user is stuck.
3. They can't proceed to "Sign & Activate" because not all tasks are confirmed
4. They can't select the next bidder
5. They can't restart the auction for that task
6. The only option is "Upload Another RFP" (full restart)

## What Should Happen

After rejecting a recommended winner, the user needs clear next steps:

**If there's a next bidder:**
- Show the next-ranked bidder's card (e.g., Meridian Geospatial at $89K)
- Same review format: compliance checks, profile, agree/reject
- User can keep rejecting down the ranked list

**If there's no next bidder (sole bidder rejected):**
- Options: re-post task with wider bid window, adjust scope/budget, skip this task
- "Skip this task" should allow proceeding with the other task(s) only

**If all tasks for an RFP are rejected:**
- Return to the RFP processing screen with option to re-post

## Research Needed

- How do DOTs handle when a low bidder is rejected?
- How do Upwork/Thumbtack handle rejection → next candidate?
- What's the right state machine for reject → next → accept?
