"""Merge a reviewed draft into its sarga file (Stage B, Step 4; CLAUDE.md §10.3).

Reads review/drafts/<sarga>.json (the generator's draft: {"gen", "verses", optionally
"title", "summary_sa", "pilot": true}) and review/drafts/<sarga>.review.json (the reviewer's verdicts:
{verse id: {"verdict": "pass" | "flag", "rules": […], "note": "…"}}). A verse is merged
only if it has a verdict and passes every automated check; its padaccheda becomes
``reviewed``. A verse with verdict "flag" is merged too and listed in review/queue.md
for the human reviewer. Nothing in ``lines`` is touched.

Usage: uv run python scripts/merge_layers.py review/drafts/VR.1.1.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from vrtools.padartha import merge_verse  # noqa: E402

from scripts.check_layers import sarga_file  # noqa: E402


def main() -> int:
    path = Path(sys.argv[1])
    draft = json.loads(path.read_text())
    verdicts = json.loads(path.with_suffix(".review.json").read_text())
    f = sarga_file(draft["verses"][0]["id"])
    d = json.loads(f.read_text())
    by_id = {v["id"]: v for v in d["verses"] + (d["appendix"]["verses"] if d["appendix"] else [])}
    merged, skipped, flagged = [], [], []
    for dv in draft["verses"]:
        verdict = (verdicts.get(dv["id"]) or {}).get("verdict")
        if verdict not in ("pass", "flag"):
            skipped.append(dv["id"])
            continue
        result = merge_verse(by_id[dv["id"]], dv, gen=draft["gen"], verdict=verdict)
        review = by_id[dv["id"]]["review"]
        review["agent_rules"] = verdicts[dv["id"]].get("rules", [])
        review["agent_note"] = verdicts[dv["id"]].get("note", "")
        merged.append(dv["id"])
        if verdict == "flag" or result["unverified"]:
            flagged.append((dv["id"], verdict, verdicts[dv["id"]].get("note", ""), result["unverified"]))
    for key in ("title", "summary_sa", "pilot"):
        if draft.get(key):
            d[key] = draft[key]
    done = [v for v in d["verses"] if v.get("padartha")]
    layer = "draft" if len(done) == len(d["verses"]) else "partial"
    d["status"].update({"padaccheda": "reviewed" if all(v.get("padaccheda_status") == "reviewed" for v in d["verses"]) else "partial",
                        "padartha": layer, "anvaya": layer, "vyakhya": layer})
    f.write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"merged {len(merged)} verse(s) into {f.relative_to(ROOT)}; no verdict yet: {len(skipped)}")
    for vid, verdict, note, unverified in flagged:
        print(f"  for the human reviewer: {vid} [{verdict}] {note}" + (f" (forms not in the word list: {' '.join(unverified)})" if unverified else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
