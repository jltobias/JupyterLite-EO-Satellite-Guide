# Run locally, publish and work offline

## Build and preview

From the repository root, using Python 3.11-3.13:

```bash
python -m pip install -r requirements.txt
python scripts/validate.py
python scripts/build.py --execute
python -m http.server 8000 --directory _site
```

Open `http://localhost:8000/`, the Book at `/book/intro.html`, the poster at `/explorer/`, and JupyterLite at `/lab/index.html?path=01_constellation_poster.ipynb`. Use HTTP for JupyterLite and the Book. To refresh only shared assets and content, use `python scripts/build.py --prepare`.

The build uses intentionally pinned **Jupyter Book v1**, in maintenance mode, for a reproducible Sphinx/MyST pipeline that does not require Node.js. See [Jupyter Book v1 documentation](https://jupyter-book.readthedocs.io/v1/intro.html). Upgrade the Book toolchain as a deliberate migration; do not install v2 into this build unchanged.

## Standalone explorer

Open `downloads/eo-explorer.html` directly from disk. Its map, catalog, styles, JavaScript, comparisons, filters, legends and citations are embedded. No CDN, fonts, tile service, analytics or data API is required. The build also creates `downloads/eo-explorer-offline.zip` in the site, with the HTML, attributions, license and catalog exports. Citation and data-access links need a network when followed.

Notebook 01 embeds exactly that offline HTML in an isolated `srcdoc` iframe. Notebooks 03 and 04 use similarly self-contained teaching simulations. This keeps browser interactions independent of a Python-to-JavaScript widget server.

## JupyterLite boundary

The default Pyodide kernel downloads its compatible runtime on first use. Browser caching can help later sessions but is not a promise of a fully offline first load. This build does **not** vendor the entire Python runtime. To make an offline JupyterLite distribution, follow [JupyterLite's offline archive guide](https://jupyterlite.readthedocs.io/en/stable/howto/configure/advanced/offline.html), vendor the runtime compatible with the pinned kernel, serve it locally and repeat first-load tests with networking disabled. The standalone poster already satisfies the plan's offline explorer requirement.

Files saved in JupyterLite live in browser storage, not in the source repository. Download edited notebooks and exports before clearing site data. A fresh incognito session can help verify published starter content after a catalog update.

## GitHub Pages

The checked-in workflow builds and validates the same `_site` artifact, then publishes it through GitHub Pages. In repository **Settings → Pages**, choose **GitHub Actions** as the source. Push this work to `main` to trigger deployment. The README links target `https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/`; they only become available after a successful Pages deployment. Building locally does not publish the repository.
