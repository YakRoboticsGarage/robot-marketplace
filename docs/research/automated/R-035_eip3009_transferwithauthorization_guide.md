# R-035: EIP-3009 transferWithAuthorization — Implementation Guide for USDC on Base

**Date:** 2026-04-07
**Topic ID:** R-035
**Module:** M18_x402
**Status:** complete
**Spawned from:** R-034 (ERC-2612 permit relay security)
**Priority:** high

---

## Executive Summary

- EIP-3009 `transferWithAuthorization` is natively implemented in Circle's USDC on Base mainnet (v2.2). It is **strictly safer** than the current `permit + transferFrom` pattern: no on-chain allowance is created, no MEV front-run window exists between authorization and transfer.
- For YAK's 88%/12% split, the buyer must sign **two separate** EIP-712 authorization messages — one per recipient. Each nonce must be a **random 32-byte value** (not sequential), allowing both to be submitted concurrently without ordering constraints.
- The relay can batch both `transferWithAuthorization` calls through **Multicall3** (deployed at `0xcA11bde05977b3631167028862bE2a173976CA11` on Base mainnet) in a single transaction, making the 88%/12% split effectively atomic from the relay's perspective.
- `receiveWithAuthorization` adds an additional caller check (only the payee contract can submit), but **requires each destination to be a smart contract** that calls the function itself — not compatible with EOA recipients or the current relay design. Use `transferWithAuthorization` for relay-submitted payments to EOA/multisig wallets.
- The frontend change is minimal: replace one `signTypedData` call (permit) with two `signTypedData` calls (two authorizations). The USDC domain name is `"USD Coin"`, version `"2"`.

---

## Findings

### 1. EIP-3009 Protocol — What It Is

EIP-3009 (`transferWithAuthorization`) is an extension of ERC-20 that enables atomic, relay-submitted token transfers via off-chain EIP-712 signatures. It differs from ERC-2612 (permit) in a critical way:

| Property | ERC-2612 permit + transferFrom | EIP-3009 transferWithAuthorization |
|---|---|---|
| On-chain allowance created? | Yes — between permit and transferFrom | No — signature consumed atomically |
| MEV front-run window? | Yes — allowance visible in mempool | None |
| Nonce type | Sequential (uint256) | Random bytes32 |
| Concurrent transactions? | No — sequential nonce | Yes — random nonce, any order |
| Transactions required | 3 (permit + 2x transferFrom) | 2 (one per recipient) |
| Replay protection | Sequential nonce + deadline + domain | Random nonce + deadline + from+to binding |

USDC on Base mainnet (v2.2) implements both ERC-2612 and EIP-3009. The contract address is `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`.

Sources:
- EIP-3009 specification: https://eips.ethereum.org/EIPS/eip-3009
- Circle USDC v2.2 announcement: https://www.circle.com/blog/announcing-usdc-v2-2
- x402 spec using EIP-3009: https://github.com/coinbase/x402/blob/main/specs/schemes/exact/scheme_exact_evm.md

---

### 2. Exact ABI and Function Signatures

The `transferWithAuthorization` and `receiveWithAuthorization` Solidity function signatures (from the canonical CoinbaseStablecoin implementation):

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
) external;

function receiveWithAuthorization(
    address from,
    address to,
    uint256 value,
    uint256 validAfter,
    uint256 validBefore,
    bytes32 nonce,
    uint8 v,
    bytes32 r,
    bytes32 s
) external;

function authorizationState(address authorizer, bytes32 nonce) view returns (bool);

function cancelAuthorization(
    address authorizer,
    bytes32 nonce,
    uint8 v,
    bytes32 r,
    bytes32 s
) external;
```

**EthersJS ABI fragments to add to `USDC_ABI` in `chatbot/src/index.js`:**

```javascript
"function transferWithAuthorization(address from, address to, uint256 value, uint256 validAfter, uint256 validBefore, bytes32 nonce, uint8 v, bytes32 r, bytes32 s)",
"function receiveWithAuthorization(address from, address to, uint256 value, uint256 validAfter, uint256 validBefore, bytes32 nonce, uint8 v, bytes32 r, bytes32 s)",
"function authorizationState(address authorizer, bytes32 nonce) view returns (bool)",
"function cancelAuthorization(address authorizer, bytes32 nonce, uint8 v, bytes32 r, bytes32 s)",
```

**Type hash constants** (from CoinbaseStablecoin/eip-3009 source — useful for server-side pre-verification):

```
TRANSFER_WITH_AUTHORIZATION_TYPEHASH:
  keccak256("TransferWithAuthorization(address from,address to,uint256 value,uint256 validAfter,uint256 validBefore,bytes32 nonce)")

RECEIVE_WITH_AUTHORIZATION_TYPEHASH:
  keccak256("ReceiveWithAuthorization(address from,address to,uint256 value,uint256 validAfter,uint256 validBefore,bytes32 nonce)")
```

Source: https://github.com/CoinbaseStablecoin/eip-3009/blob/master/contracts/lib/EIP3009.sol

---

### 3. EIP-712 Domain and Signing Payload

**USDC domain separator (exact values — confirmed from CoinbaseStablecoin gist and x402 spec):**

```javascript
const domain = {
  name: "USD Coin",     // exactly this string — not "USDC"
  version: "2",         // string "2" — not integer
  chainId: 8453,        // Base mainnet; 84532 for Base Sepolia
  verifyingContract: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
  // Base Sepolia: "0x036CbD53842c5426634e7929541eC2318f3dCF7e"
};
```

**Type definition (must match exactly — field order matters for EIP-712 hashing):**

```javascript
const types = {
  TransferWithAuthorization: [
    { name: "from",        type: "address" },
    { name: "to",          type: "address" },
    { name: "value",       type: "uint256" },
    { name: "validAfter",  type: "uint256" },
    { name: "validBefore", type: "uint256" },
    { name: "nonce",       type: "bytes32" },
  ],
};
```

**Message construction (frontend — buyer signs two messages):**

```javascript
import { ethers } from "ethers";

// Generate random bytes32 nonces — one per transfer
function randomNonce() {
  return ethers.hexlify(ethers.randomBytes(32));
}

const now = Math.floor(Date.now() / 1000);
const validBefore = now + 3600; // 1-hour window (adjust as needed)
const validAfter = 0;            // active immediately

// Authorization 1: 88% to operator
const operatorNonce = randomNonce();
const operatorMessage = {
  from:        buyerAddress,
  to:          operatorWalletAddress,    // 88% destination
  value:       operatorAmount,           // BigInt, in USDC smallest units (6 decimals)
  validAfter:  validAfter,
  validBefore: validBefore,
  nonce:       operatorNonce,
};

// Authorization 2: 12% to platform
const platformNonce = randomNonce();
const platformMessage = {
  from:        buyerAddress,
  to:          platformWalletAddress,    // 12% destination
  value:       platformAmount,
  validAfter:  validAfter,
  validBefore: validBefore,
  nonce:       platformNonce,
};

// ethers.js v6 — both sign calls happen in the buyer's wallet (MetaMask/Rabby)
const provider = new ethers.BrowserProvider(window.ethereum);
const signer = await provider.getSigner();

// Note: ethers v6 signTypedData does NOT include "EIP712Domain" in types
const sig1 = await signer.signTypedData(domain, types, operatorMessage);
const sig2 = await signer.signTypedData(domain, types, platformMessage);

// Split signature components for relay submission
const { v: v1, r: r1, s: s1 } = ethers.Signature.from(sig1);
const { v: v2, r: r2, s: s2 } = ethers.Signature.from(sig2);
```

**Send to relay endpoint (POST body):**

```json
{
  "chain_id": 8453,
  "owner": "0x<buyer-address>",
  "operator_wallet": "0x<operator>",
  "platform_wallet": "0xe33356d0d16c107eac7da1fc7263350cbdb548e5",
  "operator_amount": "<uint256-string>",
  "platform_amount": "<uint256-string>",
  "valid_before": 1234567890,
  "operator_nonce": "0x<32-bytes-hex>",
  "platform_nonce": "0x<32-bytes-hex>",
  "v1": 27, "r1": "0x...", "s1": "0x...",
  "v2": 28, "r2": "0x...", "s2": "0x..."
}
```

---

### 4. Relay-Side Submission

**Option A: Two sequential transactions (drop-in replacement for current three-tx pattern)**

```javascript
// chatbot/src/index.js — handleRelayUsdc (EIP-3009 version)
const usdc = new ethers.Contract(usdcAddr, USDC_ABI_EIP3009, relayWallet);

// Transfer 1: operator (88%)
const opTx = await usdc.transferWithAuthorization(
  owner, operator_wallet, operatorAmount,
  validAfter, validBefore, operatorNonce,
  v1, r1, s1
);
const opReceipt = await opTx.wait();

// Transfer 2: platform (12%)
const platTx = await usdc.transferWithAuthorization(
  owner, platform_wallet, platformAmount,
  validAfter, validBefore, platformNonce,
  v2, r2, s2
);
const platReceipt = await platTx.wait();
```

This reduces the transaction count from 3 to 2, eliminates the MEV allowance window, and handles the split correctly.

**Option B: Batch via Multicall3 (single transaction, atomic from relay perspective)**

Multicall3 is deployed at `0xcA11bde05977b3631167028862bE2a173976CA11` on Base mainnet (same address on 70+ chains). The `aggregate3` function executes an array of calls in one transaction, with per-call `allowFailure` control.

```javascript
const MULTICALL3_ADDRESS = "0xcA11bde05977b3631167028862bE2a173976CA11";
const MULTICALL3_ABI = [
  "function aggregate3(tuple(address target, bool allowFailure, bytes callData)[] calls) payable returns (tuple(bool success, bytes returnData)[] returnData)"
];

const usdcInterface = new ethers.Interface(USDC_ABI_EIP3009);

const call1 = usdcInterface.encodeFunctionData("transferWithAuthorization", [
  owner, operator_wallet, operatorAmount,
  validAfter, validBefore, operatorNonce,
  v1, r1, s1
]);
const call2 = usdcInterface.encodeFunctionData("transferWithAuthorization", [
  owner, platform_wallet, platformAmount,
  validAfter, validBefore, platformNonce,
  v2, r2, s2
]);

const multicall = new ethers.Contract(MULTICALL3_ADDRESS, MULTICALL3_ABI, relayWallet);
const results = await multicall.aggregate3([
  { target: usdcAddr, allowFailure: false, callData: call1 },
  { target: usdcAddr, allowFailure: false, callData: call2 },
]);
```

With `allowFailure: false`, if either transfer fails the entire multicall reverts — providing true atomicity (both succeed or neither does). This is the closest to a single atomic payment for split destinations without deploying a custom contract.

**Gas comparison (approximate, Base mainnet at ~0.005–0.2 gwei):**

| Pattern | Transactions | Approx gas (units) | Cost at $3,500 ETH, 0.01 gwei |
|---|---|---|---|
| Current: permit + 2x transferFrom | 3 | ~165,000 | ~$0.006 |
| EIP-3009: 2x transferWithAuthorization | 2 | ~130,000 | ~$0.005 |
| EIP-3009 via Multicall3 | 1 | ~145,000 | ~$0.005 |

Gas costs on Base are negligible for construction-scale payments ($1K–$45K). The primary driver for migration is security (MEV elimination), not gas savings.

Source: https://www.bitget.com/wiki/gas-fees-for-transferring-usdc-on-the-base-network

---

### 5. transferWithAuthorization vs receiveWithAuthorization — Which to Use

**transferWithAuthorization:** Any relayer (EOA or contract) can call it. Suitable for YAK's relay wallet pattern where the relay is an EOA Cloudflare Worker.

**receiveWithAuthorization:** Only the `to` address can be the `msg.sender`. This prevents front-running of the relay's mempool submission — an attacker who intercepts the signed authorization cannot redirect the payment, because only the destination contract can submit it.

**For YAK's current design:** `transferWithAuthorization` is correct. The destinations (operator EOA wallet, platform EOA) cannot call the USDC contract themselves. `receiveWithAuthorization` would require each destination to be a smart contract that calls `receiveWithAuthorization` in its own execution context.

**Important caveat on front-running:** With `transferWithAuthorization` submitted by a relay, an attacker watching the mempool can see the signed authorization and submit it first. The transfer still goes to the correct `to` address (the signature binds `from`, `to`, `value`, and `nonce`) — so the attacker cannot redirect funds. The risk is they could cause the relay's transaction to fail (wasting relay gas) by submitting earlier. This is a nuisance/DoS risk, not a theft risk. For defense-in-depth, submit via Flashbots Protect RPC (see R-036).

Source: https://github.com/CoinbaseStablecoin/eip-3009/blob/master/contracts/lib/EIP3009.sol

---

### 6. Nonce Management

EIP-3009 uses a **random bytes32 nonce** (not sequential). This is a key design choice:

- Sequential nonces (ERC-2612) prevent concurrent transactions — each pending nonce blocks the next.
- Random nonces allow multiple pending authorizations simultaneously (e.g., operator payment and platform fee submitted in parallel).

**Nonce reuse check:** The relay should call `usdc.authorizationState(owner, nonce)` before submission. If `true`, the nonce was already consumed (replay). If the buyer accidentally signs with a reused nonce (extremely unlikely with 32-byte random, but possible if client state is corrupted), the relay should detect and request a new signature.

```javascript
// Pre-check nonce freshness before on-chain submission
const nonce1Used = await usdc.authorizationState(owner, operatorNonce);
const nonce2Used = await usdc.authorizationState(owner, platformNonce);
if (nonce1Used || nonce2Used) {
  return errorResponse("Nonce already used — request new signatures from buyer");
}
```

**Nonce cancellation:** `cancelAuthorization` allows the buyer to invalidate a signed authorization before it is submitted. This is the mechanism for a buyer to revoke a payment authorization that is no longer needed (e.g., task cancelled before robot deployment). This is superior to ERC-2612 where there is no way to cancel a valid signed permit.

---

### 7. x402 Protocol Alignment

The x402 protocol (Coinbase's payment standard for AI agents) uses EIP-3009 `transferWithAuthorization` as its settlement mechanism for USDC. The x402 `exact/evm` scheme specification:

1. Buyer signs a `TransferWithAuthorization` message
2. The facilitator receives the signature and authorization parameters in the `PAYMENT-SIGNATURE` header
3. Settlement is performed by calling `transferWithAuthorization()` on the token contract
4. x402 is designed for single-recipient transfers (no split payment pattern in the spec)

For YAK's 88%/12% split, the two-message / two-call approach (or Multicall3 batch) is not directly supported by x402's single-transfer spec. YAK's relay approach with two authorizations is the correct pattern — consistent with how x402 facilitators work, extended for split destinations.

Source: https://github.com/coinbase/x402/blob/main/specs/schemes/exact/scheme_exact_evm.md

---

### 8. Frontend UX Impact

**Current flow (ERC-2612):**
1. Buyer clicks "Pay"
2. Wallet prompts: "Sign permit to authorize relay to spend X USDC"
3. One signature request

**New flow (EIP-3009):**
1. Buyer clicks "Pay"
2. Wallet prompts: "Sign transfer of 88% USDC to [operator address]"
3. Wallet prompts: "Sign transfer of 12% USDC to [platform address]"
4. Two signature requests in sequence

**UX concern:** Two signature prompts may feel like extra friction. Mitigation options:
- Display a clear "Step 1 of 2 — authorize operator payment" / "Step 2 of 2 — authorize platform fee" flow
- Combine into a single wallet prompt using `eth_signTypedData_v4` with a UI label that says "Sign payment authorization (2 of 2)"
- No gas is paid by the buyer at either step — wallet shows it as a gasless signature

**No wallet funding required:** As with ERC-2612 permits, both `transferWithAuthorization` signings are pure off-chain EIP-712 operations. The buyer pays no gas. Only the relay pays gas.

---

## Implications for the Product

1. **The migration path from ERC-2612 to EIP-3009 is clear and low-risk.** The API contract changes (two auth objects instead of one permit), but the security improvement is substantial: no on-chain allowance, no MEV window, random nonces for concurrency.

2. **Multicall3 provides atomic split payment** in a single relay transaction. Deploy `allowFailure: false` so partial splits fail atomically rather than leaving one recipient paid and the other not.

3. **The `cancelAuthorization` function provides a buyer escape hatch** that ERC-2612 permit does not. Wire it to the task cancellation flow: when a buyer cancels a task after signing authorizations but before robot deployment, call `cancelAuthorization` to invalidate the signed transfers.

4. **Server-side nonce freshness check** (`authorizationState`) should be added before submission to catch edge cases where the buyer reuses a nonce across retried form submissions.

5. **The x402 facilitator pattern** confirms this design. YAK's relay is architecturally equivalent to an x402 facilitator — EIP-3009 is the correct primitive for both.

6. **USDC v2.2 (deployed on Base) provides 6–7% gas reduction** for `transferWithAuthorization` vs v2.1. No code changes needed to benefit — the deployed contract already uses the optimized implementation.

---

## Improvement Proposals

### IMP-035: Implement EIP-3009 relay endpoint with Multicall3 batch submission
Replace the `handleRelayUsdc` and `handleExecutePayment` functions in `chatbot/src/index.js` with an EIP-3009 implementation. Buyer signs two `TransferWithAuthorization` messages (operator 88%, platform 12%). Relay submits both via Multicall3 `aggregate3` with `allowFailure: false` for atomic split. Remove the three ERC-2612 fields from `USDC_ABI` and replace with four EIP-3009 ABI fragments. See Finding 2 for exact ABI strings.
- Module: M18_x402
- Effort: medium
- Priority: high (security — eliminates MEV front-run window on live Base mainnet payments)

### IMP-036: Add cancelAuthorization to task cancellation flow
When a buyer cancels a task that has already had payment authorizations signed (but relay not yet submitted), call `usdc.cancelAuthorization(owner, nonce, v, r, s)` using the stored nonces to invalidate the buyer's signed transfers. This prevents the relay from accidentally submitting a stale authorization after task cancellation. Store nonces in KV alongside the commitment record.
- Module: M18_x402
- Effort: small
- Priority: medium

### IMP-037: Add authorizationState nonce freshness check to relay endpoint
Before submitting `transferWithAuthorization` on-chain, call `usdc.authorizationState(owner, nonce)` for each nonce. If `true`, the nonce was already consumed — return a clear error asking the buyer to re-sign with fresh nonces. This prevents confusing on-chain revert errors from duplicate submission attempts.
- Module: M18_x402
- Effort: small
- Priority: medium

---

## New Questions Spawned

- **R-036** (already queued): Flashbots Protect RPC compatibility with Cloudflare Workers and Base mainnet — for defense-in-depth against relay submission front-running even after EIP-3009 migration.
- **R-038** (new): The commit-on-hire flow stores the permit in KV and executes later when the robot is assigned. In the EIP-3009 design, the buyer signs two authorizations at hire-time. The `validBefore` timestamp must cover the robot deployment window. Research: what is the right `validBefore` window for commit-on-hire? Also: should the commit-on-hire flow use Multicall3 batch, or sequential for resume-safety?

---

## Feedback Issue Processing

Reviewed 2 open feedback issues on yakroboticsgarage/yakrover-marketplace (issues #10 and #11, both labeled `feedback`):
- Both submitted by `rafathebuilder-ZK` on 2026-04-06
- Both explicitly marked as test submissions for Demo-4 setup ("This is a test for Demo4 setup. Please disregard")
- Both are 5-star buyer feedback on FakeRover-Berlin-01 with USDC payments confirmed on-chain
- Pattern: Demo-4 is being set up and tested. No real user feedback.
- No actionable product insights. No new research topics spawned from feedback.

---

## Sources

- EIP-3009 specification: https://eips.ethereum.org/EIPS/eip-3009
- CoinbaseStablecoin EIP3009.sol reference: https://github.com/CoinbaseStablecoin/eip-3009/blob/master/contracts/lib/EIP3009.sol
- Circle's 4 USDC authorization methods: https://www.circle.com/blog/four-ways-to-authorize-usdc-smart-contract-interactions-with-circle-sdk
- Circle USDC v2.2 announcement: https://www.circle.com/blog/announcing-usdc-v2-2
- x402 EVM scheme spec (EIP-3009 usage): https://github.com/coinbase/x402/blob/main/specs/schemes/exact/scheme_exact_evm.md
- EIP-3009 extropy overview: https://academy.extropy.io/pages/articles/review-eip-3009.html
- EIP-3009 overview (DEV community): https://dev.to/extropy/an-overview-of-eip-3009-transfer-with-authorisation-3j50
- EIP-3009 forwarder contract: https://github.com/TheGreatAxios/eip3009-forwarder
- Multicall3 repository: https://github.com/mds1/multicall3
- USDC Base gas fees reference: https://www.bitget.com/wiki/gas-fees-for-transferring-usdc-on-the-base-network
- ethers.js v6 docs: https://docs.ethers.org/v6/single-page/
- MetaMask eth_signTypedData_v4: https://docs.metamask.io/wallet/reference/json-rpc-methods/eth_signtypeddata_v4/
- USDC EIP-712 Dart signing gist (domain values confirmed): https://gist.github.com/danielnordh/b546adcebc7f560e4ad899f399370551
- EIP-3009 Python reference (web3-ethereum-defi): https://web3-ethereum-defi.readthedocs.io/api/usdc/_autosummary_usdc/eth_defi.usdc.eip_3009.html
- x402 gasless transfer guide: https://blog.developerdao.com/x402-deep-dive-a-payment-standard-for-the-internet
