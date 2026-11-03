"""Build the shared offline poster, executable notebooks, Book and JupyterLite site.

Run from any directory: python scripts/build.py [--prepare] [--execute].
Only generated project paths are written; source notebooks/data are never removed.
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import re
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


def script_json(value):
    """Serialize provider metadata safely inside an HTML script element."""
    return json.dumps(value,ensure_ascii=True).replace("<", "\\u003c")


def reset_generated(directory):
    resolved=directory.resolve()
    if not resolved.is_relative_to(ROOT) or directory.is_symlink() or resolved==ROOT:
        raise ValueError(f"Unsafe generated output path: {directory}")
    if directory.exists():
        shutil.rmtree(resolved)


def version_explorer_assets(directory):
    """Keep HTML and its coupled catalog/modules consistent across cached deploys."""
    for name in ("index.html","swaths.html"):
        path=directory / name
        text=path.read_text(encoding="utf-8")
        def version(match):
            relative=match.group(2)
            asset=(directory / relative).resolve()
            if not asset.is_relative_to(directory.resolve()) or not asset.is_file():
                return match.group(0)
            digest=hashlib.sha256(asset.read_bytes()).hexdigest()[:12]
            return f'{match.group(1)}="{relative}?v={digest}"'
        text=re.sub(r'(src|href)="([^":?#]+\.(?:js|css))"',version,text)
        write(path,text)


def prepare():
    catalog_text = (ROOT / "data/catalog.json").read_text(encoding="utf-8")
    catalog = json.loads(catalog_text)
    discovery_text=(ROOT / "data/research-topics.json").read_text(encoding="utf-8")
    discovery=json.loads(discovery_text)
    orbit_text=(ROOT / "data/orbit-types.json").read_text(encoding="utf-8")
    geometry_text=(ROOT / "data/geometry-presets.json").read_text(encoding="utf-8")
    land = json.loads((ROOT / "assets/ne_110m_land.geojson").read_text(encoding="utf-8"))
    payload = "window.EO_CATALOG=" + script_json(catalog) + ";\nwindow.EO_DISCOVERY=" + script_json(discovery) + ";\nwindow.EO_ORBITS="+script_json(json.loads(orbit_text))+";\nwindow.EO_GEOMETRY="+script_json(json.loads(geometry_text))+";\nwindow.EO_LAND=" + json.dumps(land, separators=(",", ":")) + ";\n"
    write(ROOT / "explorer/catalog.js", payload)
    template = (ROOT / "explorer/index.html").read_text(encoding="utf-8")
    css = (ROOT / "explorer/style.css").read_text(encoding="utf-8")
    js = (ROOT / "explorer/app.js").read_text(encoding="utf-8")
    document = template.replace('<link rel="stylesheet" href="style.css">', f"<style>{css}</style>")
    workspace_css=(ROOT / "explorer/workspace.css").read_text(encoding="utf-8")
    document = document.replace('<link rel="stylesheet" href="workspace.css">', f"<style>{workspace_css}</style>")
    discovery_css=(ROOT / "explorer/discovery.css").read_text(encoding="utf-8")
    research_js=(ROOT / "explorer/research.js").read_text(encoding="utf-8")
    document=document.replace('<link rel="stylesheet" href="discovery.css">',f"<style>{discovery_css}</style>")
    document=document.replace('<script src="research.js"></script>',f"<script>{research_js}</script>")
    orbit_js=(ROOT / "explorer/orbits.js").read_text(encoding="utf-8")
    document=document.replace('<script src="orbits.js"></script>',f"<script>{orbit_js}</script>")
    document = document.replace('<script src="catalog.js"></script>', f"<script>{payload}</script>")
    document = document.replace('<script src="app.js"></script>', f"<script>{js}</script>")
    document = document.replace('href="../book/', 'href="https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/book/')
    document = document.replace('href="../lab/', 'href="https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/lab/')
    document = document.replace("<!doctype html>", "<!doctype html>\n<!--\n" + (ROOT / "LICENSE").read_text(encoding="utf-8") + "\n-->", 1)
    document=document.replace('href="swaths.html"','href="eo-swaths.html"')
    write(ROOT / "downloads/eo-explorer.html", document)
    write(ROOT / "notebooks/support/eo-explorer.html", document)
    study=(ROOT / "explorer/swaths.html").read_text(encoding="utf-8")
    for name in ("style.css","coverage.css"):
        study=study.replace(f'<link rel="stylesheet" href="{name}">',"<style>"+(ROOT / "explorer" / name).read_text(encoding="utf-8")+"</style>")
    study=study.replace('<script src="catalog.js"></script>',f"<script>{payload}</script>")
    for name in ("research.js","orbits.js","coverage-model.js","coverage.js"):
        study=study.replace(f'<script src="{name}"></script>',"<script>"+(ROOT / "explorer" / name).read_text(encoding="utf-8")+"</script>")
    study=study.replace('href="../book/','href="https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/book/')
    study=study.replace('href="index.html"','href="eo-explorer.html"').replace('href="swaths.html"','href="eo-swaths.html"')
    study=study.replace("<!doctype html>","<!doctype html>\n<!--\n"+(ROOT / "LICENSE").read_text(encoding="utf-8")+"\n-->",1)
    write(ROOT / "downloads/eo-swaths.html",study)
    write(ROOT / "notebooks/support/eo-swaths.html",study)
    write(ROOT / "notebooks/data/catalog.json", catalog_text)
    write(ROOT / "notebooks/data/research-topics.json", discovery_text)
    for name in ("stac-coverage.json","research-ontology.ttl","orbit-types.json","geometry-presets.json"):
        shutil.copy2(ROOT / "data" / name,ROOT / "notebooks/data" / name)
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
    export_graph(catalog,discovery)
    coverage_page()
    # The splash is an original vector drawing built from our own UI and public-domain geography.
    splash(catalog, land)
    print("Prepared offline poster, notebook support files, source registry, JSON-LD and splash.")


def export_graph(catalog,discovery):
    base = "https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/id/"
    nodes = []
    for s in catalog["satellites"]:
        curated=not s.get("stac_imported") or s.get("sensor_curation")
        nodes.append({"@id": base+s["id"], "@type": "eo:MissionGroup" if s.get("record_kind")=="constellation / mission group" else "sosa:Platform", "label": s["name"],
                      "sosa:hosts": [{"@id": base+s["id"]+"/"+i["id"]} for i in s["sensors"]] if curated else [],
                      "eo:orbitType":{"@id":base+"orbit/"+s["orbit"]["class"].replace(" ","-").replace("/","-")},
                      "prov:wasDerivedFrom": [{"@id": catalog["sources"][sid]["url"]} for sid in s["sources"]]})
        if not curated:
            continue
        for i in s["sensors"]:
            nodes.append({"@id": base+s["id"]+"/"+i["id"], "@type": "sosa:Sensor", "label": i["name"],
                          "sosa:observes": [{"@id": base+"property/"+p.replace(" ", "-")} for p in i["observes"]],
                          "prov:wasDerivedFrom": [{"@id":catalog["sources"][sid]["url"]} for sid in i["sources"]]})
            for k,p in enumerate(i["products"]):
                nodes.append({"@id":base+s["id"]+"/"+i["id"]+f"/product/{k}", "@type":"dcat:Dataset", "label":p["name"],
                              "dcat:landingPage":{"@id":p["access"]},
                              "dcterms:relation":{"@id":base+s["id"]+"/"+i["id"]},
                              "prov:wasDerivedFrom":[{"@id":catalog["sources"][sid]["url"]} for sid in p["sources"]]})
    properties = sorted({p for s in catalog["satellites"] for i in s["sensors"] for p in i["observes"] if p!="Not curated"})
    nodes.extend({"@id":base+"property/"+p.replace(" ", "-"),"@type":"sosa:ObservableProperty","label":p} for p in properties)
    for orbit in sorted({s["orbit"]["class"] for s in catalog["satellites"]}):
        node={"@id":base+"orbit/"+orbit.replace(" ","-").replace("/","-"),"@type":["eo:OrbitType","skos:Concept"],"label":orbit}
        if orbit in ("Sun-synchronous LEO","Inclined LEO","Polar LEO"):
            node["skos:broader"]={"@id":base+"orbit/LEO"}
        nodes.append(node)
    for t in discovery["topics"]:
        nodes.append({"@id":base+"topic/"+t["id"],"@type":["eo:ResearchTopic","skos:Concept"],"skos:prefLabel":t["label"],
                      "skos:altLabel":t["aliases"],"skos:broader":[{"@id":base+"topic/"+t["broader"]}] if t.get("broader") else [],
                      "eo:potentialPlatform":[{"@id":base+p} for p in t["platforms"]],
                      "eo:observableProperty":{"@id":base+"property/"+t["property"].replace(" ","-")},
                      "eo:relevantCollection":[{"@id":next(r for r in discovery["routes"] if r["id"]==rid)["collection_url"]} for rid in t["routes"]],
                      "eo:qualification":t["caution"],"prov:wasDerivedFrom":[{"@id":catalog["sources"][sid]["url"]} for sid in t["sources"]]})
    for p in sorted({t["property"] for t in discovery["topics"]}-set(properties)):
        nodes.append({"@id":base+"property/"+p.replace(" ","-"),"@type":"sosa:ObservableProperty","label":p})
    for r in discovery["routes"]:
        nodes.append({"@id":r["collection_url"],"@type":["eo:STACCollection","dcat:Dataset"],"label":r["label"],
                      "dcat:distribution":{"@id":r["collection_url"]+"#metadata-distribution"},"eo:accessNote":r["access_note"],
                      "eo:platformMention":[{"@id":base+p} for p in r["platforms"]],"prov:wasDerivedFrom":[{"@id":catalog["sources"][sid]["url"]} for sid in r["sources"]]})
        nodes.append({"@id":r["collection_url"]+"#metadata-distribution","@type":"dcat:Distribution",
                      "dcat:accessURL":{"@id":r["collection_url"]},"dcat:accessService":{"@id":r["endpoint"]}})
    for endpoint in sorted({r["endpoint"] for r in discovery["routes"]}):
        nodes.append({"@id":endpoint,"@type":"dcat:DataService","dcat:endpointURL":{"@id":endpoint}})
    graph = {"@context":{"eo":"https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/vocab/","skos":"http://www.w3.org/2004/02/skos/core#","sosa":"http://www.w3.org/ns/sosa/","dcat":"http://www.w3.org/ns/dcat#","prov":"http://www.w3.org/ns/prov#","dcterms":"http://purl.org/dc/terms/","rdfs":"http://www.w3.org/2000/01/rdf-schema#","label":"rdfs:label"},"@graph":nodes}
    write(ROOT / "data/catalog.jsonld", json.dumps(graph, indent=2)+"\n")


def coverage_page():
    import collections
    audit=json.loads((ROOT / "data/stac-audit.json").read_text(encoding="utf-8"))
    coverage=json.loads((ROOT / "data/stac-coverage.json").read_text(encoding="utf-8"))
    counts=collections.Counter(c["status"] for c in audit["catalogs"])
    supplements=audit.get("supplemental_audits",[])
    documents=sum(c['documents_checked'] for c in audit['catalogs'])+sum(a['documents_checked'] for a in supplements)
    text=["# STAC coverage audit\n",f"Metadata audit: **{audit['retrieved'][:10]}**. Registry: [STAC Index]({audit['source']}). **{len(audit['catalogs'])} listings**, **{documents:,} documents checked** (including supplementary NASA pages), **{coverage['platform_records']} platform / constellation records** in the explorer.\n",
          "This is a bounded directory-wide audit, not proof that every EO satellite or asset is represented. STAC also contains aircraft, stations, models and non-Earth observations. Platform identifiers are optional; collection summaries can omit spacecraft. Mission-group and individual-spacecraft records can overlap; the record count is not a count of unique satellites.\n",
          f"Results: {dict(counts)}. `metadata-checked` means the bounded metadata walk ended without a recorded failure; it does not establish completeness, current operations, data rights, browser access or downloadable assets. `partial` marks errors or queued/depth-limited metadata. Private/protected and credential-bearing URLs are skipped; HTTPS/TLS errors are retained.\n",
          "The crawler requests at most 100 documents per catalog, up to depth 3, with a 12-second timeout and 6 MB per document. It reads catalog/collection metadata and at most one Item sample per document without a platform summary; it never requests assets. Static trees can contain thousands of unvisited Items. Legacy catalogs and optional platform fields limit extraction. The original 13 teaching records remain, followed by reviewed spacecraft and explicit constellation identifiers. Unknown orbits, instruments and specifications remain explicit.\n",
          "Download [audit evidence](https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/data/stac-audit.json), [identifier crosswalk](https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/data/stac-coverage.json), [catalog](https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/data/catalog.json), and [semantic graph](https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/data/catalog.jsonld). Endpoint snapshots do not automatically refresh on build.\n",
          "## Catalog results\n", "| STAC Index listing | Result | Documents | Metadata records |\n|---|---|---:|---:|"]
    for c in audit["catalogs"]:
        title=c["title"].replace("|","/").replace("\n"," ")
        text.append(f"| [{title}](https://stacindex.org/catalogs/{c['slug']}) | {c['status']} | {c['documents_checked']} | {len(c['collections'])} |")
    text.append("\n## Supplementary NASA cloud summaries\n")
    for a in supplements:
        text.append(f"[NASA ALL collection summaries]({a['root']}): **{a['documents_checked']} pages**, **{len(a['collections']):,} summaries**, status **{a['status']}**. An independent bound of {a['page_limit']} pages applies. More pages remain when partial. These summaries add GPM, SMAP, ICESat, OCO, PACE, SWOT and other identifiers missed by the first walk. Model names, aircraft and stations remain excluded or unresolved rather than becoming satellites. Refresh explicitly with `python scripts/audit_nasa.py --refresh`, then review and run the crosswalk curator. No Items/assets are requested by this supplementary audit.\n")
    unresolved=sorted({r["raw"] for r in coverage["platform_crosswalk"] if not r["platform_id"] and r["catalog"]!="oie-stac-catalog"})
    text.extend(["\n## Remaining identity work\n", "Identifiers deliberately excluded from the satellite map (ground/aircraft or unresolved): "+", ".join(f"`{x}`" for x in unresolved)+". Energy-catalog station identifiers are retained in the crosswalk separately. Generic provider instrument arrays are not assigned to every spacecraft in a mixed collection.\n",
                 "## Refresh and review\n", "Run `python scripts/audit_stac.py --refresh` explicitly, review failures and bounds, then `python scripts/curate_stac.py`. The crosswalk code contains the reviewed identity rules. Recheck specific catalogs with `--catalog SLUG`. Inspect the diff before committing, validate, rebuild, and run browser tests. Expand operator-backed orbit/instrument records without replacing unknowns with guesses.\n"])
    write(ROOT / "book/stac-coverage.md","\n".join(text))


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
    for s in catalog["satellites"][:13]:
        x=100+s["display"]["x"]*1.17; y=200+s["display"]["y"]*.95
        c=colors[s["type"]]
        nodes.append(f'<g transform="translate({x:.1f} {y:.1f})"><circle r="17" fill="#0e2539" stroke="{c}"/><path d="M-12 -5H-5V5H-12ZM5 -5H12V5H5ZM-5 0H5" fill="none" stroke="{c}"/><rect x="-4" y="-4" width="8" height="8" fill="{c}"/><text y="36" text-anchor="middle" fill="#e7f2f6" font-size="13">{escape(s['name'])}</text></g>')
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000" role="img" aria-labelledby="title desc"><title id="title">Global Earth Observation Satellites</title><desc id="desc">Original schematic world-map constellation of 13 representative EO platforms. Orbits and spacecraft positions are illustrative, not to scale or live.</desc><defs><radialGradient id="bg"><stop stop-color="#15374e"/><stop offset="1" stop-color="#071522"/></radialGradient></defs><rect width="1600" height="1000" fill="url(#bg)"/><g font-family="system-ui,Segoe UI,sans-serif"><text x="80" y="70" fill="#60dfc4" font-size="14" letter-spacing="4">GLOBAL EO / THE SATELLITE GUIDE</text><text x="80" y="140" fill="#eef5f8" font-size="50" letter-spacing="-1">Global Earth Observation Satellites</text><text x="80" y="180" fill="#a7c1cf" font-size="19">One planet. Many ways to see it.</text><path d="{''.join(path)}" fill="#276174" stroke="#508998" stroke-width=".5" opacity=".7"/><ellipse cx="800" cy="480" rx="580" ry="240" fill="none" stroke="#60dfc4" opacity=".4"/><ellipse cx="800" cy="510" rx="675" ry="290" fill="none" stroke="#f2c17a" stroke-dasharray="7 9" opacity=".6"/>{''.join(nodes)}<text x="80" y="860" fill="#60dfc4" font-size="16" letter-spacing="2">EXPLORE THE CONSTELLATION → COMPARE SENSORS → FOLLOW THE EVIDENCE</text><path d="M80 890H1520" stroke="#365264"/><text x="80" y="925" fill="#b0c4d2" font-size="14">13 representative platforms · interactive poster · executable notebooks · Jupyter Book + JupyterLite</text><text x="80" y="958" fill="#819cac" font-size="12">Illustrative positions and orbit rings, not to scale. Original vectors: MIT. Made with Natural Earth (public domain). Catalog: {catalog['verified']}.</text></g></svg>'''
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
    # Recreate generated Lite output/cache so a warm build cannot skip config
    # merges or retain stale content when notebooks and shared datasets change.
    reset_generated(lite_output)
    for cache in ROOT.glob(".jupyterlite.doit.db*"):
        if cache.is_symlink() or not cache.resolve().is_relative_to(ROOT) or not cache.is_file():
            raise ValueError("Unsafe Lite task-cache path")
        cache.unlink()
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
    version_explorer_assets(site / "explorer")
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
        archive.write(ROOT / "downloads/eo-swaths.html","eo-swaths.html")
        archive.write(ROOT / "ATTRIBUTIONS.md","ATTRIBUTIONS.md")
        archive.write(ROOT / "LICENSE","LICENSE")
        archive.write(ROOT / "data/catalog.json","data/catalog.json")
        archive.write(ROOT / "data/catalog.jsonld","data/catalog.jsonld")
        for name in ("research-topics.json","research-ontology.ttl","stac-coverage.json","stac-audit.json","orbit-types.json","geometry-presets.json"):
            archive.write(ROOT / "data" / name,"data/"+name)
    hashes={str(p.relative_to(ROOT)).replace("\\","/"):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT / "data/catalog.json",ROOT / "assets/ne_110m_land.geojson",ROOT / "downloads/eo-explorer.html"]}
    write(site / "build-manifest.json",json.dumps({"catalog_verified":json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))["verified"],"sha256":hashes},indent=2)+"\n")
    print("Built _site. Serve with: python -m http.server 8000 --directory _site")


if __name__=="__main__":
    main()
