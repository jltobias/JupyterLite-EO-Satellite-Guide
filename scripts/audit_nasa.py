"""Explicit supplementary, paginated NASA cloud STAC collection-summary audit.

python scripts/audit_nasa.py --refresh
Up to 40 pages/4,000 collection summaries. No Item/asset requests. Preserves the
directory audit and records this additional, independently bounded walk.
"""
import argparse
import datetime as dt
import json
from pathlib import Path
from urllib.parse import urljoin

from audit_stac import fetch, record

ROOT=Path(__file__).resolve().parents[1]
ROOT_URL="https://cmr.earthdata.nasa.gov/cloudstac/ALL/collections?limit=100"


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh",action="store_true",required=True)
    parser.parse_args()
    path=ROOT / "data/stac-audit.json"
    audit=json.loads(path.read_text(encoding="utf-8"))
    listing=next(c for c in audit["catalogs"] if c["slug"]=="nasa-cmr-cloudstac-proxy")
    result={"root":ROOT_URL,"catalog":listing["slug"],"retrieved":dt.datetime.now(dt.timezone.utc).isoformat(),
            "page_limit":40,"documents_checked":0,"collections":[],"errors":[]}
    url=ROOT_URL;seen=set()
    while url and url not in seen and len(seen)<40:
        seen.add(url)
        try:
            doc,base=fetch(url)
            result["documents_checked"]+=1
            for c in doc.get("collections",[]):
                self_url=next((urljoin(base,l["href"]) for l in c.get("links",[]) if l.get("rel")=="self"),base)
                r=record(c,self_url,listing);r.pop("description",None)
                result["collections"].append(r)
            url=next((urljoin(base,l["href"]) for l in doc.get("links",[]) if l.get("rel")=="next"),None)
            print(result["documents_checked"],len(result["collections"]),flush=True)
        except Exception as exc:
            result["errors"].append(str(exc)[:240]);break
    result["status"]="partial" if url or result["errors"] else "metadata-checked"
    audit["supplemental_audits"]=[result]
    path.write_text(json.dumps(audit,indent=2,ensure_ascii=True)+"\n",encoding="utf-8")
    print("Saved NASA summary audit:",result["status"])


if __name__=="__main__":main()
