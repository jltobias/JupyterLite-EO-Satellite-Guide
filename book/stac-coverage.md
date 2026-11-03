# STAC coverage audit

Metadata audit: **2026-11-03**. Registry: [STAC Index](https://stacindex.org/api/catalogs). **153 listings**, **4,118 documents checked** (including supplementary NASA pages), **958 platform / constellation records** in the explorer.

This is a bounded directory-wide audit, not proof that every EO satellite or asset is represented. STAC also contains aircraft, stations, models and non-Earth observations. Platform identifiers are optional; collection summaries can omit spacecraft. Mission-group and individual-spacecraft records can overlap; the record count is not a count of unique satellites.

Results: {'unavailable': 25, 'partial': 32, 'metadata-checked': 67, 'skipped-access-or-url': 29}. `metadata-checked` means the bounded metadata walk ended without a recorded failure; it does not establish completeness, current operations, data rights, browser access or downloadable assets. `partial` marks errors or queued/depth-limited metadata. Private/protected and credential-bearing URLs are skipped; HTTPS/TLS errors are retained.

The crawler requests at most 100 documents per catalog, up to depth 3, with a 12-second timeout and 6 MB per document. It reads catalog/collection metadata and at most one Item sample per document without a platform summary; it never requests assets. Static trees can contain thousands of unvisited Items. Legacy catalogs and optional platform fields limit extraction. The original 13 teaching records remain, followed by reviewed spacecraft and explicit constellation identifiers. Unknown orbits, instruments and specifications remain explicit.

Download [audit evidence](https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/data/stac-audit.json), [identifier crosswalk](https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/data/stac-coverage.json), [catalog](https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/data/catalog.json), and [semantic graph](https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/data/catalog.jsonld). Endpoint snapshots do not automatically refresh on build.

## Catalog results

| STAC Index listing | Result | Documents | Metadata records |
|---|---|---:|---:|
| [AerialDataset](https://stacindex.org/catalogs/aerialdataset) | unavailable | 0 | 0 |
| [African Agriculture Adaptation Atlas STAC catalog](https://stacindex.org/catalogs/africa-agriculture-adaptation-atlas) | partial | 100 | 89 |
| [Agroforestry Tree Detection — India (STAC layer)](https://stacindex.org/catalogs/agroforestry-tree-detection-india-stac-layer) | metadata-checked | 3 | 2 |
| [Argentina National Geographic Institute (IGN) Reference Layers](https://stacindex.org/catalogs/argentina-ational-geographic-institute) | partial | 100 | 77 |
| [Astraea Earth OnDemand](https://stacindex.org/catalogs/astraea-earth-ondemand) | metadata-checked | 33 | 0 |
| [Boettiger Lab Geospatial Datasets](https://stacindex.org/catalogs/boettiger-lab-geospatial-datasets) | unavailable | 0 | 0 |
| [BON in a Box STAC](https://stacindex.org/catalogs/bon-in-a-box-stac) | metadata-checked | 6 | 35 |
| [Canadian Geospatial Data Collections](https://stacindex.org/catalogs/canadian-geospatial-data-collections-datacube) | metadata-checked | 2 | 52 |
| [Capella Space Open Data](https://stacindex.org/catalogs/capella-space-open-data) | partial | 99 | 93 |
| [Cassini VIMS-IR STAC catalog](https://stacindex.org/catalogs/cassini-vims-ir) | unavailable | 0 | 0 |
| [Monthly Mosaic of Sentinel 2 Images for Catalonia](https://stacindex.org/catalogs/catalonia-monthly-sentinel2) | unavailable | 0 | 0 |
| [CBERS and Amazonia-1 on AWS](https://stacindex.org/catalogs/cbers) | unavailable | 0 | 0 |
| [Copernicus Data Space Ecosystem](https://stacindex.org/catalogs/cdse) | metadata-checked | 44 | 428 |
| [Copernicus Data Space Ecosystem (openEO)](https://stacindex.org/catalogs/cdse-openeo) | skipped-access-or-url | 0 | 0 |
| [CEDA STAC API](https://stacindex.org/catalogs/ceda-stac-api) | skipped-access-or-url | 0 | 0 |
| [CIESIN STAC](https://stacindex.org/catalogs/ciesin-stac) | metadata-checked | 34 | 22 |
| [NASA CMR STAC](https://stacindex.org/catalogs/cmr-stac) | partial | 100 | 56 |
| [CoCliCo STAC Catalog](https://stacindex.org/catalogs/coclico) | metadata-checked | 25 | 24 |
| [CoRE Stack Spatio Temporal Asset Catalog](https://stacindex.org/catalogs/core-stack-spatio-temporal-asset-catalog) | partial | 100 | 98 |
| [CREODIAS](https://stacindex.org/catalogs/creodias) | skipped-access-or-url | 0 | 0 |
| [Cubes and Clouds - Snow Cover](https://stacindex.org/catalogs/cubes-and-clouds-snow-cover) | metadata-checked | 3 | 2 |
| [Cyverse STAC API](https://stacindex.org/catalogs/cyverse-stac-api) | metadata-checked | 2 | 2 |
| [Delineate Anything Boundaries Ukraine 2025](https://stacindex.org/catalogs/da-field-boundaries-ukraine-2025-simplified) | skipped-access-or-url | 0 | 0 |
| [DACCS STAC API - CRIM Hirondelle](https://stacindex.org/catalogs/daccs-stac-crim-hirondelle) | skipped-access-or-url | 0 | 0 |
| [data.geo.admin.ch](https://stacindex.org/catalogs/datageoadminch) | metadata-checked | 7 | 514 |
| [Destination Earth Data Lake (DEDL) API](https://stacindex.org/catalogs/dedl-api) | metadata-checked | 2 | 348 |
| [DestinE Data Lake](https://stacindex.org/catalogs/destine-data-lake) | skipped-access-or-url | 0 | 0 |
| [Digital Earth Africa](https://stacindex.org/catalogs/digital-earth-africa) | partial | 2 | 0 |
| [Digital Earth Australia](https://stacindex.org/catalogs/digital-earth-au) | metadata-checked | 100 | 194 |
| [Digitale Orthophotos Niedersachsen](https://stacindex.org/catalogs/digitale-orthophotos-niedersachsen) | metadata-checked | 3 | 2 |
| [Disaster Data Releases from Planet Labs PBC](https://stacindex.org/catalogs/disaster-data-releases-from-planet-labs-pbc) | metadata-checked | 63 | 45 |
| [Disasters Charter Mapper Catalog](https://stacindex.org/catalogs/disasters-charter-mapper-catalog) | skipped-access-or-url | 0 | 0 |
| [Distributed Renewable Energy (DRE) Atlas](https://stacindex.org/catalogs/dre-atlas) | metadata-checked | 2 | 2 |
| [Earth Data Hub Catalogue](https://stacindex.org/catalogs/earth-data-hub-catalogue) | skipped-access-or-url | 0 | 0 |
| [Earth Genome: Sentinel-2 L2A Temporal Mosaics](https://stacindex.org/catalogs/earth-genome) | metadata-checked | 3 | 19 |
| [Earth Search](https://stacindex.org/catalogs/earth-search) | metadata-checked | 11 | 18 |
| [Earthlab UAS Career Data Catalog](https://stacindex.org/catalogs/earthlab-uas-career-data-catalog) | skipped-access-or-url | 0 | 0 |
| [EasierData](https://stacindex.org/catalogs/easierdata) | unavailable | 0 | 0 |
| [EcoDataCube.eu](https://stacindex.org/catalogs/eco-datacube) | partial | 100 | 99 |
| [EOC EO Products Service](https://stacindex.org/catalogs/eoc-eo-products-service) | partial | 72 | 140 |
| [EODC API (openEO)](https://stacindex.org/catalogs/eodc-openeo) | skipped-access-or-url | 0 | 0 |
| [ERS open data](https://stacindex.org/catalogs/ers-open-data) | metadata-checked | 20 | 19 |
| [ESA Catalog](https://stacindex.org/catalogs/esa-catalog) | unavailable | 0 | 0 |
| [Eurac Research (openEO)](https://stacindex.org/catalogs/eurac-research-openeo) | skipped-access-or-url | 0 | 0 |
| [EuroSAT: Dataset for Land Use and Land Cover Classification](https://stacindex.org/catalogs/eurosat-dataset-for-land-use-and-land-cover) | metadata-checked | 21 | 20 |
| [Extremadura SDI (CICTEX)](https://stacindex.org/catalogs/extremadura-sdi-cictex) | metadata-checked | 39 | 28 |
| [FAIRiCUBE Hub Catalog](https://stacindex.org/catalogs/fairicube-hub-catalog) | unavailable | 0 | 0 |
| [FedEO Clearinghouse](https://stacindex.org/catalogs/fedeo-clearinghouse) | partial | 100 | 126 |
| [fiboa Field Boundaries](https://stacindex.org/catalogs/fiboa) | unavailable | 0 | 0 |
| [FMI ARD Finland](https://stacindex.org/catalogs/fmi-ard-finland) | partial | 100 | 99 |
| [California Forest Observatory](https://stacindex.org/catalogs/forest-observatory) | metadata-checked | 5 | 4 |
| [US GeoPlatform](https://stacindex.org/catalogs/geoplatform-stac-catalog) | partial | 100 | 70 |
| [Geoportal des Kantons Bern](https://stacindex.org/catalogs/geoportal-des-kantons-bern) | unavailable | 0 | 0 |
| [GEP Supersites CSK and CSG data](https://stacindex.org/catalogs/gep-supersites-csk-and-csg-data) | metadata-checked | 18 | 32 |
| [GHSL Population Grids (GHS-POP R2023A)](https://stacindex.org/catalogs/ghsl-population-grids-ghs-pop-r2023a) | metadata-checked | 25 | 24 |
| [GISTDA Drought Index in Thailand](https://stacindex.org/catalogs/gistda-drought-index-in-thailand) | skipped-access-or-url | 0 | 0 |
| [GISTDA Flood disaster in Thailand](https://stacindex.org/catalogs/gistda-flood-disaster-in-thailand) | skipped-access-or-url | 0 | 0 |
| [Google Earth Engine](https://stacindex.org/catalogs/google-earth-engine) | partial | 100 | 0 |
| [Google Earth Engine (openEO)](https://stacindex.org/catalogs/google-earth-engine-openeo) | metadata-checked | 2 | 1057 |
| [HDX HAPI Cloud-Native](https://stacindex.org/catalogs/hdx-hapi-cloud-native) | unavailable | 0 | 0 |
| [Hong Kong CSDI Trial](https://stacindex.org/catalogs/hong-kong-csdi-trial) | metadata-checked | 5 | 4 |
| [HUB Ocean´s Ocean Data Platform Catalog](https://stacindex.org/catalogs/hub-oceans-ocean-data-platform-catalog) | metadata-checked | 1 | 0 |
| [Iconem STAC - 3D Cities, monuments, archeo sites](https://stacindex.org/catalogs/iconem-stac-3d-cities-monuments-archeo-sites) | skipped-access-or-url | 0 | 0 |
| [IDE Facultad de Ciencia y Tecnología UADER](https://stacindex.org/catalogs/ide-facultad-de-ciencia-y-tecnologia-uader) | metadata-checked | 17 | 16 |
| [IGIO STAC](https://stacindex.org/catalogs/igio-stac) | metadata-checked | 2 | 8 |
| [Impact Observatory STAC API](https://stacindex.org/catalogs/impact-observatory-stac-api) | metadata-checked | 2 | 1 |
| [INPE STAC Server](https://stacindex.org/catalogs/inpe-stac-server) | metadata-checked | 81 | 158 |
| [JRC GloFAS Global Flood Hazard Maps](https://stacindex.org/catalogs/jrc-glofas-global-flood-hazard-maps) | metadata-checked | 33 | 32 |
| [KAGIS Katalog](https://stacindex.org/catalogs/kagis-katalog) | unavailable | 0 | 0 |
| [Kentucky From Above SpatioTemporal Asset Catalog](https://stacindex.org/catalogs/kentucky-from-above-spatiotemporal-asset-catalog) | metadata-checked | 2 | 9 |
| [LUCAS ML](https://stacindex.org/catalogs/lucas-ml) | partial | 2 | 0 |
| [MapBiomas Annual Land Cover and Land Use, South America](https://stacindex.org/catalogs/mapbiomas-annual-land-cover-and-land-use) | metadata-checked | 22 | 21 |
| [Markhöjdmodell Nedladdning Lantmäteriet](https://stacindex.org/catalogs/markhojdmodell-nedladdning-lantmateriet) | skipped-access-or-url | 0 | 0 |
| [Maxar ARD Sample Data](https://stacindex.org/catalogs/maxar-ard-sample-data) | unavailable | 0 | 0 |
| [Maxar Open Data Catalog (ARD format)](https://stacindex.org/catalogs/maxar-open-data-catalog-ard-format) | partial | 100 | 99 |
| [mercator gridded earth data](https://stacindex.org/catalogs/mercator) | skipped-access-or-url | 0 | 0 |
| [Microsoft ML Road Detections](https://stacindex.org/catalogs/microsoft-ml-road-detections) | metadata-checked | 2 | 1 |
| [Microsoft Planetary Computer STAC API](https://stacindex.org/catalogs/microsoft-pc) | metadata-checked | 2 | 139 |
| [MideaFind Germany DIY Store Locations](https://stacindex.org/catalogs/mideafind-germany-diy-store-locations) | unavailable | 0 | 0 |
| [MISTEO STAC SERVER](https://stacindex.org/catalogs/misteo-stac-server) | unavailable | 0 | 0 |
| [National geospatial data of the Republic of Moldova](https://stacindex.org/catalogs/moldova-geodata) | skipped-access-or-url | 0 | 0 |
| [MSC GeoMet - GeoMet-OGC-API](https://stacindex.org/catalogs/msc-geomet) | metadata-checked | 87 | 0 |
| [MTD STAC API](https://stacindex.org/catalogs/mtd-stac-api) | unavailable | 0 | 0 |
| [NAIP Aerial Imagery Mosaics](https://stacindex.org/catalogs/naip-aerial-imagery-mosaics) | unavailable | 0 | 0 |
| [NASA CMR CLOUDSTAC Proxy](https://stacindex.org/catalogs/nasa-cmr-cloudstac-proxy) | partial | 100 | 103 |
| [NASA ISERV](https://stacindex.org/catalogs/nasa-iserv) | partial | 2 | 0 |
| [NOAA Climate Data Records](https://stacindex.org/catalogs/noaa-climate-data-records) | metadata-checked | 2 | 1 |
| [New Zealand Coastal Elevation](https://stacindex.org/catalogs/nz-coastal) | partial | 100 | 99 |
| [New Zealand Elevation](https://stacindex.org/catalogs/nz-elevation) | partial | 100 | 99 |
| [New Zealand Imagery](https://stacindex.org/catalogs/nz-imagery) | partial | 100 | 99 |
| [PSL / Mines Paris / OIE / STAC Catalog / Renewable energy datasets ](https://stacindex.org/catalogs/oie-stac-catalog) | metadata-checked | 43 | 50 |
| [Open Data EOSSAT-1](https://stacindex.org/catalogs/open-data-eossat-1) | skipped-access-or-url | 0 | 0 |
| [OpenAerialMap](https://stacindex.org/catalogs/openaerialmap) | metadata-checked | 2 | 4 |
| [OpenAerialMap Example](https://stacindex.org/catalogs/openaerialmap-example) | metadata-checked | 2 | 2 |
| [openEO Platform](https://stacindex.org/catalogs/openeo-platform) | skipped-access-or-url | 0 | 0 |
| [OpenLandMap STAC](https://stacindex.org/catalogs/openlandmap) | partial | 100 | 99 |
| [OpenTopography Raster DEM Data Catalog](https://stacindex.org/catalogs/opentopography) | partial | 100 | 99 |
| [Ortofoto Nedladdning Lantmäteriet](https://stacindex.org/catalogs/ortofoto-nedladdning-lantmateriet) | skipped-access-or-url | 0 | 0 |
| [Open Science Catalog](https://stacindex.org/catalogs/osc) | partial | 100 | 92 |
| [Overture Releases](https://stacindex.org/catalogs/overture) | partial | 100 | 78 |
| [Paituli STAC (Finland)](https://stacindex.org/catalogs/paituli-stac-finland) | partial | 99 | 284 |
| [Pangeo Cloud Data Catalog](https://stacindex.org/catalogs/pangeo) | partial | 100 | 0 |
| [Panoramax](https://stacindex.org/catalogs/panoramax) | partial | 98 | 200 |
| [PDOK APIs and services](https://stacindex.org/catalogs/pdok-apis-and-services) | partial | 100 | 80 |
| [Pergamino SDI: Spatial Data Infrastructure](https://stacindex.org/catalogs/pergamino-sdi-spatial-data-infrastructure) | partial | 100 | 86 |
| [PGC Data Catalog](https://stacindex.org/catalogs/pgc-data-catalog) | unavailable | 0 | 0 |
| [Philadelphia Housing and Land Use](https://stacindex.org/catalogs/philadelphia-housing-and-land-use) | metadata-checked | 11 | 10 |
| [Planet Labs STAC Catalog](https://stacindex.org/catalogs/planet-labs-stac-catalog) | metadata-checked | 64 | 52 |
| [Polar Geospatial Center Data Catalog](https://stacindex.org/catalogs/polar-geospatial-center) | metadata-checked | 15 | 14 |
| [Portolan NL — Cloud-Native Dutch Geodata](https://stacindex.org/catalogs/portolan-nl-cloud-native-dutch-geodata) | metadata-checked | 58 | 35 |
| [Portolan Reference Catalog](https://stacindex.org/catalogs/portolan-reference-catalog) | unavailable | 0 | 0 |
| [PSUP Data](https://stacindex.org/catalogs/psup-data) | skipped-access-or-url | 0 | 0 |
| [RapidAI4EO](https://stacindex.org/catalogs/rapidai4eo-v1) | partial | 100 | 99 |
| [Rosetta OSIRIS Anaglyphs of Comet 67P](https://stacindex.org/catalogs/rosetta-osiris-anaglyphs) | metadata-checked | 43 | 1 |
| [S2 for Ghana](https://stacindex.org/catalogs/s2-for-ghana) | unavailable | 0 | 0 |
| [SEAS Guyane](https://stacindex.org/catalogs/seas-guyane) | skipped-access-or-url | 0 | 0 |
| [Sentinel-1 RTC CONUS](https://stacindex.org/catalogs/sentinel-1-rtc-conus) | metadata-checked | 46 | 1 |
| [Sentinel 3 Level 2+3 on AWS](https://stacindex.org/catalogs/sentinel-3-aws) | metadata-checked | 29 | 0 |
| [Sentinel 5P Level 2 on AWS](https://stacindex.org/catalogs/sentinel-5p-level2-aws) | partial | 64 | 1 |
| [Sentinel Hub](https://stacindex.org/catalogs/sentinel-hub) | skipped-access-or-url | 0 | 0 |
| [SkyServe Mission Data](https://stacindex.org/catalogs/skyserve-mission-data) | skipped-access-or-url | 0 | 0 |
| [Soft Commodity Infrastructure (Brazil)](https://stacindex.org/catalogs/soft-commodity-infrastructure-brazil) | metadata-checked | 2 | 1 |
| [South American Rural Cadastral Boundaries](https://stacindex.org/catalogs/south-american-rural-cadastral-boundaries) | metadata-checked | 4 | 3 |
| [Space2Stats Database](https://stacindex.org/catalogs/space2stats-database) | unavailable | 0 | 0 |
| [SPOT Orthoimages of Canada (2005-2010)](https://stacindex.org/catalogs/spot-orthoimages-canada-2005) | metadata-checked | 18 | 2 |
| [STAC for Data to Science](https://stacindex.org/catalogs/stac-for-data-to-science) | metadata-checked | 7 | 60 |
| [Super-Resolved Sentinel-2 2.5m STAC API](https://stacindex.org/catalogs/super-resolved-sentinel-2-2-5m-stac-api) | unavailable | 0 | 0 |
| [terrabyte STAC API (DLR)](https://stacindex.org/catalogs/terrabyte) | skipped-access-or-url | 0 | 0 |
| [Terrascope](https://stacindex.org/catalogs/terrascope) | skipped-access-or-url | 0 | 0 |
| [The Wildland Almanac - California](https://stacindex.org/catalogs/the-wildland-almanac-california) | metadata-checked | 44 | 42 |
| [The Wildland Almanac - CONUS](https://stacindex.org/catalogs/the-wildland-almanac-conus) | metadata-checked | 36 | 34 |
| [The Wildland Almanac - Treatment Scenarios](https://stacindex.org/catalogs/the-wildland-almanac-treatment-scenarios) | metadata-checked | 14 | 12 |
| [Thünen Earth Observation (ThEO)](https://stacindex.org/catalogs/thunen-earth-observation-theo) | metadata-checked | 3 | 12 |
| [Trazo Field Boundaries of South America](https://stacindex.org/catalogs/trazo-field-boundaries-of-south-america) | metadata-checked | 9 | 7 |
| [TriMet Geospatial Data](https://stacindex.org/catalogs/trimet-geospatial-data) | metadata-checked | 9 | 8 |
| [UK NCEO Analysis Ready Data (ARD)](https://stacindex.org/catalogs/uk-nceo-analysis-ready-data-ard) | unavailable | 0 | 0 |
| [Umbra Open SAR Data](https://stacindex.org/catalogs/umbra-open-sar-data) | partial | 100 | 0 |
| [🇺🇸 United States / Address Data Theme](https://stacindex.org/catalogs/us-address-data-theme) | metadata-checked | 1 | 1 |
| [🇺🇸 United States / Alaska Geospatial Resources](https://stacindex.org/catalogs/us-ak-geospatial-resources) | unavailable | 0 | 0 |
| [🇺🇸 United States / Alabama Geoportal Resources](https://stacindex.org/catalogs/us-al-geoportal-resources) | metadata-checked | 1 | 1 |
| [🇺🇸 United States / California Geospatial Data](https://stacindex.org/catalogs/us-ca-geospatial-resources) | metadata-checked | 1 | 1 |
| [🇺🇸 United States / Cadastre Data Theme](https://stacindex.org/catalogs/us-cadastre-data-theme) | metadata-checked | 1 | 1 |
| [🇺🇸  United States / Disasters Community Data](https://stacindex.org/catalogs/us-disasters-community) | metadata-checked | 1 | 1 |
| [United States : NGDA Transportation Theme Data](https://stacindex.org/catalogs/us-ngda-transportation-theme-data) | metadata-checked | 1 | 1 |
| [USGS 3DEP LiDAR Point Clouds](https://stacindex.org/catalogs/usgs-3dep-lidar) | metadata-checked | 1 | 0 |
| [USGS Astrogeology Provided Analysis Ready Data](https://stacindex.org/catalogs/usgs-astrogeology-ard) | skipped-access-or-url | 0 | 0 |
| [USGS Landsat Collection 2 API](https://stacindex.org/catalogs/usgs-landsat-collection-2-api) | metadata-checked | 2 | 14 |
| [UVT STAC Catalog](https://stacindex.org/catalogs/uvt-stac-catalog) | unavailable | 0 | 0 |
| [VITO (openEO)](https://stacindex.org/catalogs/vito-openeo) | skipped-access-or-url | 0 | 0 |
| [WeatherLayers](https://stacindex.org/catalogs/weatherlayers) | skipped-access-or-url | 0 | 0 |
| [World Bank - Light Every Night](https://stacindex.org/catalogs/world-bank-light-every-night) | partial | 100 | 0 |
| [WorldPop STAC API](https://stacindex.org/catalogs/worldpop-stac-api) | metadata-checked | 2 | 248 |
| [Wyvern Open Data](https://stacindex.org/catalogs/wyvern-open-data) | metadata-checked | 39 | 35 |

## Supplementary NASA cloud summaries

[NASA ALL collection summaries](https://cmr.earthdata.nasa.gov/cloudstac/ALL/collections?limit=100): **40 pages**, **4,000 summaries**, status **partial**. An independent bound of 40 pages applies. More pages remain when partial. These summaries add GPM, SMAP, ICESat, OCO, PACE, SWOT and other identifiers missed by the first walk. Model names, aircraft and stations remain excluded or unresolved rather than becoming satellites. Refresh explicitly with `python scripts/audit_nasa.py --refresh`, then review and run the crosswalk curator. No Items/assets are requested by this supplementary audit.


## Remaining identity work

Identifiers deliberately excluded from the satellite map (ground/aircraft or unresolved): `AC-690A`, `AERIAL PHOTOGRAPHS`, `AEROSONDE`, `AIRCRAFT`, `ALTUS`, `AML`, `ATLAS-1`, `ATLAS-2`, `ATLAS-3`, `Air-based Platform`, `Airplane`, `Alpha`, `Analytical Lab`, `B-200`, `BALLOONS`, `BLING`, `BT-67`, `BUOYS`, `Buoys`, `C-130`, `C-131A`, `C-23 Sherpa`, `CARB MMP`, `CASA-GFED3-V2`, `CASA-GFED3-V3`, `CESM`, `CESSNA 206`, `CESSNA T206H`, `CLIMATE MODELS`, `CLM-LSM`, `CMS-Flux`, `COMPUTERS`, `CONVAIR CV-580`, `Catchment-LSM`, `Convair-580`, `DEM`, `DHC-3`, `DHC-6`, `DLR-Falcon`, `Data Analysis`, `Data Collections`, `ECCO2_Darwin-V3`, `ECMWF`, `ECMWF ERA5`, `Eole Balloons`, `FFDAS-V2`, `FIELD INVESTIGATION`, `FIELD SURVEYS`, `FIXED OBSERVATION STATIONS`, `FLEXPART`, `FOKKER F27`, `Forcing-LSM`, `G-III`, `G-LiHT`, `G-V`, `GEOS`, `GEOS-5`, `GEOS-Chem`, `GEOSTATIONARY SATELLITES`, `GLOBAL HAWK`, `GLPPM`, `GROUND STATIONS`, `GROUND-BASED OBSERVATIONS`, `GULFSTREAM 1000 (695A)`, `HAQES`, `HELICOPTER`, `HU-25A`, `HU-25C`, `IMERG`, `J-31`, `King Air`, `L4_C`, `LABORATORY`, `LANDMET`, `LEARJET`, `LPJ-EOSIM`, `MAPS`, `MERRA-2`, `METEOROLOGICAL STATIONS`, `MIPS`, `MISSION REPORTS`, `MITgcm`, `MODELS`, `MOORINGS`, `Models`, `Mosaic-LSM`, `Multi-sensor Analysis`, `NASA DC-8`, `NASA ELECTRA`, `NASA ER-2`, `NASA MACH-2`, `NASA P-3`, `NASA WB-57F`, `NCAR ELECTRA`, `NCEP-CFSV2`, `NCEP-GFS`, `NOAA Delaware II`, `NOAA Twin Otter`, `NOBM`, `NOT APPLICABLE`, `NRL P-3`, `NSF/NCAR C-130`, `NSF/NCAR GV HIAPER`, `Noah-LSM`, `Noah-MP-LSM`, `OBSERVATION BASED`, `OCEAN PLATFORMS`, `P-3A ORION`, `P-3B`, `PIPER NAVAJO CHIEFTAIN`, `PROTEUS`, `RADIOSONDES`, `REANALYSIS MODELS`, `RM-OBS/PU`, `RQ-4`, `SATELLITES`, `SEAGLIDER`, `SMART-R`, `SMERGE`, `SPACE SHUTTLES`, `SPACELAB-3`, `STILT`, `STREAMFLOW STATION`, `STS-45`, `STS-51B`, `STS-56`, `STS-66`, `Ships`, `Spacelab-3`, `T-39`, `TMPA`, `TRAJ3D`, `TWIN OTTER CIRPAS NPS`, `UAV`, `UC-12B`, `UMD Cessna`, `VIC-LSM`, `Vaisala WXT520`, `WEATHER STATIONS`, `WP-3D ORION`, `WRF`, `modis`, `uav`. Energy-catalog station identifiers are retained in the crosswalk separately. Generic provider instrument arrays are not assigned to every spacecraft in a mixed collection.

## Refresh and review

Run `python scripts/audit_stac.py --refresh` explicitly, review failures and bounds, then `python scripts/curate_stac.py`. The crosswalk code contains the reviewed identity rules. Recheck specific catalogs with `--catalog SLUG`. Inspect the diff before committing, validate, rebuild, and run browser tests. Expand operator-backed orbit/instrument records without replacing unknowns with guesses.
