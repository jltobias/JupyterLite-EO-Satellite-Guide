# Application profile and evidence model

The authoritative editorial source is `data/catalog.json`, validated against `data/catalog.schema.json`. `data/catalog.jsonld` is a generated semantic view; it is not a second manually maintained catalog. All IDs are stable lowercase slugs. Unknown numeric values use JSON `null`; unknown contextual text explicitly says not curated. Distinguish a mission's nominal specifications from its operating status and from the availability of a particular product.

| Entity | Required context | Relationships |
|---|---|---|
| Platform | ID, operator, region, purpose, launch/end if curated, qualified status, verification date, nominal orbit | Hosts selected sensors; documented by sources |
| Sensor | Method, observed properties, spectral characteristics, native spatial resolution/sampling, coverage, citations | Observes properties; linked to products |
| Product | Name, level, access URL, processing qualifier, sources | Distributed by provider; derived through documented processing |
| Application | Evidence type, measurement-to-use chain, source, limitations | Published study or explicitly potential teaching workflow |
| Source | Exact URL, title, publisher, accessed date; publication date and locator when available | Supports field groups through `evidence` and nested source IDs |

Allowed statuses are `operational`, `retired`, `planned` and `unverified`. The starter catalog includes operational snapshots, a retired archive mission and an unverified service-status record. A planned status is supported without inventing a planned mission merely to populate that category. A source snapshot is not a real-time instrument health assessment.

## Semantic export

The export uses [SOSA/SSN](https://www.w3.org/TR/vocab-ssn/) `sosa:Platform`, `sosa:Sensor`, `sosa:hosts`, `sosa:observes` and `sosa:ObservableProperty`. Products use [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) `dcat:Dataset` and landing pages. Source lineage uses [PROV-O](https://www.w3.org/TR/prov-o/) `prov:wasDerivedFrom`. These terms provide a small application profile, not a comprehensive mission ontology. No actual observation instances or scientific analysis results are manufactured from capability records.

[SWEET](https://github.com/ESIPFed/sweet), [GCMD keywords](https://www.earthdata.nasa.gov/learn/find-data/idn/gcmd-keywords), [GeoSPARQL](https://www.ogc.org/standard/geosparql/) and [Workflow Run RO-Crate](https://www.researchobject.org/workflow-run-crate/profiles/workflow_run_crate/) are documented extension points. The pilot has no asserted cross-vocabulary equivalences, spatial query engine, reasoning engine, or execution crate. Such additions require curated concept mappings and actual workflow-run evidence.

[GEOSS](https://old.earthobservations.org/geoss.php) is the system-of-systems interoperability/discovery context. The [GEO Knowledge Hub](https://gkhub.earthobservations.org/doc/faq) can inform curated application packages. Live federation is outside the offline explorer.

## Curation procedure

Prefer the operator, instrument handbook and product specification over a secondary poster. Record citations for mission, orbit, sensors and products; sensor/product entries carry their own evidence. Cite a study for a claimed application, or mark it as potential. Refresh service/status facts each teaching term and retain the old snapshot in Git history. Log ambiguities and resolve them explicitly instead of silently choosing a number. The ARSET Hyperion acquisition-end date and NASA spacecraft shutdown date, for example, describe different events.

Run `python scripts/validate.py` and rebuild after changing data. Browser tests verify the coupled views and offline artifact; they do not establish scientific validity, complete accessibility conformance, or learning effectiveness.


## Research discovery profile

`data/research-topics.json` supplies eight curated concepts, aliases, qualified candidate-platform relations and nine exact provider routes. `data/research-ontology.ttl` defines the original schema; the generated JSON-LD includes SKOS concepts, SOSA observables, qualified platform links, orbit types, DCAT collections/endpoints and PROV source evidence. Generic imported instrument arrays do not assert that each instrument is hosted on every platform. Mission groups use a separate class. There are no equivalence assertions to FieldWork, fabricated observations or acquisition receipts. See [research discovery](research-discovery.md) for competency questions, matching limits, sharing and the downstream workflow.

`eo:studyArea` relates a research question to a declared GeoSPARQL Feature/Geometry; notebook 08 demonstrates CRS84 WKT without inferring an area from a satellite footprint. `data/orbit-types.json` holds the shared orbit palette and SSO/LEO hierarchy. `data/geometry-presets.json` holds eight independently qualified nominal examples. A geometry scenario is a teaching model, not a SOSA Observation, spacecraft state vector or acquired-data receipt. The `eo-study-area/1` brief keeps the question, bbox, preset, arbitrary phase, archive dates and assumptions together. See [study-area methods](swaths.md).
