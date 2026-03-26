# Research Plan: Decentralized Hiring of Robots on the Moon

**User Story:** "Decentralized hiring of robots on the Moon to develop various moon projects."

**Owner:** Product Research
**Date:** 2026-03-26
**Status:** Draft
**Read time:** ~5 minutes

---

## Context

We have a working robot task auction marketplace (v1.0, 151 tests, 15 MCP tools). The system today completes a sensor reading in 42 seconds for $0.35 on Earth, with sub-second communication latency. The lunar extension introduces hard physics constraints (light delay, vacuum, radiation), autonomous multi-project coordination, and cross-boundary settlement that fundamentally change several architectural assumptions.

This plan identifies what we need to learn before committing to a design.

---

## 1. Research Questions

### A. Communications & Latency (3 questions)

**RQ-1. How does 1.3-4+ second one-way latency affect the auction bid collection window?**
Today's bid collection completes in ~4 seconds with `asyncio.gather()`. A lunar round-trip adds 2.6-8+ seconds per exchange. Can we still run a synchronous RFQ, or must bids be collected asynchronously with a deadline-based window?

- **Method:** Technical prototype. Simulate 3-8s RTT on the existing bid collection path and measure auction completion time, timeout behavior, and edge cases (bid arrives after scoring starts). Include a simulation of link interruption mid-auction (relay handoff, occultation). Literature review of DTN (Delay-Tolerant Networking) and IETF Bundle Protocol (RFC 9171).
- **Output:** Latency tolerance matrix showing which auction phases break at 2s, 4s, 8s, and 30s RTT. Must include partial-failure cases (some bids arrive, link drops before all bids are in).

**RQ-2. What communication relay infrastructure exists or is planned for Earth-Moon links?**
Direct line-of-sight is intermittent (lunar far side, Earth rotation). NASA's LunaNet, ESA Moonlight, and commercial relay providers (e.g., Crescent Space) may provide always-on connectivity. What uptime, bandwidth, and latency guarantees do they offer?

- **Method:** Literature review of NASA LunaNet architecture docs, ESA Moonlight program status, and commercial lunar comms providers. Competitive analysis of existing standards (CCSDS, DTN).
- **Output:** Comms infrastructure summary table: provider, status, bandwidth, latency range, availability date, cost model.

**RQ-3. How should MCP tool calls be adapted for high-latency, intermittent links?**
MCP today assumes low-latency request/response. Can we use store-and-forward MCP (queue tool calls, batch responses), or do we need an entirely different protocol for the Earth-Moon boundary?

- **Method:** Technical analysis of MCP spec for timeout and retry semantics. Prototype a store-and-forward MCP proxy that queues calls during link outages and replays them on reconnection.
- **Output:** MCP-over-DTN feasibility assessment with recommended protocol adaptations.

### B. Autonomous Agent Architecture (2 questions)

**RQ-4. What level of on-board autonomy must lunar robots have to participate in auctions without Earth-side intervention?**
On Earth, the fleet server orchestrates auctions. On the Moon, robots may need to run local auction agents that can bid, accept tasks, execute, and report results without waiting for Earth-round-trip confirmation on each step.

- **Method:** Architecture analysis of the current 8-phase auction lifecycle. Identify which phases require Earth-side authority vs. which can be fully delegated to on-robot agents. Literature review of NASA ROSA (Robot Operating System for Autonomy) and ESA ERGO frameworks.
- **Output:** Autonomy allocation matrix: each auction phase mapped to {Earth-side, Moon-side, split} with rationale.

**RQ-5. How do multiple competing lunar projects coordinate robot hiring without a central auctioneer?**
Today, the fleet server is a single coordinator. With multiple independent projects (mining, construction, science) competing for the same robots, who runs the auction? Options: each project runs its own auctioneer, robots run a local matching engine, or a decentralized protocol (on-chain order book, peer-to-peer negotiation).

- **Method:** Literature review of multi-agent coordination protocols (contract net, combinatorial auctions, Fisher market equilibrium). Competitive analysis of existing decentralized job markets (Golem, iExec). Technical analysis of whether ERC-8004 can serve as a shared discovery + bidding layer. **Must also evaluate whether full decentralization is needed at all for a first lunar deployment** — a single trusted auctioneer with failover may be sufficient for 5-20 robots and 2-3 projects. Include a "minimum viable decentralization" option alongside the fully distributed designs.
- **Output:** Coordination architecture options paper (3-4 candidates, including a centralized-with-failover baseline) with trade-off analysis on latency tolerance, fairness, and complexity.

### C. Lunar Robotics & Operations (2 questions)

**RQ-6. What task types are realistic for first-generation lunar robots?**
Our Earth system handles sensor readings. Lunar tasks might include regolith sampling, site surveying, equipment transport, solar panel maintenance, or communications relay placement. Which are feasible with near-term hardware (2028-2032)?

- **Method:** Literature review of Artemis program surface operations plans, CLPS (Commercial Lunar Payload Services) manifests, and published lunar robot capabilities (JAXA SLIM rover, ispace micro-rover, Astrobotic CubeRover). Interviews with lunar robotics researchers if accessible. **Must also quantify task durations** — Earth tasks complete in 42 seconds; lunar tasks may take hours or days. The auction lifecycle (bid, accept, execute, verify, settle) must be evaluated against these longer timescales.
- **Output:** Lunar task taxonomy with feasibility tiers (near-term / medium-term / speculative), expected duration ranges, and mapping to auction system task spec fields.

**RQ-7. What environmental constraints must the task spec and scoring algorithm account for?**
Lunar dust, thermal cycling (-173C to +127C), radiation, 1/6 gravity, and 14-day night cycles all affect robot availability and task pricing. The current scoring algorithm (price 40%, speed 25%, confidence 20%, track record 15%) may need lunar-specific factors like power budget, thermal window, or dust exposure.

- **Method:** Literature review of lunar surface environmental data. Technical analysis of how each constraint maps to bid parameters or scoring factors. Prototype extended scoring algorithm with lunar factors.
- **Output:** Revised scoring algorithm proposal with lunar-specific weighting factors and justification.

### D. Decentralized Coordination & Settlement (3 questions)

**RQ-8. How should task verification work when the verifier is 1.3 light-seconds away?**
Today, the AI agent verifies delivery by inspecting returned data (plausible values, correct fields, on time). On the Moon, verification data takes seconds to reach Earth, and real-time inspection is impractical for time-critical tasks. Can verification be delegated to on-site agents or other robots?

- **Method:** Technical analysis of current verification logic (`confirm_delivery` tool). Design patterns: local verification agent, cross-robot attestation (robot B verifies robot A's work), optimistic verification with dispute window. Literature review of optimistic rollup verification patterns from L2 blockchain systems.
- **Output:** Verification architecture proposal with latency and trust trade-offs.

**RQ-9. Can the existing ERC-8004 + Stripe/USDC settlement model work across the Earth-Moon boundary?**
ERC-8004 registration lives on Earth-side chains. USDC settlement requires chain confirmation. Does the robot need an Earth-side settlement proxy, or can we run a lunar sidechain/rollup with periodic Earth settlement?

- **Method:** Technical analysis of settlement latency requirements vs. communication delay. Literature review of cross-chain bridging patterns and "outpost chain" designs. Evaluate whether x402 payment proofs can be batched and settled asynchronously.
- **Output:** Settlement architecture options paper: Earth-proxy vs. lunar sidechain vs. batched settlement, with latency/cost/complexity trade-offs.

**RQ-10. What happens when two projects try to hire the same robot simultaneously?**
On Earth, our single auctioneer serializes bids. With decentralized coordination, conflicting task assignments are possible — especially with communication delay hiding concurrent bids. How do we handle double-booking?

- **Method:** Technical analysis of concurrency patterns: pessimistic locking (robot locks itself to one task), optimistic concurrency (accept both, cancel loser), priority queuing (projects have priority tiers). Prototype conflict resolution under simulated 4s RTT.
- **Output:** Conflict resolution protocol spec with simulation results.

### E. Safety, Fault Tolerance & Operations (2 questions)

**RQ-13. What happens when a lunar robot fails mid-task and there is no replacement?**
On Earth, Journey C shows re-pooling to a second robot in ~90 seconds. On the Moon, the robot fleet may be 3-5 units total. If the winning robot fails, there may be zero alternatives, and the task involves irreversible physical operations (partially drilled hole, equipment moved halfway). What is the failure recovery model when re-pooling is not an option?

- **Method:** Failure mode analysis of the current 8-phase lifecycle under constrained-fleet conditions. Design patterns: partial completion credits, task checkpointing and resumption, operator-assisted remote recovery. Map failure modes to economic consequences (who bears the cost of a half-completed lunar task?).
- **Output:** Lunar failure recovery protocol with cost allocation model, covering both recoverable and irrecoverable failure cases.

**RQ-14. What safety constraints must the system enforce to prevent robots from accepting tasks that could damage themselves, other robots, or lunar infrastructure?**
On Earth, the worst case of a failed task is a missed sensor reading. On the Moon, a robot navigating to the wrong location or executing the wrong task could destroy itself ($50M+), damage shared infrastructure, or compromise another project's site. The auction system currently has no safety-critical task validation.

- **Method:** Literature review of NASA planetary protection protocols, ISRU safety standards, and multi-agent safety frameworks. Technical analysis of what safety constraints should be hard-coded vs. configurable. Evaluate whether the current hard constraint filter (capability-based) is sufficient or needs extension to include safety zones, power budgets, and task-level risk assessment.
- **Output:** Safety constraint taxonomy and recommended enforcement architecture (on-robot, on-auctioneer, or both).

### F. Economic Model (2 questions)

**RQ-11. What does a pricing model look like when operating costs are 1000x higher than Earth?**
Launching a robot to the Moon costs millions. Operating costs include power, thermal management, and limited consumable life. A $0.35 sensor reading becomes a $X,000+ capital-amortized task. How does the auction pricing model scale?

- **Method:** Cost modeling based on published lunar mission economics (CLPS pricing per kg, estimated robot lifecycle). Literature review of space resource economics (Colorado School of Mines space resources program). Model: amortized cost per task-hour for different robot types and utilization rates.
- **Output:** Lunar task pricing model with sensitivity analysis on utilization rate, robot lifetime, and delivery cost per kg.

**RQ-12. How should the platform fee and incentive structure change for a lunar marketplace?**
Earth v1.0 charges 0% platform fee during seed phase. Lunar operations have different dynamics: fewer robots, higher stakes, longer task durations, and the need to incentivize operators to deploy hardware to the Moon. What fee model aligns incentives?

- **Method:** Economic modeling of two-sided marketplace dynamics with constrained supply. Competitive analysis of high-value B2B marketplace fee structures (heavy equipment rental, satellite services). Stakeholder interviews with potential lunar robot operators.
- **Output:** Fee model proposal with operator incentive analysis.

---

## 2. Key Assumptions to Validate

These must be true for the lunar story to work. If any is false, the architecture changes significantly.

| # | Assumption | Validation method | Criticality |
|---|-----------|-------------------|-------------|
| A1 | Earth-Moon communication is available at least 80% of the time via relay infrastructure by 2030 | RQ-2 literature review | **Blocking** — if comms are sparse, robots must operate fully offline with post-hoc settlement |
| A2 | Lunar robots can run an on-board auction agent (bid engine + task executor) with available compute | RQ-4 + RQ-6 analysis of published rover compute specs | **Blocking** — if not, all coordination must happen Earth-side with massive latency |
| A3 | Multiple independent projects will deploy robots to overlapping lunar regions | Market research on Artemis program, CLPS manifests, and commercial lunar plans | **Blocking** — if each project has its own isolated fleet, there is no marketplace |
| A4 | On-chain settlement (ERC-8004 + USDC) can tolerate 3-10 second confirmation delay without breaking auction mechanics | RQ-9 technical prototype | High — determines whether we need a lunar-local settlement layer |
| A5 | Task verification can be automated without human review for lunar operations | RQ-8 analysis | High — human-in-the-loop verification adds minutes of delay per Earth-Moon round-trip |
| A6 | The ERC-8004 registry model (on-chain discovery, off-chain execution) extends to multi-body environments | RQ-9 technical analysis | Medium — may require registry sharding or mirroring |
| A7 | There will be enough robots on the Moon to create a competitive marketplace (not just bilateral contracts) | Market research, RQ-6 | **Blocking** — with only 3-5 robots on the Moon, the "marketplace" may collapse to direct assignment. The auction model assumes competition; if supply is 1-2 robots per capability, a simpler dispatch model may be more appropriate |
| A8 | The v2.0 multi-robot workflow capability is a prerequisite for meaningful lunar operations | RQ-6 task taxonomy | High — most realistic lunar tasks (site survey, construction support) are multi-step workflows, not single-shot sensor reads. If v2.0 is not built first, lunar tasks cannot be decomposed |
| A9 | Privacy requirements (from the private hiring story) do not conflict with the lunar verification model | Cross-reference with RESEARCH_PLAN_PRIVATE.md | Medium — if lunar tasks require ZKP-based verification AND high-latency tolerant verification, the intersection may be unsolvable in the near term |

---

## 3. Expected Outputs

| Output | Feeds into | Timeline |
|--------|-----------|----------|
| **Latency tolerance matrix** (RQ-1) | Architecture decision: sync vs. async auction | Week 2 |
| **Comms infrastructure summary** (RQ-2) | Assumption A1 validation | Week 2 |
| **MCP-over-DTN feasibility assessment** (RQ-3) | Protocol design | Week 3 |
| **Autonomy allocation matrix** (RQ-4) | System architecture | Week 3 |
| **Coordination architecture options paper** (RQ-5, RQ-10) | Architecture decision record | Week 4 |
| **Lunar task taxonomy** (RQ-6) | Task spec v2 design | Week 3 |
| **Revised scoring algorithm proposal** (RQ-7) | Scoring engine update spec | Week 4 |
| **Verification architecture proposal** (RQ-8) | Verification subsystem design | Week 4 |
| **Settlement architecture options paper** (RQ-9) | Payment rail design | Week 5 |
| **Lunar task pricing model** (RQ-11) | Business model | Week 5 |
| **Lunar failure recovery protocol** (RQ-13) | System architecture | Week 4 |
| **Safety constraint taxonomy** (RQ-14) | System architecture, task spec v2 | Week 3 |
| **Fee model proposal** (RQ-12) | Business model | Week 6 |
| **Go/No-Go recommendation** | Stakeholder review | Week 6 |

---

## 4. Open Questions for Stakeholders

Research alone cannot answer these. They require product, business, or strategic input.

1. **Target timeline:** Are we designing for 2028 (Artemis III timeframe), 2030, or 2035+? This determines which comms infrastructure and robot hardware we can assume.

2. **First customer profile:** Who is "Sarah" on the Moon? A NASA mission planner? A commercial mining operator? An international science consortium? The answer shapes the task taxonomy and pricing model.

3. **Regulatory posture:** The Outer Space Treaty (1967) and the Artemis Accords have implications for commercial robot operations. Do we need legal research on liability, property rights, and spectrum allocation, or is that premature?

4. **Relationship to v1.5/v2.0 roadmap:** Is the lunar extension a parallel track or a successor to v2.0 (multi-robot workflows)? Multi-robot workflows on Earth seem like a prerequisite — should we sequence accordingly?

5. **Hardware partnerships:** Are we building lunar robots, providing the marketplace software for others' robots, or both? This determines whether RQ-6 is "what can we build" vs. "what should we integrate with."

6. **Risk appetite on decentralization:** "Decentralized hiring" can mean anything from "no single point of failure" to "fully on-chain permissionless protocol." How decentralized does the first lunar version need to be?

7. **Crypto-first or crypto-optional on the Moon?** Stripe does not process payments on the Moon. Is USDC/on-chain settlement the only viable path, or do we maintain a fiat proxy for Earth-side settlement of lunar tasks?

8. **Relationship to private hiring story:** The private hiring research plan (RESEARCH_PLAN_PRIVATE.md) may require changes to the settlement chain (Base), identity model, and verification approach. If lunar tasks also need privacy (e.g., commercial mining operations that are competitively sensitive), the two stories intersect. Should the research plans be coordinated or run independently?

---

## Suggested Research Sequence

```
Week 1-2:  RQ-1, RQ-2, RQ-6 (latency bounds, comms landscape, task taxonomy)
           Validate assumptions A1, A3, A7, A8
           Cross-reference RESEARCH_PLAN_PRIVATE.md outputs if available
Week 3-4:  RQ-3, RQ-4, RQ-5, RQ-7, RQ-10, RQ-14 (protocol, autonomy, coordination, safety)
           Validate assumptions A2, A5
Week 5-6:  RQ-8, RQ-9, RQ-11, RQ-12, RQ-13 (verification, settlement, economics, failure recovery)
           Validate assumptions A4, A6, A9
           Synthesize into Go/No-Go recommendation
```

Weeks 1-2 are intentionally front-loaded with blocking assumptions. If A1, A3, or A7 fail early, we pivot the scope before investing in protocol design. A7 is particularly important: if the lunar robot population is too small for a competitive marketplace, the entire auction model may be wrong for this context.

---

## Critique and Revisions

**Reviewed:** 2026-03-26 | **Reviewer:** Engineering Director review

### Issues Found and Revisions Applied

1. **The plan assumes a marketplace exists, but the supply side may not support one (BLOCKING).** With realistic 2028-2032 lunar robot populations of 3-10 units total, the auction/marketplace model (which assumes competitive bidding from multiple capable robots) may collapse to direct bilateral assignment. The plan never asks: "Is an auction the right model for this environment?" **Revision:** Added assumption A7 as a blocking validation item. Updated RQ-5 method to include a "minimum viable decentralization" option and a centralized-with-failover baseline. A7 validation moved to Week 1-2.

2. **No safety or failure recovery research for high-stakes physical operations.** On Earth, a failed task means a missed sensor reading and $0.55 in re-pooling cost. On the Moon, a failed task could mean a destroyed $50M+ robot, damaged shared infrastructure, or an irrecoverable half-completed physical operation. The plan had zero research questions about safety constraints or failure modes unique to irreversible physical tasks. **Revision:** Added Section E (Safety, Fault Tolerance & Operations) with RQ-13 (failure recovery when no replacement robot exists) and RQ-14 (safety constraints for high-consequence tasks). Added corresponding outputs to the timeline.

3. **Task duration mismatch is unaddressed.** The entire v1.0 system is designed around 42-second tasks. Lunar tasks (site surveys, construction support, multi-day monitoring) may take hours or days. The auction lifecycle — bid collection windows, execution timeouts, auto-accept timers, wallet reservation holds — all have implicit assumptions about task duration that will break. The plan asks *what* tasks are feasible (RQ-6) but not *how the system accommodates tasks that are 1000x longer*. **Revision:** Updated RQ-6 method to require quantifying task durations and evaluating the auction lifecycle against them. Added duration ranges to the expected output.

4. **No consideration of the v2.0 prerequisite.** The roadmap shows v2.0 (multi-robot workflows) as the next milestone. Most realistic lunar tasks are inherently multi-step (survey then sample, transport then deploy). The plan treats lunar operations as if they are single-shot tasks like Earth sensor readings, but the task taxonomy (RQ-6) will almost certainly reveal that compound workflows are required. This means v2.0 is likely a hard prerequisite for any meaningful lunar deployment — yet the plan does not acknowledge this dependency. **Revision:** Added assumption A8 (v2.0 as prerequisite) with high criticality.

5. **No cross-reference to the privacy research plan.** The private hiring story (RESEARCH_PLAN_PRIVATE.md) may change the settlement chain (Base vs. a privacy chain), the identity model, and the verification architecture — all of which the lunar plan also depends on. If both stories proceed in parallel without coordination, they could produce contradictory architectural recommendations (e.g., lunar plan recommends a DTN-based settlement proxy on Base while privacy plan recommends migrating off Base entirely). Commercial lunar operations (mining, resource extraction) are also likely to be competitively sensitive, meaning privacy is not just a nice-to-have for lunar tasks. **Revision:** Added assumption A9 (privacy/lunar intersection). Added stakeholder question 8 on cross-story coordination. Updated Week 1-2 sequence to cross-reference privacy plan outputs.

6. **RQ-1 latency simulation is too clean.** The method simulates fixed RTT delays, but real Earth-Moon communication has link interruptions (relay handoff, occultation, antenna scheduling conflicts). A bid arriving during a 15-minute link outage is a fundamentally different problem than a bid arriving 4 seconds late. **Revision:** Updated RQ-1 method to include link interruption simulation and partial-failure cases in the output.

7. **RQ-5 (decentralized coordination) may be premature scope creep.** The plan invests significant research effort in fully decentralized multi-project coordination protocols (contract net, Fisher markets, on-chain order books) before validating that there will be enough independent projects and robots to warrant decentralization. With 2-3 projects and 5-10 robots in the 2028-2032 timeframe, a simple priority queue with a trusted coordinator is likely sufficient. Researching decentralized protocols before validating the market size is designing the cathedral before checking if anyone wants a chapel. **Revision:** Updated RQ-5 method to require a "minimum viable decentralization" option and include a centralized baseline. The fully decentralized designs should only be pursued if A7 validates that competitive market dynamics are realistic.

8. **Settlement research (RQ-9) is sequenced too late.** Settlement architecture is in Week 5-6, but the privacy plan recommends resolving the Base chain question *before* v1.5 ships. If the lunar settlement architecture also depends on the chain decision, and the privacy plan may force a chain migration, then RQ-9 has an upstream dependency on the privacy plan's RQ-3 and RQ-11. The current sequencing does not account for this. **Recommendation (not revised inline):** Coordinate with the privacy research timeline. If the privacy plan's Week 1 output recommends moving off Base, lunar settlement research should consume that finding rather than independently re-evaluating chain options.

9. **The "Go/No-Go" framing is too binary.** The plan culminates in a single go/no-go decision, but the realistic outcome is more nuanced: "go for which scope?" The plan should define what a *reduced* scope looks like. For example: if A3 fails (no overlapping robot fleets), the marketplace is dead, but a single-operator task dispatch system for lunar robots might still be valuable. If A7 fails (too few robots for competition), a procurement/scheduling system replaces the auction. **Recommendation:** The Go/No-Go output should include 2-3 scope tiers (full marketplace, single-operator dispatch, research-only prototype) so stakeholders can make a graduated decision.

10. **No research on the human operator role.** The plan heavily investigates autonomous on-robot agents but does not ask what the human operator's role is during lunar operations. On Earth, the operator's job is "keep robots charged, maintained, and online." On the Moon, human operators are either on-site astronauts (extremely scarce, expensive) or remote (1.3+ second delay). Who monitors the marketplace? Who handles edge cases the autonomous agents cannot resolve? Who decides to override a bad auction outcome? This gap could surface as an operational showstopper. **Recommendation:** Add a research question in Section B on the human-in-the-loop requirements for lunar marketplace operations.

### New Research Questions Added

- **RQ-13** (Section E): Failure recovery when no replacement robot exists — partial completion credits, task checkpointing, cost allocation for irrecoverable failures.
- **RQ-14** (Section E): Safety constraints for high-consequence physical tasks — safety zones, power budgets, task-level risk assessment, enforcement architecture.

### New Assumptions Added

- **A7**: Competitive marketplace viability given lunar robot population (blocking).
- **A8**: v2.0 multi-robot workflows as prerequisite for meaningful lunar operations (high).
- **A9**: Privacy story compatibility with lunar verification model (medium).
