"""Phase 2a: compare each DCS seed with Dharmamitra's segmentation of the same verse.

Both word lists are reduced to pausal SLP1 members. If their concatenations
differ, the two sources restore different letters (e.g. ca eva vs ca iva), and
the verse is flagged ``seed_disagreement`` and goes to the fix queue; its DCS
padaccheda is kept (DCS has priority, CLAUDE.md §5.1). Differences only in where
compounds are cut (DCS keeps lexicalised compounds such as kṛtajña whole) are
counted as ``granularity_only``, spelling-only differences of a nasal as agreement, and
a Dharmamitra output that dropped text (< 80% of the letters) as
``dharmamitra_incomplete``; none of these is flagged.

Usage: uv run python scripts/crosscheck_seeds.py   (after seed_dharmamitra.py)
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scripts.seed_dharmamitra import BATCH, segment, verse_text, words_of  # noqa: E402
from vrtools.dcs import pausal_candidates  # noqa: E402
from vrtools.sandhi import fold, norm, pada_words  # noqa: E402


def members_from_padaccheda(lines: list[str]) -> list[str]:
    return [norm(w) for line in lines for w in pada_words(line)]


def members_from_dharmamitra(result: str) -> list[str]:
    return [norm(pausal_candidates(w)[0]) for w in words_of(result)]


INCOMPLETE = 0.8   # Dharmamitra output shorter than this share of the DCS letters: it dropped text


def classify(dcs: list[str], dm: list[str]) -> str:
    a, b = [fold(x) for x in dcs], [fold(x) for x in dm]
    if a == b:
        return "agree"
    if "".join(a) == "".join(b):
        return "granularity_only"
    if len("".join(b)) < INCOMPLETE * len("".join(a)):
        return "dharmamitra_incomplete"
    return "disagree"


def main() -> None:
    stats = collections.Counter()
    files = sorted((ROOT / "data" / "vr").glob("*/*.json"))
    docs = {f: json.loads(f.read_text()) for f in files}
    dcs_seeded = [v for d in docs.values() for v in d["verses"] + (d["appendix"]["verses"] if d["appendix"] else [])
                  if (v.get("seed") or {}).get("source") == "dcs"]
    for i in range(0, len(dcs_seeded), BATCH):        # batches cross sarga boundaries: fewer requests
        chunk = dcs_seeded[i:i + BATCH]
        for v, res in zip(chunk, segment([verse_text(v["lines"]) for v in chunk])):
            v["seed"]["dharmamitra"] = res
            a, b = members_from_padaccheda(v["padaccheda_lines"]), members_from_dharmamitra(res)
            kind = classify(a, b)
            stats[kind] += 1
            flags = v["review"]["flags"]
            if kind == "disagree":
                v["seed"]["disagreement"] = {"dcs": a, "dharmamitra": b}
                if "seed_disagreement" not in flags:
                    flags.append("seed_disagreement")
            else:
                v["seed"].pop("disagreement", None)
                if "seed_disagreement" in flags:
                    flags.remove("seed_disagreement")
    for f, d in docs.items():
        f.write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(dict(stats))
    (ROOT / "data" / "meta" / "crosscheck_seeds.json").write_text(json.dumps(dict(stats), indent=1) + "\n")


if __name__ == "__main__":
    main()
