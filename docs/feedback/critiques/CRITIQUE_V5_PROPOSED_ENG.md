# Engineering Critique — V5 Proposed Changes

**Date:** 2026-03-27
**Scope:** Implementation feasibility for FEEDBACK_V4_FOUNDER items

---

## 1. Screen proliferation (feed, robot profile, explorer, agent link = 4 new screens)

The demo already uses a `showScreen(id, step)` pattern with 7 `div.screen` blocks. Adding 4 more is fine structurally but the single file is at ~860 lines. Recommendation: keep it in one file but extract each new screen into its own `<template>` element and hydrate on first navigation (lazy init). This avoids a premature multi-file split while keeping the HTML readable. No router needed -- the existing hash-less approach works since this is a demo, not a production SPA.

## 2. Robot type icons

Inline SVG is the cleanest option. The taxonomy is small and fixed (rover, drone, sensor, builder, humanoid, arm -- 6 types). A lookup object mapping type to a 16x16 SVG path string keeps it self-contained with zero external deps. Emoji (e.g. unicode robot faces) renders inconsistently across OS and looks unserious. Unicode symbols lack the right glyphs for "rover" vs "arm." Recommend 6 handwritten SVG icons in a single `<defs>` block at the top of the file, referenced via `<use>`.

## 3. Feed item detail view

Inline expand, not navigation. The feed is a live-updating list on the landing screen. Navigating away breaks context. Pattern: clicking a feed item expands a detail row beneath it (task spec, robot used, cost breakdown, duration) with a slide-down animation. This mirrors the existing robot detail panel approach. The "full feed page" (item 2) is the only place that should be a separate screen.

## 4. Robot grid 3+2+CTA layout

CSS grid with named areas is the direct approach:
```css
.robot-grid-top {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
.robot-grid-bottom {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
```
Row 1: 3 cards. Row 2: 2 cards + CTA in third slot. Two separate grid rows is simpler than a single 6-cell grid with `grid-column` tricks. The CTA box gets the same card dimensions automatically.

## 5. Performance — 1,047 robots on explorer page

The current code pre-generates all 1,047 cards as HTML strings at load time (`allRobotCards` array). This is already in memory. For the explorer page, pagination is sufficient -- show 24 at a time, append on "load more." Virtualization (intersection observer, recycled DOM) is overkill for 1K items with no images. The real cost is DOM nodes, and paginating at 24 keeps it under 200 nodes even after several clicks. If filtering/search is added later, filter the array and re-render the visible slice.

## 6. Agent link flow

Fully mockable in HTML/JS. Three-step flow: (1) choose agent (Claude/GPT/custom), (2) display MCP config JSON, (3) "copy to clipboard" button. The existing `copyModalContent()` function and modal pattern already support this. No backend needed -- the MCP config is a static JSON blob with a placeholder API key. Use `navigator.clipboard.writeText()` for copy (already available in the modal pattern). The agent link screen replaces the current "Works with Claude, GPT..." text with a clickable CTA.

## 7. Quick wins (items 6, 7, 8)

These are all sub-5-minute changes:
- **Item 6:** One string replacement in the operator CTA strip ("start earning per task" -> "start earning").
- **Item 7:** Add a type icon span before robot name in `renderFeed()`, bold the robot name with `<strong>` or a CSS class.
- **Item 8:** Delete the second sentence from `.hero .subtitle`. The cycling examples already do this job.

## Implementation order

Ship items 6, 7, 8 immediately (trivial). Then item 5 grid layout + item 3 icon set (small, visual wins). Then the three new screens in order: explorer (reuses existing grid code), feed page (reuses existing feed code), robot profile (extends existing detail template). Agent link flow last -- it needs the most UX thought despite being technically simple.
