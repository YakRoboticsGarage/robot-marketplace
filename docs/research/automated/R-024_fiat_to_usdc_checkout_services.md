# R-024: Fiat-to-USDC Checkout Services
**Date:** 2026-04-03
**Topic ID:** R-024
**Module:** M37_splits_distribution / M15_stripe_service / M18_x402
**Status:** Complete
**Researcher:** Automated daily research agent

---

## Executive Summary

- **Stripe is the strongest near-term fit.** Stripe Connect stablecoin payouts (USDC on Base) are live for US platforms paying individual/sole-proprietor operators. Buyers pay by card (fiat), Stripe converts and pays out USDC. This is the cleanest integration with our existing Stripe Connect Express architecture — no new rails required.
- **Coinbase Onramp offers zero-fee USDC on Base** with card/Apple Pay/Google Pay, but it sends USDC to the *buyer's* wallet, not the operator's. It solves the buyer funding problem, not the operator payout problem. Requires application for zero-fee access.
- **PayRam (launched March 2026) is purpose-built for this exact use case:** card-in, USDC-out to a merchant wallet, non-custodial, self-hosted, Base-native. Directly addresses our payment split architecture. Needs evaluation.
- **x402 is crypto-native only** — no card-to-USDC bridge in the current protocol. Future versions may add card rails. Not the right tool for fiat buyers today.
- **Regulatory risk is real but manageable via provider delegation.** If YAK routes payments through Stripe, Coinbase Onramp, or PayRam rather than handling fiat-to-crypto conversion itself, it does not become an MSB/MTT. DIY conversion would require FinCEN registration and 50-state MTLs.

---

## Findings

### 1. Stripe — Card-to-USDC via Connect Stablecoin Payouts

**Source:** https://docs.stripe.com/connect/stablecoin-payouts  
**Source:** https://support.stripe.com/express/questions/stablecoin-payouts

**How it works:**
- Buyer pays via card → Stripe PaymentIntent (fiat USD, as today)
- Platform's Stripe Connect Express account balance stays in fiat
- Operator links a crypto wallet to their Express Dashboard
- Operator sets default payout currency to USDC
- On payout trigger, Stripe converts and sends USDC to the linked wallet
- Works on Base and Polygon

**Current limitations (as of 2026-04):**
- US-based Connect platforms only (YAK is US — this applies)
- Payouts to **individuals and sole proprietors** only — not companies or non-profits
- This matters: robot operator LLCs would be blocked; sole proprietors are fine
- Express Dashboard required (we already use Express)
- No published list of recipient countries, but Remote uses this for 69+ countries

**Fee structure:** Stripe's standard 1.5% flat fee for stablecoin transactions (same as fiat acceptance). No extra conversion fee disclosed.

**Integration path:** Add `currency: "usdc"` to Connect payout calls. Operator enables wallet in Express Dashboard. No new payment provider needed.

**Rating for YAK:** High fit. This extends existing Stripe integration with no new vendor, no new KYC flow, and no new settlement layer. The sole-proprietor constraint limits operator types but covers most drone operators in the short term.

---

### 2. Coinbase Onramp — Zero-Fee Card-to-USDC for Buyer Wallet Funding

**Source:** https://docs.cdp.coinbase.com/onramp-&-offramp/introduction/welcome  
**Source:** https://www.coinbase.com/developer-platform/discover/launches/zero-fee-usdc

**How it works:**
- Embedded widget or headless API in buyer's checkout flow
- Buyer pays by card, bank transfer, Apple Pay, Google Pay, PayPal, SEPA
- USDC is sent directly to the buyer's specified wallet address
- Zero fee on USDC transactions on Base (requires application for access)
- Guest checkout available (no Coinbase account needed in US)
- Sandbox environment available for testing

**What it does NOT do:**
- It does not send USDC directly to a third-party (operator) wallet at checkout
- The flow is: buyer pays → buyer's wallet receives USDC → buyer then pays operator from their wallet
- This is a buyer funding tool, not a buyer-pays-operator checkout tool

**Use case for YAK:** 
- Relevant if we want buyers to pre-fund a USDC wallet (like a credit bundle) via card
- Does not replace the operator payout flow — a second step (x402 or direct transfer) is still needed
- Zero-fee USDC on Base is compelling for prepaid credit bundles

**KYC:** Coinbase handles KYC for the buyer. YAK does not take on KYC liability.

**Rating for YAK:** Medium fit as a buyer funding tool. Not a single-checkout solution.

---

### 3. PayRam — Card-In, Merchant-Receives-USDC (Launched March 2026)

**Source:** https://www.accessnewswire.com/newsroom/en/blockchain-and-cryptocurrency/payrams-card-to-crypto-onramp-goes-live-globally-customers-pay-by-car-1150600  
**Source:** https://payram.com/blog/state-of-stablecoins-2026

**How it works:**
- Customer (buyer) pays by card, Apple Pay, Google Pay, bank transfer, or 175+ local methods
- Merchant (platform/operator) receives USDC on Base directly in their own wallet — non-custodial
- No third party holds or moves funds
- Base-native, low fees, fast finality
- Self-hosted deployment (under 10 minutes), single button to enable card onramp
- Global: 190+ countries, 175+ payment methods

**What makes it different:**
- Unlike Coinbase Onramp (buyer's wallet), PayRam directs settlement to the *merchant's* wallet
- This is the "card-in / USDC-to-operator-wallet" architecture described in the R-024 hypothesis
- Non-custodial: USDC goes directly to specified wallet addresses at settlement

**Critical unknowns:**
- PayRam is very new (launched March 30, 2026) — production reliability unproven
- Fee structure not publicly disclosed in detail
- Regulatory status unclear — who holds the MSB license? PayRam? Underlying processor?
- Does it support routing to a Splits contract address (for platform fee split)?
- B2B pricing and API documentation quality needs direct evaluation

**Rating for YAK:** Potentially the highest architectural fit — solves "buyer pays card → operator gets USDC" in one step. Needs direct due diligence given newness.

---

### 4. MoonPay — Full-Featured Onramp with Enterprise Stablecoin Services

**Source:** https://www.moonpay.com/business/ramps  
**Source:** https://www.crossmint.com/learn/moonpay-vs-transak

**How it works:**
- Widget or API: buyer pays by card → USDC sent to specified wallet
- 160+ countries, supports Base
- Acquired Iron (March 2025) and launched enterprise stablecoin services (November 2025)
- February 2026: launched MoonPay Agents — AI agents can autonomously create wallets and transact

**Fee structure:** ~1% for bank transfers; ~4.5% for credit/debit card. Higher than Stripe's 1.5%.

**Rating for YAK:** Viable but more expensive than Stripe. Better for consumer-facing flows with high international coverage. The MoonPay Agents product is interesting for agent-to-agent payment scenarios but not the current v1.1 use case.

---

### 5. Transak — Developer-Friendly Onramp, 170+ Cryptos

**Source:** https://transak.com/  
**Source:** https://docs.transak.com/integration/api

**How it works:**
- Widget + white-label API, 64 countries, 136+ cryptos including USDC
- Partner fee (0.99%–3.5%) configurable; fixed minimum fee for small transactions
- Buyer KYC handled by Transak
- USDC sent to specified wallet address on checkout

**Rating for YAK:** Viable alternative to MoonPay. Fee structure more favorable for larger transactions (1–2% range). Less enterprise footprint than MoonPay but stronger developer docs. At construction survey scales ($1K–$200K), the percentage fee is the primary cost driver.

---

### 6. Ramp Network — 40 Currencies, 110 Cryptos, All 50 US States

**Source:** https://slashdot.org/software/comparison/MoonPay-vs-Ramp-Network-vs-Transak/

**How it works:**
- Widget/API; expanded to all 50 US states
- ~1.5% fee for bank; ~3.5% for card
- Supports USDC, multiple chains

**Rating for YAK:** Similar to Transak. Worth including in a comparison table but not a differentiated choice for construction survey use case.

---

### 7. x402 Protocol — Crypto-Native, No Fiat Bridge Today

**Source:** https://docs.cdp.coinbase.com/x402/welcome  
**Source:** https://www.x402.org/x402-whitepaper.pdf

**How it works:**
- HTTP 402 Payment Required → USDC payment via ERC-20/EIP-3009
- CDP facilitator handles verification; free tier 1,000 tx/month
- Designed for agent-to-agent and API monetization
- 10.5M+ cumulative transactions (AIsa network); 35M+ on Solana since summer

**Current fiat relevance:** None. x402 requires the payer to already hold USDC. The whitepaper notes "future versions could accommodate credit cards and bank accounts" but this is not implemented.

**YAK already uses x402 in mcp-demo-2.** This research confirms x402 is appropriate for the operator/agent payment layer but not for buyers who want to pay by card.

---

### 8. Splits (0xSplits) — USDC Payment Splitter on Base

**Source:** https://splits.org/  
**Source:** https://docs.splits.org/core/split

**How it works:**
- Non-upgradable, gas-efficient onchain splits
- Supports USDC, USDT, DAI, WBTC as ERC-20
- Deployed on Base, Ethereum, Optimism, Polygon, Zora
- SplitsKit for developer integration

**Compatibility:** PayRam card onramp explicitly routes to "merchant's own wallet" — needs verification that this can be a Splits contract address. Coinbase Onramp supports any wallet address. Stripe stablecoin payouts route to the linked wallet on the Express account, not an arbitrary contract.

**Rating:** Splits works well as the final distribution layer (platform fee + operator split) once USDC is on-chain, regardless of how it arrived. The fiat-to-Splits-contract-in-one-step is possible with PayRam and Coinbase Onramp but not with Stripe (Stripe routes to the operator's linked wallet).

---

### 9. MSB / Money Transmitter Regulatory Risk

**Source:** https://gofaizen-sherle.com/crypto-license/united-states  
**Source:** https://hodder.law/fincen-crypto-guidance/

**Key finding:** If YAK uses a licensed provider (Stripe, Coinbase, MoonPay, Transak) as the conversion layer, YAK does NOT become an MSB. If YAK were to accept fiat and convert it to USDC itself, it would need FinCEN MSB registration + Money Transmitter Licenses in ~40+ states — a multi-year, multi-million-dollar compliance project.

**Rule:** Always route through a licensed provider. Never touch the fiat-to-crypto conversion directly.

---

### 10. B2B Stablecoin Adoption Context

**Source:** https://thedefiant.io/news/infrastructure/b2b-stablecoin-payments-grew-over-730-percent-yoy-in-2025

B2B stablecoin payments grew 730%+ YoY in 2025, with B2B accounting for ~60% of the estimated $390B annual stablecoin payment volume. The GENIUS Act (signed July 18, 2025) created the first federal framework for payment stablecoins, exempting compliant stablecoins from securities classification.

**Implication for YAK:** The regulatory and adoption environment is moving in our favor. Drone operators in the construction market are more likely to accept USDC payouts in 2026 than would have been plausible in 2024.

---

## Comparison Table

| Provider | Buyer pays | Operator receives | Fee (card) | YAK fit | Status |
|---|---|---|---|---|---|
| **Stripe Connect (USDC payouts)** | Card (fiat) | USDC on Base | ~1.5% | High | Live, US platforms |
| **Coinbase Onramp** | Card/Apple Pay | USDC to buyer wallet | 0% USDC on Base | Medium (buyer funding) | Live, application required |
| **PayRam** | Card / 175+ methods | USDC to merchant wallet | TBD | High (architecture) | Live since 2026-03-30 |
| **MoonPay** | Card | USDC to wallet | ~4.5% card | Medium | Live |
| **Transak** | Card | USDC to wallet | 0.99–3.5% | Medium | Live |
| **Ramp Network** | Card | USDC to wallet | ~3.5% card | Low–Medium | Live |
| **x402** | USDC only | USDC | ~0% | Low (no fiat) | Live (agent layer) |

---

## Implications for the Product

### Short-term (v1.5): Extend Stripe Connect with USDC Payouts
The lowest-friction path is extending the existing Stripe integration. Buyer UX unchanged (card payment). Operator enables wallet in Express Dashboard. Payout in USDC on Base. This is production-ready today and requires no new vendor, no new KYC, and no new architecture.

**Constraint:** Sole proprietors only — not LLCs. Most drone operators operate as sole proprietors for initial platform onboarding; LLC operators are a v2 consideration.

### Medium-term (v1.5–v2): Evaluate PayRam for Direct Card → Splits Flow
PayRam's architecture (card-in, USDC to merchant wallet, non-custodial) is the closest match to the original R-024 hypothesis — buyer pays card, USDC goes directly to a Splits contract or operator wallet. Needs evaluation: fee structure, API quality, production reliability (very new), and whether contract addresses (Splits) are supported as destinations.

### Buyer Funding (v1.5): Coinbase Onramp for Credit Bundles
For buyers who want to pre-fund a USDC balance (credit bundle pattern at $5,000), Coinbase Onramp with zero-fee USDC on Base is the right tool. Guest checkout means no Coinbase account required. After funding their wallet, the buyer can use x402 or direct transfer to pay per task.

### Do Not Build: x402 is not the fiat bridge
x402 handles agent-to-agent USDC payments (already deployed in mcp-demo-2) but does not bridge card payments to USDC. Keep using x402 for the operator payment layer; use Stripe/PayRam/Coinbase for the buyer fiat-entry layer.

### Regulatory: Always delegate conversion to a licensed provider
YAK must never convert fiat to crypto directly. All fiat-to-USDC conversion must go through Stripe, Coinbase, or another licensed MSB provider. This is non-negotiable per the existing payment code rules.

---

## Improvement Proposals

### IMP-012: Enable Stripe Connect USDC payouts for sole-proprietor operators
Extend the existing `StripeService` to support USDC payout currency selection. Add an operator onboarding step in the Express Dashboard flow to link a crypto wallet and select USDC as default payout currency. Guard with `entity_type == "individual"` check; return a clear error for LLC operators with a note that fiat payout remains available.

### IMP-013: Integrate Coinbase Onramp for USDC credit bundle purchases
Add a "Buy credits with card" flow using Coinbase Onramp. Buyer completes onramp via widget (0% fee on USDC/Base, guest checkout), USDC goes to their wallet, then they top up their platform credit balance via x402 transfer. This enables card-funded USDC accounts without YAK touching fiat-to-crypto conversion.

### IMP-014: Evaluate and pilot PayRam for direct card → Splits settlement
Conduct a technical pilot of PayRam's card-onramp API: (1) verify USDC routing to a Splits contract address, (2) test fee structure at $1K–$10K transaction sizes, (3) assess production reliability, (4) compare total cost vs. Stripe stablecoin payout path. Decision gate: if PayRam supports Splits contract destinations and fees are under 2%, prioritize for v2 payment architecture.

---

## New Questions Spawned

- **R-025** (already queued): Stripe crypto payouts to Connect accounts — this research has substantially answered R-025. Consider marking R-025 complete with reference to this document.
- **R-027**: PayRam production reliability audit — the service is 4 days old as of this research. A follow-up in 30–60 days to assess uptime, fee structure confirmation, and API documentation quality.
- **R-028**: Operator entity-type distribution — what fraction of potential drone operators are sole proprietors vs. LLCs? Determines whether the Stripe USDC payout constraint is a material blocker.

---

## Sources

- [Coinbase Onramp Documentation](https://docs.cdp.coinbase.com/onramp-&-offramp/introduction/welcome)
- [Coinbase Zero-Fee USDC Launch](https://www.coinbase.com/developer-platform/discover/launches/zero-fee-usdc)
- [Stripe Stablecoin Payouts for Connect](https://docs.stripe.com/connect/stablecoin-payouts)
- [Stripe Stablecoin Payments Documentation](https://docs.stripe.com/payments/stablecoin-payments)
- [Stripe Stablecoin Financial Accounts (101 countries)](https://stripe.com/blog/introducing-stablecoin-financial-accounts)
- [PayRam Card-to-Crypto Launch (2026-03-30)](https://www.accessnewswire.com/newsroom/en/blockchain-and-cryptocurrency/payrams-card-to-crypto-onramp-goes-live-globally-customers-pay-by-car-1150600)
- [PayRam Stablecoin 2026 Guide](https://payram.com/blog/state-of-stablecoins-2026)
- [MoonPay Business Ramps](https://www.moonpay.com/business/ramps)
- [Transak Developer Integration](https://transak.com/)
- [x402 Protocol Documentation](https://docs.cdp.coinbase.com/x402/welcome)
- [x402 Whitepaper](https://www.x402.org/x402-whitepaper.pdf)
- [Splits.org Documentation](https://docs.splits.org/core/split)
- [B2B Stablecoin Payments +730% YoY 2025](https://thedefiant.io/news/infrastructure/b2b-stablecoin-payments-grew-over-730-percent-yoy-in-2025)
- [MSB/MTL Regulatory Requirements 2026](https://gofaizen-sherle.com/crypto-license/united-states)
- [FinCEN Crypto MSB Guidance](https://hodder.law/fincen-crypto-guidance/)
- [MoonPay vs Transak comparison](https://www.crossmint.com/learn/moonpay-vs-transak)
- [Stripe Global USDC Payments launch](https://stablecoininsider.org/stripe-global-usdc-stablecoin-payments/)
