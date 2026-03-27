# Founder Feedback — Demo v4

**Date:** 2026-03-27
**Source:** Direct founder input
**Status:** Pending implementation

---

## Changes Requested

### 1. Agent Link Flow
- Change "Works with Claude, GPT, and any MCP-compatible AI agent." to "Or click here to link your Agent"
- Clicking should go to an agent link/onboarding flow
- **Needs assessment:** What does this user journey look like? (connect MCP, configure auth, test connection)

### 2. Live Activity → Full Page Feed
- Make the "Live Activity" section clickable into a full-page feed view
- Individual activity items should be clickable to see additional details (task spec, robot used, cost breakdown, timestamp, duration)

### 3. Robot Type Icons
- Add icons to robot cards identifying type: rover, drone, sensor, builder, humanoid, arm, etc.
- Use current robot taxonomy from the codebase

### 4. Robot Profile Pages
- Make robots clickable into a full profile page (not just the inline detail panel)
- Dedicated screen with all specs, certs, reviews, task history

### 5. Robot Grid Layout Change
- Show only 5 robots: line of 3, then 2 + empty "List" CTA box
- "Show more robots" button renamed to "Explore Robots"
- "Explore Robots" navigates to a dedicated robot explorer page/screen

### 6. Operator CTA Copy
- Change "start earning per task" to just "start earning"

### 7. Feed Item Formatting
- Add an icon for robot type (rover/drone/sensor/etc.) in each feed item
- Robot name should be in distinct formatting (different color or weight) for readability

### 8. Remove Subtitle
- Remove "Sensor readings, inspections, and surveys from $0.25." from the hero
- The cycling examples under the search bar already communicate this

---

## Implementation Notes

- Items 2, 4, 5 require new screens (full feed, robot profile, robot explorer)
- Item 1 requires a new user journey assessment (agent linking flow)
- Items 3, 6, 7, 8 are simple CSS/HTML changes
