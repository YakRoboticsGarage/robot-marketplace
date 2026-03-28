# Legal Framework: Robot Survey Contracts

Research date: 2026-03-28. This document covers legal agreements, insurance, licensing,
liability, and drone/robot-specific issues for a marketplace that connects construction
projects with robotic/drone survey operators.

---

## Standard Agreements

### Industry Standard Forms

- **AIA A401-2017** — Standard Form of Agreement Between Contractor and Subcontractor.
  Establishes scope, payment, insurance, dispute resolution. Incorporates AIA A201-2017
  General Conditions by reference. Flow-down clauses bind the subcontractor to the same
  obligations the GC owes the owner. No survey-specific provisions; these must be added
  via exhibit or supplementary conditions.
- **ConsensusDocs 750** — Constructor and Subcontractor Agreement (Long Form). Considered
  more balanced than AIA for subcontractors. Indemnification is limited to each party's
  percentage of negligence and covers only insurable risks (bodily injury, property damage).
  Defense cost reimbursement is proportional to fault. SMACNA and AGC endorse it.
- **ConsensusDocs 751** — Short Form, suitable for smaller survey task orders.
- **ConsensusDocs 752** — Federal government construction subcontracts.

### Survey-Specific Contract Provisions

Standard forms do not contain survey/geospatial clauses. A survey subcontract must add:

1. **Deliverable specifications** — coordinate system (State Plane, UTM), datum (NAD83/NAVD88),
   file formats (LAS 1.4, GeoTIFF, DXF, SHP), accuracy class (ASPRS standards).
2. **PLS stamp requirement** — which deliverables require a licensed surveyor's seal.
3. **Data ownership and license** — who owns raw data, processed deliverables, and derived products.
4. **Technology provisions** — drone flight plans, autonomous robot mission parameters, sensor specs.
5. **Site access and safety** — OSHA compliance, site-specific safety plans, right-of-entry letters.

### DOT Survey Consultant Agreements

- **TxDOT** uses custom professional services agreements for survey consultants. Requires
  TxDOT Form 1560-CSS certificate of insurance. Right-of-entry letters per the TxDOT
  Surveyors' Toolkit. The TxDOT Survey Manual (revised March 2025) governs procedures.
- **MDOT (Michigan)** follows Michigan Occupational Code (MCL 339.2001 et seq.) for surveyor
  qualifications. DOT contracts typically require the consultant to carry the state as
  additional insured and waive subrogation rights.
- DOT contracts generally impose stricter insurance limits than private work (see below).

---

## Insurance Requirements (with typical limits)

### Required Coverage Types

| Coverage | Typical Private Project | DOT / Public Project |
|---|---|---|
| Commercial General Liability (CGL) | $1M per occurrence / $2M aggregate | $2M per occurrence / $5M aggregate |
| Professional Liability (E&O) | $1M per claim / $2M aggregate | $2M per claim / $5M aggregate |
| Workers Compensation | Statutory limits per state | Statutory limits per state |
| Employers Liability | $500K / $500K / $500K | $1M / $1M / $1M |
| Commercial Auto | $1M combined single limit | $1M-$2M combined single limit |
| Umbrella / Excess | $2M-$5M | $5M-$10M |
| Drone / Aviation Liability | $1M per occurrence (minimum) | $2M-$5M per occurrence |
| Drone Hull Coverage | At replacement value | At replacement value |

### Key Insurance Details

- **CGL** is occurrence-based. Must name GC and owner as Additional Insured. Include
  Waiver of Subrogation endorsement. The professional services exclusion in CGL policies
  means survey errors are NOT covered by CGL — that is what E&O is for.
- **Professional Liability / E&O** is claims-made (not occurrence). The retroactive date
  and tail coverage matter. Survey firms must maintain E&O for years after project
  completion because claims can emerge when construction reveals survey errors.
- **Drone / Aviation Liability** is a separate policy from CGL. Covers third-party bodily
  injury and property damage from drone operations. Hull coverage (8-12% of insured value
  annually) covers the aircraft itself. Providers: SkyWatch, BWI Fly, Global Aerospace.
- **TxDOT** requires auto liability minimum $600K combined single limit. Only TxDOT's own
  certificate form (Form 1560-CSS) is accepted — not ACORD forms.

### Certificate of Insurance (COI)

The industry standard is **ACORD 25** (Certificate of Liability Insurance). A single-page
form showing: producer info, insurer names with NAIC numbers, policy numbers and dates,
coverage types and limits, additional insured status (ADDL INSD column), waiver of
subrogation status (SUBR WVD column), certificate holder name, and authorized signature.

The marketplace must verify: (a) policy is current, (b) limits meet minimums, (c) additional
insured endorsement is present, (d) coverage types match requirements.

---

## Professional Licensing

### Professional Land Surveyor (PLS) Requirements

All 50 states require a PLS license to practice land surveying. Core requirements:

- **Education**: Degree in surveying or related field (ABET-accredited preferred).
- **Experience**: 4-8 years under a licensed PLS (varies by state). Michigan requires 8
  years including up to 5 years of education credit.
- **Exams**: NCEES Fundamentals of Surveying (FS), NCEES Principles and Practice of
  Surveying (PS), plus state-specific exam.
- **Continuing education**: Typically 20-30 hours per biennium. Michigan requires 30 hours
  per 2-year renewal period. Colorado has no CE requirement.

### Michigan Surveyor Licensing (MCL 339.2001 et seq.)

- **MCL 339.2001**: Defines "practice of professional surveying" — consultation, investigation,
  mapping, measurements relative to location, size, shape of the earth, land boundary
  establishment, subdivision platting.
- **MCL 339.2004**: Licensing requirements — 8 years experience, NCEES FS exam, NCEES PS
  exam, Michigan state-specific exam.
- **MCL 339.2007**: Certificate of Authorization required for firms (not just individuals).
- Continuing education: 30 hours per biennial renewal.

### PLS Stamp on Deliverables

Every state requires a PLS seal/stamp on survey plats, legal descriptions, and boundary
surveys. For construction staking and topographic surveys, most states require the PLS
stamp on final deliverables that will be relied upon for construction. Point clouds and
orthomosaics that serve as the basis for engineering design generally require PLS certification.

### FAA Part 107 and Survey Licensing Intersection

- **FAA Part 107** (14 CFR Part 107) governs commercial drone operations for aircraft under
  55 lbs. Requires a Remote Pilot Certificate. Altitude limit: 400 ft AGL (can fly higher
  within 400 ft of a structure). Daylight/civil twilight only without waiver. Controlled
  airspace (Class B/C/D/E) requires LAANC or manual authorization.
- **Part 108** (new, 2025): Enables BVLOS operations for drones up to 110 lbs — relevant
  for large-area survey missions.
- **Dual licensing**: The drone pilot needs Part 107; the survey professional needs PLS.
  These can be different people. The PLS supervises and stamps deliverables; the Part 107
  pilot operates the aircraft.
- **Can a robot operate under a PLS license?** Yes — the robot/drone is a tool, not a
  practitioner. The licensed PLS is responsible for the accuracy and quality of deliverables
  regardless of the data collection method. The PLS must supervise the mission planning,
  ground control placement, and QA/QC of results.

---

## Liability and Indemnification

### Standard of Care

Survey professionals are held to the standard of care of a "reasonably prudent surveyor"
under similar circumstances. This is not perfection — it is professional reasonableness
measured against what a similarly situated professional would do. Contractual language
that elevates the standard (e.g., "shall be free from all errors") may be uninsurable
and should be avoided.

### Limitation of Liability (LOL)

- **Typical caps**: 1x the total fees paid under the contract is the industry standard
  and widely accepted. Some contracts use 2x fees for elevated-risk work. Fixed dollar
  caps ($500K, $1M) are also common.
- **Consequential damages**: Almost always mutually waived. AIA A401 and ConsensusDocs 750
  both address consequential damage waivers.
- **Enforceability**: Varies by jurisdiction. Courts scrutinize for fairness, relative
  bargaining power, and clarity. LOL clauses are generally unenforceable for gross
  negligence, willful misconduct, or statutory violations.
- **E&O policy alignment**: The LOL cap should not exceed E&O policy limits. A $50K survey
  fee with $1M E&O coverage and a 1x fee cap ($50K) protects both parties.

### Indemnification

- **ConsensusDocs 750 approach** (recommended): Mutual indemnification limited to each
  party's percentage of negligence, covering only insurable risks. Defense costs
  reimbursed proportionally.
- **AIA approach**: Broader indemnification language; subcontractor typically indemnifies
  GC and owner. Can be one-sided.
- **Anti-indemnity statutes**: Many states (including Texas and Michigan) prohibit or limit
  broad-form indemnification that requires a party to indemnify another for the other's
  own negligence.

### Survey Error Case Law

- **Chaney & James Construction v. United States**: Damages awarded for defective
  elevation specifications in construction documents.
- **H. John Homan Co. v. United States**: Damages for defective site survey.
- **Texas statute of limitations**: 10 years from survey completion for claims arising
  from survey errors (Texas Civil Practice & Remedies Code).
- **Typical damages**: Diminution in property value, cost to correct/reconstruct,
  additional expenses caused by the error. Courts aim to put the claimant in the position
  they would have been in absent the error.

---

## Drone/Robot-Specific Legal Issues

### FAA Regulatory Compliance

- Part 107 Remote Pilot Certificate required for all commercial drone ops.
- LAANC authorization for controlled airspace (many urban construction sites).
- Part 108 BVLOS rules (2025) enable long-range autonomous survey missions.
- Registration required for all drones over 0.55 lbs (Remote ID also required).

### Drone Crash Liability on Construction Sites

- Aviation liability insurance covers third-party bodily injury and property damage.
- GC/owner should be named as additional insured on the drone operator's policy.
- Hull coverage pays for the drone itself (8-12% of insured value annually).
- The drone operator bears primary liability; the GC may have vicarious liability if the
  operator is acting under GC's direction and control.

### Autonomous Robot Liability (Spot, etc.)

- No settled case law yet for autonomous construction robots.
- Liability follows traditional product liability and negligence frameworks: manufacturer
  (defect), operator (improper use/maintenance), employer (respondeat superior).
- The human operator is legally responsible — the robot is a tool, not an agent.
- Contract should specify: who controls the robot on-site, who is responsible for
  collision avoidance, what happens if the robot damages a structure or injures a worker.

### Privacy and Airspace

- *United States v. Causby* (1946): Landowners own "immediate reaches" of airspace above
  their property.
- Nevada law: civil trespass for drones below 250 ft over private land without consent.
- FAA regulates airspace safety; privacy is a state/local matter.
- Construction surveys near private property: obtain consent or ensure flights remain
  over the project site. Capturing images of neighboring private areas with a reasonable
  expectation of privacy can trigger trespass or invasion-of-privacy claims.

---

## Data Ownership

Survey data ownership should be explicitly addressed in the subcontract. Typical structure:

- **Raw sensor data** (photos, LiDAR scans): Owned by the survey firm unless contract
  assigns it to the client. Often retained by the firm for E&O defense purposes.
- **Processed deliverables** (point clouds, orthomosaics, DEMs, contour maps): Typically
  become property of the client upon payment. Delivered in open formats (LAS, GeoTIFF,
  DXF, SHP, CSV).
- **Derived products** (3D models, BIM integration): Ownership depends on who created them
  and contract terms.
- **License back**: Even when ownership transfers, the survey firm should retain a license
  to use deliverables for portfolio, quality records, and E&O defense.
- **Re-use rights**: A single drone survey can yield multiple deliverable types. The
  contract should clarify whether the client can extract additional products from raw data.

---

## What the Marketplace Facilitates

1. **Template agreements** — Auto-populated from task spec: scope, deliverables, accuracy
   requirements, schedule, price. Based on ConsensusDocs 750 structure with survey-specific
   exhibits. Digital execution via DocuSign or Adobe Sign.
2. **Insurance verification** — Automated COI parsing (ACORD 25). Verify: policy current,
   limits meet task minimums, additional insured endorsement present. Flag expiring
   policies. Integration with providers like myCOI or Jones.
3. **License verification** — PLS license validation against state licensing board databases.
   FAA Part 107 certificate verification. Firm Certificate of Authorization check.
4. **Escrow and payment** — Hold funds in escrow; release upon deliverable acceptance.
   Progress payments for larger projects. Lien waiver exchange.
5. **Dispute resolution** — Tiered: negotiation, then mediation, then binding arbitration.
   Per ConsensusDocs model. Small claims fast-track for disputes under $25K.
6. **Digital signatures** — ESIGN Act and UETA compliant. Full audit trail.

---

## Recommended Legal Flow: Auction Award to Work Start

1. **Auction closes** — Winning bid selected. Task spec locked.
2. **Agreement generated** — Marketplace auto-generates subcontract from template + task spec.
3. **Insurance verified** — COI uploaded or pulled from vault. Limits checked against task
   requirements. Additional insured endorsement confirmed.
4. **License verified** — PLS license and Part 107 certificate validated. Firm authorization
   checked.
5. **Agreement signed** — Both parties execute digitally.
6. **Escrow funded** — Client deposits payment (or milestone schedule confirmed).
7. **Site access granted** — Right-of-entry letter issued. Safety plan acknowledged.
8. **Work begins** — Robot/drone deployed. Progress tracked in marketplace.
9. **Deliverables submitted** — QA/QC review against spec. PLS stamps applied.
10. **Acceptance and payment** — Client accepts deliverables. Escrow released. Lien waiver
    exchanged.

---

## What Should Appear on Robot Profiles

- Operator's PLS license number, state, and expiration date
- FAA Part 107 certificate number
- Firm Certificate of Authorization (where required)
- Insurance summary: CGL limits, E&O limits, drone/aviation liability limits
- COI on file (yes/no, expiration date)
- Equipment list: drone models, sensors, ground control equipment
- Accuracy capabilities (e.g., "1 cm horizontal, 2 cm vertical with RTK")
- Completed project count and client ratings
- Safety record (incidents, OSHA citations)

---

## What Should Appear at Auction Award

- Auto-generated subcontract (PDF preview) with all task-specific terms populated
- Insurance compliance status: green/yellow/red for each required coverage type
- License compliance status: PLS valid, Part 107 valid, firm auth valid
- Escrow funding status
- Estimated deliverable timeline
- Dispute resolution terms summary
- Data ownership terms summary
- Limitation of liability cap (calculated as 1x task fee, displayed explicitly)
- Required signatures checklist (both parties)

---

*Sources: AIA A401-2017, ConsensusDocs 750/751/752, MCL 339.2001-2014, 14 CFR Part 107,
14 CFR Part 108, FAA Remote Pilot Certificate program, ACORD 25 form standard, TxDOT
Survey Manual (March 2025), TxDOT Form 1560-CSS, United States v. Causby (1946),
NCEES FS/PS examinations, ASPRS accuracy standards.*
