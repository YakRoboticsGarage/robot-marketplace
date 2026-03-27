# UX Critique -- Proposed v5 Changes

**Date:** 2026-03-27
**Reviewer:** UX design review
**Source:** FEEDBACK_V4_FOUNDER.md

---

## Per-Change Assessment

**1. Agent Link CTA ("click here to link your Agent")**
Improves clarity over the passive "Works with Claude, GPT..." line. Risk: "click here" is weak copy -- use "Link your AI agent" as a verb-led CTA instead. Placing this on the landing page is premature; first-time visitors do not yet understand what the marketplace does. Move this CTA to the result screen (after first successful task) where intent is proven, and keep a subtler text link on the landing page for power users.

**2. Live Activity as full-page feed**
Good upgrade. The current feed is decorative -- making it interactive adds credibility. Per-item detail should show: robot name, task type, location, cost, and duration. Skip raw task specs and auction scores in the feed view; those belong on a dedicated task detail page, not inline. Risk: if the feed page loads slowly or feels empty (few real tasks), it undermines trust more than the current truncated list does.

**3. Robot type icons on cards**
Low-risk, high-value. Helps scanability. Ensure icons are paired with a text label (e.g., "Rover") for accessibility -- icon-only fails for unfamiliar robot types like "arm" vs "builder."

**4. Full robot profile pages**
Good. The current inline detail panel is cramped and loses grid context. A dedicated page allows richer content (task history chart, photo, operator info). Risk: adds a navigation layer -- provide a clear back button and preserve the user's scroll position in the grid.

**5. Robot grid: 3+2 layout with "Explore Robots" page**
The 3+2 grid with an empty "List" CTA box is smart -- it tightens the landing page and funnels operators. The dedicated explorer page is necessary. Risk: showing only 5 robots may feel like a small marketplace. Mitigate by showing the "312 online / 1,047 registered" count prominently near the grid.

**6. Operator CTA: "start earning" (drop "per task")**
Fine. Minor copy polish, no risk.

**7. Feed item formatting (type icon + bold robot name)**
Good for scanability. Ensure the robot name styling does not compete with the task description -- the task should remain the primary read.

**8. Remove hero subtitle**
Agree. The cycling examples already communicate scope. Removing the subtitle tightens the hero without losing information.

## Conflicts

Changes 2 (full feed page) and 7 (feed item formatting) should be designed together -- the feed item format must work at both the landing-page preview size and the full-page layout. Define one feed item component, not two.

Changes 4 (robot profile page) and 5 (explorer page) both introduce new screens. The explorer needs its own filter/search, and robot profiles need a way to return to either the explorer or the landing page. Plan the navigation hierarchy before building.

## Robot Explorer: Filtering/Search Recommendations

Primary filters (visible, always): type (rover/drone/sensor/arm/humanoid), location (map or text), online status.
Secondary filters (collapsed): price range, capability tags, rating threshold.
Search bar: free-text matching against robot name, location, and capabilities.
Sort options: price (low-high), rating, distance, tasks completed.
Avoid: filter combinations that yield zero results without explanation.

## Full-Page Feed: Signal vs Noise

Useful per item: task type, robot name + type icon, location, cost, time ago, status (completed/in-progress).
Noise to omit from the feed list: full task spec JSON, auction scoring breakdown, sensor raw data. These belong behind a "view details" tap.
Add a filter by status (completed / in-progress / failed) and by robot type.

## Agent Link Flow: Placement

The landing page is the wrong primary location. A first-time visitor needs to understand the value proposition before committing to an integration flow. Place the primary CTA on the result screen ("Automate this with your AI agent") where the user has just experienced a successful task. Keep a secondary, low-prominence link on the landing page for returning users who already know the product.
