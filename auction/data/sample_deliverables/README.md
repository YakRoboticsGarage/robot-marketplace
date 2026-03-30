# Sample Survey Deliverables

Structurally valid sample files representing real construction survey outputs.
Used by mock fleet robots during end-to-end scenario testing.

| File | Format | Represents |
|------|--------|-----------|
| landxml_surface.xml | LandXML 1.2 | TIN surface from aerial LiDAR topo survey |
| cross_sections.csv | CSV | Cross-sections at 50-ft intervals (MDOT 104.09) |
| survey_control.csv | CSV | Control points (NAD83/NAVD88) |
| accuracy_report.json | JSON | NSSDA accuracy statement with PLS certification |
| tunnel_scan_report.json | JSON | Tunnel 3D scan delivery with structural findings |
| gpr_utility_report.json | JSON | GPR subsurface utility detection (ASCE 38) |

All coordinates are near Kalamazoo, MI (42.29, -85.59) in Michigan State Plane South.
