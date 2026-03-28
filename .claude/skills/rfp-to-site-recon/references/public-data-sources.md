# Public Data Sources for Site Reconnaissance

Each source listed with: what it provides, coverage, access method, and limitations.

## Airspace

### FAA UAS Facility Map (LAANC)
- **Provides:** Airspace class, max AGL per 1nm grid cell, LAANC authorization zones
- **Coverage:** Entire US controlled airspace
- **Access:** https://faa.maps.arcgis.com/apps/webappviewer/ (interactive) or LAANC API via providers (Aloft, DroneUp, Airmap)
- **Limitations:** Does not include temporary restrictions; check NOTAMs separately

### FAA Digital Obstacle File (DOF)
- **Provides:** Towers, antennas, power lines, buildings >200ft AGL, cranes
- **Coverage:** All FAA-registered obstacles in US
- **Access:** https://tod.faa.gov/tod/public/TOD_National.xlsx (bulk download) or ArcGIS feature service
- **Limitations:** Voluntary reporting below 200ft; does not include trees, temporary cranes

### FAA NOTAM System
- **Provides:** Active TFRs, airspace closures, temporary obstacles
- **Access:** https://notams.aim.faa.gov/ or via FNS NOTAM API
- **Check:** Day-of-flight, not during planning (NOTAMs change daily)

## Site Geometry

### County GIS / Parcel Data
- **Provides:** Property boundaries, parcel polygons, ownership, zoning
- **Coverage:** Varies by county; most urban counties have public GIS portals
- **Access:** Search "[county name] GIS" or "[county name] property map"
- **Michigan:** https://gis-michigan.opendata.arcgis.com/
- **Texas:** https://tnris.org/ (Texas Natural Resources Information System)
- **National:** https://geocoding.geo.census.gov/ for parcel lookup

### USGS 3DEP / National Map
- **Provides:** Existing LiDAR coverage, elevation models (DEM), terrain slope
- **Coverage:** ~85% of CONUS (as of 2025)
- **Access:** https://apps.nationalmap.gov/downloader/ or https://usgs.entwine.io/
- **Resolution:** QL2 (2 pts/m²) in most areas; QL1 in some corridors
- **Use:** Baseline terrain data; compare new survey against existing

### NAIP Imagery
- **Provides:** Recent aerial photography (60cm-1m resolution)
- **Coverage:** Entire CONUS, refreshed every 2-4 years
- **Access:** https://naip-usdaonline.hub.arcgis.com/
- **Use:** Pre-flight site familiarization, obstacle identification

### Google Earth / Satellite
- **Provides:** Recent high-res imagery, 3D terrain, historical imagery timeline
- **Access:** Google Earth Pro (free) or Google Earth Engine API
- **Limitations:** Not survey-grade; imagery may be 6-18 months old
- **Use:** Visual site assessment, identify structures, vegetation, access routes

## Transportation

### HPMS (Highway Performance Monitoring System)
- **Provides:** Road classifications, AADT (traffic volumes), lane counts, speed limits
- **Coverage:** All federal-aid highways in US
- **Access:** https://hpms.fhwa.dot.gov/ or state DOT open data portals
- **Use:** Assess traffic control needs, identify active roadways

### National Bridge Inventory (NBI)
- **Provides:** Bridge locations, condition ratings (0-9), inspection dates, span lengths, clearances
- **Coverage:** All bridges >20ft on public roads
- **Access:** https://www.fhwa.dot.gov/bridge/nbi/ascii.cfm (bulk CSV)
- **Use:** Pre-bid condition context for bridge inspection tasks

### National Tunnel Inventory (NTI)
- **Provides:** Tunnel locations, dimensions, condition ratings
- **Access:** https://www.fhwa.dot.gov/bridge/tunnel/inventoryguide.cfm

## Environmental

### FEMA Flood Maps (NFHL)
- **Provides:** Flood zones, base flood elevations, floodway boundaries
- **Access:** https://msc.fema.gov/portal/home (interactive) or WMS/WFS services
- **Use:** Identify flood risk for equipment staging; some surveys require flood zone mapping

### National Wetlands Inventory (NWI)
- **Provides:** Wetland boundaries, classifications
- **Access:** https://fwsprimary.wim.usgs.gov/wetlands/apps/wetlands-mapper/
- **Use:** Flag wetland areas that may require permits or avoidance

### NPDES / State Environmental
- **Provides:** Discharge permits, contaminated sites, regulated areas
- **Access:** Varies by state; EPA ECHO: https://echo.epa.gov/

## Utilities

### State 811 / One-Call
- **Provides:** Utility locate notification requirement and contacts
- **Coverage:** All US states (mandatory before excavation/ground disturbance)
- **Access by state:**
  - Michigan: https://missdig811.org (Miss Dig 811)
  - Texas: https://www.texas811.org
  - National: https://call811.com
- **Lead time:** Typically 48-72 hours for locate marks
- **Use:** Required before GPR survey to cross-reference located utilities

### FCC Antenna Structure Registration
- **Provides:** Registered antenna/tower locations, heights, ownership
- **Access:** https://www.fcc.gov/antenna-structure-registration-asr-registration
- **Use:** Obstacle avoidance for drone operations

## Weather

### NOAA Climate Normals
- **Provides:** 30-year average temperature, precipitation, wind by month and station
- **Access:** https://www.ncei.noaa.gov/access/us-climate-normals/
- **Use:** Plan survey window for optimal weather; assess seasonal constraints

### Iowa Environmental Mesonet (IEM)
- **Provides:** Historical hourly wind speed, gust, direction for ASOS/AWOS stations
- **Access:** https://mesonet.agron.iastate.edu/
- **Use:** Calculate P90 wind speed for drone mission planning; assess fly/no-fly probability

### NOAA Aviation Weather (AWC)
- **Provides:** METARs, TAFs, pilot reports, SIGMETs
- **Access:** https://aviationweather.gov/
- **Check:** Day-of-flight for ceiling, visibility, wind

## Soil and Geology

### USDA Web Soil Survey
- **Provides:** Soil types, bearing capacity indicators, depth to bedrock, water table depth
- **Access:** https://websoilsurvey.nrcs.usda.gov/
- **Use:** GPR signal attenuation depends on soil moisture and clay content; plan scan depth expectations

### USGS Geologic Maps
- **Provides:** Bedrock geology, surficial deposits
- **Access:** https://ngmdb.usgs.gov/mapview/
- **Use:** Subsurface context for GPR interpretation
