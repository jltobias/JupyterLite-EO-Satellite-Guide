"""Scientific-discovery boundaries and public metadata request contracts."""
import asyncio
import json
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT / "src"),str(ROOT / "scripts")]
from eo_guide import research_matches, search_stac
from curate_stac import identity, constellation_identity
from audit_stac import audit_listing, safe
from build import script_json


class ResearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile=json.loads((ROOT / "data/research-topics.json").read_text(encoding="utf-8"))

    def test_specific_pollutant_excludes_broad_parent(self):
        result=research_matches("What can inform air quality and NO₂ measures?",self.profile)
        self.assertEqual(result["concepts"],["no2"])
        self.assertEqual(set(result["platforms"]),{"sentinel-5p","aura","intelsat-40e","meteosat-13","metop-sg-a1"})
        self.assertEqual({r["id"] for r in result["routes"]},{"s5p-no2","tempo-no2","omi-no2"})
        self.assertTrue(any("not ground-level" in q for q in result["qualifications"]))

    def test_no_substring_or_unrestricted_reasoning(self):
        self.assertEqual(research_matches("NO20 and dinosaurs",self.profile)["concepts"],[])
        self.assertEqual(research_matches("aerosols and PM2.5",self.profile)["concepts"],["aerosol"])

    def test_spacecraft_identity_and_non_satellite_exclusions(self):
        self.assertEqual(identity("JPSS-1","nasa-cmr-cloudstac-proxy")[0],"noaa-20")
        self.assertEqual(identity("DMSP 5D-3/F16","nasa-cmr-cloudstac-proxy")[0],"dmsp-f16")
        self.assertEqual(identity("IS-40e","nasa-cmr-cloudstac-proxy")[0],"intelsat-40e")
        for name in ("MERRA-2","NOAA Twin Otter","FIELD INVESTIGATION","G-III","UAV"):
            self.assertIsNone(identity(name,"nasa-cmr-cloudstac-proxy"))
        self.assertEqual(constellation_identity("capella","capella-space-open-data")[2],"constellation / mission group")
        self.assertIsNone(constellation_identity("modis","fixture"))

    def test_catalog_failure_is_reported_and_assets_are_not_followed(self):
        documents={"https://example.org/":({"type":"Catalog","links":[
            {"rel":"child","href":"c.json"},{"rel":"enclosure","href":"raster.tif"}]},"https://example.org/"),
            "https://example.org/c.json":RuntimeError("provider unavailable")}
        calls=[]
        def fake(url):
            calls.append(url);value=documents[url]
            if isinstance(value,Exception):raise value
            return value
        with patch("audit_stac.fetch",side_effect=fake):
            report=audit_listing({"slug":"fixture","title":"Fixture","url":"https://example.org/","access":"public","isApi":False})
        self.assertEqual(report["status"],"partial")
        self.assertEqual(calls,["https://example.org/","https://example.org/c.json"])
        self.assertIn("provider unavailable",report["errors"][0]["error"])
        self.assertFalse(safe("https://example.org/?api_key=secret"))
        self.assertFalse(safe("https://example.org/epat_abcdefghijklmnopqrstuv"))

    def test_live_helper_requests_only_bounded_item_metadata(self):
        calls=[]
        class Response:
            ok=True
            status=200
            async def string(self):
                return json.dumps({"type":"FeatureCollection","features":[{"type":"Feature","id":"fixture","assets":{"data":{"href":"https://example.org/asset.tif"}}}]})
        async def fake(url,**kwargs):
            calls.append((url,kwargs));return Response()
        route={"collection_url":"https://example.org/collections/no2"}
        with patch.dict(sys.modules,{"pyodide":types.ModuleType("pyodide"),"pyodide.http":types.SimpleNamespace(pyfetch=fake)}):
            result=asyncio.run(search_stac(route,bbox=[-76,39,-74,41],start="2025-07-01",end="2025-07-07",limit=3))
            self.assertEqual(len(result["features"]),1)
            self.assertEqual(len(calls),1)
            self.assertIn("/items?",calls[0][0]);self.assertIn("limit=3",calls[0][0])
            self.assertEqual(calls[0][1],{"credentials":"omit"})
            with self.assertRaises(ValueError):
                asyncio.run(search_stac(route,bbox=[-74,39,-76,41],start="2025-07-01",end="2025-07-07",limit=3))
            with self.assertRaises(ValueError):
                asyncio.run(search_stac(route,bbox=[-76,39,-74,41],start="2025-07-01",end="2025-07-07",limit=3000))
        self.assertEqual(len(calls),1)

    def test_provider_text_cannot_end_the_offline_data_script(self):
        from html.parser import HTMLParser
        tags=[]
        class Parser(HTMLParser):
            def handle_starttag(self,tag,attrs):tags.append(tag)
        value={"title":"</script><img src=x onerror=alert(1)>"}
        serialized=script_json(value)
        Parser().feed("<script>window.payload="+serialized+";</script>")
        self.assertEqual(tags,["script"])
        self.assertEqual(json.loads(serialized),value)


if __name__=="__main__":unittest.main()
