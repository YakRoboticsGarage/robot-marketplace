# Information Architecture Critique — demo/index.html

Reviewer: Information Architect | Date: 2026-03-27

---

## 1. Robot Cards: Missing Buyer-Critical Information

Cards show: name, location, capabilities (tags), price, star rating, online status.

**Missing:**
- **Sensor specs** — accuracy, range, calibration date. Buyers cannot evaluate fitness.
- **Uptime / reliability** — no SLA indicator, no "99.2% uptime" or similar.
- **Task history** — "142 ratings" is not "142 completed tasks." Show completed task count.
- **Response time** — no average time-to-result. Critical for time-sensitive buyers.
- **Certifications** — no ISO, ATEX, IP rating. Enterprise buyers filter on this.
- **Supported data formats** — JSON appears only after Claude structures the task. Show it on the card.

**Fix:** Add a compact spec row below capabilities: `42s avg | 99.2% uptime | JSON/CSV | IP67`. Keep the card scannable — link to a detail panel for full specs.

## 2. Agent Compatibility: Buried and Unclear

MCP is mentioned in exactly three places: a `<link>` tag, the footer, and the post-result "Add to Claude" modal. None of these are visible to a first-time visitor scanning the page.

**Problems:**
- The hero says nothing about AI agent or API access.
- "Connect Claude" appears mid-flow (screen 2) with no prior context. A visitor who doesn't use Claude will not understand this is a protocol-level integration.
- The `/.well-known/mcp.json` link is invisible to humans.

**Fix:**
- Add a single line below the hero subtitle: "Works with AI agents via MCP. Connect Claude, GPT, or your own tools."
- On robot cards, add an "MCP" badge alongside capability tags.
- Replace "Connect Claude" with "Connect your AI assistant" — Claude is one option, not the only one.

## 3. Landing Page Hierarchy: Wrong Order for Enterprise

Current order: Hero > Search > How it Works > Live Feed > Available Robots.

**Problems:**
- Live Feed is social proof but placed before robots. An enterprise buyer wants to evaluate the fleet first, then see activity as validation.
- No trust section exists anywhere — no "who uses this," no security mention, no compliance.
- The "For Operators" page is supply-side. Demand-side buyers have no equivalent "For Enterprise" or "For Teams" anchor.

**Fix:** Reorder to: Hero > Search > Available Robots > How it Works > Live Feed > Trust bar (logos/compliance). Add a one-line trust strip: "SOC 2 in progress | Data encrypted in transit and at rest | You own your data."

## 4. "How It Works" Section: Insufficient

Three steps: Describe > Robots Compete > Get Result. This answers "what happens" but not:

- **What does it cost?** Pricing model is unclear until screen 2.
- **How fast?** "Under a minute" is vague. Show real P50/P95.
- **What if it fails?** No mention of retries, refunds, or guarantees.
- **Who controls the robot?** Buyers may worry about safety/liability.
- **Can I automate this?** No mention of API/programmatic access in the flow.

**Fix:** Add a fourth step: "Verify and automate — inspect results, set up recurring tasks, or connect via API." Add a small-print line under the section: "All tasks are insured. If a robot fails, you're refunded automatically."

## 5. Trust Signals: Almost Entirely Absent

**Missing:**
- **Security posture** — no mention of encryption, auth model, or data handling.
- **Data ownership** — who owns the sensor readings? Not stated anywhere.
- **Compliance** — no SOC 2, GDPR, or industry-specific mentions.
- **Refund/guarantee policy** — payment screen shows $25 bundle with zero protection language.
- **Company identity** — "YAK Robotics Garage" in schema.org but no about page, no team, no address.
- **Audit trail** — the system has one (per CLAUDE.md) but the UI never communicates this to buyers.

**Fix:** Add a minimal trust footer above the site footer: "Your data, your ownership | End-to-end encrypted | Full audit trail | Refund guarantee." Link each to a detail page (even if placeholder). On the payment screen, add: "Cancel anytime. Unused credits are refundable."

---

## Priority Order

1. **Trust signals** — without these, enterprise visitors bounce immediately.
2. **Robot card specs** — buyers cannot make a decision without them.
3. **Agent/MCP visibility** — this is the differentiator; don't hide it.
4. **How it Works expansion** — answer the next three questions a buyer will ask.
5. **Page hierarchy reorder** — robots before feed, trust bar before footer.
