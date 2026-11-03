# Orbit colors and what they mean

The constellation uses **orbit colors by default**, with central **shapes for sensing families**. The same orbit color appears beside the linked table record. Choose *Color by → Sensing family* to recover the alternate encoding; orbit codes and table swatches remain available. Text labels, codes, shapes and source links carry information beyond color.

[ESA: Types of orbits](https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits) is the primary introductory reference, supplemented by [NASA's orbit guide](https://science.nasa.gov/earth/earth-observatory/catalog-of-earth-satellite-orbits/). The boundaries below describe orbital geometry, not sensor quality or data availability.

| Color / code | Meaning | Consequence to investigate |
|---|---|---|
| Teal · SSO | Sun-synchronous orbit, a near-polar LEO subtype whose orbital plane precesses to maintain similar local solar crossing time | More consistent solar timing helps comparison; seasons, clouds, terrain and look angle still change illumination |
| Blue · Other LEO | Curated low Earth orbit classes other than SSO; LEO extends to about 2,000 km | Low altitude can support fine spatial detail, but instrument design, swath, pointing and acquisition plans determine actual sampling |
| Gold · GEO | Circular equatorial orbit near 35,786 km with a sidereal-day period, about 23 h 56 min | Approximately fixed Earth view; scan cadence and regional coverage are separate from the orbital period |
| Purple · HEO | Highly elliptical orbit, with strongly varying altitude | Some designs, including Molniya, dwell near apogee over high latitudes; the orbit alone does not specify an imaging schedule |
| Coral · L1 | Trajectory near Sun–Earth L1, as used by DSCOVR | Earth distance is not a LEO altitude; the constellation's ring is not a physical representation of that trajectory |
| Gray · ? | Orbit uncurated in this catalog | A provider's platform mention or STAC `orbit_state` does not establish the full orbit class |

**SSO belongs to LEO.** Its separate color is a subtype distinction, not a disjoint altitude class. The *All LEO (including SSO)* filter includes both teal and blue records. *Other LEO* excludes SSO. Click a legend entry to filter both linked views and read its explanation. The supplied 600–800 km SSO range is a useful common example, not a universal definition: the cited Sentinel-5P reference orbit is about 824 km.

Period depends on altitude. In the spherical circular model used in the lessons, 160–2,000 km corresponds to roughly 88–127 minutes; the familiar 90–120 minute shorthand does not cover every LEO. An orbital period is not ground-track repeat, acquisition cadence, usable revisit, or product latency.

The [WMO OSCAR Arctica-M N1](https://space.oscar.wmo.int/satellites/view/arctica_m_n1) and [N2](https://space.oscar.wmo.int/satellites/view/arctica_m_n2) records support their HEO/Molniya classifications and nominal 12-hour periods. The provider's `ARCM1`/`ARCM2` platform identifiers are retained as stable catalog IDs, with readable Arktika names. No current ephemerides or operational status are inferred. [NASA JPL](https://science.jpl.nasa.gov/projects/dscovr/) supports DSCOVR's L1 classification.

Satellite slots, ring sizes and relative distances remain schematic. Color coding does not turn this poster into an orbit propagator or tracking service. The [study-area lab](swaths.md) separately explains its nominal teaching model, while optional STAC metadata footprints supply evidence about cataloged historical Items.
