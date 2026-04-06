# R-034: ERC-2612 Permit Relay Security — MEV Risk, Replay Attacks, and Relay Wallet Custody

**Date:** 2026-04-06
**Topic ID:** R-034
**Module:** M18_x402
**Status:** complete
**Triggered by:** Commits 44ae91f and 2e6bfe9 (shipped 2026-04-05) — gasless USDC payment via ERC-2612 permit relay

---

## Executive Summary

- The `/api/relay-usdc` and `/api/commit-payment`/`/api/execute-payment` flows use a three-transaction pattern (permit → transferFrom → transferFrom) that is **non-atomic**: an MEV bot can front-run the intermediate transferFrom calls and drain the relay-authorized allowance between steps.
- Cross-chain replay risk is **mitigated** by Circle's USDC implementation (it binds the permit signature to chainId in the domain separator), but the relay server does **not validate** that the buyer-provided `chain_id` matches the permit's domain separator before submitting — this is a server-side gap.
- The relay wallet (`0x4b59...0d9`) is an EOA hot wallet holding ETH for gas. Gas depletion stops all USDC payments. There is no monitoring, alerting, or replenishment automation. This is a single-point-of-failure for the payment path at any task value.
- Circle's own USDC contract supports **EIP-3009 `transferWithAuthorization`**, which eliminates the permit+transferFrom split: one signed message → one atomic transfer. This is strictly safer than the current ERC-2612 approach for the relay use case.
- ERC-4337 paymaster is **not the right solution** at current scale. It adds substantial infrastructure complexity (bundler, EntryPoint, UserOperation) with no meaningful security advantage over the EIP-3009 approach for direct USDC payments.

---

## Findings

### 1. The Three-Transaction Non-Atomicity Problem

The current `handleRelayUsdc` function in `chatbot/src/index.js` (lines 1691–1701) submits three sequential on-chain transactions:

```
tx1: usdc.permit(owner, relayWallet, totalAmount, deadline, v, r, s)
tx2: usdc.transferFrom(owner, operator_wallet, operatorAmount)      // 88%
tx3: usdc.transferFrom(owner, platform_wallet, platformAmount)      // 12%
```

Each transaction is submitted to the public mempool independently. Between tx1 and tx2, the permit allowance is public on-chain — any EOA (or MEV bot) that monitors the chain can:
1. See that `owner` has authorized `relayWallet` to spend `totalAmount` USDC
2. Call `transferFrom(owner, attacker, totalAmount)` before tx2 is mined

This is not theoretical. A DeFi user lost $700K USDC to a sandwich attack on a similar pattern (see: https://www.fxstreet.com/cryptocurrencies/news/defi-user-loses-over-700k-usdc-in-a-sandwich-attack). The risk is highest on Ethereum mainnet (deeper mempool); Base mainnet has shorter blocks (~2 sec) and lower MEV activity, but the attack vector exists.

**Severity for YAK:** Construction tasks run $1,000–$45,000. An attacker who intercepts a single payment at the operator split step could steal the full authorized amount. The current code is live on Base mainnet.

**Immediate mitigation available:** The `handleExecutePayment` function (commit-on-hire flow) does check existing allowance and attempts to skip the permit if one is already set — this is good practice but does not address the race window.

**Structural fix:** Replace the three-transaction pattern with a single `transferWithAuthorization` call (see Finding 4).

---

### 2. Cross-Chain Replay Risk — Partially Mitigated

The concern from the roadmap note was: "permit signature replay on other chains if deadline is not enforced."

**Good news:** Circle's USDC contract uses a dynamic domain separator that includes `block.chainid` recomputed at call time, not fixed at deployment. This is per the OpenZeppelin ERC20Permit implementation and the EIP-2612 spec's recommended approach. A permit signature signed for Base mainnet (chain_id 8453) will be rejected by the Ethereum mainnet USDC contract (chain_id 1).

**Remaining gap:** The relay server (`handleRelayUsdc`) accepts `chain_id` from the request body and uses it to select the RPC endpoint and USDC contract address. It does **not** verify that the buyer's permit signature was actually signed for the provided `chain_id`. An attacker who has obtained a valid Base Sepolia test permit signature (low-value test transaction) cannot replay it on Base mainnet (USDC contract enforces domain), but the relay will happily route a bogus `chain_id` to the wrong contract and fail with a confusing error rather than a clean validation rejection.

**Server-side fix needed:** Before submitting, the relay should verify: `v, r, s` recovers to `owner` using the expected domain separator for the given `chain_id` and `usdcAddr`. This can be done with `ethers.verifyTypedData()` on the permit EIP-712 struct. Reject immediately if mismatch — saves gas and provides a cleaner error.

Sources:
- EIP-2612 spec: https://eips.ethereum.org/EIPS/eip-2612
- Chain split replay risk: https://github.com/code-423n4/2021-09-swivel-findings/issues/98
- DOMAIN_SEPARATOR and chainId: https://zokyo-auditing-tutorials.gitbook.io/zokyo-tutorials/tutorials/tutorial-4-block.chainid-domain_separator-and-eip-2612-permit

---

### 3. Relay Wallet as Hot Wallet — Gas Depletion Risk

The relay wallet `0x4b59...0d9` is a funded EOA whose private key is stored as a Cloudflare Worker secret (`RELAY_PRIVATE_KEY`). It pays gas for all permit and transferFrom transactions.

**Attack scenario (DoS):** An adversary who knows the relay endpoint exists can submit many small permit relay requests with valid signatures (or even invalid ones that fail on-chain). Each failed attempt costs the relay wallet gas. On Ethereum mainnet with high gas prices (~20–50 gwei), 100 failed transactions could deplete a relay wallet funded with 0.01 ETH. No payments would succeed until the wallet is manually refunded.

**Current state:** No gas balance monitoring. No alerting. No replenishment automation. The relay_address is returned in every success response (line 1717: `relay_address: relayWallet.address`), making the hot wallet address trivially discoverable.

**Best practices for relay wallet management:**
- Monitor ETH balance of relay wallet with a Cloudflare Cron trigger or external monitor; alert at < 0.01 ETH on Base, < 0.05 ETH on Ethereum mainnet
- Do not expose relay wallet address in API responses (remove `relay_address` field from production responses)
- Implement per-IP rate limiting on `/api/relay-usdc` (already exists for demo endpoints; confirm it covers relay endpoint)
- Consider OpenZeppelin Defender Relayer or Gelato relay (https://docs.gelato.network/web3-services/relay/what-is-relaying) for managed relay with automatic gas replenishment and usage limits

Source: ERC-1613 Gas Station Network design: https://eips.ethereum.org/EIPS/eip-1613

**Cloudflare Secrets Store (2026 update):** Cloudflare launched Secrets Store public beta in April 2025, providing centralized secret management with RBAC and audit logs. The `RELAY_PRIVATE_KEY` should be migrated to Secrets Store for centralized rotation and access control.
Source: https://blog.cloudflare.com/secrets-store-beta/

---

### 4. EIP-3009 transferWithAuthorization — The Better Approach

Circle's USDC contract on Base (and all other chains) implements **EIP-3009 `transferWithAuthorization`** in addition to ERC-2612 permit. This is the key difference:

| Feature | ERC-2612 permit + transferFrom | EIP-3009 transferWithAuthorization |
|---|---|---|
| Transactions | 3 (permit + 2× transferFrom) | 1 per destination |
| Atomicity | No — allowance window between permit and transfer | Yes — signature consumed in same tx as transfer |
| Nonce type | Sequential (one pending tx at a time) | Random 32-byte (supports concurrent txs) |
| Front-run surface | High — allowance visible on-chain | None — no allowance created |
| Replay protection | Nonce + deadline + domain separator | Nonce (random) + deadline + from + to binding |

The `transferWithAuthorization` function signature:
```solidity
function transferWithAuthorization(
  address from,
  address to,
  uint256 value,
  uint256 validAfter,
  uint256 validBefore,
  bytes32 nonce,
  uint8 v,
  bytes32 r,
  bytes32 s
)
```

For YAK's use case: instead of signing a permit (approve relay) and then having the relay do two transferFrom calls, the buyer would sign **two** `transferWithAuthorization` messages (one for 88% to operator, one for 12% to platform), and the relay would submit them. Each transfer is atomic — no allowance is ever created, no MEV window exists between authorization and execution.

**Additional protection:** `receiveWithAuthorization` (also in USDC) adds a caller check ensuring that only the intended payee can submit the authorization, preventing front-running of the authorization submission itself.

Sources:
- Circle's 4 authorization methods: https://www.circle.com/blog/four-ways-to-authorize-usdc-smart-contract-interactions-with-circle-sdk
- EIP-3009 spec: https://eips.ethereum.org/EIPS/eip-3009
- EIP-3009 overview: https://academy.extropy.io/pages/articles/review-eip-3009.html

---

### 5. ERC-4337 Paymaster — Not Recommended at Current Scale

The original hypothesis asked whether an ERC-4337 paymaster is safer than the current relay approach.

**Assessment: Not worth the complexity at current scale.**

ERC-4337 account abstraction requires:
- A bundler node to assemble UserOperations
- An EntryPoint contract interaction
- A paymaster contract deployment
- UserOperation lifecycle management (validation, execution, post-op)

For YAK's relay use case (relay pays gas, buyer signs USDC authorization), this complexity is unnecessary. The EIP-3009 approach achieves the same security properties (atomic transfer, no allowance window) with no new infrastructure. ERC-4337 becomes relevant if YAK later needs:
- Session keys (agent-authorized payments without per-tx signing)
- Multi-call batching across heterogeneous contracts
- Subscription-style recurring charges

Sources:
- ERC-4337 paymasters security: https://osec.io/blog/2025-12-02-paymasters-evm/
- ERC-4337 overview: https://docs.erc4337.io/paymasters/index.html

---

### 6. Permit2 (Uniswap) — Not Applicable Here

Uniswap's Permit2 is a universal approval contract that extends permit-style approvals to tokens that do not implement ERC-2612. Since Circle's USDC already implements both ERC-2612 and EIP-3009 natively, Permit2 adds no value and introduces an additional contract dependency.

Source: https://github.com/Uniswap/permit2

---

### 7. MEV Protection via Private Mempool — Partial Mitigation

If the relay switches the RPC endpoint to a Flashbots Protect endpoint (https://docs.flashbots.net/flashbots-protect/quick-start), transactions are submitted to a private mempool. This would prevent MEV bots from seeing pending transactions and front-running the transferFrom step. Flashbots Protect supports Base mainnet as of 2025.

**However:** This is a mitigation on top of a broken pattern, not a fix. The fundamental issue is three non-atomic transactions. EIP-3009 is the structural fix; Flashbots Protect is an optional defense-in-depth measure.

---

## Implications for the Product

1. **The permit+transferFrom three-tx pattern is the primary risk.** For construction-scale payments ($1K–$45K), an MEV bot intercepting the allowance window between permit and transferFrom could steal the full authorized amount. This should be treated as a production security issue, not a research finding.

2. **EIP-3009 migration is the correct fix and it is backwards compatible.** The buyer UX change is minimal: instead of signing one permit message, they sign two `transferWithAuthorization` messages (or one, if the relay aggregates through a smart contract). The relay submits two transactions instead of three, but each is atomic. No allowance is ever created.

3. **The relay wallet address should not be returned in API responses.** Currently `relay_address` is included in the success JSON. This reveals the hot wallet address, allowing adversaries to monitor its ETH balance and plan DoS attacks. Remove from production responses.

4. **Gas monitoring is required before going to production at full task values.** A depleted relay wallet means all USDC payments fail silently. Add a Cloudflare Cron trigger that checks relay ETH balance and writes to a health KV key; alert if below threshold.

5. **Server-side permit signature pre-verification** (using `ethers.verifyTypedData`) should be added before any on-chain submission. Reduces wasted gas on invalid signatures and provides cleaner client error messages.

6. **The commit-on-hire flow (`/api/commit-payment` + `/api/execute-payment`) has better deadline validation** (5-minute minimum margin enforced server-side) than the direct relay flow. This is a good pattern. Apply the same deadline floor to `handleRelayUsdc`.

---

## Improvement Proposals

### IMP-027: Migrate permit relay to EIP-3009 transferWithAuthorization
Replace the three-transaction permit+transferFrom pattern with two `transferWithAuthorization` calls. Eliminates the MEV allowance window. Requires frontend change to sign two EIP-712 messages instead of one permit. USDC on Base already supports this.
- Module: M18_x402
- Effort: medium
- Priority: high (security)

### IMP-028: Add server-side permit signature pre-verification
Before submitting any permit to the chain, call `ethers.verifyTypedData(domain, types, value, signature)` and confirm the recovered address matches `owner`. Rejects invalid/mismatched signatures before wasting relay wallet gas.
- Module: M18_x402
- Effort: small
- Priority: high

### IMP-029: Add relay wallet gas balance monitoring (Cloudflare Cron)
Add a Cron Trigger in `wrangler.toml` that runs every 15 minutes, reads the relay wallet ETH balance, and writes a health status to KV. Alert (via email webhook or Cloudflare notification) if balance drops below 0.01 ETH on Base or 0.05 ETH on Ethereum mainnet.
- Module: M34_admin_console
- Effort: small
- Priority: high

### IMP-030: Remove relay_address from API success response
The relay wallet address is returned in every `/api/relay-usdc` success response. Remove from production responses to prevent adversaries from targeting the hot wallet.
- Module: M18_x402
- Effort: small
- Priority: medium

### IMP-031: Add deadline floor validation to handleRelayUsdc
The direct relay endpoint (`handleRelayUsdc`) does not enforce a minimum deadline margin. The commit-on-hire flow correctly requires 5 minutes. Apply the same `minDeadline = now + 300` check to `handleRelayUsdc`.
- Module: M18_x402
- Effort: small
- Priority: medium

---

## New Questions Spawned

- **R-035**: EIP-3009 `transferWithAuthorization` implementation guide for USDC on Base — what does the buyer UX look like for signing two authorization messages, and can they be combined into a single relay transaction via multicall?
- **R-036**: Flashbots Protect support for Base mainnet — does the Flashbots Protect RPC work with ethers.js v6 in Cloudflare Workers, and what is the latency vs standard RPC for construction-scale payment flows?

---

## Feedback Issue Processing

Processed 6 open feedback issues (numbers 4–9) on yakroboticsgarage/yakrover-marketplace:
- All 6 are automated demo feedback submitted by `rafathebuilder-ZK`
- Issues 4–7: Explicitly marked as test feedback by the submitter ("disregard", "discard", "this is a test")
- Issue 8: Test confirmation of on-chain fakerovers ("Onchain fakerovers worked")
- Issue 9: One genuine production user comment — "Great data, thank you for your service Tumbller!" (5-star rating, USDC payment confirmed, Tumbller-Finland-01 robot)
- **Pattern:** The feedback system is working end-to-end (automated issue creation confirmed). No complaints or feature requests. The single genuine feedback is positive.
- **Signal from issue 9:** Real on-chain USDC payment completed successfully. Robot Tumbller-Finland-01 (ERC-8004 token ID 38947) executed and received payment. This validates v1.1 milestone-4.
- **No new research topics spawned from feedback.**
- **No improvement proposals from feedback** — system working as designed.

Issues are being closed as processed (see commit).

---

## Sources

- EIP-2612 spec: https://eips.ethereum.org/EIPS/eip-2612
- EIP-3009 spec: https://eips.ethereum.org/EIPS/eip-3009
- EIP-3009 overview: https://academy.extropy.io/pages/articles/review-eip-3009.html
- Circle's 4 authorization methods: https://www.circle.com/blog/four-ways-to-authorize-usdc-smart-contract-interactions-with-circle-sdk
- DOMAIN_SEPARATOR and chainId: https://zokyo-auditing-tutorials.gitbook.io/zokyo-tutorials/tutorials/tutorial-4-block.chainid-domain_separator-and-eip-2612-permit
- Chain split replay risk: https://github.com/code-423n4/2021-09-swivel-findings/issues/98
- Permit2 vs ERC-2612: https://medium.com/@gwrx2005/permit2-a-next-generation-token-approval-mechanism-7603d292ddfc
- Flashbots Protect: https://docs.flashbots.net/flashbots-protect/overview
- Flashbots Protect quick start: https://docs.flashbots.net/flashbots-protect/quick-start
- ERC-4337 paymasters: https://osec.io/blog/2025-12-02-paymasters-evm/
- ERC-4337 docs: https://docs.erc4337.io/paymasters/index.html
- OpenZeppelin Relayers: https://docs.openzeppelin.com/defender/module/relayers
- Gelato relay: https://docs.gelato.network/web3-services/relay/what-is-relaying
- ERC-1613 Gas Station Network: https://eips.ethereum.org/EIPS/eip-1613
- Cloudflare Secrets Store: https://blog.cloudflare.com/secrets-store-beta/
- $700K USDC sandwich attack: https://www.fxstreet.com/cryptocurrencies/news/defi-user-loses-over-700k-usdc-in-a-sandwich-attack-that-experts-suggest-could-be-money-laundering-202503130610
- Flashbots race condition (Jan 2026): https://mavlevin.com/2026/01/18/flashbots-mev-relay-race-condition-vulnerability
