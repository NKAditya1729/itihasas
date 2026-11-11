"""Print verses of one sarga as plain text (read-only helper for generators and reviewers).

For each verse: its id, the text it is read in (an approved correction where one exists),
its metre if not anuṣṭubh, and the padaccheda now stored with its status (a "seed" is an
unreviewed machine hint).

Usage: uv run python scripts/show_verses.py VR.1.1 [first] [last]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from vrtools.build import text_lines  # noqa: E402


def main() -> None:
    _, k, s = sys.argv[1].split(".")
    first = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    last = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 6
    d = json.loads((ROOT / "data" / "vr" / k / f"{int(s):03d}.json").read_text())
    for i, v in enumerate(d["verses"], 1):
        if not first <= i <= last:
            continue
        metre = "" if v["metre"]["name"] == "अनुष्टुप्" else f"  [metre: {v['metre']['name']}]"
        print(f"{v['id']}{metre}")
        for line in text_lines(v):
            print("   ", line)
        if v.get("padaccheda_lines"):
            print(f"    padaccheda ({v.get('padaccheda_status')}):", " / ".join(v["padaccheda_lines"]))
        else:
            print("    padaccheda: none")


if __name__ == "__main__":
    main()
