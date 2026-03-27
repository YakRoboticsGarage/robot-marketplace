# Jobs-to-be-Done: Wedge Market Proposal

**Date:** 2026-03-27
**Purpose:** Answer the senior PM's question: "What would a robot actually be hired for?"

---

## The Wedge: Construction Site Surveying

We evaluated eight candidate verticals: construction, insurance, infrastructure, environmental compliance, real estate, agriculture, mining, and facilities management. Construction site surveying scores highest (4.25/5 weighted) because it is the only industry where every qualifying condition converges simultaneously.

The demand is real and quantifiable: U.S. construction surveying services represent an $8B/year market, with pre-bid surveys alone at $1.2B. Buyers already spend $2-5K per site visit on human survey crews and do it dozens of times per quarter across geographies, making robot ownership impractical. The sensor stack (LiDAR, RTK-GPS, photogrammetry, GPR) maps one-to-one onto lunar surface operations for Artemis base construction. The deliverables are concrete -- contour maps, cut/fill reports, BIM models -- not abstract "data." And the AI agent layer adds genuine value by converting raw point clouds into bid-ready data packages, which is the thing the buyer actually pays for.

Mining scored second (3.95) with the strongest lunar transfer path after construction, but its geographically concentrated operations weaken marketplace network effects. Infrastructure scored third (3.65) with unbeatable regulatory tailwinds (federal bridge inspection mandates), but it requires specialized robot form factors -- bridge crawlers, confined-space platforms -- that slow initial supply aggregation. Construction surveying is the wedge where we prove the model, and both mining and infrastructure become natural expansions once traction is established.

## The Buyer: Meet Marco

Marco Reyes is a senior estimator at Granite Basin Civil, a mid-size general contractor ($180M annual revenue, 340 employees) headquartered in Phoenix with active projects across Arizona, Nevada, and New Mexico. Granite Basin ranks in the ENR Top 400 regional firms, specializing in highway, bridge, and commercial site development. They win roughly 25-30% of the projects they bid on.

Marco personally manages 4-6 bids at a time. Each bid requires 1-3 site visits for survey data before he can produce reliable earthwork quantities. He has $15K discretionary authority per bid for pre-construction services -- survey crews, geotech reports, environmental screens -- without needing VP approval. Above $15K, he escalates to the pre-construction director.

His current pain is not cost. It is time. A two-person survey crew costs $8,000-10,000 per 100-acre highway corridor visit and takes 5-6 days to deliver processed data. That is fine when he has one bid in the pipeline. But Granite Basin bids on 10-15 projects per quarter, and when three bids overlap -- which happens every month during the spring letting season -- Marco cannot get survey crews scheduled fast enough. He has two regular crews he trusts (Desert Sun Surveying and Meridian Land Services), and both are chronically overbooked from March through October.

Late survey data means rushed estimates. Rushed estimates mean either losing the bid (quantities too high) or winning it at the wrong price (quantities too low, margin evaporates during construction). Marco estimates that survey scheduling bottlenecks cost Granite Basin 2-3 missed bid opportunities per quarter -- roughly $500K-1M in potential revenue per missed bid.

Marco does not care about robots. He cares about getting accurate site data into HCSS HeavyBid before Thursday's bid deadline.

## Five Jobs Marco Hires Robots For

Each job is stated in JTBD format: "When [situation], I want to [motivation], so I can [outcome]." For each, we identify the specific robot and sensor, current cost, marketplace cost, required deliverable format, and how an AI agent adds value beyond what a simple booking portal could provide.

### 1. Pre-Bid Topographic Survey

> "When I'm preparing a highway bid with a 10-day deadline, I want topographic data (elevations, contours, cross-sections) for the entire corridor, so I can calculate earthwork volumes and submit an accurate bid."

- **Robot/sensor:** DJI Matrice 350 RTK + Zenmuse L2 LiDAR (5 cm accuracy, 20MP RGB)
- **Human crew cost:** $8,000-10,000 for 100-acre corridor, 5-6 day turnaround
- **Marketplace cost:** $1,500-3,000, same-day flight, 24-hour processed delivery
- **Deliverable format:** Digital terrain model (DTM) in LandXML, contour map in DXF, cross-sections at 50-foot stations in CSV for import into HCSS HeavyBid or B2W Estimate
- **Agent value:** The agent converts raw LiDAR point clouds into bid-software-compatible formats automatically. Marco uploads the RFP scope, the agent determines survey extents, posts the task, evaluates bids from drone operators, and delivers processed files -- not raw data Marco's team would spend two days cleaning.

### 2. Existing Condition Documentation

> "When I need to verify what's actually on-site versus what the plan documents show, I want high-resolution 3D documentation of existing structures, pavement, and drainage, so I can identify discrepancies before I price demolition and site prep."

- **Robot/sensor:** Skydio X10 (50MP wide + 64MP narrow + thermal) or Boston Dynamics Spot + Leica BLK ARC for interior/structural areas
- **Human crew cost:** $3,000-5,000 per visit (manual walkthrough + photography + field notes)
- **Marketplace cost:** $2,000-4,000 (drone + ground robot combined mission)
- **Deliverable format:** Georeferenced orthomosaic (GeoTIFF), 3D point cloud (LAS/LAZ), annotated photo catalog with GPS coordinates (PDF report)
- **Agent value:** The agent overlays the captured 3D model against plan documents and flags discrepancies automatically -- a retaining wall that isn't on the plans, a drainage inlet at a different elevation, an unmarked utility corridor. This is the work a junior engineer currently spends 8 hours doing manually.

### 3. Soil/Subsurface Assessment (GPR)

> "When the geotech report only covers three borings on a 2-mile corridor, I want non-destructive subsurface imaging across the full alignment, so I can identify buried utilities, voids, and soil layer transitions that would blow up my earthwork estimate."

- **Robot/sensor:** Boston Dynamics Spot + GPR payload (ground-penetrating radar, depth-dependent resolution)
- **Human crew cost:** $5,000-15,000 for GPR survey with hand-pushed cart (GPRS or similar), 3-5 days
- **Marketplace cost:** $3,000-6,000, Spot covers ground faster and more uniformly than a human operator
- **Deliverable format:** Subsurface profile sections (GPR radargrams), utility location map with depth estimates (DXF/SHP for GIS overlay), anomaly flag report (PDF)
- **Agent value:** The agent correlates GPR returns with known utility records (811 data) and the geotech report, highlighting where subsurface conditions diverge from assumptions. It also estimates risk zones where earthwork costs may exceed the bid allowance.

### 4. Progress Monitoring During Construction

> "When the project is underway and the owner wants monthly cut/fill verification for progress billing, I want automated volumetric surveys comparing current terrain to design grade, so I can submit accurate pay applications without pulling my surveyor off layout work."

- **Robot/sensor:** DJI Matrice 350 RTK + Zenmuse L2 (repeat flights on same corridor)
- **Human crew cost:** $4,000-6,000 per monthly survey (crew redeployed from other tasks)
- **Marketplace cost:** $1,000-2,000 per flight (recurring task, agent auto-schedules monthly)
- **Deliverable format:** Cut/fill heatmap (GeoTIFF), volumetric summary table (CSV), schedule conformance overlay showing planned vs. actual grade (PDF)
- **Agent value:** The agent maintains a temporal baseline from the pre-bid survey, automatically computes volume changes between flights, trends productivity rates, and flags areas falling behind schedule. It generates the owner-ready progress report -- the actual document Marco attaches to the pay application.

### 5. As-Built Verification for Client Handoff

> "When the project is complete and I need to prove we built what the contract specified, I want a comprehensive as-built survey comparing final conditions to design intent, so I can close out the project and release retainage."

- **Robot/sensor:** Spot + BLK ARC (ground-level scan) combined with DJI Matrice 350 + L2 (aerial), producing a fused indoor/outdoor as-built model
- **Human crew cost:** $10,000-15,000 (full survey crew, 5+ days, multiple revisits)
- **Marketplace cost:** $4,000-8,000 (combined aerial + ground mission, 1-2 days)
- **Deliverable format:** As-built BIM model (IFC), deviation report showing where construction differs from design (PDF with color-coded tolerance maps), final point cloud archive (LAS)
- **Agent value:** The agent compares the final scan against the contract design model, quantifies deviations by element, and generates the closeout documentation package. This typically takes an engineer a full week to compile manually. The agent also archives all survey data from the project lifecycle, creating a complete digital twin for the owner's facility management team.

## Why Marketplace, Not Direct Partnership

Three arguments from the marketplace justification research, applied specifically to Marco's situation at Granite Basin Civil.

**1. Geographic variability kills the ownership case.** Granite Basin bids on projects across three states. A $150K survey robot sitting in Phoenix is useless for a bid in Albuquerque next week. And the utilization math is brutal: Marco needs survey data for 10-15 bids per quarter, each requiring 2-3 days of robot time. That is 20-45 days of use per year on an asset that costs $150K and depreciates on an 18-month technology cycle. The marketplace aggregates regional drone operators and ground robot fleets into on-demand national coverage -- the same aggregation logic that makes Uber work for rides and Thumbtack work for home services. Marco pays per task, not per robot.

**2. Multi-sensor tasks require multi-vendor supply.** A single highway bid may need aerial photogrammetry (DJI Matrice), ground-level 3D scanning (Spot + BLK ARC), and subsurface imaging (Spot + GPR) -- three different platforms from three different manufacturers. No single robotics company makes all three. A direct partnership with one vendor covers one-third of Marco's needs. The marketplace matches the right robot to each sub-task and assembles the combined deliverable.

**3. Auction pricing discovers the real market rate.** There is no established price for "robotic site survey of a 100-acre highway corridor." Survey crews charge $8K-10K because that is what labor costs. Robots should cost less, but how much less? Drone-as-a-service pricing ranges wildly: $150-500/acre for small sites, $1.50-30/acre for large sites. Competitive bidding from multiple operators discovers the true price for each specific task. Marco's procurement team gets price transparency they cannot get from a single vendor's rate card. Enterprise data shows multi-vendor strategies yield 10-25% cost savings through sustained competition. And for Marco, every dollar saved on pre-bid surveys is a dollar that improves his bid margin.

## Why Agent-Mediated

Three specific examples of how an AI agent makes Marco's workflow better than clicking through a web portal.

**1. Translating need to spec.** Marco says "I need site data to bid on the I-40 extension near Flagstaff." He does not know (or care) that this requires a Matrice 350 with L2 payload for topo, a Skydio X10 for structure documentation, and a Spot with GPR for subsurface. The agent translates his business need into robot task specifications, selects the right sensor packages, posts parallel tasks, evaluates competing bids, and assembles the combined deliverable. A web portal requires Marco to already know what robots he needs, what sensors they should carry, and what data formats to request -- which is exactly the expertise he is trying to buy, not provide.

**2. Multi-step orchestration across bid cycles.** Marco manages 4-6 simultaneous bids. The agent tracks each bid's survey requirements, schedules flights around weather windows, sequences dependent tasks (aerial first, ground-truth second), and delivers processed data packages by each bid deadline. On a portal, this is 15+ manual steps per bid, across multiple robot types, repeated weekly. The agent reduces this to a single conversational instruction per bid.

**3. Longitudinal project intelligence.** When Marco wins the bid and the project enters construction, the agent reuses the pre-bid survey as the baseline for progress monitoring. It auto-schedules monthly flights, computes volumetric changes against the original terrain model, and generates pay application attachments. A portal treats each task as isolated -- every flight is a new form to fill out, a new operator to select, a new data package to manually compare against last month's. The agent treats Marco's entire project lifecycle as one continuous workflow, from bid survey through construction monitoring to as-built closeout. McKinsey reports that agentic AI in procurement delivers 19-21% lower operating costs and 58% shorter cycle times versus portal-based workflows. For Marco, that means spending his time estimating and managing projects, not managing robot bookings.

## The Robot Supply Side

These robots would be listed on the marketplace for construction surveying tasks:

| Robot | Price Point | Marketplace Role | Operator Profile |
|-------|-------------|------------------|------------------|
| **DJI Matrice 350 RTK + Zenmuse L2** | ~$29,300 (combo) | Topographic survey, volumetrics, progress monitoring | Regional drone service operators (Part 107 licensed) |
| **DJI Matrice 4E** | ~$8,000-10,000 | Rapid mapping for smaller sites, photo documentation | Solo operators, lower-cost option for simple surveys |
| **Skydio X10** | ~$20,000-30,000 | Autonomous structure inspection, thermal analysis | Infrastructure inspection specialists |
| **Boston Dynamics Spot** | $74,500-195,000 | Site walkthroughs, digital twins, GPR subsurface surveys | Construction technology firms, larger operators |
| **Spot + Leica BLK ARC** | ~$120,000-160,000 | Autonomous interior/exterior LiDAR scanning | Survey companies adding robotic capabilities |
| **Leica BLK2FLY** | ~$40,000-60,000 | Autonomous aerial LiDAR (high-accuracy topo) | Geospatial firms with existing Leica workflows |
| **Flyability ELIOS 3** | ~$50,000-80,000 | Confined-space inspection (box culverts, tunnels) | Specialized inspection operators |

67% of major US construction firms already use drones on projects, and 45% of civil contractors specifically. The supply side exists -- it is just fragmented across hundreds of regional operators with no aggregation layer. None of the major robot inspection companies (Gecko, Flyability, Skydio, Boston Dynamics) operate an open marketplace. The industry standard is either buy the robot and operate it yourself, or hire the company for a contracted inspection. There is no "Uber for robots" yet. The marketplace is that missing aggregation layer, and the RaaS market ($28.5B in 2024, growing 17.9% CAGR toward $76.6B by 2030) confirms the industry is moving from CapEx to OpEx -- exactly the shift a marketplace serves.

## Path to Moon

Construction site surveying is not a metaphor for lunar operations -- it is a direct technical precursor. The Artemis program requires site preparation for landing pads, habitat foundations, and regolith processing facilities at the lunar south pole. Every task Marco hires robots for has a lunar analog:

| Marco's Job (Earth) | Kenji's Job (Moon) | What Transfers |
|---|---|---|
| Topographic survey of highway corridor | Terrain mapping of Shackleton Crater rim for pad siting | LiDAR point cloud pipeline, DTM generation, volumetric analysis |
| Existing condition documentation | Characterization of boulder fields and crater morphology | 3D photogrammetry, anomaly detection, obstacle mapping |
| Subsurface assessment via GPR | Regolith depth and ice concentration profiling for ISRU | Ground-penetrating radar data processing, subsurface modeling |
| Progress monitoring (monthly cut/fill) | Tracking autonomous excavation and sintering of landing pads | Temporal baseline comparison, volumetric change detection |
| As-built verification for client handoff | Confirming habitat foundation meets structural specs before pressurization | Design-vs-actual deviation analysis, BIM compliance checking |

The sensor stack transfers directly. LiDAR works in vacuum -- in fact, it works better without atmospheric scattering. RTK-GPS is replaced by lunar positioning beacons (NASA's LunaNet). Thermal imaging is critical for managing the -173C to +127C surface temperature swing. Drones do not fly on the Moon (no atmosphere), but the Lunar Outpost MAPP rover (10-250 kg variants, stereo cameras, LiDAR/ToF, thermal) fills that role -- and it is structurally identical to a Spot with survey payloads.

The software layer transfers completely. A marketplace task like "survey 500m corridor at Shackleton Ridge" runs through the same auction engine, agent orchestration, ERC-8004 identity/reputation system, and deliverable pipeline as "survey 500m highway corridor in Flagstaff." The processing algorithms -- point cloud classification, terrain modeling, volumetric computation, deviation analysis -- are environment-agnostic. The agent's ability to translate a business need into robot task specs, evaluate bids, sequence multi-robot missions, and deliver structured reports works identically whether the buyer is Marco in Phoenix or Kenji at JAXA mission control.

The strategic sequencing:

```
Year 1:  Construction surveying -- prove marketplace model, build robot supply, sign 10 GC customers
Year 2:  + Mining/quarrying -- same robots, same sensors, new buyer persona, dust-hardened ops
Year 3:  + Infrastructure -- add bridge crawlers, confined-space platforms, federal contracts
Year 4+: Lunar contracts -- NASA/commercial ISRU site prep, Artemis base construction support
```

By Year 4, the platform has a proven auction engine, a trained agent layer, a supply network of autonomous survey robots, and a reputation system with thousands of completed tasks. The software, the workflows, and the operator network all transfer directly to lunar program contracts. The path from Marco to Kenji is not a pivot. It is a graduation.

## The User Story (v0.1)

Meet Marco Reyes, senior estimator at Granite Basin Civil in Phoenix. It is Tuesday morning, March 10, 2026. Marco just received an RFP for a 3.2-mile highway widening project on SR-89A north of Sedona. The Arizona DOT wants to add a climbing lane through the switchbacks. Bid deadline: March 21, eleven days out. Marco needs site survey data to price earthwork, and his usual survey crew -- Desert Sun Surveying -- is booked solid on a Tucson interchange project until April.

He calls Desert Sun anyway. "Earliest I can get you a crew is April 2nd," they say. "And turnaround on processed data is five to six business days after that." That puts data in Marco's hands on April 10 -- twenty days after the bid deadline. Not an option.

Marco opens the marketplace agent in his browser and types: "I need topo and existing conditions for a highway widening bid. SR-89A, milepost 355 to 358.2, about 3.2 miles. Need cut/fill-ready terrain data and photo documentation of existing drainage structures and retaining walls. Bid is due March 21, so I need processed data no later than March 17."

The agent responds in 45 seconds. It has geocoded the corridor limits from ADOT's milepost system, estimated the survey area at 120 acres (accounting for the winding alignment and 200-foot offset buffers), and identified two task requirements: (1) aerial LiDAR topographic survey for earthwork quantities, and (2) low-altitude structure documentation with visual + thermal imaging for existing condition verification. It presents a scope summary and asks Marco to confirm and set a budget ceiling.

Marco reviews the scope and replies: "That looks right. Budget up to $4,500 for both. And flag anything that looks like it will complicate the cut -- I know there is rock outcrop in that section."

The agent posts two parallel tasks to the marketplace at 9:15 AM MST, specifying sensor requirements, deliverable formats, and the March 15 data deadline. By 11:30 AM, three drone operators have bid on the topo survey: SkyView Mapping at $2,200, Desert Hawk Geo at $2,600, and Prescott UAV Services at $1,800. Two operators have bid on the structure documentation: RedRock Aerial at $1,400 and SkyView (bundled) at $1,900.

The agent evaluates bids on three axes: capability match (does the operator's equipment meet the sensor spec?), reputation (completion rate, accuracy scores from past tasks), and price. It recommends SkyView Mapping for topo ($2,200 -- 4.8 stars, 47 completed construction surveys, Matrice 350 RTK + Zenmuse L2) and RedRock Aerial for documentation ($1,400 -- 4.6 stars, 31 completions, Skydio X10 with FLIR thermal).

Total: $3,600. That is 58% less than Desert Sun's typical $8,500 quote for the same corridor, and the data will arrive eight days sooner.

Marco approves both with one click. The agent coordinates schedules: SkyView will fly the corridor Thursday March 13 (weather window confirmed via NOAA API -- clear skies, winds under 12 mph), and RedRock will document structures on Friday March 14. Both operators acknowledge and confirm equipment readiness through the marketplace.

On March 13, SkyView's pilot launches the Matrice 350 from a pulloff at milepost 355. The drone flies the corridor in 3.5 hours across two battery swaps, capturing 4.2 million LiDAR points per second and 20MP RGB imagery at 2-second intervals. Raw data uploads to the marketplace cloud by 4 PM.

On March 14, RedRock flies the Skydio X10 along the alignment at low altitude, autonomously orbiting and documenting all 22 drainage structures, 3 retaining walls, and 8 culvert headwalls. Thermal imaging flags two culverts with apparent subsurface water flow. Raw data uploads by 3 PM.

The agent processes overnight. Point cloud classification, terrain model generation, orthomosaic stitching, and structure annotation run through the marketplace's processing pipeline. By 8 AM on March 15 -- a Saturday, because software does not take weekends off -- Marco has in his inbox:

- A LandXML digital terrain model ready for direct import into HeavyBid
- Cross-sections at 50-foot stations along the centerline, in CSV
- A 2-inch resolution orthomosaic of the full corridor in GeoTIFF
- A drainage structure photo catalog: 33 structures, GPS-tagged, condition-rated, with thermal overlays where anomalies were detected
- A summary report flagging two areas where existing ground sits 4+ feet above design grade (heavy cut zones, one with probable rock based on LiDAR return intensity) and two culverts that may need upsizing based on thermal water flow signatures

Marco spends Saturday morning importing the terrain model into HeavyBid. The earthwork quantity takeoff, which usually takes two full days working from survey crew field books, takes four hours because the data is already in the right coordinate system and format. He identifies 340,000 cubic yards of cut (including an estimated 45,000 CY of rock excavation in the flagged zone) and prices the bid at $14.2M.

On March 21, Granite Basin submits the bid -- on time, with quantities Marco trusts. On April 3, ADOT notifies them: they won.

Marco's first message back to the marketplace agent: "We got SR-89A. Set up monthly progress monitoring flights starting May 1, same corridor, same LiDAR specs. I need cut/fill volumes compared to the March 15 baseline for each pay application. Run it through closeout."

The agent creates a recurring monthly task. It stores the pre-bid terrain model as the volumetric baseline. Each month, it auto-posts the monitoring task, evaluates bids from available operators, dispatches the flight, processes the data, and delivers a progress report showing cumulative earthwork quantities, percent complete by station, and schedule variance -- formatted for direct attachment to Granite Basin's monthly pay application to ADOT.

Over the 14-month construction duration, Granite Basin spends roughly $28,000 in marketplace survey fees (the pre-bid surveys plus 14 monthly monitoring flights). A dedicated survey crew on retainer for the same scope would have cost $90,000 or more. Marco saved $62,000 in direct costs, won a bid he would have missed entirely, and never once thought about what kind of robot was flying over his project.

That is the point. Marco does not hire robots. He hires site data. The marketplace is just how it shows up -- faster, cheaper, and already formatted for his tools.

---

## Cost Summary

| Phase | Human Crew | Marketplace | Savings |
|---|---|---|---|
| Pre-bid topo survey (100-acre corridor) | $8,000-10,000 | $1,500-3,000 | 60-80% |
| Existing condition documentation | $3,000-5,000 | $2,000-4,000 | 20-50% |
| Subsurface GPR assessment | $5,000-15,000 | $3,000-6,000 | 40-60% |
| Monthly progress monitoring (per flight) | $4,000-6,000 | $1,000-2,000 | 67-75% |
| As-built verification | $10,000-15,000 | $4,000-8,000 | 47-60% |
| **Full project lifecycle (14 months)** | **~$90,000+** | **~$28,000** | **~69%** |

The savings come from three sources: faster robotic data capture (hours vs. days of field work), automated agent processing (algorithm vs. junior engineer spending two days on data cleanup), and competitive auction pricing (market-discovered rates vs. vendor rate cards). But the speed advantage is often more valuable than the cost advantage. Marco's real ROI is not the $62K saved on survey fees over 14 months -- it is the $14.2M contract he won because he had data in time to bid. The marketplace does not just reduce cost. It removes the scheduling bottleneck that prevents Granite Basin from bidding on every opportunity in their pipeline.

---

*This document synthesizes findings from the industry analysis, marketplace justification, and robots/sensors research to answer the senior PM's core question: what would a robot actually be hired for? The answer is not "sensor readings." It is "winning a highway bid before Thursday."*
