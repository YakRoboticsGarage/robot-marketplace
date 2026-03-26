# Research Synthesis: Private Robot Task Hiring

**Date:** 2026-03-26
**Status:** Complete -- pending engineering review
**Research plan:** [RESEARCH_PLAN_PRIVATE.md](RESEARCH_PLAN_PRIVATE.md)

---

## Key Findings (Executive Summary)

1. **On-robot ZK proof generation is infeasible on current robot hardware.** RISC Zero requires a minimum of 16 GB RAM for local proving. The tumbller and tello-class robots have nowhere near this. Delegated proving is mandatory, but new TEE-based private proving services (Succinct/Phala) can keep witness data hidden from the prover, mitigating the privacy leak concern.

2. **Aleo with USDCx is the most mature privacy-native stablecoin option.** Circle launched USDCx (1:1 USDC-backed) on Aleo mainnet in January 2026. This is a production-grade, privacy-by-default stablecoin with institutional backing -- a material change from the landscape assumed when v1.5 was planned.

3. **Railgun does NOT currently support Base.** Supported chains are Ethereum, BSC, Polygon, and Arbitrum. The assumption that a privacy overlay on Base could work via Railgun is currently invalidated. Horizen launched a privacy L3 on Base in Q4 2025 using TEEs, but its approach is TEE-based confidential compute, not cryptographic privacy.

4. **The x402 protocol is fundamentally tied to transparent on-chain settlement** via EIP-3009 (transferWithAuthorization). The facilitator must see the signed authorization and execute it on-chain. However, z402 (a community fork) and ZK-X402 projects have emerged that pair x402's HTTP flow with shielded settlement on Zcash and other privacy chains. x402 V2 is in development with broader scheme support.

5. **EU AMLR Article 79 will ban CASPs from handling privacy-preserving digital assets by July 2027.** This is the single most important regulatory constraint. Finland's transition period ended June 2025, making it an early enforcer. Fully shielded robot payments operated by a CASP in the EU are likely illegal under the incoming framework. Compliant privacy (selective disclosure, Privacy Pools) is the only viable path.

6. **Tornado Cash sanctions were lifted in March 2025**, with the Fifth Circuit ruling that immutable smart contracts cannot be classified as "property" under IEEPA. This is favorable precedent for privacy protocol developers, but does not affect the EU AMLR ban, and the Roman Storm criminal trial (money laundering, unlicensed money transmission) remains pending.

7. **Privacy Pools (0xbow) represent the "compliant privacy" paradigm.** Launched on Ethereum mainnet March 2025, backed by Vitalik Buterin and integrated into the Ethereum Foundation's Kohaku wallet. Uses association sets to prove funds are not from sanctioned sources while preserving transaction privacy. Not yet on Base, but expanding to other chains.

8. **BBS+ signatures are standardization-ready for anonymous credentials.** IRTF and W3C standardization efforts are active, with 2025-2026 papers addressing threshold issuance (no single trusted issuer), hardware integration (ECDSA augmentation for HSM compatibility), and privacy-preserving revocation. This is the most mature solution for anonymous robot reputation.

9. **FHE remains impractical for real-time scoring.** 4-5 orders of magnitude slowdown vs. plaintext computation. MPC for sealed-bid auctions is more viable -- recent work achieves sub-100ms for 100-bidder auctions using PSI-based approaches -- but the small fleet size (2-3 robots) makes MPC collusion-trivial, as the research plan's critique noted.

10. **The foundational chain decision is: stay on Base for v1.5, design for Aleo migration at v2.x, and use compliant privacy (Privacy Pools pattern) as the bridge.** A dual-chain approach is premature given tooling maturity. Aztec is not yet processing transactions on mainnet. Aleo + USDCx is the strongest privacy-native option but needs more ecosystem maturity.

---

## Domain A: Zero-Knowledge Proof Systems

### What We Learned

**Proof system landscape (RQ-1):**

| System | Type | Proof Time (Eth block) | Trusted Setup | Proof Size | Best For |
|--------|------|----------------------|---------------|------------|----------|
| Groth16 | zk-SNARK | Fastest per-circuit | Yes (per-circuit) | ~200 bytes | Repeated proofs, same circuit |
| PLONK | zk-SNARK | 2.25x slower than Groth16 | Universal | ~500-1000 bytes | Multiple circuit types |
| RISC Zero (R0VM 2.0) | zk-STARK via zkVM | 44s for Eth block (was 35 min) | No | Larger | General computation |
| SP1 Hypercube | zk-STARK via zkVM | 10.8s for Eth block (16 GPUs) | No | ~1MB | General computation, speed |

**Hardware feasibility (RQ-2):**
- RISC Zero minimum: **16 GB RAM** for local proof generation. This immediately disqualifies on-robot proving for tumbller/tello class hardware.
- SP1 Hypercube real-time proving requires 16x NVIDIA RTX 5090 GPUs (~$100K cluster). Even simple computations need multi-GB RAM and GPU acceleration for reasonable times.
- Compiler optimizations yield 17-22% improvement (SP1/RISC Zero), but the base requirements remain far above embedded hardware.
- **Delegated proving is mandatory.** The question is whether delegated proving leaks privacy.

**Private delegated proving:**
- Succinct launched **Private Proving** on Phala Cloud's TEE infrastructure in 2025. SP1 runs inside confidential VMs where neither the prover operator nor cloud provider can access private inputs.
- TEE overhead converges to <20% for compute-intensive tasks like zkVM proving -- effectively negligible.
- This solves the delegated-prover privacy leak: the robot sends encrypted witness data to a TEE-backed prover that generates the proof without seeing the inputs.
- Trust assumption shifts from "trust the prover" to "trust the TEE hardware" (Intel SGX/TDX, NVIDIA H200). This is a weaker assumption than trusting the platform itself.

**Proof generation for robot tasks:**
- A simple sensor verification circuit ("temperature in range R") would be far less complex than an Ethereum block proof. Estimated cycle count: 10K-100K cycles vs. 32M gas/143 tx for an Eth block.
- Using delegated SP1 proving with TEE, estimated proof time for a simple robot task: **1-5 seconds** (extrapolating from Eth block benchmarks, which take 10.8s for vastly more complex computation).
- This is well within the 60-second target from A1.

### Implications for Architecture

1. **On-robot proving is off the table.** All ZK proof generation must be delegated to a cloud prover service.
2. **TEE-backed private proving (Succinct/Phala model) is the correct pattern.** Robot sends encrypted task witness to TEE prover; prover generates proof without seeing plaintext.
3. **SP1 is preferred over RISC Zero** for this use case: no trusted setup, better performance, established private proving infrastructure.
4. **The proof generation service becomes infrastructure, not a privacy bottleneck.** Budget for Succinct Prover Network usage or self-hosted TEE provers.
5. **Proof times for robot tasks (1-5s) add acceptable latency to the 42s task completion.** Total overhead ~5-12%, well under the "don't 10x it" threshold.

---

## Domain B: Privacy-Preserving Settlement

### What We Learned

**Base privacy assessment (RQ-3):**

Base is a transparent optimistic rollup. There is **no native privacy capability** and no immediate path to one. Assessment of overlay options:

| Option | Status | USDC Support | Verdict |
|--------|--------|-------------|---------|
| Railgun on Base | **Not deployed.** Supports Ethereum, BSC, Polygon, Arbitrum only. | Yes (on supported chains) | Not viable for Base |
| Privacy Pools (0xbow) on Base | Not deployed. Ethereum mainnet only. Expanding to BNB Chain Q1 2026. | ETH, WBTC, USDC, DAI on Ethereum | Not yet viable for Base |
| Horizen L3 on Base | **Live on mainnet** Q4 2025. TEE-based confidential compute. | Not confirmed for USDC | Possible but TEE-based, not cryptographic privacy |
| Aztec (separate L2) | Ignition Chain live Nov 2025. Empty blocks only. Transactions expected early 2026. | Planned, not yet live | Immature; not Base-compatible |

**Privacy-native chain assessment:**

| Chain | Privacy Model | USDC Status | Maturity | Verdict |
|-------|--------------|-------------|----------|---------|
| **Aleo** | ZK by default (Leo/snarkVM) | **USDCx live on mainnet Jan 2026** (Circle xReserve, 1:1 USDC) | Production mainnet, expanding tooling | **Strongest option** |
| Aztec | ZK rollup on Ethereum | Planned but not live | Mainnet has empty blocks; transactions "early 2026" | Too immature for v1.5-v2.0 timeline |
| Mina | Lightweight ZK blockchain | No native USDC support | Market cap collapsed ($64M); team reduced 60% | **Not viable** -- project at risk |
| Zcash | Shielded transactions | No native USDC | Mature privacy but limited smart contract capability | Viable for payments only, not programmable |

**x402 compatibility (RQ-4):**

x402 is architecturally dependent on transparent settlement:
- Payment authorization uses **EIP-3009** (transferWithAuthorization) -- a signed message that a facilitator submits as a public on-chain transaction
- The facilitator **must see** the authorization parameters (sender, recipient, amount, nonce) to execute and verify settlement
- The on-chain transaction is fully transparent and linkable

**However, privacy extensions exist:**
- **z402** (z402.cash): Pairs x402's HTTP 402 flow with Zcash shielded transactions. A "Zcash Facilitator" generates single-use shielded addresses and verifies payment via zk-SNARKs without seeing transaction details.
- **ZK-X402** (zk-x402.tech): Privacy relayer for P2P transactions with ZK attestations and instant verification.
- **x402 V2** is in development with broader scheme support, potentially opening the door for privacy-native payment schemes.

These are community projects, not Coinbase-official. Maturity is low but the pattern is proven.

### Implications for Architecture

1. **Base cannot support private settlement without a privacy overlay, and no mature overlay exists on Base today.** The plan to use x402 + USDC on Base for v1.5 is fine for a transparent MVP, but architecturally incompatible with privacy.
2. **Aleo + USDCx is the most credible privacy settlement path.** Circle's institutional backing de-risks the stablecoin peg. The bridge (xReserve) is production-grade.
3. **x402 can be adapted for privacy** via the z402/ZK-X402 pattern, but this requires building or adopting a privacy-aware facilitator. This is non-trivial engineering.
4. **The dual-chain approach (Base for public + Aleo for private) is the pragmatic path.** v1.5 ships on Base with transparent x402. v2.x adds Aleo as an optional private settlement rail. Users choose their privacy level.
5. **Aztec is worth monitoring but not ready.** If Aztec reaches transaction-capable mainnet in 2026 with USDC bridge support, it may become viable for v3.0+. Its Noir language and Ethereum L2 nature are attractive.

---

## Domain C: Encrypted Task Specifications

### What We Learned

**Task spec encryption (RQ-5):**

The research plan identifies three approaches. Assessment:

| Approach | Feasibility | Privacy Leak | Complexity |
|----------|------------|-------------|------------|
| Two-phase commit (encrypted spec, public capability vector) | High | **Critical:** capability vector deanonymizes task. Requesting [temperature, humidity, Bay 3] reveals the task. | Low |
| Homomorphic encryption (robots evaluate encrypted spec) | Low | Minimal if done correctly | Very high; FHE is 4-5 orders of magnitude slower |
| TEE on fleet server | Medium | Minimal; spec decrypted only inside enclave | Medium; requires TEE infrastructure |

The capability vector leakage problem (identified in the plan's critique) is the fundamental challenge. Even with encrypted specs, the *shape* of what's requested reveals intent.

**Possible mitigations for capability vector leakage:**
- **Generalized capability classes** rather than specific vectors (e.g., "environmental sensing" rather than [temperature, humidity])
- **Broadcast all tasks to all robots** and let robots self-select inside a TEE or via local ZK proof of capability match
- **Dummy tasks / chaff** to obscure real task patterns (expensive, increases load)

**Encrypted scoring (RQ-6):**

| Technique | Performance | Privacy | Fleet-size Problem |
|-----------|------------|---------|-------------------|
| FHE scoring | 4-5 orders of magnitude slower | Strong | N/A |
| MPC (MP-SPDZ) | Sub-100ms for 100 bidders (PSI-based) | Strong with enough parties | **Collusion-trivial with 2-3 robots** |
| Order-preserving encryption | Fast | **Leaks ordering** -- defeats bid privacy | N/A |
| TEE-based scoring | Near-plaintext speed | Platform-mediated (TEE trust) | Works at any fleet size |

**Verdict:** For seed-network scale (2-3 robots), **TEE-based scoring** is the only practical option. MPC becomes meaningful at 10+ independent robots. FHE is not viable for real-time scoring in any foreseeable timeframe.

### Implications for Architecture

1. **TEE-based task handling is the pragmatic v2.x approach.** Fleet server runs a TEE enclave that receives encrypted task specs, matches against robot capabilities, scores bids, and reveals only the winning assignment. The platform-as-TEE sees data inside the enclave but cannot exfiltrate it.
2. **This is "platform-mediated privacy" (stakeholder question 3), not full ZK.** Acceptable as a first step, with a path to ZK scoring when fleet sizes grow.
3. **The capability vector leakage problem must be addressed in the task posting protocol.** Recommend generalized capability classes + noise/chaff for the initial design.
4. **FHE scoring should be deferred to v4.0+ or later.** The performance gap is too large.

---

## Domain D: Private Reputation & Scoring

### What We Learned

**Anonymous credentials (RQ-7):**

BBS+ signatures are the leading solution:
- **IRTF standardization** is underway (draft-irtf-cfrg-bbs-signatures)
- **W3C Verifiable Credentials** working group uses BBS+ for selective disclosure
- Key capabilities: prove knowledge of a signature while selectively disclosing any subset of signed messages
- A robot can hold a credential attesting to "847 tasks, 99.2% success rate" without revealing which tasks, for whom, or what they involved
- **Threshold BBS+** (2023-2025 papers) enables distributed credential issuance -- no single trusted issuer needed, addressing assumption A4
- **Hardware integration** (2026 paper): BBS+ credentials can be augmented with conventional ECDSA signatures, enabling use with HSMs that don't yet support BBS natively

**Semaphore protocol:**
- Proves anonymous group membership ("I am a registered robot on this platform") without revealing which robot
- Prevents double-signaling (a robot can't claim the same task completion twice)
- Part of Ethereum Foundation's PSE initiative; actively maintained
- Useful for anonymous group membership but less suited for aggregate statistics

**Anonymous audit (RQ-8):**
- **Homomorphic aggregation** can produce "N tasks completed, M USDC settled" without revealing individual records
- **ZK batch proofs** (rollup-style) can prove aggregate platform metrics
- The Privacy Pools (0xbow) model demonstrates this pattern: proving aggregate fund provenance without revealing individual transactions

**Credential update protocol:**
- After each task, the platform (or a distributed issuer set) updates the robot's credential with new aggregate stats
- BBS+ supports efficient credential re-issuance
- With threshold issuance, multiple platform nodes can jointly issue updated credentials without any single node seeing the full history

### Implications for Architecture

1. **BBS+ is the recommended credential scheme for robot reputation.** Mature, standardizing, supports the exact use case (aggregate stats without individual records).
2. **Threshold BBS+ issuance addresses the trusted-issuer concern (A4).** Requires 3+ platform nodes for distributed issuance -- viable even at seed scale.
3. **Semaphore can complement BBS+ for group membership proofs** ("prove you're a registered robot without revealing which one") but is not sufficient alone for reputation.
4. **Platform health proofs (aggregate metrics) are feasible** using ZK batch proofs or homomorphic aggregation. This is a v2.0+ feature, not v1.5.
5. **ERC-8004 robot identity is a privacy liability.** Public on-chain registry links every task to a permanent robot identity. For privacy, robots need either rotating keys or a shielded identity layer. BBS+ credentials can sit atop ERC-8004 as a selective-disclosure layer.

---

## Domain E: Regulatory & Compliance

### What We Learned

**US regulatory landscape:**
- **Tornado Cash delisted by OFAC March 2025.** Fifth Circuit ruled immutable smart contracts are not "property" under IEEPA. Favorable precedent for privacy protocol builders.
- **Roman Storm trial** (July 2025): charges include money laundering, sanctions violations, operating unlicensed money-transmitting business. Outcome will set precedent for whether privacy protocol developers face criminal liability.
- **Privacy Pools approach** (0xbow) is explicitly designed to be "compliant privacy" -- proving funds are not from sanctioned sources while preserving transaction privacy. This is the US-viable model.

**EU regulatory landscape:**
- **EU AMLR Article 79 (Regulation 2024/1624):** CASPs are **prohibited from handling privacy-preserving digital assets** effective July 1, 2027. This explicitly covers tokens like Monero and Zcash.
- **Critical question:** Does Article 79 cover privacy-preserving *mechanisms* (like shielded USDC transfers) or only privacy-native *tokens*? The implementing acts from EBA are not yet finalized. This is a major uncertainty.
- **Travel Rule** requirements under MiCA mandate that CASPs transmit originator and beneficiary information for crypto transfers. Fully shielded transfers are incompatible with the Travel Rule.
- **Finland specifically:** Transition period ended June 30, 2025. Finland is an early enforcer of MiCA. The seed network operates in Finnish warehouses.

**Compliant privacy models:**
- **Railgun PPOI (Private Proofs of Innocence):** Automatically screens deposits against Chainalysis sanctioned address lists and OFAC lists. Tainted funds cannot enter the privacy set. Proof of innocence is generated without revealing user balances or activity.
- **Privacy Pools (0xbow):** Association sets prove funds are not from sanctioned sources. Integrated into Ethereum Foundation's Kohaku wallet.
- **Selective disclosure / viewer keys:** Enterprise buyers get viewer keys that reveal their own transaction history for internal audit, while external observers see nothing. Compatible with both Railgun and Aztec models.

**Risk assessment for shielded robot payments in Finland/EU:**

| Model | US Legal Risk | EU Legal Risk | Feasibility |
|-------|-------------|-------------|-------------|
| Fully shielded (Monero-style) | Medium (post-Tornado Cash delisting) | **High -- likely prohibited by Art. 79** | Not viable for EU operation |
| Compliant privacy (Privacy Pools) | Low | **Uncertain** -- depends on EBA interpretation | Possible but needs legal opinion |
| Platform-mediated privacy (TEE) | Low | Low -- platform retains data for compliance | **Most viable** |
| Selective disclosure (viewer keys) | Low | Low-Medium -- if regulator gets viewer key | Viable with compliance framework |

### Implications for Architecture

1. **EU AMLR Article 79 is a hard constraint.** Fully shielded payments are likely illegal for a CASP operating in the EU by 2027. The platform cannot use Monero, Zcash, or fully private Aleo transactions if it operates as a regulated entity in Finland.
2. **"Compliant privacy" is the only viable EU path.** This means: Privacy Pools-style proofs of fund provenance, selective disclosure to regulators on request, and platform-level data retention for compliance.
3. **Platform-mediated privacy (TEE model) is the safest regulatory choice for v1.5-v2.0.** The platform retains data inside TEEs for compliance but external observers see encrypted data. This satisfies both privacy goals and regulatory requirements.
4. **Viewer keys for enterprise buyers (RQ-10) are architecturally necessary.** "Private from the world, auditable by my CFO" is the correct design target.
5. **Get a legal opinion on whether Privacy Pools-style compliant privacy satisfies Article 79.** This is the critical regulatory question that determines the v2.x architecture.
6. **The seed network's Finnish jurisdiction makes this urgent.** Finland is an early MiCA enforcer. The team must understand the compliance requirements *before* building privacy features.

---

## Domain F: Foundational Architecture Decision

### The Chain Question

The research plan poses three options. Here is the decision matrix:

| Criterion | (a) Base + Privacy Overlay | (b) Aztec as Primary | (c) Base + Aleo (Dual-Chain) |
|-----------|--------------------------|---------------------|------------------------------|
| **USDC liquidity** | Excellent (Base native USDC) | Not yet available | Base: excellent; Aleo USDCx: early but Circle-backed |
| **Privacy capability** | None native. Horizen L3 (TEE) is the only option on Base. Railgun not on Base. | Full ZK privacy, not yet live | Full ZK privacy on Aleo with USDCx |
| **Bridge risk** | None (native) | Ethereum L1 bridge (immature) | xReserve bridge for USDCx (Circle-operated) |
| **Developer tooling** | Mature (EVM, Solidity) | Noir language -- good DX but small ecosystem | Leo language (Aleo) -- smaller ecosystem |
| **x402 compatibility** | Native | None | Base rail: native; Aleo rail: needs z402-style adapter |
| **Regulatory compatibility** | Transparent = compliant | Full privacy = EU problematic | Choose per-transaction privacy level |
| **Transaction cost** | ~$0.001 (L2) | Unknown (not live) | Base: ~$0.001; Aleo: low (ZK-optimized) |
| **Latency** | ~200ms settlement | Unknown | Base: ~200ms; Aleo: seconds |
| **Time to production** | Now | 6-12+ months | Base: now; Aleo: 3-6 months for integration |
| **PD-8 fiat accessibility** | Excellent (Coinbase on/off ramp) | Poor (no fiat ramp) | Base: excellent; Aleo: limited |

### Recommendation with Rationale

**Recommended: Option (c) -- Base for v1.5 (transparent) + design Aleo privacy rail for v2.x, using compliant privacy patterns throughout.**

Rationale:

1. **v1.5 should ship on Base as planned.** The privacy research reveals no mature privacy overlay on Base, but it also reveals that EU regulations (Article 79) prohibit fully shielded payments for CASPs by 2027. Therefore, the privacy features that are *legally viable in the EU* do not require a chain migration -- they require platform-level privacy (TEEs, selective disclosure, viewer keys) which can be built on any chain.

2. **Aleo + USDCx is the correct privacy chain for when/if full cryptographic privacy is needed.** Circle's backing, the xReserve bridge, and Aleo's ZK-by-default architecture make it the strongest option. But the regulatory landscape means fully private settlement may only be viable for non-EU markets.

3. **Aztec is not ready.** Empty blocks on mainnet, no USDC support, and uncertain timeline make it a v3.0+ consideration at best.

4. **The dual-chain approach lets users choose their privacy level.** EU warehouse operators use Base (transparent, compliant). Non-EU operators with different regulatory requirements can use Aleo (private). The application layer remains chain-agnostic.

5. **Do not block v1.5.** The research reveals that the privacy features achievable in the EU regulatory environment (platform-mediated privacy, selective disclosure, compliant privacy pools) do not require a chain change. They require application-layer changes that can be built on Base.

---

## Assumption Validation

| # | Assumption | Status | Evidence |
|---|-----------|--------|----------|
| A1 | ZKP proof generation feasible in <60s on robot hardware | **INVALIDATED** | RISC Zero requires minimum 16 GB RAM. Robot-class hardware cannot generate proofs locally. However, delegated proving via TEE-backed services (Succinct/Phala) achieves 1-5s for simple circuits with privacy preserved. The assumption is invalidated for on-robot proving but the *intent* (fast proof generation) is achievable via delegation. |
| A2 | Privacy-preserving settlement layer exists with USDC liquidity | **VALIDATED** | Aleo + USDCx launched January 2026, backed 1:1 by USDC via Circle xReserve. Railgun supports USDC on Ethereum/Polygon/Arbitrum (not Base). Privacy Pools supports USDC on Ethereum mainnet. |
| A3 | Encrypted task specs support enough info for bid eligibility | **INCONCLUSIVE** | The capability vector leakage problem is real and unsolved. Generalized capability classes reduce leakage but may be too coarse for efficient matching. TEE-based matching avoids the problem entirely but introduces trust assumptions. No solution achieves both full privacy and efficient matching without TEEs. |
| A4 | Anonymous reputation credentials updateable without trusted issuer | **VALIDATED** | Threshold BBS+ signatures (2023-2025 papers) enable distributed credential issuance across 3+ nodes. No single trusted issuer required. Standardization underway at IRTF and W3C. |
| A5 | Shielded payments don't trigger money transmission classification | **INVALIDATED for EU** | EU AMLR Article 79 explicitly prohibits CASPs from handling privacy-preserving digital assets by July 2027. Finland is early enforcer. US landscape is more favorable post-Tornado Cash delisting, but Roman Storm trial outcome pending. |
| A6 | Enterprise buyers accept aggregate audit reports | **INCONCLUSIVE** | No enterprise buyer interviews conducted (seed-stage startup). However, the viewer-key / selective-disclosure model provides a technical path to satisfy both privacy and audit requirements. |
| A7 | x402 can work with shielded payments | **PARTIALLY VALIDATED** | x402 core is tied to transparent on-chain settlement (EIP-3009). However, z402 (Zcash-based) and ZK-X402 community projects demonstrate the HTTP 402 flow can be adapted for shielded settlement. x402 V2 may broaden scheme support. Not Coinbase-official; maturity is low. |
| A8 | Users actually want full cryptographic privacy | **INCONCLUSIVE** | No user research conducted. The regulatory findings suggest that in the EU, full cryptographic privacy may not be legally available regardless of user desire. Platform-mediated privacy (invisible to external observers, visible to platform/regulators) may be the only viable offering. |
| A9 | Privacy can be layered onto v2.0 multi-robot handoff | **INCONCLUSIVE** | Not directly researched in this synthesis. TEE-based privacy can likely be layered on top of any handoff protocol. Full ZK privacy for chained workflows (encrypted output of step N feeding step N+1) is a fundamentally harder problem that likely requires privacy-aware design from the start. |
| A10 | Seed network has enough anonymity set for privacy to be meaningful | **INVALIDATED** | With 2-3 robots in 3 Finnish warehouses, metadata analysis trivially deanonymizes all transactions regardless of cryptographic privacy. Privacy features only become meaningful at scale (dozens of robots, many buyers). This confirms the critique's recommendation to defer cryptographic privacy until minimum viable anonymity. |

---

## Architecture Recommendations

### 1. Ship v1.5 on Base with transparent x402 as planned

No privacy overlay on Base is mature enough to justify delaying v1.5. The regulatory landscape (EU AMLR Article 79) means that even if a privacy overlay existed, fully shielded payments would be legally problematic for the Finnish seed network. Transparent settlement on Base is correct for v1.5.

### 2. Build platform-mediated privacy as the v2.0 privacy layer

Use TEE-based confidential computation (following the Horizen-on-Base / Succinct Private Proving patterns) to achieve "private from external observers, visible to platform and regulators":
- Task specs encrypted at rest, decrypted only inside TEE enclaves
- Scoring/matching runs inside TEEs
- Viewer keys for enterprise buyers to audit their own transaction history
- Platform retains compliance data in encrypted storage accessible to regulators on lawful request

This satisfies the user story ("verified but private") within EU regulatory constraints and is buildable on Base.

### 3. Design the settlement abstraction layer for future chain optionality

The `RobotTaskEscrow.sol` contract and payment middleware should be designed with a settlement abstraction that can route to:
- Base (transparent, v1.5+)
- Aleo via USDCx (private, v2.x+ for non-EU markets)
- Future chains as they mature

This means: do not hardcode Base-specific assumptions into the escrow logic. Use an interface that supports both transparent and shielded settlement behind a common API.

### 4. Adopt BBS+ credentials for robot reputation starting in v2.0

Implement BBS+ signed credentials for robot reputation with selective disclosure:
- Platform (or distributed issuer set) issues updated credentials after each task
- Robot can prove aggregate stats (task count, success rate, average speed) without revealing individual task history
- Threshold issuance across 3+ platform nodes to avoid single-issuer trust
- Builds on W3C Verifiable Credentials standard for interoperability

### 5. Remove on-chain `request_id` (AD-3) before it becomes a privacy liability

The current design embeds `request_id` in on-chain transaction memos. This creates a permanent, public, immutable link between payments and tasks. Even with future privacy features, historical on-chain data is forever transparent. **Recommendation: move request_id tracking off-chain (to platform database) before v1.5 ships.** Link payments to tasks via platform-internal references, not on-chain memos.

---

## Foundational Design Impact on v1.5

**Bottom line: v1.5 on Base should proceed, with three design changes to avoid privacy debt.**

The research concludes that the v1.5 Base decision does NOT need to change. The reasons:

1. No mature privacy overlay exists on Base, but the EU regulatory environment (AMLR Article 79) means fully shielded payments are likely illegal for EU CASPs by 2027 anyway.
2. The privacy features that ARE legally viable (platform-mediated confidentiality, selective disclosure, viewer keys) are application-layer concerns that work on any chain, including Base.
3. The seed network's tiny anonymity set (2-3 robots, 3 warehouses) makes cryptographic privacy security theater at current scale.

**Three design changes for v1.5 to avoid privacy debt:**

1. **Remove `request_id` from on-chain transaction memos.** Store task-payment linkage in the platform database only. On-chain transactions should carry only the minimum needed for settlement (amount, escrow contract, nonce). This is a small change now that avoids a permanent privacy leak.

2. **Design the escrow contract with a settlement interface, not Base-specific calls.** Use an abstraction layer so the contract interaction can be swapped for a privacy-preserving settlement (Aleo, z402, future Privacy Pools on Base) without rewriting the escrow logic.

3. **Do not expose robot wallet addresses publicly in the API.** Use platform-internal identifiers in the API layer; translate to on-chain addresses only at the settlement layer. This preserves the option to introduce rotating/shielded addresses later.

These three changes add minimal engineering effort (~1-2 days) but preserve the option to add meaningful privacy features in v2.0+ without architectural rewrites.

**The v1.5 go/no-go answer: GO on Base, with these three changes.**

---

## Sources

### ZK Proof Systems
- [RISC Zero Performance Benchmarks](https://dev.risczero.com/api/zkvm/benchmarks)
- [Comparative Analysis of SP1 and RISC Zero](https://medium.com/@gwrx2005/comparative-analysis-of-sp1-and-risc-zero-zero-knowledge-virtual-machines-4abf806daa70)
- [SP1 Hypercube Real-Time Proving](https://blog.succinct.xyz/real-time-proving-16-gpus/)
- [PLONK vs Groth16 Benchmarks (Aztec)](https://medium.com/aztec-protocol/plonk-benchmarks-2-5x-faster-than-groth16-on-mimc-9e1009f96dfe)
- [Succinct Private Proving with Phala TEE](https://phala.com/posts/private-proving-succinct-sets-new-standard-for-zk-privacy-with-phala-cloud)
- [Evaluating Compiler Optimization Impacts on zkVM Performance](https://arxiv.org/abs/2508.17518)

### Privacy-Preserving Settlement
- [Aleo USDCx Launch (Circle)](https://www.circle.com/blog/usdcx-on-aleo-testnet-via-circle-xreserve)
- [Aleo USDCx Mainnet Announcement](https://www.businesswire.com/news/home/20251209069657/en/Aleo-to-Launch-USDCx-a-Private-and-Programmable-Stablecoin-Built-for-Real-World-Use)
- [Railgun Privacy System Documentation](https://docs.railgun.org/wiki/learn/privacy-system)
- [Railgun Private Proofs of Innocence](https://docs.railgun.org/wiki/assurance/private-proofs-of-innocence)
- [Aztec Network Road to Mainnet](https://aztec.network/blog/road-to-mainnet)
- [Aztec Roadmap](https://aztec.network/roadmap)
- [Horizen Layer 3 on Base Launch](https://www.theblock.co/post/381846/privacy-horizen-launches-layer-3-base-mainnet)

### x402 Protocol
- [x402 Coinbase Documentation](https://docs.cdp.coinbase.com/x402/welcome)
- [x402 Whitepaper](https://www.x402.org/x402-whitepaper.pdf)
- [x402 EVM Scheme Specification (GitHub)](https://github.com/coinbase/x402/blob/main/specs/schemes/exact/scheme_exact_evm.md)
- [z402: Privacy-Preserving Micropayment Protocol](https://z402.cash/)
- [ZK-X402 Privacy-Preserving Payment Protocol](https://www.zk-x402.tech/)
- [x402 V2 Launch Announcement](https://www.x402.org/writing/x402-v2-launch)

### Anonymous Credentials & Reputation
- [BBS Signature Scheme (IRTF Draft)](https://identity.foundation/bbs-signature/draft-irtf-cfrg-bbs-signatures.html)
- [Anonymous Credential System Specification (BBS+)](https://eprint.iacr.org/2025/824)
- [Threshold BBS+ Signatures for Distributed Issuance](https://eprint.iacr.org/2023/602)
- [Augmenting BBS with Conventional Signatures (2026)](https://eprint.iacr.org/2026/087)
- [Semaphore Protocol](https://semaphore.pse.dev/)

### Privacy Pools & Compliant Privacy
- [Privacy Pools by 0xbow (GitHub)](https://github.com/0xbow-io/privacy-pools-core)
- [0xbow Seed Round Announcement](https://www.globenewswire.com/news-release/2025/11/18/3190435/0/en/0xbow-Closes-3-5M-Round-for-Compliant-Crypto-Privacy-Technology-Following-Ethereum-Foundation-Integration.html)
- [Vitalik Buterin's Privacy Toolkit Kohaku](https://unchainedcrypto.com/vitalik-unveils-new-ethereum-privacy-toolkit-kohaku/)
- [From Aztec to Zcash: Pragmatic Privacy in 2025](https://www.theblock.co/post/383680/aztec-zcash-year-pragmatic-privacy-root)

### Regulatory
- [Treasury Lifts Tornado Cash Sanctions (Venable Analysis)](https://www.venable.com/insights/publications/2025/04/a-legal-whirlwind-settles-treasury-lifts-sanctions)
- [Tornado Cash Delisting Press Release](https://home.treasury.gov/news/press-releases/sb0057)
- [EU AMLR Article 79 -- Privacy Coin Ban](https://cointelegraph.com/news/eu-crypto-ban-anonymous-privacy-tokens-2027)
- [Finland Updated AML Guidelines July 2025](https://www.zigram.tech/resources/finland-updated-aml-guidelines-july-2025/)
- [MiCA Regulation Guide 2026](https://complyfactor.com/mica-regulation-guide-2026-eu-crypto-asset-framework-explained/)
- [Finland Crypto Compliance Framework 2026](https://www.onesafe.io/blog/finland-crypto-reporting-framework-2026)
- [Tornado Cash Sanctions Compliance Implications (K2 Integrity)](https://www.k2integrity.com/en/knowledge/policy-alerts/the-tornado-cash-delisting-and-sanctions-compliance-implications-for-crypto/)

### MPC & FHE
- [MPC for Sealed-Bid Auctions (ScienceDirect)](https://www.sciencedirect.com/science/article/abs/pii/S1389128625009430)
- [Partisia MPC Guide 2026](https://www.partisia.com/tech/multi-party-computation)
- [FHE GPU Acceleration Benchmarks (MDPI)](https://www.mdpi.com/2504-2289/10/3/79)
- [Practical Solutions in FHE (Springer)](https://cybersecurity.springeropen.com/articles/10.1186/s42400-023-00187-4)
