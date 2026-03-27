# Robot & Sensor Mapping Reference

Load this when determining which robots fulfill specific survey requirements.

## Survey Need → Robot Platform

| Survey Need | Robot Type | Sensor | Platform | Price Range |
|---|---|---|---|---|
| Topographic survey | Aerial drone | LiDAR + RTK-GPS | DJI Matrice 350 RTK + Zenmuse L2 | $150-300/acre |
| Photogrammetry | Aerial drone | High-res camera | DJI Matrice 350 + Zenmuse P1 (45MP) | $100-200/acre |
| Subsurface/GPR | Ground robot | Ground-penetrating radar | Spot + GSSI StructureScan Mini XT | $3,000-6,000/site |
| Bridge under-deck | Inspection drone | Visual + thermal | Flyability ELIOS 3 | $2,000-4,000/structure |
| Bridge visual | Inspection drone | Camera + AI defect | Skydio X10 | $500-1,500/structure |
| 3D scanning | Ground robot | Terrestrial LiDAR | Spot + Leica BLK ARC | $2,000-5,000/structure |
| Progress monitoring | Aerial drone | Camera + optional LiDAR | DJI Matrice 350 / Skydio X10 | $400-1,200/visit |
| Structural inspection | Crawler | Visual + crack detection | Gecko TOKA | $5,000-15,000/structure |
| Environmental | Multi-platform | Water/air/soil sensors | Custom platforms | Varies |
| Pavement condition | Ground vehicle | GPR + profiler | Specialized vehicle | $1,000-3,000/mile |

## Sensor Specifications

### DJI Zenmuse L2 (LiDAR)
- 5 returns per pulse
- ±3-5cm vertical accuracy (with GCPs)
- 150m effective survey AGL (250m max range)
- 240,000 pts/sec

### DJI Zenmuse P1 (Camera)
- 45MP full-frame
- 2.5cm/px GSD at 120m AGL with 35mm lens
- RTK-enabled for direct georeferencing

### Skydio X10
- 50MP wide + 48MP telephoto
- FLIR Boson+ 640×512 thermal
- AI obstacle avoidance, autonomous flight planning
- BVLOS capable (with waiver)

### GSSI StructureScan Mini XT (GPR)
- 1.6 GHz center frequency
- 0.5m depth typical (concrete), 3m soil
- ±2cm positioning with RTK

### Leica BLK ARC (SLAM Scanner)
- Survey-grade SLAM, ±5mm-1cm relative accuracy
- Mounts on Spot for autonomous scanning
- Outputs LAS/LAZ/e57

## Certification Requirements by Task

| Task | Required | Common |
|---|---|---|
| Any aerial | FAA Part 107 | OSHA 10-hr for construction sites |
| Highway survey | Licensed surveyor (state) | MOT certified |
| Bridge inspection | PE + FHWA-NHI-130055 | Confined space (if applicable) |
| BVLOS operations | FAA BVLOS waiver (site-specific) | Insurance $1M+ |
| Underwater | Dive certified | ADCI commercial diver |
