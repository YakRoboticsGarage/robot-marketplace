# Wedge Industry Analysis: First Market for Robot Task Auction Marketplace

**Date:** 2026-03-27
**Purpose:** Evaluate 8 candidate verticals, recommend top 3 wedge industries.
**Constraint:** First Earth industry must transfer credibly to lunar construction ops.

---

## 1. Construction Site Surveying

**Sub-industry:** Pre-bid site surveys for civil/heavy construction (highway, bridge, commercial).
**Buyer persona:** Estimator or project manager at a GC or civil engineering firm (ENR Top 400).

**Jobs-to-be-done:**
1. Capture topographic data (elevation, grade, contours) to feed bid estimation software.
2. Verify existing infrastructure (utilities, drainage) against plan documents before mobilization.
3. Generate progress monitoring reports (cut/fill volumes, schedule conformance) for owner billing.
4. Produce as-built verification scans at project closeout for handoff to facility owner.
5. Perform soil density / bearing capacity spot-checks at designated test points.

**Sensors / capabilities:** LiDAR, RTK-GPS, photogrammetry camera, ground-penetrating radar (GPR), IMU, autonomous navigation over unstructured terrain, dust/weather resilience.

**Market size:** U.S. construction surveying services ~$8B/yr. Pre-bid surveys alone represent ~15% ($1.2B). GCs pay survey crews $2-5K per site visit; a single large highway bid may require 3-5 visits.

**Why marketplace > direct partnership:** GCs bid on dozens of projects per quarter across geographies. They cannot own robots in every metro. A marketplace gives on-demand access to the nearest capable robot, with competitive pricing. Multi-vendor supply also prevents single-vendor lock-in on a critical-path activity.

**Why agent mediation adds value:** An AI agent converts raw point clouds and imagery into structured deliverables (cut/fill reports, BIM-compatible models, bid-ready data packages). Agents can also schedule recurring progress scans automatically, match task specs to robot capabilities, and flag discrepancies vs. design intent.

**Path to lunar:** Direct. Lunar construction (Artemis base, regolith pads) requires site surveying, terrain mapping, and progress monitoring in unstructured, dusty, GPS-denied environments. Every sensor and workflow transfers. NASA and commercial lunar programs (Blue Origin, SpaceX) will need exactly these capabilities.

---

## 2. Insurance Inspections

**Sub-industry:** Commercial property condition assessments and post-disaster damage surveys.
**Buyer persona:** Claims adjuster, underwriting engineer, or risk manager at a P&C carrier.

**Jobs-to-be-done:**
1. Photograph and measure roof condition for policy renewal underwriting.
2. Assess post-storm/fire/flood structural damage for claims processing.
3. Generate 3D models of damaged properties for litigation support.
4. Perform periodic condition monitoring on high-value insured assets (warehouses, solar farms).

**Sensors / capabilities:** High-res camera (visual + thermal), LiDAR for dimensional accuracy, weather-resistant airframe or ground platform, AI-driven damage classification.

**Market size:** U.S. P&C inspection market ~$3B/yr. Carriers spend $300-800 per property inspection; post-catastrophe surge demand can 10x volume in affected regions.

**Why marketplace > direct partnership:** Demand is geographically unpredictable (catastrophe-driven). Carriers need surge capacity in disaster zones within 24-48 hours. No single robotics vendor can cover every geography; a marketplace aggregates supply where and when it is needed.

**Why agent mediation adds value:** Agents structure raw imagery into standardized damage reports (IICRC categories, Xactimate-compatible estimates). They auto-triage severity, flag fraud indicators, and route high-severity claims for priority handling. This turns a 5-day manual process into hours.

**Path to lunar:** Moderate. Structural inspection skills transfer to habitat integrity monitoring. Thermal and visual inspection of pressurized modules, landing pads, and equipment is critical for lunar base safety. However, the insurance-specific business logic does not transfer.

---

## 3. Infrastructure Monitoring

**Sub-industry:** Bridge deck and structural inspection for state DOTs and transportation authorities.
**Buyer persona:** Bridge program manager at a state DOT or engineering consultant under DOT contract.

**Jobs-to-be-done:**
1. Conduct biennial bridge deck condition surveys (NBI compliance) without lane closures.
2. Inspect under-bridge structural elements (bearings, abutments, steel fatigue cracks).
3. Survey pipeline rights-of-way for encroachment, leak indicators, and coating degradation.
4. Patrol power transmission corridors for vegetation encroachment and insulator damage.
5. Generate condition-rated inventory databases for capital planning.

**Sensors / capabilities:** High-res camera, thermal IR, LiDAR, ultrasonic thickness gauge, magnetometer (rebar detection), ability to climb or fly in confined structural spaces, beyond-visual-line-of-sight (BVLOS) operation.

**Market size:** U.S. bridge inspection alone ~$1.5B/yr (600K+ bridges, federally mandated). Pipeline integrity management ~$4B/yr. Total addressable: $6-8B.

**Why marketplace > direct partnership:** DOTs and utilities manage assets spread across thousands of miles. Inspection windows are seasonal and weather-dependent. A marketplace lets agencies procure the right robot type for each asset class (crawler for bridge, drone for power line) without fleet ownership.

**Why agent mediation adds value:** Agents map inspection findings to federal condition rating scales (NBI, SNBI), auto-populate FHWA reporting templates, and flag elements trending toward critical condition. For pipelines, agents correlate inspection data with PHMSA compliance requirements.

**Path to lunar:** Strong for structural inspection (habitat modules, landing pads, excavation sites). Weak for the regulatory framework. The physical inspection skills and autonomous navigation in constrained spaces transfer well.

---

## 4. Environmental Compliance

**Sub-industry:** Emissions monitoring and water quality sampling for industrial permit compliance.
**Buyer persona:** EHS (Environment, Health & Safety) director at a manufacturing plant or energy facility.

**Jobs-to-be-done:**
1. Conduct fence-line emissions monitoring per EPA Method 21 or optical gas imaging requirements.
2. Sample and test water discharge quality at permitted outfall points.
3. Monitor construction site stormwater BMPs for NPDES permit compliance.
4. Survey protected habitat areas for endangered species presence before construction.

**Sensors / capabilities:** Gas analyzers (VOC, methane, H2S), water quality probes (pH, DO, turbidity, metals), optical gas imaging camera, GPS-tagged sample collection, all-weather ground mobility.

**Market size:** U.S. environmental compliance services ~$5B/yr. Facility monitoring specifically ~$1.5B. Penalties for non-compliance create strong willingness to pay.

**Why marketplace > direct partnership:** Facilities need periodic (quarterly, event-triggered) monitoring, not continuous robot presence. Different compliance tasks require different sensor packages. A marketplace matches the right instrumented robot to each monitoring event.

**Why agent mediation adds value:** Agents auto-generate regulatory submission documents (DMRs, emissions reports), compare readings against permit thresholds in real-time, and alert operators before violations occur. They maintain chain-of-custody records for legal defensibility.

**Path to lunar:** Moderate. Life support system monitoring (air quality, water recycling) on a lunar base has structural similarity. Sensor calibration and environmental data pipelines transfer. But Earth regulatory frameworks do not exist on the Moon.

---

## 5. Real Estate

**Sub-industry:** Commercial property due diligence inspections and listing media.
**Buyer persona:** Commercial real estate broker, institutional investor, or property manager.

**Jobs-to-be-done:**
1. Capture marketing-grade aerial and interior photography for listings.
2. Produce accurate floor plans and square footage measurements for lease verification.
3. Generate pre-acquisition condition reports for due diligence.
4. Monitor vacant property condition between tenants.

**Sensors / capabilities:** High-res camera (photo + video), LiDAR for measurement, 360-degree capture, indoor navigation capability.

**Market size:** U.S. CRE inspection/media services ~$2B/yr. Residential adds ~$3B but is fragmented and price-sensitive.

**Why marketplace > direct partnership:** Brokers and investors deal with properties across markets. They need local robot operators wherever the property is, on short notice. Marketplace aggregation solves the geographic coverage problem.

**Why agent mediation adds value:** Agents produce standardized property reports, auto-compare measurements against lease abstracts, flag maintenance issues, and generate marketing-ready media packages with minimal human editing.

**Path to lunar:** Weak. The skills (photography, measurement) are basic and ubiquitous. No unique transfer to lunar ops. Business context is entirely Earth-bound.

---

## 6. Agriculture

**Sub-industry:** Precision ag scouting for row-crop operations.
**Buyer persona:** Agronomist or farm operations manager at a 2,000+ acre operation.

**Jobs-to-be-done:**
1. Generate multispectral crop health maps (NDVI) for variable-rate input decisions.
2. Scout for pest/disease presence and quantify infestation boundaries.
3. Measure soil moisture and compaction at grid-sampled points.
4. Assess irrigation system performance (uniformity, leak detection).

**Sensors / capabilities:** Multispectral/hyperspectral camera, thermal IR, soil probes, weather station, RTK-GPS, long-endurance flight or ground traversal over soft terrain.

**Market size:** U.S. precision ag services ~$4B/yr growing 12% annually. Farmers pay $5-15/acre for scouting services.

**Why marketplace > direct partnership:** Seasonal demand (planting, mid-season, harvest windows). Farmers want results, not robot ownership. Different crop types need different sensing (thermal for irrigation, multispectral for health). Marketplace matches the right tool to each scouting mission.

**Why agent mediation adds value:** Agents convert raw spectral data into prescription maps compatible with John Deere Operations Center or Climate FieldView. They correlate multi-temporal scans to trend crop stress, recommend input adjustments, and auto-schedule follow-up scans.

**Path to lunar:** Moderate-to-strong for future lunar agriculture (controlled environment agriculture in habitats). Soil/substrate analysis and plant health monitoring will be needed. But the timeline is long and the operating environment radically different.

---

## 7. Mining / Quarrying

**Sub-industry:** Open-pit volumetric surveys and safety compliance inspections.
**Buyer persona:** Mine surveyor or safety officer at an aggregate/mineral extraction operation.

**Jobs-to-be-done:**
1. Conduct volumetric stockpile surveys for inventory management and royalty calculations.
2. Map blast patterns and assess fragmentation results post-detonation.
3. Inspect highwalls and bench faces for stability risks (MSHA compliance).
4. Survey haul road conditions and grade for fleet optimization.
5. Monitor tailings dam structural integrity.

**Sensors / capabilities:** LiDAR, photogrammetry, thermal IR, GPS/RTK, dust-hardened chassis, ability to operate in blast exclusion zones, autonomous navigation on rough terrain.

**Market size:** U.S. mining survey services ~$1.5B/yr. Global mining tech spend ~$8B with strong automation tailwinds. Operators pay $5-20K per volumetric survey.

**Why marketplace > direct partnership:** Mining operations are geographically remote and distributed. Operators run multiple pit faces and stockpile areas. Survey demand is periodic but critical for financial reporting. A marketplace provides access to survey-capable robots without the overhead of maintaining specialized equipment at every site.

**Why agent mediation adds value:** Agents auto-compute volumetric changes between surveys, generate MSHA-formatted safety reports, predict highwall failure risk from trend data, and reconcile survey volumes against truck-scale tonnage for inventory accuracy.

**Path to lunar:** Very strong. Lunar regolith mining (ice extraction at poles, construction material processing) is a NASA-funded priority. Volumetric surveying, terrain assessment, autonomous navigation over unstructured regolith, dust-hardened operations -- these are near-identical to open-pit mining on Earth. The ISRU (In-Situ Resource Utilization) programs at NASA and commercial partners need exactly these capabilities.

---

## 8. Facilities Management

**Sub-industry:** Commercial building compliance inspections (HVAC, fire, electrical).
**Buyer persona:** Facilities director at a corporate campus, hospital system, or property management firm.

**Jobs-to-be-done:**
1. Conduct HVAC performance verification and energy audit scans.
2. Perform fire safety equipment inspection (sprinkler, alarm, extinguisher inventory).
3. Assess building envelope condition (thermal bridging, moisture intrusion).
4. Generate ADA compliance surveys for accessibility renovations.

**Sensors / capabilities:** Thermal IR camera, air quality sensors (CO2, particulates), humidity/temperature probes, visual camera, indoor navigation (SLAM), compact form factor for hallways and mechanical rooms.

**Market size:** U.S. building inspection and compliance services ~$3B/yr. Recurring revenue model (annual/quarterly inspections).

**Why marketplace > direct partnership:** Property managers oversee portfolios of diverse buildings. Each inspection type requires different sensor loadouts. The marketplace matches the right robot to each building and compliance requirement.

**Why agent mediation adds value:** Agents map findings to code requirements (NFPA, ASHRAE, ADA), auto-generate deficiency reports with remediation cost estimates, and schedule follow-up inspections. They maintain compliance calendars across building portfolios.

**Path to lunar:** Moderate for habitat systems monitoring. Life support, thermal management, and structural integrity inspection in pressurized modules have overlap. But Earth building codes are irrelevant on the Moon.

---

## Comparative Scoring Matrix

| Criterion (weight)                  | Construction | Insurance | Infrastructure | Environ. | Real Estate | Agriculture | Mining | Facilities |
|-------------------------------------|:-----------:|:---------:|:--------------:|:--------:|:-----------:|:-----------:|:------:|:----------:|
| Lunar transfer (30%)                |     5       |     2     |       3        |    2     |      1      |      2      |   5    |     2      |
| Market size & willingness to pay (20%) |  4       |     4     |       4        |    3     |      3      |      4      |   3    |     3      |
| Marketplace advantage (15%)         |     4       |     5     |       4        |    3     |      4      |      3      |   3    |     3      |
| Agent mediation value (15%)         |     4       |     4     |       4        |    4     |      3      |      4      |   4    |     4      |
| Existing robot readiness (10%)      |     4       |     4     |       3        |    3     |      4      |      4      |   3    |     3      |
| Regulatory tailwind (10%)           |     3       |     3     |       5        |    4     |      2      |      3      |   4    |     3      |
| **Weighted total**                  |   **4.25**  |  **3.35** |    **3.65**    | **2.90** |   **2.45**  |   **3.10**  |**3.95**|  **2.80**  |

---

## Ranked Recommendation: Top 3

### #1: Construction Site Surveying (Score: 4.25)

**The strongest wedge.** It directly addresses the founder's own example (pre-bid highway survey), has the clearest lunar transfer path, and targets buyers with real budget authority who already spend $2-5K per site visit on survey crews. The JTBD are concrete and quantifiable: faster bid turnaround, lower survey cost, higher data fidelity. Every sensor and autonomy capability needed for construction surveying (LiDAR, RTK-GPS, rough-terrain nav, dust tolerance) maps directly to lunar surface operations. The marketplace model works because GCs bid on projects across geographies and need on-demand, local robot access. Agent mediation converts raw sensor data into bid-ready deliverables, which is the actual value the buyer pays for.

**Start here.** The first 10 customers are estimators at mid-size civil GCs ($50-500M revenue) preparing highway and commercial site bids.

### #2: Mining / Quarrying (Score: 3.95)

**The strongest lunar transfer after construction.** Open-pit mining operations are the closest Earth analog to lunar ISRU: unstructured terrain, dust, volumetric measurement, autonomous navigation, and remote/hostile environments. The buyer persona (mine surveyor) has budget and recurring need. The limitation is smaller addressable market and more geographically concentrated operations, which weakens the marketplace network effect compared to construction. However, mining operators are sophisticated technology adopters, and the data-to-decision pipeline (volumetric survey to inventory/safety report) is well-suited to agent mediation.

**Second market after construction traction is proven.** Many capabilities (LiDAR scanning, terrain nav, dust hardening) overlap, allowing robot supply-side to serve both verticals.

### #3: Infrastructure Monitoring (Score: 3.65)

**Strongest regulatory tailwind.** Federal bridge inspection mandates (23 CFR 650) and pipeline safety rules (49 CFR 192/195) create non-discretionary demand. DOTs must inspect 600K+ bridges biennially. The marketplace model is strong because assets are geographically dispersed and inspection windows are constrained. Agent mediation maps findings to federal reporting standards, saving engineers hours of manual data entry. Lunar transfer is moderate -- structural inspection of habitats and landing pads is relevant, but the specific regulatory context does not carry over. This vertical also requires more specialized robot form factors (bridge crawlers, confined-space platforms) that may slow initial supply aggregation.

**Third market, or a parallel play if a DOT pilot opportunity arises.** The federal mandate creates a reliable demand floor.

---

## Strategic Sequencing

```
Year 1:  Construction surveying — prove marketplace model, build robot supply
Year 2:  + Mining/quarrying — extend same robots, same sensors, new buyer persona
Year 3:  + Infrastructure — add specialized form factors, federal contracts
Year 4+: Lunar contracts — NASA/commercial ISRU and construction site prep
```

This sequence maximizes sensor/capability reuse across verticals, builds the supply side efficiently, and creates a credible narrative from Earth construction through mining to lunar surface operations.
