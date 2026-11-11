"""Phase 2a: seed padaccheda from DCS for verses linked to a CE verse.

The DCS words of the linked CE verse and of its neighbours are searched for a
contiguous run that re-joins to the verse (DCS blocks and vulgate verses are
often cut at different places).
A seed is kept only if the re-join check passes. Idempotent: verses already
seeded (with an unchanged mūla hash) are skipped. A verse whose padaccheda is
``reviewed`` is never touched. If a DCS split fails only because of the avagraha
(it would pass the loose check), it is recorded in seed.dcs_avagraha_mismatch.

Usage: uv run python scripts/seed_dcs.py
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from vrtools.build import mula_hash, text_lines  # noqa: E402
from vrtools.dcs import parse_dcs, pausal_candidates  # noqa: E402
from vrtools.sandhi import CHECKER_VERSION, to_deva  # noqa: E402
from vrtools.seed import seed_window  # noqa: E402

DCS = ROOT / "sources" / "upstream" / "ambuda-dcs" / "ramayanam.txt"


def neighbours(ce: str) -> list[list[str]]:
    """DCS verse blocks are not cut where the CE verses are (DCS R.1.1.4 holds only the
    second half of CE 1.1.4), so runs of neighbouring blocks are searched."""
    k, s, v = ce.split(".")
    key = lambda d: f"{k}.{s}.{int(v) + d}"
    return [[key(0)], [key(-1), key(0)], [key(0), key(1)], [key(-1), key(0), key(1)],
            [key(-2), key(-1), key(0)], [key(0), key(1), key(2)]]


def main() -> None:
    dcs = parse_dcs(DCS.read_text())
    hashes = json.loads((ROOT / "data" / "meta" / "mula_hashes.json").read_text())
    stats = collections.Counter()
    for f in sorted((ROOT / "data" / "vr").glob("*/*.json")):
        d = json.loads(f.read_text())
        changed = False
        for v in d["verses"] + (d["appendix"]["verses"] if d["appendix"] else []):
            seed = v.get("seed") or {}
            if v.get("padaccheda_status") == "reviewed":
                stats["reviewed_kept"] += 1
                continue
            lines = text_lines(v)                           # an approved correction, else the source text
            text_hash = mula_hash(lines)
            if (seed.get("source") == "dcs" and seed.get("mula_hash") == text_hash
                    and seed.get("checker") == CHECKER_VERSION):
                stats["already"] += 1
                continue
            cw = v["crosswalk"]
            if cw["relation"] == "absent" or not cw["ce"]:
                stats["no_ce"] += 1
                continue
            windows = neighbours(cw["ce"])
            result, best = None, None
            for keys in windows:
                words = [w for key in keys for w in dcs.get(key, [])]
                if not words:
                    continue
                r = seed_window(lines, words)
                if r["ok"]:
                    result = (keys, r)
                    break
                f0 = (r.get("failures") or [{}])[0]
                if best is None or f0.get("pos", -1) > best[1].get("pos", -1):
                    best = (keys, f0, " ".join(to_deva(pausal_candidates(w)[0]) for w in words))
            if result is None:
                stats[f"fail_{cw['relation']}"] += 1
                if seed.get("source") == "dcs":             # an older DCS seed no longer passes
                    v["padaccheda_lines"], v["groups"] = None, None
                v["seed"] = {**{k: x for k, x in seed.items() if k == "dharmamitra"},
                             "source": None if seed.get("source") in (None, "dcs") else seed["source"],
                             "dcs_tried": True}
                if best:
                    v["seed"].update({"dcs_verses": best[0], "dcs_failure": best[1], "dcs_candidate": best[2]})
                for keys in windows:                         # would it pass with the avagraha ignored?
                    words = [w for key in keys for w in dcs.get(key, [])]
                    loose = seed_window(lines, words, avagraha=False) if words else {"ok": False}
                    if loose["ok"]:
                        v["seed"]["dcs_avagraha_mismatch"] = loose["padaccheda_lines"]
                        stats["avagraha_mismatch"] += 1
                        break
                changed = True
                continue
            keys, r = result
            v["padaccheda_lines"], v["groups"] = r["padaccheda_lines"], r["groups"]
            v["seed"] = {**{k: x for k, x in seed.items() if k == "dharmamitra"},
                         "source": "dcs", "dcs_verses": keys, "mula_hash": text_hash, "checker": CHECKER_VERSION}
            if "compound_boundaries_unknown" in v["review"]["flags"]:
                v["review"]["flags"].remove("compound_boundaries_unknown")
            stats[f"ok_{cw['relation']}"] += 1
            changed = True
        if changed:
            f.write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(dict(stats))
    (ROOT / "data" / "meta" / "seed_dcs.json").write_text(json.dumps(dict(stats), indent=1) + "\n")


if __name__ == "__main__":
    main()
