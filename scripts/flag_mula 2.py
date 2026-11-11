"""Stage B: apply the hand-kept mūla flags of data/meta/mula_flags.json (CLAUDE.md §12).

Each entry is {"id", "flag", "note"}; the flag is added to the verse's review.flags and
the note to review.notes. Nothing else is changed: the mūla text stays as ingested.
Idempotent; run after scripts/ingest_vulgate.py (which rebuilds the verses) and before
`make check`.

Usage: uv run python scripts/flag_mula.py
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from vrtools.build import add_flag  # noqa: E402


def main() -> None:
    entries = collections.defaultdict(list)
    for e in json.loads((ROOT / "data" / "meta" / "mula_flags.json").read_text()):
        entries[e["id"]].append(e)
    stats = collections.Counter()
    for f in sorted((ROOT / "data" / "vr").glob("*/*.json")):
        d = json.loads(f.read_text())
        before = json.dumps(d, ensure_ascii=False)
        for v in d["verses"] + (d["appendix"]["verses"] if d["appendix"] else []):
            for e in entries.get(v["id"], []):
                add_flag(v, e["flag"], e["note"])
                stats[e["flag"]] += 1
        if json.dumps(d, ensure_ascii=False) != before:
            f.write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(dict(stats))


if __name__ == "__main__":
    main()
