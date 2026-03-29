---
name: legal-terms-compare
description: Compare legal terms between a robot/drone survey operator's standard terms and a GC's proposed subcontract. Identifies conflicts, flags unenforceable clauses (anti-indemnity statutes), and highlights risk imbalances across 12 key dimensions. Use whenever the user uploads two contracts, asks to compare subcontract terms, mentions "AIA A401", "ConsensusDocs 750", "indemnification clause", "limitation of liability", "subcontract review", or needs to understand how two sets of terms differ. Also trigger on "compare contracts", "review subcontract", or "what are the risks in this agreement."
---

# Legal Terms Comparison

Compare two sets of construction contract terms side-by-side across 12 key dimensions. Flag conflicts, unenforceable clauses, and risk imbalances. This is NOT legal advice — it's a structured comparison to inform negotiation.

## Workflow

### 1. Accept two documents

Accept any combination of:
- Operator's standard terms (their default agreement)
- GC's proposed subcontract (what they want the operator to sign)
- A standard form reference (AIA A401, ConsensusDocs 750, MDOT 1302-FED)
- Marketplace-generated template (ConsensusDocs 751 auto-populated)

If only one document is provided, compare it against the marketplace default terms (ConsensusDocs 751 baseline in `references/marketplace-baseline-terms.md`).

### 2. Extract clauses across 12 dimensions

For each document, extract the specific clause language for:

1. **Indemnification** — broad, intermediate, or comparative fault?
2. **Limitation of liability** — cap amount (1x fee, 2x, uncapped)?
3. **Insurance requirements** — CGL, E&O, aviation minimums?
4. **Payment terms** — net-30/60/90? Pay-when-paid or pay-if-paid?
5. **Retainage** — percentage? Release conditions?
6. **Data ownership** — who owns deliverables upon payment?
7. **Standard of care** — professional standard or warranty?
8. **Consequential damages** — waived or not?
9. **Dispute resolution** — litigation, mediation, or arbitration?
10. **Termination** — for cause only, or for convenience too?
11. **Change orders** — how are scope changes priced?
12. **PLS responsibility** — whose licensed surveyor stamps deliverables?

Mark each as: FOUND (with exact clause text) or NOT FOUND (missing from document).

### 3. Load applicable state law

Read `references/anti-indemnity-by-state.md` for the project's state. Flag any clause that violates the state's anti-indemnity statute.

For Michigan public projects: MCL 691.991 prohibits broad-form indemnity (indemnifying for sole negligence of the indemnitee).

### 4. Compare and flag

For each dimension, classify as:
- **MATCH** — both documents agree
- **CONFLICT** — documents disagree (state what each says)
- **MISSING** — one or both documents don't address this
- **UNENFORCEABLE** — clause violates applicable law (cite statute)
- **RISK IMBALANCE** — one party bears disproportionate risk

### 5. Generate comparison report

Output:

```json
{
  "comparison_status": "COMPATIBLE | CONFLICTS_FOUND | REVIEW_REQUIRED",
  "project_state": "MI",
  "documents": {
    "doc_a": "Operator standard terms",
    "doc_b": "GC proposed subcontract"
  },
  "dimensions": [
    {
      "dimension": "Indemnification",
      "doc_a": "Intermediate — each party indemnifies for own negligence",
      "doc_b": "Broad — sub indemnifies for any claim arising from the work",
      "status": "UNENFORCEABLE",
      "detail": "Broad-form indemnity unenforceable on MI public projects per MCL 691.991",
      "risk_level": "high",
      "recommendation": "Negotiate to intermediate form (comparative fault)"
    }
  ],
  "summary": {
    "matches": 5,
    "conflicts": 4,
    "missing": 2,
    "unenforceable": 1,
    "risk_imbalances": 3
  },
  "negotiation_points": [
    "Indemnification: request intermediate form per MCL 691.991",
    "LOL: cap at 1x task fee ($72,000) — current draft is uncapped",
    "Data ownership: specify client owns upon payment (currently silent)"
  ],
  "disclaimer": "This comparison is informational only. It is not legal advice. Consult an attorney before signing."
}
```

### 6. Validate output

```bash
python scripts/validate_terms_comparison.py < report.json
```

## References

- `references/marketplace-baseline-terms.md` — The marketplace's default terms (ConsensusDocs 751 framework). Used as comparison baseline when only one document is provided.
- `references/anti-indemnity-by-state.md` — Anti-indemnity statutes for key states (MI, TX, CA, OH, FL). Which indemnity forms are void and unenforceable.
- `references/clause-comparison-guide.md` — For each of the 12 dimensions: what "good" looks like for operators, what "good" looks like for GCs, and what the balanced position is.

## What this skill explicitly CANNOT do

- Provide legal advice
- Interpret ambiguous language definitively
- Predict court outcomes for disputed clauses
- Replace attorney review (especially for contracts >$50K)

Every output includes the disclaimer. The skill informs negotiation; it does not authorize signing.
