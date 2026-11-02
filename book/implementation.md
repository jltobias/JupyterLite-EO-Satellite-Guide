# From the supplied plan to this implementation

The user's request governs the repository work. The supplied `earth-observation-explorer-plan.md` is a design reference. Its first implementation slice requested three contrasting platforms; this starter expands to thirteen while retaining explicit evidence and unknown values.

| Plan requirement | Implemented location |
|---|---|
| Local HTML/CSS/JS/SVG, no required live API | `explorer/`; generated standalone `downloads/eo-explorer.html` |
| Clickable constellation and expandable metadata | Satellite selection, inspector, nested sensor/product disclosures |
| Search by operator, status, orbit, sensor/property/application | Search plus six categorical filters |
| Zoom and a route back | Selection zoom, zoom controls, Overview, Escape |
| Multiple comparisons, preserve missing/incompatible values | Persistent pins and contextual comparison matrix |
| Linked table/map selection | Shared selected, brushed and pinned states in both views |
| Product and application evidence chains | Inspector pathways; notebooks 02, 05 and 06 |
| One traced health example | Philadelphia heat study, with historical Landsat lineage separated from modern analogues |
| HELIX, Jackson and OSM contextual examples | Notebook 05, with evidence and attribution boundaries |
| Offline package | Standalone HTML and build-generated ZIP; zero required remote assets for explorer |
| Sources and verification dates | Field groups, nested sources, complete source registry |
| Knowledge model | JSON Schema and generated SOSA/DCAT/PROV JSON-LD |
| Keyboard access | Native controls, SVG keyboard selection, table access, focus highlights, Escape |
| Browser learning environment | Six Python notebooks with shared local support files, packaged into JupyterLite and Jupyter Book |

## Explicit extension work

This is a working, curated starter rather than a complete inventory of every global EO platform. Further work includes full instrument manifests, more national and commercial constellations, verified planned-mission records, validated GCMD/SWEET mappings, optional geographic footprint queries and real workflow-run packages. Current application graphs are explanatory curated pathways; the lessons do not reproduce published epidemiological results or process real satellite cubes.

User testing is needed to establish classroom usefulness and accessibility across assistive technologies. A full offline JupyterLite/Pyodide distribution requires separately vendoring the compatible runtime. Current offline guarantees apply to the standalone explorer, not the first launch of the browser Python kernel.

The reference diagram's author and license could not be established. It is treated as visual inspiration, not as a factual catalog or redistributable asset. The replacement splash, icons and interface are original SVG/code, with public-domain Natural Earth geography.
