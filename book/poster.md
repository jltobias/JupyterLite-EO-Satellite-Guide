# Interactive constellation poster

<a href="../explorer/index.html">Open the full-width poster</a> for the most comfortable map and table view. <a href="../lab/index.html?path=01_constellation_poster.ipynb">Open the executable notebook</a> to embed it in your own investigation.

```{raw} html
<iframe src="../explorer/index.html" title="Global EO interactive satellite constellation poster" height="1250" loading="lazy"></iframe>
```

## Interaction guide

Select a satellite or table name to expand its metadata. Select it again, use Close or press Escape to contract the panel. Open a sensor to inspect spatial and spectral characteristics, coverage, observed properties, products and citations. Open a product to inspect its processing level and data access route. The Overview button restores the full atlas after zooming.

Hover or keyboard-focus a map object or table control to highlight the corresponding platform in both views. Pins mark map objects and populate the comparison matrix. Pinned selections persist across filters, so you can compare missions from different filtered subsets. Reset filters restores the catalog; Clear pins resets the comparison.

All platforms are accessible through search, standard buttons and the table. Central icon shapes and textual labels complement family colours. Tab traverses controls; Enter/Space selects; Escape closes details. Browser zoom remains available. A full screen-reader and classroom usability assessment remains future work.

## Print and export

The Print poster control restores the atlas overview and uses an A1 landscape stylesheet. The print view includes the constellation, mission index and comparison. In the browser print dialog choose A1 landscape, enable backgrounds and check the preview. A large comparison can require additional pages. Export filtered CSV includes full spatial/temporal qualifiers, verification dates and source URLs.

Satellite markers are **schematic slots**, not points projected from orbital elements. The top map uses bundled Natural Earth land geometry. Rings distinguish LEO and GEO conceptually and do not encode scaled orbital radii or exact inclinations. Notebook 04 explores generic orbit geometry separately.
