"""Reconcile the saved audit through an explicit, reviewable satellite crosswalk.

No network. Metadata mentions do not prove current operations or usable assets.
The report preserves all unrecognized and non-satellite platform identifiers.
"""
from __future__ import annotations

import collections
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-11-03"


def load(name):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def save(name, value):
    (ROOT / "data" / name).write_text(json.dumps(value, indent=2, ensure_ascii=True)+"\n", encoding="utf-8")


def identity(raw, catalog):
    key = re.sub(r"[^a-z0-9]+", "-", raw.lower()).strip("-")
    aliases = {"alos":"alos-1", "earth-observing-1":"eo-1", "sentinel-5-precursor":"sentinel-5p",
               "sentinel-3-olci":"sentinel-3", "formosat2":"formosat-2", "suomi-npp":"suomi-npp",
               "is-40e":"intelsat-40e", "srtm":"endeavour-srtm", "sts-99":"endeavour-srtm", "ov-105":"endeavour", "planet":"planet-mixed",
               "jpss-1":"noaa-20", "jpss-2":"noaa-21", "tsx":"terrasar-x", "tdx":"tandem-x", "mt1":"megha-tropiques",
               "aquarius-sac-d":"sac-d", "ostm-jason-2":"jason-2", "topex-poseidon":"topex-poseidon",
               "scisat-1-ace":"scisat-1", "cosmic-2-formosat-7":"cosmic-2", "cosmic-formosat-3":"cosmic-1",
               "seasat-1":"seasat-1", "hexagon-kh-9":"hexagon-kh-9", "ep-toms":"earth-probe-toms",
               "cosmo-skymed-second-generation-csg":"cosmo-skymed-second-generation"}
    key = aliases.get(key, key)
    key = re.sub(r"^(noaa|meteosat)-?0?(\d+)$", r"\1-\2", key)
    if raw.startswith("DMSP"):
        f = re.search(r"[Ff](\d+)$", raw)
        if f:
            key = "dmsp-f"+f[1]
    if catalog in ("planet-labs-stac-catalog", "disaster-data-releases-from-planet-labs-pbc") and re.fullmatch(r"(?:[0-9a-f]{4}|SSC\d+|SS02)", raw):
        return "planet-"+raw.lower(), "Planet "+raw, "spacecraft identifier"
    exact = {"adeos-i","adeos-ii","aem-2","aeolus","amazonia-1","aqua","aura","biros","beijing-1","belka","biomass",
             "calipso","cbers","cfosat","champ","cosmo-skymed","cosmo-skymed-second-generation","cloudsat","cryosat-2",
             "earthcare","enmap","envisat","eo-1","firebird","flex","formosat-2","fsscat","goce","goes","iceye","irs-p5",
             "iss","metop","meteosat","mfg","msg","mtg","noaa-poes","orbview-2","planet-mixed","planetscope","proba-v","quikscat",
             "rapideye","sentinel-2","sentinel-3","smos","suomi-npp","tandem-x","terra","terrasar-x","tiros-n","vision-1","paz",
             "endeavour-srtm","endeavour","intelsat-40e","noaa-21","pace","acrimsat","coms","coriolis","cygnss","dmsp","dscovr",
             "earth-probe-toms","erbs","explorer-7","gfo-1","gms","gosat","gpm","grace","grace-fo","hexagon-kh-9","icesat","icesat-2",
             "landsat","megha-tropiques","mtsat","nisar","oco-2","sac-d","saral","scisat-1","seasat-1","smap","sms-1","spire",
             "swot","topex-poseidon","trmm","uars","planetiq-gnomes","cosmic-1","cosmic-2","eole"}
    pattern = r"(?:alos|cbers|cosmo-skymed|dmsp-f|ers|fy-3|gcom-[cw]|geoeye|geosat|ghgsat-c|gms|goes|himawari|kompsat|landsat|meteosat|metop|nigeriasat|noaa|pleiades|pleiades-neo|quickbird|radarsat|resourcesat|sentinel|spot|uk-dmc|dragonette|worldview|irs|jason|nimbus|meteor|mtsat|prefire-sat|tropics)-?[0-9abcdefmpr]+"
    if key in exact or re.fullmatch(pattern, key):
        families = {"cbers","cosmo-skymed","cosmo-skymed-second-generation","firebird","fsscat","goes","iceye","metop","meteosat","mfg","msg","mtg","noaa-poes","planet-mixed","planetscope","rapideye","sentinel-2","sentinel-3","cosmic-1","cosmic-2","cygnss","dmsp","gms","landsat","mtsat","planetiq-gnomes","spire","grace","grace-fo","tandem-x"}
        return key, raw, "constellation / mission group" if key in families else "spacecraft"
    # These aliases need operator identity work before merging them with a spacecraft.
    if key in {"arcm1","arcm2","el2","el3","el4","el-arcm","elektro-l-n1","mm2-4"}:
        return key, raw, "spacecraft identifier"
    return None


def constellation_identity(raw,catalog):
    """Provider constellation fields also supply families when platform is absent."""
    key=re.sub(r"[^a-z0-9]+","-",raw.lower()).strip("-")
    groups={"a-train","beijing","capella","dmc","dragonette","formosat","geoeye","geosat","goes-r","himawari",
            "jpss","kompsat","nigeriasat","noaa","pelican","pleiades","pleiades-neo","quickbird","radarsat",
            "resourcesat","sentinel-1","sentinel-5","sentinel-6","skysat","spot","superview","tanager","tiros",
            "triplesat","uk-dmc","vision","worldview"}
    if key=="modis":
        return None  # An instrument name is not a spacecraft constellation.
    if key in groups:
        return key,raw+" (mission group)","constellation / mission group"
    if key=="alos":
        return "alos-family","ALOS (mission family)","constellation / mission group"
    if key=="proba-1":
        return key,"PROBA-1","spacecraft"
    return identity(raw,catalog)


def main():
    audit=load("stac-audit.json")
    catalog=load("catalog.json")
    # Re-running preserves the original curated records and replaces imported ones.
    catalog["satellites"]=[s for s in catalog["satellites"] if not s.get("stac_imported")]
    sources=catalog["sources"]
    extras={
      "stac-index":("STAC Index public catalog registry","STAC Index","https://stacindex.org/api/catalogs"),
      "stac-cdse":("Copernicus STAC collections","Copernicus Data Space Ecosystem","https://stac.dataspace.copernicus.eu/v1/collections?limit=1000"),
      "stac-earth-search":("Earth Search collections","Element 84","https://earth-search.aws.element84.com/v1/collections"),
      "stac-pc":("Planetary Computer collections","Microsoft","https://planetarycomputer.microsoft.com/api/stac/v1/collections"),
      "s5p-mission":("Sentinel-5P mission and orbit","ESA / Copernicus","https://sentiwiki.copernicus.eu/web/s5p-mission"),
      "tropomi-no2":("TROPOMI nitrogen dioxide product","KNMI / TROPOMI","https://www.tropomi.eu/data-products/nitrogen-dioxide"),
      "tempo-products":("TEMPO data for scientists","Smithsonian Astrophysical Observatory / NASA","https://tempo.si.edu/data_for_scientists.html"),
      "tempo-mission":("TEMPO mission overview","Smithsonian Astrophysical Observatory / NASA","https://tempo.si.edu/overview.html"),
      "omi-mission":("Ozone Monitoring Instrument","NASA Aura","https://aura.gsfc.nasa.gov/omi.html"),
      "nasa-aerosols":("MODIS aerosol products","NASA MODIS atmosphere team","https://atmosphere-imager.gsfc.nasa.gov/products/aerosol"),
      "modis-maiac":("MODIS Terra+Aqua MAIAC MCD19A2","NASA LAADS DAAC","https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/MCD19A2"),
      "dscovr-orbit":("DSCOVR L1 Lissajous orbit","NASA JPL","https://science.jpl.nasa.gov/projects/dscovr/"),
      "s3-orbit":("Sentinel-3 mission orbit","ESA / Copernicus","https://sentiwiki.copernicus.eu/web/s3-mission"),
      "eumetsat-orbits":("Meteosat, Metop and Sentinel launch/orbit overview","EUMETSAT","https://www.eumetsat.int/satellite-operations/launches-and-orbits"),
      "esa-orbits":("Types of orbits","ESA","https://www.esa.int/Enabling_Support/Space_Transportation/Types_of_orbits"),
      "fieldwork-profile":("FieldWork STAC application profile (experimental)","Digital Twin Public Health contributors","https://github.com/digital-twin-ph/fieldwork/blob/main/ontology/stac.ttl")}
    for key,(title,publisher,url) in extras.items():
        sources[key]={"title":title,"publisher":publisher,"url":url,"accessed":DATE}
    by_id={s["id"]:s for s in catalog["satellites"]}
    mentions=collections.defaultdict(list)
    crosswalk=[]
    for c in audit["catalogs"]:
        extra=[r for a in audit.get("supplemental_audits",[]) if a["catalog"]==c["slug"] for r in a["collections"]]
        for r in c["collections"]+extra:
            for field,raw in [("platform",p) for p in r["platforms"]]+[("constellation",p) for p in r["constellation"]]:
                match=identity(raw,c["slug"]) if field=="platform" else constellation_identity(raw,c["slug"])
                # Energy-catalog station names are not interpreted as spacecraft.
                if c["slug"]=="oie-stac-catalog" and not match:
                    category="non-satellite / station"
                else:
                    category="mapped" if match else "unresolved / non-satellite"
                crosswalk.append({"raw":raw,"field":field,"catalog":c["slug"],"document":r["url"],
                                  "platform_id":match[0] if match else None,"classification":category})
                if match:
                    mentions[match[0]].append((match,r,c))
    # TEMPO is a hosted instrument, not a spacecraft. The stable platform ID names its host.
    for sid in ("intelsat-40e","noaa-21","pace"):
        mentions.setdefault(sid,[])
    for sid,entries in sorted(mentions.items()):
        if sid in by_id:
            s=by_id[sid]
        else:
            match=entries[0][0] if entries else (sid,sid.replace("-"," ").upper(),"spacecraft")
            refs=list(dict.fromkeys(quote(r["url"],safe=":/?#[]@!$&'()*+,;=%") for _,r,_ in entries))
            source="stac-platform-"+sid
            sources[source]={"title":f"STAC metadata platform mention: {match[1]}","publisher":entries[0][2]["title"] if entries else "NASA",
                             "url":refs[0] if refs else "https://search.earthdata.nasa.gov/","accessed":DATE,
                             "locators":"Mission identity in provider platform/constellation metadata. This is not verification of operations, orbit or asset usability."}
            instruments=sorted({i for _,r,_ in entries for i in r.get("instruments",[])})
            s={"id":sid,"name":match[1],"agency":"Not curated; see provider metadata","region":"Not curated",
               "status":"unverified","status_note":"STAC metadata mention only; a catalog entry may be an archive, derived product, mission grouping or planned data. Operations and data access are not inferred.",
               "verified":DATE,"type":"other","launch":None,"end":None,"record_kind":match[2],"stac_imported":True,
               "purpose":"Discover source metadata and confirm the platform, instrument, product, coverage, access and license before use.",
               "orbit":{"class":"Unknown / not curated","altitude_km":None,"repeat_days":None,
                        "temporal_note":"Not curated. Collection extent is advertised archive coverage, not repeat, revisit or current operations."},
               "display":{"x":600,"y":80},"sources":[source],"evidence":{k:[source] for k in ("mission","orbit","sensors","products")},
               "sensors":[{"id":"metadata-instruments","name":", ".join(instruments[:6]) or "Instrument not curated",
                           "method":"Not curated; collection instrument list can span multiple platforms",
                           "observes":["Not curated"],"spatial":"Not curated; collection grid spacing is not native resolution",
                           "spectral":"Not curated","coverage":"Inspect collection extent and individual Item footprints",
                           "sources":[source],"products":[{"name":"Provider STAC metadata","level":"Not curated","access":refs[0] if refs else "https://search.earthdata.nasa.gov/",
                             "note":"Metadata discovery only. Follow Item assets and provider documentation for real data and rights.","sources":[source]}]}]}
            catalog["satellites"].append(s);by_id[sid]=s
        s["stac_collections"]=[{"catalog":c["slug"],"id":r["id"],"url":quote(r["url"],safe=":/?#[]@!$&'()*+,;=%"),"type":r["type"]} for _,r,c in entries]
        # Keep a compact set; the complete unabridged crosswalk is in stac-coverage.json.
        s["stac_collections"]=list({r["url"]:r for r in s["stac_collections"]}.values())

    def enrich(sid,name,agency,orbit,altitude,sensor,observes,spatial,spectral,temporal,refs,product_url):
        s=by_id[sid];s.update(name=name,agency=agency,type="atmosphere",record_kind="spacecraft",sensor_curation=True,sources=list(dict.fromkeys(s["sources"]+refs)))
        s["orbit"].update({"class":orbit,"altitude_km":altitude,"temporal_note":temporal})
        s["evidence"]={"mission":refs,"orbit":refs,"sensors":refs,"products":refs}
        s["sensors"]=[{"id":sensor.lower(),"name":sensor,"method":"Passive atmospheric spectroscopy; radiance to trace-gas retrieval",
                       "observes":observes,"spatial":spatial,"spectral":spectral,"coverage":"Check the cited product coverage and individual granules",
                       "sources":refs,"products":[{"name":sensor+" nitrogen dioxide column","level":"Level 2 retrieval",
                       "access":product_url,"note":"Atmospheric column retrieval, not surface concentration. Apply version-specific quality guidance.","sources":refs}]}]
    enrich("sentinel-5p","Sentinel-5P","ESA / Copernicus","Sun-synchronous LEO",824,"TROPOMI",["tropospheric nitrogen dioxide column","aerosol index"],
           "Product-dependent footprint; inspect version and across-track position. STAC advertises 3,500 m gsd; this is not a complete footprint specification.","UV, visible, NIR and SWIR spectrometers",
           "Near-daily global sampling; 16-day orbital cycle; 13:30 mean local solar time ascending node. Clouds and QA reduce usable retrievals.",
           ["s5p-mission","tropomi-no2","stac-cdse"],"https://stac.dataspace.copernicus.eu/v1/collections/sentinel-5p-l2-no2-offl")
    enrich("intelsat-40e","Intelsat 40e / TEMPO","Intelsat (host) / NASA + SAO (instrument)","Geostationary",35786,"TEMPO",["tropospheric nitrogen dioxide column"],
           "2.0 × 4.75 km nominal Level-2 footprint; varies with viewing geometry; Level-3 gridding is separate.","Ultraviolet-visible spectroscopy",
           "Hourly daytime scans over North America; scan schedule, cloud and quality affect usable sampling.",
           ["tempo-mission","tempo-products"],"https://cmr.earthdata.nasa.gov/stac/LARC_CLOUD/collections/TEMPO_NO2_L2_V04")
    if "aura" in by_id:
        enrich("aura","Aura / OMI","NASA","Sun-synchronous LEO",None,"OMI",["tropospheric nitrogen dioxide column"],
               "Product- and view-dependent; inspect OMI documentation and row-anomaly flags.","Ultraviolet-visible spectroscopy",
               "Daily global sampling design; usable observations depend on instrument status, row anomaly, clouds and QA.",
               ["omi-mission"],"https://aura.gsfc.nasa.gov/omi.html")
    if "dscovr" in by_id:
        s=by_id["dscovr"];s["orbit"]["class"]="Sun-Earth L1 Lissajous"
        s["orbit"]["temporal_note"]="Observes the sunlit Earth from near Sun-Earth L1. Sampling is product-dependent; distance from Earth is not a LEO altitude or repeat cycle."
        s["sources"].append("dscovr-orbit");s["evidence"]["orbit"]=["dscovr-orbit"]
    orbit_facts={
        **{sid:("Sun-synchronous LEO",814.5,"s3-orbit") for sid in ("sentinel-3a","sentinel-3b")},
        **{sid:("Sun-synchronous LEO",817,"eumetsat-orbits") for sid in ("metop-b","metop-c")},
        **{sid:("Geostationary",None,"eumetsat-orbits") for sid in ("meteosat-9","meteosat-10","meteosat-11")},
        "sentinel-6a":("LEO",1336,"eumetsat-orbits")}
    for sid,(kind,height,ref) in orbit_facts.items():
        if sid in by_id:
            s=by_id[sid];s["orbit"].update({"class":kind,"altitude_km":height})
            s["sources"].append(ref);s["evidence"]["orbit"]=[ref]
    # Orbit information is only transferred from same-series operator evidence for these explicit siblings.
    for sid,original in {"sentinel-1a":"sentinel-1c","sentinel-1b":"sentinel-1c","sentinel-1d":"sentinel-1c","sentinel-2a":"sentinel-2b"}.items():
        if sid in by_id:
            s=by_id[sid];ref=by_id[original]["evidence"]["orbit"]
            s["orbit"]["class"]="Sun-synchronous LEO";s["evidence"]["orbit"]=ref;s["sources"]=list(dict.fromkeys(s["sources"]+ref))
    catalog.update(version="2.0.0",verified=DATE,scope=f"{len(catalog['satellites'])} curated and STAC-discovered spacecraft / constellation records, including archives and mission groups. Directory-wide bounded audit; not an exhaustive inventory, operating-status feed or proof of usable assets. Imported specifications remain unknown unless independently curated.")
    save("catalog.json",catalog)
    unique={(r["raw"],r["catalog"],r["field"]):r for r in crosswalk}
    coverage={"verified":DATE,"audit":"stac-audit.json","catalog_count":len(audit["catalogs"]),
              "statuses":dict(collections.Counter(c["status"] for c in audit["catalogs"])),
              "platform_records":len(catalog["satellites"]),"mapped_platform_ids":sorted(mentions),
              "platform_crosswalk":list(unique.values()),"scope":audit["scope"]}
    save("stac-coverage.json",coverage)
    print("Curated",len(catalog["satellites"]),"records;",len(unique),"source identifier mappings")


if __name__=="__main__":
    main()
