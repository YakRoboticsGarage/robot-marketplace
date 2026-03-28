# Autonomous Execution Gap Analysis

**Question:** After both skills run (rfp-to-robot-spec + rfp-to-site-recon), what gaps remain before a robot can autonomously execute a single task from an RFP?

**Date:** 2026-03-28

---

## The Two Skills Produce

| Skill | Output | Consumed by |
|-------|--------|-------------|
| rfp-to-robot-spec | Task spec (what to bid on) | Auction engine → operators bid |
| rfp-to-site-recon | Execution context (how to get there and do it) | Winning operator → pre-mobilization |

## What the Robot Knows After Both Skills

1. **What to measure** — sensors, accuracy, deliverable formats (from task spec)
2. **Where to go** — site boundary polygon, coordinates (from site recon LOOKUP)
3. **Airspace constraints** — class, max AGL, LAANC zones (from site recon LOOKUP)
4. **Known obstacles** — FAA-registered towers, power lines (from site recon LOOKUP)
5. **Weather expectations** — wind, rain, temperature norms (from site recon LOOKUP)
6. **Terrain** — elevation, slope, land cover (from site recon LOOKUP)
7. **What it doesn't know** — explicit UNKNOWN list with questions (from site recon)

## What the Robot Still Cannot Do Autonomously

### Gap 1: Flight/Mission Planning

**Problem:** The robot knows the boundary and the sensors needed but doesn't have a flight plan. A DJI Matrice 350 flying a 20-acre site at QL1 density needs:
- Waypoints calculated from boundary + altitude + overlap + GSD requirements
- Flight lines with proper sidelap (typically 60-80%)
- Battery swap points (where does it land mid-mission?)
- Takeoff/landing zones (flat, clear, accessible)

**Current state:** Flight planning software (DJI Pilot 2, Pix4Dcapture, DroneDeploy) generates flight plans from a polygon + parameters. The robot or its MCP server could call a flight planning API.

**Gap:** No flight planning API exists in our MCP tool set. A `plan_flight` tool that takes (boundary polygon, sensor, altitude, overlap) and returns waypoints would close this.

**Severity:** HIGH — without this, a human pilot plans every flight manually.

### Gap 2: Ground Control Point Placement

**Problem:** Survey-grade LiDAR requires GCPs. Someone has to physically place and survey targets on the ground before the drone flies. This is currently a human-only task.

**Current state:** Some workflows use PPK (Post-Processed Kinematic) instead of GCPs, reducing or eliminating ground targets. RTK-enabled drones (like the M350 RTK) can achieve ±3-5cm without GCPs.

**Gap:** The task spec should declare whether GCPs are required or PPK/RTK is acceptable. If GCPs are required, this is a separate human task that must complete before the robot task starts — it's a dependency, not a robot capability.

**Severity:** MEDIUM — solvable by making GCP placement a separate task (or specifying RTK-only for lower accuracy jobs).

### Gap 3: Physical Site Access

**Problem:** The robot arrives at the site boundary coordinates but needs to:
- Get through the gate/fence
- Navigate from the access point to the launch position
- Avoid construction equipment, workers, vehicles
- Comply with safety requirements (which it can't — it doesn't wear a hard hat)

**Current state:** For drones, this means a human pilot drives to the site, sets up, launches. For Spot, the robot navigates autonomously but someone opens the gate.

**Gap:** True autonomous execution requires either (a) the robot is already on-site (permanently deployed), or (b) a human transports and launches it. The marketplace model works better for (a) — operators who have robots already stationed at or near the site.

**Severity:** HIGH for remote deployment, LOW for on-site robots.

### Gap 4: Real-Time Obstacle Avoidance

**Problem:** The FAA obstacle database misses temporary cranes, newly erected scaffolding, stockpiles, and construction equipment that weren't there when the site recon pulled satellite imagery.

**Current state:** Skydio X10 has AI obstacle avoidance. DJI M350 has basic sense-and-avoid. Spot has autonomous navigation.

**Gap:** The robot needs real-time obstacle detection AND the authority to deviate from its planned path. The task spec doesn't include a "deviation tolerance" — how far can the robot go off-plan to avoid an obstacle before the mission is compromised?

**Severity:** MEDIUM — modern platforms handle this, but the task spec doesn't account for it.

### Gap 5: Data Quality Validation In-Field

**Problem:** After collecting data, how does the robot know the data is good enough? If cloud cover ruins photogrammetry, or wind vibration degrades LiDAR accuracy, the robot should detect this and re-fly rather than delivering bad data.

**Current state:** Most drones capture data blind — QC happens in post-processing hours later. Some platforms (DroneDeploy, Pix4D) do real-time processing previews.

**Gap:** A `validate_capture` function that checks point density, coverage completeness, GSD, and accuracy estimates against the task spec before declaring the mission complete. Without this, the robot may deliver data that fails the accuracy requirement, and the operator owes a re-fly.

**Severity:** HIGH — this is the difference between "robot completed task" and "robot completed task correctly."

### Gap 6: Post-Processing and Deliverable Generation

**Problem:** Raw sensor data (LAS points, JPG photos) is not a deliverable. The RFP asks for processed outputs: DTM surfaces, contour maps, orthomosaics, cross-sections, formatted reports. This processing typically happens on a workstation, not on the robot.

**Current state:** Cloud processing (DroneDeploy, Pix4D, Bentley ContextCapture) can automate most of this. But format conversion to agency-specific standards (TxDOT CAD, MDOT layer naming) is often manual.

**Gap:** The marketplace task spec specifies deliverable formats but not who does the processing. Options:
1. The robot operator processes (most realistic today)
2. The marketplace platform processes (SaaS model — value-add)
3. A separate "processing task" is posted to the marketplace (agent-mediated)

**Severity:** MEDIUM — this is a business model question, not a robot capability gap.

### Gap 7: Legal and Regulatory Execution

**Problem:** The robot can't file its own LAANC authorization, obtain a COA, notify 811 for utility locates, or sign a survey certification as a licensed surveyor.

**Current state:** All of these require a human — a licensed pilot files LAANC, a PE stamps the survey, a human calls 811.

**Gap:** The agent can automate some of this (LAANC is API-accessible via Aloft/DroneUp), but PE certification and 811 notification require human involvement. These are pre-mobilization dependencies that the site recon skill should flag.

**Severity:** LOW — the operator handles this, not the robot. But the task spec should distinguish between "robot task" and "operator obligations."

---

## Summary: The Autonomous Execution Stack

```
Layer 5: Deliverable generation   ← post-processing (cloud or operator workstation)
Layer 4: In-field QC              ← validate_capture before declaring complete
Layer 3: Mission execution        ← fly the plan, avoid obstacles, handle weather holds
Layer 2: Mission planning         ← convert boundary + spec → flight plan / scan plan
Layer 1: Site access              ← physically get to launch position
Layer 0: Regulatory compliance    ← LAANC, 811, COA, PE oversight
```

**What the two skills cover:** Layer 0 (identified, not executed) + Layer 2 inputs (boundary, constraints)
**What the auction engine covers:** Operator selection (who has the right robot, certs, location)
**What's missing:** Layers 2 (flight planning API), 4 (in-field QC), and 5 (automated processing)

## Validation Strategy for Each Skill

### Validating rfp-to-robot-spec output

1. **Schema validation** — `validate_task_spec.py` (exists, checks fields/types)
2. **Source tracing** — every extracted value should cite the RFP section it came from. A validation pass could check: "does the RFP text actually contain '±0.05 ft'?" via string search.
3. **Completeness** — compare extracted requirements against a checklist of "things RFPs typically specify." Flag if key fields are missing from both the RFP and the output (accuracy not specified + not defaulted = error).
4. **Cross-reference** — if the task spec says `USGS_QL1`, verify the accuracy numbers match QL1 standards (NVA ≤10cm). The validation script could encode these relationships.
5. **Budget sanity** — compare budget_ceiling against (area × price_per_acre) from the robot mapping reference. Flag if the budget is >3x or <0.3x the expected range.

### Validating rfp-to-site-recon output

1. **Source tagging** — `validate_site_recon.py` (exists, checks every field has a tag)
2. **LOOKUP verification** — for critical fields (airspace class, site boundary), the agent could independently query the same public data source and compare results.
3. **UNKNOWN completeness** — the pre-mobilization checklist should have at least one item for every UNKNOWN field. Validate this relationship.
4. **Staleness check** — LOOKUP data should include `queried_date`. Flag any data older than 90 days (satellite imagery, NBI ratings, NOTAM status).
5. **Consistency with task spec** — the site recon's airspace data should be consistent with the task spec's certification requirements (if airspace is Class B, task spec must include `faa_part_107` + LAANC or COA).
