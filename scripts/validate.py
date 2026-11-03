"""Validate editorial data, source closure and notebook code before a build."""
from __future__ import annotations

import ast
import datetime as dt
import json
import sys
from pathlib import Path

import jsonschema
import nbformat

ROOT=Path(__file__).resolve().parents[1]


def main():
    catalog=json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8"))
    schema=json.loads((ROOT / "data/catalog.schema.json").read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema,format_checker=jsonschema.FormatChecker()).validate(catalog)
    sources=catalog["sources"]
    ids=[s["id"] for s in catalog["satellites"]]
    assert len(ids)==len(set(ids)),"Duplicate platform IDs"

    def check_refs(value):
        if isinstance(value,dict):
            for key,item in value.items():
                if key=="sources" and isinstance(item,list):
                    assert item,"Empty source list"
                    assert set(item)<=set(sources),f"Unknown source IDs: {item}"
                elif key=="evidence":
                    for field,refs in item.items():
                        assert refs and set(refs)<=set(sources),f"Invalid {field} evidence"
                else:
                    check_refs(item)
        elif isinstance(value,list):
            for item in value:
                check_refs(item)
    check_refs(catalog)
    for s in catalog["satellites"]:
        assert {"mission","orbit","sensors","products"}<=set(s["evidence"])
        assert s["status_note"].strip() and s["orbit"]["temporal_note"].strip()
        assert dt.date.fromisoformat(s["verified"])<=dt.date.fromisoformat(catalog["verified"])
        if s["status"]=="retired":
            assert s.get("end"),"Retired mission needs an end qualifier"
        sensor_ids=[i["id"] for i in s["sensors"]]
        assert len(sensor_ids)==len(set(sensor_ids)),"Duplicate sensor ID within platform"
        assert 0<=s["display"]["x"]<=1200 and 0<=s["display"]["y"]<=650
        for field,refs in s["evidence"].items():
            assert set(refs)<=set(s["sources"]),f"{s['id']}: {field} evidence absent from platform source registry"
    for app in catalog["applications"]:
        assert set(app["satellites"])<=set(ids),"Application refers to unknown platform"
    notebook_paths=sorted((ROOT / "notebooks").glob("*.ipynb"))
    assert len(notebook_paths)==8,"Expected eight guided lessons"
    for path in notebook_paths:
        notebook=nbformat.read(path,as_version=4)
        nbformat.validate(notebook)
        for cell in notebook.cells:
            if cell.cell_type=="code":
                ast.parse(cell.source,filename=str(path))
    sys.path.insert(0,str(ROOT / "src"))
    from eo_guide import orbital_period_minutes, synthetic_reflectance, research_matches
    discovery=json.loads((ROOT / "data/research-topics.json").read_text(encoding="utf-8"))
    topic_ids={t["id"] for t in discovery["topics"]}
    route_ids={r["id"] for r in discovery["routes"]}
    assert len(topic_ids)==len(discovery["topics"]) and len(route_ids)==len(discovery["routes"])
    for t in discovery["topics"]:
        assert set(t["platforms"])<=set(ids) and set(t["routes"])<=route_ids
        assert t["caution"] and t["chain"] and set(t["sources"])<=set(sources)
        if t.get("broader"):
            assert t["broader"] in topic_ids
    for r in discovery["routes"]:
        assert set(r["platforms"])<=set(ids) and set(r["sources"])<=set(sources)
        assert r["collection_url"]==r["endpoint"]+"/collections/"+r["collection"]
        assert r["access_note"] and r["format"] and r["verified"]
    no2=research_matches("air quality and NO₂ measures",discovery)
    assert no2["concepts"]==["no2"] and set(no2["platforms"])=={"sentinel-5p","aura","intelsat-40e"}
    assert not research_matches("NO20 dinosaur observations",discovery)["concepts"]
    assert "no2" not in research_matches("aerosol and PM2.5",discovery)["concepts"]
    coverage=json.loads((ROOT / "data/stac-coverage.json").read_text(encoding="utf-8"))
    assert set(coverage["mapped_platform_ids"])<=set(ids)
    audit=json.loads((ROOT / "data/stac-audit.json").read_text(encoding="utf-8"))
    assert len(audit["catalogs"])==coverage["catalog_count"]
    assert all(c["documents_checked"]<=audit["limits"]["documents_per_catalog"] for c in audit["catalogs"])
    assert all(a["documents_checked"]<=a["page_limit"] for a in audit.get("supplemental_audits",[]))
    orbits=json.loads((ROOT / "data/orbit-types.json").read_text(encoding="utf-8"))
    for orbit in orbits["types"]:
        assert orbit["description"] and set(orbit["sources"])<=set(sources)
        assert len(orbit["color"])==7 and orbit["color"].startswith("#")
    geometry=json.loads((ROOT / "data/geometry-presets.json").read_text(encoding="utf-8"))
    assert len({p["id"] for p in geometry["presets"]})==len(geometry["presets"])
    for p in geometry["presets"]:
        assert p["id"] in ids and p["altitude_km"]>0 and p["pixel_x_m"]>0 and p["pixel_y_m"]>0
        assert p["route"] in route_ids and set(p["sources"])<=set(sources)
        if p["kind"]=="leo":
            assert 0<=p["inclination_deg"]<=180 and p["swath_km"]>0
        else:
            assert p["kind"]=="geo" and len(p["envelope"])==4
        for concept,override in p.get("measurement_overrides",{}).items():
            assert concept in topic_ids and override["pixel_x_m"]>0 and override["pixel_y_m"]>0
            assert set(override["sources"])<=set(sources)
    assert abs(orbital_period_minutes(705)-98.73)<.5
    assert 1435<orbital_period_minutes(35786)<1440
    assert all(0<synthetic_reflectance(w)<1 for w in range(400,2401))
    print(f"Validated {len(ids)} platforms, {len(sources)} sources, {len(catalog['applications'])} pathways and {len(notebook_paths)} executable notebooks.")


if __name__=="__main__":
    main()
