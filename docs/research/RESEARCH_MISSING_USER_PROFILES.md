# Research: Missing User Profiles for Robot Task Marketplace

**Date:** 2026-03-27
**Status:** Draft
**Method:** Gap analysis against existing 15 user types + comparable marketplace taxonomies (Upwork, Thumbtack, AWS Marketplace, Uber, Airbnb)
**Existing profiles:** Sarah (buyer), Diane (private buyer), Kenji (lunar buyer), Alex (operator), IT admin, CFO auditor, fleet operator, regulator, AI agents, and others documented in user journey docs.

---

## Summary

Of 8 candidate profiles investigated, **4 are clearly needed** (Anonymous Visitor, Developer/Integrator, Platform Administrator, Enterprise Procurement), **2 are likely needed later** (Data Consumer, Referral Partner), and **2 are premature** (Hardware Manufacturer, Insurance Provider). The first two -- Anonymous Visitor and Platform Admin -- are blocking: the demo already assumes them but no profile exists to guide their features.

---

## 1. Anonymous Web Visitor

**Needed: YES -- blocking for v1.5 frontend**

The FRONTEND_DESIGN_SPRINT.md already describes this user in detail (Sarah v2 lands on yakrobot.bid with zero credentials), but no standalone profile exists. Every major marketplace (Airbnb, Thumbtack, Upwork) treats the anonymous visitor as a distinct conversion stage with its own metrics and design constraints.

**Primary journey:** Land via search/link -> browse live feed + robot cards -> type intent into search bar -> see structured preview with cost estimate -> hit conversion wall (connect AI assistant) -> become Sarah.

**Why it matters:** The demo's landing screen (hero, cycling examples, live feed, robot grid) is entirely designed for this user. Without a profile, there is no definition of success metrics (bounce rate, intent capture rate, conversion to authenticated user) or guardrails on what to show pre-login.

**Backend features needed:**
- Anonymous intent capture endpoint (store raw query string, no auth required)
- Public robot listing API (read-only, no wallet addresses per PP-2)
- Public feed API (recent completed tasks, anonymized)
- Session tracking for conversion funnel analytics

**When:** v1.5 (ships with the frontend)

---

## 2. Developer / Integrator

**Needed: YES -- v2.0**

This is the user who builds on top of the marketplace rather than buying or operating. Comparable: Uber's developer platform team serves external partners who embed Uber into their own apps. Thumbtack launched a Pro API specifically for workflow platforms (GoSite was the first integration partner). AWS Marketplace has ISVs as a distinct role from buyers and sellers.

The marketplace already exposes MCP tools and plans a `.well-known/mcp.json` endpoint. The AI Agent user story in the design sprint describes agent-discoverable endpoints. But no profile captures the *human* developer who reads docs, gets API keys, builds integrations, and files bugs.

**Primary journey:** Find API docs (via `.well-known/mcp.json` or developer portal) -> get API key (self-service) -> build integration (MCP client, webhook consumer, or REST wrapper) -> test against sandbox -> go live.

**Backend features needed:**
- Developer portal / API documentation site
- Self-service API key provisioning (separate from buyer API keys)
- Sandbox environment with simulated robots
- Webhook registration for task lifecycle events
- Rate limiting and usage dashboard
- OpenAPI / MCP schema publishing

**When:** v2.0 (after core marketplace is stable; premature before that)

---

## 3. Enterprise Procurement

**Needed: YES -- v2.0**

Sarah buys single tasks. Enterprise procurement buys robot services at volume with contracts, SLAs, and invoicing. This is a different user with different needs. AWS Marketplace handles this with private offers, multi-level approval workflows, and consolidated billing. Upwork has Enterprise accounts with team management and compliance controls.

The current $25 credit bundle model does not work for a company that wants 500 sensor readings/month across 12 facilities with a net-30 invoice.

**Primary journey:** Evaluate marketplace via anonymous browsing or sales contact -> negotiate volume pricing and SLA terms -> sign contract (offline or platform-generated) -> onboard facilities and robot requirements -> receive consolidated monthly invoice -> audit via CFO dashboard (already partially covered by existing CFO profile).

**Backend features needed:**
- Organization accounts with role hierarchy (admin, buyer, finance)
- Volume pricing / committed-use discounts
- SLA definitions per contract (max response time, uptime guarantees)
- Invoice generation (net-30/net-60) alongside prepaid credits
- Approval workflows (budget holder -> manager -> procurement)
- Usage reporting and export (CSV/API)

**When:** v2.0 (requires stable single-buyer flow first; this is a growth-stage feature)

---

## 4. Robot Hardware Manufacturer

**Needed: MAYBE -- v3.0 or later**

The demo already has a "Buy a Robot" screen with YakRover Starter Kit ($299) and Pro ($799). But today this is a first-party offering, not a third-party manufacturer marketplace. The question is whether to open supply-side listings to external hardware vendors.

Airbnb does not sell furniture; Uber does not sell cars. The marketplace's job is to match task demand with robot supply, not to be a hardware retailer. However, growing the supply side faster may require partnerships with manufacturers who bundle marketplace registration with their hardware.

**Primary journey:** Apply as a hardware partner -> list starter kit with marketplace-compatible specs -> buyers purchase kit -> kit arrives pre-registered on-chain -> manufacturer earns revenue share.

**Backend features needed:**
- Partner application and approval workflow
- Hardware listing pages with compatibility verification
- Pre-registration flow (ERC-8004 identity provisioned at factory)
- Revenue share tracking and payouts

**When:** v3.0+ (only if supply-side growth becomes a bottleneck; premature now)

---

## 5. Data Consumer

**Needed: MAYBE -- v2.0 as a feature, not a separate profile initially**

A user who wants aggregated sensor data (temperature trends across 50 warehouses) rather than individual task results. This is a real market -- environmental monitoring, urban planning, agricultural surveys -- but it is a *product extension*, not a core marketplace role.

**Primary journey:** Browse available datasets or define a recurring data collection schedule -> subscribe to data feed -> receive structured datasets (JSON/CSV) -> pay per data point or subscription.

**Backend features needed:**
- Recurring task scheduling (post the same task daily/hourly)
- Data aggregation and export API
- Subscription billing (beyond one-off credits)
- Data licensing and usage terms

**When:** v2.0 can add recurring tasks as a feature for Sarah. A standalone "data marketplace" persona is v3.0+. Do not build a separate product for this yet.

---

## 6. Insurance / Risk Provider

**Needed: NO -- premature**

Robot task insurance (covering equipment damage, task failure, liability) is a real need at scale, but the marketplace must first have enough volume and failure data to underwrite risk. No comparable early-stage marketplace launched with an insurance provider role. Uber added insurance years after launch. Airbnb's Host Protection Insurance came after massive scale.

**Primary journey:** Would involve actuarial risk assessment, policy integration into task flow, claims processing.

**Backend features needed:** Would be extensive (claims API, risk scoring, policy management). Not worth designing now.

**When:** Future (v3.0+ at earliest, and only if task volume justifies it). For now, operator-controlled escrow release and platform dispute resolution cover the risk gap.

---

## 7. Platform Administrator

**Needed: YES -- blocking for v1.5**

Every marketplace needs an admin. The current codebase has no admin interface -- everything runs via CLI and direct database access. The roadmap mentions operator-controlled escrow release but does not define who the platform operator is as a user.

Comparable: every marketplace platform (Sharetribe, CS-Cart, Virto Commerce) ships with admin roles that manage sellers, fees, disputes, and platform health. This is table stakes.

**Primary journey:** Monitor platform health (active robots, task volume, error rates) -> review and resolve disputes -> manage payouts and fee schedules -> onboard/suspend operators -> configure auction parameters.

**Backend features needed:**
- Admin dashboard (task volume, revenue, robot health, error rates)
- Dispute resolution workflow (buyer reports issue -> admin reviews -> refund or release)
- Operator management (approve, suspend, configure fee splits)
- Payout management and reconciliation
- Auction parameter configuration (scoring weights, timeout values)
- Audit log viewer (all payment state changes already logged per CLAUDE.md rules)

**When:** v1.5 (basic health monitoring and dispute resolution) expanding through v2.0 (full admin suite). Without this, the platform cannot operate in production.

---

## 8. Referral / Channel Partner

**Needed: MAYBE -- v2.0**

AWS Marketplace has a formal Channel Partner program (CPPO) where partners create private offers, own the customer relationship, and earn margins. This only makes sense when the marketplace has enough product-market fit that distribution becomes the bottleneck.

For a robot task marketplace, channel partners could be: facility management companies that refer their clients, robotics consultancies that onboard operators, or system integrators who bundle marketplace access into their offerings.

**Primary journey:** Apply as partner -> receive referral tracking link/code -> bring buyers or operators -> earn commission on referred revenue -> view earnings dashboard.

**Backend features needed:**
- Partner registration and approval
- Referral tracking (attribution via links or codes)
- Commission calculation and payout
- Partner dashboard with referred user activity

**When:** v2.0 at earliest (only after proving the core marketplace works and growth becomes the priority). This is a growth lever, not a product feature.

---

## Priority Matrix

| Profile | Needed? | Version | Blocking? |
|---|---|---|---|
| Anonymous Web Visitor | YES | v1.5 | YES -- frontend ships without conversion model |
| Platform Administrator | YES | v1.5 | YES -- cannot operate in production without it |
| Developer / Integrator | YES | v2.0 | No -- but needed before opening the ecosystem |
| Enterprise Procurement | YES | v2.0 | No -- growth-stage feature |
| Data Consumer | MAYBE | v2.0 feature / v3.0 persona | No |
| Referral / Channel Partner | MAYBE | v2.0+ | No |
| Hardware Manufacturer | MAYBE | v3.0+ | No |
| Insurance / Risk Provider | NO | Future | No |

---

## Recommended Next Steps

1. **Write the Anonymous Web Visitor profile now.** The frontend demo is already built for this user. Define conversion metrics: intent capture rate, auth conversion rate, first-task completion rate.
2. **Write a minimal Platform Admin profile for v1.5.** Scope it to: health dashboard, dispute resolution, payout oversight. Full admin suite is v2.0.
3. **Defer the rest to v2.0 planning.** Developer/Integrator and Enterprise Procurement are real but not blocking. They should be profiled when v2.0 scoping begins.

---

## Comparable Marketplace References

- [Uber Developer Platform](https://developer.uber.com/) -- developer/integrator as a distinct role with dedicated APIs and partner engineering
- [Thumbtack Pro API](https://pro-api.thumbtack.com/docs/) -- opened API for workflow platform integrators (GoSite first partner)
- [AWS Marketplace Channel Partner Program](https://aws.amazon.com/marketplace/partners/channel-programs) -- ISV, Channel Partner, and Consulting Partner as formal roles with resale authorization
- [Sharetribe Marketplace Software](https://www.sharetribe.com/) -- admin role as table stakes in every marketplace platform
- [User Role Management Guide for Marketplaces](https://fleexy.dev/blog/user-role-management-guide-for-marketplaces-2024/) -- consumer, seller, admin, moderator as minimum role set
