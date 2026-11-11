"""Phase 2a: crosswalk every vulgate verse to the Critical Edition.

Candidate CE verses for a vulgate sarga are those of the CE sarga(s) that share
half-verses with it (``map_sargas``). hms-cap's own sarga map is not used: it
was computed for the Ramayana_Book copy, whose sarga boundaries differ from
Wikisource's in parts of Ayodhyā and Yuddha. Writes verse["crosswalk"] in data/vr/ and a summary in
data/meta/crosswalk.json.

Usage: uv run python scripts/crosswalk.py
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from vrtools.crosswalk import align_sarga, map_sargas  # noqa: E402

HMS = ROOT / "sources" / "upstream" / "hms-cap-Ramayana" / "data"


def main() -> None:
    ce_by_sarga = collections.defaultdict(list)
    for line in (HMS / "normalized" / "ce.jsonl").read_text().splitlines():
        c = json.loads(line)
        ce_by_sarga[(c["k"], c["s"])].append(c)
    files = sorted((ROOT / "data" / "vr").glob("*/*.json"))
    sargas = {}
    for f in files:
        d = json.loads(f.read_text())
        sargas[(d["kanda"], d["sarga"])] = d["verses"] + (d["appendix"]["verses"] if d["appendix"] else [])
    vu_to_ce = map_sargas(sargas, ce_by_sarga)
    stats = collections.defaultdict(collections.Counter)
    for f in files:
        d = json.loads(f.read_text())
        cands = [c for key in vu_to_ce[(d["kanda"], d["sarga"])] for c in ce_by_sarga[key]]
        verses = d["verses"] + (d["appendix"]["verses"] if d["appendix"] else [])
        links = align_sarga(verses, cands) if cands else {}
        for v in verses:
            v["crosswalk"] = links.get(v["id"], {"ce": None, "relation": "absent", "score": 0.0})
            stats[d["kanda"]][v["crosswalk"]["relation"]] += 1
        f.write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")) + "\n")
    total = sum(stats.values(), collections.Counter())
    unmapped = [f"{k}.{s}" for (k, s), v in sorted(vu_to_ce.items()) if not v]
    out = {"sargas_unmapped": unmapped, "sarga_map": {f"{k}.{s}": [f"{a}.{b}" for a, b in v] for (k, s), v in sorted(vu_to_ce.items())},
           "per_kanda": {k: dict(c) for k, c in sorted(stats.items())}, "total": dict(total),
           "thresholds": {"same": 0.85, "partial_half": 0.85, "variant": 0.6}}
    (ROOT / "data" / "meta" / "crosswalk.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out))


if __name__ == "__main__":
    main()
