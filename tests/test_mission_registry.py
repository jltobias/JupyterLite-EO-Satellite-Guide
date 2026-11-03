"""Coverage, identity and lifecycle boundaries for the global mission inventory."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from mission_registry import HOSTS,apply_registry,key,numeric,parse_table


class MissionRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog=json.loads((ROOT/"data/catalog.json").read_text(encoding="utf-8"))
        cls.registry=json.loads((ROOT/"data/mission-registry.json").read_text(encoding="utf-8"))
        cls.report=json.loads((ROOT/"data/mission-coverage.json").read_text(encoding="utf-8"))

    def test_full_source_roster_and_named_families_are_accounted_for(self):
        by_id={s["id"]:s for s in self.catalog["satellites"]}
        self.assertEqual({r["id"] for r in self.registry["records"]},{r["registry_id"] for r in self.report["crosswalk"]})
        for prefix,last in (("landsat",10),("noaa",21),("goes",19)):
            self.assertTrue({f"{prefix}-{n}" for n in range(1,last+1)}<=set(by_id))
        expected={"sentinel-1a","sentinel-1b","sentinel-1c","sentinel-1d","sentinel-2a","sentinel-2b","sentinel-2c","sentinel-2d",
            "sentinel-3a","sentinel-3b","sentinel-3c","sentinel-3d","sentinel-5p","sentinel-6a","sentinel-6b",*HOSTS.values()}
        self.assertTrue(expected<=set(self.report["families"]["sentinel"]))
        for r in self.registry["records"]:
            if r["name"].startswith("Sentinel"):
                match=next(x for x in self.report["crosswalk"] if x["registry_id"]==r["id"])
                self.assertIn(match["platform_id"],self.report["families"]["sentinel"])

    def test_hosted_payloads_do_not_become_duplicate_spacecraft(self):
        by_id={s["id"]:s for s in self.catalog["satellites"]}
        for payload,host in HOSTS.items():
            self.assertNotIn(payload,by_id)
            self.assertIn(payload,{m["id"] for m in by_id[host]["hosted_missions"]})
        self.assertIn("Sentinel-5A",by_id["metop-sg-a1"]["name"])
        self.assertNotEqual(key("Sentinel-5 precursor"),"metop-sg-a1")

    def test_failed_and_planned_missions_do_not_claim_observations(self):
        by_id={s["id"]:s for s in self.catalog["satellites"]}
        self.assertEqual(by_id["landsat-6"]["status"],"failed")
        self.assertEqual(by_id["landsat-6"]["orbit"]["class"],"No orbit achieved")
        self.assertIsNone(by_id["landsat-6"]["orbit"]["altitude_km"])
        self.assertEqual(by_id["landsat-10"]["status"],"planned")
        self.assertIsNone(by_id["landsat-10"]["end"])
        self.assertEqual(by_id["suomi-npp"]["end"],"2026-11-02")

    def test_reconciliation_is_idempotent(self):
        catalog=copy.deepcopy(self.catalog);apply_registry(catalog,self.registry)
        before=json.dumps(catalog,sort_keys=True);apply_registry(catalog,self.registry)
        self.assertEqual(before,json.dumps(catalog,sort_keys=True))

    def test_source_parser_rejects_missing_tables_and_ambiguous_numbers(self):
        with self.assertRaises(ValueError):parse_table("<p>Service unavailable</p>")
        self.assertEqual(numeric("824 km","km"),824)
        self.assertIsNone(numeric("400-800 km","km"))
        self.assertIsNone(numeric("1899-12-30T16:44:00.000Z","mins"))


if __name__=="__main__":unittest.main()
