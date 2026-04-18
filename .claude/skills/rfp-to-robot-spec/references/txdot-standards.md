# TxDOT Survey Standards Reference

Use when processing Texas DOT RFPs or any project referencing TxDOT specifications.

**Sources:**
- TxDOT Survey Manual (ESS), Revised March 2025
- TxDOT UAS Aerial Mapping Specifications
- TxDOT Airborne LiDAR Specifications

## Accuracy Requirements

| Survey Type | Accuracy Standard | ASPRS Equivalent | Notes |
|-------------|-------------------|------------------|-------|
| UAS aerial mapping (design) | ASPRS Class 1 | 2.5cm class | GCP accuracy: TxDOT Level 3 |
| Airborne LiDAR (design) | ASPRS Class 1 | 2.5cm class | 20–25 pts/m² minimum density |
| PS&E surveys | ±0.15 ft RMSEV | 5cm class | Cross-section precision <0.2 ft |
| Schematic surveys | ±1 ft | 33.3cm class | Cross-section precision <1 ft |

## LiDAR Specifications

| Parameter | Value |
|-----------|-------|
| Minimum point density | 20–25 pts/m² |
| GSD (aerial photography) | ≥5 cm for 2D planimetric compilation |
| LAS format | LAS/LAZ 1.4 |
| GCP accuracy | TxDOT Level 3 |
| Ground-truthing | LiDAR ground-truthing report required as deliverable |

## Cross-Section Intervals

| Survey Type | Interval |
|-------------|----------|
| PS&E surveys | 25 ft |
| Schematic surveys | 50 ft |

## Coordinate System

| Zone | EPSG | Key Counties |
|------|------|-------------|
| Texas North | 2275 | Potter (Amarillo), Lubbock |
| Texas North Central | 2276 | Dallas, Tarrant, Collin |
| Texas Central | 2277 | Travis (Austin), Bexar (San Antonio) |
| Texas South Central | 2278 | Harris (Houston) |
| Texas South | 2279 | Cameron, Hidalgo |

- Horizontal datum: NAD83(2011)
- Vertical datum: NAVD88 via GEOID18
- Default `vertical_datum_epsg: 5703`

## CAD Format

TxDOT accepts both MicroStation DGN and AutoCAD DWG per TxDOT CAD Standards. Historically DGN-preferred.

## Regulatory

- UAS operations must comply with TxDOT UAS Flight Operations and User's Manual
- Integrated LiDAR + photogrammetry workflow (both sensors required together for design-grade)
- RPLS (Registered Professional Land Surveyor) required for survey deliverables
- Texas is a high-TAM market (Houston, Dallas-Fort Worth, Austin, San Antonio metro areas)

## Task Spec Defaults for Texas DOT RFPs

```json
{
  "asprs_horizontal_class": "2.5cm",
  "asprs_vertical_class": "2.5cm",
  "usgs_quality_level": "QL1",
  "min_point_density_ppsm": 20,
  "gsd_cm": 5,
  "cross_section_interval_ft": 25,
  "crs_epsg": 2278,
  "vertical_datum_epsg": 5703,
  "deliverables": [
    {"format": "LAS", "version": "1.4", "point_record_format": 6},
    {"format": "DWG", "version": "R2018+"},
    {"format": "GeoTIFF", "version": "1.1"},
    {"format": "PDF", "notes": "LiDAR ground-truthing report"}
  ]
}
```
