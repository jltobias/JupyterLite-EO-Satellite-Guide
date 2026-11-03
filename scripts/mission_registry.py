"""Snapshot and reconcile the public CC BY 4.0 CEOS mission registry.

Refresh is explicit; ordinary curation/builds use the checked-in factual snapshot.
The registry describes missions, including hosted payloads, proposed and cancelled
projects. It is not a count of spacecraft currently in orbit or a data-access feed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urljoin, urlsplit
from urllib.request import HTTPCookieProcessor, Request, build_opener
from http.cookiejar import CookieJar

from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
DATE="2026-11-03"
TABLE="https://database.eohandbook.com/database/missiontable.aspx"
ABOUT="https://database.eohandbook.com/about.aspx"
LICENCE="https://creativecommons.org/licenses/by/4.0/"


def parse_table(html):
    soup=BeautifulSoup(html,"html.parser")
    table=soup.select_one("#MainContent_gvMissionTable")
    if table is None:
        raise ValueError("CEOS mission table missing; source format may have changed")
    records=[]
    for row in table.select("tr"):
        cells=row.find_all("td",recursive=False)
        if len(cells)!=8:
            continue
        link=cells[0].select_one('a[href*="missionsummary.aspx?missionID="]')
        if not link:
            raise ValueError("Mission row without permanent identifier")
        url=urljoin(TABLE,link["href"])
        mid=parse_qs(urlsplit(url).query)["missionID"][0]
        if not mid.isdigit():
            raise ValueError("Invalid mission identifier")
        orbit={}
        for line in cells[7].get_text("\n",strip=True).splitlines():
            if ":" in line:
                key,value=line.split(":",1)
                if key in ("Type","Altitude","Period","Inclination","Repeat cycle","LST","Longitude (if geo)","Asc/desc"):
                    orbit[key]=value.strip()
        instruments=[{"name":a.get_text(" ",strip=True),"url":urljoin(TABLE,a["href"])}
                     for a in cells[6].select('a[href*="instrumentsummary.aspx?instrumentID="]')]
        links=[{"label":a.get_text(" ",strip=True),"url":urljoin(TABLE,a["href"])} for a in cells[7].select("a[href]")
               if urlsplit(urljoin(TABLE,a["href"])).scheme in ("https","http")]
        records.append({"id":mid,"name":link.get_text(" ",strip=True),"full_name":" ".join(cells[0].get_text("\n",strip=True).splitlines()[1:]),"url":url,
            "agency":[a.get_text(" ",strip=True) for a in cells[1].select("a")],
            "status":cells[2].get_text(" ",strip=True),"launch":cells[3].get_text(" ",strip=True),
            "eol":cells[4].get_text(" ",strip=True),"orbit":orbit,"instruments":instruments,"links":links})
    if len({r["id"] for r in records})!=len(records):
        raise ValueError("Duplicate permanent mission identifiers")
    return records


def refresh():
    opener=build_opener(HTTPCookieProcessor(CookieJar()))
    def read(request):
        with opener.open(request,timeout=45) as response:
            data=response.read(8_000_001)
            if len(data)>8_000_000:
                raise ValueError("Registry response exceeded 8 MB")
            return data
    first=BeautifulSoup(read(TABLE).decode("utf-8"),"html.parser")
    fields={e["name"]:e.get("value","") for e in first.select("input[type=hidden][name]")}
    for select in first.select("select[name]"):
        option=select.select_one("option[selected]") or select.select_one("option")
        if not select.has_attr("disabled") and option:
            fields[select["name"]]=option.get("value",option.get_text())
    fields.update({"ctl00$MainContent$ddlMissionStatus":"All","ctl00$MainContent$ddlDisplayResults":"All",
                   "ctl00$MainContent$btFilter":"Apply Filter"})
    raw=read(Request(TABLE,data=urlencode(fields).encode(),headers={"Content-Type":"application/x-www-form-urlencoded"}))
    records=parse_table(raw.decode("utf-8"))
    if len(records)<500:
        raise ValueError("Unexpectedly small All-missions response; refusing partial replacement")
    return snapshot(records,hashlib.sha256(raw).hexdigest())


def snapshot(records,digest):
    return {"verified":DATE,"source":TABLE,"about":ABOUT,"license":"CC BY 4.0","license_url":LICENCE,
        "attribution":"CEOS MIM Database, https://database.eohandbook.com, accessed "+DATE,
        "selection":"All mission statuses; All results per page", "response_sha256":digest,
        "scope":"Factual mission registry snapshot. Includes past, current, proposed, cancelled and hosted missions; expected EOL is not retirement. No imagery copied.",
        "record_count":len(records),"records":records}


def key(name):
    name=name.lower().strip()
    aliases={"sentinel-5 precursor":"sentinel-5p","sentinel-6  a michael freilich":"sentinel-6a",
        "adeos":"adeos-i","earth observing-1":"eo-1","suomi-npp":"suomi-npp","arctica-m n1":"arcm1","arctica-m n2":"arcm2",
        "mtg-i1 (imaging)":"meteosat-12","mtg-s1 (sounding)":"meteosat-13","metop-sg a1":"metop-sg-a1","srtm":"endeavour-srtm","oceansat-3":"eos-06"}
    if name in aliases:
        return aliases[name]
    if name=="mtg-s1":return "meteosat-13"
    if name.startswith("mtg-s"):
        return re.match(r"mtg-s\d",name)[0]
    value=re.sub(r"[^a-z0-9]+","-",name).strip("-")
    value=re.sub(r"^sentinel-([1-6])-([a-d])$",r"sentinel-\1\2",value)
    return {"sentinel-6-a-michael-freilich":"sentinel-6a","eo-1-hyperion":"eo-1"}.get(value,value)


HOSTS={"sentinel-4a":"meteosat-13","sentinel-4b":"mtg-s2","sentinel-5a":"metop-sg-a1",
       "sentinel-5b":"metop-sg-a2","sentinel-5c":"metop-sg-a3"}
STATUSES={"Operational (nominal)":"operational","Operational (extended)":"operational","Commissioning":"commissioning",
          "Mission complete":"retired","Approved":"planned","Planned":"planned","Considered":"considered","Cancelled":"cancelled"}
ORBITS={"Sun-synchronous":"Sun-synchronous LEO","Inclined, non-sun-synchronous":"Inclined LEO",
        "Geostationary":"Geostationary","Highly elliptical":"Highly elliptical","Earth-Sun L-1":"Sun-Earth L1"}


def numeric(label,unit):
    match=re.fullmatch(r"(\d+(?:\.\d+)?)\s*"+re.escape(unit),label.strip())
    return float(match[1]) if match else None


def blank(sid,name,source):
    return {"id":sid,"name":name,"agency":"See mission registry","region":"See agency sources","status":"unverified",
        "status_note":"Mission registry snapshot; confirm operations with the responsible agency.","verified":DATE,"type":"other",
        "launch":None,"end":None,"record_kind":"mission record / platform identity not independently reviewed",
        "registry_imported":True,"stac_imported":True,"purpose":"Explore the cited mission and instrument records; confirm product coverage, quality, access and license.",
        "orbit":{"class":"Unknown / not curated","altitude_km":None,"repeat_days":None,"temporal_note":"Orbit, repeat, scan interval and usable data revisit are different quantities."},
        "display":{"x":600,"y":80},"sources":[source],"evidence":{f:[source] for f in ("mission","orbit","sensors","products")},
        "sensors":[{"id":"registry-payload","name":"Payload details in the mission registry","method":"Inspect the source-backed payload links below",
            "observes":["Not curated"],"spatial":"Not curated; instrument/mode/product specific","spectral":"Not curated",
            "coverage":"Inspect actual products and Item footprints; a mission listing is not evidence of usable data",
            "sources":[source],"products":[{"name":"Mission and data-access documentation","level":"Not curated","access":"https://database.eohandbook.com/",
                "note":"Documentation link; no STAC collection or data availability is inferred.","sources":[source]}]}]}


def apply_registry(catalog,registry):
    sources=catalog["sources"];by_id={s["id"]:s for s in catalog["satellites"]};crosswalk=[]
    for r in sorted(registry["records"],key=lambda r:key(r["name"]) in HOSTS):
        identity=key(r["name"]);sid=HOSTS.get(identity,identity);source="ceos-"+r["id"]
        sources[source]={"title":"CEOS mission record: "+r["name"],"publisher":"CEOS MIM Database","url":r["url"],"accessed":DATE,
            "license":"CC BY 4.0","locators":"Derived from the All-status mission table. Agency evidence takes precedence; expected EOL is not a retirement date."}
        if sid not in by_id:
            s=blank(sid,r["name"],source);catalog["satellites"].append(s);by_id[sid]=s
        s=by_id[sid];s["sources"]=list(dict.fromkeys(s["sources"]+[source]));s.setdefault("registry_records",[])
        s["registry_records"]=[old for old in s["registry_records"] if old["id"]!=r["id"]]+[r]
        s.setdefault("aliases",[]);s["aliases"]=list(dict.fromkeys(s["aliases"]+[r["name"]]))
        if identity in HOSTS:
            s.setdefault("hosted_missions",[]);s["hosted_missions"]=[m for m in s["hosted_missions"] if m["id"]!=identity]+[{"id":identity,"name":r["name"],"sources":[source]}]
            s["name"]=re.sub(r"\s*/\s*Sentinel-.*$","",s["name"])+" / "+r["name"].replace("Sentinel-4 ","Sentinel-4").replace("Sentinel-5 ","Sentinel-5")
            s["type"]="atmosphere";s["record_kind"]="spacecraft with hosted Sentinel instrument"
        else:
            s["agency"]=" / ".join(r["agency"]) or s["agency"]
            s["registry_status"]=r["status"];s["status"]=STATUSES.get(r["status"],"unverified")
            s["status_note"]=f"CEOS registry reports {r['status']} as checked {DATE}. This is a source snapshot, not a live operations feed. Planned dates and expected end of life do not establish operations or data availability."
            s["launch"]=r["launch"] or s.get("launch");s["end"]=(r["eol"] or "End date not specified by the registry") if s["status"]=="retired" else None
            s["verified"]=DATE;s["evidence"]["mission"]=list(dict.fromkeys(s["evidence"]["mission"]+[source]))
            if s.get("stac_imported"):
                kind=ORBITS.get(r["orbit"].get("Type"),"Unknown / not curated")
                s["orbit"]["class"]=kind
                s["orbit"]["altitude_km"]=numeric(r["orbit"].get("Altitude",""),"km") if kind not in ("Highly elliptical","Sun-Earth L1") else None
                if kind=="Inclined LEO" and (s["orbit"]["altitude_km"] is None or s["orbit"]["altitude_km"]>2000):
                    s["orbit"]["class"]="Unknown / not curated"
                s["orbit"]["repeat_days"]=numeric(r["orbit"].get("Repeat cycle",""),"days")
                s["orbit"]["temporal_note"]="CEOS nominal orbit: "+r["orbit"].get("Type","not specified")+". Reported repeat: "+(r["orbit"].get("Repeat cycle") or "not specified")+"; period: "+(r["orbit"].get("Period") or "not specified")+". These are not usable data revisit or pass predictions."
                s["evidence"]["orbit"]=list(dict.fromkeys(s["evidence"]["orbit"]+[source]))
            if sid.startswith("sentinel-") and re.match(r"sentinel-[1236][a-d]$",sid):
                s["record_kind"]="spacecraft";s["type"]={"1":"radar","2":"multispectral","3":"ocean","6":"ocean"}[sid[9]]
                s["name"]=re.sub(r"^(Sentinel-[1236])\s+([A-D])",r"\1\2",r["name"])
            if re.fullmatch(r"(?:noaa|goes)-\d+",sid):
                s["record_kind"]="spacecraft";s["type"]="weather"
            if re.fullmatch(r"landsat-\d+",sid):
                s["record_kind"]="spacecraft";s["type"]="multispectral";s["name"]=r["name"]
        crosswalk.append({"registry_id":r["id"],"registry_name":r["name"],"platform_id":sid,"hosted_payload":identity in HOSTS})
    for sid,payload,number in (("meteosat-13","UVN",4),("metop-sg-a1","UVNS",5)):
        if sid not in by_id:continue
        source=f"eumetsat-sentinel{number}"
        sources[source]={"title":f"Sentinel-{number} atmospheric composition mission","publisher":"EUMETSAT","url":f"https://www.eumetsat.int/sentinel-{number}","accessed":DATE}
        s=by_id[sid];s["sources"]=list(dict.fromkeys(s["sources"]+[source]));s["sensor_curation"]=True
        for field in ("sensors","products"):s["evidence"][field]=[source]
        s["sensors"]=[{"id":payload.lower(),"name":f"Sentinel-{number} / {payload}","method":"Passive ultraviolet-visible atmospheric spectroscopy; retrieved atmospheric columns",
            "observes":["tropospheric nitrogen dioxide column","trace gases","aerosols"],"spatial":"Product- and viewing-geometry dependent; inspect EUMETSAT product documentation",
            "spectral":"UV, visible and near infrared"+("; shortwave infrared" if number==5 else ""),"coverage":"Europe and surrounding region; daytime scans" if number==4 else "Global polar-orbit sampling; consult actual products and QA",
            "sources":[source],"products":[{"name":f"Sentinel-{number} atmospheric composition products","level":"Product-dependent retrievals","access":sources[source]["url"],
                "note":"Operator documentation route. No verified STAC collection is bundled for this hosted mission; do not substitute a Sentinel-5P collection.","sources":[source]}]}]
    # Include launch failures in the historical inventory without drawing an achieved orbit.
    source="usgs-landsat6"
    sources[source]={"title":"Landsat 6: launch failure","publisher":"USGS","url":"https://www.usgs.gov/landsat-missions/landsat-6","accessed":DATE}
    if "landsat-6" not in by_id:
        s=blank("landsat-6","Landsat 6",source);catalog["satellites"].append(s);by_id[s["id"]]=s
    s=by_id["landsat-6"];s["sources"]=list(dict.fromkeys(s["sources"]+[source]));s["evidence"]["mission"]=[source];s.update(status="failed",record_kind="spacecraft / launch failure",agency="EOSAT / US Department of Commerce",launch="1993-10-05",end="1993-10-05",
        status_note="Landsat 6 failed to achieve orbit. It produced no Earth observation archive; included for historical completeness.")
    s["orbit"].update({"class":"No orbit achieved","altitude_km":None,"repeat_days":None,"temporal_note":"Launch failure; nominal orbit specifications do not describe an achieved orbit or observations."})
    s["sensors"][0].update(name="ETM design / no observations",method="Launch failure; consult USGS for the planned instrument specifications",spatial="Design specifications only; no EO measurements acquired",sources=[source])
    s["sensors"][0]["products"]=[{"name":"Landsat 6 mission history","level":"No EO archive","access":sources[source]["url"],"note":"No Earth observation data acquired; intended specifications must not be treated as measurements.","sources":[source]}]
    # Operator mission history supersedes the older CEOS end-of-imaging year.
    if "landsat-7" in by_id:
        source="usgs-landsat7"
        sources[source]={"title":"Landsat 7 mission history and decommissioning","publisher":"USGS","url":"https://www.usgs.gov/landsat-missions/landsat-7","accessed":DATE}
        s=by_id["landsat-7"];s.update(status="retired",end="2025-06-04",status_note="USGS reports Landsat 7 decommissioned on 4 June 2025; imaging ended earlier. CEOS end-of-imaging and spacecraft retirement are different dates.")
        s["sources"]=list(dict.fromkeys(s["sources"]+[source]));s["evidence"]["mission"]=[source]
    for s in catalog["satellites"]:
        families=[];name=s["id"]
        if name.startswith("sentinel") or s.get("hosted_missions") or any(r["name"].startswith("Sentinel") for r in s.get("registry_records",[])):families.append("sentinel")
        if name.startswith("landsat"):families.append("landsat")
        if name.startswith(("noaa","goes","tiros","jpss")) or name=="suomi-npp" or any("NOAA" in r["agency"] for r in s.get("registry_records",[])):families.append("noaa")
        s["mission_families"]=families
        if s["id"]=="meteosat-13":s["aliases"]=list(dict.fromkeys(s.get("aliases",[])+["MTG-S1","Sentinel-4A"]))
    if "suomi-npp" in by_id:
        source="noaa-snpp-cessation"
        sources[source]={"title":"S-NPP permanent science-data cessation, 2 November 2026","publisher":"NOAA NESDIS","accessed":DATE,
            "url":"https://www.nesdis.noaa.gov/news/update-4-cessation-of-suomi-national-polar-orbiting-partnership-s-npp-data-users-november-02-2026-1540-utc-and-decommissioning-issued-november-2-2026-1800-utc"}
        s=by_id["suomi-npp"];s.update(status="retired",end="2026-11-02",status_note="NOAA confirms permanent cessation of S-NPP science-data delivery on 2 November 2026 at 15:40 UTC. This is service retirement; planned later deorbit is a separate event. Historical archives remain distinct from new data delivery.")
        s["sources"]=list(dict.fromkeys(s["sources"]+[source]));s["evidence"]["mission"]=[source]
    catalog.update(version="3.0.0",verified=DATE,scope=f"{len(catalog['satellites'])} mission/platform records combining the full CEOS All-status table and the saved STAC audit. Includes mission groups, hosted payloads, archives, proposals, cancellations and launch failures; not a unique operating-satellite count or a claim of universal coverage. Agency sources supersede registry snapshots.")
    return {"verified":DATE,"registry_record_count":len(registry["records"]),"mapped_record_count":len(crosswalk),"crosswalk":crosswalk,
        "catalog_record_count":len(catalog["satellites"]),"families":{f:[s["id"] for s in catalog["satellites"] if f in s["mission_families"]] for f in ("sentinel","landsat","noaa")},
        "scope":catalog["scope"],"attribution":registry["attribution"],"license":registry["license"]}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--refresh",action="store_true");parser.add_argument("--from-html",type=Path);args=parser.parse_args()
    path=ROOT/"data/mission-registry.json"
    if args.refresh:
        registry=refresh();path.write_text(json.dumps(registry,indent=2,ensure_ascii=True)+"\n",encoding="utf-8")
    elif args.from_html:
        raw=args.from_html.read_bytes();registry=snapshot(parse_table(raw.decode("utf-8")),hashlib.sha256(raw).hexdigest());path.write_text(json.dumps(registry,indent=2,ensure_ascii=True)+"\n",encoding="utf-8")
    else:registry=json.loads(path.read_text(encoding="utf-8"))
    catalog=json.loads((ROOT/"data/catalog.json").read_text(encoding="utf-8"));report=apply_registry(catalog,registry)
    for name,value in (("catalog.json",catalog),("mission-coverage.json",report)):
        (ROOT/"data"/name).write_text(json.dumps(value,indent=2,ensure_ascii=True)+"\n",encoding="utf-8")
    print(f"Mapped all {report['mapped_record_count']} CEOS records into {report['catalog_record_count']} catalog records.")


if __name__=="__main__":main()
