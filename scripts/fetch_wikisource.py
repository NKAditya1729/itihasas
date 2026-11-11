"""Fetch the Vālmīki Rāmāyaṇa sarga pages from Sanskrit Wikisource (CC BY-SA 4.0).

Polite: one request at a time, at least 2 s apart, 50 titles per request.
Every raw API response is kept under cache/wikisource/ with the revision id and
timestamp, so the base text is pinned and re-buildable offline.

Usage: uv run python scripts/fetch_wikisource.py [--refresh]
"""
from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://sa.wikisource.org/w/api.php"
UA = "ramayana-reader-build/0.1 (static Sanskrit study site; polite batch fetch)"
ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache" / "wikisource"
PREFIX = "रामायणम्/"
KANDAS = ["बालकाण्डम्", "अयोध्याकाण्डम्", "अरण्यकाण्डम्", "किष्किन्धाकाण्डम्",
          "सुन्दरकाण्डम्", "युद्धकाण्डम्", "उत्तरकाण्डम्"]
_last = 0.0


def get(params: dict, gap: float = 5.0) -> dict:
    global _last
    body = urllib.parse.urlencode({**params, "format": "json", "formatversion": "2",
                                   "maxlag": "5"}).encode()
    for attempt in range(6):
        wait = gap - (time.monotonic() - _last)
        if wait > 0:
            time.sleep(wait)
        req = urllib.request.Request(API, data=body, headers={"User-Agent": UA})  # POST: long title lists
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.load(r)
            _last = time.monotonic()
            return data
        except urllib.error.HTTPError as e:
            _last = time.monotonic()
            if e.code not in (429, 503):
                raise
            back = int(e.headers.get("Retry-After") or 0) or 30 * (attempt + 1)
            print(f"HTTP {e.code}; waiting {back}s")
            time.sleep(back)
    raise RuntimeError("gave up after repeated rate limiting")


def list_titles() -> list[str]:
    titles, cont = [], {}
    while True:
        d = get({"action": "query", "list": "allpages", "apprefix": PREFIX,
                 "apnamespace": 0, "aplimit": 500, **cont})
        titles += [p["title"] for p in d["query"]["allpages"]]
        if "continue" not in d:
            return titles
        cont = d["continue"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()
    CACHE.mkdir(parents=True, exist_ok=True)
    tpath = CACHE / "titles.json"
    if args.refresh or not tpath.exists():
        tpath.write_text(json.dumps(list_titles(), ensure_ascii=False, indent=1))
    titles = json.loads(tpath.read_text())
    sargas = [t for t in titles if any(t.startswith(PREFIX + k + "/सर्गः") for k in KANDAS)]
    print(f"{len(titles)} pages under {PREFIX}; {len(sargas)} sarga pages")
    for i in range(0, len(sargas), 50):
        out = CACHE / f"batch_{i // 50:03d}.json"
        if out.exists() and not args.refresh:
            continue
        d = get({"action": "query", "prop": "revisions", "rvprop": "ids|timestamp|content",
                 "rvslots": "main", "titles": "|".join(sargas[i:i + 50])})
        out.write_text(json.dumps(d, ensure_ascii=False))
        print("wrote", out.name)


if __name__ == "__main__":
    main()
