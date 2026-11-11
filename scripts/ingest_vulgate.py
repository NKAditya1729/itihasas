"""Phase 1 ingest: cached Wikisource pages → data/vr/{k}/{sss}.json + meta files.

Idempotent: rerunning rewrites the same files from the same cache.
Usage: uv run python scripts/ingest_vulgate.py
"""
from __future__ import annotations

import collections
import glob
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vrtools.build import KANDA_NAMES, make_sarga, mula_hash  # noqa: E402
from vrtools.parse import parse_sarga, to_int  # noqa: E402

KANDA_OF = {name: k for k, name in KANDA_NAMES.items()}
DATA = ROOT / "data"
RB = ROOT / "sources" / "upstream" / "Ramayana_Book" / "san"
RB_FILES = {1: "balakanda_all.json", 2: "ayodhyakanda_all.json", 3: "aranyakanda_all.json",
            4: "kishkindhakanda_all.json", 5: "sundarakanda_all.json", 6: "yudhhakanda_all.json",
            7: "uttarakanda_all.json"}


def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n")


def ramayana_book_counts() -> dict[tuple[int, int], int]:
    out = {}
    for k, f in RB_FILES.items():
        if not (RB / f).exists():
            continue
        d = json.loads((RB / f).read_text())
        for ch in next(iter(d.values()))["chapters"]:
            out[(k, ch["chapter_number"])] = len(ch["slokas"])
    return out


def main() -> None:
    pages = {}
    for f in sorted(glob.glob(str(ROOT / "cache" / "wikisource" / "batch_*.json"))):
        for p in json.loads(Path(f).read_text())["query"]["pages"]:
            _, kname, sname = p["title"].split("/")
            rev = p["revisions"][0]
            pages[(KANDA_OF[kname], to_int(sname.split()[-1]))] = (
                rev["slots"]["main"]["content"],
                {"revid": rev["revid"], "timestamp": rev["timestamp"], "title": p["title"]})
    anomalies, hashes, index = [], {}, []
    counts = collections.defaultdict(lambda: {"sargas": 0, "verses": 0, "half": 0, "appendix_verses": 0,
                                              "metre": collections.Counter(), "metre_not_ok": 0,
                                              "presplit_verses": 0, "presplit_sargas": []})
    rb = ramayana_book_counts()
    for (k, s) in sorted(pages):
        text, rev = pages[(k, s)]
        parsed = parse_sarga(text, k, s)
        rec = make_sarga(parsed, k, s, rev)
        dump(DATA / "vr" / str(k) / f"{s:03d}.json", rec)
        anomalies += parsed["anomalies"]
        allv = rec["verses"] + (rec["appendix"]["verses"] if rec["appendix"] else [])
        for v in allv:
            hashes[v["id"]] = mula_hash(v["lines"])
        c = counts[k]
        c["sargas"] += 1
        c["verses"] += rec["verse_count"]
        c["appendix_verses"] += len(allv) - rec["verse_count"]
        c["half"] += sum(v["half"] for v in rec["verses"])
        for v in rec["verses"]:
            c["metre"][v["metre"]["name"] or "—"] += 1
            c["metre_not_ok"] += not v["metre"]["ok"]
            c["presplit_verses"] += "source_presplit" in v["review"]["flags"]
        if "source_presplit" in rec["flags"]:
            c["presplit_sargas"].append(s)
        if (k, s) in rb and rb[(k, s)] != rec["verse_count"]:
            anomalies.append({"kanda": k, "sarga": s, "type": "count_differs_from_ramayana_book",
                              "wikisource": rec["verse_count"], "ramayana_book": rb[(k, s)]})
        first = rec["verses"][0]["lines"][0] if rec["verses"] else ""
        index.append({"id": f"VR.{k}.{s}", "k": k, "s": s, "verses": rec["verse_count"],
                      "incipit": first.rstrip(" ।॥"), "title": rec["title"],
                      "metres": sorted({v["metre"]["name"] for v in rec["verses"]
                                        if v["metre"]["name"] not in (None, "अनुष्टुप्")}),
                      "flags": rec["flags"], "appendix": bool(rec["appendix"]), "status": rec["status"]})
    totals = {"sargas": sum(c["sargas"] for c in counts.values()),
              "verses": sum(c["verses"] for c in counts.values()),
              "appendix_verses": sum(c["appendix_verses"] for c in counts.values())}
    dump(DATA / "vr" / "index.json", {"kandas": [{"k": k, "name": KANDA_NAMES[k],
                                                  "sargas": counts[k]["sargas"], "verses": counts[k]["verses"]}
                                                 for k in sorted(counts)],
                                      "sargas": index})
    (DATA / "meta").mkdir(parents=True, exist_ok=True)
    (DATA / "meta" / "counts.json").write_text(json.dumps(
        {"per_kanda": {k: {**c, "metre": dict(c["metre"].most_common())} for k, c in sorted(counts.items())},
         "total": totals}, ensure_ascii=False, indent=1) + "\n")
    (DATA / "meta" / "anomalies.json").write_text(json.dumps(anomalies, ensure_ascii=False, indent=1) + "\n")
    (DATA / "meta" / "mula_hashes.json").write_text(json.dumps(hashes, ensure_ascii=False, indent=0) + "\n")
    print(json.dumps(totals), collections.Counter(a["type"] for a in anomalies))


if __name__ == "__main__":
    main()
