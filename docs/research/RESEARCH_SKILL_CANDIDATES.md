# Skill Candidates: 55 Opportunities Ranked by Value

**Date:** 2026-03-29
**Status:** Research complete. Ready for prioritization review.
**Excludes:** rfp-to-robot-spec, rfp-to-site-recon, bond-verification, legal-terms-compare (already built)

---

## Methodology

Candidates were identified through four complementary passes:

1. **YAML traversal** -- Every node in `PRODUCT_DSL_v2.yaml` was examined for actions that an AI agent or human user performs that could be encapsulated as a repeatable skill. Focus areas: `journeys`, `execution_stack`, `state_machines`, `legal`, `payment_flow`, `capabilities`, `mcp_tools.planned`, `unknowns`, `scoring_profiles`.

2. **Journey stage analysis** -- Each stage of every journey (pre_bid_survey, operator_onboarding, controller_setup, agent_onboarding, recurring_task, reject_recovery, weather_hold, no_robots_available) was checked for gaps where a skill would automate what is currently manual or planned-but-unbuilt.

3. **Gap analysis cross-reference** -- The autonomous execution gaps (Layers 0-5) from `ANALYSIS_AUTONOMOUS_EXECUTION_GAPS.md` each represent at least one skill. The legal framework, payment flow, operator onboarding, and award confirmation research documents surfaced domain-specific skills.

4. **Hard World value filter** -- Per Jay Springett's "Hard Worlds for Little Guys" framework, the best skills promote constraints from advice into physics. They build environmental enforcement into the marketplace so that a solo drone operator (Alex) or a mid-size GC estimator (Marco) gets the same compliance rigor, legal protection, and operational intelligence that a large firm's back office provides. Skills were evaluated on whether they make the marketplace a harder, more legible world -- where actions bind to consequences and small actors can trust the environment.

---

## Ranking Table

| Rank | Skill Name | Description | Category | Persona | YAML Node / Phase | Complexity | Hard World Value |
|------|-----------|-------------|----------|---------|-------------------|------------|-----------------|
| 1 | `task-decomposer` | Decompose a natural-language survey request into parallel/sequential subtasks with sensor routing | USER_JOURNEY | Marco, agent | journey:pre_bid_survey.stages[1], cap:multi_robot_workflows / v2.0 | HIGH | A solo estimator gets the same multi-sensor orchestration that a large firm's survey department provides in-house. |
| 2 | `subcontract-generator` | Auto-generate ConsensusDocs 751 subcontract from task spec + winning bid | USER_JOURNEY | Marco, operator | contract:consensusdocs_751, cap:award_confirmation / v2.0 | HIGH | Small operators get enforceable contracts without paying a construction attorney $3K per agreement. |
| 3 | `coi-parser` | Parse ACORD 25 certificate of insurance PDFs and extract all structured fields | USER_JOURNEY | operator, admin | legal:coi_verification, coi_schema / v2.0 | MEDIUM | Automates insurance verification that large GCs have dedicated compliance staff to perform. |
| 4 | `bid-evaluator` | Score and rank bids using vertical-specific weighted scoring with qualification checks | USER_JOURNEY | Marco, agent | scoring:construction, cap:filter_then_score / v1.5 | MEDIUM | Marco sees the same analytically rigorous bid leveling that BuildingConnected charges enterprise subscriptions for. |
| 5 | `weather-scheduler` | Check NOAA Aviation Weather API against task weather constraints and find flyable windows | USER_JOURNEY | agent, operator | journey:weather_hold, unknown:flight_planning_api / v2.0 | MEDIUM | A one-person drone shop gets automated weather intelligence instead of manually checking forecasts at 5 AM. |
| 6 | `deliverable-validator` | Validate output files (LandXML, DXF, GeoTIFF, LAS) against task spec format and accuracy requirements | USER_JOURNEY | agent, operator | layer:5_deliverable_generation / v2.0 | HIGH | Catches format errors before delivery -- prevents the re-fly that kills a small operator's profit margin. |
| 7 | `pls-license-checker` | Validate PLS license number against state board databases (AZ, NV, NM, MI) | USER_JOURNEY | admin, Marco | legal:pls_licensing / v2.0 | MEDIUM | Automated credential check that replaces calling the state board -- levels the field for operators in multiple states. |
| 8 | `award-review-briefing` | Generate a qualification summary for recommended winner with all automated check results | USER_JOURNEY | Marco, agent | journey:pre_bid_survey.stages[4], cap:award_confirmation / v2.0 | LOW | Marco gets a one-page brief equivalent to what a procurement analyst at a large GC would prepare. |
| 9 | `flight-plan-generator` | Convert boundary polygon + sensor + altitude + overlap into waypoints and estimated duration | USER_JOURNEY | operator, agent | layer:2_mission_planning, mcp_tools.planned:plan_flight / v2.0 | HIGH | Closes the highest-severity execution gap -- without this, every mission needs a human flight planner. |
| 10 | `operator-rate-advisor` | Suggest per-acre pricing based on local market data, equipment tier, and task complexity | USER_JOURNEY | Alex (operator) | supply_side.economics, operator_rates / v2.0 | LOW | Prevents new operators from underpricing (race to bottom) or overpricing (losing bids) -- knowledge that takes years to learn. |
| 11 | `recurring-task-scheduler` | Auto-schedule monthly progress monitoring flights with baseline comparison setup | USER_JOURNEY | Marco, agent | journey:recurring_task / v2.0 | MEDIUM | Turns a one-time win into 14 months of recurring revenue -- automation that only large firms can staff. |
| 12 | `debarment-checker` | Check SAM.gov Entity Management API + state debarment lists for operator eligibility | USER_JOURNEY | admin, Marco | legal:debarment_check / v2.0 | LOW | Federal compliance check that small GCs often skip because they lack a compliance department. |
| 13 | `laanc-filer` | File LAANC authorization via Aloft/DroneUp API for controlled airspace operations | USER_JOURNEY | operator, agent | legal:laanc, mcp_tools.planned:file_laanc / v2.0 | MEDIUM | Automates airspace authorization that experienced operators know by heart but newcomers fumble. |
| 14 | `capture-qc` | In-field quality validation: point density, coverage, GSD, accuracy vs. task spec | USER_JOURNEY | operator, agent | layer:4_infield_qc, mcp_tools.planned:validate_capture / v2.0 | HIGH | Prevents delivering bad data -- the mistake that ends a small operator's reputation on the platform. |
| 15 | `progress-diff-report` | Compare current survey against baseline to produce cut/fill heatmaps and volume tables | USER_JOURNEY | Marco, agent | journey:recurring_task, phase:v2.0 / v2.0 | HIGH | Generates the same monthly progress report that a $200K/yr survey manager would produce internally. |
| 16 | `equipment-qualifier` | Map operator's equipment to eligible task types and sensor capabilities | USER_JOURNEY | Alex (operator) | supply_side.equipment_catalog / v2.0 | LOW | New operator instantly knows what they can bid on without trial-and-error or industry connections. |
| 17 | `rejection-recovery` | Walk ranked bidder list after award rejection, re-run checks, present next candidate | USER_JOURNEY | Marco, agent | journey:reject_recovery, state_machines.award_confirmation / v2.0 | MEDIUM | Implements the DOT-standard reject-and-advance flow that large procurement teams run manually. |
| 18 | `dbe-compliance-tracker` | Track DBE/MBE participation against project goals with MDOT MERS Form 2124A support | USER_JOURNEY | Marco, admin | legal:dbe_tracking / v2.0 | MEDIUM | Automates federal DBE tracking that large GCs have dedicated staff for -- essential for public project bids. |
| 19 | `lien-waiver-generator` | Auto-generate conditional and unconditional lien waivers at payment milestones | USER_JOURNEY | operator, Marco | legal.payment_flow.lien_waiver / v2.5 | MEDIUM | Eliminates the legal document that small operators most often forget, risking payment disputes. |
| 20 | `prompt-payment-monitor` | Track MDOT 10-day payment deadlines with penalty calculation and alerts | USER_JOURNEY | operator, admin | legal.payment_flow.prompt_payment_timers / v2.5 | LOW | Small operators get the same payment enforcement awareness that large firms' AP departments track. |
| 21 | `retainage-tracker` | Track retainage held/released per project with MI 50% completion reduction | USER_JOURNEY | operator, Marco | legal.payment_flow.retainage / v2.5 | LOW | Prevents the retainage disputes that disproportionately hurt small subs with thin cash reserves. |
| 22 | `demand-heatmap-generator` | Aggregate unserved task locations into geographic demand signals for operators | USER_JOURNEY | Alex (operator), admin | journey:no_robots_available, journey:operator_onboarding / v2.0 | MEDIUM | Shows a solo operator exactly where to deploy -- market intelligence that only large fleet companies have. |
| 23 | `rfp-budget-sanity-check` | Compare budget ceiling against area x price-per-acre benchmarks, flag outliers | USER_JOURNEY | Marco, agent | validation_register, supply_side.operator_rates / v1.5 | LOW | Prevents Marco from posting tasks at unrealistic prices -- saves time for both buyer and operators. |
| 24 | `civil3d-export-validator` | Validate LandXML/DXF exports for Civil 3D and HeavyBid import compatibility | USER_JOURNEY | agent, operator | phase:v2.0, layer:5_deliverable_generation / v2.0 | MEDIUM | Ensures deliverables actually import into Marco's tools -- the #1 quality complaint in drone survey. |
| 25 | `operator-onboarding-wizard` | Guide new operator through Part 107, equipment, insurance, pricing setup | USER_JOURNEY | Alex (operator) | journey:operator_onboarding / v2.0 | MEDIUM | Compresses the 10-16 week onboarding timeline by automating the checklist a mentor would provide. |
| 26 | `insurance-expiration-alerter` | Monitor COI expiration dates, send yellow (30-day) and red (7-day) alerts | USER_JOURNEY | operator, admin | pol:coi_expiration_alerts / v1.5 | LOW | Prevents the expired-policy surprise that grounds operators mid-project. |
| 27 | `milepost-geocoder` | Convert DOT milepost references to GPS coordinates and survey area polygons | USER_JOURNEY | agent | journey:pre_bid_survey.stages[1] / v1.5 | LOW | Automates the ADOT/MDOT milepost lookup that experienced estimators do from memory. |
| 28 | `part107-verifier` | Verify FAA Part 107 certificate status via FAA Airmen Inquiry | USER_JOURNEY | admin | legal:faa_part_107 / v1.5 | LOW | Instant credential check that replaces manual FAA database lookups. |
| 29 | `scoring-weight-tuner` | Adjust bid scoring weights per vertical/project type based on historical outcomes | PRODUCT_BUILD | admin | scoring_profiles / v2.0 | MEDIUM | Data-driven scoring refinement that only platforms with dedicated data science teams can do. |
| 30 | `task-spec-schema-gen` | Generate construction task spec schemas from YAML node definitions for validation | PRODUCT_BUILD | admin, agent | architecture.capabilities / v1.5 | LOW | Accelerates building validated task specs from the YAML ontology. |
| 31 | `state-machine-validator` | Verify state transitions in code match YAML-defined state machines | PRODUCT_BUILD | admin | state_machines.task_lifecycle, state_machines.award_confirmation / v1.5 | LOW | Catches state machine drift between documentation and implementation. |
| 32 | `settlement-routing-tester` | Generate test scenarios for all 4 settlement modes with edge cases | PRODUCT_BUILD | admin | architecture.settlement.modes / v1.5 | MEDIUM | Ensures payment code correctness across settlement modes without manual test writing. |
| 33 | `escrow-milestone-manager` | Manage rolling escrow deposits, milestone triggers, and fund releases | USER_JOURNEY | Marco, operator | legal.payment_flow / v2.5 | HIGH | Replaces the escrow management that requires a dedicated project accountant at large firms. |
| 34 | `volumetric-survey-spec` | Generate mining-specific task specs (stockpile, blast, highwall) from site description | USER_JOURNEY | mine surveyor | vertical:mining, phase:v2.5 / v2.5 | MEDIUM | Extends the RFP-to-spec pattern to mining -- a new vertical where small mine surveyors lack procurement tools. |
| 35 | `airspace-conflict-detector` | Detect scheduling conflicts between drone and ground robot operations on same site | USER_JOURNEY | agent | cap:multi_robot_workflows / v2.0 | MEDIUM | Prevents the airspace deconfliction errors that only experienced multi-crew operations avoid. |
| 36 | `operator-revenue-forecaster` | Project monthly revenue based on equipment tier, location, and historical task volume | USER_JOURNEY | Alex (operator) | supply_side.economics / v2.0 | LOW | Gives an independent operator the business planning tools that franchise operations provide. |
| 37 | `rfp-completeness-checker` | Validate that a posted task spec has all required fields for its survey type | PRODUCT_BUILD | agent | skill:rfp_to_robot_spec.validation_scripts / v1.5 | LOW | Catches incomplete specs before they hit the auction -- prevents wasted bid effort. |
| 38 | `gcp-placement-planner` | Determine GCP requirements and optimal placement based on task accuracy needs | USER_JOURNEY | operator | layer:2_mission_planning, unknown:flight_planning_api / v2.0 | MEDIUM | The ground control decision that new operators get wrong and experienced ones do from instinct. |
| 39 | `811-notification-drafter` | Draft utility locate notification for dig/GPR tasks with site coordinates | USER_JOURNEY | operator | layer:0_regulatory / v2.0 | LOW | Automates the 811 call that experienced operators never forget but newcomers often skip. |
| 40 | `bridge-inspection-spec` | Generate NBI-formatted bridge inspection task specs from FHWA requirements | USER_JOURNEY | bridge PM | vertical:infrastructure, phase:v3.0 / v3.0 | HIGH | Opens infrastructure vertical to small inspection firms that lack NBI formatting expertise. |
| 41 | `privacy-task-encryptor` | Encrypt task specs for TEE-based confidential matching (Diane's journey) | USER_JOURNEY | Diane | cap:privacy_tee, phase:v2.0 / v2.0 | HIGH | Enables classified inspections for government buyers without enterprise security infrastructure. |
| 42 | `erc8004-agent-card-builder` | Generate ERC-8004 agent cards with sensor capabilities and pricing from operator profile | USER_JOURNEY | operator | architecture.repos, feature:F-8 / v1.5 | MEDIUM | Automates on-chain identity setup that requires blockchain expertise to do manually. |
| 43 | `commitment-hash-auditor` | Verify task-payment linkage by computing H(request_id, salt) against on-chain memos | PRODUCT_BUILD | admin, regulator | inv:commitment_hash_only, feature:F-4 / v1.5 | LOW | Enables audit without exposing task details -- transparency tool for regulators. |
| 44 | `dot-rfp-analyzer` | Extract structured requirements from DOT RFP documents (MDOT, TxDOT, ADOT formats) | USER_JOURNEY | Marco, agent | executive_summary.sources / v1.5 | MEDIUM | Levels the field: a small GC gets the same RFP analysis that large firms assign to junior PMs. |
| 45 | `eo-tail-coverage-monitor` | Track E&O claims-made policy tail coverage and flag operators at risk | USER_JOURNEY | admin | legal.insurance_requirements.eo_tail_policy / v2.0 | LOW | Catches the insurance gap that exposes the platform to downstream claims years later. |
| 46 | `survey-accuracy-benchmarker` | Compare delivered accuracy against NSSDA/ASPRS standards and task spec requirements | USER_JOURNEY | agent | layer:4_infield_qc / v2.0 | MEDIUM | Objective quality measurement that removes subjective disputes about "good enough" data. |
| 47 | `dtn-message-builder` | Construct idempotent DTN bundle messages for lunar task dispatch and settlement | USER_JOURNEY | Kenji, agent | transfer_map.lunar_task_spec_extensions, feature:F-10 / v4.0 | HIGH | Enables lunar operations for small commercial space companies without NASA-scale ground stations. |
| 48 | `multi-state-license-tracker` | Track PLS licenses across multiple states with CE compliance monitoring | USER_JOURNEY | operator | legal.pls_licensing / v2.0 | LOW | Automates multi-state license management that only large survey firms with admin staff handle well. |
| 49 | `billing-format-generator` | Generate AIA G702/G703 pay applications from task completion data | USER_JOURNEY | operator | legal.payment_flow.billing_format / v2.5 | MEDIUM | Produces the billing documents that large subs have accounting departments to generate. |
| 50 | `site-safety-plan-drafter` | Generate site-specific safety plans from task spec and site recon data | USER_JOURNEY | operator | legal:osha_compliance / v2.0 | MEDIUM | OSHA compliance document that large firms have safety departments for -- a solo operator generates it in minutes. |
| 51 | `remote-id-compliance-checker` | Verify FAA Remote ID module registration for operator drones | USER_JOURNEY | admin | legal:remote_id / v1.5 | LOW | Quick compliance check that prevents regulatory violations before field deployment. |
| 52 | `bet-confidence-updater` | Update bet chain confidence scores based on validation register experiment results | PRODUCT_BUILD | admin | validation_register / ongoing | LOW | Systematic strategy tracking that prevents confirmation bias in product decisions. |
| 53 | `competitive-response-drafter` | Draft competitive response playbook updates when market signals trigger | PRODUCT_BUILD | admin | market.competitive_moats.response_playbook / ongoing | LOW | Strategic monitoring that keeps a small startup aware of competitive moves without a strategy team. |
| 54 | `mining-deliverable-formatter` | Convert survey outputs to MSHA-formatted safety reports and volumetric change reports | USER_JOURNEY | mine surveyor | vertical:mining / v2.5 | MEDIUM | Mining-specific format conversion that small survey firms lack templates for. |
| 55 | `data-ownership-clause-gen` | Generate data ownership and re-use clauses based on task type and project requirements | USER_JOURNEY | Marco, operator | legal.data_ownership / v2.0 | LOW | Prevents the data rights disputes that cost small operators legal fees they cannot afford. |

---

## Detailed Descriptions (Top 20)

### 1. task-decomposer

**Full description:** Takes a natural-language survey request (e.g., "I need topo and subsurface data for SR-89A widening, 12 acres") and decomposes it into structured parallel or sequential subtasks, each with the correct sensor type, accuracy requirements, and deliverable formats. Handles multi-robot coordination: drone morning, Spot afternoon, GPR after topo baseline is established.

**YAML reference:** `journey:pre_bid_survey.stages[1]`, `cap:multi_robot_workflows`, `scoring_profiles`
**Input:** Natural language request + site location + deadline
**Output:** Array of task specs with dependency graph, sensor assignments, schedule constraints
**Why it matters:** This is the core intelligence that makes the agent more than a booking portal. Without it, Marco must know which sensors to request and how to sequence them -- exactly the expertise he is paying for. The skill embodies `bet:agent_mediation_adds_value`.

### 2. subcontract-generator

**Full description:** Auto-generates a ConsensusDocs 751 (short form) subcontract populated from: task spec (scope, accuracy, deliverables, weather constraints), winning bid (price, schedule), operator profile (insurance, licensing), and account-level defaults (data ownership, LOL cap at 1x fee, mutual indemnification). Outputs a PDF ready for digital execution.

**YAML reference:** `contract:consensusdocs_751`, `cap:award_confirmation`, `journey:pre_bid_survey.stages[5]`
**Input:** Task spec + winning bid + operator profile + account defaults
**Output:** Populated subcontract PDF with exhibits
**Why it matters:** Construction contracts are the #1 barrier to fast task execution. Large GCs have in-house legal; small operators sign whatever is put in front of them. This skill ensures balanced terms for both sides.

### 3. coi-parser

**Full description:** Parses uploaded ACORD 25 certificate of insurance PDFs using OCR and field extraction. Extracts: producer info, insurer names with NAIC numbers, policy numbers, effective/expiration dates, coverage types and limits (CGL, E&O, drone/aviation, workers comp, umbrella), additional insured status (ADDL INSD), waiver of subrogation (SUBR WVD). Handles TxDOT Form 1560-CSS variant.

**YAML reference:** `legal:coi_verification`, `legal.insurance_requirements`
**Input:** ACORD 25 PDF (or TxDOT 1560-CSS)
**Output:** Structured insurance record with field-level confidence scores
**Why it matters:** Insurance verification is the trust foundation. Manual COI review takes 15-30 minutes per operator. Automated parsing enables real-time qualification checks at bid time.

### 4. bid-evaluator

**Full description:** Applies vertical-specific scoring weights (construction: price 40%, SLA 25%, confidence 20%, reputation 15%) to a set of bids. Runs hard-constraint filtering first (accuracy capability, insurance minimums, PLS license state, Part 107 currency), then weighted scoring on remaining bids. Produces a ranked list with per-factor scores and a recommendation.

**YAML reference:** `scoring:construction`, `cap:filter_then_score`, `journey:pre_bid_survey.stages[2]`
**Input:** Array of bids + task spec + account-level insurance minimums
**Output:** Ranked bid list with scores, filtered-out bids with reasons, recommended winner
**Why it matters:** Transforms the subjective "who do I know?" into an objective, auditable scoring process. The same rigor that BuildingConnected provides at enterprise pricing.

### 5. weather-scheduler

**Full description:** Queries NOAA Aviation Weather API for task GPS coordinates. Checks wind speed, precipitation, visibility, and temperature against task weather constraints (e.g., max 25 mph wind, no rain, visibility > 3 statute miles). Identifies flyable windows in a 72-hour forecast. Triggers weather holds when conditions breach limits and auto-resume signals when conditions clear and stabilize for 15 minutes.

**YAML reference:** `journey:weather_hold`, state transitions in `state_machines.task_lifecycle`
**Input:** Task GPS coordinates + weather constraints + current/forecast NOAA data
**Output:** Flyable window schedule, hold/resume signals, weather event log
**Why it matters:** Weather is the #1 cause of drone survey delays. Automated monitoring replaces the experienced pilot's intuition about when to fly.

### 6. deliverable-validator

**Full description:** Validates output files against task spec requirements. For LandXML: schema conformance, coordinate system (NAD83/NAVD88), units. For DXF: layer naming conventions (agency-specific), coordinate system, entity types. For GeoTIFF: CRS, resolution matches GSD requirement, band count. For LAS: version, point record format, classification codes, point density vs. spec.

**YAML reference:** `layer:5_deliverable_generation`, Risk 2 in ROADMAP_v4.md
**Input:** Deliverable files + task spec (format requirements, accuracy requirements, coordinate system)
**Output:** Validation report with pass/fail per file, specific errors, suggested fixes
**Why it matters:** "Marco needs LandXML that imports cleanly into Civil 3D." This skill is the quality gate that prevents bad data from reaching the buyer.

### 7. pls-license-checker

**Full description:** Validates a PLS license number against state licensing board databases. Starting states: AZ (Board of Technical Registration), NV (Board of Professional Engineers and Land Surveyors), NM (Board of Licensure), MI (LARA). Checks: license active, not expired, firm Certificate of Authorization valid (MCL 339.2007), continuing education current.

**YAML reference:** `legal.pls_licensing`, `phase:v2.0`
**Input:** PLS license number + state
**Output:** License status (active/expired/suspended), expiration date, firm authorization status, CE compliance
**Why it matters:** PLS stamp is legally required on survey deliverables. Catching an expired license before award prevents legal exposure for the buyer.

### 8. award-review-briefing

**Full description:** Compiles all automated check results (COI verification, PLS validation, Part 107, debarment, DBE status) into a one-page qualification summary for the recommended winner. Includes: bid price, operator profile, equipment details, past project history, and red/yellow/green compliance indicators. Presented to Marco for the confirm/reject decision.

**YAML reference:** `journey:pre_bid_survey.stages[4]`, `cap:award_confirmation`
**Input:** Bid evaluation results + operator profile + automated check outputs
**Output:** Structured briefing document with compliance indicators and recommendation
**Why it matters:** Reduces Marco's review time from 30 minutes to 3 minutes. The same pre-award analysis that a DOT procurement analyst produces.

### 9. flight-plan-generator

**Full description:** Converts a survey boundary polygon, sensor specification, target altitude, and overlap percentage into a complete flight plan with waypoints, flight lines with proper sidelap (60-80%), battery swap points, and takeoff/landing zones. Accounts for terrain elevation, obstacle clearance, and airspace ceiling.

**YAML reference:** `layer:2_mission_planning`, `mcp_tools.planned:plan_flight`, `unknown:flight_planning_api`
**Input:** GeoJSON boundary + sensor ID + altitude AGL + overlap % + terrain data
**Output:** Waypoint array, estimated duration, battery swap plan, coverage map
**Why it matters:** Closes the highest-severity gap in the autonomous execution stack. Without this, a human pilot plans every flight -- the bottleneck that limits scalability.

### 10. operator-rate-advisor

**Full description:** Analyzes local market rates, the operator's equipment tier, task complexity (terrain, acreage, required accuracy), and historical platform pricing to suggest per-acre or day-rate pricing. Shows comparable rates: "Operators in your area with M350+L2 charge $50-$120/acre for LiDAR topo."

**YAML reference:** `supply_side.economics.operator_rates`, common failure mode "Underprice work"
**Input:** Operator equipment profile + task type + geographic area
**Output:** Suggested rate range with market comparisons, min/max guidance
**Why it matters:** Underpricing is the #2 failure mode for drone operators. This skill gives a new operator the pricing intelligence that takes 2 years of experience to develop.

### 11. recurring-task-scheduler

**Full description:** Sets up a recurring task sequence (e.g., monthly progress monitoring for 14 months). Links all tasks to the same project and baseline terrain model. Auto-posts each month's task, collects bids (with loyalty pricing for the previous operator), dispatches, and delivers progress reports formatted for pay applications.

**YAML reference:** `journey:recurring_task`, `cap:recurring_task_automation`
**Input:** Initial completed task + recurrence schedule + baseline deliverable
**Output:** Scheduled task queue with baseline comparison setup
**Why it matters:** One survey win becomes 14 months of recurring revenue. This automation is what turns the marketplace from transactional to relationship-building.

### 12. debarment-checker

**Full description:** Queries SAM.gov Entity Management API (1,000 queries/day) for federal debarment/suspension status. Also checks state-specific debarment lists for AZ, NV, NM, MI. Returns clear/flagged status with details.

**YAML reference:** `legal:debarment_check`, `journey:pre_bid_survey.stages[3]`
**Input:** Operator business name + DUNS/UEI number
**Output:** Federal debarment status + state status + check timestamp
**Why it matters:** A compliance check that small GCs routinely skip. One debarred-operator incident on a federal project can disqualify the GC from future work.

### 13. laanc-filer

**Full description:** Files LAANC authorization via Aloft or DroneUp API. Takes the task boundary polygon, requested max altitude, and date. Checks airspace class, determines if LAANC is needed, and files the request. Returns authorization ID and expiration.

**YAML reference:** `legal:laanc`, `mcp_tools.planned:file_laanc`
**Input:** GeoJSON boundary + max altitude AGL (ft) + date
**Output:** LAANC authorization ID, status, expiration, or denial reason
**Why it matters:** Most urban construction sites fall in controlled airspace. Filing LAANC is routine for experienced operators but a common stumbling block for newcomers.

### 14. capture-qc

**Full description:** Runs quality checks on captured sensor data against task spec requirements: point density (pts/m2), coverage completeness (% of boundary), GSD achieved, accuracy estimate from flight log + GCP residuals. Determines whether the data meets spec or needs re-capture.

**YAML reference:** `layer:4_infield_qc`, `mcp_tools.planned:validate_capture`, `unknown:infield_qc`
**Input:** Captured data path + task spec accuracy requirements
**Output:** QC report with pass/fail, metrics achieved vs. required, re-capture recommendations
**Why it matters:** The difference between "task completed" and "task completed correctly." Without in-field QC, bad data is discovered in post-processing, hours later and miles away.

### 15. progress-diff-report

**Full description:** Compares a current survey against the pre-bid baseline terrain model. Generates cut/fill heatmaps, volumetric summary tables, cross-section comparisons, and schedule conformance overlays. Formats output for attachment to AIA G702/G703 pay applications.

**YAML reference:** `journey:recurring_task`, `phase:v2.0` (progress comparison)
**Input:** Current survey deliverables + baseline terrain model + design model
**Output:** Cut/fill heatmap, volume change table, conformance overlay, pay application attachment
**Why it matters:** Monthly progress reports are what make the marketplace indispensable. This is the deliverable that justifies Marco's subscription-like usage pattern.

### 16. equipment-qualifier

**Full description:** Takes an operator's registered equipment (drone model + sensor) and maps it to eligible task types, accuracy capabilities, and marketplace tier. Shows: "Your M350 + L2 qualifies you for: topo survey, volumetrics, progress monitoring, as-built. Not eligible for: confined-space inspection (needs ELIOS 3)."

**YAML reference:** `supply_side.equipment_catalog`, `journey:operator_onboarding.stages[1]`
**Input:** Equipment model(s)
**Output:** Eligible task types, accuracy specs, marketplace tier, upgrade recommendations
**Why it matters:** Instant clarity on what a new operator can bid on. No more guessing or bidding on tasks their equipment cannot serve.

### 17. rejection-recovery

**Full description:** Implements the DOT-standard reject-and-advance flow. When Marco rejects a recommended winner, the skill walks to the next-ranked bidder, runs the same automated checks (COI, PLS, Part 107, debarment), and presents a new qualification briefing. Tracks rejection reasons for analytics. After all bidders exhausted, offers re-post/skip/withdraw.

**YAML reference:** `journey:reject_recovery`, `state_machines.award_confirmation`
**Input:** Task ID + rejection reason + ranked bidder list
**Output:** Next candidate briefing, or exhaustion options (re-post/skip/withdraw)
**Why it matters:** Fixes the known dead-end UX bug. Without this, a rejection terminates the flow -- broken experience that erodes buyer trust.

### 18. dbe-compliance-tracker

**Full description:** Tracks DBE/MBE/WBE participation against project-level goals for federally-funded projects. Verifies DBE certification against MDOT directory. Monitors actual payments to DBE firms (MERS Form 2124A). Flags when participation falls below goal.

**YAML reference:** `legal:dbe_tracking`, `phase:v2.0`
**Input:** Project DBE goal + operator DBE certification status + payment records
**Output:** DBE compliance report, participation percentage, good-faith-effort documentation
**Why it matters:** DBE compliance is mandatory for federal-aid projects. Small GCs often lose points on this. Automated tracking ensures they meet goals without a dedicated compliance manager.

### 19. lien-waiver-generator

**Full description:** Auto-generates conditional lien waivers (before payment) and unconditional lien waivers (after payment) at each milestone. Tracks waiver status per operator per project. Uses Michigan MCL 570.1101 et seq. forms as templates, with state-variant support.

**YAML reference:** `legal.payment_flow.lien_waiver`, `phase:v2.5`
**Input:** Payment milestone + operator ID + project ID + payment amount
**Output:** Conditional or unconditional lien waiver document, exchange status tracker
**Why it matters:** Lien waivers are legally required for payment closeout. Missed waivers create lien risk. Small operators who forget this step face payment holds.

### 20. prompt-payment-monitor

**Full description:** Tracks payment deadlines per jurisdiction. MDOT: 10 days after receiving owner payment (MCL 125.1561). Federal: 30 days (Prompt Payment Act). Calculates penalties (MI: 1.5%/month). Sends alerts at 5-day and 2-day marks. Generates compliance dashboard.

**YAML reference:** `legal.payment_flow.prompt_payment_timers`
**Input:** Payment event + jurisdiction + statute reference
**Output:** Deadline tracker, penalty calculations, alert schedule
**Why it matters:** Late payment is the #1 cash flow killer for small subs. Automated monitoring gives them the same enforcement awareness that large firms' AP departments provide.

---

## Category Breakdown

| Category | Count | Percentage |
|----------|-------|------------|
| USER_JOURNEY | 46 | 84% |
| PRODUCT_BUILD | 9 | 16% |

### By Roadmap Phase

| Phase | Count | Key Skills |
|-------|-------|------------|
| v1.5 | 10 | task-spec-schema-gen, rfp-budget-sanity-check, milepost-geocoder, part107-verifier, insurance-expiration-alerter, remote-id-compliance-checker, commitment-hash-auditor, state-machine-validator, erc8004-agent-card-builder, settlement-routing-tester |
| v2.0 | 30 | task-decomposer, subcontract-generator, coi-parser, bid-evaluator, weather-scheduler, deliverable-validator, pls-license-checker, award-review-briefing, flight-plan-generator, operator-rate-advisor, recurring-task-scheduler, debarment-checker, laanc-filer, capture-qc, progress-diff-report, equipment-qualifier, rejection-recovery, dbe-compliance-tracker, demand-heatmap-generator, civil3d-export-validator, operator-onboarding-wizard, airspace-conflict-detector, scoring-weight-tuner, gcp-placement-planner, 811-notification-drafter, data-ownership-clause-gen, eo-tail-coverage-monitor, site-safety-plan-drafter, survey-accuracy-benchmarker, privacy-task-encryptor |
| v2.5 | 7 | lien-waiver-generator, prompt-payment-monitor, retainage-tracker, escrow-milestone-manager, volumetric-survey-spec, billing-format-generator, mining-deliverable-formatter |
| v3.0 | 1 | bridge-inspection-spec |
| v4.0 | 1 | dtn-message-builder |
| Ongoing | 2 | bet-confidence-updater, competitive-response-drafter |
| Multi-phase | 4 | operator-revenue-forecaster, multi-state-license-tracker, dot-rfp-analyzer, rfp-completeness-checker |

### By Persona

| Persona | Skills Where Primary Beneficiary |
|---------|--------------------------------|
| Marco (buyer) | 18 |
| Alex / operator | 15 |
| Agent (Claude) | 12 |
| Platform admin | 8 |
| Mine surveyor | 2 |
| Bridge PM | 1 |
| Diane (privacy) | 1 |
| Kenji (lunar) | 1 |
| Regulator | 1 |
| Controller | 1 |

---

## Recommended Build Order

The first 10 skills to build, sequenced for maximum impact and dependency satisfaction:

### Batch 1: Foundation (weeks 1-2) -- v1.5 alignment

| # | Skill | Rationale |
|---|-------|-----------|
| 1 | `milepost-geocoder` | LOW complexity. Unblocks task posting for DOT projects. Agent needs this before decomposition works. |
| 2 | `rfp-budget-sanity-check` | LOW complexity. Prevents bad tasks from entering the auction. Quick win for quality. |
| 3 | `part107-verifier` | LOW complexity. Prerequisite for any operator qualification check. |
| 4 | `insurance-expiration-alerter` | LOW complexity. Immediate value for operator compliance monitoring. |

### Batch 2: Auction Quality (weeks 3-4) -- v1.5/v2.0 bridge

| # | Skill | Rationale |
|---|-------|-----------|
| 5 | `bid-evaluator` | MEDIUM complexity. Core to the auction flow. Scoring is built but vertical-specific tuning and qualification checks need to be a composable skill. |
| 6 | `coi-parser` | MEDIUM complexity. Unlocks automated insurance verification. Prerequisite for award-review-briefing. |
| 7 | `award-review-briefing` | LOW complexity. Depends on bid-evaluator + coi-parser outputs. Completes Marco's happy path. |

### Batch 3: Execution (weeks 5-8) -- v2.0 core

| # | Skill | Rationale |
|---|-------|-----------|
| 8 | `task-decomposer` | HIGH complexity. The single highest-value skill. Unlocks multi-robot workflows and proves `bet:agent_mediation_adds_value`. |
| 9 | `weather-scheduler` | MEDIUM complexity. Required for any real-world flight operation. Enables Journey C (weather hold). |
| 10 | `deliverable-validator` | HIGH complexity. The quality gate that makes the marketplace trustworthy. Without this, bad data reaches Marco. |

**Why this order:** Batches 1-2 complete the v1.5 user journey with low-effort, high-trust skills. Batch 3 tackles the v2.0 capabilities that differentiate the marketplace from a simple booking portal. The sequence respects dependencies (coi-parser before award-review-briefing, milepost-geocoder before task-decomposer) and alternates LOW/MEDIUM/HIGH complexity to maintain momentum.

**Hard World principle applied:** Each batch makes the marketplace environment harder -- more legible, more enforceable, more trustworthy. Batch 1 makes credentials real (not advisory). Batch 2 makes scoring objective (not subjective). Batch 3 makes execution intelligent (not manual). By the end, a solo operator in Tucson and a $180M GC in Phoenix both inhabit a world where actions bind to consequences, contracts are enforceable, and quality is measurable.

### What comes after the first 10

**Batch 4 (weeks 9-12): Operator empowerment** -- `operator-rate-advisor`, `equipment-qualifier`, `operator-onboarding-wizard`, `demand-heatmap-generator`. These four skills directly address Alex's journey and solve the #1 operator failure mode (finding clients). They convert the marketplace from a buyer-first tool into a two-sided platform.

**Batch 5 (weeks 13-16): Legal automation** -- `subcontract-generator`, `pls-license-checker`, `debarment-checker`, `rejection-recovery`. These close the award confirmation flow end-to-end. After Batch 5, the full journey from Marco's request through signed subcontract is automated.

**Batch 6 (weeks 17-20): Payment maturation** -- `lien-waiver-generator`, `prompt-payment-monitor`, `retainage-tracker`, `escrow-milestone-manager`. These implement the payment lifecycle state machine and are prerequisites for the mining expansion (v2.5).

---

## Complexity Distribution

| Complexity | Count | Total Effort (estimated) |
|------------|-------|-------------------------|
| LOW (1-2 days) | 20 | 20-40 days |
| MEDIUM (3-5 days) | 22 | 66-110 days |
| HIGH (1-2 weeks) | 13 | 65-130 days |
| **Total** | **55** | **151-280 days** |

At a pace of 2-3 skills per week (mixing complexities), the full catalog represents roughly 6-9 months of skill development. The recommended build order front-loads impact: the first 10 skills (Batches 1-3, ~8 weeks) cover the core user journey for both Marco and Alex.

---

## Relationship to Hard Worlds Theory

Jay Springett's "Hard Worlds for Little Guys" argues that AI agents become reliable not through better instructions but through hard worlds where constraints are built into the environment as physics rather than communicated as advice. The marketplace skills embody this principle at three levels:

1. **Credential skills** (coi-parser, pls-license-checker, part107-verifier, debarment-checker) promote compliance from "the operator says they have insurance" to "the system has verified their ACORD 25 and the policy is current." This is converting a speed-limit sign into a speed bump.

2. **Quality skills** (capture-qc, deliverable-validator, civil3d-export-validator, survey-accuracy-benchmarker) promote data quality from "the operator says the data is good" to "the system measured point density at 23.4 pts/m2 against a 20 pts/m2 requirement." Consequences become real and measurable.

3. **Contract skills** (subcontract-generator, lien-waiver-generator, data-ownership-clause-gen) promote legal protection from "we should probably have a contract" to "the system generated and both parties digitally signed a ConsensusDocs 751 before work began." The world enforces legal structure.

For the "little guy" -- Alex with his $40K drone setup competing against a 50-person survey firm -- these skills mean the marketplace environment provides the same back-office infrastructure that the large firm built over 20 years: compliance, legal, quality control, pricing intelligence, and payment enforcement. The marketplace is not just a place to find work; it is a hard world that makes both sides trustworthy by design.
