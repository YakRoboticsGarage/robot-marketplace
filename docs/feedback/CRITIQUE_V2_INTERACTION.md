# Interaction Critique — v2 Demo

## 1. Robot cards are dead ends

Cards have `cursor:default` and no click handler. They tease info but deliver nothing.

**Fix:** Make cards clickable (`cursor:pointer`). Open a slide-up panel or detail screen showing:
- Full sensor specs (accuracy, calibration date, firmware version)
- Certifications (IP rating, safety compliance)
- Task history / completion rate
- Reviews with timestamps, not just star count
- Current location on a mini-map
- "Hire this robot" shortcut that pre-fills the search

## 2. Agent-compatibility is hidden behind "Connect Claude" on screen 2

Users don't learn the system is MCP-compatible until mid-flow. The `/.well-known/mcp.json` link is invisible.

**Fix:** Add a small badge on the landing hero: "Works with Claude, ChatGPT, and any MCP client". Put the MCP endpoint URL in the footer visibly (it's there but styled as a dead link). On robot cards, show an "MCP-ready" chip next to capabilities.

## 3. Blue-to-orange color swap — watch these spots

Swapping `--accent:#2563eb` to `#e67e22` is straightforward in `:root`, but:
- **Score bars and winner highlight** (`bid-card.winner` border, `.score-fill`) use hard-coded `rgba(37,99,235,0.1)`. Replace with `rgba(230,126,34,0.12)`.
- **Search focus ring** (`.search-input:focus`) uses `--border-focus:#3b82f6` and a blue `rgba` shadow. Both need updating.
- **Capability chips** (`.cap`) use `--accent-light`/`--accent` — orange-on-light-orange may look washed. Test contrast; may need `#d35400` for text on a `#fef5ee` background.
- **Step indicator** (`.step.active`) — white text on orange is fine, but verify WCAG AA at small font size.
- **"How it works" numbers** (`.how-num`) — same contrast concern.
- Links in footer and operator screen use `color:var(--accent)` — orange links look non-standard. Consider keeping links blue and only branding buttons/badges orange.

## 4. Missing states

- **No-match / empty result:** Typing "underwater welding" goes straight to the review screen with the same hardcoded Bay 3 task preview. Need a "No robots available for this task" state with suggestions.
- **Empty search:** Clicking the arrow with no input silently does nothing. Show a shake animation or inline hint.
- **Network/error:** No error UI anywhere. Add a generic error banner component for failed auctions, payment failures, and timeout.
- **Auction with no bids:** Not handled. Need a "No bids received — try expanding location or budget" state.

## 5. Landing-to-result friction

The 4-step flow (Search > Review > Pay > Result) forces payment before every first task. That's a wall.

**Fix:** Let users see the auction run before paying. Move payment to after auction-won, before execution. "Grey Subtlety won at $0.35 — pay to get your result." This builds trust and reduces the $25 pre-commitment barrier.

## 6. "Register a Robot" CTA

The dashed-border card in the grid is subtle — easy to miss. Clicking it jumps to the operator screen with no transition, and the step indicator breaks (no step highlighted).

**Fix:** Hide the step indicator on the operator screen. Make the CTA copy action-oriented: "List your robot — start earning" instead of just "Register a Robot". Add expected revenue ("Operators earn $X/month avg") to reduce ambiguity about what registration means.

## 7. Robot card interaction model

Current: hover lifts the card, click does nothing. This violates the affordance the hover creates.

**Fix:** Use a two-tier model:
- **Click** opens the detail panel (see item 1).
- **Quick-action button** ("Hire") visible on hover, triggers search pre-filled with that robot's capabilities.
- Add `cursor:pointer` and `role="button"` / `tabindex="0"` for keyboard access.
- On mobile (no hover), show the hire button persistently and make the full card tappable.
