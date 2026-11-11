"""Phase 2a: run the re-join check (CLAUDE.md §7.3) on every verse and build the fix queue.

* A verse with padaccheda_lines is re-checked from the stored text alone
  (independent of how the seed was found); the result goes to
  review.auto_checks.rejoin. A failure clears the padaccheda and queues the verse.
* A verse with no accepted seed, or whose DCS and Dharmamitra splits disagree,
  is queued with every candidate and the failure position.
* The mūla hash is compared with data/meta/mula_hashes.json (§7.2).

Writes queue/padaccheda_fix.jsonl (one JSON object per line) and
data/meta/rejoin.json. Nothing in the queue is resolved here (Stage A).

Usage: uv run python scripts/check_rejoin.py
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from vrtools.build import mula_hash  # noqa: E402
from vrtools.sandhi import check_rejoin  # noqa: E402

INSTRUCTION = "Do not change the mūla. Give a padaccheda (CLAUDE.md §5.1) that re-joins to it."


def main() -> None:
    hashes = json.loads((ROOT / "data" / "meta" / "mula_hashes.json").read_text())
    queue, stats = [], collections.defaultdict(collections.Counter)
    for f in sorted((ROOT / "data" / "vr").glob("*/*.json")):
        d = json.loads(f.read_text())
        for v in d["verses"] + (d["appendix"]["verses"] if d["appendix"] else []):
            seed = v.get("seed") or {}
            src = seed.get("source") or "none"
            if mula_hash(v["lines"]) != hashes[v["id"]]:
                raise SystemExit(f"mūla changed after ingest: {v['id']}")
            entry = None
            if v["padaccheda_lines"]:
                r = check_rejoin(v["lines"], v["padaccheda_lines"])
                v["review"]["auto_checks"]["rejoin"] = r["ok"]
                stats[src]["pass" if r["ok"] else "fail"] += 1
                if not r["ok"]:
                    entry = {"reason": "stored_padaccheda_fails", "failure": r["failures"][0],
                             "rejected": v["padaccheda_lines"]}
                    v["padaccheda_lines"], v["groups"] = None, None
                    seed["source"] = None
                elif "seed_disagreement" in v["review"]["flags"]:
                    entry = {"reason": "seed_disagreement", **seed.get("disagreement", {})}
            else:
                v["review"]["auto_checks"]["rejoin"] = False
                stats["unseeded"]["fail"] += 1
                entry = {"reason": "no_seed_rejoins",
                         "dcs_failure": seed.get("dcs_failure"), "dharmamitra_failure": seed.get("dharmamitra_failure")}
            if entry:
                queue.append({"id": v["id"], "lines": v["lines"], "flags": v["review"]["flags"],
                              "candidates": {"dcs": seed.get("dcs_candidate") or (v["padaccheda_lines"] if src == "dcs" else None),
                                             "dcs_verses": seed.get("dcs_verses"),
                                             "dharmamitra": seed.get("dharmamitra")},
                              **entry, "instruction": INSTRUCTION})
            v["seed"] = seed
        d["status"]["padaccheda"] = "seeded" if all(v["padaccheda_lines"] for v in d["verses"]) else "partial"
        f.write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")) + "\n")
    (ROOT / "queue").mkdir(exist_ok=True)
    with open(ROOT / "queue" / "padaccheda_fix.jsonl", "w") as out:
        for q in queue:
            out.write(json.dumps(q, ensure_ascii=False) + "\n")
    summary = {"by_source": {k: dict(c) for k, c in stats.items()}, "queued": len(queue),
               "queue_reasons": dict(collections.Counter(q["reason"] for q in queue))}
    (ROOT / "data" / "meta" / "rejoin.json").write_text(json.dumps(summary, indent=1) + "\n")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
