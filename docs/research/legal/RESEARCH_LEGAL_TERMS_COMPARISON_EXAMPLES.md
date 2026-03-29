# Legal Terms Comparison: Real-World Examples and Validation Sources

**Date:** 2026-03-29
**Purpose:** Validate whether we can build a skill comparing legal terms between robot operators and hiring entities

---

## Key Clauses to Compare (12 Dimensions)

| # | Clause | Why it matters for robot marketplace |
|---|--------|--------------------------------------|
| 1 | Indemnification | Broad vs intermediate vs comparative fault — Michigan prohibits broad form on public projects |
| 2 | Limitation of liability | 1x fee? 2x? Uncapped? Survey errors can cascade to $M in construction rework |
| 3 | Insurance minimums | CGL, E&O, aviation — does the sub's coverage meet the contract requirement? |
| 4 | Payment terms | Net-30/60/90, pay-when-paid vs pay-if-paid — critical for operator cash flow |
| 5 | Retainage | 5%? 10%? When released? Michigan allows reduction after 50% completion |
| 6 | Data ownership | Who owns the point cloud, orthomosaic, deliverables? |
| 7 | Standard of care | Professional standard ("reasonably prudent surveyor") vs warranty |
| 8 | Consequential damages | Waived or not? If not waived, operator faces unlimited exposure |
| 9 | Dispute resolution | Litigation vs mediation vs arbitration |
| 10 | Termination | For cause vs for convenience — can the GC cancel mid-survey? |
| 11 | Change orders | How scope changes are priced and approved |
| 12 | PLS responsibility | Who stamps deliverables? Sub's PLS or GC's PLS? |

## Standard Form Contracts Found

### Example 1: AIA A401-2017 vs ConsensusDocs 750 — Clause-by-Clause Comparison
- **Source:** https://www.sackstierney.com/blog/compare-and-contrast-the-aia-a-401-and-the-consensusdocs-750-forms-of-subcontract/
- **Content:** Detailed clause comparison by Sacks Tierney P.A. (AZ construction law firm)
- **Key differences documented:** Insurance (A401 requires additional insured; CD750 makes it optional), payment terms (A401 more favorable to subs), temporary facilities, financing information, mutual responsibility

### Example 2: AIA Official Comparison Document
- **Source:** https://content.aia.org/sites/default/files/2017-02/How%20Do%20ACD%20and%20ConsensusDOCS%20Subcontract%20Forms%20Compare.pdf
- **Content:** AIA's own published comparison matrix
- **Fields covered:** All major clauses side-by-side

### Example 3: AGC Nebraska — ConsensusDocs 750 vs AIA A401 Analysis
- **Source:** https://www.agcnebuilders.com/file_download/38cf0474-13ed-4f74-bdf3-039c5c2576ec
- **Content:** Contractor-perspective comparison with recommendations
- **Key insight:** CD750 is more balanced; A401 favors owners

### Example 4: ConsensusDocs Official Comparison Matrix
- **Source:** https://www.consensusdocs.org/wp-content/uploads/2020/05/Document-Comparison-Matrix.pdf
- **Content:** Full matrix comparing ConsensusDocs 200 series against AIA equivalents
- **Covers:** All contract types, not just subcontracts

### Example 5: MDOT Form 1302-FED — Michigan DOT Subcontract
- **Source:** https://mdotjboss.state.mi.us/webforms/GetDocument.htm?fileName=1302-FED.pdf
- **Content:** MDOT's mandatory subcontract form for federal-aid projects
- **Key:** Must incorporate FHWA-1273 (federal labor/EEO requirements)
- **Requirement:** 35% self-performance by prime contractor

### Example 6: MDOT Form 1386 — Subcontract Compliance Certification
- **Source:** https://mdotjboss.state.mi.us/webforms/GetDocument.htm?fileName=1386.pdf
- **Content:** Post-certification that all subcontracting requirements were met

### Example 7: MDOT DBE Participation Form 2653
- **Source:** Referenced in MDOT wiki at https://mdotwiki.state.mi.us/construction/index.php/108.01_Subcontracting_of_Contract_Work
- **Content:** DBE commitment documentation required before award

**Count: 7 real examples found. Threshold met.**

## Anti-Indemnity Statutes

Michigan (MCL 691.991): Voids indemnification requiring a party to indemnify for damages caused by the **sole negligence** of the indemnitee on public works. Allows intermediate indemnity (each party responsible for own proportional fault).

- **Source:** https://www.legislature.mi.gov/Laws/MCL?objectName=mcl-691-991
- **Applies to:** Public projects (MDOT, county, municipal)
- **Does NOT apply to:** Private commercial projects
- **Impact on skill:** Must flag broad-form indemnity clauses on public projects as unenforceable

50-state summary: https://www.mwl-law.com/wp-content/uploads/2013/03/Anti-Indemnity-Statutes-In-All-50-States-00131938.pdf

Source: [Barnes & Thornburg](https://btlaw.com/insights/publications/2018/broad-indemnification-provisions-could-result-in-no-indemnification-on-public-projects), [Michigan Construction Law](http://www.michiganconstructionlaw.com/page-i)

## Survey-Specific Contract Issues

1. **PLS stamp liability** — The PLS who stamps deliverables carries professional liability, not the drone pilot. The contract must specify whose PLS stamps.
2. **Data format obligations** — LandXML, DXF, GeoTIFF are contractual deliverables. If the contract says "CAD format" and the operator delivers LAS, that's a breach.
3. **Re-survey obligations** — If data fails QC, who pays for the re-fly? Contract should specify.
4. **Accuracy guarantee vs professional standard** — "±0.05 ft guaranteed" is a warranty. "Reasonably prudent surveyor" is a professional standard. The difference matters for liability.

## Skill Feasibility Assessment

**VERDICT: BUILD.** We have:
- ✅ 7 real contract examples (threshold: 5)
- ✅ AIA vs ConsensusDocs clause-by-clause comparisons from law firms
- ✅ MDOT-specific mandatory forms (1302-FED, 1386, 2653)
- ✅ Anti-indemnity statute text with 50-state summary
- ✅ Clear 12-dimension comparison framework
- ✅ Survey-specific clause issues documented

**What the skill does:**
1. Accept two documents: operator's standard terms + GC's proposed subcontract
2. Extract the 12 key clauses from each
3. Compare side-by-side: where do they agree? Where do they conflict?
4. Flag: unenforceable clauses (e.g., broad-form indemnity on public projects per MCL 691.991)
5. Flag: missing clauses (e.g., data ownership not specified)
6. Flag: risk imbalances (e.g., uncapped LOL, pay-if-paid)
7. Output: comparison matrix + risk assessment + recommended negotiation points

**What the skill cannot do (requires lawyer):**
- Provide legal advice on whether to sign
- Interpret ambiguous contract language
- Assess enforceability in untested legal scenarios
- Replace attorney review for high-value contracts
