# YAK ROBOTICS — Robot Task Auction Marketplace

A marketplace where AI agents post construction survey tasks, certified robot operators bid autonomously, and the best one delivers. Starting with construction site surveying, scaling to mining, infrastructure, and lunar operations.

**Live demo:** [yakrobot.bid/demo](https://yakrobot.bid/demo/) — 100 robots across 18 Michigan operators, 9 RFP presets, EAS attestation, geographic filtering

## The Problem

Construction survey scheduling is a 2-3 week bottleneck costing GCs missed bids. 368,000+ Part 107 holders own survey drones but lack a demand pipeline. No platform exists where AI agents post physical-world tasks and robots bid autonomously.

## The Product

Upload an RFP → the system extracts survey requirements → decomposes into independently biddable tasks → certified operators bid → you review winners with automated compliance checks → sign and activate → get survey deliverables.

## Project Structure

```
yakrover-marketplace/
│
├── auction/                     # Core auction engine (Python)
│   ├── core.py                  # Task, Bid, scoring, signing, haversine geo filter
│   ├── engine.py                # AuctionEngine — state machine, geo + busy filtering
│   ├── mcp_tools.py             # 37 MCP tool handlers
│   ├── delivery_schemas.py      # 8 category-specific QA schemas
│   ├── mcp_robot_adapter.py     # Bridges marketplace to robot MCP servers
│   ├── deliverable_qa.py        # Schema-driven delivery validation
│   └── tests/                   # Unit + integration tests
│
├── demo/                        # Live sites (published via here.now)
│   ├── marketplace/             # yakrobot.bid/demo — auction demo
│   ├── landing/                 # yakrobot.bid — landing page
│   └── explorer/                # yakrobot.bid/yaml — ontology browser
│
├── infra/                       # Deployment configs
│   ├── fleet/                   # Fleet MCP server (Fly.io)
│   ├── fleet-sim/               # 9 category simulator servers (Fly.io)
│   └── deploy/                  # Tunnel + deployment scripts
│
├── data/                        # Static data
│   ├── fleet_manifest.yaml      # 100-robot fleet database
│   └── sample_certs/            # FAA Part 107, ACORD 25, PLS, OSHA samples
│
├── scripts/                     # CLI tools
│   ├── register_fleet.py        # Batch robot registration on-chain
│   ├── eas_attest.py            # EAS attestation management
│   └── deploy-demo.sh           # Demo site deployment
│
├── chatbot/                     # Cloudflare Worker (payment + demo proxy)
├── docs/                        # Documentation
│   ├── architecture/            # 22 technical design docs + implementation plans
│   ├── research/                # 55 research docs + PRODUCT_DSL ontology + backlog
│   ├── feedback/                # Product feedback synthesis
│   ├── guides/                  # Getting started, operator onboarding
│   └── archive/                 # Historical versions
│
├── mcp_server.py                # MCP API server entry point
├── Dockerfile, fly.toml         # Marketplace deployment (Fly.io)
└── pyproject.toml               # Dependencies, ruff, mypy config
```

## Quick Start

```bash
# Clone and install
git clone https://github.com/YakRoboticsGarage/yakrover-marketplace.git
cd yakrover-marketplace && uv sync --all-extras

# Run tests
uv run pytest auction/tests/ -q --tb=short

# Run the demo auction
PYTHONPATH=. uv run python auction/demo.py

# Connect as MCP server
claude mcp add-json yakrover '{"type":"http","url":"http://localhost:8001/fleet/mcp"}'
```

See [Getting Started](docs/guides/GETTING_STARTED.md) for full setup including Stripe and robot simulator.

## Key Documents

| # | Document | What it tells you |
|---|----------|-------------------|
| 1 | **[PRODUCT_DSL_v2.yaml](docs/research/PRODUCT_DSL_v2.yaml)** | The entire product in one file — vision, bets, users, architecture, market, legal, roadmap |
| 2 | **[Roadmap v4](docs/ROADMAP_v4.md)** | Construction → Mining → Infrastructure → Lunar |
| 3 | **[Decisions](docs/DECISIONS.md)** | Every product and technical decision with rationale |
| 4 | **[Fleet Plan](docs/PLAN_100_ROBOT_FLEET.md)** | 100-robot demo fleet: registration, attestation, testing |
| 5 | **[Architecture](docs/architecture/)** | 22 system design docs, implementation plans, tech assessments |
| 6 | **[Improvement Backlog](docs/research/IMPROVEMENT_BACKLOG.yaml)** | 63 tracked items with status and priority |

## Live Sites

| URL | What it is |
|-----|-----------|
| **[yakrobot.bid/demo](https://yakrobot.bid/demo/)** | Live auction — 100 robots, 9 RFP presets, EAS attestation, 3-method payment |
| **[yakrobot.bid](https://yakrobot.bid)** | Landing page — MDOT I-94 RFQ walkthrough |
| **[yakrobot.bid/yaml](https://yakrobot.bid/yaml)** | YAML ontology explorer |

## Key Numbers

- **37 MCP tools** — auction lifecycle, RFP parsing, operator registration, compliance, EAS attestation
- **100 test robots** on Base Sepolia — 18 Michigan operators, 14 real commercial models (DJI M350, Skydio X10, Spot, WingtraOne, ELIOS 3, Autel EVO, Anzu Raptor, IF1200)
- **9 category MCP servers** on Fly.io — aerial LiDAR, photo, thermal, GPR, bridge, corridor, tunnel, confined, env sensing
- **101 EAS attestations** — 100 demo_fleet (Base Sepolia) + 1 live_production Tumbller (Base mainnet)
- **Geographic filtering** — haversine hard cutoff, robots only bid within service radius
- **Busy state** — winning robot excluded for task-type-specific duration (15s to 2hr)
- **9 RFP presets** — real Michigan projects (MDOT I-94, MSU Farm Lane, US-31 bridge, Huntington Place)
- **3-method payment** — Card, Bank Transfer (ACH), Stablecoin (USDC on Base)
- **CI pipeline** — ruff (security linting), mypy, pytest on every push

## Related Repositories

| Repository | What it contains |
|-----------|-----------------|
| **[robotTAM](https://github.com/rafaeldavid/robotTAM)** | Business strategy — pitch, outreach, financial model, founder notes |
| **[yakrover-8004-mcp](https://github.com/YakRoboticsGarage/yakrover-8004-mcp)** | Robot framework — MCP servers, ERC-8004 discovery, robot plugins |

## License

Apache 2.0
