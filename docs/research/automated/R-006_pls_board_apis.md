# R-006: State PLS Board API Availability (All 50 States)

**Date:** 2026-04-01  
**Topic ID:** R-006  
**Module:** M36_pls_review  
**Status:** Complete  
**Researcher:** Automated daily research agent (two-pass: broad survey + 8-state deep dive)

---

## Executive Summary

- **No state PLS board exposes a public REST API.** All programmatic access requires scheduled file downloads, web scraping, or FOIA/public records requests.
- **NCEES has no public API** — verification is licensee-initiated via the MyNCEES web portal; no third-party pull access exists.
- **Two states have direct CSV downloads (no account required):** Texas TBPELS publishes a daily RPLS roster CSV at a stable URL; Michigan LARA offers an on-demand Excel/CSV report generator covering Professional Surveyor with name, status, expiration, address, and email.
- **Critical agency split in Florida:** Professional Surveyors and Mappers are licensed by **FDACS** (Dept. of Agriculture), not DBPR. Any integration targeting DBPR will miss the entire Florida PLS population.
- **Commercial APIs exist but are priced for employment screening.** Checkr charges ~$12/check; Certn charges $3–$25/check. At construction-task volumes, building a state-adapter layer against TX CSV + MI report + CA DCA Open Data is more cost-effective than per-check APIs.
- **The current codebase accepts PLS data at face value** — `set_pls()` in `operator_registry.py` and `upload_document()` in `compliance.py` store operator-submitted data without any external verification call. This is the primary gap to close.

---

## Findings

### 1. NCEES — No Public API

NCEES (National Council of Examiners for Engineering and Surveying) runs the **MyNCEES Records Program**: a verified portfolio of exam results, transcripts, and experience records for engineers and surveyors seeking multi-state licensure. State boards use it to electronically transmit verification data between jurisdictions.

**NCEES does not expose a public API.** All access is through the [MyNCEES web portal](https://ncees.org/launch-login/). Verification is licensee-initiated — there is no bulk lookup or third-party pull mechanism.

States that require an NCEES Record for comity licensure: Georgia, Kentucky, Massachusetts, Puerto Rico, Rhode Island, Wyoming.

**Action:** Contact NCEES directly about data-sharing agreements for marketplace use cases.

---

### 2. State-by-State Deep Dive (8 Key Markets)

#### Michigan — LARA Bureau of Professional Licensing ⭐ Best in Class
- **Lookup:** https://val.apps.lara.state.mi.us/ (individual) | https://aca-prod.accela.com/MILARA/ (Accela)
- **Bulk method:** Self-serve Excel/CSV report generator, no account required
- **Bulk URL:** https://www.michigan.gov/lara/bureau-list/bpl/license-lists-and-reports
- **Data fields:** Name, profession name, profession type, status, expiration date, address, issue date, specialties, **email address**
- **Update frequency:** Real-time query at generation time
- **Professional Surveyor:** Explicitly listed as a covered profession in the report generator
- **API:** None public; underlying platform is MiPLUS/Accela
- **Notes:** Michigan has not yet removed address and email from bulk exports (contrast: Texas removed these in 2023). This is the richest bulk dataset of all surveyed states.

#### Texas — TBPELS ⭐ Direct CSV Download
- **Lookup:** https://pels.texas.gov/roster/rplssearch.html
- **Bulk URLs:**
  - RPLS: `https://pels.texas.gov/roster/rpls_roster.csv`
  - Surveying Firms: `https://pels.texas.gov/roster/sur-firm_roster.csv`
  - Also available: LSLS roster, SIT roster
- **Data fields:** License number, name, license type, status, city, state — **addresses, phone numbers, and email removed** as of September 1, 2023 (SB 510)
- **Update frequency:** Daily
- **API:** None. Direct file download, no authentication required.
- **Notes:** Most accessible bulk data of all states — stable URL, daily refresh, no account or FOIA request needed. Name + license number + status is sufficient for verification.

#### California — DCA / BPELSG ⭐ Downloadable List (Not CSV API)
- **Lookup:** https://search.dca.ca.gov/ (DCA unified) | https://www.bpelsg.ca.gov/consumers/lic_lookup.shtml (BPELSG direct)
- **Bulk method:** Downloadable licensee list via DCA Open Data Portal (https://www.dca.ca.gov/data/index.shtml)
- **Data fields:** License number, license type code (**L** = Land Surveyor, **PS** = Photogrammetric Surveyor), name, status (Clear/Cancelled/Delinquent/Revoked), address, disciplinary actions
- **Update frequency:** Daily (individual lookup); bulk list cadence not documented
- **API:** No public REST API. File download only.
- **Contact for bulk/verification:** BPELSG.License.Verifications@dca.ca.gov | (916) 999-3600
- **Notes:** `search.dca.ca.gov` may expose an undocumented JSON endpoint (see R-006c — browser DevTools investigation needed).

#### Florida — **⚠️ FDACS, NOT DBPR**
- **CRITICAL:** Professional Surveyors and Mappers in Florida are licensed by **FDACS** (Dept. of Agriculture and Consumer Services), **not DBPR**. DBPR covers contractors, real estate, cosmetology, etc.
- **FDACS PSM page:** https://www.fdacs.gov/psm
- **Bulk data:** No public CSV download found. A Chapter 119 (Florida Sunshine Law) public records request to FDACS is the route for bulk data.
- **DBPR** (does NOT cover surveyors): offers bulk ASCII/CSV downloads at `myfloridalicense.com/dbpr/sto/file_download/index.html` — weekly, 365K records — but this is wrong agency for PLS.
- **Apify scraper exists for DBPR** (not FDACS): https://apify.com/exclusive_data/dbpr-myfloridalicense/api
- **Action required:** Contact FDACS directly or file a Ch. 119 request for FL PLS bulk data.

#### Ohio — PEPS / eLicense Ohio
- **Lookup:** https://www.elicense.ohio.gov/oh_verifylicense?board=Engineers+and+Surveyors+Board
- **Board:** https://peps.ohio.gov
- **Scale:** 27,000+ individual registrants, 3,200+ firms
- **Bulk method:** Web form only. Ohio Open Data Portal (data.ohio.gov) exists but no confirmed PE/PS dataset.
- **API:** eLicense Ohio is Salesforce-backed; no public API documented.
- **Notes:** eLicense covers 24 Ohio agencies. Primary source verification recognized by Joint Commission and NCQA. The Indiana eLicense API (separate from Ohio) is a different platform.

#### Illinois — IDFPR / CORE
- **Lookup:** https://online-dfpr.micropact.com/lookup/licenselookup.aspx
- **Bulk method:** CSV export within CORE system (launched October 30, 2024); monthly Active License Reports in PDF at https://idfpr.illinois.gov/dpr/active-license-report.html
- **Data fields:** Full license verification data; CORE includes "Export to CSV" functionality. CSV column schema not publicly documented.
- **Professional Land Surveyor:** Live in CORE since October 30, 2024
- **Update frequency:** Real-time (CORE); PDF reports monthly
- **API:** No public API. CORE uses Illinois ILogin for access. Micropact/OpenEdge platform.
- **Scale:** 1.2M+ licensees across 100+ professions

#### New York — NYSED Office of the Professions
- **Lookup:** https://www.op.nysed.gov (Online Verification Service)
- **Board:** State Board for Engineering, Land Surveying & Geology | Survey@nysed.gov | 518-474-3817
- **Active PLS population:** ~1,098 land surveyors (2020 data — small population relative to state size)
- **Bulk method:** Web form only. FOIL (Freedom of Information Law) request required for bulk data.
- **NY Open Data Portal** (data.ny.gov): May have datasets but none confirmed for NYSED land surveyors.
- **API:** None public.

#### Washington — DOL / BRPELS
- **Lookup:** https://professions.dol.wa.gov/s/license-lookup
- **Board:** https://brpels.wa.gov/
- **Bulk method:** Web form for individual lookup. WA DOL Open Data (data.wa.gov) has a "Professional License Counts" dataset — **aggregate counts by county/profession, not individual records**. Updated March 2026.
- **API:** None documented.
- **Notes:** BRPELS licenses expire on licensee's birthday every 2 years. DNR maintains a Public Land Survey records database (monuments, not surveyor licenses) — separate system, not relevant here.

---

### 3. Additional States with Free/Low-Cost Programmatic Access

These states were not in the 8-state deep dive but surfaced with notable access options:

| State | Method | URL | Notes |
|-------|--------|-----|-------|
| Colorado | **Socrata REST API** | https://data.colorado.gov/resource/7s5z-vewr.json | Free; supports `$where`, `$select`, `$limit`; all professions including Land Surveyor |
| Indiana | **eLicense API** | Indiana Professional Licensing Agency | Designed for B2B credential verification; contact IN PLA directly |
| Massachusetts | **Mass.gov API** | https://www.mass.gov | Explicit engineer/land surveyor license verification endpoint |
| Kentucky | **Searchable roster** | http://elsweb.kyboels.ky.gov/kweb/Searchable-Roster | Public roster; scrapeable |
| Maryland | Web form | https://www.dllr.state.md.us/license/ls/lsverify.shtml | Individual lookup only |

---

### 4. Commercial License Verification APIs

#### Checkr — API-First, Employment-Oriented
- **URL:** https://checkr.com/background-check/professional-license-verification
- **API:** https://checkr.com/our-technology/background-check-api
- **Pricing:** ~**$12/check** (add-on to base screening package)
- **What it verifies:** Active status, good standing, name match via government/regulatory databases
- **Speed:** Most licenses verified instantly
- **Surveyor-specific:** Not highlighted in marketing; primarily oriented toward healthcare and finance regulated roles. Coverage of PLS licenses needs direct confirmation.
- **Best for:** Post-bid operator vetting (not real-time bid eligibility gating at construction volumes)

#### MeshVerify — Specialized for Professional Licenses
- **URL:** https://meshverify.com/
- **Focus:** Professional license verification and business identity — more specialized than Checkr for this use case
- **API:** https://meshverify.com/product-business-entity-verification
- **Pricing:** Not publicly listed; contact required

#### Certn — Broad Coverage, HR-Stack Oriented
- **API:** https://docs.certn.co/api/
- **Pricing:** **$3–$25/check**; low-volume (~< 100/yr) ~$10/check; enterprise ~$24K/yr contracts
- **Coverage:** 200,000+ sources, 150+ countries; more HR/employment-oriented than construction-sector specific
- **Turnaround:** Initiated within 1 business day; depends on source responsiveness (not instant)
- **Integrations:** Workday, Lever, Greenhouse, Workable ATS

#### Sterling (First Advantage) — Enterprise
- **API:** https://apidocs.sterlingcheck.app
- **Notes:** Enterprise-grade; higher implementation overhead. Contact for pricing.

#### EnvZone — Aggregated PE/PLS Directory
- **URL:** https://envzone.com/professional-license-verification/
- **Source:** Claims to aggregate from NCEES and NCARB member board data
- **Coverage:** 900K+ professionals across all 50 states, updated quarterly
- **Access:** Web lookup only; no documented API or commercial data feed

---

### 5. Commercial SaaS Platforms Used by Boards (Not Consumer APIs)

**Thentia Cloud** is used by some state licensing boards (Oklahoma PELS, Arizona BTR, New Mexico SBLPES). Boards on Thentia expose public licensee search, but Thentia does not offer a consumer API — it's regulatory SaaS. Relevant only in that Thentia-hosted boards have consistent UX and data schemas.

**Accela** is used by Michigan LARA (and many municipalities). Accela has a documented REST API, but Michigan has not confirmed public API exposure. Worth checking if Accela's public endpoint is accessible for MI LARA records.

---

### 6. Typical Data Fields Available

| Field | Availability |
|-------|-------------|
| Full name | Universal |
| License number | Universal |
| License type (PLS/RPLS/PS) | Universal |
| Status (active/expired/suspended) | Universal |
| State of licensure | Universal |
| Expiration/renewal date | Most states |
| City | Common |
| Address | Some (MI has it; TX removed it 2023) |
| Email | Rare (MI still includes it) |
| Disciplinary actions | Some states (CA, NY) |
| Specializations/endorsements | Rare |

---

### 7. Build vs. Buy Analysis

At YAK ROBOTICS task volumes (construction survey market, MI/TX/CA primary states):

| Approach | Cost | Coverage | Implementation |
|----------|------|----------|----------------|
| TX CSV + MI report + CA DCA download | **$0** | TX, MI, CA (~3 key states) | 2–3 weeks (state adapter layer) |
| + CO Socrata API | $0 | + CO | +1 day |
| + FL FDACS FOIA (annual) | ~$50/request | + FL | 1-time setup |
| Checkr API (all states) | ~$12/check | All 50 states | 1 week |
| Certn API (all states) | $3–25/check | All 50 states | 1 week |
| State adapter layer + Checkr fallback | Low | All 50 states | 3–4 weeks |

**Recommendation:** State adapter (TX, MI, CA, CO for free) + Checkr/MeshVerify fallback for all other states. This optimizes cost for primary markets while providing coverage for edge cases.

---

## Implications for the Product

### Current Code Gap

`auction/operator_registry.py:116–134` (`set_pls()`): stores operator-submitted PLS info without external verification.

`auction/compliance.py:54–75` (`upload_document()`): marks all compliance docs as `VERIFIED` immediately on upload with the comment "In a production system, this would trigger async verification against external APIs."

The SAM.gov debarment check (`check_sam_exclusion()`) in `compliance.py` is the right architectural pattern — PLS verification should follow it exactly: env var API key gates real vs. WARN mode.

### Required Architecture

```python
def check_pls_license(license_number: str, state: str, name: str) -> dict:
    """Verify PLS license against state source or commercial API.
    
    Routes by state tier:
    - Tier 1 (free): TX (CSV), MI (report), CA (DCA), CO (Socrata)
    - Tier 2 (commercial): Checkr/MeshVerify via PLS_VERIFY_API_KEY
    - Tier 3 (manual): WARN status, human review required
    """
```

---

## Improvement Proposals

### IMP-001: Integrate external PLS license verification API (Checkr or MeshVerify)
Add `check_pls_license()` to `compliance.py` following the `check_sam_exclusion()` pattern. Gate on `PLS_VERIFY_API_KEY` env var. Trigger from `upload_document()` when `doc_type == "pls_license"`. **Effort: medium.**

### IMP-002: Free-tier state adapter for TX, MI, CA, CO
Implement a state-specific verification tier using direct file downloads: TX daily CSV (`pels.texas.gov/roster/rpls_roster.csv`), MI on-demand report (`michigan.gov/lara/...`), CA DCA Open Data, CO Socrata API. No API key required. **Effort: medium.**

### IMP-003: State-tiered PLS verification routing table
Build routing table in `compliance.py`: Tier 1 → free state data, Tier 2 → commercial API, Tier 3 → WARN/manual. Allows incremental rollout and cost optimization. **Effort: medium.**

---

## New Questions Spawned

- **R-006b:** Checkr vs. MeshVerify PLS verification — API schema, cost, and coverage at 100–1000 checks/month
- **R-006c:** California DCA `search.dca.ca.gov` — is there an undocumented JSON endpoint? (browser DevTools investigation)
- **R-006d:** Michigan LARA bulk data format — confirm exact column schema, field names, and whether email is present in Professional Surveyor exports
- **R-007:** Electronic survey seal/stamp regulations by state (now unblocked — depends on R-006)

---

## Sources

- NCEES Records Program: https://ncees.org/ncees-services/records-program/
- NCEES License Verification FAQs: https://help.ncees.org/article/68-license-verification-faqs
- Michigan LARA Verify A License: https://val.apps.lara.state.mi.us/
- Michigan LARA License Lists and Reports: https://www.michigan.gov/lara/bureau-list/bpl/license-lists-and-reports
- Michigan LARA Accela portal: https://aca-prod.accela.com/MILARA/GeneralProperty/PropertyLookUp.aspx?isLicensee=Y&TabName=APO
- Texas TBPELS RPLS Roster: https://pels.texas.gov/roster/rplssearch.html
- Texas TBPELS RPLS CSV: https://pels.texas.gov/roster/rpls_roster.csv
- Texas TBPELS Roster pages: https://pels.texas.gov/roster/ls_rosters.html
- California BPELSG License Lookup: https://www.bpelsg.ca.gov/consumers/lic_lookup.shtml
- California BPELSG License Verification: https://www.bpelsg.ca.gov/licensees/verification.shtml
- California DCA Open Data Portal: https://www.dca.ca.gov/data/index.shtml
- Florida FDACS Professional Surveyors and Mappers: https://www.fdacs.gov/psm
- Florida DBPR MyFloridaLicense: https://www2.myfloridalicense.com
- Florida DBPR Apify scraper (DBPR only, not surveyors): https://apify.com/exclusive_data/dbpr-myfloridalicense/api
- Ohio eLicense Engineers and Surveyors: https://www.elicense.ohio.gov/oh_verifylicense?board=Engineers+and+Surveyors+Board
- Ohio PEPS board: https://peps.ohio.gov
- Illinois IDFPR CORE: https://idfpr.illinois.gov/core.html
- Illinois IDFPR Active License Report: https://idfpr.illinois.gov/dpr/active-license-report.html
- Illinois IDFPR lookup: https://online-dfpr.micropact.com/lookup/licenselookup.aspx
- New York NYSED Office of the Professions: https://www.op.nysed.gov
- Washington DOL License Lookup: https://professions.dol.wa.gov/s/license-lookup
- Washington BRPELS: https://brpels.wa.gov/
- Washington DOL Open Data: https://dol.wa.gov/about/reports-and-data/open-data
- Colorado Information Marketplace (Socrata API): https://data.colorado.gov/Regulations/Professional-and-Occupational-Licenses-in-Colorado/7s5z-vewr/data
- Massachusetts engineer/surveyor license verification: https://www.mass.gov/how-to/request-a-license-verification-or-certified-license-history-document-engineers-and-land-surveyors
- Kentucky BOELS Searchable Roster: http://elsweb.kyboels.ky.gov/kweb/Searchable-Roster
- Maryland DLLR LS Verify: https://www.dllr.state.md.us/license/ls/lsverify.shtml
- OpenGovUS Michigan licenses: https://opengovus.com/michigan-license
- EnvZone PE/PLS directory: https://envzone.com/professional-license-verification/
- Thentia Cloud: https://thentia.com/license-registration-renewals/
- Checkr Professional License Verification: https://checkr.com/background-check/professional-license-verification
- Checkr API: https://checkr.com/our-technology/background-check-api
- MeshVerify: https://meshverify.com/
- Certn Credential Verification: https://certn.co/credential-verification/
- Certn API docs: https://docs.certn.co/api/
- Certn pricing: https://certn.co/us/pricing/
- Sterling API: https://apidocs.sterlingcheck.app
- SAM.gov Exclusions API (existing pattern in codebase): https://open.gsa.gov/api/exclusions-api/
