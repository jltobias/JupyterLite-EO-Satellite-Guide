# Attributions and reuse

<!-- book-content -->

## Original work

The explorer code, original schematic satellite symbols, original splash SVG, lesson code and original prose are provided under the repository's [MIT license](https://github.com/jltobias/JupyterLite-EO-Satellite-Guide/blob/main/LICENSE). No mission insignia or agency logo is used. Original graphics are conceptual drawings and do not assert spacecraft geometry, position, status or scaled orbital radius. No AI-generated bitmap is included.

## Bundled map data

**Made with Natural Earth.** `assets/ne_110m_land.geojson` is Natural Earth's 1:110m land geometry, downloaded on 2026-11-02 from the [Natural Earth vector source repository](https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_110m_land.geojson). Credit: Tom Patterson, Nathaniel Vaughn Kelso and contributors. Natural Earth map data are [public domain](https://www.naturalearthdata.com/about/terms-of-use/). The explorer and splash project and restyle these polygons; no political boundaries are shown. The build manifest records the bundled file hash.

## NASA ARSET educational reference

Amber Jean McCullum, Juan L. Torres-Perez and Zach Bengtsson. *Hyperspectral Data for Land and Coastal Systems*, Part 2, NASA Applied Remote Sensing Training Program, 26 January 2021. [Original PDF](https://appliedsciences.nasa.gov/sites/default/files/2021-01/Hyperspectral_Part2_Final.pdf). The supplied local copy was read as reference. The hyperspectral lesson paraphrases selected concepts from pp. 8-20 and 24-26 and cites them; the PDF and its figures are not redistributed. Its third-party figures retain their credited owners' rights, and NASA authorship must not be taken to license all embedded images. Original synthetic teaching spectra replace copied figures.

## Supplied plan and raster poster

The user supplied `earth-observation-explorer-plan.md` as an implementation reference. Its author, date and reuse license were not provided. Requirements are implemented and summarized in original prose; the document is not redistributed. The user also supplied a raster titled *Global Earth Observation Satellite System*. Its original author, publisher, date and reuse terms remain unresolved. It is visual inspiration only, is not bundled, and is not a source for verified mission facts. Its old mission labels are not automatically interpreted as current operations.

## Scientific metadata and studies

The catalog contains short, independently curated factual summaries from NASA, USGS, ESA/Copernicus, JAXA, DLR/GFZ/EnMAP, CMA/NSMC, ISRO/NRSC, NOAA, JMA, EUMETSAT and WMO OSCAR. Exact titles, publishers, access dates, field-group citations and product sources are in [data/catalog.json](https://github.com/jltobias/JupyterLite-EO-Satellite-Guide/blob/main/data/catalog.json) and the Book source registry. These summaries are not the providers' complete datasets or imagery; linked external material retains its own terms.

Johnson DP, Wilson JS, Luber GC (2009). *Socioeconomic indicators of heat-related health risk supplemented with remotely sensed data.* International Journal of Health Geographics 8:57. [DOI:10.1186/1476-072X-8-57](https://doi.org/10.1186/1476-072X-8-57). The study is paraphrased with attribution; no figures, individual health records or patient locations are redistributed. The study predates Landsat 8/9; those missions are clearly labeled as modern teaching analogues.

Al-Hamdan and colleagues. *The Use of GIS and Remotely Sensed Data in Environmental Public Health Tracking: The HELIX-Atlanta Experience*. [NASA NTRS 20070032007](https://ntrs.nasa.gov/citations/20070032007). Described as a pilot and collaboration, using the source abstract's scope. Chang HH and colleagues (2019), *Time-series analysis of satellite-derived fine particulate matter pollution and asthma morbidity in Jackson, MS*, Environmental Monitoring and Assessment 191 (Suppl 2):280. [CDC Stacks record](https://stacks.cdc.gov/view/cdc/126808). NCEH's surveillance-support role is distinguished from study leadership.

The orbit lesson uses conventional spherical-Earth/two-body constants, with references to the [NASA Earth fact sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html) and [IERS Conventions 2010](https://iers-conventions.obspm.fr/content/tn36.pdf). Its simulated paths are not actual ephemerides. Spectral lesson values are invented, not measured.

## Semantic standards and contextual resources

The STAC inventory is derived from the [official STAC Index registry API](https://stacindex.org/api/catalogs), maintained by the STAC Index contributors, and factual metadata in the linked provider catalogs. The bounded audit, timestamps, failures and source-document URLs are preserved in `data/stac-audit.json`; the reviewed identifier mapping is in `data/stac-coverage.json`. Only short factual identifiers, titles, platform/instrument lists and metadata references are redistributed; provider descriptions, imagery and assets are not bundled. A public registry listing does not grant rights to its data assets. Inspect each collection/Item's license and provider terms.

The original research vocabulary, matcher and schema are MIT-licensed repository work. [W3C SKOS](https://www.w3.org/TR/skos-reference/) supplies concept/label/broader identifiers, alongside SOSA/SSN, DCAT and PROV. [STAC common metadata](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md) supplies the meaning of platform, constellation and instruments fields; a platform can also be an aircraft or ground-based system. No official STAC ontology or unrestricted natural-language reasoning is claimed. Atmospheric pathway summaries credit [ESA/Copernicus Sentinel-5P](https://sentiwiki.copernicus.eu/web/s5p-mission), [KNMI TROPOMI NO₂](https://www.tropomi.eu/data-products/nitrogen-dioxide), [NASA/SAO TEMPO](https://tempo.si.edu/data_for_scientists.html) and [NASA MODIS aerosol](https://atmosphere-imager.gsfc.nasa.gov/products/aerosol) documentation. Images from those pages are not copied.

[JupyterLite STAC Browser](https://github.com/jltobias/JupyterLite-STAC-Browser) is linked as a separate discovery/export tool; no upstream application code is vendored. [FieldWork](https://github.com/digital-twin-ph/fieldwork), by the Digital Twin Public Health contributors (Apache-2.0), supplies a related [experimental STAC metadata profile](https://github.com/digital-twin-ph/fieldwork/blob/main/ontology/stac.ttl). Its concepts are discussed and linked, without copying ontology code, asserting equivalent semantics or implementing an importer. The John Snow workflow concerns travel time/cholera, not snow cover. Follow the destination projects' own licenses, data notices and input contracts.

[W3C SOSA/SSN](https://www.w3.org/TR/vocab-ssn/), [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/), and [PROV-O](https://www.w3.org/TR/prov-o/) supply vocabulary identifiers. Standards documents retain W3C terms; they are linked, not copied. [SWEET](https://github.com/ESIPFed/sweet), [NASA GCMD](https://www.earthdata.nasa.gov/learn/find-data/idn/gcmd-keywords), [OGC GeoSPARQL](https://www.ogc.org/standard/geosparql/), [Workflow Run RO-Crate](https://www.researchobject.org/workflow-run-crate/profiles/workflow_run_crate/), [GEOSS](https://old.earthobservations.org/geoss.php) and [GEO Knowledge Hub](https://gkhub.earthobservations.org/doc/faq) are linked extension/context resources; no source content or ontology distribution is vendored.

OpenStreetMap tagging examples link to [`amenity=blood_bank`](https://wiki.openstreetmap.org/wiki/Tag:amenity%3Dblood_bank) and [`healthcare=blood_donation`](https://wiki.openstreetmap.org/wiki/Tag:healthcare%3Dblood_donation). No OSM data extract, map tiles or wiki text is bundled. Any future OSM database use must credit OpenStreetMap contributors and comply with the [ODbL and attribution guidance](https://www.openstreetmap.org/copyright). These tags describe facilities, not live blood inventories.

## Software

Jupyter Book v1 and Sphinx Book Theme: Executable Books / Jupyter Book community, BSD-3-Clause. JupyterLite Core and JupyterLite Pyodide Kernel: JupyterLite contributors, BSD-3-Clause. Pyodide: Pyodide contributors, MPL-2.0 (runtime packages carry their own licenses). IPython, nbformat and nbclient: Project Jupyter, BSD-3-Clause. jsonschema: Julian Berman and contributors, MIT. Playwright: Microsoft, Apache-2.0 (development tests only). Transitive packages retain their own licenses and distribution notices; nothing in the repository MIT license overrides them. See [Jupyter Book documentation](https://jupyter-book.readthedocs.io/v1/intro.html), [JupyterLite documentation](https://jupyterlite.readthedocs.io/en/stable/), [Pyodide](https://github.com/pyodide/pyodide) and [Playwright](https://github.com/microsoft/playwright-python).
