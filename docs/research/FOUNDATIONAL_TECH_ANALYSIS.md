# Foundational Tech Build Analysis

**Date:** 2026-03-26
**Status:** Approved analysis — informs v1.5 architecture decisions
**Source:** Cross-synthesis of RESEARCH_SYNTHESIS_LUNAR.md, RESEARCH_SYNTHESIS_PRIVATE.md, RESEARCH_CRITIQUE.md, and ROADMAP_v2.md

---

## Six Foundational Considerations

### 1. Settlement Abstraction Is the Single Highest-Leverage Decision

The research converged on this from two completely independent directions — lunar needs batched async settlement over DTN links, privacy needs shielded settlement on a future chain. If `RobotTaskEscrow.sol` is built with Base-specific x402 calls hardcoded in, it will need to be rewritten twice.

**What to build now:** A `SettlementMode` interface with four modes (immediate/batched × transparent/private). Only mode 1 (immediate transparent, Base x402) ships in v1.5. The other three are empty implementations behind the same interface. The cost is ~1-2 days of design work. The cost of *not* doing it is a full escrow rewrite at v2.1.

| Mode | Timing | Privacy | Chain | Version |
|------|--------|---------|-------|---------|
| 1. Immediate transparent | Real-time | Public | Base / x402 | v1.5 (implemented) |
| 2. Immediate private | Real-time | Shielded | Base + Privacy Pools or future chain | v2.1-P |
| 3. Batched transparent | Async / DTN windows | Public | Base | v2.1-L |
| 4. Batched private | Async / DTN windows | Shielded | Future | v3.0 |

### 2. On-Chain Data Hygiene — Three Small Changes That Prevent Permanent Leaks

These are cheap now, expensive or impossible later because blockchain data is immutable:

- **Remove `request_id` from on-chain memos.** Replace with `H(request_id || salt)`. Breaks the permanent public link between tasks and payments. Audit capability preserved via platform database.
- **Hide robot wallet addresses from the public API.** Use platform-internal IDs. Translate to on-chain addresses only inside the settlement layer.
- **Don't add new metadata fields to ERC-8004 entries.** Every field on-chain is permanent and public. Adding pricing, reputation, or capability metadata on-chain creates a surveillance surface.

These changes directly conflict with AD-3 (raw `request_id` on-chain). That decision was correct for v1.0's goals but becomes a liability when privacy enters the picture.

### 3. Chain Selection: Base Is Correct, but for the Right Reasons

Both research tracks independently concluded "stay on Base." The privacy research initially recommended designing for Aleo migration; the critique overruled:

- EU AMLR Article 79 bans CASPs from handling privacy-preserving digital assets by mid-2027. Finland is an early enforcer. Makes Aleo unusable for seed market.
- Privacy features that ARE legally viable (TEE-based platform confidentiality, viewer keys, selective disclosure) are application-layer — they work on any chain.
- Aleo + USDCx is real (Circle-backed, mainnet since Jan 2026), but no identified user today.

**Decision:** Base for v1.5 through v2.0. Aleo is a monitor target only. Settlement abstraction preserves optionality.

### 4. Identity and Reputation Must Be Designed Once, Not Per-Track

- **ERC-8004 stays as identity anchor.** Don't layer more metadata onto it on-chain.
- **BBS+ credentials** are the privacy-compatible reputation layer. One schema, two update protocols:
  - Earth (low-latency): credential reissued within seconds of task completion
  - Lunar (DTN-tolerant): credential reissued on Earth, relayed via DTN, stale credentials accepted with configurable scoring discount

Credential schema: task count, success rate, avg completion time, capability attestations, environmental survival history (lunar-only).

**Caveat:** BBS+ threshold issuance requires 3+ independent nodes. At seed scale, platform runs all nodes — threshold trust is theater. Implement the protocol anyway (right abstraction) but don't pretend real trust distribution exists until independent operators run issuer nodes.

### 5. Privacy Is an Application-Layer Concern, Not a Chain-Layer Concern

The most important finding. The original research asked "does the chain need to change?" Answer: **no**.

- Full ZK privacy (chain-level) is legally problematic in EU
- Useful privacy (encrypted task specs, confidential scoring, viewer keys, selective disclosure) is TEE and application-layer
- At seed scale, cryptographic anonymity is security theater (anonymity set too small). But payload *confidentiality* is valuable at any scale.

**Implication:** Don't need a privacy chain. Need encrypted storage, TEE enclaves for matching/scoring, viewer key system. v1.5 should implement payload confidentiality in API layer even before TEE ships in v2.0.

### 6. DTN Protocol Layer Is Shared Infrastructure

DTN/Bundle Protocol is the lunar transport, but privacy features (encrypted task specs, ZK proofs, credential updates) must also travel over DTN for lunar operations:

- DTN message protocol needs to handle encryption, proof bundling, credential transport natively
- BBS+ credential updates over DTN introduce staleness (hours of outdated reputation data)
- TEE proof generation round-trip (robot → DTN → Earth TEE → DTN → robot) could take hours

**Design now:** DTN message schema extensible enough for auction messages, encrypted specs, ZK proofs, and credentials. Don't build DTN transport yet (v2.1-L) but define format in v1.5.

---

## What Ships in v1.5 vs. What's Designed in v1.5

| Ships (implemented) | Designed (interface only) |
|---|---|
| x402 on Base (mode 1) | Settlement abstraction interface (4 modes) |
| Commitment hash in on-chain memos | DTN message schema |
| Robot wallet addresses hidden from API | BBS+ credential schema |
| Encrypted task specs at rest (API layer) | TEE enclave interface for matching/scoring |

Total overhead on v1.5: ~1-2 weeks of design work beyond existing scope. Payoff: v2.0, v2.1-L, and v2.1-P don't require rewrites.

---

## Open Research: Privacy Base-Layer Chain Comparison

**Status:** Complete — see `RESEARCH_PRIVACY_CHAINS.md` for full comparative analysis of ZKsync Prividium, Aztec, Polygon Miden, Fhenix, Horizen L3, and Oasis Sapphire. Key finding: Prividium is enterprise-permissioned (wrong model for open marketplace), Aztec is pre-transaction, and **Horizen L3 on Base** is the most architecturally relevant option for Mode 2 settlement — same EVM, same USDC liquidity, TEE-based compliant privacy. All five foundational conclusions confirmed; one addition: evaluate Horizen L3 for v2.1-P.
