# Technical Co-Founder Critique: Pitch Deck

**Date:** 2026-03-29
**Perspective:** Senior engineer, marketplace platform background, evaluating co-founder role

---

## Is the technical vision credible?

The core loop -- reverse auction for physical robot tasks -- is sound and buildable. I have seen this pattern work for compute (Akash), for labor (Upwork), for freight (Convoy). The construction surveying wedge is narrow enough to actually execute on. The AI-agent-posts-tasks angle is a real differentiator now that MCP is maturing.

What concerns me: the deck presents a system where AI extracts specs from RFPs, decomposes into biddable tasks, operators bid in minutes, and deliverables come back Civil 3D-ready. That is four separate hard problems (NLP extraction, task decomposition, operator matching, deliverable QA) stitched together as if it is one product. Each of those is a startup's worth of work. The pitch needs to be honest about which of those the platform does vs which are manual for now.

## What is actually built vs demo vs marketing?

- **Built:** Auction engine with state machine, scoring, settlement abstraction, Stripe integration, SQLite persistence, MCP tool handlers. ~5,300 LOC of application code, ~3,700 LOC of tests. This is a real backend.
- **Demo:** yakrobot.bid is a static interactive demo site, not a production application. No user auth, no real operator accounts, no actual task execution.
- **Marketing:** "Certified bids in minutes," the 58% cost reduction stat, the 24-hour turnaround -- none of this has been validated with a real transaction. The 43 MDOT RFPs were analyzed by the founder, not processed by the platform.

The gap between "built" and "demo" is normal for pre-seed. The gap between "demo" and what the deck implies is a problem. An investor who clicks yakrobot.bid expecting a working marketplace will feel misled.

## Is the lunar vision inspiring or a distraction?

It is a distraction at this stage. For a seed deck, "Year 4: Lunar" signals that the founder is more excited about the moonshot than the grind of selling to Michigan GCs. The founder's own feedback already flags this. I would cut it entirely from the pitch and save it for the "what could this become" conversation after you have revenue.

The deeper issue: lunar operations require a fundamentally different trust model (no human oversight loop), different latency constraints (seconds of signal delay), and different regulatory regime. "Same sensors, same workflows" is not true. It is a different company.

## What technical risks are understated?

1. **Cold start / chicken-and-egg.** The deck skips this entirely. Who bids on the first task? You need operators on the platform before any GC will use it, and operators will not join until there are tasks. The Michigan family connections might solve this, but the deck should address it.
2. **Deliverable quality assurance.** The platform promises "Civil 3D-ready deliverables" but has no data processing pipeline. LiDAR point clouds do not turn into LandXML terrain models automatically. Who does the photogrammetry? Who does the QA? This is where most drone survey startups actually die.
3. **PLS stamp requirement.** Construction surveys in Michigan require a Professional Land Surveyor stamp. The deck mentions "PLS-affiliated" operators but does not explain how a marketplace handles licensed professional liability. This is a legal and insurance problem, not a tech problem, and it could kill the business model.
4. **12% take rate at $72K task size.** An $8,640 platform fee on a single job invites disintermediation after the first successful match. Marketplaces at this price point need lock-in (escrow, insurance, recurring relationships) that is not built yet.
5. **On-chain settlement is premature.** No GC or drone operator is asking for USDC payments. Building crypto rails before you have 10 paying customers is resume-driven development. Ship Stripe, get revenue, add crypto when someone asks for it.

## Would I join?

Not yet. But I am interested. Here is what I would need to see:

- **One completed transaction.** Pay a real operator to fly a real site for a real GC. Even if you broker it manually. Prove the unit economics with a spreadsheet before building the platform.
- **Drop the crypto and lunar from the near-term plan.** Focus the v1.5 sprint entirely on: auth, operator onboarding, one task type (aerial topo), Stripe checkout, and a deliverable upload flow.
- **A conversation with 3 GCs.** Not "identified" -- actually talked to. What did they say? Would they pay? What did they object to?
- **Founder-market fit evidence.** The "family ties in Michigan construction" line needs to be a story, not a bullet point. Who exactly? What is the relationship? Can they get you in the door at one of those 15 GCs next week?

The research depth is genuinely impressive. 40+ docs and a 2,617-line product ontology shows serious thinking. But research is not traction. The next step is not more code -- it is one real customer saying yes.
