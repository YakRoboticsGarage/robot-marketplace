# Award Confirmation: From Winning Bid to Confirmed Award

Research date: 2026-03-28. This document covers the gap between a winning bid and a confirmed contract award -- what checks happen, who makes the decision, and how the marketplace should model this step.

---

## How DOTs Handle Bid-to-Award

### The "Responsive and Responsible" Framework

Every state DOT follows the federal framework requiring award to the "lowest responsive and responsible bidder." These are two distinct checks:

- **Responsive bid** = the bid itself complies with solicitation requirements. Submitted on time, correct forms, no material deviations from specs, required bonds/certifications attached. This is binary -- pass or fail at bid opening.
- **Responsible bidder** = the company has the capacity to perform. Financial resources, equipment, experience, workforce, licensing, insurance, and a track record of completing similar work. This is a judgment call made after bid opening.

### What Gets Checked (Post-Bid Opening)

1. **Prequalification status** -- is the bidder prequalified for this work category and dollar amount?
2. **Licensing** -- valid contractor's license, PLS license (for survey), FAA Part 107 (for drones).
3. **Insurance** -- CGL, E&O, auto, workers comp, drone/aviation liability at required limits.
4. **Bonding capacity** -- can the bidder obtain a performance bond and payment bond for this contract value?
5. **Past performance** -- completion history, change order rates, safety record, prior defaults.
6. **Debarment** -- checked against SAM.gov (federal) and state-specific debarment lists. SAM.gov Entity Management API provides programmatic access with 1,000 queries/day rate limit.
7. **DBE compliance** -- did the bidder meet the DBE goal or demonstrate good faith efforts?

### Typical Review Timelines

- **FHWA guidance**: Award should occur "within a reasonable time" after bid opening. FHWA interprets "shortly after award" as no more than 90 calendar days for certain post-award actions.
- **TxDOT**: Conducts statewide lettings monthly on two consecutive days. Award decisions typically follow within 30-45 days. TxDOT may reject any bid where the bidder is not "physically organized and equipped with the financial wherewithal to undertake and complete the contract."
- **MDOT**: Contract Awards Unit processes awards after the Contract Services staff meet with the State Design Engineer. Senior managers review bid information and draft final recommendation. Typical timeline: 14-30 days from bid opening to award on straightforward projects; longer if DBE compliance review is needed.
- **MoDOT**: Published process shows bid opening, followed by staff review, engineer recommendation, then commission approval on larger projects.

### Grounds for Rejecting the Low Bidder

- Bidder not prequalified for the work category or dollar amount
- Financial capacity insufficient (liabilities exceed assets, inadequate bonding)
- Mathematically or materially unbalanced bid (front-loading early items)
- Failed to meet DBE goal and did not demonstrate good faith efforts
- Active debarment or suspension (federal or state)
- Incomplete or non-conforming bid package (missing forms, unsigned documents)
- Poor past performance (defaults, excessive claims, safety violations)
- License expired or not valid in the project state

---

## DBE/MBE Requirements

### What Is the DBE Program?

The Disadvantaged Business Enterprise program is a federally mandated program under 49 CFR Part 26 that applies to all federal-aid highway, transit, and airport projects. Congress has maintained a cumulative national aspirational goal of at least 10% DBE participation. Only firms that are small, independently owned, and controlled by socially and economically disadvantaged individuals qualify.

### How DBE Goals Work on a Project

1. The state DOT sets an **overall triennial goal** based on relative availability of DBEs in their market.
2. For each federally funded project, the DOT sets a **contract-specific DBE goal** (e.g., 8% of the contract value).
3. The prime contractor must either **meet the goal** by committing sufficient DBE subcontractor/supplier participation, or **demonstrate good faith efforts** (documented outreach, solicitation of DBE quotes, explanation of why goal could not be met).
4. Good faith efforts are evaluated at bid time. A bidder who neither meets the goal nor demonstrates good faith efforts is deemed non-responsive.

### MDOT DBE Specifics

- MDOT maintains a [certified DBE directory](https://www.michigan.gov/mdot/programs/dbe) listing firms by work category, location, and certification status.
- MDOT publishes DBE letting reports for each monthly bid letting showing project-level DBE goals.
- **Subcontractor substitution**: To replace a DBE subcontractor, the prime must submit MDOT Form 0196 (Request to Replace DBE). The DBE being replaced gets 5 business days written notice. The construction engineer reviews and approves in consultation with MDOT's Office of Business Development (OBD). A good faith effort to find a replacement DBE is required. The substitute DBE must be approved by MDOT before starting work.
- DBE payment tracking uses MERS (Form 2124A) to verify actual payments to DBE firms.

### Can a GC Reject a Lower-Priced Sub to Meet DBE Goals?

Yes. On federal-aid projects, the GC is expected to consider DBE firms for subcontracting opportunities and may select a DBE subcontractor over a lower-priced non-DBE firm to meet the contract DBE goal. This is not bid-rigging -- it is compliance with a federal program requirement. The GC documents the decision as part of their good faith efforts.

---

## Automated vs. Human Checks

### Automatable (API or Database Lookup)

| Check | Source | Automation Method |
|-------|--------|-------------------|
| Federal debarment | SAM.gov | Entity Management API (free, 1K/day) |
| State contractor license | State licensing board | Varies; some have APIs, most require scraping |
| PLS license validity | State board of licensure | Database lookup (no standard API) |
| FAA Part 107 certificate | FAA Airmen Inquiry | Public lookup tool |
| Insurance limits vs. minimums | ACORD 25 COI | OCR/parsing of uploaded certificate |
| COI expiration date | ACORD 25 COI | Date field extraction |
| Bonding capacity (binary) | Surety letter | Document upload + verification |
| MDOT prequalification status | MDOT contractor directory | Public web lookup |
| DBE certification status | MDOT DBE directory | Public web lookup |

### Requires Human Judgment

| Check | Why It Cannot Be Automated |
|-------|---------------------------|
| Prior relationship / bad experience | Subjective; not in any database |
| Conflict of interest | Operator works for a competitor; context-dependent |
| DBE strategy | GC decides how to allocate subcontracting to meet goals |
| Client prohibited vendor list | MDOT or owner may have informal exclusions |
| Project-specific risk assessment | Site complexity, schedule criticality, remote location |
| Insurance adequacy beyond limits | Policy exclusions, retroactive dates, tail coverage |
| Good faith effort evaluation | Judgment call on whether DBE outreach was genuine |
| Price reasonableness | Is the bid too low to be credible? |

### The 80/20 Split

Roughly 60-70% of the "responsive and responsible" determination can be automated through database lookups and document verification. The remaining 30-40% requires a human reviewer who knows the project context, the client's requirements, and the local market.

---

## Marketplace Platform Patterns

### Upwork: Proposal Review + Hire

1. Client posts job. Freelancers submit proposals.
2. Client reviews proposals on a dashboard with actions: **Message**, **Hire**, **Decline**, **Archive**.
3. Client can shortlist candidates and conduct interviews before hiring.
4. **"Hire" button** sets contract terms (rate, milestones) and sends an offer.
5. Freelancer accepts. Escrow funds milestone. Work begins.
6. Key insight: the client always makes the final hire decision. The platform recommends but never auto-awards.

### Thumbtack: Select This Pro

1. Customer posts request. Pros respond with quotes.
2. Customer reviews profiles, ratings, price, and availability.
3. Customer selects a pro and contacts them directly.
4. Payment happens off-platform (Thumbtack earns from lead fees, not transaction fees).
5. Key insight: even simpler flow, but still a deliberate human selection step.

### AWS Marketplace: Private Offer Acceptance

1. Seller creates a private offer with negotiated pricing and custom EULA terms.
2. Buyer receives offer in their AWS Marketplace console under "Private offers."
3. Buyer reviews terms, pricing, payment schedule.
4. Buyer with proper IAM permissions clicks **Accept**.
5. AWS charges the account. Subscription becomes active.
6. Key insight: governance layer -- only users with `AWSMarketplaceManageSubscriptions` permission can accept. Mirrors the "authorized procurement officer" concept in construction.

### BuildingConnected (Autodesk): Bid Leveling + Award

1. GC creates bid package with scope, plans, specs, bid forms.
2. Subs are invited or discover the project; submit bids electronically.
3. GC uses **bid leveling** tools to compare proposals by trade, price, scope coverage.
4. GC reviews sub qualifications, insurance, bonding, references within the platform.
5. GC selects winning sub and issues a **notice of award** or subcontract through the platform.
6. Key insight: closest analog to our marketplace. The platform facilitates comparison and review but the GC makes the award decision with full context.

### PlanHub: Bid Board + Award Tracking

1. GC posts project. Subs discover via search or invitation.
2. Subs submit bids through the Bid Board.
3. GC uses bid leveling to compare side-by-side.
4. Subs receive **bid status updates** (viewed, under review, awarded).
5. Key insight: transparency in bid status is a feature subs value highly.

---

## Recommended Flow for Robot Marketplace

Based on DOT practice and marketplace patterns, the flow should be:

### Step 1: Auction Closes -- Recommended Winner Presented
- Bids scored by the engine (price, schedule, equipment match, operator rating).
- System presents **"Recommended Winner"** with a ranked list of all bidders.
- Automated checks run immediately: debarment (SAM.gov), license validity, insurance limits, MDOT prequalification status, DBE certification.
- Each check shows green/yellow/red status on the review screen.

### Step 2: GC Reviews and Confirms (Human Decision)
- GC sees a **review dashboard** with: bid price, operator profile, automated check results, equipment details, past project history, and any flags.
- GC can: **Confirm Award**, **Reject and Select Next Bidder**, or **Request More Information**.
- If the project has a DBE goal, the dashboard shows DBE participation percentage for each bidder's proposed team.
- The GC can override the recommended winner for documented reasons (conflict of interest, prior experience, DBE strategy, client requirement).

### Step 3: Award Confirmed -- Agreement Generated
- On confirmation, the subcontract auto-generates from template + task spec + winning bid.
- Insurance verification finalizes (COI uploaded to vault).
- Both parties sign digitally.
- Escrow or bond verification triggers.
- Work authorization issued.

### State Transitions
```
AUCTION_CLOSED -> RECOMMENDED_WINNER -> AWARD_CONFIRMED -> AGREEMENT_SIGNED -> WORK_AUTHORIZED
                                     -> WINNER_REJECTED -> NEXT_BIDDER_REVIEWED -> ...
```

### Timeout Behavior
- If the GC does not act within 72 hours of auction close, the system sends a reminder.
- After 7 days of inaction, the auction expires and all bidders are released.
- This mirrors DOT practice where bids have a validity period (typically 60-90 days, but marketplace moves faster).

---

## Implications for Demo

The demo currently jumps from "winner selected" to "awarded." It needs an intermediate screen:

1. **Award Review Screen** showing the recommended winner with automated check badges (license: green, insurance: green, debarment: clear, prequalification: valid). Include a mock "DBE participation: 9.2% (goal: 8%)" line for the MDOT scenario.

2. **Confirm Award Button** that the GC clicks after reviewing. This is the "hire" moment -- equivalent to Upwork's hire button or BuildingConnected's award action.

3. **Rejection Path** where the GC can select "Reject -- choose reason" (conflict of interest, insufficient insurance, DBE non-compliance, prior experience, other) and the system surfaces the next-ranked bidder for review.

4. For the MDOT demo scenario specifically: show the DBE compliance check, the MDOT prequalification badge, and the 10-day prompt payment term auto-populated in the agreement.

The key message: the marketplace adds value by automating the 60-70% of checks that are database lookups, while preserving the human judgment that construction procurement requires. This is what separates it from a simple reverse auction.

---

Sources:
- [FHWA: Bid Analysis and Award of Contract](https://www.fhwa.dot.gov/construction/cqit/award.cfm)
- [FHWA: Companion Resource for Project Advertisement, Bid Review](https://www.fhwa.dot.gov/federal-aidessentials/companionresources/05projadbidcon.pdf)
- [FHWA: DBE Program](https://highways.dot.gov/civil-rights/programs/disadvantaged-business-enterprise-dbe-program)
- [FHWA: DBE Contract Goals](https://highways.dot.gov/fed-aid-essentials/videos/civil-rights/disadvantaged-business-enterprise-dbe-contract-goals)
- [MDOT: Construction Prequalification](https://www.michigan.gov/mdot/business/contractors/prequalification)
- [MDOT: Awards & Payments](https://www.michigan.gov/mdot/business/contractors/awards-payments)
- [MDOT: DBE Program](https://www.michigan.gov/mdot/programs/dbe)
- [MDOT: 102.17 Subletting to DBEs](https://mdotwiki.state.mi.us/construction/index.php/102.17_Subletting_Contract_Work_to_Disadvantaged_Business_Enterprises_(DBEs))
- [MDOT: Prequalification of Bidders](https://mdotwiki2.state.mi.us/construction/index.php?title=102.01_Prequalification_of_Bidders)
- [TxDOT: Bid Analysis](https://www.txdot.gov/manuals/tpd/lgp/letting_and_award/letting-i1003258/bid_analysis-i1003986.html)
- [TxDOT: Contract Award](https://www.txdot.gov/government/processes-procedures/lgp-toolkit/letting-award/award.html)
- [SAM.gov Entity Management API](https://open.gsa.gov/api/entity-api/)
- [Upwork: Review Proposals](https://support.upwork.com/hc/en-us/articles/211063268-Review-proposals)
- [AWS: Private Offers in AWS Marketplace](https://docs.aws.amazon.com/marketplace/latest/buyerguide/buyer-private-offers.html)
- [BuildingConnected vs PlanHub](https://planhub.com/resources/buildingconnected-vs-planhub/)
- [US DOT: DBE Program](https://www.transportation.gov/civil-rights/disadvantaged-business-enterprise)
- [MRSC: Responsive & Responsible Bids](https://mrsc.org/stay-informed/mrsc-insight/july-2022/saying-yes-to-responsive-responsible-bids)
