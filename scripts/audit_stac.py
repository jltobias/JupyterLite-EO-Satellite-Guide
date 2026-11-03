"""Explicit, bounded metadata-only STAC Index audit; builds never run this crawler.

python scripts/audit_stac.py --refresh
Only public, credential-free HTTPS metadata links are requested. No assets.
Per-catalog bounds, failures and skipped listings remain in the saved report.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import json
import re
from collections import deque
from pathlib import Path
from urllib.parse import urljoin, urlsplit, parse_qsl
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = "https://stacindex.org/api/catalogs"
MAX_DOCS = 100
MAX_BYTES = 6_000_000


def safe(url):
    p = urlsplit(url)
    return (p.scheme == "https" and p.hostname and not p.username and not p.password
            and not re.search(r"(?:epat_|eyJ)[A-Za-z0-9_-]{15,}", p.path)
            and not any(any(t in k.lower() for t in ("key", "token", "signature", "credential"))
                        for k, _ in parse_qsl(p.query)))


def fetch(url):
    if not safe(url):
        raise ValueError("Not a credential-free HTTPS metadata URL")
    with urlopen(Request(url, headers={"User-Agent": "Global-EO-Guide/2.0 metadata-audit",
                                      "Accept": "application/json"}), timeout=12) as response:
        if not safe(response.url):
            raise ValueError("Unsafe metadata redirect")
        raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("Metadata response exceeds byte bound")
        return json.loads(raw), response.url


def values(value):
    if isinstance(value, list):
        return [str(v) for v in value if isinstance(v, (str, int, float))]
    if isinstance(value, str):
        return [value]
    return []


def record(doc, url, listing):
    summary = doc.get("summaries", {})
    props = doc.get("properties", {})
    platforms = values(summary.get("platform")) + values(props.get("platform"))
    instruments = values(summary.get("instruments")) + values(props.get("instruments"))
    return {"catalog": listing["slug"], "id": str(doc.get("id", "")),
            "title": doc.get("title", doc.get("id", "")), "url": url,
            "type": doc.get("type", "Collection" if "extent" in doc else "Catalog"),
            "platforms": sorted(set(platforms)), "instruments": sorted(set(instruments)),
            "constellation": values(summary.get("constellation")) + values(props.get("constellation")),
            "keywords": values(doc.get("keywords")), "license": doc.get("license"),
            "gsd": summary.get("gsd", props.get("gsd")),
            "description": str(doc.get("description", ""))[:1200]}


def audit_listing(listing):
    result = {k: listing.get(k) for k in ("slug", "title", "url", "access", "isApi")}
    result.update({"documents_checked": 0, "collections": [], "errors": [], "omitted_depth_links": 0})
    if listing.get("access") != "public" or not safe(listing["url"]):
        result["status"] = "skipped-access-or-url"
        # Never redistribute credential-bearing addresses from directory listings.
        if not safe(listing["url"]):
            result["url"] = None
        return result
    queue = deque([(listing["url"], 0)])
    seen = set()
    while queue and len(seen) < MAX_DOCS:
        url, depth = queue.popleft()
        if url in seen or not safe(url):
            continue
        seen.add(url)
        try:
            doc, base = fetch(url)
            if not isinstance(doc, dict):
                raise ValueError("Not a STAC JSON object")
            result["documents_checked"] += 1
            docs = doc.get("collections", [doc])
            for entry in docs:
                if not isinstance(entry, dict):
                    continue
                entry_url = next((urljoin(base, l["href"]) for l in entry.get("links", [])
                                  if l.get("rel") == "self" and safe(urljoin(base, l.get("href", "")))), base)
                if entry.get("type") in ("Collection", "Feature") or entry.get("summaries") or "extent" in entry:
                    result["collections"].append(record(entry, entry_url, listing))
            links = doc.get("links", [])
            for link in links:
                rel = link.get("rel")
                if rel == "next" or (rel in ("data", "child") and depth < 3):
                    if link.get("method", "GET") == "GET":
                        queue.append((urljoin(base, link.get("href", "")), depth + (rel != "next")))
                elif rel in ("data", "child"):
                    result["omitted_depth_links"] += 1
            # Only sample one Item where a Collection omits platform metadata.
            if not record(doc, base, listing)["platforms"]:
                link = next((l for l in links if l.get("rel") == "item"), None)
                if link:
                    queue.append((urljoin(base, link["href"]), depth + 1))
        except Exception as exc:
            result["errors"].append({"url": url, "error": str(exc)[:240]})
    result["remaining_links"] = len(queue)
    result["status"] = ("unavailable" if not result["documents_checked"] else
                        "partial" if queue or result["errors"] or result["omitted_depth_links"] else "metadata-checked")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true", required=True)
    parser.add_argument("--catalog", action="append", help="Refresh only these registry slugs; retain other saved results")
    args = parser.parse_args()
    listings, _ = fetch(REGISTRY)
    assert isinstance(listings, list) and 1 < len(listings) < 2000
    previous = None
    if (ROOT / "data/stac-audit.json").exists():
        previous = json.loads((ROOT / "data/stac-audit.json").read_text(encoding="utf-8"))
    if args.catalog:
        assert previous is not None, "A selective refresh needs a saved directory audit"
        listings = [x for x in listings if x["slug"] in args.catalog]
    report = {"retrieved": dt.datetime.now(dt.timezone.utc).isoformat(), "source": REGISTRY,
              "limits": {"documents_per_catalog": MAX_DOCS, "depth": 3,
                         "bytes_per_document": MAX_BYTES, "timeout_seconds": 12},
              "scope": "Directory-wide bounded metadata audit, not an exhaustive satellite inventory. "
                       "No assets fetched. Item platform values are samples. Protected, failing and "
                       "truncated catalogs remain explicit. Collection summaries can omit missions.",
              "catalogs": []}
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        futures = {pool.submit(audit_listing, x): x for x in listings}
        for f in concurrent.futures.as_completed(futures):
            value = f.result()
            report["catalogs"].append(value)
            print(value["slug"], value["status"], value["documents_checked"],
                  len(value["collections"]), flush=True)
    if previous and args.catalog:
        refreshed = {c["slug"] for c in report["catalogs"]}
        report["catalogs"].extend(c for c in previous["catalogs"] if c["slug"] not in refreshed)
    report["catalogs"].sort(key=lambda x: x["slug"])
    if previous and previous.get("supplemental_audits"):
        report["supplemental_audits"] = previous["supplemental_audits"]
    # Descriptions aid review locally; only identifiers/facts are redistributed.
    for c in report["catalogs"]:
        for r in c["collections"]:
            r.pop("description", None)
    target = ROOT / "data/stac-audit.json"
    target.write_text(json.dumps(report, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print("Saved", target)


if __name__ == "__main__":
    main()
