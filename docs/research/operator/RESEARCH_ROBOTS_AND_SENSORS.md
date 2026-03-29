# Robots and Sensors for Construction/Infrastructure Inspection Marketplace

Research date: 2026-03-27

---

## 1. Robots Currently Used in Construction Surveying

### Aerial Platforms (Drones)

| Robot | Role | Key Specs | Price (USD) |
|-------|------|-----------|-------------|
| **DJI Matrice 350 RTK** | Large-scale mapping, multi-payload | 55 min flight, IP55, centimeter RTK, triple payload mount | ~$14,800 (combo) |
| **DJI Matrice 4E** | Rapid mapping/surveying | Mechanical shutter, 0.5s interval, laser rangefinder | ~$8,000-10,000 |
| **Skydio X10** | Autonomous inspection | 6x 32MP nav cams, 50MP wide + 64MP narrow, FLIR Boson+ 640x512 thermal, NightSense, GPS-denied flight, 40 min, IP55 | ~$20,000-30,000 (est.) |
| **Flyability ELIOS 3** | Confined-space inspection | Collision-tolerant cage, LiDAR SLAM, indoor 3D mapping | ~$50,000-80,000 (est.) |
| **Leica BLK2FLY** | Autonomous flying LiDAR | 420K pts/sec, 5-camera SLAM, GNSS, 20mm relative accuracy | ~$40,000-60,000 (est.) |

### Ground Platforms

| Robot | Role | Key Specs | Price (USD) |
|-------|------|-----------|-------------|
| **Boston Dynamics Spot** | Site walkthrough, digital twin, progress monitoring | Quadruped, all-terrain, hot-swappable payloads, 90 min runtime | $74,500 base; $100K-195K fully equipped |
| **Spot + Leica BLK ARC** | Autonomous interior scanning | LiDAR SLAM on Spot, static + mobile scans in one mission | ~$120,000-160,000 combined |
| **Gecko Robotics TOKA 4** | Wall-climbing UT inspection | Magnetic wheels, 24-32 UT sensors, 1080p camera, 9 m/min | Service: $50K-100K per deployment |

### Key Payloads / Sensors Sold Separately

| Sensor | Mounts On | Specs | Price |
|--------|-----------|-------|-------|
| **DJI Zenmuse L2** (LiDAR) | Matrice 350/300 | 5 cm H / 4 cm V accuracy @ 150m, 20MP RGB | $14,500 |
| **DJI Zenmuse H30T** (multi) | Matrice 350 | Wide + zoom + thermal + laser rangefinder | ~$16,000 |
| **Spot LiDAR add-on** | Spot | 360-degree mapping | ~$18,450 |
| **Spot Inspection Camera** | Spot | PTZ + thermal | ~$29,750 |
| **Spot Arm** | Spot | Manipulation, door opening, sample collection | ~$25,000 |

---

## 2. Sensors Required for Construction/Infrastructure Inspection

| Sensor Type | What It Measures | Typical Accuracy | Use Case |
|-------------|-----------------|------------------|----------|
| **RGB Photogrammetry** | 2D orthomosaics, 3D models | 1 cm H, 3 cm V RMS | Progress tracking, volumetrics, as-builts |
| **LiDAR (airborne)** | Dense 3D point clouds | 2-5 cm absolute | Topographic surveys, digital twins, BIM overlay |
| **LiDAR (terrestrial)** | Interior / structural geometry | 1-2 mm at short range | As-built verification, deformation monitoring |
| **Ground Penetrating Radar (GPR)** | Subsurface utilities, rebar, voids | Depth-dependent | Utility locating, concrete imaging, bridge deck assessment |
| **Thermal / IR** | Surface temperature differentials | +/- 2 deg C typical | Insulation defects, water infiltration, electrical hot spots, delamination |
| **Ultrasonic Thickness (UT)** | Steel wall thickness / corrosion | 0.1 mm resolution | Tank/pipe/boiler wall thinning, bridge steel members |
| **Eddy Current** | Surface and near-surface cracks in metal | Sub-mm crack detection | Weld inspection, fatigue crack detection |
| **GMR Sensor Array** | Corrosion and cracks in steel | Magnetic field mapping | Steel bridge decks, pipelines |
| **Gas Detection** | CH4, CO, H2S, VOCs | ppm-level | Confined space pre-entry, pipeline leak detection |
| **Multispectral / NDVI** | Vegetation health, moisture | Band-specific | Erosion assessment, drainage path identification |

Multi-sensor drone platforms combining RGB + thermal + LiDAR reduce inspection time by ~67% and improve defect detection by ~43% vs. single-sensor approaches.

---

## 3. Highway Bid Measurement Tasks (What a Civil Engineer Actually Needs)

A typical highway project bid requires these deliverables, each mappable to a robot task:

| Task | Traditional Method | Robot Method | Deliverable |
|------|-------------------|--------------|-------------|
| **Topographic survey** | 2-person crew + total station, 3-5 days | Drone photogrammetry or LiDAR, 3-4 hours on-site | Contour map, DTM, cross-sections |
| **Existing condition survey** | Manual walkthrough + photos | Spot or drone 3D scan | As-built model, defect catalog |
| **Soil / geotechnical** | Drill rigs, lab testing, 1.5-3.0m depth | GPR for subsurface imaging (non-destructive) | Soil profile, bearing capacity est. |
| **Drainage assessment** | Manual watershed delineation | LiDAR-derived flow accumulation model | Drainage map, culvert sizing |
| **Utility locating** | GPR + EM hand-pushed carts | Robot-mounted GPR (Spot + GPR payload) | Utility map with depth |
| **Traffic count** | Pneumatic tube counters, 48-72 hrs | AI camera + edge compute (not a robot task) | AADT, turning movements |
| **Pavement condition** | Visual + FWD testing | Drone thermal + LiDAR crack detection | PCI scoring, distress map |
| **Right-of-way survey** | Licensed surveyor + monuments | RTK drone for boundary confirmation | Legal plat support data |

---

## 4. Bridge Inspection Robot Requirements

Bridge inspections (NBIS / FHWA) require access to every structural member. Robot needs:

| Capability | Sensor / System | Why |
|------------|----------------|-----|
| **Visual defect detection** | 4K+ camera, AI crack detection (>0.3mm) | Section loss, spalling, efflorescence |
| **Crack measurement** | High-res camera + calibrated AI | Quantify crack width, length, progression |
| **Corrosion mapping** | UT phased array, GMR sensor, eddy current | Steel thickness loss, section rating |
| **Concrete delamination** | Thermal camera, chain drag equivalent (impact-echo) | Deck condition, overlay decisions |
| **Scour assessment** | Sonar / bathymetry (underwater) | Foundation stability |
| **Load response** | Strain gauges, accelerometers, displacement sensors | Load rating verification |
| **Under-deck access** | Climbing robot (magnetic) or caged drone | Replace snooper trucks ($2K-5K/day) |

Current approach: Skydio X10 or DJI Matrice for external/deck, Flyability ELIOS for box girders and confined cells, Gecko-style magnetic climber for steel members. AI cloud analysis identifies cracks >0.3mm and thermal anomalies indicating subsurface delamination.

---

## 5. Cost Comparison: Human Crews vs. Robots

### Site Survey (100-acre highway corridor)

| Method | Time | Labor Cost | Equipment | Total |
|--------|------|------------|-----------|-------|
| **2-person survey crew** | 5-6 days | ~$7,200 ($75/hr loaded) | Total station, GPS rover | ~$8,000-10,000 |
| **Drone photogrammetry** | 3-4 hours on-site | ~$800 | DJI Matrice 4E | ~$1,500-3,000 |
| **Drone LiDAR** | 3-4 hours on-site | ~$800 | Matrice 350 + Zenmuse L2 | ~$3,000-5,000 |

### Per-Acre Service Pricing (drone-as-a-service)

| Service | Cost/Acre |
|---------|-----------|
| Photogrammetry (small site <50 acres) | $150-300/acre |
| Photogrammetry (large site >500 acres) | $1.50-4/acre |
| LiDAR (small site) | $150-500/acre |
| LiDAR (large site) | $4-30/acre |

### Industrial Inspection

| Task | Traditional | Robot | Savings |
|------|-------------|-------|---------|
| Tank internal inspection | $50K-100K (scaffolding + confined entry) | $15K-25K (Flyability ELIOS) | 70-80% |
| Boiler wall UT survey | Multi-day outage + rope access | Gecko TOKA: 1 shift, $50K-100K | Time savings 60-80% |
| Bridge under-deck | Snooper truck $2K-5K/day, 5+ days | Drone: $3K-8K total | 50-70% |

Adoption: 67% of major US construction firms and 45% of civil contractors used drones on projects as of 2024.

---

## 6. Commercial Robot Inspection Companies

| Company | Robot/Platform | Specialization | Business Model | Pricing |
|---------|---------------|----------------|----------------|---------|
| **Gecko Robotics** | TOKA 3/4/Flex wall climbers, StratoSight drone | Industrial assets: boilers, tanks, pipelines | Multi-year service contracts + Cantilever SaaS platform | $50K-100K per deployment |
| **Flyability** | ELIOS 3 | Confined spaces: tanks, mines, tunnels | Hardware sale + inspection services | Hardware ~$50K-80K; saves $15K/tank inspection |
| **Skydio** | X10, X10D, R10 | Infrastructure, construction, public safety | Hardware + Skydio Cloud SaaS | Enterprise pricing |
| **Boston Dynamics** | Spot | Construction digital twins, facility monitoring | Hardware sale + annual SW licenses ($3,600+/yr) | $75K-195K per unit |
| **Leica/Hexagon** | BLK2FLY, BLK ARC | Autonomous laser scanning | Hardware sale | $40K-60K per unit |
| **Zipline** | P2 delivery drones | Medical/logistics delivery | On-demand delivery fees | Per-delivery pricing |
| **DJI Enterprise** | Matrice series | Mapping, survey, inspection | Hardware + DJI FlightHub SaaS | $8K-30K per system |

None of these operate a true open marketplace model. Gecko comes closest with service contracts. The industry standard is either (a) buy the robot and operate it yourself, or (b) hire the company for a contracted inspection. There is no "Uber for robots" yet -- which is exactly the gap this marketplace fills.

---

## 7. ERC-8004 and MCP Compatibility

### ERC-8004 (Ethereum, live since Jan 2026)

ERC-8004 provides on-chain identity, reputation, and validation registries for autonomous agents. Three registries:
1. **Identity Registry** -- ERC-721 NFT handle resolving to agent registration file
2. **Reputation Registry** -- bounded scores + categorical tags (response time, uptime, accuracy)
3. **Validation Registry** -- hooks for stakers, zkML verifiers, TEE oracles

Direct applicability to marketplace: each robot operator mints an agent identity, accumulates reputation per completed task, and validators can independently verify deliverable quality.

**No existing inspection robot company has adopted ERC-8004 yet.** This is greenfield.

### MCP (Model Context Protocol)

MCP (Anthropic, donated to Linux Foundation AAIF Dec 2025) is the de facto standard for connecting AI systems to external tools. 6,400+ registered MCP servers as of Feb 2026. Robotics integration path: robots expose MCP tool interfaces for mission planning, sensor data retrieval, and status reporting. AI agents orchestrate multi-robot missions via MCP.

**No inspection robot currently exposes an MCP interface.** Another greenfield opportunity. A marketplace MCP server could let an AI agent: discover available robots, request bids, dispatch missions, and retrieve deliverables.

---

## 8. Lunar Path: Which Robots Could Operate on the Moon?

| Earth Robot | Lunar Modification Needed | Lunar Analog |
|-------------|--------------------------|--------------|
| **Boston Dynamics Spot** | Vacuum-rated actuators, thermal management (-173 to +127C), regolith-sealed joints, rad-hardened electronics | Closest to Lunar Outpost HL-MAPP (250 kg, 200 kg payload) |
| **DJI Matrice drones** | No atmosphere = no flight. Not viable. | N/A -- replaced by ballistic hoppers or tethered systems |
| **Gecko TOKA climbers** | Magnetic wheels work only on steel; lunar structures would need ferrous surfaces or gecko-adhesion pads | Viable for inspecting lunar habitat hull exterior |
| **Leica BLK LiDAR** | LiDAR works in vacuum (no atmospheric scattering benefit actually). Thermal management needed. | Directly mountable on lunar rovers for terrain mapping |

### Lunar Outpost MAPP Rover (actual lunar platform)

- **Standard MAPP**: 10 kg, 10 cm/s, 15 kg payload, stereo nav cams, RESOURCE depth sensor (12MP color + 1MP ToF), thermal camera, solar powered, 14 Earth-day mission life
- **MAPP-Ultra**: 30 kg, 1 m/s, 30 kg payload, extended battery
- **HL-MAPP**: 250 kg, 200 kg payload, lunar night survival, designed for ISRU equipment transport

MAPP's sensor suite (stereo cameras, LiDAR/ToF, thermal) maps directly to construction survey tasks. A lunar marketplace task like "survey 500m corridor at Shackleton Ridge" is structurally identical to "survey 500m highway corridor in Texas" -- different environment, same data pipeline.

---

## 9. What Actually Shows Up on the Marketplace

### Tier 1: Available Now (Earth, commercial-ready)

- **DJI Matrice 350 RTK + Zenmuse L2** -- topographic survey, volumetrics, progress monitoring
- **Skydio X10** -- autonomous bridge/structure inspection, thermal analysis
- **Boston Dynamics Spot + BLK ARC** -- interior scanning, digital twins, construction progress
- **Flyability ELIOS 3** -- confined space (tanks, tunnels, box girders)
- **Gecko TOKA** -- wall-climbing UT for steel infrastructure

### Tier 2: Integration Required (6-12 months)

- MCP tool interfaces on Tier 1 robots (mission dispatch, data retrieval)
- ERC-8004 agent identity for robot operators
- Standardized deliverable formats (point clouds, orthomosaics, defect reports)

### Tier 3: Lunar Extension (18-36 months)

- Lunar Outpost MAPP or HL-MAPP with marketplace-compatible firmware
- Earth-based AI orchestration via deep-space MCP relay
- ERC-8004 reputation accrual for lunar mission completion

---

*Sources: DJI Enterprise, Boston Dynamics, Skydio, Flyability, Gecko Robotics, Leica Geosystems, Lunar Outpost, Ethereum EIP-8004, Anthropic MCP documentation, UAV Coach, ROCK Robotic, GPRS, various industry pricing guides (The Drone U, FlyGuys, UAV Sphere). Research conducted 2026-03-27.*
