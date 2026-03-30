# Auction Data Files

## circular_570.xlsx

Real Treasury Circular 570 data — the official list of federally approved surety companies.

**Source:** https://fiscal.treasury.gov/surety-bonds/list-certified-companies.html
**Downloaded:** 2026-03-30
**Contains:** 501 surety companies with NAIC codes, underwriting limits, state licensing, addresses, phone numbers

### Updating

Download the latest version:
```bash
curl -L -o auction/data/circular_570.xlsx \
  "https://fiscal.treasury.gov/system/files/files/surety-bonds/list-certified-companies.xlsx"
```

The file is updated continuously by the Treasury Department. Recommend refreshing weekly.

### What's verified with real data

| Check | Source | Status |
|-------|--------|--------|
| Surety on Circular 570 | fiscal.treasury.gov Excel | Real |
| State licensing | Circular 570 state columns | Real |
| Underwriting limit | Circular 570 limit column | Real |
| Penal sum extraction | Regex from bond text | Automated |
| Bond number extraction | Regex from bond text | Automated |
| PDF text extraction | PyMuPDF | Automated |

### What requires external APIs (not yet available)

| Check | Would need | Status |
|-------|-----------|--------|
| Bond is active (not cancelled) | Surety portal API (Travelers, Liberty Mutual, etc.) | No public API exists |
| Power of Attorney authentic | Surety portal | No public API |
| AM Best rating | AM Best API | Paid subscription ($5K+/yr) |
| SAM.gov entity exclusion | SAM.gov Exclusions API | Free API (key required) |
| Real-time surety status | Individual surety portals | Web forms only, no REST API |
