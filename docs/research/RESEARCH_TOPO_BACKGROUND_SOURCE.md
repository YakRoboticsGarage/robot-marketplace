# Research: Topographic Background Watermark Source Data

**Date:** 2026-03-29
**Purpose:** Find real, public-domain topographic/survey data for a subtle SVG watermark on the marketplace site.

---

## Best Source: USGS NED 1/3 Arc-Second Contours for Detroit W, Michigan

**Direct download (Shapefile ZIP, ~100 MB):**
https://prd-tnm.s3.amazonaws.com/StagedProducts/Contours/Shape/ELEV_Detroit_W_MI_1X1_Shape.zip

**Catalog page:** https://www.sciencebase.gov/catalog/item/5a68b48ee4b06e28e9c7067d

This is a vector shapefile of real contour lines (feet above sea level, NAVD88) derived
from the USGS 3D Elevation Program. It covers the 1x1 degree tile that includes the
I-94 corridor through Detroit and Wayne County. Contour intervals are available at
multiple levels (10 ft, 20 ft, etc.).

**License: Public domain.** Per 17 USC 105, USGS-authored data are U.S. public domain.
No permission needed, just credit "USGS" as source.
- https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits

## Alternative Sources

### USGS topoView - Historical Topo Maps
- **URL:** https://ngmdb.usgs.gov/topoview/viewer/#12/42.3500/-83.1000
- Download 7.5-minute quad sheets for Detroit as GeoTIFF or JPEG (free).
- Good for tracing contour aesthetics from classic USGS cartography.
- Public domain (all USGS topo maps except certain 2010-2016 road overlays).

### OpenTopography - SRTM Contour Generation
- **URL:** https://portal.opentopography.org/raster?opentopoID=OTSRTM.082015.4326.1
- On-demand contour generation from SRTM 30m DEM for any bounding box.
- Output: Shapefile, DXF, or GeoPackage. Public domain (NASA/USGS).

### USGS National Map Contour WMS
- **URL:** https://carto.nationalmap.gov/arcgis/rest/services/contours/MapServer
- Live map service; can export a PNG/SVG of contour lines for any area.
- Useful for quick visual reference before downloading full shapefiles.

### MDOT I-94 Modernization Project
- **Project site:** https://i94detroit.org/
- **MDOT page:** https://www.michigan.gov/mdot/projects-studies/studies/environmentally-cleared-projects/i-94-modernization-detroit
- DSEIS and NAC presentations are public but contain copyrighted engineering drawings.
- **Not recommended for direct use** -- government contractor work may carry restrictions.
- Standard Plans (https://mdotjboss.state.mi.us/stdplan/standardPlansHome.htm) are public
  but show construction details, not topography.

## Conversion Pipeline: Shapefile to SVG Watermark

1. **Download** the USGS Detroit W contour shapefile (link above).
2. **Open in QGIS** (free). Filter to the I-94 corridor bounding box:
   - Approx bounds: lat 42.30-42.38, lon -83.20 to -83.00
3. **Simplify geometry** (Vector > Geometry Tools > Simplify) to reduce vertex count.
   Target ~500-1000 vertices total for a lightweight SVG.
4. **Export as SVG** via Print Layout (Project > New Print Layout > Export as SVG).
   Alternatively, export as GeoJSON and convert with `ogr2ogr` + a script.
5. **Style for watermark use:**
   - Stroke: single color (e.g., `#94a3b8` slate-300), width 0.3-0.5px
   - No fill, no labels
   - Add a few "+" crosshair markers at grid intersections for survey feel
   - Final SVG should be ~5-15 KB
6. **Apply in CSS** as `background-image` at 3-5% opacity, `background-size: 800px`,
   with `background-repeat: repeat`.

## Recommended Approach

Use the **USGS NED contour shapefile** as the primary source. It gives real elevation
data for the exact I-94/Detroit corridor. The contour lines will be authentic -- anyone
in the survey industry who looks closely will recognize real Michigan terrain at ~580-620
ft elevation with the gentle grade toward the Detroit River.

For the quickest path, use the **USGS contour MapServer** to export a small PNG of the
area, then auto-trace it in Inkscape (Path > Trace Bitmap) and clean up manually.
