# Construction Payment Flows: JSON to Valid Auction

Research date: 2026-03-28

## How Construction Survey Payments Work Today

**Contract formation.** A GC issues a purchase order (PO) or subcontract agreement to the survey firm. For $50K-$500K survey contracts, this is almost always a written subcontract -- not a handshake. The subcontract specifies scope, schedule, payment terms, retainage, insurance requirements, and bonding (if any).

**Payment terms.** The industry standard for subcontractors is Net-30, though Net-60 and Net-90 exist on larger or public projects. "Pay-when-paid" clauses are common: the GC pays the sub within 7-10 days of receiving payment from the owner. In practice, survey subs often wait 45-90 days from invoice submission to actual payment. Michigan does NOT have a private prompt payment statute, so private project payment timing is purely contractual.

**Progress billing.** For survey contracts over ~$25K, progress billing is standard. The sub submits a monthly pay application (AIA G702/G703 format or equivalent) showing percentage of work complete. The GC reviews, approves (often with markup/reduction), and includes the sub's billing in the GC's own pay app to the owner.

**Retainage.** Standard retainage is 5-10% of each progress payment, held until substantial completion or project closeout. On a $72K survey contract at 10% retainage, the sub would have $7,200 withheld until the end -- potentially months after their fieldwork is done. Michigan allows retainage reduction to 0% after 50% completion on public projects.

**How a GC proves ability to pay.** On private projects: the GC's subcontract is the promise. No proof-of-funds requirement exists unless the sub demands it. On public projects: the GC's payment bond (required by law) IS the proof -- the surety company has underwritten the GC's financial capacity. Smart survey firms check the GC's payment bond before starting work.

## Legal Framework

### Miller Act (Federal Projects)
- Applies to federal construction contracts exceeding $150,000 (FAR Part 28 threshold; statute says $100K)
- Prime contractor must furnish both a **performance bond** and a **payment bond**, each equal to the contract price
- Payment bond protects first-tier and second-tier subs and suppliers
- First-tier subs (direct to prime) can sue on the bond without prior notice
- Second-tier subs must notify the prime in writing within 90 days of last furnishing
- All claimants must file suit within 1 year of final furnishing
- Source: [40 U.S.C. sections 3131-3134](https://www.americanbar.org/groups/construction_industry/publications/under_construction/2022/winter2022/miller-act-payment-bond-claims/)

### Michigan's Little Miller Act (Public Projects)
- Applies to state/local public projects with contract price **$50,000 or more**
- Prime must post a payment bond
- Protects subs and suppliers through the second tier
- Subcontractors must serve written notice within **60 days** of last furnishing
- Construction liens **cannot** be filed against public property -- the bond is the substitute
- Source: [MCL 129.201 et seq.](https://www.levelset.com/bond-claim/michigan-bond-claim-faqs/)

### Michigan Prompt Payment (Public Projects Only)
- GC must pay subs within **10 calendar days** of receiving payment from the public owner
- Penalty: **1.5% per month** interest on late payments
- Bad faith: court awards reasonable attorney fees
- **Does NOT apply to MDOT projects, schools, or contracts under $30,000**
- Michigan has **no private prompt payment statute** -- private project payment terms are purely contractual
- Source: [MCL 125.1561 et seq.](https://www.levelset.com/prompt-payment/michigan-prompt-payment-faqs/)

### MDOT-Specific Requirements
- Prime must pay subs within **10 calendar days** of receiving MDOT payment (separate special provision)
- DBE payment tracking via MERS (Form 2124A)
- Sanctions for non-compliance with prompt payment provisions
- Source: [MDOT Prompt Payment Special Provisions](https://www.michigan.gov/mdot/-/media/Project/Websites/MDOT/Programs/DBE/Resources/Prompt-Payment-Special-Provisions.pdf)

### Mechanic's Lien Rights for Surveyors (Private Projects)
- Michigan expanded lien rights in 2018 to include **licensed professional surveyors** as "design professionals"
- Surveyors follow separate recording procedures under MCL 570.1107a and 570.1107b
- **Critical caveat:** surveying may not qualify as "actual physical improvement" -- lien enforcement depends on whether survey work is directly tied to construction improvement
- Source: [Michigan Construction Lien Act, MCL 570.1101 et seq.](https://www.legislature.mi.gov/documents/mcl/pdf/mcl-act-497-of-1980.pdf)

## Digital Payment Platforms in Construction

| Platform | What It Does | Who Pays | Relevance |
|----------|-------------|----------|-----------|
| **GCPay** | Automates pay applications between GC and subs. Lien waiver exchange, compliance docs, ERP integration. | GC subscribes; subs use free or paid tier | Digitizes the paper pay-app process. No escrow or financing. |
| **Textura (Oracle)** | Pay application + lien waiver management. GC-driven: subs submit pay apps online, get paid electronically after approval. | GC buys; subs often forced to pay per-transaction fees | Largest incumbent. Handles billions in construction payments annually. No escrow. |
| **Billd** | Pays suppliers upfront on behalf of subs. Sub repays in 120 days. Also offers "Pay App Advances" -- sub gets paid immediately against approved pay apps. | Sub pays fees (discount on advance) | Solves the cash-flow gap. A sub waiting 60 days for GC payment can get cash now. Partnered with AmEx (Jan 2025). |
| **Levelset (Procore Payments)** | Lien rights management, preliminary notices, payment risk monitoring, lien waiver exchange. Now part of Procore. | Subscription model | Risk intelligence layer. Alerts when a project participant has payment problems. |
| **Payapps** | Cloud pay-app submission and approval. Popular in Australia, growing in US. | Subscription | Similar to GCPay but with retention tracking built in. |

**Do any support crypto/stablecoin?** None of the major construction payment platforms support cryptocurrency or stablecoin settlement as of March 2026. However, the infrastructure exists: smart contract escrow on stablecoins (USDC, USDT) is being piloted in real estate closings, and platforms like Uniscrow offer blockchain-based escrow. The construction industry has not adopted this yet due to regulatory uncertainty and the deeply entrenched banking/surety system.

## Proof of Funds / Commitment Mechanisms

At $72K-$250K, "swipe a credit card" doesn't work. Here's what the industry actually uses:

**1. Payment Bonds (most common on public projects)**
- A surety company guarantees the GC will pay its subs
- Cost: typically 1-3% of the bond amount ($720-$2,160 on a $72K sub)
- The surety underwrites the GC's financials before issuing the bond
- This IS the proof of funds for public projects

**2. Letters of Credit (LOCs)**
- A bank guarantees payment up to a stated amount
- Irrevocable LOC = the bank MUST pay if conditions are met
- Used on large private projects where the owner's creditworthiness is uncertain
- Cost: 1-3% annually of the LOC face value

**3. Construction Escrow Accounts**
- Third-party (title company or bank) holds project funds
- Disbursements require sworn statements listing all subs to be paid + lien waivers
- Common in residential and owner-funded commercial projects
- Adds cost and friction but provides strong payment assurance

**4. Subcontractor Pre-Qualification**
- Large GCs (Barton Malow, Walbridge) require subs to pre-qualify financially
- The GC reviews the sub's financials, bonding capacity, and insurance
- This is one-directional: the GC vets the sub, not vice versa
- A survey firm rarely gets to vet the GC's ability to pay

**5. Joint Check Agreements**
- Owner or GC issues checks payable to both sub and sub's supplier
- Ensures funds flow to the right party
- Common for material-heavy subs, less relevant for survey (labor-heavy)

## Marketplace Payment Models (Upwork, Thumbtack)

**Upwork (escrow model):**
- Client funds escrow upon contract creation (full amount or per-milestone)
- Minimum milestone: $5.00
- Freelancer submits work; client has 14 days to approve or request changes
- Auto-release after 14-day timeout
- Disputes: 5-day response window, then non-binding mediation by Upwork staff
- **No special treatment for large contracts** -- same process at $500 and $50,000
- Upwork takes 10% service fee (reduced at higher volume)

**Thumbtack (no escrow):**
- Thumbtack does NOT escrow or process project payments
- Payment flows directly between customer and contractor
- Revenue model: lead fees to contractors, not payment processing
- No payment protection for either party beyond the direct relationship

**Implication:** Upwork's milestone escrow model is the closest analog to what our marketplace needs, but it lacks construction-specific features (retainage, lien waivers, sworn statements, bonding integration).

## Recommended Marketplace Payment Flow

For a $72K robot survey task, here is the legally sound sequence from task spec to work start:

### Phase 1: Pre-Auction Qualification (Before Bidding Opens)
1. **GC posts task spec** with budget range and project details
2. **GC completes financial qualification** -- one of:
   - (a) Upload proof of payment bond covering the project (public projects)
   - (b) Fund marketplace escrow account for 25% of estimated value ($18K)
   - (c) Provide irrevocable letter of credit
   - (d) Connect verified bank account + agree to ACH authorization
3. **Marketplace verifies** the commitment mechanism and marks the auction as "funded"
4. **Robot operators see "funded" badge** before deciding to bid

### Phase 2: Auction & Award
5. Robot operators submit bids with price, schedule, equipment specs
6. GC selects winning bid ($72K)
7. **Smart contract or escrow locks Phase 1 mobilization payment** (typically 10-15% = $7,200-$10,800)
8. Both parties digitally sign the subcontract (auto-generated from task spec + bid)

### Phase 3: Execution & Payment
9. **Mobilization payment released** when robot arrives on-site (GPS/geofence verification)
10. **Progress payments** at defined milestones (e.g., 30% survey complete, 60%, 90%)
    - Each milestone triggers: work verification (point cloud QA) -> invoice auto-generated -> GC has 5 business days to approve or dispute -> funds released from escrow
11. **Final payment** (minus retainage) upon deliverable acceptance
12. **Retainage release** (5-10%) after punch-list / final QA period (30-60 days)

### Phase 4: Closeout
13. Lien waivers exchanged automatically
14. Final escrow reconciliation and release
15. Both parties rate each other

### Escrow Structure at $72K
- **Option A (Full Escrow):** GC deposits $72K upfront. Released per milestones. Maximum protection for the robot operator. High friction for the GC.
- **Option B (Rolling Escrow):** GC funds each milestone 5 days before it's due. Moderate friction, moderate protection.
- **Option C (Bond-Backed):** GC provides payment bond. No cash escrowed. Robot operator relies on bond claim if unpaid. Lowest friction, standard construction practice.

**Recommendation for MVP:** Option B (Rolling Escrow) with Option C available for bonded GCs. This balances construction industry norms with marketplace trust requirements.

## Implications for the Demo

The demo should NOT show a credit card form. Instead, it should show:

1. **"Fund Auction" step** where the GC chooses a commitment mechanism:
   - "Connect Bank Account" (ACH authorization for rolling milestone funding)
   - "Upload Payment Bond" (for bonded GCs on public projects)
   - "Fund Escrow" (wire/ACH a deposit to marketplace escrow)

2. **"Funded" badge on the task spec** visible to robot operators -- this is the marketplace's value proposition. Operators know they'll get paid before they bid.

3. **Milestone payment dashboard** showing:
   - Escrow balance
   - Next milestone and funding requirement
   - Payment history with dates
   - Auto-generated lien waivers

4. **For the $72K MDOT demo scenario specifically:**
   - The GC would have a payment bond (MDOT requires it on projects over $50K)
   - The marketplace verifies the bond and shows "Bond-Verified" status
   - Progress payments follow MDOT's 10-day prompt payment requirement
   - The demo shows the bond verification step, not a credit card swipe

**What makes this different from Upwork:** Construction-native payment rails. Retainage handling. Bond verification. Lien waiver automation. Prompt payment compliance tracking. These are the features that justify a construction-specific marketplace vs. posting on a general freelance platform.

---

Sources:
- [Crewcost: Common Payment Terms for Contractors](https://crewcost.com/blog/common-payment-terms-for-contractors/)
- [ABA: Miller Act Payment Bond Claims](https://www.americanbar.org/groups/construction_industry/publications/under_construction/2022/winter2022/miller-act-payment-bond-claims/)
- [Procore: Little Miller Acts by State](https://www.procore.com/library/little-miller-acts-bond-requirements-by-state)
- [Levelset: Michigan Prompt Payment FAQs](https://www.levelset.com/prompt-payment/michigan-prompt-payment-faqs/)
- [MDOT Prompt Payment Special Provisions](https://www.michigan.gov/mdot/-/media/Project/Websites/MDOT/Programs/DBE/Resources/Prompt-Payment-Special-Provisions.pdf)
- [Levelset: Michigan Bond Claim FAQs](https://www.levelset.com/bond-claim/michigan-bond-claim-faqs/)
- [Michigan Construction Lien Act](https://www.legislature.mi.gov/documents/mcl/pdf/mcl-act-497-of-1980.pdf)
- [Billd: Contractor Financing](https://billd.com/)
- [GCPay: Pay Application Software](https://ww3.gcpay.com/)
- [Oracle: Textura Construction Payment Management](https://www.oracle.com/construction-engineering/textura-construction-payment-management/)
- [Upwork: How Milestone Payments Work](https://support.upwork.com/hc/en-us/articles/211063718-How-payments-for-milestones-and-fixed-price-contracts-work)
- [Procore: Construction Escrow Accounts](https://www.procore.com/library/construction-escrow-accounts)
- [NetSuite: Retainage in Construction](https://www.netsuite.com/portal/resource/articles/accounting/retainage.shtml)
- [Levelset: Michigan Mechanics Lien FAQs](https://www.levelset.com/mechanics-lien/michigan-lien-law-faqs/)
