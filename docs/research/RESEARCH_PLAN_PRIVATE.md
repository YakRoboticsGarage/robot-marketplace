# Research Plan: Private Robot Task Hiring

**User Story:** "A user who wants to hire robots but wants their activities to be both verified but private."

**Date:** 2026-03-26
**Status:** Draft — pending stakeholder review
**Estimated research duration:** 3-4 weeks

> This story introduces a fundamental tension: the platform must prove tasks were completed correctly (verifiability) while revealing nothing about what was done, by whom, or for whom (confidentiality). This is not a feature bolt-on — it may require rethinking base-layer decisions made in v1.0-v1.5.

---

## 1. Research Questions

### Domain A — Zero-Knowledge Proof Systems

**RQ-1. Which ZKP scheme fits robot task verification?**
Can a robot produce a succinct proof that it executed a task matching a hidden specification, without revealing the specification itself? Evaluate zk-SNARKs (Groth16, PLONK), zk-STARKs, and Circom/Noir circuits for proving "sensor reading X satisfies predicate Y" without exposing X, Y, or the task spec.

- **Method:** Literature review of ZKP-based computation verification (RISC Zero, SP1, Jolt). Build a toy circuit for "prove temperature reading is within range R without revealing R or the reading." Benchmark proof generation time on embedded-class hardware (ARM Cortex, RPi-class) vs. cloud prover. **Define pass/fail criteria before prototyping:** proof generation under 60s, memory under 512MB, circuit complexity manageable by one engineer in one week.
- **Key sub-question:** Can proof generation run on-robot (edge), or must it be delegated to a prover service? If delegated, does the prover become a privacy leak?

**RQ-2. What is the proof generation latency and cost for typical robot tasks?**
Sarah's current task completes in 42 seconds. Adding ZKP generation must not 10x that.

- **Method:** Prototype proof generation for 3 representative task types (sensor read, photo capture, navigation confirmation). Measure wall-clock time and memory on target hardware. Compare on-robot vs. off-robot proving. **Specify the "target hardware" concretely** — the tumbller and tello have specific compute profiles; benchmark on those, not generic RPi specs.

### Domain B — Privacy-Preserving Blockchain & Settlement

**RQ-3. Can Base/Ethereum L2 support private settlement, or does the chain choice need to change?**
Base is a transparent rollup. Every transaction, amount, sender, and receiver is public. If `request_id` is embedded on-chain (per AD-3), task-payment linkage is trivially deanonymizable.

- **Method:** Evaluate three architectures: (a) privacy overlay on Base (Aztec Connect-style shielded pool, Railgun on L2), (b) native privacy chain as settlement layer (Aztec Network, Aleo, Mina), (c) hybrid — Base for public operations + privacy chain for task settlement. Assess each for USDC support, bridge maturity, and developer tooling.

**RQ-4. Can x402 (the v1.5 crypto rail) work with shielded transactions?**
x402 embeds payment proof in HTTP headers. If the payment is shielded, can the middleware still verify payment without seeing sender/amount on a block explorer?

- **Method:** Read x402 SDK source for payment verification logic. Determine if it requires on-chain transparency or can accept a ZK payment receipt. Contact Coinbase DevRel if needed.

### Domain C — Encrypted Task Specifications

**RQ-5. How should task specs be encrypted so that only the winning robot can read them?**
Currently, `post_task()` broadcasts the full spec (hard constraints, soft preferences, payload schema) to all robots for bidding. A private task must let robots assess whether they *can* bid without revealing *what* the task is.

- **Method:** Research designs: (a) two-phase commit — post encrypted spec hash, robots bid on capability match against a public capability vector, winner gets decryption key; (b) homomorphic encryption — robots evaluate bid eligibility on encrypted spec; (c) trusted execution environment (TEE) on fleet server — spec decrypted only inside enclave. Evaluate feasibility and trust assumptions of each. **Critical gap in option (a):** The public capability vector itself may leak task intent — if the vector requests `[temperature, humidity]` in `Bay 3`, the task is effectively deanonymized regardless of spec encryption. Quantify the information leakage of the capability vector for each design.

**RQ-6. Can the 4-factor scoring algorithm run on encrypted bids?**
The scoring function (price 40%, speed 25%, confidence 20%, track record 15%) currently operates on plaintext values. Can it run under MPC or FHE so the platform scores without seeing individual bid values?

- **Method:** Prototype the scoring function in an MPC framework (MP-SPDZ, EMP-toolkit). Measure overhead vs. plaintext scoring. Determine if approximate scoring (e.g., order-preserving encryption) is acceptable. **Note:** Order-preserving encryption leaks ordering information by definition — evaluate whether this defeats the privacy goal for bids. Also assess whether MPC with 2-3 robots is even meaningful (MPC protocols assume multiple independent parties; with a small fleet, collusion is trivial).

### Domain D — Private Reputation & Scoring

**RQ-7. How can robots accumulate reputation without linking tasks to clients?**
The current model (DM-5) builds track records from task history. If task details are hidden, how does a robot prove "I completed 847 tasks with 99.2% success" without revealing which tasks, for whom, or what they involved?

- **Method:** Research anonymous credential schemes (Idemix, BBS+ signatures, zk-SNARK credential proofs). Evaluate: can a robot hold a credential that attests to aggregate stats, updated after each task, without revealing the underlying task graph? Look at Semaphore/Worldcoin's approach to anonymous group membership as a pattern.

**RQ-8. Can an auditor verify aggregate platform metrics without seeing individual tasks?**
The auditor needs: total spend, completion rate, average latency, robot utilization. They must not see: which client hired which robot, what the task was, or individual payment amounts.

- **Method:** Research homomorphic aggregation and ZK-rollup-style batch proofs. Can the platform publish a periodic "platform health proof" — a ZK proof that "N tasks completed, M USDC settled, average latency T" — verifiable by anyone, revealing nothing about individual tasks?

### Domain E — Regulatory & Compliance

**RQ-9. Does task privacy conflict with AML/KYC obligations?**
If the platform facilitates shielded payments for robot services, does it become a money transmission service operating a mixer? OFAC compliance, Travel Rule implications.

- **Method:** Legal memo from counsel familiar with crypto privacy protocols (Tornado Cash precedent, Railgun's compliance approach). Map the regulatory surface for each settlement architecture from RQ-3. Identify jurisdictions where shielded robot payments are clearly permissible vs. grey-area. **Include Finland specifically** — the seed network operates there (per TC-3), and Finnish/EU AML6 transposition may have specific requirements for privacy-preserving payments.

**RQ-10. What audit rights must be preserved for enterprise clients?**
Enterprise buyers (Sarah's employer) may require internal audit trails even if external observers cannot see them. "Private from the world, auditable by my CFO."

- **Method:** Interview 3-5 potential enterprise buyers. Determine minimum audit granularity: do they need per-task detail internally, or are aggregate reports sufficient? This shapes whether we need viewer keys, selective disclosure, or full ZK.

### Domain F — Foundational Architecture Implications

**RQ-11. Does the v1.5 chain selection (Base) need to change before shipping?**
If privacy requires a different settlement layer, building v1.5 on Base and then migrating is wasted work. Conversely, if a privacy overlay on Base is sufficient, the current plan holds.

- **Method:** Decision matrix comparing: (a) Base + privacy overlay, (b) Aztec as primary settlement, (c) dual-chain (Base public + Aztec private). Criteria: USDC liquidity, bridge risk, developer tooling maturity, latency, cost per transaction, and alignment with PD-8 (fiat accessibility).

**RQ-12. Does the identity model need to change?**
Current model: buyers have Stripe customer IDs, robots have ERC-8004 on-chain identities. For privacy, buyers may need pseudonymous or rotating identities. Does this break the wallet/ledger model from v1.0?

- **Method:** Map current identity touchpoints across all 8 journey phases. For each, determine if the identity is (a) necessarily public, (b) can be pseudonymized, or (c) must be hidden. Identify breaking changes to `SyncTaskStore`, wallet ledger, and Stripe integration.

### Domain G — UX and Adoption Risk

**RQ-13. What does the user experience look like when privacy features add latency or reduce transparency?**
Sarah currently sees "Cost: $0.35, two robots competed, the closest one won." In a private model, she may see "Cost: hidden, a robot completed your task." Does this degraded transparency reduce trust and adoption? What is the minimum information Sarah needs to feel confident the platform is working correctly?

- **Method:** Design 3 prototype result screens at different privacy levels (full detail, partial detail, zero detail). Run lightweight usability tests or structured interviews with 3-5 potential users. Identify the privacy-UX Pareto frontier.

**RQ-14. How does privacy interact with the v2.0 multi-robot workflow story?**
v2.0 introduces compound tasks where output of step N feeds into step N+1. If step N's output is encrypted for privacy, how does step N+1's robot read it? Private multi-robot handoff is a fundamentally harder problem than private single-robot tasks. Does the privacy design need to account for this now, or can it be layered later?

- **Method:** Analyze the v2.0 compound task decomposition design. Identify which data flows between robots in a chained workflow. Determine whether privacy can be added as a layer on top of plaintext handoff, or whether the handoff protocol must be privacy-aware from the start.

**RQ-15. How does privacy interact with the lunar story's requirements?**
The lunar research plan (RESEARCH_PLAN_LUNAR.md) proposes decentralized coordination, DTN-based MCP, and on-robot auction agents. Several lunar design choices have privacy implications: (a) if robots run local auction agents (lunar RQ-4), those agents see task specs in the clear — does privacy require re-centralizing coordination? (b) If settlement moves to a lunar sidechain (lunar RQ-9), does privacy need to work on that chain too? (c) Cross-robot verification (lunar RQ-8, robot B verifies robot A) directly conflicts with task privacy.

- **Method:** Cross-reference each lunar research question against the privacy threat model. Flag architectural conflicts. Determine whether privacy and lunar are independent tracks or have shared prerequisites that must be sequenced.

---

## 2. Key Assumptions to Validate

| # | Assumption | If False |
|---|-----------|----------|
| A1 | ZKP proof generation for sensor-task verification is feasible in under 60 seconds on robot-class hardware | Must use delegated proving, adding a trust assumption and latency |
| A2 | A privacy-preserving settlement layer exists that supports USDC with sufficient liquidity | May need to settle in a native token and bridge to USDC, adding exchange risk |
| A3 | Encrypted task specs can support enough information for robots to assess bid eligibility | The two-phase model may leak too much via the capability vector; may need TEEs |
| A4 | Anonymous reputation credentials can be updated incrementally without a trusted issuer | If a trusted issuer is required, the platform itself becomes the privacy bottleneck |
| A5 | Shielded payments for robot services do not trigger money transmission classification | Regulatory risk may require a compliance-first design (selective disclosure to regulators) |
| A6 | Enterprise buyers accept aggregate audit reports without per-task payment detail | If not, the privacy model must support buyer-side decryption (viewer keys), adding complexity |
| A7 | The x402 protocol can be extended or wrapped to work with shielded payments | If x402 is fundamentally tied to transparent on-chain verification, a new payment middleware is needed |
| A8 | Users actually want full cryptographic privacy, not just platform-level access controls | If users only need "don't show my tasks to other users" (ACLs), the entire ZKP/MPC/private-chain stack is massive over-engineering |
| A9 | The privacy design can be layered onto v2.0 multi-robot handoff without requiring a redesign of the handoff protocol | If not, the v2.0 architecture must be privacy-aware from inception, which changes its timeline and complexity |
| A10 | The seed network (3 warehouses, handful of robots) has enough anonymity set for privacy to be meaningful | With 2-3 robots and 1 buyer, metadata analysis trivially deanonymizes all transactions regardless of cryptographic privacy |

---

## 3. Expected Outputs

| Output | Format | Audience |
|--------|--------|----------|
| **Architecture options matrix** | Decision doc with pros/cons/costs for 3 settlement architectures | Engineering leads, CTO |
| **ZKP feasibility report** | Benchmark data + toy circuit code for sensor task verification | Engineering |
| **Privacy threat model** | Diagram of all information flows with classification (public/private/auditable) | Security, product |
| **Regulatory surface memo** | Legal analysis of shielded robot payments across US/EU/FI jurisdictions | Legal, executive team |
| **v1.5 impact assessment** | Go/no-go recommendation on Base as settlement layer given privacy requirements | CTO, product lead |
| **Private reputation design sketch** | Candidate credential scheme with update protocol | Engineering, product |
| **Revised user journey** | "Private Sarah" journey map showing all 8 phases with privacy annotations | Product, design |

---

## 4. Open Questions for Stakeholders

These cannot be resolved by research alone and require product/business decisions:

1. **Is privacy a must-have for v2.0, or is this a v3.0+ horizon feature?** If v3.0+, the v1.5 Base decision stands and we revisit chain selection later. If v2.0, we may need to change v1.5 plans *now*.

2. **What is the acceptable latency overhead for privacy?** If adding ZKP doubles task completion time (42s to 84s), is that acceptable? What about 3x? This sets the engineering constraint envelope.

3. **Is "private from other users but visible to the platform" an acceptable first step?** Full ZK (platform-blind) is much harder than platform-mediated privacy (platform sees everything, external observers don't). Which does the user story actually require?

4. **Does the fiat path (Stripe) need privacy too?** Stripe inherently knows buyer identity and payment amounts. If fiat buyers also need privacy, the architecture is fundamentally different from "just use a privacy chain for crypto."

5. **Are there specific customer conversations driving this story?** If a named enterprise prospect has stated privacy requirements, their specific needs should shape the research. If this is speculative, the research should stay broad.

6. **What is the budget tolerance for per-task privacy overhead?** ZK proofs on privacy chains cost gas. If a $0.35 task now costs $0.15 in proof/settlement fees, the unit economics change. What overhead percentage is acceptable?

---

## 5. Foundational Design Alert

**This section exists because the privacy story may force changes to decisions already shipped in v1.0 or planned for v1.5.**

### What is at risk

| Decision | Current State | Privacy Implication |
|----------|--------------|-------------------|
| **Settlement chain: Base** (v1.5, TC-4) | USDC on Base via x402 | Base is fully transparent. Every task payment is publicly linkable to buyer wallet, robot wallet, amount, and `request_id`. **Privacy is architecturally impossible on Base without an overlay or chain migration.** |
| **On-chain `request_id`** (AD-3) | Embedded in transaction memos for audit | Creates a permanent, public, immutable link between payment and task. Directly contradicts task-payment unlinkability. |
| **ERC-8004 robot identity** | Public on-chain registry | Robot identities are public and permanent. Every task acceptance is linkable to the robot's full history. Privacy requires either rotating keys or a shielded identity layer on top of ERC-8004. |
| **Buyer identity: Stripe customer ID** (TC-2, TC-3) | Stripe knows buyer identity | Even with a private chain, the fiat on-ramp (Stripe wallet top-up) links real identity to platform balance. True buyer privacy requires decoupling identity from funding. |
| **4-factor scoring on plaintext** (AD-6) | Runs in the clear | If bids or track records are encrypted, the scoring function must change to operate on encrypted data or inside a TEE. |

### Recommendation

**Do not ship v1.5 on Base until RQ-3 and RQ-11 are answered.** If the research concludes that a privacy overlay on Base is viable and sufficient, proceed with the current plan. If not, the 4 weeks allocated to v1.5 should be spent building on a privacy-native chain instead. The cost of migrating later (rewriting `RobotTaskEscrow.sol`, new wallet integration, re-onboarding operators) far exceeds the cost of choosing correctly now.

### Minimum viable investigation before v1.5 ships

1. Prototype a shielded USDC transfer on Base using Railgun or similar — does it actually work with the amounts and latency we need?
2. Deploy `RobotTaskEscrow.sol` on Aztec testnet — is the developer experience viable?
3. Get a legal opinion on shielded payment compliance in at least US and EU.

If all three are negative, privacy on a private chain is not viable and Base is fine for v1.5. If any are positive, the chain decision must be revisited before v1.5 development begins. **Note:** "All three negative" does not mean privacy is deferred — it means the *chain migration path* to privacy is not viable, which may also mean privacy itself is architecturally blocked. Distinguish between "privacy is a v3.0 feature" and "privacy is impossible with current technology." These have very different product implications.

---

## Research Schedule

| Week | Focus | Key Deliverable |
|------|-------|----------------|
| 1 | RQ-3, RQ-4, RQ-11, RQ-15 (settlement layer + cross-story conflicts) | Architecture options matrix, v1.5 go/no-go recommendation, cross-story dependency map |
| 2 | RQ-1, RQ-2 (ZKP feasibility) | Benchmark report with toy circuit |
| 3 | RQ-5, RQ-6, RQ-7, RQ-8, RQ-14 (encrypted ops + reputation + v2.0 interaction) | Privacy threat model, reputation design sketch |
| 4 | RQ-9, RQ-10, RQ-12, RQ-13 (regulatory + identity + UX) | Legal memo, revised user journey, UX privacy-transparency trade-off analysis |

Week 1 is prioritized because its output may change the v1.5 plan. If it does, engineering needs to know immediately.

**Schedule risk:** Week 3 is overloaded with 5 research questions spanning encrypted task specs, MPC scoring, anonymous credentials, homomorphic aggregation, and multi-robot privacy. These are distinct technical domains. Consider splitting Week 3 across two researchers or extending to 5 weeks.

---

## Critique and Revisions

*Added 2026-03-26 during engineering review.*

### Issues Found

1. **The plan never questions whether users actually want cryptographic privacy (A8).** The user story says "private," but that could mean ACL-based access control (trivial), platform-mediated confidentiality (moderate), or full zero-knowledge privacy (extremely hard). The plan jumps straight to ZKPs and MPC without validating the requirement level. If Sarah just wants "don't show my task history to other buyers on a dashboard," this entire plan is a $500K research project solving a $5K access control problem. **Revision:** Added assumption A8 to force this question early. Stakeholder question 3 partially covers this but needs to be the gating question before any other research begins.

2. **Anonymity set problem at seed-network scale (A10).** The plan designs privacy for a network with 2-3 robots in 3 Finnish warehouses. With such a small anonymity set, cryptographic privacy is security theater — if Bay 3 only has one robot, any task completed in Bay 3 is trivially attributed regardless of ZK proofs. Privacy only becomes meaningful at scale (dozens of robots, many buyers). The plan never addresses when the network will be large enough for privacy to matter. **Revision:** Added assumption A10. This may mean privacy research should be deferred until the network reaches minimum viable anonymity.

3. **No cross-story dependency analysis with the lunar plan.** The lunar research plan (RESEARCH_PLAN_LUNAR.md) makes several architectural choices that directly conflict with privacy: decentralized on-robot auction agents that see task specs in the clear (lunar RQ-4), cross-robot verification (lunar RQ-8), and potentially a lunar sidechain (lunar RQ-9). These two stories are being researched in parallel without any coordination on shared architectural decisions. If both ship, the architecture must support privacy AND high-latency decentralization simultaneously — a much harder problem than either alone. **Revision:** Added RQ-15 and scheduled it in Week 1 alongside the settlement layer investigation.

4. **No interaction analysis with v2.0 multi-robot workflows.** The roadmap has v2.0 (multi-robot workflows) as the next milestone. If privacy is v2.0 or v2.x, it must coexist with compound task decomposition where robot A's output feeds robot B's input. The plan never addresses how encrypted handoff works in a chained workflow. Retrofitting privacy onto a plaintext handoff protocol may be impossible. **Revision:** Added RQ-14 and scheduled it in Week 3.

5. **Week 3 is dangerously overloaded.** The original schedule packs encrypted task specs (RQ-5), MPC scoring (RQ-6), anonymous credentials (RQ-7), and homomorphic aggregation (RQ-8) into a single week. These are four distinct cryptographic research areas, each of which could consume a full week on its own. An engineer attempting all four in one week will produce surface-level assessments that miss critical feasibility issues. **Revision:** Added a schedule risk note. Recommend either splitting across two researchers or extending to 5 weeks.

6. **RQ-6 (MPC scoring) method has a logical flaw.** The plan proposes MPC for the 4-factor scoring function, but MPC requires multiple independent parties. In the current architecture, the platform is the sole scorer. MPC with 2-3 robots is meaningless — collusion between 2 of 3 parties trivially breaks MPC security guarantees. The plan also proposes order-preserving encryption as a fallback, but OPE leaks ordering by definition, which defeats bid privacy (you know who bid lowest). **Revision:** Added inline note flagging both issues in RQ-6 method.

7. **RQ-5 (encrypted task specs) misses the capability vector leakage problem.** Option (a) proposes posting a public capability vector so robots can assess bid eligibility. But the capability vector itself deanonymizes the task — requesting `[temperature, humidity]` in a specific location effectively reveals the task. The plan treats the capability vector as non-sensitive when it is the primary information leakage channel. **Revision:** Added inline note in RQ-5 method requiring capability vector information leakage quantification.

8. **The Foundational Design Alert recommendation has a logic gap.** It says "if all three [minimum viable investigations] are negative, privacy becomes a v3.0 feature and Base is fine." But all three being negative could mean privacy is architecturally impossible, not just deferred. The plan conflates "we can't build it yet" with "we'll build it later." If no privacy-preserving settlement layer works, the v3.0 plan needs a fundamentally different approach. **Revision:** Added inline clarification distinguishing "deferred" from "blocked."

9. **No UX research question.** The plan is entirely about cryptographic and architectural feasibility. It never asks whether users will accept the UX trade-offs privacy introduces: longer task times, less transparency in results, inability to compare robot performance, opaque pricing. Privacy that makes the product worse may not ship even if it is technically feasible. **Revision:** Added RQ-13 covering UX and adoption risk.

10. **Regulatory research (RQ-9) method is hand-wavy.** "Legal memo from counsel" is a deliverable, not a method. The plan does not specify: which law firm, what budget, what turnaround time, or what happens if counsel cannot be engaged within Week 4. Legal research on novel crypto privacy questions typically takes 4-8 weeks, not 1. **Recommended revision (not made inline):** Add a contingency plan — if legal counsel cannot deliver in Week 4, what interim heuristic does the team use for the go/no-go decision? Consider splitting into a quick regulatory screen (Week 1, done internally) and a deep legal memo (Weeks 4-8, external counsel).

11. **Enterprise interview method (RQ-10) assumes access to 3-5 enterprise buyers.** The plan states "interview 3-5 potential enterprise buyers" without acknowledging that the platform has zero paying customers. Recruiting enterprise buyers for privacy requirement interviews during a seed-phase startup is non-trivial and may take weeks of lead time. **Recommended revision (not made inline):** Start recruitment in Week 1, conduct interviews in Week 4. Have a fallback plan using published enterprise procurement requirements from analogous domains (cloud services, IoT platforms).

12. **Missing threat model for metadata analysis.** The plan focuses on encrypting payloads and shielding payments but never addresses metadata analysis: timing correlation (task posted at 9:14, payment at 9:14:40 — obviously linked), transaction amount correlation ($0.35 task with $0.35 payment), and network-level observation (IP addresses, MCP connection timing). Even with perfect cryptographic privacy, metadata analysis can deanonymize most transactions in a small network. **Recommended revision (not made inline):** Add a sub-question under RQ-5 or as a new RQ: "What metadata side-channels exist, and which must be mitigated for privacy to be meaningful?"

13. **The plan does not define "done."** There are expected outputs but no exit criteria. How does the team know when research is complete? What constitutes a sufficient answer to each RQ? Without pass/fail criteria, research expands indefinitely. **Recommended revision (not made inline):** Add a decision framework — for each RQ, define what answer leads to "proceed," "pivot," or "kill the feature."
