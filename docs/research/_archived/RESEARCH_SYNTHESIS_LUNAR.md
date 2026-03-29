# Research Synthesis: Lunar Robot Marketplace

**Date:** 2026-03-26
**Status:** Initial synthesis from web research
**Covers:** Research questions RQ-1 through RQ-14 from RESEARCH_PLAN_LUNAR.md
**Confidence level:** Mixed (see per-section assessments)

---

## Key Findings (Executive Summary)

1. **Earth-Moon latency is 1.28s one-way (2.56s RTT) minimum, but relay availability is the harder problem.** Continuous coverage requires orbital relay infrastructure that is only now being deployed (Lunar Pathfinder late 2026, ESA Moonlight full ops 2030, Crescent Space Parsec 2026). Until constellation completion, communication windows will be intermittent with multi-hour blackouts.

2. **DTN (Delay-Tolerant Networking) is space-proven and is the mandated protocol for lunar comms.** NASA's LunaNet Interoperability Specification requires DTN/Bundle Protocol (RFC 9171). It has been tested on the ISS and is operational on NASA missions. DTN's store-and-forward model maps naturally to asynchronous auction bidding.

3. **LunaNet data rates are modest: 50 Mbps Ka-band, 36 Kbps S-band.** This is sufficient for auction protocol messages (small JSON payloads) but not for streaming telemetry or real-time video verification. Verification must rely on structured data, not raw sensor feeds.

4. **Near-term lunar robot populations are too small for a competitive marketplace.** Even with NASA targeting up to 30 robotic landings/year from 2027, individual surface robot populations at any given site will likely be 3-10 units through 2030. The auction model may collapse to direct assignment or priority queuing for the first generation.

5. **Lunar task durations are orders of magnitude longer than Earth tasks.** Where Earth tasks complete in 42 seconds, lunar tasks (site surveys, regolith sampling, equipment transport) will take hours to days. The entire auction lifecycle -- bid windows, execution timeouts, settlement holds -- must be redesigned for long-duration operations.

6. **Rover onboard compute is severely constrained.** Current flight-qualified processors (RAD750) run at ~400 MIPS -- comparable to a late-1990s desktop. Running an on-board auction agent is feasible only if it is extremely lightweight. NASA's HPSC next-gen processor will improve this, but is not yet flight-qualified.

7. **Lunar delivery costs are ~$1.2M/kg, making every robot a $50M+ asset.** At these economics, task pricing will be $1,000-$100,000+ per task-hour (amortized), and failure of a single robot is catastrophic. The marketplace must prioritize safety over speed.

8. **Blockchain settlement over DTN links is an active research area with working prototypes.** The DTNB framework and Ethereum-based delay-tolerant payment schemes demonstrate that batched, asynchronous settlement is technically feasible. Optimistic rollup patterns (7-day dispute windows) are architecturally compatible with Earth-Moon latency.

9. **Lunar night (14 Earth days of darkness, -173C) is the dominant operational constraint.** Most near-term rovers cannot survive lunar night without radioisotope heaters. This means robots are available only during the ~14-day lunar day, creating hard scheduling windows and seasonal capacity constraints.

10. **The "minimum viable decentralization" for a first lunar deployment is a trusted Earth-side coordinator with DTN-tolerant protocols** -- not a fully decentralized on-chain marketplace. Full decentralization is premature for 3-10 robots and 2-3 projects.

---

## Domain A: Communications & Latency

### What We Learned

**Earth-Moon Latency (RQ-1):**
- One-way light-time: 1.28 seconds (average Earth-Moon distance ~384,400 km)
- Round-trip time: 2.56 seconds minimum, up to 2.7 seconds at apogee
- With relay hops and processing delays, practical RTT is 3-8 seconds
- Link interruptions from occultation, relay handoff, and antenna scheduling can cause blackouts of minutes to hours

**Relay Infrastructure (RQ-2):**

| Provider | Asset | Status | Bandwidth | Timeline | Coverage |
|----------|-------|--------|-----------|----------|----------|
| ESA/SSTL | Lunar Pathfinder | In production | S-band + UHF, X-band to Earth | Launch NET Nov 2026 | Southern hemisphere, intermittent |
| ESA | Moonlight (5 satellites) | Funded (EUR 176M confirmed Nov 2025) | TBD (high data rate + nav) | Initial ops end of 2028, full ops 2030 | Near-global |
| Crescent Space (Lockheed Martin) | Parsec network | First nodes 2025 | TBD | Operational 2026, expanding | TBD |
| NASA | LCRNS | In development | Ka-band: 50 Mbps return, 10 Mbps forward; S-band: 36 Kbps | Incremental from Artemis III (2027) | Via relay satellites |
| JAXA | LNSS | Planned | TBD | 2028 | TBD |

**Key finding:** Continuous, reliable Earth-Moon communication is NOT available today and will not be until ~2028-2030 when multiple relay constellations reach initial operating capability. The Lunar Pathfinder (2026) provides only intermittent coverage of the southern hemisphere.

**DTN and Bundle Protocol (RQ-3):**
- DTN is the mandated networking protocol for LunaNet (per the LunaNet Interoperability Specification v5, published Feb 2025)
- Bundle Protocol v7 (RFC 9171, updated by RFC 9713 in Jan 2025) is the core transport
- DTN operates on a "store-and-forward" model: data bundles are held at each node until the next link becomes available
- Successfully tested on ISS: all transmitted bundles received without corruption
- NASA's PACE mission (2024) was the first Class-B mission to use DTN operationally
- ION and DTNME implementations have over a decade of operational experience
- LunaNet supports both real-time frame service and non-real-time DTN service over S-band and Ka-band

**Source confidence:** HIGH for latency physics and DTN maturity. MEDIUM for relay deployment timelines (subject to launch delays). LOW for commercial pricing models (not publicly disclosed).

### Implications for Architecture

1. **Auction bid collection must be deadline-based, not synchronous.** The current `asyncio.gather()` pattern with ~4s timeout will not work. Replace with a "bid window" model: publish RFQ via DTN bundle, collect bids for a configurable window (e.g., 30-120 seconds), then score. Bids arriving after the window closes are rejected.

2. **MCP-over-DTN requires a store-and-forward proxy.** MCP tool calls should be queued as DTN bundles during link outages and replayed on reconnection. This is architecturally similar to a message queue (RabbitMQ/NATS pattern) but using Bundle Protocol as transport.

3. **Design for intermittent connectivity as the default, not the exception.** The system must handle multi-hour blackouts gracefully. All state transitions must be idempotent, and the protocol must support "resume from last known state" after reconnection.

4. **Bandwidth is sufficient for auction protocol messages but not for rich verification data.** Auction bids, task specs, and settlement confirmations are small (< 10 KB). Verification images or sensor dumps may need to be sent during Ka-band windows only.

---

## Domain B: Autonomous Agent Architecture

### What We Learned

**On-board Autonomy (RQ-4):**

Current lunar rover compute capabilities:
- **RAD750** (used on Perseverance, Curiosity): ~400 MIPS, radiation-hardened to 200K-1M Rads. Comparable to a late-1990s PowerPC.
- **Astrobotic CubeRover**: Dual-computer architecture -- one space-hardened processor for core rover software, one higher-performance (less hardened) processor for image processing and autonomy. Per-kg payload allocation: 0.5W continuous power, 10 kbps bandwidth.
- **JAXA LEV-1/LEV-2**: Demonstrated fully autonomous operations on the lunar surface (Jan 2024). LEV-2 (250g, baseball-sized) achieved world's first fully autonomous lunar surface exploration, including autonomous image selection and transmission.
- **NASA HPSC** (next-gen): Radiation-hardened multicore SoC, 64-bit, with edge processing. Not yet flight-qualified but represents a step change in onboard compute.
- **NASA Space ROS**: Open-source framework for flight-quality robotic and autonomous space systems, based on ROS 2. Used in Astrobee (ISS), planned for VIPER.
- **NASA ROSA**: AI agent for interacting with ROS-based robotics via natural language queries.

**Multi-project Coordination (RQ-5):**

The Contract Net Protocol (CNP), introduced by Reid G. Smith in 1980, remains the foundational model for multi-agent task allocation:
- Manager broadcasts task announcement
- Agents evaluate and submit bids
- Manager selects winning bid
- Close to sealed auction protocols

Modern extensions include:
- **Combinatorial auctions**: Robots bid on bundles of tasks, enabling optimization of multi-task assignments
- **Decentralized adaptive allocation** (Nature, 2025): Two-layer architecture with adaptive controllers that predict task parameters and selectively broadcast to relevant agents
- **Market-based mechanisms**: Apply economic principles (pricing, supply/demand) to decentralized task allocation
- **Golem / iExec**: Decentralized compute marketplaces that use dockerized task execution with worker pools -- a precedent for decentralized task dispatch, though designed for compute tasks, not physical robots

**Source confidence:** HIGH for rover compute specs (published hardware data). MEDIUM for autonomy framework maturity (Space ROS is still maturing). LOW for how well CNP/auction mechanisms perform at lunar-scale latencies (no published experiments at 3-8s RTT).

### Implications for Architecture

1. **The on-board auction agent must be extremely lightweight.** On a RAD750-class processor, a full Python auction engine is not viable. The agent should be a minimal C/Rust state machine: receive RFQ bundle, evaluate against local capability/availability, emit bid bundle. Earth-side components handle scoring, assignment, and settlement.

2. **Split the auction lifecycle between Moon-side and Earth-side:**
   - **Moon-side (on-robot):** Capability advertisement, bid generation, task acceptance, task execution, result reporting, local safety checks
   - **Earth-side (coordinator):** RFQ origination, bid scoring/ranking, assignment decision, payment settlement, dispute resolution, global scheduling
   - **Split (either side with fallback):** Task verification (prefer Moon-side with Earth-side audit)

3. **For 3-10 robots and 2-3 projects, use a centralized Earth-side coordinator with DTN tolerance.** The fully decentralized Contract Net model adds complexity without benefit at this scale. The coordinator should be a single service with geographic failover, not an on-chain protocol. Decentralize later when robot populations exceed ~20 and multiple independent operators exist.

4. **JAXA's LEV-1/LEV-2 results prove that fully autonomous surface operations are feasible even with tiny computers.** The barrier is not "can a robot operate autonomously" but "can it participate in a market protocol autonomously." The latter requires only a thin bidding agent, not general AI.

---

## Domain C: Lunar Robotics & Operations

### What We Learned

**Task Types and Feasibility (RQ-6):**

| Task Type | Feasibility Tier | Expected Duration | Hardware Examples | Notes |
|-----------|-----------------|-------------------|-------------------|-------|
| Site imaging/survey | Near-term (2026-2028) | Hours | CubeRover, LEV-2, any camera-equipped rover | Already demonstrated by SLIM/LEV-2 |
| Regolith sampling | Near-term (2027-2029) | Hours | ispace TENACIOUS (has shovel), CLPS payloads | Demonstrated in concept by ispace M2 design |
| Sensor deployment | Near-term (2027-2029) | Hours to 1 day | CubeRover (payload delivery) | Place-and-leave sensors |
| Equipment transport | Medium-term (2028-2030) | Hours to days | Lunar Terrain Vehicle, larger rovers | Requires >10 kg payload capacity |
| Solar panel maintenance | Medium-term (2029-2031) | Hours | Specialized robots with manipulators | Dust mitigation is key challenge |
| Communications relay placement | Medium-term (2028-2030) | Hours to 1 day | CubeRover-class with relay payload | Relatively straightforward transport task |
| Construction support | Speculative (2030+) | Days to weeks | Not yet designed | Requires multi-robot workflows (v2.0 prerequisite) |
| ISRU (ice mining, processing) | Speculative (2030+) | Continuous | Specialized industrial robots | Multi-month campaigns, not task-based |

**CLPS Mission Cadence:**
- NASA targeting up to 30 robotic landings/year starting 2027
- Firefly Blue Ghost Mission 1 landed March 2, 2025 (successful)
- Intuitive Machines Nova-C IM-2 landed March 6, 2025
- Intuitive Machines received $180.4M for payload delivery to lunar south pole (announced March 2026)
- Australian Space Agency rover and Blue Origin/Honeybee Robotics payloads manifested

**Environmental Constraints (RQ-7):**
- **Temperature:** -173C (lunar night) to +127C (lunar day). 300C thermal swing.
- **Lunar night:** 14 Earth days of darkness. Most rovers cannot survive without RTG or thermal shelter. Providing 1W over 14-day night requires ~5 kg of extra solar cells and batteries.
- **Dust:** Electrostatically charged, abrasive lunar regolith. Degrades mechanisms, optics, seals.
- **Radiation:** No atmosphere or magnetosphere. RAD750 handles 200K-1M Rads; unshielded electronics will fail.
- **Gravity:** 1/6 Earth. Affects mobility, sample handling, construction.
- **Communication windows:** As detailed in Domain A -- intermittent until relay constellations mature.

**Source confidence:** HIGH for environmental data and near-term task feasibility. MEDIUM for mission cadence (launch schedules slip frequently). LOW for medium-term and speculative tasks (no demonstrated hardware).

### Implications for Architecture

1. **The task spec must include lunar-specific fields:** thermal window (acceptable temperature range), power budget (Wh available), dust exposure rating, illumination requirement (day-only vs. night-capable), communication window requirement, and maximum task duration.

2. **Scoring algorithm needs lunar factors.** The current Earth weights (price 40%, speed 25%, confidence 20%, track record 15%) should be augmented with:
   - **Power margin** (does the robot have enough energy to complete the task AND return to safe harbor?): 15-20% weight
   - **Thermal window compliance** (is the task scheduled within the robot's operating temperature range?): hard constraint (pass/fail)
   - **Dust exposure** (cumulative dust impact on robot's remaining useful life): 5-10% weight
   - **Communication coverage** (will the robot have relay access during critical task phases?): hard constraint for verification-required tasks

3. **v2.0 multi-robot workflows are a prerequisite for most meaningful lunar tasks.** Site surveys that require multiple vantage points, sample-and-return operations, and construction support all require task decomposition and sequencing. Single-shot task execution covers only the simplest use cases.

4. **Seasonal capacity planning is critical.** Robot availability follows the 14-day day/night cycle. The marketplace must model "available capacity per lunar day" and support advance booking across multiple lunar days.

---

## Domain D: Decentralized Coordination & Settlement

### What We Learned

**Task Verification (RQ-8):**

Verification patterns applicable to high-latency lunar operations:

- **Optimistic verification (from L2 rollups):** Assume task completion is valid; allow a dispute window (hours to days) for challenges. This is architecturally compatible with Earth-Moon latency -- a 24-hour dispute window is trivial when tasks take hours/days anyway.
- **Cross-robot attestation:** Robot B verifies Robot A's work by observing the result (e.g., confirming a sensor was placed at the correct location). Demonstrated in concept by JAXA LEV-1/LEV-2 inter-robot communication.
- **Structured proof of completion:** Instead of sending raw sensor data for verification, the robot sends a structured attestation (GPS coordinates, timestamped photos, sensor checksums) that can be verified against the task spec.

**Settlement Across High-Latency Links (RQ-9):**

- **DTNB (Discrete Token Negotiation Blockchain):** Published 2021, IEEE. A blockchain transaction framework specifically designed for DTN environments. Uses discrete token generation and mining qualification attribution to handle intermittent connectivity. Demonstrated advantages in throughput, block generation time, and fork rate vs. standard blockchain in DTN conditions.
- **Ethereum Delay-Tolerant Payment Scheme:** Published 2019, IEEE. Demonstrates reliable payment services on top of unreliable networks by leveraging blockchain mining nodes for transaction processing during connectivity windows.
- **Batched settlement:** Standard practice in rollup architectures. The sequencer batches transactions and posts them as a bundle to L1 during connectivity windows -- directly analogous to posting settlement bundles during Earth-Moon communication windows.
- **Optimistic rollup dispute windows:** Typically 7 days. This timeframe is compatible with lunar operations (tasks take hours/days, settlement can wait for the next communication window).

**Conflict Resolution (RQ-10):**

Double-booking risk is real with 3-8 second RTT:
- Two projects could submit hire requests for the same robot within the same RTT window
- With relay blackouts, the window of potential conflict extends to hours
- **Pessimistic locking** (robot locks itself to one task upon acceptance) is the simplest solution for small fleets
- **Priority queuing** (projects have priority tiers based on contracts/SLAs) handles contention without complex distributed consensus
- For a first deployment, pessimistic locking + a centralized coordinator eliminates all double-booking by design

**Source confidence:** HIGH for optimistic rollup patterns (well-established in Ethereum ecosystem). MEDIUM for DTNB and DTN payment schemes (published research but not production-deployed). LOW for cross-robot attestation at scale (only demonstrated in 2-robot JAXA experiment).

### Implications for Architecture

1. **Use optimistic verification with structured proofs.** The robot submits a completion attestation (task ID, GPS fix, timestamp, photo hash, sensor data hash). The system assumes validity. The hiring project has a configurable dispute window (default: 24 hours or next communication window, whichever is longer) to challenge.

2. **Settlement should be batched and asynchronous.** Do not require real-time on-chain confirmation for each task. Instead:
   - Robot completes task and submits completion proof via DTN
   - Earth-side coordinator validates and queues settlement transaction
   - Settlement transactions are batched and posted to L1 (Base/Ethereum) during the next communication window
   - USDC transfer executes on-chain; confirmation is relayed back to Moon-side agents in the next DTN pass

3. **An Earth-side settlement proxy is simpler and more practical than a lunar sidechain for v1.** The proxy holds escrow, executes on-chain settlements, and relays confirmations. A lunar sidechain adds consensus complexity for negligible benefit with 3-10 robots.

4. **Pessimistic locking on the robot side eliminates double-booking.** When a robot accepts a task (locally), it immediately marks itself as unavailable. The Earth-side coordinator sees this status in the next DTN update. No distributed consensus needed.

---

## Domain E: Economic Model

### What We Learned

**Delivery Costs (RQ-11):**
- **CLPS per-kg pricing:** ~$1.2M/kg to lunar surface (derived from Intuitive Machines Nova-C: $118M contract / 100 kg payload capacity)
- **Rideshare pricing:** From ~$4M per payload slot (Intuitive Machines financial reporting), more economical than dedicated missions
- **Total CLPS program ceiling:** $2.6 billion through November 2028
- **Intuitive Machines recent contract:** $180.4M for multi-payload delivery to lunar south pole (March 2026)

**Robot Asset Value:**
- A 5 kg CubeRover at $1.2M/kg delivery = $6M in delivery cost alone, plus hardware cost
- A 50 kg capable rover: $60M+ in delivery cost
- Lunar Terrain Vehicle (crewed): hundreds of millions in total program cost

**Operating Cost Modeling:**
- Lunar base operating costs: ~$7.35B/year for a manned facility (CSIS estimate)
- Telerobotic operations from Earth are "mainly just labor with overhead" -- significantly cheaper than manned
- Commercial teleoperations pricing exists: Lunatix plans EUR 500 ($590) for a 20-minute teleop session
- Providing 1W of power during lunar night costs ~5 kg of batteries/solar cells = ~$6M at CLPS rates

**Amortized Task Pricing Model (estimated):**

Assumptions: 5 kg rover, $1.2M/kg delivery ($6M delivery), $2M hardware, $8M total asset value, 14-day operational windows, 2-year useful life (~24 lunar days), 8 hours productive work per lunar day.

- Total productive hours: 24 days x 8 hours = 192 hours
- Amortized cost per hour: $8M / 192 hours = ~$41,700/hour
- At 50% utilization: ~$83,400/hour
- A 1-hour survey task: ~$42,000-$83,000 (amortized capital only, excluding Earth-side ops costs)

For comparison, Earth v1.0 pricing: $0.35 per 42-second task = ~$30/hour.

**Lunar pricing is approximately 1,000-3,000x Earth pricing**, consistent with the research plan's estimate.

**Fee Model (RQ-12):**
- No direct comparables found for lunar marketplace fees
- Heavy equipment rental marketplaces (Ritchie Bros, BigRentz) typically charge 10-20% platform fees
- Satellite services (bandwidth, imaging) use capacity-based pricing, not per-transaction fees
- With only 3-10 robots and high asset values, a percentage-of-task-value fee (5-15%) is more appropriate than a flat fee
- The platform's primary value proposition is utilization optimization: even a 10% improvement in robot utilization at $42K/hour saves $800K+ over a robot's lifetime

**Source confidence:** HIGH for delivery cost per kg (multiple published sources). MEDIUM for operating cost estimates (few published figures for robotic operations specifically). LOW for fee model (no lunar marketplace precedents).

### Implications for Architecture

1. **The pricing model must be capital-amortization-aware.** Task pricing should factor in: delivery cost amortized over expected lifetime, operating cost per hour, risk premium (probability of robot loss during task), opportunity cost (what else could the robot be doing), and margin.

2. **Utilization rate is the critical economic variable.** At $42K/hour amortized cost, the difference between 30% and 70% utilization is the difference between $140K/hour and $60K/hour effective pricing. The marketplace's core value is maximizing utilization.

3. **Insurance and risk pooling are essential.** At $8-60M+ per robot, task failure risk must be shared. Options: mandatory task insurance (premium based on risk rating), operator self-insurance with escrow, or mutual risk pools among operators.

4. **The 0% seed-phase fee from Earth v1.0 may not work.** Lunar operators need confidence that the platform adds value before deploying $50M+ assets. Consider a "guaranteed minimum utilization" model: the platform guarantees X hours/lunar-day of paid work, taking a fee only on hours above the guarantee.

---

## Assumption Validation

| # | Assumption | Verdict | Evidence |
|---|-----------|---------|----------|
| A1 | Earth-Moon communication available 80%+ of the time by 2030 | **INCONCLUSIVE (leaning plausible)** | Lunar Pathfinder (2026), Crescent Parsec (2026), ESA Moonlight full ops (2030), and NASA LCRNS together should provide near-continuous coverage by 2030. However, no single provider guarantees 80% uptime yet, and launch delays are common. Combined multi-provider coverage could reach 80% by 2029-2030. |
| A2 | Lunar robots can run an on-board auction agent | **VALIDATED (with constraints)** | JAXA LEV-1/LEV-2 demonstrated fully autonomous decision-making on tiny computers (250g rover). A lightweight bidding agent (capability check + bid generation) is feasible on RAD750-class processors. A full Python auction engine is not. |
| A3 | Multiple independent projects will deploy to overlapping lunar regions | **VALIDATED** | NASA, ESA, JAXA, ISRO, and multiple commercial operators (Intuitive Machines, Astrobotic, ispace, Firefly) are all targeting the lunar south pole region. CLPS is manifesting payloads from multiple organizations on the same landers. Overlap is virtually guaranteed at the south pole by 2028-2030. |
| A4 | On-chain settlement can tolerate 3-10 second confirmation delay | **VALIDATED** | 3-10 seconds is trivial compared to Ethereum's 12-second block time and L2 rollup finality times. The real challenge is link interruptions (hours, not seconds). Batched asynchronous settlement via Earth-side proxy handles this. DTNB research demonstrates blockchain transactions are feasible over DTN. |
| A5 | Task verification can be automated without human review | **INCONCLUSIVE** | Structured proof-of-completion (GPS + timestamp + photo hash) can be verified automatically for simple tasks (did the rover go to location X and take a photo?). Complex tasks (quality of regolith sample, structural integrity of construction) likely still need human review. Optimistic verification with dispute windows is the bridge. |
| A6 | ERC-8004 registry model extends to multi-body environments | **INCONCLUSIVE** | No technical barrier to having lunar robots registered on an Earth-side ERC-8004 registry with a DTN-tolerant discovery proxy. But registry updates (robot status changes) will be delayed by communication latency. A cached local registry on the Moon-side coordinator, synced periodically via DTN, is likely needed. |
| A7 | Enough robots on the Moon for a competitive marketplace | **INVALIDATED for 2028, INCONCLUSIVE for 2030+** | Through 2028, surface robot populations at any single site will be 3-10 units, likely from 2-3 operators. This is not enough for competitive auction dynamics. By 2030+, with NASA targeting 30 robotic landings/year, populations may reach 15-30, approaching marketplace viability. **The first deployment should use a dispatch/scheduling model, not an open auction.** |
| A8 | v2.0 multi-robot workflows are a prerequisite | **VALIDATED** | The lunar task taxonomy shows that nearly all medium-term tasks (equipment transport, construction support, multi-point surveys) require task decomposition and multi-robot coordination. Single-shot tasks (take a photo, place a sensor) are the only viable v1.0-compatible operations. |
| A9 | Privacy requirements do not conflict with lunar verification | **INCONCLUSIVE** | Not enough data to assess. Commercial lunar operations (mining prospecting, resource claims) are likely competitively sensitive. If task details must be private (which mine site? what resource?), then the structured proof-of-completion model must be compatible with zero-knowledge or selective-disclosure proofs. This intersection needs dedicated research. |

---

## Architecture Recommendations

### 1. Start with a Centralized Earth-Side Coordinator, DTN-Tolerant by Design

Do not build a decentralized on-chain marketplace for the first lunar deployment. Instead:
- Run a centralized task coordinator on Earth with geographic failover
- Communicate with lunar robots via DTN/Bundle Protocol through relay infrastructure
- Use deadline-based bid windows (not synchronous RFQ) with configurable timeouts
- Design all protocol messages as idempotent DTN bundles that tolerate replay and reordering
- The coordinator handles scheduling, assignment, settlement, and dispute resolution

This gives you 90% of the value with 10% of the complexity. Decentralize when robot populations and operator diversity warrant it (likely 2030+).

### 2. Build a Thin Moon-Side Agent, Keep Intelligence Earth-Side

The on-robot agent should be a minimal state machine (~100 KB binary) that:
- Maintains a local capability/availability register
- Receives RFQ bundles and generates bids based on local constraints (power, thermal, schedule)
- Accepts task assignments and executes via Space ROS / local autonomy stack
- Generates structured completion proofs (GPS, timestamps, data hashes)
- Uses pessimistic self-locking (marks itself unavailable upon task acceptance)

All scoring, optimization, settlement, and dispute resolution stays Earth-side where compute is cheap and connectivity to chains is direct.

### 3. Use Optimistic Verification with Batched Settlement

- Robot submits structured completion proof via DTN
- Earth-side coordinator applies automated verification checks
- If checks pass, queue settlement (USDC transfer) in the next batch
- Batch is posted on-chain during the next communication window
- Hiring project has a 24-hour dispute window after proof is relayed to them
- For high-value tasks: require cross-robot attestation (a second robot confirms the work)

This mirrors optimistic rollup patterns and is well-suited to the communication constraints.

### 4. Design the Task Spec for Lunar Day Cycles and Long-Duration Operations

Extend the task specification with:
- `thermal_window`: Acceptable temperature range for execution
- `power_budget_wh`: Maximum energy the task may consume
- `max_duration_hours`: Expected and maximum task duration
- `illumination_required`: Boolean (day-only vs. night-capable)
- `comm_window_required`: Whether the task needs active relay coverage during execution
- `safety_zone`: Geofence defining acceptable operating area
- `checkpoint_intervals`: For long tasks, define intermediate progress checkpoints
- `failure_recovery_mode`: `abort_and_safe` | `checkpoint_and_resume` | `operator_escalate`

### 5. Phase the Deployment: Dispatch First, Marketplace Later

- **Phase 0 (2027-2028):** Single-operator task dispatch. One operator, their own robots, scheduling tasks via the platform. Validates DTN protocol, task spec, and settlement flow.
- **Phase 1 (2028-2030):** Multi-operator dispatch with priority queuing. 2-3 operators share a coordinator. Tasks assigned by priority/capability, not competitive bidding. Validates cross-operator coordination.
- **Phase 2 (2030+):** Competitive marketplace. When robot populations reach 15-30+ and operator diversity warrants it, introduce auction-based bidding. By this point, relay infrastructure should support near-continuous communication.

---

## Sources

### Communications & Relay Infrastructure
- [NASA LunaNet Overview](https://www.nasa.gov/humans-in-space/lunanet-empowering-artemis-with-communications-and-navigation-interoperability/)
- [NASA LCRNS Project](https://www.nasa.gov/goddard/esc/lcrns/)
- [LunaNet Interoperability Specification](https://www.nasa.gov/directorates/somd/space-communications-navigation-program/lunanet-interoperability-specification/)
- [LunaNet - Wikipedia](https://en.wikipedia.org/wiki/LunaNet)
- [ESA Moonlight Programme](https://www.esa.int/Applications/Connectivity_and_Secure_Communications/ESA_s_Moonlight_programme_Pioneering_the_path_for_lunar_exploration)
- [ESA Moonlight Launch Press Release](https://www.esa.int/Newsroom/Press_Releases/ESA_launches_Moonlight_to_establish_lunar_communications_and_navigation_infrastructure)
- [Lunar Pathfinder - Wikipedia](https://en.wikipedia.org/wiki/Lunar_Pathfinder)
- [Lunar Pathfinder - BSGN/ESA](https://bsgn.esa.int/service/lunar-pathfinder/)
- [Crescent Space (Lockheed Martin)](https://crescentspace.com/)
- [Crescent Space Announcement - Lockheed Martin](https://news.lockheedmartin.com/2023-03-28-Crescent-Space-to-Deliver-Critical-Services-to-a-Growing-Lunar-Economy)
- [NASA Lunar Relay Services Requirements Document](https://www.nasa.gov/wp-content/uploads/2025/08/lunar-relay-services-requirements-document-srd.pdf)

### DTN & Bundle Protocol
- [NASA DTN Overview](https://www.nasa.gov/communicating-with-missions/delay-disruption-tolerant-networking/)
- [RFC 9171 - Bundle Protocol Version 7](https://datatracker.ietf.org/doc/rfc9171/)
- [DTN Flight Test Results from ISS (ResearchGate)](https://www.researchgate.net/publication/224130972_DelayDisruption-Tolerant_Networking_Flight_test_results_from_the_international_space_station)
- [NASA HDTN Technical Memo](https://ntrs.nasa.gov/api/citations/20240004702/downloads/TM-20240004702.pdf)
- [NASA/ESA DTN Robot Control from ISS](https://www.nasa.gov/news-release/nasa-esa-use-experimental-interplanetary-internet-to-test-robot-from-international-space-station/)

### Lunar Robotics & Rovers
- [Astrobotic CubeRover](https://www.astrobotic.com/lunar-delivery/rovers/cuberover/)
- [Astrobotic CubeRover Payload User Guide (PDF)](https://www.astrobotic.com/wp-content/uploads/2024/01/Astrobotic_CubeRover-PUG_V2-2.pdf)
- [ispace HAKUTO-R Mission 2 - Wikipedia](https://en.wikipedia.org/wiki/Hakuto-R_Mission_2)
- [JAXA LEV-1 Results](https://global.jaxa.jp/press/2024/01/20240125-2_e.html)
- [JAXA LEV-2 SORA-Q](https://www.ihub-tansa.jaxa.jp/english/LEV2_en.html)
- [JAXA SLIM - Wikipedia](https://en.wikipedia.org/wiki/Smart_Lander_for_Investigating_Moon)
- [NASA HPSC Overview](https://etd.gsfc.nasa.gov/our-work/hpsc-transforming-spaceflight-computing-with-radiation-hardened-multicore-technology/)
- [Mars Rover Computers Comparison - Wikipedia](https://en.wikipedia.org/wiki/Comparison_of_embedded_computer_systems_on_board_the_Mars_rovers)
- [NASA Space ROS](https://space.ros.org/)
- [NASA ROSA (Robot Operating System Agent)](https://github.com/nasa-jpl/rosa)

### Artemis Program & CLPS
- [NASA Artemis Program](https://www.nasa.gov/humans-in-space/artemis/)
- [NASA CLPS Program](https://www.nasa.gov/reference/commercial-lunar-payload-services/)
- [Intuitive Machines $180.4M CLPS Award (March 2026)](https://www.intuitivemachines.com/post/intuitive-machines-expands-lunar-surface-operations-with-180-4-million-nasa-clps-award)
- [Payload Research: CLPS Economics](https://payloadspace.com/payload-research-the-ultra-low-cost-economics-of-nasas-clps-lunar-program/)
- [Intuitive Machines Nova-C - Wikipedia](https://en.wikipedia.org/wiki/Intuitive_Machines_Nova-C)
- [NASA 30 Robotic Landings/Year Target](https://www.nextbigfuture.com/2026/03/high-gear-moonbase-program-kicks-off-with-30-robotic-moon-missions-starting-in-2027-and-nuclear-powered-base-by-2030.html)
- [NASA Robots/Rovers Monthly Launch Cadence](https://www.wusf.org/science-space/2026-03-20/nasa-could-send-robots-rovers-moon-once-a-month-next-year)

### Multi-Agent Coordination
- [Contract Net Protocol - Wikipedia](https://en.wikipedia.org/wiki/Contract_Net_Protocol)
- [Decentralized Adaptive Task Allocation (Nature, 2025)](https://www.nature.com/articles/s41598-025-21709-9)
- [Auction-Based Task Allocation for Multi-Robot Teams (CMU)](https://www.ri.cmu.edu/pub_files/pub4/zlot_robert_michael_2006_2/zlot_robert_michael_2006_2.pdf)
- [Multi-Agent Coordination Survey (arXiv, 2025)](https://arxiv.org/html/2502.14743v2)

### Blockchain & Settlement
- [DTNB Framework (IEEE, 2021)](https://ieeexplore.ieee.org/document/9373925/)
- [Delay-Tolerant Payment Scheme on Ethereum (IEEE, 2019)](https://ieeexplore.ieee.org/document/8661611/)
- [Blockchain Transaction Mechanism in DTN (ScienceDirect, 2024)](https://www.sciencedirect.com/science/article/abs/pii/S1084804524001759)
- [Optimistic Rollups - ethereum.org](https://ethereum.org/developers/docs/scaling/optimistic-rollups/)
- [CCIP Execution Latency - Chainlink](https://docs.chain.link/ccip/ccip-execution-latency)

### Lunar Environment & Economics
- [Lunar Night Thermal Shelter (ScienceDirect)](https://www.sciencedirect.com/science/article/abs/pii/S0094576520301211)
- [Lunar Night Energy Storage (ScienceDirect)](https://www.sciencedirect.com/science/article/abs/pii/S0094576521002101)
- [Costs of an International Lunar Base (CSIS)](https://www.csis.org/analysis/costs-international-lunar-base)
- [Artemis Base Camp Concept - NASA](https://www.nasa.gov/blogs/missions/2020/10/28/lunar-living-nasas-artemis-base-camp-concept/)
- [Lunatix Rover Teleop Pricing - IEEE Spectrum](https://spectrum.ieee.org/how-much-would-you-pay-to-drive-a-jumping-robot-on-the-moon)
