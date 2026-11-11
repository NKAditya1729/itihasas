"""Apply the approved mūla corrections of data/meta/corrections.json (CLAUDE.md §12).

Each entry is {"id", "lines_corrected", "correction": {what, evidence, approved_by, date}}.
The verse's ``lines`` (the Wikisource text) are never changed: the corrected text goes to
``lines_corrected``, the record to ``correction``, and the metre is recomputed for the
corrected text. A machine seed made for the old text is dropped so that the seeding
scripts redo it; a ``reviewed`` padaccheda is kept (its reviewer must look at it again,
and `make check` will say so if it no longer re-joins).

No entry may be added to corrections.json without the user's approval, verse by verse.
Idempotent. Run before the seeding scripts.

Usage: uv run python scripts/apply_corrections.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from vrtools.build import apply_correction  # noqa: E402


def main() -> None:
    entries = {e["id"]: e for e in json.loads((ROOT / "data" / "meta" / "corrections.json").read_text())}
    done = []
    for f in sorted((ROOT / "data" / "vr").glob("*/[0-9]*.json")):
        d = json.loads(f.read_text())
        before = json.dumps(d, ensure_ascii=False)
        for v in d["verses"] + (d["appendix"]["verses"] if d["appendix"] else []):
            e = entries.get(v["id"])
            if not e:
                continue
            changed = v.get("lines_corrected") != e["lines_corrected"]
            apply_correction(v, e)
            if changed and v.get("padaccheda_status") != "reviewed":
                v["padaccheda_lines"], v["groups"], v["padaccheda_status"] = None, None, None
                v["seed"] = {**(v.get("seed") or {}), "source": None}
            done.append(v["id"])
        if json.dumps(d, ensure_ascii=False) != before:
            f.write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")) + "\n")
    missing = sorted(set(entries) - set(done))
    if missing:
        raise SystemExit(f"corrections for unknown verses: {missing}")
    print(f"{len(done)} corrections in place: {', '.join(done)}")


if __name__ == "__main__":
    main()
