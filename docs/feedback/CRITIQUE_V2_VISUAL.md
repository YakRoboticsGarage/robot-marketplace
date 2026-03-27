# Visual Design Critique v2 — Orange Accent Swap

## 1. Orange Accent Mapping (blue -> #e67e22)

There are 19 touchpoints using `--accent` / `--accent-light` / `--accent-hover`. Direct swap works for most, but two collisions:

- **Amber warning (`--amber: #d97706`) vs orange accent (`#e67e22`):** These are 1.5 hue steps apart. At small sizes (capability tags next to `$0.80 amber` prices, bid confidence next to score bars) they will read as the same color. **Fix:** Shift warnings to `#b45309` (darker amber/brown) or switch to a red-tinted warning like `#c2410c`.
- **Feed dot `.fdot.bid`** uses `--accent`. With orange accent, a bid dot sits next to green done dots and amber online dots — three warm tones in a 6px circle. **Fix:** Keep bid dots orange but make online dots neutral gray (`--text-3`), reserving warm colors for actionable states only.

## 2. Card Design

- **Robot cards:** Clean structure. The hover lift (`translateY(-2px)`) is tasteful. One issue: the `robot-avatar` boxes (36x36, bg-subtle, initials) look placeholder-grade. Replace with a subtle brand-tinted background (`--accent-light` at 40% opacity) or use a small robot icon.
- **Bid cards:** The `.winner` border uses a hardcoded `rgba(37,99,235,0.1)` blue glow — **must update** to orange-derived value when swapping. Same for `.search-input:focus` box-shadow.
- **Result meta boxes:** Functional but flat. Add a `border: 1px solid var(--border)` to give them definition against `--bg-subtle` background. Currently they float without edges.

## 3. Spacing and Rhythm

- **Hero to search:** 60px top padding on `.hero` is generous, then 28px to search, then 16px to cycling text. Good.
- **How-section to feed:** Both use `24px` vertical padding with only a `1px` border between. The feed section starts immediately — feels slightly cramped. **Fix:** Add `margin-top: 8px` to `.feed-section`.
- **Screen 2 (Review):** Uses inline `padding: 32px 0` on a wrapper div, but child elements have inconsistent bottom margins (20px, then 0). The spec-card gets `margin: 20px 0` but the CTA block above it gets `margin: 20px 0` as well, creating a 40px visual gap that reads as two separate sections. **Fix:** Reduce spec-card top margin to `12px`.
- **Step indicator:** `padding: 16px 0` is tight — only 4px gap between pills. Reads fine on desktop but will compress on mobile. OK for now.

## 4. Typography Scale

The scale is: 2.4rem -> 1.1rem -> 1rem -> 0.95rem -> 0.9rem -> 0.88rem -> 0.85rem -> 0.82rem -> 0.8rem -> 0.78rem -> 0.75rem -> 0.72rem -> 0.7rem -> 0.68rem -> 0.65rem.

That is 14 distinct sizes. Too many below 1rem — the difference between 0.78rem and 0.82rem (0.64px) is invisible. **Fix:** Collapse to 5-6 body sizes: `0.95, 0.875, 0.8, 0.72, 0.65`. Map current sizes to nearest step.

## 5. Step Indicator

Current pill-style works. Two improvements:
- Add a connecting line or subtle chevron between steps (even a `>` character in `--text-3`) to convey sequence.
- The `.done` state uses green text with no background — it disappears. Give done steps `background: var(--green-bg)` for visible completion.

## 6. Button Hierarchy

- Primary vs outline distinction is clear. Good padding (10px 24px).
- **Missing:** a ghost/link-style button for tertiary actions. The result screen has 4 buttons — primary + 3 outlines. The outlines all look equal weight. **Fix:** Make "View Receipt" a text-link style, keep "Add to Claude" and "Download" as outlines.
- Focus-visible ring uses `--accent` — will be orange after swap. Confirm it passes 3:1 contrast on white (`#e67e22` on white = 3.0:1, borderline). May need `#d35400` for focus rings.

## 7. Cycling Example Animation

- 3500ms interval with 500ms transition is reasonable but the implementation recreates all `<span>` elements on every tick via `innerHTML`. This causes a hard cut rather than a crossfade because the exiting span is destroyed, not faded out.
- **Fix:** Keep two spans in DOM, toggle `.visible` class. CSS handles enter/exit. Current approach technically works because only the new visible span animates in, but there is no exit animation — text just vanishes. Add `.cycling-example span:not(.visible){opacity:0;transform:translateY(-8px)}` for symmetry. Consider `ease-in-out` instead of default ease for smoother transitions.

## Summary of Required Changes for Orange Swap

```css
--accent:#e67e22; --accent-light:#fdf2e6; --accent-hover:#d35400;
--border-focus:#e67e22;
--amber:#b45309; --amber-bg:#fef3c7;  /* shift away from orange */
```

Plus update two hardcoded rgba blues:
- Line 65: `box-shadow:0 0 0 3px rgba(230,126,34,0.12)`
- Line 166: `border-color:var(--accent);box-shadow:0 0 0 3px rgba(230,126,34,0.12)`
