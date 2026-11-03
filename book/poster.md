# Interactive constellation poster

<a href="../explorer/index.html">Open the full-width poster</a> for the most comfortable map and table view. <a href="../lab/index.html?path=01_constellation_poster.ipynb">Open the executable notebook</a> to embed it in your own investigation.

```{raw} html
<iframe src="../explorer/index.html" title="Global EO interactive satellite constellation poster" height="1250" loading="lazy" allowfullscreen></iframe>
```

## Interaction guide

The **Satellite legend** stays across the top while you scroll and in fullscreen. Orbit colors use plain-language labels; the sensor legend pairs each shape with its sensing family. **Active**, **Retired** and **Other statuses** switch those lifecycle layers on or off. **Layers** exposes individual lifecycle states and multiple mission-family switches: for example, show Sentinel and Landsat together while displaying only retired missions. Other filters and research questions still apply. The Status shortcut controls the same lifecycle switches. **Reset filters** restores all layers, while **Show all layers** changes only the layers.

Family layers are exclusive browsing groups so a record is not duplicated when several are enabled. Hosted Sentinel-4/5 missions follow the Sentinel layer. The NOAA-and-partners focus can span several browsing layers. Counts refer to catalog records and cited lifecycle snapshots. Pins persist when their layers are hidden, supporting comparisons across subsets.

Use **Full screen** beside the constellation or in the top navigation to open a linked workspace. The default **All matching records** overview displays the complete filtered inventory, with 13 table rows visible at a time. Hover/focus a mark to reveal its table page and highlight both views. **Mission family** starts a fresh Sentinel, Landsat or NOAA/partner view; **Locate a mission** opens a named record. Choose **Table page** for 13 larger, labeled symbols synchronized with the current table page. The atlas remains at the overview when selecting a row in fullscreen. See the [family rosters and source crosswalk](mission-coverage.md).

The workspace's **Filters**, **Details** and **Compare** controls expose the full filters, selected mission metadata and pinned comparison. Hover over a shortened table cell for its complete text. **Exit full screen** or **Escape** returns to the page while preserving filters and pins. If browser fullscreen is unavailable, the same workspace fits the current window. Narrow or short screens keep scrolling within the table pane so the constellation remains visible.

Select a satellite or table name to expand its metadata. Select it again, use Close or press Escape to contract the panel. Open a sensor to inspect spatial and spectral characteristics, coverage, observed properties, products and citations. Open a product to inspect its processing level and data access route. The Overview button restores the full atlas after zooming.

Hover or keyboard-focus a map object or table control to highlight the corresponding platform in both views. Pins mark map objects and populate the comparison matrix. Pinned selections persist across filters, so you can compare missions from different filtered subsets. Reset filters restores the catalog; Clear pins resets the comparison.

All platforms are accessible through search, standard buttons and the table. Central sensor shapes and textual labels complement orbit colours; the color selector also offers sensing-family colours. See the [orbit guide](orbit-guide.md) for the palette and SSO/LEO hierarchy. Tab traverses controls; Enter/Space selects; Escape closes details. Browser zoom remains available. A full screen-reader and classroom usability assessment remains future work.

## Print and export

The Print poster control restores the atlas overview and uses an A1 landscape stylesheet. The print view includes the constellation, mission index and comparison. In the browser print dialog choose A1 landscape, enable backgrounds and check the preview. A large comparison can require additional pages. Export filtered CSV includes full spatial/temporal qualifiers, verification dates and source URLs.

Satellite markers are **schematic slots**, not points projected from orbital elements. The top map uses bundled Natural Earth land geometry. Rings distinguish LEO and GEO conceptually and do not encode scaled orbital radii or exact inclinations. Notebook 04 explores generic orbit geometry separately.


Use **Research** to enter a question such as air quality and NO₂. Gold highlights mark potential matches, while hover/focus uses mint. The orbit label on each symbol also appears in the table and live brushing readout. **Previous / Next** pages the larger catalog in both views; see [research discovery](research-discovery.md) and the [coverage audit](stac-coverage.md).
