"""Build the shared offline poster, executable notebooks, Book and JupyterLite site.

Run from any directory: python scripts/build.py [--prepare] [--execute].
Only generated project paths are written; source notebooks/data are never removed.
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from importlib.metadata import distribution
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def reset_generated(directory):
    resolved=directory.resolve()
    if not resolved.is_relative_to(ROOT) or directory.is_symlink() or resolved==ROOT:
        raise ValueError(f"Unsafe generated output path: {directory}")
    if directory.exists():
        shutil.rmtree(resolved)


def prepare():
    catalog_text = (ROOT / "data/catalog.json").read_text(encoding="utf-8")
    catalog = json.loads(catalog_text)
    land = json.loads((ROOT / "assets/ne_110m_land.geojson").read_text(encoding="utf-8"))
    payload = "window.EO_CATALOG=" + json.dumps(catalog, ensure_ascii=True) + ";\nwindow.EO_LAND=" + json.dumps(land, separators=(",", ":")) + ";\n"
    write(ROOT / "explorer/catalog.js", payload)
    template = (ROOT / "explorer/index.html").read_text(encoding="utf-8")
    css = (ROOT / "explorer/style.css").read_text(encoding="utf-8")
    js = (ROOT / "explorer/app.js").read_text(encoding="utf-8")
    document = template.replace('<link rel="stylesheet" href="style.css">', f"<style>{css}</style>")
    document = document.replace('<script src="catalog.js"></script>', f"<script>{payload}</script>")
    document = document.replace('<script src="app.js"></script>', f"<script>{js}</script>")
    document = document.replace('href="../book/', 'href="https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/book/')
    document = document.replace('href="../lab/', 'href="https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/lab/')
    document = document.replace("<!doctype html>", "<!doctype html>\n<!--\n" + (ROOT / "LICENSE").read_text(encoding="utf-8") + "\n-->", 1)
    write(ROOT / "downloads/eo-explorer.html", document)
    write(ROOT / "notebooks/support/eo-explorer.html", document)
    write(ROOT / "notebooks/data/catalog.json", catalog_text)
    shutil.copy2(ROOT / "src/eo_guide.py", ROOT / "notebooks/eo_guide.py")
    # Sources are kept next to each notebook in both the book and the Lite filesystem.
    for directory in (ROOT / "book/notebooks", ROOT / "_build/lite-content"):
        reset_generated(directory)
        shutil.copytree(ROOT / "notebooks", directory, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("__pycache__", ".ipynb_checkpoints"))
    refs = ["# Sources and evidence\n", "This registry is generated from the same catalog used by the poster. Dates record the curation snapshot, not a real-time operational check.\n"]
    for key, source in catalog["sources"].items():
        refs.append(f"({key})=\n## {key}\n\n{source['publisher']}. [{source['title']}]({source['url']}). Accessed {source['accessed']}. {source.get('locators', '')}\n")
    refs.append("## Software and semantic standards\n\nSee [Attributions](attributions.md) and the [application profile](data-model.md) for software, map, reference-image and ontology credits.\n")
    write(ROOT / "book/references.md", "\n".join(refs))
    export_graph(catalog)
    # The splash is an original vector drawing built from our own UI and public-domain geography.
    splash(catalog, land)
    print("Prepared offline poster, notebook support files, source registry, JSON-LD and splash.")


def export_graph(catalog):
    base = "https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/id/"
    nodes = []
    for s in catalog["satellites"]:
        nodes.append({"@id": base+s["id"], "@type": "sosa:Platform", "label": s["name"],
                      "sosa:hosts": [{"@id": base+s["id"]+"/"+i["id"]} for i in s["sensors"]],
                      "prov:wasDerivedFrom": [{"@id": catalog["sources"][sid]["url"]} for sid in s["sources"]]})
        for i in s["sensors"]:
            nodes.append({"@id": base+s["id"]+"/"+i["id"], "@type": "sosa:Sensor", "label": i["name"],
                          "sosa:observes": [{"@id": base+"property/"+p.replace(" ", "-")} for p in i["observes"]],
                          "prov:wasDerivedFrom": [{"@id":catalog["sources"][sid]["url"]} for sid in i["sources"]]})
            for k,p in enumerate(i["products"]):
                nodes.append({"@id":base+s["id"]+"/"+i["id"]+f"/product/{k}", "@type":"dcat:Dataset", "label":p["name"],
                              "dcat:landingPage":{"@id":p["access"]},
                              "dcterms:relation":{"@id":base+s["id"]+"/"+i["id"]},
                              "prov:wasDerivedFrom":[{"@id":catalog["sources"][sid]["url"]} for sid in p["sources"]]})
    properties = sorted({p for s in catalog["satellites"] for i in s["sensors"] for p in i["observes"]})
    nodes.extend({"@id":base+"property/"+p.replace(" ", "-"),"@type":"sosa:ObservableProperty","label":p} for p in properties)
    graph = {"@context":{"sosa":"http://www.w3.org/ns/sosa/","dcat":"http://www.w3.org/ns/dcat#","prov":"http://www.w3.org/ns/prov#","dcterms":"http://purl.org/dc/terms/","rdfs":"http://www.w3.org/2000/01/rdf-schema#","label":"rdfs:label"},"@graph":nodes}
    write(ROOT / "data/catalog.jsonld", json.dumps(graph, indent=2)+"\n")


def splash(catalog, land):
    from html import escape
    colors = {"multispectral":"#60dfc4","radar":"#bb9cf5","hyperspectral":"#f29d81","weather":"#84b7f6","ocean":"#f2d879"}
    path = []
    for feature in land["features"]:
        polygons = [feature["geometry"]["coordinates"]] if feature["geometry"]["type"]=="Polygon" else feature["geometry"]["coordinates"]
        for polygon in polygons:
            for ring in polygon:
                path.append("".join(f"{'M' if i==0 else 'L'}{280+(lon+180)/360*1040:.1f},{285+(90-lat)/180*360:.1f}" for i,(lon,lat) in enumerate(ring))+"Z")
    nodes=[]
    for s in catalog["satellites"]:
        x=100+s["display"]["x"]*1.17; y=200+s["display"]["y"]*.95
        c=colors[s["type"]]
        nodes.append(f'<g transform="translate({x:.1f} {y:.1f})"><circle r="17" fill="#0e2539" stroke="{c}"/><path d="M-12 -5H-5V5H-12ZM5 -5H12V5H5ZM-5 0H5" fill="none" stroke="{c}"/><rect x="-4" y="-4" width="8" height="8" fill="{c}"/><text y="36" text-anchor="middle" fill="#e7f2f6" font-size="13">{escape(s['name'])}</text></g>')
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000" role="img" aria-labelledby="title desc"><title id="title">Global Earth Observation Satellites</title><desc id="desc">Original schematic world-map constellation of 13 representative EO platforms. Orbits and spacecraft positions are illustrative, not to scale or live.</desc><defs><radialGradient id="bg"><stop stop-color="#15374e"/><stop offset="1" stop-color="#071522"/></radialGradient></defs><rect width="1600" height="1000" fill="url(#bg)"/><g font-family="system-ui,Segoe UI,sans-serif"><text x="80" y="70" fill="#60dfc4" font-size="14" letter-spacing="4">GLOBAL EO / THE SATELLITE GUIDE</text><text x="80" y="140" fill="#eef5f8" font-size="50" letter-spacing="-1">Global Earth Observation Satellites</text><text x="80" y="180" fill="#a7c1cf" font-size="19">One planet. Many ways to see it.</text><path d="{''.join(path)}" fill="#276174" stroke="#508998" stroke-width=".5" opacity=".7"/><ellipse cx="800" cy="480" rx="580" ry="240" fill="none" stroke="#60dfc4" opacity=".4"/><ellipse cx="800" cy="510" rx="675" ry="290" fill="none" stroke="#f2c17a" stroke-dasharray="7 9" opacity=".6"/>{''.join(nodes)}<text x="80" y="860" fill="#60dfc4" font-size="16" letter-spacing="2">EXPLORE THE CONSTELLATION → COMPARE SENSORS → FOLLOW THE EVIDENCE</text><path d="M80 890H1520" stroke="#365264"/><text x="80" y="925" fill="#b0c4d2" font-size="14">13 representative platforms · interactive poster · executable notebooks · Jupyter Book + JupyterLite</text><text x="80" y="958" fill="#819cac" font-size="12">Illustrative positions and orbit rings, not to scale. Original vectors: MIT. Made with Natural Earth (public domain). Catalog: 2026-11-02.</text></g></svg>'''
    write(ROOT / "assets/global-eo-splash.svg", svg)


def execute_notebooks():
    import nbformat
    from nbclient import NotebookClient
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    for path in sorted((ROOT / "notebooks").glob("*.ipynb")):
        nb=nbformat.read(path, as_version=4)
        NotebookClient(nb, timeout=120, kernel_name="python3", resources={"metadata":{"path":str(ROOT / "_build/lite-content")}}).execute()
        # Keep executed outputs in the book only; source notebooks remain clean and diffable.
        nbformat.write(nb, ROOT / "book/notebooks" / path.name)
        print("Executed", path.name)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare",action="store_true",help="Only prepare assets and content; no book/Lite build")
    parser.add_argument("--execute",action="store_true",help="Execute all notebooks into the book before building")
    args=parser.parse_args()
    prepare()
    if args.execute:
        execute_notebooks()
    if args.prepare:
        return
    book_output=ROOT / "_build/book-output"
    reset_generated(book_output)
    subprocess.run([sys.executable,"-c","from jupyter_book.cli.main import main; main()","build",str(ROOT / "book"),"--path-output",str(book_output),"--all","--warningiserror","--nitpick","--keep-going"],check=True,cwd=ROOT)
    # Lite owns and may recreate its entire output directory. Keep it isolated
    # from Book/explorer outputs, then assemble the public site after both builds.
    lite_output=ROOT / "_build/lite-site"
    if lite_output.is_symlink() or not lite_output.resolve().is_relative_to(ROOT):
        raise ValueError("Unsafe Lite output path")
    # Discover the installed extension through its wheel metadata. Windows user
    # installs may live outside sys.prefix, which Lite does not scan by default.
    kernel_dist=distribution("jupyterlite-pyodide-kernel")
    kernel_path=next(Path(kernel_dist.locate_file(f)).resolve().parent for f in kernel_dist.files
                     if str(f).replace("\\","/").endswith("pyodide-kernel-extension/package.json"))
    config=json.loads((ROOT / "jupyter_lite_config.json").read_text(encoding="utf-8"))
    config["LiteBuildConfig"].update({"ignore_sys_prefix":True,"federated_extensions":[str(kernel_path)]})
    lite_config=ROOT / "_build/lite-build-config.json"
    write(lite_config,json.dumps(config,indent=2))
    subprocess.run([sys.executable,"-m","jupyterlite_core.app","build","--config",str(lite_config),"--contents",str(ROOT / "_build/lite-content"),"--output-dir",str(lite_output)],check=True,cwd=ROOT)
    site=ROOT / "_site"
    site.mkdir(exist_ok=True)
    shutil.copytree(lite_output,site,dirs_exist_ok=True)
    shutil.copytree(book_output / "_build/html",site / "book",dirs_exist_ok=True)
    for name in ("explorer","assets","data","downloads"):
        shutil.copytree(ROOT / name,site / name,dirs_exist_ok=True)
    for name in ("ATTRIBUTIONS.md","LICENSE"):
        shutil.copy2(ROOT / name,site / name)
    # The config loader reads the root index as well as jupyter-lite.json.
    # Preserve its required JSON element when replacing the default redirect.
    landing=(ROOT / "site/index.html").read_text(encoding="utf-8")
    landing=landing.replace("</head>",'<script id="jupyter-config-data" type="application/json">{}</script></head>')
    write(site / "index.html",landing)
    write(site / ".nojekyll", "")
    with zipfile.ZipFile(site / "downloads/eo-explorer-offline.zip","w",zipfile.ZIP_DEFLATED) as archive:
        archive.write(ROOT / "downloads/eo-explorer.html","eo-explorer.html")
        archive.write(ROOT / "ATTRIBUTIONS.md","ATTRIBUTIONS.md")
        archive.write(ROOT / "LICENSE","LICENSE")
        archive.write(ROOT / "data/catalog.json","data/catalog.json")
        archive.write(ROOT / "data/catalog.jsonld","data/catalog.jsonld")
    hashes={str(p.relative_to(ROOT)).replace("\\","/"):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT / "data/catalog.json",ROOT / "assets/ne_110m_land.geojson",ROOT / "downloads/eo-explorer.html"]}
    write(site / "build-manifest.json",json.dumps({"catalog_verified":"2026-11-02","sha256":hashes},indent=2)+"\n")
    print("Built _site. Serve with: python -m http.server 8000 --directory _site")


if __name__=="__main__":
    main()
