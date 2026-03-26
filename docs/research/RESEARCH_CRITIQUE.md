# Research Critique: Cross-Story Review

**Date:** 2026-03-26
**Reviewer role:** Senior technical advisor, pre-roadmap gate review
**Documents reviewed:**
- `RESEARCH_SYNTHESIS_LUNAR.md`
- `RESEARCH_SYNTHESIS_PRIVATE.md`
- `ROADMAP.md` (for context)

---

## Lunar Synthesis -- Issues Found

1. **CRITICAL: The "30 robotic landings/year" figure is misleadingly cited.** The synthesis uses NASA's target of "up to 30 robotic landings/year from 2027" to project robot populations of 15-30 by 2030+. But landings are not resident robots. Most CLPS payloads are landers with fixed payloads, not rovers. Of 30 landings, perhaps 3-5 deploy mobile robots that could participate in a marketplace. The synthesis needs to distinguish between lander payloads and mobile task-capable robots, and re-derive the population estimates accordingly. This affects the Phase 2 (2030+) competitive marketplace timeline -- it may be even later than stated.

2. **HIGH: The $42K/hour amortized pricing model uses optimistic assumptions that are presented without sensitivity analysis.** The model assumes 8 productive hours per lunar day, 24 operational lunar days over a 2-year life, and a 5 kg rover. These are all best-case. A CubeRover is unlikely to survive 24 lunar day/night cycles (the synthesis itself notes most rovers cannot survive lunar night). If the rover survives only 6 lunar days, the amortized cost is $167K/hour. The synthesis should include a pessimistic scenario (6 lunar days, 4 productive hours/day) and a realistic scenario alongside the optimistic one.

3. **HIGH: "Centralized Earth-side coordinator" is recommended without addressing the trust problem it creates.** If NASA, ESA, and JAXA robots share a coordinator, who operates it? The synthesis dismisses decentralization as premature for 3-10 robots but does not address why independent space agencies would trust a single operator's coordinator with scheduling their $50M+ assets. At minimum, the synthesis should outline what governance or transparency guarantees the coordinator must offer (e.g., auditable scheduling logs, open-source scheduling algorithm, multi-party oversight). "Decentralize later" is not a trust model.

4. **HIGH: DTNB and DTN blockchain research is cited as evidence of feasibility, but neither prototype has been tested at Earth-Moon latency.** The DTNB paper (IEEE 2021) and Ethereum delay-tolerant payment scheme (IEEE 2019) are simulations or terrestrial DTN experiments. The synthesis says "blockchain settlement over DTN links is an active research area with working prototypes" -- this overstates the evidence. Revise to: "simulated prototypes exist but none have been tested on actual cislunar links." This matters because real DTN link characteristics (variable bandwidth, relay scheduling, custody transfer failures) introduce failure modes not captured in simulations.

5. **MEDIUM: The task taxonomy conflates "demonstrated" with "feasible."** The table lists site imaging/survey as "Near-term (2026-2028)" and cites JAXA LEV-2 as evidence. But LEV-2 performed a pre-programmed photo operation from a fixed position, not a marketplace-dispatched survey task. The gap between "a rover took a photo autonomously" and "a rover accepted a market-dispatched survey task, navigated to a specified location, completed a survey, and submitted a structured proof" is enormous. The feasibility tier should reflect the full marketplace-integrated task, not just the raw physical capability.

6. **MEDIUM: Lunar night constraint is noted but not carried into the economic model.** The synthesis identifies 14-day lunar night as a dominant constraint and says most rovers cannot survive it. But the economic model assumes a 2-year useful life (24 lunar days). If rovers cannot survive lunar night, their useful life is a single 14-day lunar day unless they are placed in a permanently illuminated region (south pole peaks of eternal light). The synthesis should explicitly address whether the economic model assumes night survival or permanent illumination, and note that permanently illuminated sites are extremely limited in area and will be contested.

7. **MEDIUM: The cross-robot attestation pattern is recommended for high-value tasks without addressing incentive problems.** If Robot B is asked to verify Robot A's work, what prevents collusion (both robots belong to the same operator) or free-riding (Robot B has no incentive to spend energy and time verifying)? The synthesis should note that cross-robot attestation requires independent operators and an explicit incentive mechanism (verification bounty or protocol-mandated verification duty).

8. **LOW: The RAD750 comparison to "a late-1990s desktop" is misleading for software feasibility assessment.** The RAD750 runs at 400 MIPS but has 256 MB RAM, runs VxWorks, and has no standard library ecosystem. Saying it's "comparable to a late-1990s desktop" makes it sound like you could run a stripped-down Python script on it. The constraint is not just MIPS -- it's the entire software environment. Clarify that the on-board agent must be bare-metal C or a minimal Rust binary, not just "lightweight."

9. **LOW: Source for "NASA targeting up to 30 robotic landings/year" is nextbigfuture.com and wusf.org.** These are secondary/tertiary sources that may be interpreting NASA statements loosely. If this figure drives marketplace sizing assumptions, it needs a primary NASA source (budget document, program plan, or official press release). If no primary source exists, the figure should be flagged as unconfirmed.

---

## Privacy Synthesis -- Issues Found

1. **CRITICAL: The Aleo + USDCx recommendation has a fatal regulatory contradiction.** The synthesis recommends Aleo as the "strongest option" for privacy settlement (Finding 2, Architecture Recommendation 3). But Finding 5 and Domain E conclude that EU AMLR Article 79 bans CASPs from handling privacy-preserving digital assets by 2027, and the seed network operates in Finland. The synthesis tries to resolve this by saying Aleo is "for non-EU markets" -- but the roadmap has no non-EU markets planned. There is no identified user for the Aleo rail. The synthesis should either (a) identify a concrete non-EU deployment scenario that justifies Aleo integration work, or (b) downgrade Aleo from "recommended" to "monitor" and redirect that engineering effort toward platform-mediated privacy on Base, which is the only EU-viable path.

2. **HIGH: The "1-5 second" proof time estimate for robot tasks is extrapolated, not measured.** The synthesis says: "estimated proof time for a simple robot task: 1-5 seconds (extrapolating from Eth block benchmarks)." An Ethereum block proof involves 143 transactions and 32M gas. A "temperature in range" circuit involves 10K-100K cycles. The extrapolation assumes linear scaling from Eth block complexity to robot task complexity, which is incorrect -- proof generation has significant fixed overhead (circuit compilation, witness generation, memory allocation) that does not scale linearly with circuit size. The actual proof time for a trivial circuit on SP1 could be 0.5s or could be 8s. This needs a benchmark, not an extrapolation. Add a task: "build a minimal SP1 circuit for sensor range verification and measure actual proving time on Succinct Prover Network."

3. **HIGH: The capability vector leakage problem is identified but the proposed mitigations are inadequate.** The synthesis proposes "generalized capability classes" and "dummy tasks / chaff." Generalized classes reduce matching efficiency (the synthesis acknowledges this). Chaff increases network load and cost on systems where every watt matters (especially for lunar, see cross-story section). The TEE-based matching solution is noted as the pragmatic answer, but the synthesis does not address what happens when TEE trust is compromised (side-channel attacks on SGX are well-documented). Add a fallback plan for TEE compromise and note that the capability vector problem remains fundamentally unsolved for the zero-trust case.

4. **HIGH: BBS+ threshold issuance "requires 3+ platform nodes" -- but the seed network is a single-operator platform.** The synthesis recommends threshold BBS+ to avoid a single trusted issuer (A4 validation). But at seed scale, who runs the 3+ nodes? If the platform operator runs all of them, threshold issuance provides no meaningful trust distribution. The synthesis should specify at what scale threshold issuance becomes real (e.g., when there are 3+ independent operators willing to run issuer nodes) and acknowledge that at seed scale, the platform is the trusted issuer whether or not the credential scheme is "threshold."

5. **MEDIUM: The z402 and ZK-X402 projects are cited without maturity assessment.** The synthesis mentions these as evidence that x402 can be adapted for privacy, but provides no information about their contributor count, production deployments, audit status, or maintenance activity. "Community projects" could mean anything from a single-developer experiment to an active multi-team effort. Add: number of contributors, last commit date, whether there is a deployed instance, and whether the code has been audited. If this information is not available, state clearly that these are unvalidated prototypes.

6. **MEDIUM: The "remove request_id from on-chain memos" recommendation (AD-3) contradicts the v1.5 roadmap deliverable.** The roadmap explicitly lists "request_id embedded in on-chain transaction memos for audit (per AD-3)" as a v1.5 key deliverable and success criterion. The privacy synthesis recommends removing it. This is a direct conflict that must be resolved before user journey writing. The synthesis should acknowledge the conflict, explain why the privacy concern overrides the audit benefit, and propose an alternative audit mechanism (e.g., platform-side audit log with cryptographic commitment on-chain).

7. **MEDIUM: The claim that "privacy features only become meaningful at scale" (A10 validation) is not fully accurate.** Even with 2-3 robots, there are privacy properties worth protecting: task pricing (competitors shouldn't see what you pay for robot services), task content (what you're sensing and where), and buyer identity (who is hiring robots). These are business-sensitive even in a 3-robot network. The anonymity set argument applies to transaction unlinkability but not to payload confidentiality. The synthesis should distinguish between anonymity (requires scale) and confidentiality (valuable at any scale).

8. **LOW: The Mina assessment ("market cap collapsed, team reduced 60%") may be outdated.** Market cap is volatile and team size can recover. If Mina is being dismissed, cite structural technical limitations (limited smart contract capability, no USDC path) rather than market conditions that could change. The technical limitations alone are sufficient to justify "not viable."

---

## Cross-Story Dependencies

### 1. Lunar operations need privacy -- and neither synthesis addresses this adequately

The lunar synthesis flags this in assumption A9 ("INCONCLUSIVE -- Not enough data to assess") and then drops it. But the scenario is concrete: if Intuitive Machines and Astrobotic both have rovers at the lunar south pole, Intuitive Machines does not want Astrobotic to see what sites it is surveying, what resources it is prospecting, or how much it is paying for robot services. Competitive intelligence from on-chain task history could reveal prospecting strategies worth billions.

**What to add to the lunar synthesis:** A section on "competitive sensitivity of lunar task data" that explicitly identifies which task metadata is commercially sensitive (location, task type, timing patterns, pricing) and requires that the task spec and settlement design support confidentiality for these fields from day one -- even in the centralized coordinator model. This is not about ZK proofs on the Moon; it's about not publishing commercially sensitive data to a public blockchain from the Earth-side coordinator.

**What to add to the privacy synthesis:** A section on "privacy requirements for multi-operator environments beyond the seed network" that treats the lunar scenario as a concrete privacy use case. The TEE-based coordinator model from the privacy synthesis maps directly onto the centralized Earth-side coordinator from the lunar synthesis -- but neither document makes this connection.

### 2. The privacy story needs delay tolerance -- and doesn't acknowledge it

The privacy synthesis assumes low-latency interactions throughout: TEE proving latency of "1-5 seconds," sub-100ms MPC for sealed bids, near-real-time credential updates after each task. None of this accounts for a DTN environment where messages take seconds to hours to arrive. Specific gaps:

- **TEE-backed proving over DTN:** The robot sends encrypted witness data to a TEE prover on Earth. Over DTN, this bundle may arrive hours after the task completed. The proof generation then adds 1-5 seconds. But the result must be relayed back via DTN. Total latency for a verified private proof: potentially days, not seconds. The privacy synthesis should model the full round-trip proof lifecycle under DTN conditions.
- **BBS+ credential updates over DTN:** After a lunar task completes, the credential update (reissue by threshold issuers on Earth) must be relayed back to the robot via DTN. Until the robot receives its updated credential, it is presenting stale reputation data. The privacy synthesis should address credential staleness under intermittent connectivity.
- **Async settlement with privacy:** The lunar synthesis recommends batched async settlement. The privacy synthesis recommends Privacy Pools-style compliant privacy. These need to be reconciled: can a batched settlement transaction include Privacy Pools association proofs? What is the proof generation overhead per batch?

### 3. Shared infrastructure that both stories need but neither fully specifies

**Settlement abstraction layer:** Both syntheses recommend a settlement abstraction. The lunar synthesis wants it for DTN-tolerant batched settlement. The privacy synthesis wants it for chain optionality (Base vs. Aleo). These are the same abstraction layer, but with different interface requirements. The settlement abstraction must support: (a) immediate settlement (Earth, Base), (b) batched async settlement (lunar, DTN), (c) transparent settlement (Base), and (d) private settlement (Aleo or Privacy Pools). Neither synthesis specifies this combined interface. Write it.

**Reputation system:** The lunar synthesis mentions reputation as a scoring factor (Domain C) but does not specify the credential model. The privacy synthesis specifies BBS+ credentials in detail but only for the Earth seed network. These need to be unified: the same BBS+ credential model should work for both Earth robots (low-latency updates, small anonymity set) and lunar robots (high-latency updates, stale credentials acceptable, commercially sensitive task history). The credential schema and update protocol must be designed once, not twice.

**DTN protocol layer:** The lunar synthesis specifies DTN/Bundle Protocol for all Moon-Earth communication. The privacy synthesis does not mention DTN at all. But if privacy features (encrypted task specs, ZK proofs, credential updates) are carried over DTN links, the Bundle Protocol integration must handle encryption, proof bundling, and credential transport. This is shared infrastructure that should be designed as a single DTN message protocol, not bolted on separately by each feature team.

---

## Foundational Design Consensus

Reconciling the two syntheses' recommendations into a unified view:

### Chain Selection

Both syntheses converge on **Base for the near term**, but for different reasons:
- Lunar: Base is fine because the first deployment is a centralized coordinator; chain selection barely matters for v1.
- Privacy: Base is fine because EU regulations prohibit the fully private alternatives anyway.

**Unified position:** Base is the settlement chain for v1.5 through v2.0. Aleo is a monitoring target, not a build target, until (a) a non-EU market is identified that needs cryptographic privacy and (b) Aleo's ecosystem matures further. Do not invest engineering time in Aleo integration until both conditions are met. This contradicts the privacy synthesis's "design for Aleo migration at v2.x" recommendation -- that recommendation should be downgraded to "design a settlement abstraction that does not preclude future Aleo integration."

### Identity Model

The two syntheses have an unresolved tension:
- Lunar: ERC-8004 registry with DTN-tolerant discovery proxy, cached locally on Moon-side.
- Privacy: ERC-8004 is a "privacy liability" because it creates permanent on-chain identity links. BBS+ credentials should sit on top as a selective-disclosure layer.

**Unified position:** ERC-8004 remains the identity anchor (it's already built into v1.0). For Earth operations, add BBS+ selective disclosure as a privacy layer in v2.0. For lunar operations, the ERC-8004 registry is cached Moon-side via DTN with a sync protocol. The privacy concern about on-chain identity linkage is real but is a v2.0 problem -- at seed scale, every participant knows every other participant anyway. The design change for v1.5 is: do not add new on-chain metadata fields to ERC-8004 entries (the privacy synthesis's recommendation to not expose wallet addresses in the API is correct and should be implemented).

### Settlement Architecture

- Lunar: Batched async settlement via Earth-side proxy, posting to L1 during comm windows.
- Privacy: Settlement abstraction supporting transparent (Base) and private (future) rails.

**Unified position:** Build a single settlement abstraction with four modes:
1. **Immediate transparent** (Base, x402) -- for Earth v1.5
2. **Immediate private** (future, Privacy Pools on Base or Aleo) -- for Earth v2.x when legally viable
3. **Batched transparent** (Base, DTN-tolerant) -- for lunar Phase 0-1
4. **Batched private** (future) -- for lunar Phase 2 when privacy + DTN is solved

The abstraction interface should be designed in v1.5 even though only mode 1 is implemented. This is the privacy synthesis's recommendation and it is correct. The lunar synthesis should adopt it explicitly rather than specifying a separate "Earth-side settlement proxy."

---

## Recommended Revisions

### Lunar Synthesis

1. **Add a sensitivity analysis to the economic model (Domain E).** Include pessimistic (6 lunar days, 4 hours/day, single rover), realistic (12 lunar days, 6 hours/day), and optimistic (24 lunar days, 8 hours/day) scenarios. State assumptions about lunar night survival and site illumination explicitly.

2. **Rewrite the "30 landings/year" population projection (Domain C).** Distinguish between lander payloads and mobile task-capable robots. Provide a revised estimate of mobile robot population at the south pole by year (2027, 2028, 2029, 2030). Cite primary NASA sources if available; flag the figure as unverified if not.

3. **Add a governance section to Architecture Recommendation 1.** The centralized coordinator recommendation must address: who operates it, what transparency guarantees it provides, what happens if the operator is compromised or biased, and how the transition to decentralized operation is triggered.

4. **Add a "competitive sensitivity" subsection to Domain D or a new section.** Address which task metadata is commercially sensitive in a multi-operator lunar environment and what confidentiality guarantees the coordinator must provide. Reference the privacy synthesis's TEE-based confidential compute model as the recommended approach.

5. **Downgrade DTNB and DTN blockchain evidence from "working prototypes" to "simulated prototypes."** In Domain D, second paragraph, change "active research area with working prototypes" to "active research area with simulation-validated prototypes." Add a note that no cislunar testing has occurred.

6. **Add cross-robot attestation incentive design to Domain D implications.** Note that attestation requires independent operators and an explicit incentive mechanism. Propose a verification bounty funded from the task fee.

### Privacy Synthesis

1. **Resolve the Aleo regulatory contradiction.** Either identify a concrete non-EU deployment scenario or downgrade Aleo from "recommended path for v2.x" to "monitoring target." Replace the dual-chain recommendation with: "design a settlement abstraction that supports future chain additions without committing to Aleo integration work."

2. **Resolve the request_id conflict with the roadmap.** Explicitly acknowledge that the recommendation to remove request_id from on-chain memos contradicts ROADMAP.md v1.5 deliverables and AD-3. Propose a replacement: a cryptographic commitment (hash of request_id) on-chain that proves linkage without revealing the ID, with the plaintext mapping stored off-chain.

3. **Add a DTN compatibility section.** For each privacy mechanism recommended (TEE proving, BBS+ credentials, Privacy Pools settlement), describe how it behaves under DTN conditions: what is the full round-trip latency, what happens during link outages, what is the credential staleness model. This does not need to solve all problems -- it needs to identify which problems exist.

4. **Benchmark the SP1 proof time claim.** Replace the extrapolated "1-5 seconds" with either (a) an actual measurement from a minimal SP1 circuit, or (b) an explicit disclaimer that this is an untested extrapolation with a recommended task to benchmark it. Do not present extrapolated figures as estimates without qualification.

5. **Add TEE compromise fallback to Domain C.** The TEE-based task matching recommendation should include: what happens if a SGX/TDX side-channel vulnerability is disclosed? What is the degraded-mode operation? (Answer: fall back to generalized capability classes with reduced matching efficiency, notify affected parties, rotate enclave keys.)

6. **Distinguish anonymity from confidentiality in the A10 validation.** The current text says privacy is meaningless at small scale. Correct this to: transaction unlinkability requires a larger anonymity set, but payload confidentiality (task content, pricing) is valuable at any scale. Recommend that v1.5 implement payload confidentiality (encrypted task specs in the API, platform-internal only) even before cryptographic privacy is viable.

### Both Syntheses

1. **Add a shared "Settlement Abstraction Interface" section** (or create a separate short document) that specifies the four settlement modes (immediate/batched x transparent/private) and defines the interface that both the Earth v1.5 and lunar Phase 0 implementations must satisfy.

2. **Unify the reputation model.** The privacy synthesis's BBS+ credential design and the lunar synthesis's reputation scoring factors should be reconciled into a single credential schema that supports both environments. The credential should include: task count, success rate, average completion time, capability attestations, and (for lunar) environmental survival history. The update protocol should handle both low-latency (Earth) and high-latency (DTN) credential reissuance.

3. **Create a shared risk: "regulatory uncertainty on compliant privacy."** Both syntheses depend on the EU AMLR Article 79 interpretation. The privacy synthesis flags this but treats it as a privacy-story risk. It is equally a lunar-story risk (lunar operators in ESA member states face the same regulation). Elevate this to a cross-story risk with a single mitigation: obtain legal opinion before v2.0 architecture is finalized.
