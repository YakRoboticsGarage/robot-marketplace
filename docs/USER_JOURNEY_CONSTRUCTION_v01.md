# User Journey: Construction Site Surveying (v0.1)

> **Version:** 0.1.1 | **Date:** 2026-03-28 | **Story:** Construction Wedge
>
> This is the construction-focused user journey for the marketplace.
> It describes Marco's experience hiring robots for a pre-bid highway survey.
> For research backing, see `research/SYNTHESIS_JTBD_WEDGE_PROPOSAL.md`, `research/RESEARCH_ROBOTS_AND_SENSORS.md`.
> For payment/legal research, see `research/RESEARCH_CONSTRUCTION_PAYMENT_FLOWS.md`, `research/RESEARCH_PAYMENT_BOND_VERIFICATION.md`, `research/RESEARCH_LEGAL_FRAMEWORK_SURVEY_CONTRACTS.md`.
> For gap analysis, see `research/ANALYSIS_AUTONOMOUS_EXECUTION_GAPS.md`.
> See also: `_archive/USER_JOURNEY_MARKETPLACE_v01.md` (Sarah), `USER_JOURNEY_LUNAR_v01.md` (Kenji), `USER_JOURNEY_PRIVATE_v01.md` (Diane).

---

## Meet Marco

Marco Reyes is a senior estimator at Ridgeline Civil, a mid-size general contractor ($180M annual revenue, 340 employees) headquartered in Phoenix with active projects across Arizona, Nevada, and New Mexico. Ridgeline specializes in highway, bridge, and commercial site development.

Marco manages 4-6 bids at a time. Each bid requires 1-3 site visits for survey data before he can produce reliable earthwork quantities. He has $15K discretionary authority per bid for pre-construction services -- survey crews, geotech reports, environmental screens -- without VP approval.

His problem is not cost. It is time. A two-person survey crew runs $8,000-10,000 per 100-acre highway corridor and takes 5-6 days to deliver processed data. Marco has two regular crews and both are booked solid from March through October. When three bids overlap -- which happens every month during spring letting season -- he cannot get survey data fast enough. Late data means rushed estimates. Rushed estimates mean lost bids or winning at the wrong price.

Marco does not care about robots. He cares about getting accurate site data into Civil 3D before Thursday's bid deadline.

---

## One-Time Setup (15 minutes, once)

Before Marco ever posts a task, someone at Ridgeline sets up the account.

1. **Ridgeline's controller visits the platform dashboard** and creates a company account. The controller chooses a payment method based on project type:
   - **MDOT / public projects:** Upload the project's payment bond certificate (PDF). The marketplace verifies the bond number, surety, and coverage amount against the surety's online portal. Tasks are marked **"Payment Bonded"** -- operators can see surety-guaranteed payment security before they bid.
   - **Private projects:** Connect a bank account via Plaid (ACH verification) and fund a milestone escrow, or purchase a prepaid credit bundle. Tasks are marked **"Escrow Funded."**
   - **Small tasks (under $5K):** Purchase a prepaid credit bundle -- a single line item: `YAK ROBOTICS MARKETPLACE $5,000.00`. Or transfer 5,000 USDC to the platform wallet.
2. **Marco's AI assistant (Claude) is connected.** The controller pastes an API key into Claude's configuration. Marco's assistant can spend up to $5,000 per task, auto-approving anything under $500.
3. **Default deliverable formats are set:** LandXML for terrain models, DXF for plan overlays, CSV for cross-sections. These match Ridgeline's Civil 3D and HCSS HeavyBid import requirements.
4. **Insurance and licensing defaults are set:** The controller enters Ridgeline's minimum insurance requirements (CGL $1M/$2M, E&O $1M/$2M, drone/aviation liability $1M) and licensing requirements (PLS in Arizona, FAA Part 107). These become automatic qualification checks on every auction.

That's it. Marco has verified payment capability on the platform. No blockchain wallet setup, no drone pilot certifications, no sensor selection. His assistant is authorized to act on his behalf.

<details>
<summary>Under the hood</summary>

**Payment verification depends on project type.** For MDOT projects, the payment bond already exists (required by Michigan law MCL 129.201 for public projects over $50K). The marketplace extracts bond number, surety name, principal, and penal sum from the uploaded PDF and cross-references against the surety's verification portal (Travelers, Liberty Mutual, CNA, etc.). The GC does not pay anything new -- the marketplace verifies an existing instrument. For private projects, the controller funds milestone escrow via ACH. For small tasks, prepaid credits work like before. USDC deposits are detected on-chain and credited to the internal ledger. All funding sources look identical to Marco.

**Insurance minimums** are stored as account-level defaults and applied to every auction as hard constraints. Operators whose COI does not meet the minimums are filtered out before their bids are scored.

</details>

---

## Journey A: Happy Path

**Marco needs a pre-bid topographic survey for a 12-acre highway widening project. His agent posts the task, two robots win different subtasks, the survey completes in 4 hours for $3,600. Marco wins the $14.2M contract.**

### The Request

**Tuesday, 8:15 AM MST** -- Marco types a message to Claude:

> "I need topo and subsurface data for a pre-bid survey. SR-89A widening near Sedona, milepost 340 to 342, about 12 acres. Need cut/fill-ready terrain and GPR for utilities. Bid deadline is next Thursday -- I need processed data by Saturday."

Claude responds in 30 seconds:

> "Got it. I've scoped this as two parallel tasks:
>
> 1. **Aerial LiDAR topographic survey** -- 12 acres, 5 cm accuracy, deliverables in LandXML + DXF + CSV cross-sections at 50-ft stations.
> 2. **Ground-penetrating radar subsurface scan** -- full alignment, utility location + depth, deliverables in DXF overlay + anomaly report.
>
> Budget ceiling: $4,500 for both. I'm posting now. You'll have bids within two hours."

Marco goes back to his quantity takeoff for another project. He did not specify which robots, which sensors, or which data formats. Claude handled all of that.

<details>
<summary>Under the hood</summary>

Claude translated Marco's plain-English request into two structured task specifications. It geocoded the corridor limits from ADOT's milepost system, estimated the survey area, identified sensor requirements (LiDAR for topo, GPR for subsurface), set accuracy thresholds (5 cm horizontal, 4 cm vertical per Zenmuse L2 spec), and posted both tasks to the auction engine with a Saturday data deadline.

</details>

### The Auction (Marco doesn't see this)

Two tasks hit the marketplace at 8:16 AM. By 10:30 AM, bids are in.

**Task 1 -- Aerial LiDAR:**

| | SkyView Mapping | Desert Hawk Geo | Prescott UAV |
|---|---|---|---|
| **Robot** | DJI Matrice 350 RTK + Zenmuse L2 | DJI Matrice 350 RTK + Zenmuse L2 | DJI Matrice 4E |
| **Price** | $2,200 | $2,600 | $1,400 |
| **Rating** | 4.8 (47 surveys) | 4.5 (22 surveys) | 4.2 (15 surveys) |
| **Accuracy** | 5 cm (meets spec) | 5 cm (meets spec) | 8 cm (below spec) |

Prescott's Matrice 4E is filtered out -- 8 cm accuracy does not meet the 5 cm requirement. SkyView wins on the combined score: strong reputation, competitive price, meets all specs.

**Task 2 -- GPR Subsurface:**

| | RedRock Robotics | Basin Survey Tech |
|---|---|---|
| **Robot** | Boston Dynamics Spot + GPR payload | Spot + GPR payload |
| **Price** | $1,400 | $1,800 |
| **Rating** | 4.6 (31 tasks) | 4.3 (12 tasks) |

RedRock wins. Lower price, stronger track record.

**Total: $3,600.** That is 58% less than a human survey crew's $8,500 quote for the same corridor, and data arrives days sooner.

### Award Confirmation (Marco reviews the recommended winners)

Claude presents the recommended winners to Marco with a qualification summary:

> "I'm recommending two operators for your SR-89A survey. Here's the summary:
>
> **Task 1 -- Aerial LiDAR:** SkyView Mapping ($2,200)
> - Insurance: CGL $2M/$5M, E&O $1M/$2M, drone liability $2M -- all exceed your minimums
> - Licensing: PLS #48271 (Arizona, active through Dec 2027), FAA Part 107 current
> - Track record: 4.8 stars, 47 completed surveys, no disputes
>
> **Task 2 -- GPR Subsurface:** RedRock Robotics ($1,400)
> - Insurance: CGL $1M/$2M, E&O $1M/$2M -- meets minimums
> - Licensing: PLS #51034 (Arizona, active through Jun 2027), FAA Part 107 current
> - Track record: 4.6 stars, 31 completed tasks, no disputes
>
> Total: $3,600. SkyView flies Wednesday morning (weather clear, winds 8 mph). RedRock runs GPR Wednesday afternoon. Processed data to you by Friday evening.
>
> Confirm award, or would you like to review other bidders?"

Marco replies: "Confirmed."

Claude generates the subcontract agreements automatically -- one for each operator, populated from the task spec, bid terms, and Ridgeline's standard provisions. Both operators receive their agreements and countersign digitally. Work is authorized to begin.

<details>
<summary>Under the hood</summary>

The award confirmation step is a deliberate pause between the auction engine's recommendation and the start of work. The system runs automated checks before presenting the recommendation to Marco: (a) COI parsed from ACORD 25 form -- policy current, limits verified, additional insured endorsement confirmed, (b) PLS license validated against the Arizona Board of Technical Registration database, (c) FAA Part 107 certificate verified, (d) no DBE/MBE conflicts for the project. If any check fails, the operator is flagged and the next-ranked bidder is presented instead. Marco can also reject a recommended winner for reasons the system cannot detect -- prior bad experience, conflict of interest, client-prohibited vendor -- and the system moves to the next bidder.

After Marco confirms, the marketplace auto-generates a subcontract based on ConsensusDocs 751 (short form) with survey-specific exhibits: scope from task spec, price from bid, deliverable formats, accuracy requirements, weather constraints, data ownership terms, limitation of liability (1x task fee), and mutual indemnification. Digital signatures via ESIGN/UETA-compliant e-signature. Both parties execute before work begins.

</details>

### The Survey

**Wednesday, 7:00 AM** -- SkyView's pilot launches the Matrice 350 RTK from a pulloff at milepost 340. The drone flies the corridor in 2.5 hours across two battery swaps, capturing 4.2 million LiDAR points per second and 20MP RGB imagery.

**Wednesday, 1:00 PM** -- RedRock deploys Spot with a GPR payload at the north end. The robot traverses the alignment autonomously, scanning for buried utilities, voids, and soil layer transitions. Coverage complete by 4:30 PM.

Both operators upload raw data to the platform by end of day.

### The Deliverables

**Friday, 6:00 AM** -- The processing pipeline runs overnight. By morning, Marco has in his inbox:

- A **LandXML digital terrain model** ready for Civil 3D import
- **Cross-sections at 50-foot stations** along the centerline, in CSV for HeavyBid
- A **2-inch resolution orthomosaic** of the full corridor (GeoTIFF)
- A **DXF utility overlay** showing 14 detected subsurface features with depth estimates
- An **anomaly report** flagging two areas where GPR returns suggest rock outcrop at 3-4 feet (heavy cut zones) and one unmarked utility crossing at station 42+00

Marco spends Friday morning importing the terrain model into Civil 3D. The earthwork quantity takeoff -- which usually takes two full days working from survey crew field books -- takes four hours because the data is already in the right coordinate system and format. He prices the bid at $14.2M.

**Next Thursday** -- Ridgeline submits the bid on time, with quantities Marco trusts.

**Two weeks later** -- ADOT notifies them: they won.

### What Happens Next

Marco's first message back to Claude:

> "We got SR-89A. Set up monthly progress monitoring flights starting May 1, same corridor, same LiDAR specs. I need cut/fill volumes compared to the pre-bid baseline for each pay application."

Claude creates a recurring monthly task. The pre-bid terrain model becomes the volumetric baseline. Each month, the system posts the monitoring task, collects bids, dispatches the flight, processes data, and delivers a progress report -- formatted for direct attachment to Ridgeline's monthly pay application to ADOT.

---

## Journey B: No Robots Available

**Marco needs a survey in rural New Mexico where no operators are registered. He finds out immediately. No charge.**

**9:00 AM** -- Marco types:

> "I need topo for a bridge replacement bid near Raton, NM. US-64, milepost 280 to 282."

Claude responds within 10 seconds:

> "No drone or ground robot operators are currently registered in the Raton, NM area. The nearest operators are in Albuquerque (180 miles) and Trinidad, CO (35 miles, but not registered on the platform).
>
> I can:
> 1. **Notify you** when an operator registers within 50 miles of this site.
> 2. **Suggest a manual survey vendor** -- Meridian Land Services has availability next week, estimated $7,200 for this scope.
>
> No charge for checking coverage."

Marco's balance is untouched. He calls Meridian, books the crew, and makes a note to check back in six months. The platform logged the unserved demand -- this data feeds the operator heatmap that shows where new operators should deploy.

<details>
<summary>Under the hood</summary>

The platform queried all registered operators, found none with coverage area including Colfax County, NM. The task was never posted to the auction. No bids were solicited, no credits reserved. The unserved location was logged to the demand analytics pipeline.

</details>

---

## Journey C: Mid-Task Weather Hold

**A drone survey is interrupted by wind exceeding 25 mph. The system pauses, notifies Marco, auto-resumes when conditions clear. Partial data is preserved.**

**Wednesday, 9:30 AM** -- SkyView's Matrice 350 is 40 minutes into the LiDAR survey of a different corridor. Wind speed at the site climbs from 15 to 27 mph.

**9:31 AM** -- The platform receives a weather alert from the NOAA API. Wind exceeds the 25 mph operational limit for the Matrice 350 RTK.

**9:32 AM** -- The system sends SkyView a hold command. The drone lands safely. Marco gets a notification from Claude:

> "Weather hold on your I-17 survey. Wind at 27 mph exceeds the drone's 25 mph limit. SkyView has landed safely. 40% of the corridor is captured and preserved. I'm monitoring conditions -- forecast shows winds dropping below 15 mph by 1:00 PM. I'll auto-resume and notify you. No action needed."

**1:15 PM** -- Wind drops to 12 mph. The platform checks the NOAA feed, confirms the window, and sends a resume signal. SkyView relaunches from where it stopped.

**3:45 PM** -- Survey complete. The remaining 60% is captured and merged with the morning's partial data into a single seamless dataset.

**4:00 PM** -- Claude notifies Marco:

> "I-17 survey complete. Weather hold added 3.5 hours but all data is captured. Processing now -- deliverables by tomorrow morning."

Marco was never asked to make a decision. The system paused, waited, resumed, and merged. His cost did not change -- the bid price covered the full corridor regardless of weather interruptions.

<details>
<summary>Under the hood</summary>

The task spec includes weather constraints: max wind 25 mph, no precipitation, visibility > 3 statute miles. The platform monitors NOAA's Aviation Weather API for the task's GPS coordinates. When conditions breach limits, the task state transitions from `executing` to `weather_hold`. Partial data is checkpointed. When conditions clear and remain stable for 15 minutes, the task resumes. The operator's bid covers weather-related delays up to 8 hours; beyond that, the task is renegotiated.

</details>

---

## What Marco Sees on His Expense Report

At the end of the quarter, Ridgeline's controller sees one or two line items on the corporate card:

| Date | Description | Amount |
|------|-------------|--------|
| Mar 3 | YAK ROBOTICS MARKETPLACE | $5,000.00 |
| Apr 15 | YAK ROBOTICS MARKETPLACE | $5,000.00 |

On the platform dashboard, the controller sees the per-task breakdown:

| Date | Project | Task | Cost | Balance |
|------|---------|------|------|---------|
| Mar 5 | SR-89A Sedona | Aerial LiDAR topo (12 acres) | $2,200 | $2,800 |
| Mar 5 | SR-89A Sedona | GPR subsurface scan | $1,400 | $1,400 |
| Mar 19 | I-17 Corridor | Aerial LiDAR topo (22 acres) | $3,100 | $3,300 |
| May 1 | SR-89A Sedona | Monthly progress flight #1 | $1,200 | $2,100 |
| Jun 1 | SR-89A Sedona | Monthly progress flight #2 | $1,200 | $900 |

When the balance runs low, the controller tops up. One card charge, many surveys.

---

## What the Robot Operator Sees

SkyView Mapping operates a fleet of three DJI Matrice 350 RTK drones across Arizona. Their experience:

- **Setup (once):** Register each drone on the platform. Configure pricing rules (base rate per acre, adjustments for terrain complexity and turnaround time). Set coverage area (Phoenix metro + northern Arizona). Connect bank account or USDC wallet for payouts.
- **Ongoing:** The platform sends bid requests matching SkyView's coverage area and equipment. The operator reviews and accepts bids, or configures auto-bidding rules. After each completed survey, raw data is uploaded and the processing pipeline handles deliverable generation.
- **Payout:** After delivery confirmation, payment transfers to SkyView's account. For Marco's SR-89A survey: $2,200 received within 24 hours.
- **Dashboard:** Completed tasks, revenue by month, drone utilization rates, upcoming scheduled flights, maintenance reminders.

RedRock Robotics operates two Spot robots with GPR payloads serving the Southwest. Same model -- register, configure pricing, accept tasks, upload data, receive payment.

---

## What Marco Never Saw

Everything below happened invisibly between Marco's one-sentence request and his processed survey data:

- Claude parsed "SR-89A widening near Sedona" into GPS coordinates using ADOT's milepost database, calculated a 12-acre survey extent with 200-foot offset buffers.
- The system decomposed Marco's request into two parallel subtasks -- aerial LiDAR and ground GPR -- based on sensor requirements for earthwork estimation and utility detection.
- Six robots across four operators submitted bids. One was filtered out for insufficient accuracy. Five were scored on capability match, reputation, price, and estimated turnaround.
- The NOAA Aviation Weather API was queried to confirm a flyable window on Wednesday (clear skies, winds under 12 mph, visibility 10+ miles).
- $3,600 in platform credits were reserved at bid acceptance -- split 25% on acceptance, 75% on delivery confirmation.
- Both operators coordinated schedules so the drone flew in the morning and Spot ran GPR in the afternoon, avoiding airspace conflicts.
- Raw LiDAR point clouds (4.2M points/sec, 2.5 hours) were classified -- ground, vegetation, structures -- using automated algorithms.
- GPR radargrams were correlated against 811 utility records to distinguish known utilities from unknown anomalies.
- The processing pipeline converted everything into Marco's preferred formats: LandXML for Civil 3D, DXF for plan overlays, CSV for HeavyBid cross-sections.
- A commitment hash `H(request_id || salt)` was recorded on Base for the USDC settlement -- not the raw task ID.
- Both operators' wallet addresses were resolved internally at settlement time. Marco never saw a blockchain address.

Marco typed two sentences and got a bid-ready data package. That's the product.

---

## What Marco's Legal Team Sees

Ridgeline's project administrator and legal counsel have a separate dashboard view. For the SR-89A survey, they see:

**Payment Security:**
- Payment method: Prepaid credits (private project) or Payment Bond verified (MDOT project)
- Bond status (if public): Bond #SUR-2026-48812, Travelers Casualty and Surety, penal sum $18.4M, verified against Travelers portal
- Escrow status (if private): $3,600 reserved from prepaid balance at award confirmation

**Operator Qualifications (per operator):**
- Certificate of Insurance (ACORD 25): parsed and verified
  - CGL: carrier, policy number, limits, additional insured status, waiver of subrogation
  - Professional Liability / E&O: carrier, retroactive date, limits
  - Drone / Aviation Liability: carrier, limits, hull coverage
  - Workers Comp: statutory, employer's liability limits
- PLS license: number, state, expiration, firm Certificate of Authorization
- FAA Part 107: certificate number, expiration
- DBE/MBE status (for federally-funded projects): certified or N/A

**Agreement Status:**
- Auto-generated subcontract (ConsensusDocs 751 short form + survey exhibits)
- Key terms: scope, price, deliverable formats, accuracy requirements, schedule, retainage (if applicable), data ownership, limitation of liability (1x fee), mutual indemnification, dispute resolution (negotiation -> mediation -> arbitration)
- Execution status: both parties signed digitally (ESIGN/UETA compliant)
- Audit trail: timestamped log of all actions from task posting through award confirmation

**Compliance Flags (auto-monitored):**
- Insurance expiration alerts (yellow at 30 days, red at 7 days)
- PLS license renewal reminders
- MDOT prompt payment tracking (10-day requirement after receiving owner payment, MCL 125.1561)
- Lien waiver exchange status (auto-generated conditional/unconditional waivers at each payment milestone)

The legal team never touches a routine survey task. They review only when the system flags an exception -- an expired policy, a licensing gap, a DBE shortfall, or a disputed deliverable.

---

## Timing

| Event | Time | Elapsed |
|-------|------|---------|
| Marco sends request | Tue 8:15 AM | 0 |
| Claude scopes and posts two tasks | Tue 8:16 AM | 1 min |
| Payment verification (bond or escrow confirmed) | Tue 8:17 AM | 2 min |
| Bids received from 6 robots | Tue 10:30 AM | 2 hr 15 min |
| Automated qualification checks (COI, PLS, Part 107) | Tue 10:31 AM | 2 hr 16 min |
| Claude presents recommended winners to Marco | Tue 10:32 AM | 2 hr 17 min |
| Marco reviews qualifications and confirms award | Tue 10:35 AM | 2 hr 20 min |
| Subcontracts auto-generated and sent for e-signature | Tue 10:36 AM | 2 hr 21 min |
| Both operators countersign agreements | Tue 11:15 AM | 3 hr |
| Drone LiDAR survey (SkyView) | Wed 7:00-9:30 AM | Day 2 |
| GPR subsurface scan (RedRock) | Wed 1:00-4:30 PM | Day 2 |
| Raw data uploaded by both operators | Wed 6:00 PM | Day 2 |
| Processing pipeline runs overnight | Wed-Thu | Day 2-3 |
| Processed deliverables in Marco's inbox | Fri 6:00 AM | Day 3 |
| Marco completes earthwork takeoff | Fri 12:00 PM | Day 3 |
| Lien waivers exchanged, escrow released | Fri 1:00 PM | Day 3 |
| **Total: request to bid-ready data** | | **~3 days** |

Compare: human survey crew would have delivered in 10-12 days (5-6 days field work + 5-6 days processing). Marco gained a full week. The award confirmation, agreement execution, and payment verification added less than one hour to the timeline -- all happening while Marco was doing other work.

---

## Cost Breakdown

| | Amount | Recipient |
|---|---|---|
| **Marco pays (total)** | $3,600 | Debited from platform credits |
| SkyView Mapping (aerial LiDAR) | $2,200 | Transferred to operator |
| RedRock Robotics (GPR scan) | $1,400 | Transferred to operator |
| **Platform fee** | $0.00 (seed phase) | Platform takes no cut during seed phase |
| **Human crew equivalent** | $8,500 | What Marco would have paid Desert Sun |
| **Savings** | $4,900 (58%) | Plus 7 days faster |

### Full Project Lifecycle Cost Comparison

| Phase | Human Crew | Marketplace | Savings |
|---|---|---|---|
| Pre-bid topo + GPR (12 acres) | $8,500 | $3,600 | 58% |
| Monthly progress monitoring (x14) | $56,000-84,000 | $16,800 | 70-80% |
| As-built verification at closeout | $10,000-15,000 | $5,000 | 50-67% |
| **Full project (14 months)** | **~$78,500-107,500** | **~$25,400** | **~68-76%** |

The cost savings matter. But the real ROI is the $14.2M contract Marco won because he had data in time to bid. His survey scheduling bottleneck cost Ridgeline 2-3 missed bids per quarter before the marketplace existed.

---

## From Seed to Scale

- **Construction surveying (now):** Prove the marketplace model with pre-bid topo, GPR, and progress monitoring. Sign 10 GC customers. The first buyers are estimators at mid-size civil contractors ($50-500M revenue) preparing highway and commercial bids. The robots are DJI Matrice 350 RTK drones and Boston Dynamics Spot with survey payloads -- already deployed by hundreds of regional operators.

- **Mining and quarrying (Year 2):** Same robots, same sensors, new buyer persona. Open-pit volumetric surveys, blast pattern assessment, highwall inspections. The mine surveyor has budget and recurring need. LiDAR scanning, terrain nav, and dust hardening overlap with construction. Supply side serves both verticals.

- **Infrastructure monitoring (Year 3):** Add bridge inspections (600K+ federally mandated), pipeline surveys, power line patrols. Requires specialized form factors -- bridge crawlers, confined-space drones -- but the auction engine, processing pipeline, and settlement layer are identical. Federal mandates create a reliable demand floor. Diane's privacy story applies here: government contracts require encrypted task specs and audit trails.

- **Lunar contracts (Year 4+):** Every task Marco hires robots for has a lunar analog. Topographic survey becomes terrain mapping at Shackleton Crater. GPR becomes regolith depth profiling for ISRU. Progress monitoring becomes tracking autonomous excavation of landing pads. The sensor stack transfers directly -- LiDAR works in vacuum, thermal imaging is critical for the -173C to +127C surface swing. The software layer transfers completely: same auction engine, same agent orchestration, same deliverable pipeline. The path from Marco to Kenji is not a pivot. It is a graduation.
