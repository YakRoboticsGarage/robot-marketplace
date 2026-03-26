# Privacy Base-Layer Chain Comparison

**Date:** 2026-03-26
**Status:** Research complete — informs settlement abstraction design decisions
**Companion to:** FOUNDATIONAL_TECH_ANALYSIS.md (consideration #5: "Privacy Is an Application-Layer Concern")

---

## Executive Summary (10 bullets)

1. **ZKsync Prividium is real and in production** — Memento ZK Chain is live on mainnet with $112M TVL and three tokenized RWA funds. Deutsche Bank, Cari Network (five US regional banks), and 30+ institutions are building on it. This is not vaporware.

2. **Prividium is enterprise-permissioned, not public-permissionless.** Each Prividium is a private, permissioned Validium chain with its own sequencer/prover inside the enterprise's infrastructure. It is architecturally a private appchain, not a public privacy L2. A robot task marketplace open to the public cannot deploy on a Prividium chain — it would need to operate its own.

3. **Aztec is the most technically ambitious privacy L2** but remains pre-transaction on mainnet as of March 2026. Ignition chain launched Nov 2025 with 500 sequencers producing empty blocks. Transactions expected to go live in early-to-mid 2026. Not production-ready for settlement.

4. **Horizen L3 on Base is the most architecturally relevant option** for our use case — it is live on Base mainnet, uses TEE-based confidential compute, is EVM-native, and explicitly designed for "compliant privacy" with selective disclosure. Being an L3 on Base means USDC liquidity from Base is accessible.

5. **No privacy chain today has native Circle USDC (CCTP-supported).** Base has $4.1B USDC supply. Privacy chains either bridge USDC (introducing trust assumptions) or don't support it at all. This is a dealbreaker for x402 settlement in 2026.

6. **The 4-mode settlement abstraction remains correct** even with privacy chains. Chain-level privacy does not eliminate the need for immediate vs. batched timing modes. It potentially simplifies the privacy dimension (modes 2 and 4 become simpler), but the timing dimension is orthogonal.

7. **x402 payment proofs work on transparent chains by design.** On a privacy chain, the facilitator verification model breaks unless the chain supports selective disclosure to the facilitator. Shielded-x402 (Noir + ZK proofs) and z402 (Zcash shielded pools) are experimental alternatives but not production-ready.

8. **EU AMLR Article 79 (effective July 2027) bans CASPs from handling privacy-preserving digital assets.** Privacy chains that offer compliant selective disclosure (Prividium, Horizen) survive this; fully private chains without disclosure (Zcash-style) do not. This regulatory constraint heavily favors application-layer privacy over chain-layer privacy.

9. **For v1.5 shipping now: no change needed.** Base + application-layer privacy remains the correct architecture. The foundational tech analysis conclusion #5 holds under scrutiny.

10. **For v2.0+: Horizen L3 on Base is the leading candidate** for Mode 2 (immediate private) settlement. It sits within the Base ecosystem (same USDC liquidity, same bridges), adds TEE-based confidential compute, and is designed for the compliance model we need. Monitor closely; evaluate for v2.1-P.

---

## ZKsync Prividium Deep Dive

### Architecture

Prividium is not a single public chain. Each Prividium instance is a **private, permissioned ZKsync chain** (Validium mode) that runs:

- **Its own dedicated sequencer** — orders transactions privately within the enterprise's infrastructure
- **Its own prover** — generates ZK-STARK validity proofs for batches
- **Off-chain state database** — all transaction data, contract state, and balances stored off-chain (enterprise cloud or on-prem)
- **Proxy RPC layer** — single entry point enforcing role-based access control; authenticates via Okta SSO or Sign-In With Ethereum (SIWE)
- **ZKsync Gateway** — receives state roots and ZK proofs, publishes commitments to Ethereum L1

The settlement flow:
1. User authenticates via Proxy RPC (Okta/SIWE)
2. Proxy validates identity, role, and function-level permissions
3. Authorized request forwarded to sequencer
4. Sequencer executes privately, updates off-chain state
5. Prover generates ZK-STARK proof over batch
6. State root + proof submitted to Ethereum via ZK Gateway

**What goes on-chain (Ethereum L1):** Only state roots and validity proofs. No transaction inputs, addresses, calldata, or contract state.

**What stays off-chain:** Everything else — transaction details, balances, contract storage, user identities.

**Key technical decisions:**
- **ZK-STARKs** (not SNARKs) — no trusted setup, quantum-resistant (hash-based cryptography)
- **TEEs used for interoperability** — ZKsync uses TEEs to validate ZK computation and speed up cross-chain operations (TEEs are faster than ZK proofs for verification)
- **Validium mode** (not rollup) — data availability is off-chain, not posted to Ethereum. This is a deliberate privacy choice but means data availability depends on the enterprise operator, not Ethereum consensus.

Sources:
- [ZKsync Prividium Architecture Docs](https://docs.zksync.io/zk-stack/prividium/architecture)
- [ZKsync Prividium Features Docs](https://docs.zksync.io/zk-stack/prividium/features)
- [BlockEden.xyz: Prividium Banking Stack](https://blockeden.xyz/blog/2026/01/30/prividium-zksync-privacy-banking-stack-institutional-blockchain/)

### Privacy Model

**What is private:**
- Transaction sender and receiver identities (within the private chain)
- Transaction amounts and calldata
- Contract state and storage
- All business logic execution

**What is NOT private (by design):**
- State roots on Ethereum (publicly visible but reveal nothing about individual transactions)
- Validity proofs on Ethereum (prove correctness without revealing data)
- Selectively disclosed data (configured by admin)

**Selective disclosure model:**
- Administrators configure what data is exposed via read-only public endpoints
- Options include: total token supply, circulating supply, contract bytecode
- Auditors/regulators can access approved on-chain data without accessing the full private ledger
- Supports sanctions checks, proof of reserves, and regulatory verification on demand

**Important distinction:** Prividium's privacy is *access-control-based*, not *cryptographic per-transaction*. The chain operator (enterprise) sees everything. Privacy is from the outside world, not from the operator. This is fundamentally different from Aztec's model where even the chain itself cannot see private state.

### Current Status

**Production deployments (confirmed):**
- **Memento ZK Chain** — first live Prividium on mainnet. Three tokenized RWA funds, $112M TVL. Collaboration with Deutsche Bank for DAMA 2 (Digital Assets Management Access) supporting 24+ institutions. Won the first Prividium Prize (10M ZK tokens). ([Source](https://x.com/Memento_Bc/status/2011126255207231750))
- **Cari Network** — consortium of five US regional banks (including Huntington and KeyCorp) building tokenized deposit platform on Prividium. Announced March 17, 2026. Targeting Q3 2026 rollout. ([Source](https://cointelegraph.com/news/cari-picks-zksync-prividium-regional-banks))
- **UBS** — completed proof-of-concept for Key4 Gold product (fractional gold investments via permissioned blockchain)
- **GRVT** — regulated hybrid DEX on ZKsync
- **Buenos Aires government** — digital identity for 3.6M residents (ZKsync, likely not Prividium-specific)

**Claimed but unverifiable:** "Over 30 major global institutions including Citi and Mastercard" and "two central banks" referenced in marketing materials but without detailed public confirmation.

**Infrastructure status:**
- ZK Gateway hit testnet (mainnet Q2 2025)
- Airbender (next-gen proving system) introduced June 2025
- Atlas upgrade (Oct 2025) — targets 15K+ TPS, ~1s ZK finality, ~$0.0001 proving cost per transfer
- ChonkyBFT consensus live
- Execution delay reduced from 21 hours to 3 hours

### USDC/Stablecoin Support

**Direct USDC support: No.** Prividium is oriented toward tokenized deposits (bank liabilities with FDIC insurance) rather than stablecoins. The Cari Network explicitly positions tokenized deposits as a *competitor* to stablecoins.

Key quote from ZKsync: Stablecoins "don't carry deposit-insurance protection, don't sit on a bank's balance sheet, and don't support bank compliance obligations." Tokenized deposits are positioned as "the payment tokens by banks when money needs to move in and out."

**For a robot task marketplace:** This is a poor fit. We need USDC (or EURC) for x402 settlement. Prividium's financial model is built around bank deposits, not stablecoin-denominated commerce.

### Developer Experience

- **Full EVM compatibility** — existing Solidity contracts deploy without modification
- Prividium is built on ZK Stack, which uses the standard Ethereum toolchain (Hardhat, Foundry, etc.)
- Enterprise SSO integration (Okta, Azure AD) alongside crypto-native wallet auth
- Admin dashboard for managing roles, permissions, and selective disclosure (no YAML/code changes needed)
- Block explorer restricted to chain operators and internal systems
- **Custom gas token support** — can define a custom gas token or operate in fully gasless mode

### Regulatory Approach

Prividium is explicitly designed for regulatory compliance:
- Permissioned access means KYC/AML is enforced at the RPC proxy level
- Selective disclosure enables auditor access without exposing the full ledger
- The enterprise operator has full visibility (no privacy from the chain operator)
- Positioned as "compliant by design" for banking regulation

**EU AMLR Article 79 compatibility:** Strong. Prividium's model (permissioned chain, operator sees all, selective disclosure to regulators) is architecturally aligned with AMLR requirements. However, it's designed for banks running their own chains, not for open public marketplaces.

---

## Comparative Matrix

| Criterion | ZKsync Prividium | Aztec Network | Polygon Miden | Fhenix (CoFHE) | Horizen L3 (Base) | Oasis Sapphire |
|---|---|---|---|---|---|---|
| **Architecture** | Permissioned Validium (ZK Stack) | Public ZK rollup | Public ZK rollup (STARK) | FHE coprocessor on existing chains | OP Stack L3 on Base | Confidential ParaTime (TEE) |
| **Privacy tech** | Access control + ZK-STARKs for settlement | Client-side ZK proofs (Noir/Honk) | Client-side STARKs | Fully Homomorphic Encryption | TEE (Trusted Execution Environments) | TEE (Intel SGX) |
| **What's private** | Everything on-chain (from outside); operator sees all | Sender, receiver, amount, contract state (cryptographic) | Sender, receiver, amount, contract state (cryptographic) | Encrypted computation on-chain | Computation inside TEE; configurable disclosure | Contract state, transaction inputs, return values |
| **Privacy from chain operator** | No — operator sees everything | Yes — cryptographic privacy | Yes — client-side proofs | Partial — FHE computation is opaque | No — TEE operator could theoretically access | No — TEE operator trust |
| **USDC (native Circle CCTP)** | No (tokenized deposits focus) | No (bridge only, not yet live) | No (testnet only) | Inherits from host chain (Base possible) | Inherits from Base (bridge from L2) | No (bridged only) |
| **EVM compatible** | Yes (full Solidity) | No (Noir/Aztec.nr — new language) | No (Miden Assembly/Rust) | Yes (fhEVM Solidity extensions) | Yes (full EVM, OP Stack) | Yes (Sapphire EVM) |
| **Mainnet status** | Live (Memento chain) | Ignition live, no transactions yet | Testnet v6, mainnet late May 2026 | CoFHE on mainnet (Ethereum, Arbitrum); L2 testnet only | Live on Base mainnet | Live (mainnet since 2022) |
| **TPS / Latency** | 10K-15K TPS, sub-second finality | 36-72s blocks now, target 4s by end 2026 | Not published | Depends on host chain | Inherits Base performance | ~1000 TPS estimated |
| **Transaction cost** | ~$0.0001 per tx (target) | Not yet applicable | Not published | Depends on host chain + FHE overhead | Inherits Base costs (~$0.001-0.01) | ~$0.01 range |
| **Selective disclosure** | Yes (admin-configured, read-only endpoints) | Planned (viewing keys concept) | Not yet specified | Not yet specified | Yes (designed for compliant privacy) | Developer-configurable per contract |
| **Regulatory posture** | Designed for banks; compliant by design | "Pragmatic privacy" stance; compliance through viewing keys | Enterprise-focused (a16z backed) | Coprocessor model avoids direct chain regulation | "Compliant privacy" — explicit regulatory alignment | Flexible (TEE-based, not fundamentally private) |
| **EU AMLR Art. 79 risk** | Low (permissioned, selective disclosure) | Medium-High (fully private chain; viewing keys may satisfy but untested) | Medium (client-side privacy, unclear disclosure) | Low (coprocessor on compliant chains) | Low (TEE + selective disclosure on Base) | Low (TEE-based, configurable) |
| **Production readiness** | Production (enterprise) | Pre-production | Pre-production (testnet) | Early production (coprocessor); L2 pre-production | Production (mainnet live on Base) | Production (live since 2022, small ecosystem) |
| **Developer ecosystem** | Enterprise-focused (small but funded) | Growing (Noir community, $100M+ raised) | Small (seed stage, $25M raised) | Small (early) | Small but growing (1M ZEN grants) | Small (~$235M ecosystem fund) |
| **Backing/Funding** | Matter Labs (ZKsync); major bank partnerships | $100M+ raised; Vitalik endorsed | a16z crypto, 1kx, Hack VC ($25M seed) | $15M Series A; EigenLayer partnership | DCG-backed; Horizen Labs (Vela platform) | Oasis Foundation; $235M ecosystem fund |

Sources:
- Aztec: [Bankless](https://www.bankless.com/read/privacy-l2-aztec-is-almost-ready-for-primetime), [CoinDesk](https://www.coindesk.com/markets/2025/11/20/privacy-focused-aztec-network-s-ignition-chain-lights-up-on-ethereum/), [Aztec Roadmap](https://aztec.network/roadmap)
- Miden: [CoinDesk](https://www.coindesk.com/tech/2025/04/29/polygon-spin-off-miden-secures-25m-to-bring-speed-privacy-to-institutional-giants/), [Miden Build](https://miden.xyz/build)
- Fhenix: [Fhenix.io](https://www.fhenix.io/), [The Block](https://www.theblock.co/post/298443/ethereum-layer-2-fhenix-confidentiality-series-a-funding-testnet)
- Horizen: [The Block](https://www.theblock.co/post/381846/privacy-horizen-launches-layer-3-base-mainnet), [BeInCrypto](https://beincrypto.com/horizen-mainnet-launch-base/)
- Oasis: [Oasis Sapphire Docs](https://docs.oasis.io/build/sapphire/), [Oasis.net](https://oasis.net/sapphire)

---

## Chain-Level vs Application-Level Privacy

### The Architectural Question

The core question: **If you settle on a privacy-native chain, does it simplify the architecture enough to justify the migration cost, liquidity loss, and regulatory risk?**

There are three distinct privacy architectures:

| Approach | Example | Privacy Source | Trust Model | Regulatory Profile |
|---|---|---|---|---|
| **Chain-level cryptographic** | Aztec, Miden | ZK proofs, client-side proving | Trustless (math) | High regulatory risk (Art. 79) |
| **Chain-level access control** | Prividium, Horizen | Permissioned access + TEE/ZK settlement | Trust the operator | Low regulatory risk |
| **Application-level** | TEE enclaves on Base | Application encrypts/computes privately | Trust the TEE operator | Low regulatory risk |

### When Chain-Level Privacy Makes Sense

1. **When all participants need privacy from each other AND from the platform** — e.g., dark pool trading where even the exchange shouldn't see orders. Aztec's cryptographic model excels here.
2. **When regulatory frameworks explicitly support it** — e.g., regulated securities with built-in compliance (viewing keys accepted by regulators).
3. **When the privacy set needs to be large** — cryptographic chain-level privacy provides a larger anonymity set than application-layer shielding on a transparent chain.
4. **When the application IS the chain** — enterprise-to-enterprise settlement where each party runs their own Prividium instance.

### When Application-Level Privacy Is Sufficient

1. **When the platform is trusted to see data** — a marketplace operator that matches tasks to robots inevitably sees both sides. Chain-level privacy from the platform is unnecessary.
2. **When privacy needs are selective** — some data must be private (task specs, bid amounts), other data should be public (robot capabilities, reputation scores). Application-layer gives granular control.
3. **When USDC liquidity matters** — Base has $4.1B USDC supply and x402/Stripe integration. Moving to a privacy chain fragments liquidity.
4. **When regulatory compliance is paramount** — application-layer privacy with TEE-based computation is clearly legal. Chain-level cryptographic privacy faces Article 79 challenges.
5. **When the anonymity set is too small** — at seed scale (hundreds of robots/operators), cryptographic anonymity is security theater. The set is too small for meaningful privacy. But payload confidentiality (encrypted task specs) is still valuable.

### Hybrid Approaches

The 2025-2026 trend is toward **hybrid privacy** combining multiple techniques:

- **Horizen on Base** = hybrid: transparent Base chain for settlement, TEE compute for confidential execution, selective disclosure for compliance. This is the closest to what our marketplace needs.
- **Fhenix CoFHE** = hybrid: FHE coprocessor adds encrypted computation to existing chains (Base, Arbitrum) without moving settlement. Interesting but very early.
- **Shielded-x402** = hybrid: ZK proofs (Noir circuits) create a shielded pool layer on top of transparent x402 payments. Experimental but architecturally elegant.

**Key insight from 2025 research:** "No single technique optimizes performance, trust minimization, and flexibility" ([StarkWare](https://starkware.co/blog/blockchain-privacy/)). The center of gravity is shifting from "pick a privacy chain" to "compose privacy at multiple layers."

---

## Impact on Settlement Abstraction Design

### Does a privacy chain simplify or replace the 4-mode model?

**No. The 4-mode model survives intact.**

The settlement abstraction has two orthogonal dimensions:
- **Timing:** Immediate vs. Batched (driven by network latency — DTN links, offline robots)
- **Privacy:** Transparent vs. Private (driven by regulatory requirements and user preferences)

A privacy-native chain collapses the privacy dimension for modes 2 and 4 — if the chain is inherently private, you don't need application-layer privacy shielding. But it does NOT eliminate the timing dimension. Batched settlement is needed for:
- DTN/lunar operations with multi-hour latency
- Offline robot scenarios where immediate settlement is impossible
- Gas optimization through batch aggregation

If anything, a privacy chain might ADD complexity: you'd need to handle both transparent settlement (Mode 1/3 on Base) and private settlement (Mode 2/4 on privacy chain), with bridging between them.

**Updated mode analysis with privacy chains:**

| Mode | Without Privacy Chain | With Privacy Chain (e.g., Horizen L3) |
|---|---|---|
| 1. Immediate transparent | Base x402 | Base x402 (unchanged) |
| 2. Immediate private | Base + TEE application layer | Horizen L3 (simpler — chain handles privacy) |
| 3. Batched transparent | Base batched x402 | Base batched x402 (unchanged) |
| 4. Batched private | Base + TEE + batch aggregator | Horizen L3 + batch aggregator (still need batching logic) |

**Net: Mode 2 gets simpler. Mode 4 stays complex. Modes 1/3 unchanged. The abstraction still earns its keep.**

### x402 Compatibility Analysis

**Current x402 architecture:** Resource server requires payment → client pays on-chain → facilitator verifies payment proof (on-chain receipt) → resource served.

**The verification problem on privacy chains:**

x402's facilitator model requires **publicly verifiable payment proofs**. The facilitator calls `/verify` on the payment, checking the on-chain transaction. On a transparent chain (Base), this is trivial — the transaction is publicly visible.

On a privacy chain, three scenarios:

1. **Prividium (permissioned Validium):** Facilitator would need to be a permissioned participant on the Prividium chain to verify payments. This defeats the purpose of an open marketplace where any facilitator can verify.

2. **Aztec (cryptographic privacy):** Payment proofs would need viewing keys or ZK proof of payment. The shielded-x402 project ([GitHub](https://github.com/nhestrompia/shielded-x402)) demonstrates this is possible using Noir circuits — the payer generates a ZK proof that they paid the correct amount to the correct recipient, without revealing their identity or balance. But this is experimental.

3. **Horizen L3 (TEE-based):** TEE-based privacy can selectively expose payment receipts to facilitators. The facilitator trusts the TEE attestation. This is the most x402-compatible privacy model because selective disclosure can be configured to expose exactly what the facilitator needs.

**Emerging solutions:**
- **shielded-x402** ([GitHub](https://github.com/nhestrompia/shielded-x402)) — Noir circuits + shielded pool + relayer. Agent deposits into shielded pool, generates ZK proof of payment, relayer verifies and settles. Experimental, not production.
- **z402** ([z402.cash](https://z402.cash/)) — Integrates Zcash shielded transactions with x402 flow. Uses zk-SNARKs for confidential/untraceable machine payments. Conceptual/early.
- **x402 V2 encrypted amounts** — x402 V2 supports "encrypted amounts, keeping procurement strategies confidential." This is application-layer amount privacy, not chain-level. ([Source](https://www.x402.org/writing/x402-v2-launch))

**Verdict:** x402 works best on transparent chains (Base). Privacy chain compatibility is possible but requires either permissioned facilitator access (Prividium), ZK payment proofs (shielded-x402, not production), or TEE-based selective disclosure (Horizen — most practical). For v1.5-v2.0, staying on Base for x402 is correct. For v2.1+, Horizen L3 on Base is the most compatible privacy option.

### Implications for RobotTaskEscrow.sol

The settlement abstraction interface defined in FOUNDATIONAL_TECH_ANALYSIS.md remains the right design:

1. **Mode 1 (immediate transparent)** — ships in v1.5 on Base. No changes needed.
2. **Mode 2 (immediate private)** — if implemented on Horizen L3 on Base:
   - Escrow contract deploys on Horizen L3 (same Solidity, same EVM)
   - TEE handles confidential task matching/scoring
   - x402 facilitator gets selective disclosure access to payment receipts
   - USDC bridges from Base L2 to Horizen L3 (one additional hop)
   - Settlement confirmation flows back through x402 with TEE attestation
3. **Commitment hash approach from FOUNDATIONAL_TECH_ANALYSIS.md** (replace `request_id` with `H(request_id || salt)`) is still needed even on a privacy chain — defense in depth against data leaks during bridging or selective disclosure.

---

## Recommendation

### For v1.5 (shipping now)

**No change to architecture.** Base + application-layer privacy is correct.

- Continue with Base x402 settlement (Mode 1)
- Implement commitment hash in on-chain memos (already planned)
- Hide robot wallet addresses from public API (already planned)
- Encrypt task specs at rest in API layer (already planned)
- The settlement abstraction interface with 4 modes is validated by this analysis

### For v2.0-v2.1 (next 6 months)

**Add Horizen L3 on Base to the evaluation pipeline for Mode 2 (immediate private).**

Specific actions:
- Deploy a test escrow contract on Horizen L3 testnet (same Solidity, should be trivial)
- Test USDC bridging from Base L2 → Horizen L3 (latency, cost, reliability)
- Evaluate Horizen Confidential Compute Environment (HCCE) for TEE-based task matching — scheduled for full launch Q1 2026, should be available for integration testing
- Test x402 facilitator verification with Horizen's selective disclosure
- Monitor Aztec transaction launch — if transactions go live and the developer experience matures, evaluate as a longer-term option (but language barrier: Noir vs. Solidity is a real cost)

**Do NOT:**
- Deploy on a Prividium chain (wrong model — permissioned enterprise, not open marketplace)
- Wait for Aztec (too early, no transactions, new language)
- Wait for Miden (testnet only, mainnet late May 2026 at earliest)
- Depend on Fhenix CoFHE (FHE overhead is high, Base support "coming soon" but not live)

### For v3.0+ (12+ months)

**Re-evaluate the landscape.** By Q1 2027:
- Aztec should have live transactions and possibly USDC bridge support
- Miden mainnet should be live
- EU AMLR Article 79 enforcement begins July 2027 — the regulatory picture will be clearer
- Fhenix CoFHE on Base may be production-ready
- x402 privacy extensions (shielded-x402 or similar) may have matured

If Aztec delivers on its promise (cryptographic privacy + programmable smart contracts + reasonable developer experience), it becomes the strongest long-term candidate for Mode 2/4. But the Noir language requirement (not Solidity) is a significant adoption barrier.

If Horizen L3 continues maturing and HCCE proves reliable, it may be the pragmatic long-term choice: same EVM, same USDC, same Base ecosystem, added TEE privacy, compliant by design.

### Does the foundational tech analysis need to change?

**No.** The five key conclusions from FOUNDATIONAL_TECH_ANALYSIS.md all hold:

1. **Settlement abstraction is highest-leverage** — confirmed. Privacy chains don't eliminate the need for timing modes, and the abstraction enables evaluating Horizen L3 or Aztec without rewriting escrow logic.

2. **On-chain data hygiene** — confirmed and reinforced. Even on a privacy chain, commitment hashes and hidden addresses are defense-in-depth against bridge leaks and selective disclosure edge cases.

3. **Base is correct for v1.5-v2.0** — confirmed. No privacy chain has Base's USDC liquidity ($4.1B), x402 integration (Stripe), or developer ecosystem. Horizen L3 is interesting precisely because it lives within the Base ecosystem.

4. **Identity/reputation designed once** — confirmed. BBS+ credentials work regardless of settlement chain.

5. **Privacy is an application-layer concern** — **confirmed with nuance.** For v1.5-v2.0, application-layer privacy (TEE + encrypted storage) is correct. For v2.1+, chain-level privacy via Horizen L3 on Base may simplify Mode 2 implementation. But this is an optimization, not a foundational change — the same privacy goals (encrypted task specs, confidential scoring, selective disclosure) are achieved either way.

**The one addition:** Add Horizen L3 on Base as an explicit "evaluate for v2.1-P" item alongside the existing settlement abstraction plan. This was not in the original analysis because Horizen's mainnet launch on Base happened in March 2026.

---

## Sources

### ZKsync Prividium
- [ZKsync Prividium Official Page](https://www.zksync.io/prividium)
- [ZKsync Prividium Architecture Docs](https://docs.zksync.io/zk-stack/prividium/architecture)
- [ZKsync Prividium Features Docs](https://docs.zksync.io/zk-stack/prividium/features)
- [ZKsync Prividium Overview Docs](https://docs.zksync.io/zk-stack/prividium/overview)
- [Messari: Prividiums for Enterprise-Grade Privacy](https://messari.io/report/zksync-prividiums-for-enterprise-grade-privacy)
- [BlockEden: Prividium Banking Stack](https://blockeden.xyz/blog/2026/01/30/prividium-zksync-privacy-banking-stack-institutional-blockchain/)
- [Cryptonomist: ZKsync Prividium Corporate Privacy](https://en.cryptonomist.ch/2025/12/22/zksync-prividium-the-new-frontier-of-corporate-privacy-on-ethereum/)
- [99Bitcoins: ZKsync 2026 Plan](https://99bitcoins.com/news/altcoins/zksync-2026-privacy-roadmap/)
- [The Defiant: ZKsync Introduces Prividium](https://thedefiant.io/news/tradfi-and-fintech/zksync-introduces-private-blockchain-platform-prividium)
- [Cointelegraph: Cari Picks ZKsync Prividium](https://cointelegraph.com/news/cari-picks-zksync-prividium-regional-banks)
- [Memento ZK Chain (first live Prividium)](https://x.com/Memento_Bc/status/2011126255207231750)
- [ZK Nation Forum: Prividium Prize Winner Memento](https://forum.zknation.io/t/first-prividium-prize-winner-memento/853)

### Aztec Network
- [Aztec Official Site](https://aztec.network/)
- [Aztec Roadmap](https://aztec.network/roadmap)
- [Bankless: Privacy L2 Aztec Almost Ready](https://www.bankless.com/read/privacy-l2-aztec-is-almost-ready-for-primetime)
- [CoinDesk: Aztec Ignition Chain](https://www.coindesk.com/markets/2025/11/20/privacy-focused-aztec-network-s-ignition-chain-lights-up-on-ethereum/)
- [The Block: Aztec Public Testnet](https://www.theblock.co/post/352776/aztec-network-launches-public-testnet-for-privacy-focused-ethereum-layer-2)
- [Aztec: Noir 1.0 Pre-Release](https://aztec.network/blog/the-future-of-zk-development-is-here-announcing-the-noir-1-0-pre-release)
- [CoinGecko: What Is Aztec Network](https://www.coingecko.com/learn/what-is-aztec-network-ethereum-privacy-layer-2)

### Polygon Miden
- [CoinDesk: Miden Secures $25M](https://www.coindesk.com/tech/2025/04/29/polygon-spin-off-miden-secures-25m-to-bring-speed-privacy-to-institutional-giants/)
- [Miden Build / Roadmap](https://miden.xyz/build)
- [Polygon Blog: Miden Alpha Testnet v6](https://polygon.technology/blog/polygon-miden-alpha-testnet-v6-is-live)
- [Miden GitHub](https://github.com/0xMiden)

### Fhenix
- [Fhenix Official Site](https://www.fhenix.io/)
- [Fhenix: Privacy in DeFi 2025 Recap](https://www.fhenix.io/blog/privacy-in-defi-2025-landscape-recap)
- [The Block: Fhenix Series A](https://www.theblock.co/post/298443/ethereum-layer-2-fhenix-confidentiality-series-a-funding-testnet)
- [CoFHE Documentation](https://cofhe-docs.fhenix.zone/fhe-library/introduction/quick-start)
- [Fhenix CoFHE Contracts GitHub](https://github.com/FhenixProtocol/cofhe-contracts)

### Horizen
- [The Block: Horizen Launches L3 on Base](https://www.theblock.co/post/381846/privacy-horizen-launches-layer-3-base-mainnet)
- [BeInCrypto: Horizen Mainnet on Base](https://beincrypto.com/horizen-mainnet-launch-base/)
- [Horizen Blog: Welcome to Privacy on Base](https://blog.horizen.io/welcome-to-privacy-on-base)
- [Horizen Roadmap](https://www.horizen.io/roadmap)
- [Horizen Official Site](https://horizen.io/)
- [The Block: DCG-backed Horizen Transitions to Base](https://www.theblock.co/post/364064/horizen-zen-base-appchain)

### Oasis Sapphire
- [Oasis Sapphire Documentation](https://docs.oasis.io/build/sapphire/)
- [Oasis Sapphire Product Page](https://oasis.net/sapphire)
- [Oasis 2025 Roadmap](https://oasis.net/blog/2025-the-oasis-roadmap)
- [Oasis TEE Break Challenge](https://oasis.net/blog/oasis-tee-break-challenge)
- [Medium: Sapphire EVM Deep Dive](https://medium.com/@caerlower/sapphire-evm-explained-a-deep-dive-into-confidential-smart-contract-execution-on-oasis-7fcca7cf9e5c)

### x402 and Privacy Payments
- [x402 Official Site](https://www.x402.org/)
- [x402 V2 Launch](https://www.x402.org/writing/x402-v2-launch)
- [x402 GitHub](https://github.com/coinbase/x402)
- [shielded-x402 GitHub](https://github.com/nhestrompia/shielded-x402)
- [z402: Privacy-Preserving Micropayments](https://z402.cash/)
- [HoZK: x402 & ZK](https://www.hozk.io/articles/x402-zk-building-the-internets-payment-standard)
- [InfoQ: x402 Major Upgrade](https://www.infoq.com/news/2026/01/x402-agentic-http-payments/)

### Regulatory
- [CoinGeek: EU Banning Anonymous Wallets by 2027](https://coingeek.com/eu-law-banning-anonymous-digital-asset-wallets-by-2027-final/)
- [TechLawPolicy: EU vs Crypto Anonymity](https://techlawpolicy.com/2025/06/eu-vs-crypto-anonymity-what-you-need-to-know/)
- [Jones Day: AMLR Compliance](https://www.jonesday.com/en/insights/2025/07/crypto-assets-casps-and-amlcft-compliance-the-new-european-regulatory-landscape-under-mica-and-amlr)
- [arXiv: Privacy-Preserving Compliance via Selective Disclosure](https://arxiv.org/abs/2602.18539)
- [The Block: Year of Pragmatic Privacy](https://www.theblock.co/post/383680/aztec-zcash-year-pragmatic-privacy-root)

### Privacy Architecture
- [StarkWare: Blockchain Privacy](https://starkware.co/blog/blockchain-privacy/)
- [Blockworks Research: Programmable Privacy Landscape](https://app.blockworksresearch.com/unlocked/programmable-privacy-landscape)
- [insights4vc: Privacy Trends for 2026](https://insights4vc.substack.com/p/privacy-trends-for-2026)
