# Mission inventory and family coverage

Snapshot: **2026-11-03**. The explorer combines **958 mission/platform records** with **all 789 records** from the [CEOS All-status mission table](https://database.eohandbook.com/database/missiontable.aspx) and the saved [STAC audit](stac-coverage.md). Every CEOS permanent identifier is accounted for in the [mission crosswalk](https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/data/mission-coverage.json).

The default **All matching records** map displays every matching record at once. **Mission family** starts a fresh view of all Sentinels, Landsats, or NOAA and partners; it clears other filters and the research question. Search accepts punctuation variants such as `Sentinel 5` and `Sentinel-5`. **Locate a mission** selects a named record, reveals its table page and opens its evidence. Hover/focus a small overview mark to reveal its table row. Large marks identify the current 13 table rows. Choose **Table page** for 13 larger, labeled symbols. Both views retain fullscreen, pins, orbit colors and linked brushing.

## What the count means

These are registry records, not a count of unique spacecraft now in orbit. CEOS includes completed, operational, commissioning, approved, planned, considered and cancelled missions; STAC adds mission groups and commercial identifiers. Some records describe multi-spacecraft missions or hosted instruments. Generic registry entries retain the type `MissionRecord` until platform identity is reviewed. Forecast dates, expected end of life, nominal repeat and intended orbit do not establish flight, usable observations or a data service.

The full checked-in [CEOS factual snapshot](https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/data/mission-registry.json) records the source selection, response hash, original mission IDs, payload links and nominal orbit fields. CEOS is an agency-survey registry; [its documentation](https://database.eohandbook.com/about.aspx) says agency information takes precedence. This union substantially broadens coverage, but cannot certify every private, newly launched or unreported EO spacecraft worldwide.

## Hosted Sentinel missions

[EUMETSAT](https://www.eumetsat.int/our-satellites/sentinel-series) distinguishes dedicated Sentinel spacecraft from hosted Sentinel-4 and Sentinel-5 instruments. Sentinel-4A is represented on **Meteosat-13 / MTG-S1**; Sentinel-4B on **MTG-S2**. Sentinel-5A/B/C are represented on **Metop-SG A1/A2/A3**. Sentinel-5P is a separate spacecraft. Host and payload source identifiers map to the same physical host record, with explicit hosted-mission links in the ontology. Planned hosts retain planned labels.

The NO2 profile now also highlights the Sentinel-4A and Sentinel-5A hosts using [Sentinel-4](https://www.eumetsat.int/sentinel-4) and [Sentinel-5](https://www.eumetsat.int/sentinel-5) operator evidence. Their operator documentation routes are separate from the three verified STAC NO2 routes; a Sentinel-5P collection must not be substituted for Sentinel-5 data. Geometry presets are not inferred for the newly added hosts.

## Family rosters

Family membership includes archive and future records. The NOAA view includes missions with NOAA listed as an agency, plus the NOAA/GOES/TIROS/JPSS identifiers in the STAC audit; partnership does not imply exclusive NOAA ownership.

### Sentinel

**41 records**. [Open this family](https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/explorer/?family=sentinel).

| Mission / host | Lifecycle label | Record type | Evidence |
|---|---|---|---|
| Sentinel-2B | operational | spacecraft | [Source](https://sentiwiki.copernicus.eu/web/s2-mission) |
| Sentinel-2C | operational | spacecraft | [Source](https://sentiwiki.copernicus.eu/web/s2-mission) |
| Sentinel-1C | operational | spacecraft | [Source](https://sentiwiki.copernicus.eu/web/s1-mission) |
| sentinel-1 (mission group) | unverified | constellation / mission group | [Source](https://stac.dataspace.copernicus.eu/v1/collections/clms_ssm_europe_1km_daily_v1_cog) |
| Sentinel-1A | retired | spacecraft | [Source](https://stac.dataspace.copernicus.eu/v1/collections/clms_wsi_sar-wet-snow_europe_utm_60m_daily_v2) |
| Sentinel-1B | retired | spacecraft | [Source](https://stac.dataspace.copernicus.eu/v1/collections/clms_wsi_sar-wet-snow_europe_utm_60m_daily_v2) |
| Sentinel-1D | operational | spacecraft | [Source](https://stac.dataspace.copernicus.eu/v1/collections/clms_wsi_sar-wet-snow_europe_utm_60m_daily_v2) |
| sentinel-2 | unverified | constellation / mission group | [Source](https://stac.dataspace.copernicus.eu/v1/collections/ccm-optical) |
| Sentinel-2A | operational | spacecraft | [Source](https://stac.dataspace.copernicus.eu/v1/collections/ccm-optical) |
| sentinel-3 | unverified | constellation / mission group | [Source](https://stac.dataspace.copernicus.eu/v1/collections/clms_ba_global_300m_daily_v3_cog) |
| Sentinel-3A | operational | spacecraft | [Source](https://stac.dataspace.copernicus.eu/v1/collections/clms_lswt-nrt_global_1km_10daily_v1_cog) |
| Sentinel-3B | operational | spacecraft | [Source](https://stac.dataspace.copernicus.eu/v1/collections/clms_toc_global_300m_daily_v2_nc) |
| sentinel-5 (mission group) | unverified | constellation / mission group | [Source](https://stac.dataspace.copernicus.eu/v1/collections/sentinel-5p-l1-ra) |
| Sentinel-5P | operational | spacecraft | [Source](https://sentiwiki.copernicus.eu/web/s5p-mission) |
| sentinel-6 (mission group) | unverified | constellation / mission group | [Source](https://stac.dataspace.copernicus.eu/v1/collections/sentinel-6-amr-c-nrt) |
| Sentinel-6A Michael Freilich | operational | spacecraft | [Source](https://stac.dataspace.copernicus.eu/v1/collections/sentinel-6-amr-c-nrt) |
| Sentinel-6B | operational | spacecraft | [Source](https://cmr.earthdata.nasa.gov/cloudstac/POCLOUD/collections/JASON_CS_S6B_L2_ALT_HR_STD_OST_NRT_G_G) |
| Meteosat-13 / Sentinel-4A | operational | spacecraft with hosted Sentinel instrument | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=556) |
| METOP-SG A1 / Sentinel-5A | operational | spacecraft with hosted Sentinel instrument | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=557) |
| METOP-SG A2 / Sentinel-5B | planned | spacecraft with hosted Sentinel instrument | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=838) |
| METOP-SG A3 / Sentinel-5C | planned | spacecraft with hosted Sentinel instrument | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=839) |
| MTG-S2 (sounding) / Sentinel-4B | planned | spacecraft with hosted Sentinel instrument | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=618) |
| Sentinel CHIME-A | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1047) |
| Sentinel CHIME-B | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1048) |
| Sentinel CIMR-A | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1035) |
| Sentinel CIMR-B | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1032) |
| Sentinel CO2M-A | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1033) |
| Sentinel CO2M-B | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1037) |
| Sentinel CO2M-C | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1038) |
| Sentinel CRISTAL-A | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1039) |
| Sentinel CRISTAL-B | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1040) |
| Sentinel LSTM-A | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1041) |
| Sentinel LSTM-B | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1042) |
| Sentinel ROSE-L A | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1036) |
| Sentinel ROSE-L B | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1034) |
| Sentinel-1 NG-A | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1464) |
| Sentinel-1 NG-B | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1465) |
| Sentinel-2D | planned | spacecraft | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=920) |
| Sentinel-3C | commissioning | spacecraft | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=579) |
| Sentinel-3D | planned | spacecraft | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=921) |
| Sentinel-6C | cancelled | spacecraft | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1463) |


### Landsat

**11 records**. [Open this family](https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/explorer/?family=landsat).

| Mission / host | Lifecycle label | Record type | Evidence |
|---|---|---|---|
| Landsat 8 | operational | spacecraft | [Source](https://www.usgs.gov/landsat-missions/landsat-8) |
| Landsat 9 | operational | spacecraft | [Source](https://www.usgs.gov/landsat-missions/landsat-9) |
| landsat | unverified | constellation / mission group | [Source](https://stac.dataspace.copernicus.eu/v1/collections/landsat-c2-l1-oli) |
| Landsat 1 | retired | spacecraft | [Source](https://hda.data.destination-earth.eu/stac/v2/collections/EO.NASA.DAT.LANDSAT.C2_L1) |
| Landsat 2 | retired | spacecraft | [Source](https://hda.data.destination-earth.eu/stac/v2/collections/EO.NASA.DAT.LANDSAT.C2_L1) |
| Landsat 3 | retired | spacecraft | [Source](https://hda.data.destination-earth.eu/stac/v2/collections/EO.NASA.DAT.LANDSAT.C2_L1) |
| Landsat 4 | retired | spacecraft | [Source](https://hda.data.destination-earth.eu/stac/v2/collections/EO.NASA.DAT.LANDSAT.C2_L1) |
| Landsat 5 | retired | spacecraft | [Source](https://hda.data.destination-earth.eu/stac/v2/collections/EO.NASA.DAT.LANDSAT.C2_L1) |
| Landsat 7 | retired | spacecraft | [Source](https://www.usgs.gov/landsat-missions/landsat-7) |
| Landsat 10 | planned | spacecraft | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1016) |
| Landsat 6 | failed | spacecraft / launch failure | [Source](https://www.usgs.gov/landsat-missions/landsat-6) |


### NOAA and partners

**126 records**. [Open this family](https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/explorer/?family=noaa).

| Mission / host | Lifecycle label | Record type | Evidence |
|---|---|---|---|
| GOES-19 | operational | spacecraft | [Source](https://www.noaa.gov/news-release/noaas-goes-19-satellite-now-operational-providing-critical-new-data-to-forecasters) |
| ADEOS-II | retired | spacecraft | [Source](https://fedeo.ceos.org/series/eo:platform/ADEOS-II) |
| CYGNSS | operational | constellation / mission group | [Source](https://cmr.earthdata.nasa.gov/cloudstac/POCLOUD/collections/CYGNSS_L1_V3.2_3.2) |
| DSCOVR | operational | spacecraft | [Source](https://cmr.earthdata.nasa.gov/cloudstac/LARC_CLOUD/collections/DSCOVR_EPIC_L2_AER_03) |
| GOES | unverified | constellation / mission group | [Source](https://hda.data.destination-earth.eu/stac/v2/collections/EO.EUM.DAT.MULT.PMW_IR-GIRAFE_PRECIP-CDR-V001) |
| GOES-1 | retired | spacecraft | [Source](https://fedeo.ceos.org/series/eo:platform/GOES-1) |
| GOES-10 | retired | spacecraft | [Source](https://fedeo.ceos.org/series/eo:platform/GOES-10) |
| GOES-11 | retired | spacecraft | [Source](https://fedeo.ceos.org/series/eo:platform/GOES-11) |
| GOES-12 | retired | spacecraft | [Source](https://hda.data.destination-earth.eu/stac/v2/collections/EO.EUM.DAT.MULT.PMW_IR-GIRAFE_PRECIP-CDR-V001) |
| GOES-13 | unverified | spacecraft | [Source](https://hda.data.destination-earth.eu/stac/v2/collections/EO.EUM.DAT.MULT.PMW_IR-GIRAFE_PRECIP-CDR-V001) |
| GOES-14 | unverified | spacecraft | [Source](https://hda.data.destination-earth.eu/stac/v2/collections/EO.EUM.DAT.MULT.PMW_IR-GIRAFE_PRECIP-CDR-V001) |
| GOES-15 | unverified | spacecraft | [Source](https://hda.data.destination-earth.eu/stac/v2/collections/EO.EUM.DAT.MULT.PMW_IR-GIRAFE_PRECIP-CDR-V001) |
| GOES-16 | operational | spacecraft | [Source](https://hda.data.destination-earth.eu/stac/v2/collections/EO.EUM.DAT.MULT.PMW_IR-GIRAFE_PRECIP-CDR-V001) |
| GOES-17 | operational | spacecraft | [Source](https://hda.data.destination-earth.eu/stac/v2/collections/EO.EUM.DAT.MULT.PMW_IR-GIRAFE_PRECIP-CDR-V001) |
| GOES-18 | operational | spacecraft | [Source](https://hda.data.destination-earth.eu/stac/v2/collections/EO.EUM.DAT.MULT.PMW_IR-GIRAFE_PRECIP-CDR-V001) |
| GOES-2 | retired | spacecraft | [Source](https://fedeo.ceos.org/series/eo:platform/GOES-2) |
| GOES-3 | retired | spacecraft | [Source](https://fedeo.ceos.org/series/eo:platform/GOES-3) |
| GOES-4 | retired | spacecraft | [Source](https://fedeo.ceos.org/series/eo:platform/GOES-4) |
| GOES-5 | retired | spacecraft | [Source](https://fedeo.ceos.org/series/eo:platform/GOES-5) |
| GOES-6 | retired | spacecraft | [Source](https://fedeo.ceos.org/series/eo:platform/GOES-6) |
| GOES-7 | retired | spacecraft | [Source](https://cmr.earthdata.nasa.gov/cloudstac/ORNL_CLOUD/collections/BFO_hmet02_gridded_met_phase2-3_607_1) |
| GOES-8 | retired | spacecraft | [Source](https://cmr.earthdata.nasa.gov/cloudstac/LPCLOUD/collections/GEOLST4KHR_002) |
| GOES-9 | retired | spacecraft | [Source](https://cmr.earthdata.nasa.gov/cloudstac/LARC_CLOUD/collections/CER_GEO_Ed4_GOE09_NH_V01) |
| goes-r (mission group) | unverified | constellation / mission group | [Source](https://data.inpe.br/bdc/stac/v1/collections/GOES19-L2-CMI-1) |
| JASON-3 | operational | spacecraft | [Source](https://cmr.earthdata.nasa.gov/cloudstac/POCLOUD/collections/OSCAR_L4_OC_NRT_V2.0_2.0) |
| jpss (mission group) | unverified | constellation / mission group | [Source](https://stac.dataspace.copernicus.eu/v1/collections/clms_lie_europe_250m_daily_v2_cog) |
| METOP-A | retired | spacecraft | [Source](https://cmr.earthdata.nasa.gov/stac/ESA/collections/AVHRRLocalAreaCoverageImagery10_10.0) |
| METOP-B | operational | spacecraft | [Source](https://cmr.earthdata.nasa.gov/stac/ESA/collections/AVHRRLocalAreaCoverageImagery10_10.0) |
| METOP-C | operational | spacecraft | [Source](https://hda.data.destination-earth.eu/stac/v2/collections/EO.EUM.DAT.METOP.AMSUL1) |
| NOAA (mission group) | unverified | constellation / mission group | [Source](https://hda.data.destination-earth.eu/stac/v2/collections/EO.EUM.DAT.METOP.AVHRRGACR02) |
| NOAA-1 | retired | spacecraft | [Source](https://cmr.earthdata.nasa.gov/stac/ESA/collections/AVHRRLocalAreaCoverageImagery10_10.0) |
| NOAA-10 | retired | spacecraft | [Source](https://cmr.earthdata.nasa.gov/stac/ESA/collections/AVHRRLocalAreaCoverageImagery10_10.0) |
| NOAA-11 | retired | spacecraft | [Source](https://cmr.earthdata.nasa.gov/stac/ESA/collections/AVHRRLocalAreaCoverageImagery10_10.0) |
| NOAA-12 | retired | spacecraft | [Source](https://cmr.earthdata.nasa.gov/stac/ESA/collections/AVHRRLocalAreaCoverageImagery10_10.0) |
| NOAA-13 | retired | spacecraft | [Source](https://cmr.earthdata.nasa.gov/stac/ESA/collections/AVHRRLocalAreaCoverageImagery10_10.0) |
| NOAA-14 | retired | spacecraft | [Source](https://cmr.earthdata.nasa.gov/stac/ESA/collections/AVHRRLocalAreaCoverageImagery10_10.0) |
| NOAA-15 | retired | spacecraft | [Source](https://cmr.earthdata.nasa.gov/stac/ESA/collections/AVHRRLocalAreaCoverageImagery10_10.0) |
| NOAA-16 | retired | spacecraft | [Source](https://cmr.earthdata.nasa.gov/stac/ESA/collections/AVHRRLocalAreaCoverageImagery10_10.0) |
| NOAA-17 | retired | spacecraft | [Source](https://cmr.earthdata.nasa.gov/stac/ESA/collections/AVHRRLocalAreaCoverageImagery10_10.0) |
| NOAA-18 | retired | spacecraft | [Source](https://cmr.earthdata.nasa.gov/stac/ESA/collections/AVHRRLocalAreaCoverageImagery10_10.0) |
| NOAA-19 | retired | spacecraft | [Source](https://cmr.earthdata.nasa.gov/stac/ESA/collections/AVHRRLocalAreaCoverageImagery10_10.0) |
| NOAA-2 | retired | spacecraft | [Source](https://cmr.earthdata.nasa.gov/stac/ESA/collections/AVHRRLocalAreaCoverageImagery10_10.0) |
| noaa-20 | operational | spacecraft | [Source](https://stac.dataspace.copernicus.eu/v1/collections/clms_lie_europe_250m_daily_v2_cog) |
| NOAA-21 | operational | spacecraft | [Source](https://cmr.earthdata.nasa.gov/cloudstac/LAADS/collections/VJ202MOD_2.1) |
| NOAA-3 | retired | spacecraft | [Source](https://cmr.earthdata.nasa.gov/stac/ESA/collections/AVHRRLocalAreaCoverageImagery10_10.0) |
| NOAA-4 | retired | spacecraft | [Source](https://cmr.earthdata.nasa.gov/stac/ESA/collections/AVHRRLocalAreaCoverageImagery10_10.0) |
| NOAA-5 | retired | spacecraft | [Source](https://cmr.earthdata.nasa.gov/stac/ESA/collections/AVHRRLocalAreaCoverageImagery10_10.0) |
| NOAA-6 | retired | spacecraft | [Source](https://cmr.earthdata.nasa.gov/stac/ESA/collections/AVHRRLocalAreaCoverageImagery10_10.0) |
| NOAA-7 | retired | spacecraft | [Source](https://cmr.earthdata.nasa.gov/stac/ESA/collections/AVHRRLocalAreaCoverageImagery10_10.0) |
| NOAA-8 | retired | spacecraft | [Source](https://cmr.earthdata.nasa.gov/stac/ESA/collections/AVHRRLocalAreaCoverageImagery10_10.0) |
| NOAA-9 | retired | spacecraft | [Source](https://cmr.earthdata.nasa.gov/stac/ESA/collections/AVHRRLocalAreaCoverageImagery10_10.0) |
| NOAA POES | unverified | constellation / mission group | [Source](https://cmr.earthdata.nasa.gov/stac/ESA/collections/AVHRRLocalAreaCoverageImagery10_10.0) |
| Sentinel-6A Michael Freilich | operational | spacecraft | [Source](https://stac.dataspace.copernicus.eu/v1/collections/sentinel-6-amr-c-nrt) |
| Sentinel-6B | operational | spacecraft | [Source](https://cmr.earthdata.nasa.gov/cloudstac/POCLOUD/collections/JASON_CS_S6B_L2_ALT_HR_STD_OST_NRT_G_G) |
| suomi npp | retired | spacecraft | [Source](https://www.nesdis.noaa.gov/news/update-4-cessation-of-suomi-national-polar-orbiting-partnership-s-npp-data-users-november-02-2026-1540-utc-and-decommissioning-issued-november-2-2026-1800-utc) |
| TIROS (mission group) | unverified | constellation / mission group | [Source](https://hda.data.destination-earth.eu/stac/v2/collections/EO.EUM.DAT.METOP.AVHRRGACR02) |
| TIROS-N | retired | spacecraft | [Source](https://hda.data.destination-earth.eu/stac/v2/collections/EO.EUM.DAT.METOP.AVHRRGACR02) |
| CDARS | cancelled | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=725) |
| CLARREO-1 | cancelled | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=643) |
| CLARREO-2 | cancelled | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=688) |
| CLARREO-3 | cancelled | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=689) |
| CLARREO-4 | cancelled | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=690) |
| COSMIC-1 FM1 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=482) |
| COSMIC-1 FM2 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=483) |
| COSMIC-1 FM3 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=484) |
| COSMIC-1 FM4 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=485) |
| COSMIC-1 FM5 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=486) |
| COSMIC-1 FM6 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=487) |
| COSMIC-2/FORMOSAT-7 (1) | operational | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=771) |
| COSMIC-2/FORMOSAT-7 (2) | operational | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=926) |
| COSMIC-2/FORMOSAT-7 (3) | operational | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=927) |
| COSMIC-2/FORMOSAT-7 (4) | operational | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=928) |
| COSMIC-2/FORMOSAT-7 (5) | operational | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=929) |
| COSMIC-2/FORMOSAT-7 (6) | operational | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=930) |
| COSMIC-2B (Polar) | cancelled | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=786) |
| DMSP F-10 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=302) |
| DMSP F-11 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=303) |
| DMSP F-12 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=304) |
| DMSP F-13 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=305) |
| DMSP F-14 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=306) |
| DMSP F-15 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=345) |
| DMSP F-16 | operational | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=381) |
| DMSP F-17 | operational | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=408) |
| DMSP F-18 | operational | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=409) |
| DMSP F-19 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=410) |
| DMSP F-20 | cancelled | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=411) |
| DMSP F-7 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=500) |
| DMSP F-8 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=300) |
| DMSP F-9 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=301) |
| EWS-G2 | operational | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=335) |
| EWS-G3 | operational | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=266) |
| Free Flyer-2 | unverified | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=726) |
| Geo-S1 | cancelled | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1457) |
| Geo-S2 | cancelled | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1459) |
| GeoXO-1 | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=980) |
| GeoXO-2 | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=981) |
| GeoXO-3 | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1458) |
| GeoXO-4 | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1460) |
| GOES (SMS 1) | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=515) |
| GOES (SMS 2) | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=516) |
| JPSS-3 | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=801) |
| JPSS-4 | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=802) |
| NPOESS-1 | cancelled | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=270) |
| NPOESS-2 | cancelled | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=264) |
| NPOESS-3 | cancelled | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=361) |
| NPOESS-4 | cancelled | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=362) |
| NPOESS-5 | cancelled | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=382) |
| NPOESS-6 | cancelled | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=383) |
| OSTM (Jason-2) | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=419) |
| QuickSounder | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1461) |
| Sentinel-6C | cancelled | spacecraft | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1463) |
| SOLAR-1 | operational | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=919) |
| SOLAR-A | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1416) |
| SOLAR-B | planned | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=1417) |
| TCTE | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=734) |
| TIROS M (ITOS-1) | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=514) |
| TIROS-1 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=896) |
| TIROS-10 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=903) |
| TIROS-2 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=897) |
| TIROS-3 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=898) |
| TIROS-4 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=899) |
| TIROS-5 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=900) |
| TIROS-6 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=901) |
| TIROS-7 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=902) |
| TIROS-8 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=886) |
| TIROS-9 | retired | mission record / platform identity not independently reviewed | [Source](https://database.eohandbook.com/database/missionsummary.aspx?missionID=885) |


## Operator corrections and reference resources

[USGS](https://www.usgs.gov/landsat-missions/landsat-6) confirms that Landsat 6 failed to achieve orbit; its historical record is labeled **failed / no orbit achieved**, and supplies no EO archive. [Landsat 7](https://www.usgs.gov/landsat-missions/landsat-7) distinguishes its end of imaging from decommissioning on 4 June 2025. The [NOAA S-NPP notice](https://www.nesdis.noaa.gov/news/update-4-cessation-of-suomi-national-polar-orbiting-partnership-s-npp-data-users-november-02-2026-1540-utc-and-decommissioning-issued-november-2-2026-1800-utc) confirms permanent science-data delivery cessation on 2 November 2026; this service retirement overrides the older registry status without claiming that the spacecraft has already reentered.

The user-supplied [NOAA introduction](https://www.nesdis.noaa.gov/news/what-satellite) explains satellites and their bus, instruments and power source; its 2016 fleet counts are historical. The [Wikipedia EO satellite list](https://en.wikipedia.org/wiki/List_of_Earth_observation_satellites) is a secondary discovery reference with an update warning, rather than the authority for current lifecycle labels. [KeepTrack](https://app.keeptrack.space/) is linked as a separate orbit exploration tool; no KeepTrack code, imagery or orbital feed is copied or implied by the schematic positions here.

## Attribution and refresh

CEOS MIM Database, https://database.eohandbook.com, accessed 2026-11-03. CEOS-derived factual metadata are adapted under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); normalization, crosswalks, host consolidation and agency overrides are documented transformations. No source imagery is reproduced. The original application code and graphics retain their MIT license; CEOS metadata retain CC BY 4.0.

Refresh explicitly with `python scripts/mission_registry.py --refresh`, then `python scripts/curate_stac.py` and `python scripts/curate_research.py`. Review source/identity changes, run validation and tests, and rebuild. Ordinary builds use the saved snapshot and make no registry requests. The permanent-ID crosswalk and validation guard against dropping family members on refresh.
