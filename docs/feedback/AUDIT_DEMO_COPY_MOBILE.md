# Demo Copy & Mobile Audit (375px)

Reviewed: `demo/index.html` | Date: 2026-03-27

---

## 1. Mobile Line Breaks

| Element | Issue | Fix |
|---------|-------|-----|
| Hero badge `47 operators online · 312 robots · AZ, NV, NM, CA` | At 375px (20px padding each side = 335px usable), this wraps after "robots" leaving "AZ, NV, NM, CA" orphaned on line 2 | Shorten to `47 operators · 312 robots · 4 states` or split into two lines by design |
| Cycling example `Pre-bid topographic survey, 12-acre highway project, I-17 corridor` | ~62 chars at 0.8rem. Wraps to 3 lines on 375px; "corridor" orphans | Shorten: `Pre-bid topo survey, 12-acre highway, I-17 corridor` |
| Cycling example `Existing condition photos + LiDAR, commercial site in Scottsdale` | Same overflow, "Scottsdale" orphans | `Existing condition photos + LiDAR, Scottsdale commercial site` |
| Cycling example `Monthly progress monitoring, Phase 2 grading, Mesa project` | Borderline; "project" may orphan | `Monthly progress monitoring, Phase 2 grading, Mesa` |
| Cycling example `Underwater pipe inspection (try me!)` | Fine width but `(try me!)` alone on line 2 in some viewports | `Underwater pipe inspection — try me!` (em dash, no parens) |
| Robot specs line `42min avg · 99.4% uptime · LandXML/DXF · FAA Part 107` | This is generated as `Xs avg · XX.X% uptime · JSON · IPXX`. At 0.72rem mono it fits ~40 chars; the first 3 robots use longer spec text in the detail panel but the card line is fine | No change needed for card specs |
| Bid card desc `Phoenix Metro · DJI Matrice 350 RTK · LiDAR + RTK` | At 0.72rem in a full-width card (stacks to 1col on mobile), this is ~50 chars; "RTK" orphans | Shorten to `Phoenix Metro · DJI M350 RTK · LiDAR` |
| Bid card desc `Southwest US · Spot + GPR · LiDAR + ground combo` | "combo" orphans | `Southwest US · Spot + GPR · LiDAR + ground` |
| Payment copy `$10,000 credit bundle · use across multiple surveys · this topo survey will cost ~$2,400` | 87 chars at 0.8rem, wraps to 3+ lines; "~$2,400" orphans | Break into two lines: `$10,000 credit bundle · use across multiple surveys` then `This topo survey will cost ~$2,400` |
| Result sub `I-17 Corridor · SkyVista Survey · ±1.8cm accuracy verified` | "verified" orphans at 375px | `I-17 Corridor · SkyVista Survey · ±1.8cm verified` |
| Operator CTA `Own a robot? List it on the marketplace and start earning.` + inline button | Text + button on one line wraps badly; button may drop to its own line leaving "earning." orphaned | Already handled by `@media(max-width:600px)` flex-direction:column -- OK |
| Trust strip 4 items inline | `white-space:nowrap` on each span is correct, but 4 items overflow 375px and are not scrollable; they stack and break layout | Add `overflow-x:auto` or reduce to 3 items on mobile |

## 2. Copy Quality

| Location | Issue | Fix |
|----------|-------|-----|
| How-it-works step 1 `Your AI agent translates needs into sensor specs and deliverable formats.` | An estimator doing a pre-bid survey does not think in terms of "AI agents" yet | `We translate your needs into sensor specs and deliverable formats.` |
| How-it-works step 3 `LiDAR point clouds, topo maps, GPR profiles in Civil 3D-ready formats.` | "GPR profiles" is fine for construction; "Civil 3D-ready" is the right jargon for this audience | OK |
| Claude spec card `survey_type: topographic (pre-bid)` | Key-value format reads as developer output, not estimator-friendly | Acceptable -- it is intentionally "structured by Claude" technical output |
| `ERC-8004 identity pre-registered` (buy-robot screen) | Blockchain jargon; an estimator does not know ERC-8004 | `On-chain identity pre-registered` or just `Registered on the network` |
| `ERC-8004 compatible` (register CTA) | Same issue | `Network-compatible` |
| Feed label `14,283 tasks completed this week` | Inconsistent with feed screen header `14,283 tasks this week` (missing "completed") | Pick one; the shorter version is better for both locations |
| Operator step 1 `Register your equipment on-chain (ERC-8004)` | Again, drop the spec number for this audience | `Register your equipment on the network` |

## 3. Consistency

| Check | Status |
|-------|--------|
| Auction winner = result screen operator | SkyVista Survey in both. OK |
| Auction price $2,400 = result cost $2,400 | Match. OK |
| Balance: $10,000 - $2,400 = $7,600 | Shown correctly. OK |
| Receipt matches result screen data | All fields consistent. OK |
| Robot count: hero badge says 312 robots, available section says 1,047 registered / 312 online | 312 = online count, 1,047 = total. Consistent. OK |
| Step indicator labels: Search > Review > Pay > Result | "Result" on step 4, but auction screen is step 4 too, then result replaces it. Minor: consider "Done" or "Deliver" to distinguish from the auction step | Optional |

## 4. Step Pills on Small Screens

The step indicator uses `padding:4px 12px` per pill with 4 pills + 3 chevrons. At 375px this totals ~300px -- tight but fits. However, if labels were longer it would break. Current labels (Search, Review, Pay, Result) are safe.

## 5. Summary of Required Changes (Priority Order)

1. **Hero badge**: shorten for mobile or add a `@media` line break
2. **Cycling examples**: trim 3 of 7 examples that exceed ~50 chars
3. **Bid card descriptions**: abbreviate "DJI Matrice 350 RTK" to "DJI M350 RTK"
4. **Payment screen**: break the 87-char line into two sentences
5. **Trust strip**: add `overflow-x:auto` or hide 4th item on mobile
6. **ERC-8004 references** (3 locations): replace with plain language
7. **"AI agent" in how-it-works**: reword to "we" for estimator audience
8. **Feed label consistency**: use `14,283 tasks this week` in both places
