# PLS Digital Seal Requirements by State

Reference for operator onboarding and compliance checks when PLS-stamped deliverables are required.

## Seal Type Definitions

| Type | Description | Accepted States |
|------|-------------|-----------------|
| `image_only` | Scanned image of physical seal/stamp | Most states for internal/preliminary work |
| `docusign_esign` | DocuSign, Adobe Sign, or equivalent e-signature | States that accept ESIGN Act / UETA compliant signatures |
| `pki_cert` | PKI digital certificate from AATL-listed CA | OH, VA, NJ, FL (required for final deliverables) |

## States Requiring PKI Digital Certificates

These states explicitly require a PKI-based digital certificate (not a standard e-signature) for electronically sealed survey documents:

| State | Statute/Rule | Key Requirement |
|-------|-------------|-----------------|
| **Ohio** | OAC 4733-35-04 | Digital signature via PKI certificate from CA on AATL |
| **Virginia** | 18VAC10-20-760 | Digital seal using certificate-based signature |
| **New Jersey** | N.J.A.C. 13:40-6.3 | Electronic seal with digital certificate |
| **Florida** | 61G17-8.002 | Digital signature with certificate from approved CA |

## AATL-Listed Certificate Authorities

Operators in PKI-required states should obtain a certificate from an Adobe Approved Trust List (AATL) provider:

- **IdenTrust** — IGC certificates, widely used in government/engineering ($99-199/year)
- **GlobalSign** — AATL Document Signing certificates ($149-249/year)
- **DigiCert** — Document Signing certificates ($224/year)
- **Sectigo (Comodo)** — Personal Authentication certificates ($75-175/year)

## Onboarding Guidance

When registering operators who plan to deliver PLS-stamped work:

1. Ask which states they are licensed in
2. If any license is in OH, VA, NJ, or FL, inform them:
   - Standard DocuSign/Adobe Sign e-signatures do NOT satisfy PKI requirements
   - They need a PKI certificate from an AATL-listed CA (~$100-200/year)
   - The certificate must be in the name of the licensed PLS
3. Record their `pls_seal_capability` as one of: `image_only`, `docusign_esign`, `pki_cert`
4. For tasks requiring PLS stamp in PKI states, operators with `image_only` or `docusign_esign` capability should not be matched

## Task Spec Integration

When processing RFPs that require PLS-stamped deliverables in PKI states, add to capability_requirements:

```json
{
  "hard": {
    "certifications_required": ["licensed_surveyor"],
    "pls_seal_required": "pki_cert"
  }
}
```
