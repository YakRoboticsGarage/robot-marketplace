# R-006: State PLS Board API Availability (All 50 States)

**Date:** 2026-04-01  
**Topic ID:** R-006  
**Module:** M36_pls_review  
**Status:** Complete  
**Researcher:** Automated daily research agent

---

## Executive Summary

- **No centralized API exists.** NCEES (the closest thing to a national registry) operates via a web portal only — there is no public REST API for license lookups.
- **Three states offer real programmatic access:** Colorado (Socrata open-data API), Indiana (eLicense API), and Massachusetts (Mass.gov API). All others require web scraping or manual verification.
- **Commercial APIs are the fastest path to broad coverage.** Checkr and MeshVerify both offer professional license verification APIs that aggregate state data, check active status, and return results instantly. Certn and Sterling also have APIs but appear less specialized for PLS/PE verification.
- **The current codebase accepts PLS license data at face value** — `set_pls()` in `operator_registry.py` stores whatever the operator submits without any external verification call. This is the primary gap.
- **A tiered strategy is viable:** use free state APIs where available, commercial API (Checkr/MeshVerify) for core markets, and flag remaining states as "manual review required."

---

## Findings

### 1. NCEES — No Public API

NCEES (National Council of Examiners for Engineering and Surveying) runs the **MyNCEES Records Program**, a verified portfolio of exam results, transcripts, and experience records for engineers and surveyors seeking multi-state licensure. It is used by state boards to electronically transmit verification data between jurisdictions.

However, **NCEES does not expose a public API**. All access is through the [MyNCEES web portal](https://ncees.org/launch-login/). Verification is initiated by the licensee or state board — there is no bulk lookup or third-party access mechanism documented publicly.

States that **require** an NCEES Record for comity licensure: Georgia, Kentucky, Massachusetts, Puerto Rico, Rhode Island, Wyoming.

**Action:** Contact NCEES directly to ask about data-sharing agreements or API access for marketplace use cases. URL: https://ncees.org/ncees-services/records-program/

---

### 2. States with Programmatic Access

#### Colorado — Socrata Open Data API ⭐ Free
- **Dataset:** "Professional and Occupational Licenses in Colorado"
- **URL:** https://data.colorado.gov/Regulations/Professional-and-Occupational-Licenses-in-Colorado/7s5z-vewr/data
- **Method:** Socrata REST API (standard `$where`, `$select`, `$limit` parameters)
- **Fields available:** License number, name, profession type, status, expiration date, county
- **Cost:** Free; no API key required for basic public access
- **Notes:** Dataset covers all professions regulated by the Division of Professions and Occupations. Land Surveyors are included. Updated periodically. The CIM API is documented at https://publicapis.io/colorado-information-marketplace-api
- **Example query:** `GET https://data.colorado.gov/resource/7s5z-vewr.json?profession_name=Land+Surveyor`

#### Indiana — eLicense Professional Licensing Agency API ⭐ Free
- **Method:** REST API (`pla-everification-api`)
- **Coverage:** Professional licenses issued by Indiana's Professional Licensing Agency
- **Notes:** Designed for businesses and organizations that need to verify employee/contractor credentials. PLS licenses are included.
- **Status:** Public API; implementation details require direct inquiry to Indiana PLA.

#### Massachusetts — Mass.gov Professional Licensing API ⭐ Free
- **URL:** https://www.mass.gov/how-to/request-a-license-verification-or-certified-license-history-document-engineers-and-land-surveyors
- **Method:** API available via Mass.gov developer resources
- **Fields:** License verification and certified license history for engineers and land surveyors specifically
- **Notes:** Explicit coverage of engineers and land surveyors makes this immediately useful.

---

### 3. States with Rosters / Downloadable Data (Partial Automation)

#### Texas — TBPELS Roster Search
- **URL:** https://pels.texas.gov/roster/rplssearch.html
- **Method:** Web form search; roster pages (RPLS, LSLS, SIT, Surveying Firm)
- **Fields:** License number, name (Last, First Middle), registration status, renewal status
- **Notes:** TBPELS maintains a public roster of all RPLS licensees updated regularly. Texas RPLS registrations renew yearly; only "Registered" status is valid. Privacy restrictions limit bulk export. Scraping the roster is technically feasible but requires rate limiting and courtesy.
- **Michigan's LARA** also lists a "License Lists and Reports" page at https://www.michigan.gov/lara/bureau-list/bpl/license-lists-and-reports — this may include downloadable bulk data. Multiple portals exist: Verify A License (val.apps.lara.state.mi.us), Accela Citizen Access (aca-prod.accela.com/MILARA), and ADMS Search. All update daily.

#### New York — NYSED Online Search
- **Method:** Web search; 1.5M+ licensees across 50+ professions
- **Fields:** Name, profession, license number, location, original license date, registration status
- **Notes:** NY requires NYSED registration for land surveyors. No bulk API documented. OpenGovUS aggregates some NY data.

#### Michigan — LARA "License Lists and Reports"
- **URL:** https://www.michigan.gov/lara/bureau-list/bpl/license-lists-and-reports
- **Method:** Likely downloadable report (format TBD); verify directly
- **Notes:** OpenGovUS.com (opengovus.com/michigan-license) aggregates Michigan license data and may offer its own API. Accela Citizen Access is the underlying platform — Accela has a documented REST API that some municipalities expose; unclear if MI LARA exposes it publicly.

---

### 4. Web Form Only (Manual or Scraping Required)

| State | Board | URL | Notes |
|-------|-------|-----|-------|
| California | BPELSG | https://www.bpelsg.ca.gov/consumers/lic_lookup.shtml | Web form; also at search.dca.ca.gov — possible undocumented API |
| Florida | DBPR | https://www2.myfloridalicense.com | No official API; Apify has a scraper (apify.com/exclusive_data/dbpr-myfloridalicense/api) |
| Ohio | Ohio Board | eLicense Ohio portal | eLicense is a commercial platform — may have API with board agreement |
| Washington | BRPELS | https://brpels.wa.gov | Web form |
| Maryland | DLLR | https://www.dllr.state.md.us/license/ls/lsverify.shtml | Web form |
| Kentucky | KY BOELS | http://elsweb.kyboels.ky.gov/kweb/Searchable-Roster | Public searchable roster |
| Maine | OPLR | https://www.maine.gov/pfr/professionallicensing | Web portal |

California's DCA (which oversees BPELSG) uses `search.dca.ca.gov` as its unified license search. Browser DevTools inspection suggests there may be an undocumented JSON endpoint — this requires further investigation (R-007 or a follow-up technical spike).

---

### 5. Commercial License Verification APIs

#### Checkr — Recommended for MVP ⭐⭐⭐
- **URL:** https://checkr.com/background-check/professional-license-verification
- **API:** https://checkr.com/our-technology/background-check-api
- **What it verifies:** Active status, good standing, name match against candidate-provided license number
- **Speed:** Most licenses verified instantly
- **Coverage:** Professional licenses across all 50 states (specific coverage of PLS licenses not confirmed — needs direct inquiry)
- **Integration:** REST API with background check dashboard
- **Pricing:** Per-check; contact Checkr for volume pricing

#### MeshVerify — Specialized for Professional Licenses ⭐⭐⭐
- **URL:** https://meshverify.com/
- **Focus:** Professional license verification and business identity verification specifically
- **API:** Documented at meshverify.com/product-business-entity-verification
- **Notes:** More specialized than Checkr for the professional license use case. Likely covers PE/PLS licenses directly.

#### Certn — Broad Coverage, API-First ⭐⭐
- **API docs:** https://docs.certn.co/api/
- **Credential Verification:** Validates license status, issuance date, conditions/restrictions
- **Coverage:** 200+ countries and territories
- **Returns:** Active/inactive status, issuance date, expiration date, any restrictions
- **Pricing:** Per-check; pass-through access fees for some checks. Pricing at certn.co/us/pricing/

#### Sterling (First Advantage) — Enterprise ⭐⭐
- **API:** https://apidocs.sterlingcheck.app
- **Notes:** Enterprise-grade background check platform; likely covers professional license verification as part of broader offering. Higher implementation overhead than Checkr or MeshVerify.

#### verify-license.com ⭐ (Unknown Quality)
- **URL:** https://www.verify-license.com/
- **Notes:** Found in search; unclear quality, coverage, or pricing. Low-cost option worth investigating.

---

### 6. Aggregator / Open Data Sources

- **OpenGovUS** (opengovus.com): Aggregates public license data from multiple states including Michigan. May have a commercial API.
- **data.gov**: Inconsistent coverage; most state license data is not on the federal open data portal.
- **NASCLA**: Focused on general contractor licensing, not professional land surveyors. Interstate reciprocity framework exists but is separate from PLS boards.

---

### 7. Typical Data Fields Available in State PLS Lookups

Based on cross-state review, the following fields are commonly available:

| Field | Availability |
|-------|-------------|
| Full name | Universal |
| License number | Universal |
| License type (PLS/RPLS/PS) | Universal |
| Status (active/expired/suspended) | Universal |
| State of licensure | Universal |
| Expiration/renewal date | Most states |
| County/city | Common |
| Disciplinary actions | Some states (CA, NY) |
| Endorsements/specializations | Rare |
| Business affiliation | Rare |

---

## Implications for the Product

### Current Code Gap

`auction/operator_registry.py` — `set_pls()` (line 116-134): stores operator-submitted PLS info without any external verification. `auction/compliance.py` — `upload_document()` (line 54-75): marks all compliance docs as `VERIFIED` immediately on upload, noting "In a production system, this would trigger async verification against external APIs." This comment is the gap we must close.

The compliance module already has SAM.gov debarment checking as the model for how to integrate an external API — PLS verification should follow the same pattern.

### Required Architecture

A `check_pls_license()` function in `compliance.py` following the same pattern as `check_sam_exclusion()`:
- When `PLS_VERIFICATION_API_KEY` is set (Checkr, MeshVerify, or Certn), call the external API
- Without a key, return `WARN` indicating manual verification needed
- Log verification result to audit trail
- Cache results with expiration (daily re-check on expiry)

The verification should be triggered from `upload_document()` when `doc_type == "pls_license"`.

---

## Improvement Proposals

### IMP-001: Integrate External PLS License Verification API
Add an async external verification call for PLS licenses in `compliance.py`, following the existing SAM.gov pattern. Use Checkr or MeshVerify as the verification provider (API key configurable via env var `PLS_VERIFY_API_KEY`).

### IMP-002: Integrate Colorado Socrata API for Free Tier Verification
For Colorado-licensed operators, query the free Socrata open-data API (data.colorado.gov) to verify PLS license status without a commercial API key. This provides a no-cost fallback for CO-licensed surveyors.

### IMP-003: State-Tiered PLS Verification Strategy
Build a state routing table in the compliance module: Tier 1 (free API — CO, IN, MA), Tier 2 (commercial API — Checkr/MeshVerify), Tier 3 (manual review flag). Route verification attempts to the appropriate tier based on the operator's license state.

---

## New Questions Spawned

- **R-007** (already queued): Electronic survey seal/stamp regulations by state — now unblocked since R-006 is complete.
- **R-006b** (new): What are the specific API schemas and rate limits for Checkr vs. MeshVerify PLS verification? What is the per-check cost at 100/month vs. 1000/month volume?
- **R-006c** (new): Does the California DCA `search.dca.ca.gov` expose an undocumented JSON endpoint via browser inspection? A technical spike to check network requests during a license lookup could reveal an API.
- **R-006d** (new): Does Michigan LARA's "License Lists and Reports" page provide a downloadable bulk CSV? If so, we could build a nightly sync for Michigan operators (our primary market) at zero cost.

---

## Sources

- NCEES Records Program: https://ncees.org/ncees-services/records-program/
- NCEES License Verification FAQs: https://help.ncees.org/article/68-license-verification-faqs
- Colorado Information Marketplace (Socrata API): https://data.colorado.gov/Regulations/Professional-and-Occupational-Licenses-in-Colorado/7s5z-vewr/data
- Colorado CIM API listing: https://publicapis.io/colorado-information-marketplace-api
- Michigan LARA Verify A License: https://val.apps.lara.state.mi.us/
- Michigan LARA License Lists and Reports: https://www.michigan.gov/lara/bureau-list/bpl/license-lists-and-reports
- Michigan LARA Accela portal: https://aca-prod.accela.com/MILARA/GeneralProperty/PropertyLookUp.aspx?isLicensee=Y&TabName=APO
- Texas TBPELS RPLS Roster: https://pels.texas.gov/roster/rplssearch.html
- Texas TBPELS RPLS Roster Search: https://pels.texas.gov/roster/ls_rosters.html
- California BPELSG License Lookup: https://www.bpelsg.ca.gov/consumers/lic_lookup.shtml
- California BPELSG License Verification: https://www.bpelsg.ca.gov/licensees/verification.shtml
- Florida DBPR MyFloridaLicense: https://www2.myfloridalicense.com
- Florida DBPR Apify scraper: https://apify.com/exclusive_data/dbpr-myfloridalicense/api
- Massachusetts engineer/surveyor license verification: https://www.mass.gov/how-to/request-a-license-verification-or-certified-license-history-document-engineers-and-land-surveyors
- Kentucky BOELS Searchable Roster: http://elsweb.kyboels.ky.gov/kweb/Searchable-Roster
- Maryland DLLR LS Verify: https://www.dllr.state.md.us/license/ls/lsverify.shtml
- Washington BRPELS: https://brpels.wa.gov/licensing/land-surveying/professional-land-surveyor-license-exam
- OpenGovUS Michigan licenses: https://opengovus.com/michigan-license
- Checkr Professional License Verification: https://checkr.com/background-check/professional-license-verification
- Checkr API: https://checkr.com/our-technology/background-check-api
- MeshVerify: https://meshverify.com/
- Certn Credential Verification: https://certn.co/credential-verification/
- Certn API docs: https://docs.certn.co/api/
- Certn pricing: https://certn.co/us/pricing/
- Sterling API: https://apidocs.sterlingcheck.app
- verify-license.com: https://www.verify-license.com/
- SAM.gov Exclusions API (existing pattern in codebase): https://open.gsa.gov/api/exclusions-api/
