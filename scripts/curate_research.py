"""Prepare explicitly curated topic-to-collection routes. No network at build time."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
path=ROOT / "data/research-topics.json"
profile=json.loads(path.read_text(encoding="utf-8"))
for topic in profile["topics"]:
    topic["routes"]=["sentinel3-aod" if r=="modis-aod" else r for r in topic["routes"]]
    if topic["id"] in ("aerosol","air-quality"):
        topic["platforms"]=list(dict.fromkeys(topic["platforms"]+["sentinel-3a","sentinel-3b"]))
        topic["routes"]=list(dict.fromkeys(topic["routes"]+["modis-aod"]))
    if topic["id"] in ("no2","air-quality"):
        topic["routes"]=list(dict.fromkeys(topic["routes"]+["omi-no2"]))

data=[
 ("s5p-no2","Sentinel-5P · TROPOMI NO₂ OFFL","https://stac.dataspace.copernicus.eu/v1","sentinel-5p-l2-no2-offl","NO₂ atmospheric columns","NetCDF","Metadata public; CDSE asset downloads require authentication","Check timeliness, version, qa_value, units and averaging kernels.",["sentinel-5p"],["tropomi-no2","stac-cdse"]),
 ("tempo-no2","Intelsat 40e · TEMPO NO₂ V04","https://cmr.earthdata.nasa.gov/stac/LARC_CLOUD","TEMPO_NO2_L2_V04","NO₂ atmospheric columns, North America","NetCDF","Metadata public; Earthdata Login may be required for assets","A regional, daytime geostationary pathway. TEMPO is an instrument on Intelsat 40e.",["intelsat-40e"],["tempo-products"]),
 ("sentinel3-aod","Sentinel-3 · SYNERGY aerosol optical depth","https://planetarycomputer.microsoft.com/api/stac/v1","sentinel-3-synergy-aod-l2-netcdf","Aerosol optical depth","NetCDF","Metadata public; asset access may need provider signing","AOD is not PM₂.₅. This route serves Sentinel-3, not every aerosol candidate.",["sentinel-3a","sentinel-3b"],["stac-pc"]),
 ("sentinel1-radar","Sentinel-1 · radiometric terrain-corrected radar","https://planetarycomputer.microsoft.com/api/stac/v1","sentinel-1-rtc","Radar backscatter for water-extent inference","GeoTIFF / COG","Metadata public; asset access may need provider signing","Flood maps require additional processing. Inspect actual Item platform and polarisation.",["sentinel-1a","sentinel-1b","sentinel-1c"],["stac-pc"]),
 ("landsat-temperature","Landsat · Collection 2 Level 2","https://earth-search.aws.element84.com/v1","landsat-c2-l2","Surface reflectance and surface temperature","GeoTIFF / COG","Public metadata and open-data assets; inspect Item license","Collection spans Landsat 4/5/7/8/9. Temperature is a retrieval, not air temperature.",["landsat-4","landsat-5","landsat-7","landsat-8","landsat-9"],["stac-earth-search","landsat-products"]),
 ("sentinel2-reflectance","Sentinel-2 · Level-2A surface reflectance","https://earth-search.aws.element84.com/v1","sentinel-2-l2a","Surface reflectance; vegetation, snow and water inference","GeoTIFF / COG","Public metadata and open-data assets; inspect Item license","Audited collection summary names Sentinel-2A/2B. Confirm platform per Item; 2C support is not assumed here.",["sentinel-2a","sentinel-2b"],["stac-earth-search"]),
 ("sentinel3-ocean","Sentinel-3 · OLCI water full-resolution NTC","https://stac.dataspace.copernicus.eu/v1","sentinel-3-olci-2-wfr-ntc","Water-leaving radiance and ocean-colour retrievals","NetCDF product","Metadata public; CDSE asset downloads require authentication","Inspect coastal algorithm validity, atmospheric correction and QA.",["sentinel-3a","sentinel-3b"],["stac-cdse"])
]
data.extend([
 ("omi-no2","Aura · OMI NO₂ V004","https://cmr.earthdata.nasa.gov/cloudstac/GES_DISC","OMNO2_004","NO₂ atmospheric columns","HDF-EOS5","Metadata public; Earthdata Login may be required for assets","Inspect row-anomaly flags, retrieval version, units, QA and sampling. Archive availability is not current instrument health.",["aura"],["omi-mission"]),
 ("modis-aod","Terra + Aqua · MODIS MAIAC aerosol optical depth","https://cmr.earthdata.nasa.gov/cloudstac/LPCLOUD","MCD19A2_061","Aerosol optical depth","HDF-EOS2","Metadata public; Earthdata Login may be required for assets","MAIAC AOD is not surface PM2.5 concentration. Check QA, cloud/snow masks and validation.",["terra","aqua"],["nasa-aerosols"])
])
profile["routes"]=[dict(id=k,label=label,endpoint=endpoint,collection=collection,collection_url=endpoint+"/collections/"+collection,
                        measurement=measurement,format=fmt,access_note=access,note=note,platforms=platforms,sources=sources,verified="2026-11-03")
                     for k,label,endpoint,collection,measurement,fmt,access,note,platforms,sources in data]
path.write_text(json.dumps(profile,indent=2,ensure_ascii=True)+"\n",encoding="utf-8")
print("Prepared",len(data),"curated collection routes")
