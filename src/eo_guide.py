"""Small, dependency-free helpers shared by CPython and JupyterLite/Pyodide."""
from __future__ import annotations

import html
import json
import math
import asyncio
import re
import unicodedata
from urllib.parse import urlencode, urlsplit
from pathlib import Path


def data_path(name="catalog.json"):
    """Resolve bundled data from a notebook, the repository, or the book."""
    for root in (Path.cwd(), Path.cwd().parent, Path(__file__).resolve().parent):
        candidate = root / "data" / name
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Bundled data/{name} missing. Run scripts/build.py --prepare.")


def load_catalog():
    return json.loads(data_path().read_text(encoding="utf-8"))


def research_matches(question, profile=None):
    """Resolve curated aliases; no language model, inference or network request."""
    profile = profile or json.loads(data_path("research-topics.json").read_text(encoding="utf-8"))
    def normalize(text):
        return re.sub(r"[^a-z0-9.]+", " ", unicodedata.normalize("NFKD", text).lower()).strip()
    q = " " + normalize(question) + " "
    topics = [t for t in profile["topics"] if any(" "+normalize(a)+" " in q for a in t["aliases"])]
    topics = [t for t in topics if not any(c.get("broader") == t["id"] for c in topics)]
    route_ids = {r for t in topics for r in t["routes"]}
    return {"question": question, "concepts": [t["id"] for t in topics],
            "platforms": sorted({p for t in topics for p in t["platforms"]}),
            "routes": [r for r in profile["routes"] if r["id"] in route_ids],
            "qualifications": [t["caution"] for t in topics]}


async def search_stac(route, *, bbox, start, end, limit=3):
    """Bounded, public STAC collection Item metadata GET. Never downloads assets.

    JupyterLite uses browser CORS through pyfetch. CPython uses urllib with TLS.
    The caller must choose dates/area and explicitly run this function.
    """
    import datetime as dt
    if not isinstance(limit, int) or not 1 <= limit <= 10:
        raise ValueError("Choose 1–10 metadata Items")
    if (len(bbox) != 4 or any(not isinstance(n, (int, float)) or isinstance(n, bool) or not math.isfinite(n) for n in bbox)
            or not -180 <= bbox[0] < bbox[2] <= 180 or not -90 <= bbox[1] < bbox[3] <= 90):
        raise ValueError("Use a valid west,south,east,north CRS84 bbox; split antimeridian areas")
    begin, finish = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
    if finish < begin:
        raise ValueError("End date precedes start date")
    def safe_url(value):
        parts = urlsplit(value)
        if (parts.scheme != "https" or not parts.hostname or parts.username or parts.password or parts.query or parts.fragment):
            raise ValueError("Use a public HTTPS metadata URL without credentials or query parameters")
        return value
    collection_url = safe_url(route["collection_url"])

    async def fetch(url):
        try:
            from pyodide.http import pyfetch
        except ImportError:
            from urllib.request import Request, urlopen
            def blocking():
                with urlopen(Request(url, headers={"Accept":"application/json"}), timeout=20) as response:
                    raw = response.read(6_000_001)
                    if len(raw) > 6_000_000:
                        raise ValueError("Metadata response exceeds 6 MB bound")
                    return json.loads(raw)
            return await asyncio.to_thread(blocking)
        response = await asyncio.wait_for(pyfetch(url, credentials="omit"), timeout=20)
        if not response.ok:
            raise RuntimeError(f"STAC HTTP {response.status}; check provider availability/access")
        text = await asyncio.wait_for(response.string(), timeout=20)
        if len(text.encode("utf-8")) > 6_000_000:
            raise ValueError("Metadata response exceeds 6 MB bound")
        return json.loads(text)
    params = {"bbox": ",".join(map(str, bbox)), "datetime": f"{start}T00:00:00Z/{end}T23:59:59Z", "limit": limit}
    result = await fetch(collection_url.rstrip("/") + "/items?" + urlencode(params))
    if result.get("type") != "FeatureCollection" or not isinstance(result.get("features"), list):
        raise ValueError("Provider did not return a STAC ItemCollection")
    result["features"] = result["features"][:limit]
    return result


def iframe_document(document, title, height=780):
    """Isolate each interactive HTML output; allow local scripts and user exports."""
    from IPython.display import HTML
    return HTML(
        '<div class="eo-guide-output">'
        f'<iframe title="{html.escape(title, quote=True)}" '
        'allowfullscreen '
        f'sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox allow-downloads allow-modals" '
        f'style="width:100%;height:{int(height)}px;border:1px solid #345;border-radius:8px" '
        f'srcdoc="{html.escape(document, quote=True)}"></iframe></div>'
    )


def poster(height=1100, question=""):
    for root in (Path.cwd(), Path(__file__).resolve().parent):
        path = root / "support" / "eo-explorer.html"
        if path.exists():
            document=path.read_text(encoding="utf-8")
            document=document.replace('href="eo-swaths.html"','href="https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/explorer/swaths.html"')
            initial=json.dumps(str(question)[:500]).replace("<", "\\u003c")
            document=document.replace("<head>","<head><script>window.EO_INITIAL_QUESTION="+initial+";</script>",1)
            return iframe_document(document, "Interactive EO constellation poster", height)
    raise FileNotFoundError("support/eo-explorer.html missing. Run scripts/build.py --prepare.")


def swath_lab(height=1350, question="air quality and NO2 measures", bbox=(-76,39,-74,41), mission="sentinel-5p"):
    """Embed the shared, offline-capable AOI teaching model; no provider requests."""
    if (len(bbox)!=4 or not all(isinstance(v,(int,float)) and math.isfinite(v) for v in bbox)
            or not -180<=bbox[0]<bbox[2]<=180 or not -90<=bbox[1]<bbox[3]<=90):
        raise ValueError("Use west,south,east,north coordinates; split date-line boxes")
    for root in (Path.cwd(),Path(__file__).resolve().parent):
        path=root / "support/eo-swaths.html"
        if path.exists():
            initial=json.dumps({"question":str(question)[:500],"bbox":list(bbox),"mission":str(mission)}).replace("<","\\u003c")
            document=path.read_text(encoding="utf-8").replace("<head>","<head><script>window.EO_INITIAL_SWATH="+initial+";</script>",1)
            return iframe_document(document,"EO study-area swaths and orbits",height)
    raise FileNotFoundError("support/eo-swaths.html missing. Run scripts/build.py --prepare.")


def query(catalog, *, family=None, property_name=None, agency=None):
    return [s for s in catalog["satellites"] if
            (family is None or s["type"] == family) and
            (agency is None or agency.lower() in s["agency"].lower()) and
            (property_name is None or any(property_name in i["observes"] for i in s["sensors"]))]


def comparison(catalog, ids):
    """Preserve contexts instead of ranking incompatible numeric resolutions."""
    from IPython.display import HTML
    satellites = [next(s for s in catalog["satellites"] if s["id"] == sid) for sid in ids]
    rows = []
    for s in satellites:
        citations = "; ".join(catalog["sources"][key]["url"] for key in s["sources"])
        values = (s["name"], s["type"], "; ".join(i["spatial"] for i in s["sensors"]),
                  s["orbit"]["temporal_note"], s["status"], citations)
        rows.append("<tr>" + "".join(f"<td>{html.escape(v)}</td>" for v in values) + "</tr>")
    return HTML('<div style="overflow:auto"><table><caption>Contextual comparison; no universal ranking</caption>'
                '<thead><tr><th>Platform</th><th>Family</th><th>Spatial context</th><th>Temporal context</th>'
                '<th>Status snapshot</th><th>Evidence URLs</th></tr></thead><tbody>' + "".join(rows) + '</tbody></table></div>')


def orbital_period_minutes(altitude_km, radius_km=6371.0, mu=398600.4418):
    """Illustrative circular orbit; no drag, oblateness, propagation or tracking."""
    if altitude_km < 0:
        raise ValueError("Altitude must be nonnegative")
    return 2 * math.pi * math.sqrt((radius_km + altitude_km) ** 3 / mu) / 60


def synthetic_reflectance(wavelength_nm, chlorophyll=0.7, water=0.5):
    """Invented teaching curve. Never interpret as observed or calibrated data."""
    w = wavelength_nm
    red_edge = 0.05 + 0.42 / (1 + math.exp(-(w - 715) / 16))
    green = 0.06 * math.exp(-((w - 550) / 45) ** 2)
    red = chlorophyll * 0.035 * math.exp(-((w - 670) / 26) ** 2)
    absorption = water * (0.20 * math.exp(-((w - 1450) / 80) ** 2)
                          + 0.28 * math.exp(-((w - 1950) / 110) ** 2))
    return max(0.005, red_edge + green - red - absorption)


def spectrum_demo():
    document = '''<!doctype html><html lang="en"><meta charset="utf-8"><style>
body{font:15px system-ui;background:#0b2030;color:#eaf5fa;padding:22px}label{display:block;margin:15px 0}input{width:240px}svg{width:100%;max-width:900px}p{max-width:800px;color:#b8cfda}text{fill:#c3dce8;font:13px system-ui}</style>
<h2>Spectral detail, without false precision</h2><p>SYNTHETIC DATA. Move the controls to change an invented vegetation curve. The rectangles show simple band averages, not any actual instrument response.</p>
<label>Water absorption strength <input id="water" type="range" min="0" max="1" step=".05" value=".5"> <output id="water-value">0.5</output></label>
<label>Illustrative band width (nm) <input id="width" type="range" min="10" max="180" step="10" value="80"> <output id="width-value">80</output></label>
<svg viewBox="0 0 900 360" role="img" aria-label="Synthetic spectral reflectance and adjustable band averages"><path d="M55 20V300H865" fill="none" stroke="#a9c5d4"/><text x="55" y="330">400 nm</text><text x="785" y="330">2400 nm</text><text x="55" y="17">Illustrative reflectance (0 to 0.6)</text><g id="bands"></g><path id="curve" fill="none" stroke="#60dfc4" stroke-width="3"/></svg><p id="description" role="status" aria-live="polite"></p>
<script>const water=document.getElementById('water'),width=document.getElementById('width');
function r(w,v){return Math.max(.005,.05+.42/(1+Math.exp(-(w-715)/16))+.06*Math.exp(-((w-550)/45)**2)-.7*.035*Math.exp(-((w-670)/26)**2)-v*(.20*Math.exp(-((w-1450)/80)**2)+.28*Math.exp(-((w-1950)/110)**2)));}
function draw(){const v=+water.value,bw=+width.value;document.getElementById('water-value').value=v;document.getElementById('width-value').value=bw;let d='',b='';for(let w=400;w<=2400;w+=5)d+=(w===400?'M':'L')+(55+(w-400)/2000*810)+','+(300-r(w,v)/.6*270);for(let c=450;c<2400;c+=220){let sum=0,n=0;for(let w=c-bw/2;w<=c+bw/2;w+=2){sum+=r(w,v);n++;}const x=55+(c-bw/2-400)/2000*810,y=300-sum/n/.6*270;b+='<rect x="'+x+'" y="'+y+'" width="'+(bw/2000*810)+'" height="'+(300-y)+'" fill="#f2c17a" opacity=".3"/>';}document.getElementById('curve').setAttribute('d',d);document.getElementById('bands').innerHTML=b;document.getElementById('description').textContent='Water strength '+v+', band width '+bw+' nm. Broad bands average narrow features. Curves and band placements are invented.';}water.oninput=draw;width.oninput=draw;draw();</script></html>'''
    return iframe_document(document, "Interactive synthetic spectral sampling exercise", 650)


def orbit_demo():
    document = '''<!doctype html><html lang="en"><meta charset="utf-8"><style>
body{font:15px system-ui;background:#0b2030;color:#eaf5fa;padding:22px}label{display:block;margin:14px 0}input{width:240px}svg{width:100%;max-width:900px}p{color:#b8cfda;max-width:850px}text{fill:#c3dce8;font:12px system-ui}</style><h2>Orbit geometry laboratory</h2><p>Generic circular-orbit model over a rotating spherical Earth. This is a simulation, with arbitrary initial longitude. It is not a mission ground track or coverage guarantee.</p>
<label>Altitude, km <input id="h" type="range" min="400" max="1200" step="10" value="705"> <output id="hv">705</output></label><label>Inclination, degrees <input id="i" type="range" min="0" max="110" step="1" value="98"> <output id="iv">98</output></label>
<svg viewBox="0 0 900 420" role="img" aria-label="Simulated ground track over longitude and latitude axes"><rect x="50" y="35" width="800" height="330" fill="#112e40" stroke="#7591a6"/><path d="M50 200H850M450 35V365" stroke="#7591a6" stroke-dasharray="4 6"/><path id="track" fill="none" stroke="#60dfc4" stroke-width="2"/><text x="50" y="390">180 W</text><text x="430" y="390">0</text><text x="810" y="390">180 E</text><text x="4" y="42">90 N</text><text x="4" y="365">90 S</text></svg><p id="result" role="status" aria-live="polite"></p>
<script>const h=document.getElementById('h'),inc=document.getElementById('i');function draw(){const alt=+h.value,i=+inc.value*Math.PI/180,T=2*Math.PI*Math.sqrt((6371+alt)**3/398600.4418),omega=2*Math.PI/86164.0905;let d='',last=null;for(let n=0;n<=1800;n++){let t=n/1800*T*3,u=2*Math.PI*t/T,x=Math.cos(u),y=Math.sin(u)*Math.cos(i),lat=Math.asin(Math.sin(u)*Math.sin(i))*180/Math.PI,lon=(Math.atan2(y,x)-omega*t)*180/Math.PI;lon=((lon+180)%360+360)%360-180;d+=(last===null||Math.abs(lon-last)>180?'M':'L')+(50+(lon+180)/360*800)+','+(35+(90-lat)/180*330);last=lon;}document.getElementById('track').setAttribute('d',d);document.getElementById('hv').value=alt;document.getElementById('iv').value=inc.value;document.getElementById('result').textContent='Circular period: '+(T/60).toFixed(1)+' minutes. Three simulated orbits. Maximum latitude: '+Math.min(+inc.value,180-inc.value)+' degrees. Sensor swath, Earth oblateness, precession, drag and actual mission elements are omitted.';}h.oninput=draw;inc.oninput=draw;draw();</script></html>'''
    return iframe_document(document, "Interactive generic circular-orbit simulation", 700)
