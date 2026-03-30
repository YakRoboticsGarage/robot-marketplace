# Jennifer Chen — PLS Review Checklist (Aerial LiDAR)

## Pre-Review Verification
- [ ] Task specification document received and reviewed
- [ ] Operator credentials verified (Part 107, insurance)
- [ ] GC terms reviewed for accuracy requirements
- [ ] Coordinate system and datum confirmed

## Point Cloud Quality (LAS/LAZ)
- [ ] Point density meets specification (pts/m2)
- [ ] Classification correct (ASPRS Class 2 ground, Class 6 buildings, etc.)
- [ ] No systematic gaps or voids in coverage
- [ ] Noise and outlier points removed
- [ ] Overlap between flight lines within tolerance
- [ ] Point cloud georeferenced to correct datum

## Accuracy Assessment
- [ ] RMSE computed against independent checkpoints
- [ ] Horizontal accuracy meets NSSDA 95% threshold
- [ ] Vertical accuracy meets NSSDA 95% threshold (hard surface)
- [ ] Vertical accuracy meets NSSDA 95% threshold (vegetated)
- [ ] Minimum number of QC checkpoints met
- [ ] Checkpoint distribution covers full project extent

## Coordinate System and Datum
- [ ] Correct state plane zone (Michigan South for SE Michigan projects)
- [ ] NAD83(2011) horizontal datum confirmed
- [ ] NAVD88 vertical datum confirmed
- [ ] GEOID model specified and applied (GEOID18)
- [ ] Units confirmed (US Survey Feet)

## Deliverable Completeness
- [ ] LandXML surface model — correct format, no artifacts
- [ ] DXF planimetric map — correct layers per MDOT standard
- [ ] LAS point cloud — correct ASPRS classification
- [ ] GeoTIFF orthomosaic — correct GSD, no seam artifacts
- [ ] Cross-sections — correct interval, format
- [ ] Metadata — FGDC compliant

## Cross-Section Review
- [ ] Interval matches specification (25-ft or 50-ft)
- [ ] All features captured at cross-section locations
- [ ] Elevation values consistent with surface model
- [ ] Station labeling correct

## Feature Extraction
- [ ] Drainage structures located and attributed
- [ ] Utility indicators mapped
- [ ] Signs, signals, barriers captured
- [ ] Pavement edges and lane lines mapped
- [ ] ADA ramps documented

## Final Certification
- [ ] All checklist items pass or documented exceptions noted
- [ ] Digital PLS seal applied per MCL 339.2007
- [ ] Certification date and license number on all deliverable sheets
- [ ] Signed certification letter generated
