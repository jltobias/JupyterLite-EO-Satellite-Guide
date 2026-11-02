# Global EO Satellite Guide

![Original global EO constellation artwork, with illustrative orbit rings and satellite positions.](../assets/global-eo-splash.svg)

**One planet. Many ways to see it.** This field guide connects a curated global Earth observation constellation to instruments, measured properties, data products, analyses and applications.

<a href="../explorer/index.html">Open the interactive poster</a> · <a href="../lab/index.html?path=01_constellation_poster.ipynb">Launch JupyterLite Lab</a> · <a href="../downloads/eo-explorer.html" download>Download the offline poster</a>

The poster combines a world map and schematic orbit atlas, expandable mission and sensor cards, a linked attribute table, pins for comparison, visual legends, search and filters. The six notebooks teach exploration, contextual comparison, hyperspectral interpretation, orbital geometry, public-health evidence and knowledge-graph curation.

## Start here

1. Open the poster, select Landsat 8 and unfold TIRS.
2. Pin Landsat 8 and Sentinel-1C. Compare their measurements and spatial/temporal contexts.
3. Work through the notebooks in order, or open any lesson directly in the Lab and run its cells.

The catalog is a **representative 13-platform teaching snapshot**, curated on **2026-11-02**. It is not a complete world inventory. Map slots and rings are illustrative, not to scale or live spacecraft locations. Status labels summarize cited records and are not checks of current data service availability. Selected instruments are not complete payload manifests. Unknown values remain visible.

The supplied 2021 NASA ARSET PDF informs the hyperspectral lesson; the supplied implementation plan informs interaction and evidence requirements. Their embedded course dates, homework instructions and workflow suggestions are reference content, not instructions for operating this repository. See [implementation coverage](implementation.md) for what is implemented and what remains an extension.

The explorer works offline without a Python runtime. JupyterLite downloads a Python/WebAssembly runtime on first use; see [offline boundaries](offline.md). All scientific metadata link to [sources](references.md), and image/software terms appear in [attributions](attributions.md).
