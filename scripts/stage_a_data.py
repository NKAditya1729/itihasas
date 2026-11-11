"""Generate the data sections of docs/STAGE_A_REPORT.md (Gate A items 1–5) from data/.

Writes docs/stage_a_data.md. Random samples use a fixed seed so reruns are stable.
Usage: uv run python scripts/stage_a_data.py
"""
from __future__ import annotations

import collections
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / "data" / "meta"
DIG = str.maketrans("0123456789", "०१२३४५६७८९")


def load_verses():
    out = []
    for f in sorted((ROOT / "data" / "vr").glob("*/*.json")):
        d = json.loads(f.read_text())
        for v in d["verses"] + (d["appendix"]["verses"] if d["appendix"] else []):
            out.append((d, v))
    return out


def table(rows, head):
    s = "| " + " | ".join(head) + " |\n|" + "---|" * len(head) + "\n"
    return s + "".join("| " + " | ".join(str(c) for c in r) + " |\n" for r in rows)


def main() -> None:
    counts = json.loads((META / "counts.json").read_text())
    anomalies = json.loads((META / "anomalies.json").read_text())
    cw = json.loads((META / "crosswalk.json").read_text())
    rj = json.loads((META / "rejoin.json").read_text())
    verses = load_verses()
    names = {1: "बाल", 2: "अयोध्या", 3: "अरण्य", 4: "किष्किन्धा", 5: "सुन्दर", 6: "युद्ध", 7: "उत्तर"}
    md = []

    # 1. counts and anomalies
    md.append("## 1. Sargas and verses per kāṇḍa, anomalies\n")
    rows = []
    for k, c in counts["per_kanda"].items():
        rows.append([f"{k} {names[int(k)]}", c["sargas"], c["verses"], c["appendix_verses"], c["half"],
                     c["presplit_verses"], len(c["presplit_sargas"]), c["metre_not_ok"]])
    t = counts["total"]
    rows.append(["**total**", t["sargas"], t["verses"], t["appendix_verses"], sum(c["half"] for c in counts["per_kanda"].values()),
                 sum(c["presplit_verses"] for c in counts["per_kanda"].values()),
                 sum(len(c["presplit_sargas"]) for c in counts["per_kanda"].values()),
                 sum(c["metre_not_ok"] for c in counts["per_kanda"].values())])
    md.append(table(rows, ["kāṇḍa", "sargas", "verses", "prakṣipta appendix verses", "half verses",
                           "half-split verses (flagged)", "half-split sargas", "metre not ok"]))
    md.append("\nMetres found (verses):\n")
    metre = collections.Counter()
    for c in counts["per_kanda"].values():
        metre.update(c["metre"])
    md.append(", ".join(f"{k} {v}" for k, v in metre.most_common()) + "\n")
    presplit = {k: c["presplit_sargas"] for k, c in counts["per_kanda"].items() if c["presplit_sargas"]}
    md.append("\nSargas flagged `source_presplit` (≥30% of verses half-split in the Wikisource text): " +
              "; ".join(f"{k}: {', '.join(map(str, v))}" for k, v in presplit.items()) + "\n")
    inv = [v["id"] + " (" + " ".join(f"U+{ord(ch):04X}" for ch in v["invalid_chars"]) + ")" for _, v in verses if v.get("invalid_chars")]
    md.append(f"\nVerses with characters outside Sanskrit Devanagari (`invalid_char`, mūla left as is): {len(inv)} — " + ", ".join(inv) + "\n")
    md.append("\nEvery anomaly logged by the parser and ingest (`data/meta/anomalies.json`):\n")
    by = collections.defaultdict(list)
    for a in anomalies:
        by[a["type"]].append(a)
    for typ, items in sorted(by.items(), key=lambda x: -len(x[1])):
        md.append(f"\n**{typ}** ({len(items)})\n")
        for a in items:
            extra = {k: v for k, v in a.items() if k not in ("kanda", "sarga", "type", "printed")}
            md.append(f"- {a['kanda']}.{a['sarga']}: " + json.dumps(extra, ensure_ascii=False)[:220] + "\n")

    # 2. crosswalk
    md.append("\n## 2. Crosswalk to the Critical Edition\n")
    rows = [[f"{k} {names[int(k)]}", c.get("same", 0), c.get("partial", 0), c.get("variant", 0), c.get("absent", 0)]
            for k, c in cw["per_kanda"].items()]
    t = cw["total"]
    rows.append(["**total**", t.get("same", 0), t.get("partial", 0), t.get("variant", 0), t.get("absent", 0)])
    md.append(table(rows, ["kāṇḍa", "same (exactly or ≤ a few letters)", "partly (a half-verse shared)",
                           "variant (similar, no half shared)", "not at all"]))
    md.append(f"\nVulgate sargas with no CE counterpart ({len(cw['sargas_unmapped'])}): {', '.join(cw['sargas_unmapped'])}\n")

    # 3. seeding
    md.append("\n## 3. Padaccheda seeding and re-join pass rate\n")
    src = collections.Counter((v.get("seed") or {}).get("source") or "none" for _, v in verses)
    tried_dcs = sum(1 for _, v in verses if (v.get("seed") or {}).get("dcs_tried") or (v.get("seed") or {}).get("source") == "dcs")
    tried_dm = sum(1 for _, v in verses if (v.get("seed") or {}).get("source") != "dcs" and "dharmamitra" in (v.get("seed") or {}))
    rows = [["DCS (via crosswalk; tried on every verse with a CE link)", tried_dcs, src["dcs"], f"{100 * src['dcs'] / tried_dcs:.1f}%"],
            ["Dharmamitra (tried on every verse DCS did not seed)", tried_dm, src["dharmamitra"], f"{100 * src['dharmamitra'] / tried_dm:.1f}%"]]
    md.append(table(rows, ["seed source", "verses tried", "accepted (re-join passes)", "re-join pass rate"]))
    by_src = rj["by_source"]
    md.append(f"\nIndependent re-check of the stored padaccheda text (`scripts/check_rejoin.py`): DCS {by_src.get('dcs', {}).get('pass', 0)} pass / "
              f"{by_src.get('dcs', {}).get('fail', 0)} fail; Dharmamitra {by_src.get('dharmamitra', {}).get('pass', 0)} pass / "
              f"{by_src.get('dharmamitra', {}).get('fail', 0)} fail. Unseeded: {src['none']} verses. "
              f"Overall coverage: {src['dcs'] + src['dharmamitra']} of {len(verses)} verses ({100 * (src['dcs'] + src['dharmamitra']) / len(verses):.1f}%).\n")
    cc = META / "crosscheck_seeds.json"
    if cc.exists():
        c = json.loads(cc.read_text())
        md.append(f"\nDCS vs Dharmamitra on the DCS-seeded verses: agree {c.get('agree', 0)}, "
                  f"disagree in restored letters {c.get('disagree', 0)} (queued), "
                  f"compound granularity only {c.get('granularity_only', 0)}, "
                  f"Dharmamitra output incomplete {c.get('dharmamitra_incomplete', 0)} (neither queued).\n")
    md.append(f"\nFix queue `queue/padaccheda_fix.jsonl`: {rj['queued']} verses — " +
              ", ".join(f"{k} {v}" for k, v in rj["queue_reasons"].items()) + "\n")

    # 5. samples
    rnd = random.Random(20261111)
    seeded = [(d, v) for d, v in verses if v["padaccheda_lines"]]
    md.append("\n## 5a. 30 random seeded verses (mūla | padaccheda)\n")
    for d, v in rnd.sample(seeded, 30):
        md.append(f"\n**{v['id']}** · seed {v['seed']['source']}" +
                  (" · compound boundaries unknown" if "compound_boundaries_unknown" in v["review"]["flags"] else "") + "\n\n")
        md.append(table([[m, p] for m, p in zip(v["lines"], v["padaccheda_lines"])], ["mūla", "padaccheda"]))
    queue = [json.loads(l) for l in (ROOT / "queue" / "padaccheda_fix.jsonl").read_text().splitlines()]
    md.append("\n## 5b. 30 verses from the failure queue\n")
    for q in rnd.sample(queue, min(30, len(queue))):
        f = q.get("failure") or q.get("dcs_failure") or q.get("dharmamitra_failure") or {}
        md.append(f"\n**{q['id']}** · {q['reason']}" + (f" · flags: {', '.join(q['flags'])}" if q["flags"] else "") + "\n\n")
        md.append("mūla: " + " / ".join(q["lines"]) + "\n\n")
        if q["candidates"].get("dcs"):
            dc = q["candidates"]["dcs"]
            md.append("DCS candidate: " + (" / ".join(dc) if isinstance(dc, list) else dc) + "\n\n")
        if q["candidates"].get("dharmamitra"):
            md.append("Dharmamitra: " + q["candidates"]["dharmamitra"].replace("_", " ").strip() + "\n\n")
        if f:
            md.append(f"first mismatch (normalised SLP1, pos {f.get('pos')}): expected `{f.get('expected')}`, joined `{f.get('got')}`\n")
    (ROOT / "docs" / "stage_a_data.md").write_text("".join(md))
    print("wrote docs/stage_a_data.md", len("".join(md)), "chars")


if __name__ == "__main__":
    main()
