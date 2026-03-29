# Demo Realism Audit — Construction Surveying

Reviewer perspective: 15-year construction surveying professional.
Date: 2026-03-27

---

## 1. Pricing

| Item | Demo Value | Realistic Range | Verdict |
|------|-----------|----------------|---------|
| Topo survey (12 acres) | $2,400 | $1,800–$3,600 (12 ac × $150–300/ac) | **Pass.** Mid-range for a small urban site. |
| GPR scan (Mesa commercial) | $1,800 | $3,000–$6,000 (research); GPRS quotes $5K–15K for hand-pushed | **Too low.** Spot+GPR operators charge $3K+ minimum. Change to **$3,200**. |
| Progress photos (feed) | $380 implied | $500–$1,500 for drone photo documentation | **Slightly low** but passable for a tiny site. Add "per acre" context or raise to **$800**. |
| $10K credit bundle | $10,000 | Marco's discretionary budget is $15K/bid. A GC running 10–15 bids/quarter spending $2–5K each = $20–75K/quarter. | **Pass.** Reasonable starter bundle. |

## 2. Response Times

| Metric | Demo Value | Realistic Value | Verdict |
|--------|-----------|----------------|---------|
| SkyVista "42min avg" | 42 min | This is labeled "avg response time." If it means auction-to-dispatch, 42 min is aggressive but plausible for an online operator. If it means flight time for 12 acres, realistic (3–4 hrs on-site per research, but flight-only for 12 ac is ~30–45 min). | **Ambiguous.** Label should say "avg auction response" or "avg flight time." |
| GroundTruth "3.2hr" | 3.2 hr | Spot GPR survey of a commercial lot: 2–4 hours on-site is correct. | **Pass.** |
| AeroSpec "28min" | 28 min | Skydio X10 visual inspection of a single structure: 20–40 min is right. | **Pass.** |
| Result screen "3.2 hrs" total | 3.2 hr | For 12-acre LiDAR topo with Matrice 350: 2–4 hrs on-site (research confirms). Does not include processing. | **Pass** if on-site only. Clarify it excludes data processing (overnight per user story). |

## 3. Accuracy Specs

| Spec | Demo Value | Actual Spec | Verdict |
|------|-----------|-------------|---------|
| LiDAR "±2cm vertical" | ±2cm | Zenmuse L2: 4 cm vertical accuracy at 150m AGL (research). Airborne LiDAR is 2–5 cm absolute (research). | **Optimistic.** ±2cm is achievable only with GCPs and low AGL. Change to **±3–5cm** or specify "with GCPs at 80m AGL." |
| RTK-GPS "±1cm" | ±1cm horizontal | Multi-constellation RTK: ±1cm H, ±1.5cm V is standard. | **Pass** for horizontal. Demo should add "horizontal" qualifier. |
| Result "±1.8cm verified" | ±1.8cm | Beating the L2's rated 4cm V spec by 2x requires ideal conditions + heavy GCP. Plausible but cherry-picked. | **Borderline.** Acceptable as a best-case result, but note it as exceptional. |
| Zenmuse L2 "250m range" | 250m | DJI specs L2 at 250m max range for reflective targets. Effective survey range is ~150m AGL. | **Misleading.** Say "250m max / 150m effective survey altitude." |
| Zenmuse L2 "5 returns" | 5 returns | L2 supports 5 returns per pulse. | **Pass.** Correct. |

## 4. Equipment Specs

| Equipment | Demo Claim | Reality | Verdict |
|-----------|-----------|---------|---------|
| DJI Matrice 350 RTK | Real product | Correct. ~$14,800 combo. | **Pass.** |
| Zenmuse L2 | Real product | Correct. $14,500. | **Pass.** |
| Skydio X10 "48MP" | 48MP | Research says 50MP wide + 64MP narrow. Skydio's own spec is 48MP zoom + 50MP wide. | **Fix.** Change to **"50MP wide + 48MP telephoto"** or just "50MP+." |
| Skydio X10 thermal "FLIR overlay" | FLIR | X10 has FLIR Boson+ 640×512. Calling it "FLIR overlay" is vague but not wrong. | **Pass.** |
| Spot "90min battery" | 90 min | Boston Dynamics rates Spot at ~90 min runtime. | **Pass.** |
| GSSI StructureScan Mini XT "1.6GHz" | 1.6 GHz | StructureScan Mini XT is a real GSSI product rated at 1.6 GHz center frequency. | **Pass.** |
| Leica BLK ARC "±1cm accuracy" | ±1cm | BLK ARC achieves ~5mm–1cm relative accuracy in SLAM mode. | **Pass.** |
| "61MP full-frame, 4cm/px GSD at 120m AGL" (SkyVista photogrammetry) | 61MP | No DJI payload is 61MP full-frame. The P1 is 45MP full-frame. The Zenmuse L2 has a 20MP RGB camera. | **Wrong.** Change to **"45MP full-frame (Zenmuse P1)"** or **"20MP (L2 integrated RGB)"** and recalculate GSD. At 120m AGL, P1 achieves ~2.5cm/px GSD with 35mm lens. |

## 5. Certifications

| Cert | Operator | Verdict |
|------|----------|---------|
| FAA Part 107 | SkyVista, AeroSpec | **Required.** Correct for any commercial drone op. |
| OSHA 10-Hour | SkyVista, AeroSpec | **Pass.** Standard for anyone entering a construction site. |
| AZ ROC Licensed | SkyVista, GroundTruth | **Pass.** Arizona Registrar of Contractors license is real and relevant for construction services. |
| ISO 9001 | SkyVista, GroundTruth | **Unusual.** Most small drone operators are not ISO 9001 certified. More realistic for a larger firm with a fleet. | **Minor flag** — fine for a 4-unit fleet operator. |
| BVLOS Waiver (AZ) | AeroSpec | **Pass.** FAA issues site-specific BVLOS waivers. Listing state is reasonable. |
| Confined Space Certified | GroundTruth | **Pass.** Relevant for Spot in enclosed areas. |

## 6. Deliverable Formats

| Format | Usage | Verdict |
|--------|-------|---------|
| LandXML | DTM import into Civil 3D, HeavyBid, Trimble Business Center | **Pass.** Industry standard. |
| DXF | Contour maps, linework | **Pass.** Universal CAD exchange. |
| GeoTIFF | Orthomosaics, rasters | **Pass.** Standard for georeferenced imagery. |
| LAS | Point clouds | **Pass.** Industry standard (LAS/LAZ). |
| Missing: CSV cross-sections | The user story mentions CSV at 50-ft stations — demo deliverables modal does not list it. | **Add CSV** to the download modal for completeness. |

## 7. Review Text

- "LandXML imported directly into Civil 3D" — sounds like a real estimator. **Pass.**
- "GPR scan found a utility line our plans missed" — realistic GPR success story. **Pass.**
- "Slight delay due to wind hold but they resumed automatically" — realistic drone ops issue. **Pass.**
- "BVLOS capability means they can cover large highway corridors without repositioning" — technically accurate. **Pass.**
- Overall the reviews read as genuine construction professional language. No marketing-speak detected.

## 8. Operator Names

| Name | Risk | Verdict |
|------|------|---------|
| SkyVista Survey | "SkyVista" is used by multiple real companies (SkyVista Imaging, etc.) | **Low risk** — common compound. Fine for demo. |
| GroundTruth Robotics | "Ground Truth" is a real geospatial company (groundtruthautonomy.com) | **Medium risk.** Consider "GroundScan Robotics" or "SubTerra Robotics." |
| AeroSpec Solutions | No obvious conflicts found. | **Pass.** |

## 9. Feed Events

- Construction activities (topo survey, GPR scan, progress photos, bridge inspection, as-built verification) are all real survey tasks. **Pass.**
- Locations are real US cities appropriate for the AZ/NV/NM service area plus national expansion. **Pass.**
- "14,283 tasks completed this week" for a pre-launch marketplace is aspirational but acceptable as demo theater. Label as "simulated" or remove the specific count.
- Feed prices for non-survey tasks ($0.20–$1.20) are mixed in with survey prices ($1,800–$2,400), creating a jarring range. The IoT sensor reading prices belong to a different product than construction surveys. **Separate these** or remove the sub-dollar prices from the construction-focused demo.

## Summary: 6 Items to Fix

1. **GPR price**: $1,800 → $3,200 (too low vs. research and market)
2. **Skydio X10 camera**: 48MP → 50MP wide (wrong spec)
3. **Photogrammetry camera**: 61MP full-frame → 45MP full-frame (Zenmuse P1) — no 61MP DJI payload exists
4. **LiDAR accuracy**: ±2cm vertical → ±3–5cm vertical (or add "with GCPs" qualifier)
5. **Zenmuse L2 range**: 250m → "250m max / 150m survey altitude"
6. **Feed price mixing**: Sub-dollar IoT readings in the same feed as $2,400 surveys — visually confusing for the construction buyer persona
