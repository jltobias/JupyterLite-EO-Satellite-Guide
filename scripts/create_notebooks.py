"""Recreate starter lessons. Maintainers: this overwrites the six source notebooks."""
from pathlib import Path
import nbformat as nbf

ROOT=Path(__file__).resolve().parents[1]


def save(name, cells):
    nb=nbf.v4.new_notebook(metadata={"kernelspec":{"display_name":"Python (Pyodide)","language":"python","name":"python3"},"language_info":{"name":"python","version":"3.13"}})
    nb.cells=[]
    for index,(kind,text) in enumerate(cells):
        cell=nbf.v4.new_markdown_cell(text.strip()) if kind=="md" else nbf.v4.new_code_cell(text.strip())
        cell.id=f"{name[:2]}-{index:02}"
        nb.cells.append(cell)
    path=ROOT / "notebooks" / name
    path.parent.mkdir(exist_ok=True)
    nbf.write(nb,path)
    print("Created",path.name)


def main():
    save("01_constellation_poster.ipynb",[
        ("md", """# 01 · Explore the global constellation

**Goal:** move between a planet-scale overview, a mission record, its sensors and data products, and a contextual comparison.

This curated snapshot contains 13 representative platforms, not every EO satellite. Satellite positions and orbit rings are illustrative, not to scale, not orbital predictions, and not a live feed. Metadata was curated on **2026-11-02**.

Run the cells in order with **Run → Run All Cells**. JupyterLite runs Python in your browser. Its first kernel launch needs internet access to download Pyodide; the standalone poster itself works offline. No account, API key, live API, or pip installation is needed for these lessons.

If notebook HTML is not displayed, open the [standalone poster](https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/explorer/) or trust your own local notebook after reviewing it."""),
        ("code", "from eo_guide import load_catalog, poster\ncatalog = load_catalog()\nprint(catalog['scope'])\nprint('Metadata verified:', catalog['verified'])"),
        ("code", "poster(height=1150)"),
        ("md", """## A guided investigation

1. Select **Landsat 8** in the map, then select it again to contract the metadata. Reopen it and unfold **TIRS**, then its product.
2. Hover over or keyboard-focus **Sentinel-1C** in the mission index. Observe the corresponding map highlight. Select it and inspect C-SAR.
3. Pin Landsat 8, Sentinel-1C and GOES-19. Read the comparison matrix below the table. Explain why a radar resolution, a thermal native resolution and an ABI nadir resolution are not interchangeable.
4. Filter by **hyperspectral**. Inspect retired EO-1 and operational EnMAP; distinguish historical archive access from new acquisition capability.
5. Return to **Overview**, reset filters, export the filtered CSV and print the poster. Choose A1 landscape and enable background graphics in your browser print settings. Long comparison panels may add pages.

All map functions have keyboard controls: **Tab**, **Enter/Space**, and **Escape**. Search, table names and pins provide parallel access to all platform records. Textual legends and different central shapes complement colour.

## Explain your choice

Pick a question (vegetation condition, surface temperature, or radar change). Identify a sensor, product, processing level, spatial context, temporal limitation and source. State one thing that sensor cannot establish by itself.

**Evidence:** mission/sensor citations and access dates are embedded in every detail panel, comparison, and source registry. The map uses [Natural Earth](https://www.naturalearthdata.com/about/terms-of-use/) public-domain land geometry; satellite icons and the poster interface are original vectors. The supplied raster reference is not reproduced."""),
    ])
    save("02_sensor_comparison.ipynb",[
        ("md", """# 02 · Ask the catalog a scientific question

**Goal:** filter the same local records that drive the poster, preserve unknown values, and compare measurements with their contexts. The code uses the Python standard library plus the notebook's built-in display support.

Facts are curated summaries of official documentation, not observations downloaded from satellites. All records include citations and a verification date."""),
        ("code", "from eo_guide import load_catalog, query, comparison\ncatalog = load_catalog()\nfor family in sorted({s['type'] for s in catalog['satellites']}):\n    print(family, ':', ', '.join(s['name'] for s in query(catalog, family=family)))"),
        ("code", "# Change property_name or agency to investigate another capability.\nselected = query(catalog, property_name='surface reflectance')\n[(s['name'], s['agency'], s['status']) for s in selected]"),
        ("code", "comparison(catalog, ['landsat-8', 'sentinel-1c', 'enmap', 'goes-19'])"),
        ("md", """## Keep uncertainty visible

`None` means **not curated**. A geostationary imager's scan interval is deliberately not stored as an orbital repeat. Likewise, an observation plan or a cloud-free revisit cannot be deduced from orbital period."""),
        ("code", "unknown = [s['name'] for s in catalog['satellites'] if s['orbit']['repeat_days'] is None]\nprint('No numeric repeat curated:', unknown)\nmission = next(s for s in catalog['satellites'] if s['id'] == 'landsat-8')\nfor field, source_ids in mission['evidence'].items():\n    print(field)\n    for sid in source_ids:\n        source = catalog['sources'][sid]\n        print(' ', source['publisher'], source['url'], 'accessed', source['accessed'])"),
        ("md", """## Export a contextual comparison

This export is a local file in the notebook filesystem. In JupyterLite, right-click it in the file browser to download it. Notebook browser storage is separate from the checked-out repository."""),
        ("code", "import csv\nfrom pathlib import Path\nexport_path = Path('my-sensor-comparison.csv')\nwith export_path.open('w', newline='', encoding='utf-8') as stream:\n    writer = csv.writer(stream)\n    writer.writerow(['mission', 'measurement', 'spatial_context', 'temporal_context', 'source_urls'])\n    for s in selected:\n        for instrument in s['sensors']:\n            writer.writerow([s['name'], '; '.join(instrument['observes']), instrument['spatial'], s['orbit']['temporal_note'], '; '.join(catalog['sources'][sid]['url'] for sid in instrument['sources'])])\nprint('Saved', export_path)"),
        ("md", """## Exercise

Compare a flooding question with a crop-stress question. Which measurement is useful, which product needs preprocessing, and what field observations are needed? Do not rank platforms only by their smallest pixel number.

Sources: [USGS Landsat 8](https://www.usgs.gov/landsat-missions/landsat-8), [Sentinel-1 mission](https://sentiwiki.copernicus.eu/web/s1-mission), [EnMAP mission](https://www.enmap.org/mission/) and [NOAA ABI products](https://www.ncei.noaa.gov/products/goes-terrestrial-weather-abi-glm); the catalog contains the complete record-level registry."""),
    ])
    save("03_hyperspectral_land.ipynb",[
        ("md", """# 03 · Hyperspectral land and coastal systems

**Goal:** explain how spectral sampling changes the information available for interpretation, and distinguish radiance from surface reflectance.

This lesson adapts concepts from McCullum, Torres-Perez and Bengtsson, **NASA ARSET, 26 January 2021**, *Hyperspectral Data for Land and Coastal Systems, Part 2*. The supplied PDF's application examples include crops, forest restoration, invasive species, drought and mineral mapping (pp. 8-20). Hyperion characteristics are on p. 24; product levels and correction are on pp. 25-26. [Original NASA training PDF](https://appliedsciences.nasa.gov/sites/default/files/2021-01/Hyperspectral_Part2_Final.pdf).

The exercises below use **invented curves**, not Hyperion, EnMAP, field spectra or a species-identification model. No figures from the training slides are copied. Some source examples use **airborne AVIRIS or HyMap**, which are not satellites."""),
        ("code", "from eo_guide import synthetic_reflectance, spectrum_demo, load_catalog, comparison\nspectrum_demo()"),
        ("code", "# Compare point samples and a simple top-hat band average.\n# Actual instruments require their measured spectral response functions.\ndef band_average(center_nm, width_nm):\n    samples = range(int(center_nm-width_nm/2), int(center_nm+width_nm/2)+1)\n    return sum(synthetic_reflectance(w) for w in samples) / len(samples)\nfor width in (10, 40, 160):\n    print(f'Invented band centred at 1450 nm, width {width} nm: {band_average(1450, width):.3f}')"),
        ("code", "catalog = load_catalog()\ncomparison(catalog, ['eo-1', 'enmap', 'sentinel-2b'])"),
        ("md", """## Radiance is not reflectance

NASA ARSET explains that Hyperion Level-1 data contain radiance. Radiometric and geometric processing do not, by themselves, produce surface reflectance. Atmospheric correction requires a physical model and appropriate inputs. Water absorption, aerosols, illumination, viewing geometry, terrain, bad bands and sensor noise complicate interpretation.

This notebook does **not** implement FLAASH or claim that rescaling radiance is atmospheric correction. Its synthetic dimensionless reflectance curve is only a teaching device.

## Archive workflow to investigate

1. Search [USGS EarthExplorer](https://earthexplorer.usgs.gov/) for historical EO-1 Hyperion scenes using area, date and cloud constraints; downloading may require registration.
2. Inspect product level, band validity and radiometric/geometric metadata.
3. Choose and document a suitable atmospheric correction workflow before interpreting surface reflectance.
4. Validate vegetation, mineral or water interpretations with independent observations.

For current hyperspectral data, inspect [EnMAP data access](https://www.enmap.org/data_access/). Off-nadir opportunity and completed acquisitions are different concepts. Large GeoTIFF/hyperspectral cubes may exceed browser memory; use appropriate desktop or cloud tools for full scenes.

**Historical dates:** ARSET reports hyperspectral data through 22 February 2017; NASA reports spacecraft shutdown on 30 March 2017. These describe different events. [NASA retirement account](https://www.nasa.gov/technology/nasa-says-goodbye-to-a-pathfinder-earth-satellite-after-17-years/).

## Exercise

Increase the simulated bandwidth. Which absorption feature becomes less distinct? Explain why this does not prove that one satellite can identify a particular species, or why one index alone is a reliable drought diagnosis."""),
    ])
    save("04_orbits_and_resolution.ipynb",[
        ("md", r"""# 04 · Orbits, cadence and resolution

**Goal:** distinguish orbital period, ground-track repeat, observation opportunity, scan cadence and product latency.

The poster uses **schematic** positions. This notebook adds a **generic circular-orbit simulation** with an arbitrary initial longitude. It has no mission state vectors, epoch, TLEs, SGP4 propagator or real satellite tracking. No path is a coverage or acquisition prediction.

For the illustrative calculations we use a mean spherical Earth radius of 6371 km, gravitational parameter 398600.4418 km³/s², and sidereal rotation period 86164.0905 s, conventional approximate model constants. The point-mass period follows Kepler's two-body relation, $T=2\pi\sqrt{(R+h)^3/\mu}$. These model assumptions omit oblateness, nodal precession, drag and maneuvers. [NASA Earth fact sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html); [IERS numerical standards](https://iers-conventions.obspm.fr/content/tn36.pdf)."""),
        ("code", "from eo_guide import orbital_period_minutes, orbit_demo\nfor altitude in (400, 705, 786, 35786):\n    print(f'{altitude:>5} km -> {orbital_period_minutes(altitude):7.1f} min (circular model)')"),
        ("code", "orbit_demo()"),
        ("md", """## Interpret the geometry

Move inclination from 30° to 98°. For a circular orbit, the maximum sub-satellite latitude is approximately the smaller of inclination and 180° minus inclination. Changing altitude changes the model period; the rotating Earth shifts successive ground tracks.

A sun-synchronous orbit maintains an approximately consistent local solar overpass time through precession. The simple model above does not simulate that precession. A geostationary orbit requires near-zero inclination, near-zero eccentricity and the Earth's sidereal period; altitude alone is insufficient.

## Do not substitute period for revisit

Landsat's approximately 99-minute orbit and 16-day repeat are different quantities. The nominal Sentinel-2 pair's five-day revisit is not the ten-day cycle of one platform. ABI's ten-minute full-disk scan is neither an orbit period nor a low-Earth-orbit revisit. Usable optical samples also depend on clouds and illumination. [USGS](https://www.usgs.gov/landsat-missions/landsat-8), [SentiWiki](https://sentiwiki.copernicus.eu/web/s2-mission), [GOES-R guide](https://www.goes-r.gov/downloads/resources/documents/Beginners_Guide_to_GOES-R_Series_Data.pdf).

## Pixel-grid exercise

A 100 m thermal measurement resampled to a 30 m grid still contains approximately 100 m native spatial information. Native sampling, optical resolution, product grid spacing and minimum detectable feature size need separate descriptions."""),
        ("code", "native_m, grid_m = 100, 30\nprint('Output grid cells per nominal native-pixel area:', round((native_m/grid_m)**2, 2))\nprint('More cells do not create new independent thermal observations.')"),
        ("md", """## Exercise

Why could two missions with the same orbital period deliver different usable revisit intervals? Give one geometric, one operational and one environmental reason. Then explain why smaller pixels alone cannot make radar backscatter comparable to optical surface reflectance."""),
    ])
    save("05_observation_to_public_health.ipynb",[
        ("md", """# 05 · From an observation to a public-health question

**Goal:** follow a source-backed application chain, distinguish an observed association from an intervention, and identify the role of contextual geospatial data.

This lesson bundles no personal, clinical or address-level health data. It teaches evidence interpretation, not medical advice or an exposure model for individuals."""),
        ("code", "from eo_guide import load_catalog\ncatalog = load_catalog()\napplication = next(a for a in catalog['applications'] if a['id'] == 'philadelphia-heat')\nprint(application['name'], '-', application['evidence_type'])\nprint(application['historical_platform'])\nfor index, step in enumerate(application['chain'], 1):\n    print(index, step)\nprint('Limitations:', application['limitations'])\nfor sid in application['sources']:\n    print(catalog['sources'][sid]['url'])"),
        ("md", """## Philadelphia: trace the original study

Johnson, Wilson and Luber (2009) studied Philadelphia's 1993 extreme heat event using Landsat TM thermal context, socioeconomic indicators and heat-related mortality from Pennsylvania vital records. They compared logistic-regression risk models at census-tract scale. Their combined approach supported finer spatial characterization than socioeconomic indicators alone in that study. This is a retrospective observational finding, not proof that a new explorer prevents deaths.

**Chronology matters:** Landsat 8 and 9 launched long after the study's event and publication. They are modern sensor analogues in this teaching catalog, not the actual data sources for the 1993 event. The catalog does not assign the study's historical sensor to a present-day spacecraft. Land-surface temperature is not ambient air temperature, personal dose or a causal mechanism by itself.

Source: [Johnson et al., 2009, DOI 10.1186/1476-072X-8-57](https://doi.org/10.1186/1476-072X-8-57). NCEH coauthorship is distinct from program ownership or leadership of every related application.

## Two other evidence patterns

| Record | EO-to-health pathway | Attribution / boundary |
|---|---|---|
| HELIX-Atlanta | Satellite air-quality observations and monitoring data → modeled PM2.5 → linkage with asthma clinic visits in five Atlanta-area counties | NCEH / NASA collaboration described as a feasibility and surveillance pilot, not a mature operational health service. [NASA NTRS abstract, 20070032007](https://ntrs.nasa.gov/citations/20070032007). |
| Jackson, Mississippi (2019) | Remotely sensed aerosol optical depth plus other inputs → modeled daily PM2.5 → asthma morbidity time series | 2003-2011 patient records were aggregated to a 0.1° grid. The surveillance-data support role of NCEH does not make this an NCEH-led paper. [Chang et al., CDC Stacks](https://stacks.cdc.gov/view/cdc/126808). |

These summaries are evidence records, not executable replications. The small catalog does not invent spacecraft-specific lineage where the source summary has not established it.

## OpenStreetMap is contextual data

Blood-storage facilities can use [`amenity=blood_bank`](https://wiki.openstreetmap.org/wiki/Tag:amenity%3Dblood_bank) or `healthcare=blood_bank`; donation facilities can use [`healthcare=blood_donation`](https://wiki.openstreetmap.org/wiki/Tag:healthcare%3Dblood_donation). These are mapped facilities, **not satellite observations or current blood inventories**. No OSM extract is bundled. Future data reuse needs OSM attribution and ODbL terms.

## Evidence audit exercise

For one application, fill in: design, geography, observation period, EO input, health-data source, spatial-linkage unit, finding, uncertainty and publication. Which claims are directly reported? Which are your proposed extensions? What validation would be required before using them for decisions?"""),
        ("code", "# A local evidence worksheet; replace 'Not yet assessed' after reading the source.\nworksheet = {key: 'Not yet assessed' for key in [\n    'study_design', 'geography', 'time_period', 'eo_input', 'health_data_source',\n    'spatial_linkage', 'principal_finding', 'limitations', 'publication']}\nworksheet['publication'] = 'https://doi.org/10.1186/1476-072X-8-57'\nworksheet"),
    ])
    save("06_knowledge_graph_and_curation.ipynb",[
        ("md", """# 06 · Curate evidence and connect the knowledge graph

**Goal:** inspect a small application profile, validate its relationships and export interoperable records without a graph database.

The local JSON is the editorial source. `data/catalog.jsonld` in the repository is a generated semantic view. Satellites are [SOSA](https://www.w3.org/TR/vocab-ssn/) platforms, selected instruments are sensors, curated products are [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) datasets, and evidence links use [PROV-O](https://www.w3.org/TR/prov-o/). A **capability** is not an actual observation; no `sosa:Observation` instances are fabricated.

[SWEET](https://github.com/ESIPFed/sweet), [NASA GCMD keywords](https://www.earthdata.nasa.gov/learn/find-data/idn/gcmd-keywords), [GeoSPARQL](https://www.ogc.org/standard/geosparql/), and [Workflow Run RO-Crate](https://www.researchobject.org/workflow-run-crate/profiles/workflow_run_crate/) are extension points. The pilot does not claim validated mappings, spatial reasoning, or a reproducible execution crate.

[GEOSS](https://old.earthobservations.org/geoss.php) supplies a system-of-systems discovery context. The [GEO Knowledge Hub](https://gkhub.earthobservations.org/doc/faq) can inform future reusable application packages. Neither is treated as the one ontology for every entity, and no live federation is required for the offline poster."""),
        ("code", "from eo_guide import load_catalog\ncatalog = load_catalog()\nids = [s['id'] for s in catalog['satellites']]\nassert len(ids) == len(set(ids))\nfor satellite in catalog['satellites']:\n    assert satellite['verified'] and satellite['status'] in {'operational', 'retired', 'planned', 'unverified'}\n    for source_id in satellite['sources']:\n        assert source_id in catalog['sources']\n    for sensor in satellite['sensors']:\n        for source_id in sensor['sources']:\n            assert source_id in catalog['sources']\nprint('Unique platform IDs, explicit statuses and source references verified.')"),
        ("code", "# Export a small, explicit platform/sensor view using standard vocabulary terms.\nimport json\nfrom pathlib import Path\nbase = 'https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/id/'\nmission = next(s for s in catalog['satellites'] if s['id'] == 'landsat-8')\ngraph = {\n    '@context': {'sosa': 'http://www.w3.org/ns/sosa/', 'rdfs': 'http://www.w3.org/2000/01/rdf-schema#', 'label': 'rdfs:label'},\n    '@graph': [{'@id': base + mission['id'], '@type': 'sosa:Platform', 'label': mission['name'],\n                'sosa:hosts': [{'@id': base + mission['id'] + '/' + i['id']} for i in mission['sensors']]}]\n}\ngraph['@graph'].extend({'@id': base + mission['id'] + '/' + i['id'], '@type': 'sosa:Sensor', 'label': i['name']} for i in mission['sensors'])\nPath('my-platform-graph.jsonld').write_text(json.dumps(graph, indent=2), encoding='utf-8')\ngraph"),
        ("md", """## Add a satellite responsibly

1. Choose an official operator, mission or instrument source. Record its exact URL, title, publisher and access date.
2. Create a stable platform ID, explicit status, status qualifier and verification date. Do not substitute a design lifetime for a verified mission end date.
3. Record orbit, instruments, observed properties, native resolution/sampling, temporal definitions, coverage and products with citations by field group. Use `null` or an explanatory string for uncurated values.
4. Validate `data/catalog.json` against `data/catalog.schema.json` using `python scripts/validate.py`, then run `python scripts/build.py --execute` and browser checks.
5. Audit the source terms before copying an image or dataset. Linking a source and redistributing its content have different requirements.

Refresh changing status and access records at least each teaching term, and record what changed. The current snapshot is intentionally finite. Expand toward NOAA/JPSS, Metop, Sentinel-3/5P, CBERS, KOMPSAT, SAOCOM and additional national/commercial missions only after curation.

## Exercise

Explain the difference between a sensor's capability, an observation, a dataset and an analysis result. Draft one new record with at least one explicitly unknown field. Identify which semantic mappings you can support and which remain unverified."""),
    ])


if __name__=="__main__":
    main()
