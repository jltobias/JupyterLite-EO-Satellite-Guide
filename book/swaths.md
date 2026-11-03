# Research questions, swaths and study areas

[Open the Swaths & orbits tab](https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/explorer/swaths.html?q=air+quality+and+NO2+measures&bbox=-76,39,-74,41&mission=sentinel-5p) · [Launch notebook 08](https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/lab/index.html?path=08_swaths_orbits_study_area.ipynb) · [Download the offline study-area lab](https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/downloads/eo-swaths.html)

<iframe title="EO research study-area geometry lab" src="../explorer/swaths.html?q=air+quality+and+NO2+measures&amp;bbox=-76,39,-74,41&amp;mission=sentinel-5p" style="width:100%;height:1150px;border:1px solid #345;border-radius:8px" loading="lazy" allowfullscreen></iframe>

## Connect the question to the area

Enter a research question such as **air quality and NO₂ measures**. The same curated concept profile used by the constellation identifies potential platforms. The tab lists all candidates and identifies which have nominal geometry presets. Eight named examples currently cover TROPOMI, OMI, TEMPO, Landsat 8/9 OLI, Sentinel-2B/2C MSI and Sentinel-1C IW. A candidate without a preset is explicitly uncurated, rather than receiving invented orbital or swath parameters.

Set a CRS84 bounding box as **west, south, east, north**, or draw a rectangle. Switching candidates keeps the study box. Use *Zoom to box* and *World view* to connect local and global scales. A NO₂ question lets a researcher contrast a wide-swath polar spectrometer with regional daytime geostationary sampling while retaining the measurement's interpretation limits.

*Demonstrate a pass over this box* deliberately aligns the circular model at T+0. Play, pause and scrub time to examine the moving 60-second swath strip. That alignment is a teaching action, not evidence that a spacecraft will pass there. Calendar dates belong to the separate archive query; the arbitrary model phase is not tied to those dates.

## Spatial and temporal meaning

Each spatial inset draws **30 × 20 illustrative cells**. Their labeled physical extent changes with the chosen sensor's sampling, so equal screen-sized cells can represent very different areas on Earth. The approximate grid count over the whole box uses a rectangular approximation at the center latitude. It does not estimate valid pixels, file size or the true number of swath samples.

Resolution, pixel spacing and product grids differ. MSI bands have different sampling; Landsat thermal data can be distributed on a finer grid than native thermal sampling; Sentinel-1 IW uses side-looking radar geometry and its output grid is not its native resolution. The profiles retain these qualifiers. Actual footprint shape also varies across scan and with processing/version.

For a **heat** question, the Landsat examples switch the sampling illustration to TIRS/TIRS-2's 100 m native thermal context, rather than presenting OLI's 30 m reflectance sampling as a thermal capability. For a vegetation question, the default optical context remains. The orbit/swath geometry is still only the stated nominal example.

The temporal panel separates:

- **Orbital period:** one revolution in the teaching model.
- **Ground-track repeat:** an operator-documented nominal cycle, not calculated from the arbitrary model phase.
- **Scan interval:** the stated nominal GEO scan cadence; displayed ticks are illustrative, not actual scan times.
- **Modeled proximity intervals:** a sampled geometric proxy in this scenario, not measured revisit or predicted acquisition.
- **Usable observations:** require an acquisition, working instrument, suitable illumination/viewing conditions, processing, QA and product availability.

## Model and assumptions

LEO examples use a spherical Earth of radius 6,371 km and a circular two-body period, `2π√((R+h)³/μ)`, with `μ = 398600.4418 km³/s²`. Earth rotates uniformly with a sidereal period of 86,164.0905 seconds. The code rotates a circular inclined orbit into the Earth frame using an arbitrary initial node/argument. It does not ingest TLEs, current state vectors, schedules, J2 precession, attitude or instrument pointing. The nominal SSO inclination is a teaching input, not a full Sun-synchronous propagator. The existing [orbit lesson](notebooks/04_orbits_and_resolution.ipynb) supplies the constants' sources.

The swath polygon approximates a symmetric nadir strip across the nominal swath width between the current point and its position 60 seconds later, using spherical offsets. **Real SAR is side-looking**: the Sentinel-1 example demonstrates swath width and sampling scale, not real SAR access. The timeline samples at 10-second intervals and compares ground-track distance to a clamped study-box point against half the swath width. This distance-to-box proxy is not a rigorous polygon/sensor access calculation and can miss brief or complex edge cases. Use an appropriate geodesic sensor model and authoritative ephemerides for actual access predictions.

For GEO, the subpoint stays fixed. A spherical geometric horizon is calculated independently of the instrument's viewing region. The TEMPO rectangle is the provider's [advertised collection envelope](https://cmr.earthdata.nasa.gov/stac/LARC_CLOUD/collections/TEMPO_NO2_L2_V04), not its sensor field of view. Intersecting that envelope and passing a horizon test do not establish an observation, daytime illumination or a valid NO₂ retrieval. The current lab does not propagate HEO or L1 trajectories; their source-backed classifications remain available in the [orbit legend](orbit-guide.md).

Bounding boxes must have west < east and south < north within ±180°/±90°; split date-line study areas. Display paths are split/wrapped at the map seam. High-latitude and large-area interpretation requires care with the equirectangular projection and local sampling approximation.

## Observed STAC footprints

Only **Fetch up to 10 Item footprints** makes a provider request. It sends the chosen box/dates to the named public collection Items endpoint, with a 25-second timeout and 6 MB response bound. No proxy, login, token or asset transfer is added. Provider CORS, TLS, access rules and availability can still block metadata retrieval. The working teaching model remains available offline.

Orange polygons are **observed Item metadata footprints**; hover/focus the table or polygon to link the views. Null/missing geometries remain metadata-only records. A footprint can describe an entire orbit, tile or broad envelope and does not establish valid pixels or cloud/quality conditions inside your box. Multi-platform collections can return other spacecraft; the table explicitly distinguishes a matching platform from another/unspecified platform. A 10-Item sample is not a complete archive search.

Changing the mission, box, route or archive dates cancels obsolete requests and clears stale results. Saving footprint GeoJSON exports geometry, selected metadata, source URLs and query provenance, without data assets. Copy the **catalog API root**, collection identifier, bbox and dates to [JupyterLite STAC Browser](https://jltobias.github.io/JupyterLite-STAC-Browser/explorer/) for fuller discovery and asset inspection. Its current Explorer has no URL query importer; collection URLs alone open metadata-only mode there.

## Share the research context

*Copy study link* preserves question, mission, bbox, arbitrary phase, model duration/time and archive dates. *Save study brief* writes the `eo-study-area/1` planning profile with source-backed nominal inputs and assumptions. Questions/coordinates in shared URLs are visible to recipients and can enter browser/server history. This is not a FieldWork importer, an acquisition receipt or an analysis result.

Notebook 08 demonstrates a question-to-area graph using the original `eo:studyArea` relation and [GeoSPARQL](https://www.ogc.org/standard/geosparql/) geometry/WKT. It makes no observation, exposure or workflow-run assertion. FieldWork remains a downstream workflow option after appropriate real data preparation; direct STAC acquisition and automatic brief import are not currently implemented there.

## Specifications and citations

The checked-in [geometry presets](https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/data/geometry-presets.json) and [orbit vocabulary](https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/data/orbit-types.json) record snapshot dates and source IDs. Each mission's source disclosure links the same registry used by the constellation. References include [USGS Landsat 8](https://www.usgs.gov/landsat-missions/landsat-8), [Copernicus Sentinel-2](https://sentiwiki.copernicus.eu/web/s2-mission), [Sentinel-1](https://sentiwiki.copernicus.eu/web/s1-mission), [Sentinel-5P](https://sentiwiki.copernicus.eu/web/s5p-mission), [NASA Aura spacecraft](https://science.nasa.gov/mission/aura/spacecraft-and-instruments/), [NASA OMI geometry](https://aura.gsfc.nasa.gov/images/aura_validation_v1.0.pdf), [NASA's high-resolution TROPOMI product record](https://data.nasa.gov/dataset/sentinel-5p-tropomi-near-real-time-nrt-tropospheric-no2-1-orbit-l2-5-5km-x-3-5km-v2-s5p-l2), [TEMPO products](https://tempo.si.edu/data_for_scientists.html) and [WMO's hosted TEMPO record](https://space.oscar.wmo.int/satellites/view/tempo). No source figures or satellite imagery are copied.
