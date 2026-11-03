# From a research question to usable data

Open the [explorer](https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/explorer/?q=air+quality+and+NO2+measures) and enter **air quality and NO₂ measures**. The curated vocabulary recognizes NO₂ and highlights Sentinel-5P/TROPOMI, Aura/OMI and Intelsat 40e/TEMPO in both the map and table. A specific pollutant takes precedence over the broad air-quality concept. A gold outline means potential relevance. Hover/focus and selection remain separate linked states.

The default map shows every research match. The table shows 13 rows at a time; hovering/focusing a map mark reveals its row. **Table page** mode keeps 13 larger symbols synchronized with the table. Other filters still intersect research matches. Selecting a mission family starts a fresh family view, clearing the question and other filters. All filtered matches export to CSV. Fullscreen keeps both views visible, with question controls under **Research**. The NO2 profile includes Sentinel-4A and Sentinel-5A hosts with operator documentation links; their data are not substituted with a Sentinel-5P STAC collection.

## The evidence chain

> Research question → curated SKOS concept → observable property → sensor/retrieval → platform → STAC collection → provider → Item/asset review.

The ontology is an original application profile, using [SKOS](https://www.w3.org/TR/skos-reference/), [SOSA/SSN](https://www.w3.org/TR/vocab-ssn/), [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) and [PROV-O](https://www.w3.org/TR/prov-o/). Download the [schema vocabulary](https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/data/research-ontology.ttl), [curated concepts and routes](https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/data/research-topics.json) and [generated graph](https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/data/catalog.jsonld). `eo:potentialPlatform` is deliberately a qualified editorial relationship; it is not an assertion of study suitability or acquired data. Mission groups are separate from individual spacecraft. Imported mixed instrument arrays do not create invented hosted-sensor assertions.

Matching is deterministic phrase/alias lookup, performed locally. Eight starting concepts cover NO₂, aerosols, broad air quality, surface heat, vegetation, flooding, coastal/ocean colour and snow. This is an extensible vocabulary, not an unrestricted natural-language reasoner. Unsupported wording produces an explicit no-match result. The [coverage report](stac-coverage.md) describes the inventory's limits.

## NO₂ example

**Compare these candidates over your study area** carries the question into the [Swaths & orbits tab](swaths.md). Candidate selection preserves the bbox. The nominal model teaches geometric relationships; a separate optional query checks historical Item footprints in the same area. Study briefs preserve the question, area, preset, arbitrary phase and archive settings without asserting a pass prediction or valid observation.

[TROPOMI's NO₂ product](https://www.tropomi.eu/data-products/nitrogen-dioxide) contains atmospheric column retrievals. [Sentinel-5P](https://sentiwiki.copernicus.eu/web/s5p-mission) flies in a near-polar Sun-synchronous orbit: near-daily sampling and a 16-day orbital cycle describe different temporal properties. [TEMPO](https://tempo.si.edu/overview.html) is hosted on the geostationary Intelsat 40e spacecraft and observes North America during daytime. Its [Level-2 products](https://tempo.si.edu/data_for_scientists.html) have a nominal 2.0 × 4.75 km footprint; viewing geometry and processing matter. Neither column retrieval is automatically a near-surface concentration or an exposure estimate.

The NO₂ route cards name verified collection identifiers and access conditions. Copernicus metadata can be public while asset downloads require authentication. NASA assets can require Earthdata Login. Read version-specific units, quality flags, clouds, averaging kernels, sampling and validation documentation before analysis. NetCDF products are not automatically GeoTIFF rasters accepted by downstream tools.

## Share and execute

1. **Copy research link** creates a URL containing the question. Anyone opening it gets the same curated concept matching against the deployed catalog. Questions in shared URLs are visible to recipients and may enter browser/server history.
2. **Save research brief** records the question, matched concepts/platforms, routes, catalog date and interpretation limits. It is planning metadata, not a STAC Item, a workflow-run receipt, or a FieldWork import format.
3. **Save runnable STAC notebook**, open this Guide's Lab, upload the notebook, edit study area/dates and run. It carries the exact route and uses the bundled `search_stac` helper for a bounded request of at most 10 Item metadata records. No asset bytes are requested. Notebook 07 also teaches this path; network cells remain opt-in during Book builds.
4. In the [JupyterLite STAC Browser](https://jltobias.github.io/JupyterLite-STAC-Browser/explorer/), choose **Custom HTTPS URL**, paste the copied **catalog URL**, connect, select the separately named collection and set the area/dates. The API root advertises search; a collection URL alone opens metadata-only browsing in that Explorer. The current Explorer has no URL-based query importer. This repository does not silently modify that separate application. Its [notebooks](https://jltobias.github.io/JupyterLite-STAC-Browser/lite/lab/index.html?path=03_other_catalogs_and_export.ipynb) provide the fuller discovery, provenance and export workflow.

Provider availability, browser CORS, authentication, signing, licensing and file formats remain real access conditions. The live helper reports errors; it never substitutes an unrelated dataset or downloads imagery automatically.

## FieldWork connection

[FieldWork](https://digital-twin-ph.github.io/fieldwork/?example=snow-isochrone) supplies typed, browser-based geospatial/public-health workflows. Its John Snow isochrone example concerns historical cholera and travel time. It is not a snow-cover example or a ready-made air-quality analysis.

The [STAC Browser handoff guide](https://github.com/jltobias/JupyterLite-STAC-Browser/blob/main/book/fieldwork-integration.md) describes selection exports and compatible crop sidecars. Inspect an Item/asset there, obtain a suitable raster, and use FieldWork's documented manual inputs. A supported crop may offer a `fieldwork-raster-handoff/1` sidecar, subject to grid, CRS, size and provenance checks. This does not imply that a NO₂ NetCDF product is compatible: unit-preserving extraction, QA, aggregation and conversion require a real processing step.

FieldWork's [experimental STAC vocabulary](https://github.com/digital-twin-ph/fieldwork/blob/main/ontology/stac.ttl) distinguishes catalogs, collections, Items and assets. This profile links to it as related work without asserting vocabulary equivalence or importing its terms as an official standard. Direct STAC acquisition and automatic research-brief import are not currently implemented there. No FieldWork code, data, or workflow is redistributed by this Guide.
