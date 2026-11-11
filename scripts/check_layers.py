"""Check a draft of generated layers against the verse text (Stage B, Step 4d).

A draft is a JSON file {"verses": [{"id", "padaccheda_lines", "padartha", "anvaya",
"vyakhya_sa", "speaker", "context_note_sa"}, …]}. Each verse is checked with
vrtools.padartha.check_layers against the text the verse is read in (an approved
correction where one exists). Read-only: nothing is written.

Usage: uv run python scripts/check_layers.py review/drafts/VR.1.1.json [VR.1.1.3 …]
Exit status 1 if any verse has an error.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from vrtools.build import text_lines  # noqa: E402
from vrtools.padartha import check_layers  # noqa: E402


def sarga_file(vid: str) -> Path:
    _, k, s = vid.split(".")[:3]
    return ROOT / "data" / "vr" / k / f"{int(s.rstrip('A')):03d}.json"


def verse_texts(vid: str) -> dict[str, list[str]]:
    d = json.loads(sarga_file(vid).read_text())
    return {v["id"]: text_lines(v) for v in d["verses"] + (d["appendix"]["verses"] if d["appendix"] else [])}


def main() -> int:
    draft = json.loads(Path(sys.argv[1]).read_text())
    only = set(sys.argv[2:])
    texts, bad = {}, 0
    for v in draft["verses"]:
        if only and v["id"] not in only:
            continue
        if v["id"] not in texts:
            texts.update(verse_texts(v["id"]))
        r = check_layers(texts[v["id"]], v)
        bad += bool(r["errors"])
        print(f"{v['id']}: {'OK' if not r['errors'] else str(len(r['errors'])) + ' error(s)'}"
              + (f"  [not in the word list: {' '.join(r['unverified'])}]" if r["unverified"] else ""))
        for e in r["errors"]:
            print("   -", e)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
