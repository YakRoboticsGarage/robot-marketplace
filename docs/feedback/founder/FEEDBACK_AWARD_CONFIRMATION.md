# Feedback: Award Confirmation Step Between Winning Bid and Work Start

**Date:** 2026-03-28
**Source:** Founder
**Context:** Currently the demo goes directly from "auction winner selected" to "awarded." In reality, the hiring org needs to review the winning bid before confirming the award — checking for conflicts, verifying qualifications, and making a human decision.

## The Gap

The current flow:
1. Bids come in → scored → winner selected automatically → AWARDED → work starts

What should happen:
1. Bids come in → scored → **recommended winner** presented
2. Hiring org reviews: operator qualifications, insurance, conflicts, price
3. Hiring org **confirms award** (or rejects and picks another bidder)
4. Agreement auto-generated → signed → work starts

## Why This Matters

- A GC might reject a winning bidder due to:
  - Prior bad experience (not in the system)
  - Conflict of interest (operator also works for a competitor)
  - Insurance limits insufficient for this specific project
  - DBE/MBE requirements not met (common on public DOT projects)
  - The GC's client (MDOT) has a prohibited vendor list
  - The operator's PLS isn't licensed in the right state

- This is standard in construction procurement — even in low-bid environments, there's a "responsive and responsible" check after bid opening

## Research Needed

1. How does the "responsive and responsible" check work on DOT projects?
2. What's the typical review period between bid opening and award?
3. What automated checks can the marketplace do vs. what requires human judgment?
4. How do existing platforms (Upwork, Thumbtack, AWS Marketplace) handle post-bid review?
5. DBE/MBE requirements on federally-funded projects — how does this affect award?
