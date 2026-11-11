"""Read-only checks for `make check` (CLAUDE.md §7.1–7.3, 7.5). Exits non-zero on any error.

1 schema   every sarga file against schema/sarga.schema.json
2 mūla     sha256 of every verse's lines equals data/meta/mula_hashes.json
3 re-join  every stored padaccheda re-joins to its mūla; same line count
5 hygiene  NFC; padaccheda lines Devanagari only (schema pattern); mūla lines with
           characters outside Sanskrit Devanagari must carry the invalid_char flag
"""
from __future__ import annotations

import json
import sys
import unicodedata
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from vrtools.build import mula_hash  # noqa: E402
from vrtools.normalize import invalid_chars  # noqa: E402
from vrtools.sandhi import check_rejoin  # noqa: E402


def main() -> int:
    schema = json.loads((ROOT / "schema" / "sarga.schema.json").read_text())
    validator = jsonschema.Draft202012Validator(schema)
    hashes = json.loads((ROOT / "data" / "meta" / "mula_hashes.json").read_text())
    errors, n_verses, n_pada = [], 0, 0
    for f in sorted((ROOT / "data" / "vr").glob("*/*.json")):
        d = json.loads(f.read_text())
        errors += [f"{f.name}: schema: {e.message[:120]}" for e in validator.iter_errors(d)][:3]
        for v in d["verses"] + (d["appendix"]["verses"] if d["appendix"] else []):
            n_verses += 1
            if mula_hash(v["lines"]) != hashes.get(v["id"]):
                errors.append(f"{v['id']}: mūla hash differs from ingest")
            if any(unicodedata.normalize("NFC", l) != l for l in v["lines"]):
                errors.append(f"{v['id']}: mūla not NFC")
            if any(invalid_chars(l) for l in v["lines"]) and "invalid_char" not in v["review"]["flags"]:
                errors.append(f"{v['id']}: unflagged non-Sanskrit characters in the mūla")
            if v["padaccheda_lines"]:
                n_pada += 1
                if not check_rejoin(v["lines"], v["padaccheda_lines"])["ok"]:
                    errors.append(f"{v['id']}: stored padaccheda does not re-join")
    print(f"checked {n_verses} verses, {n_pada} with padaccheda; {len(errors)} errors")
    for e in errors[:50]:
        print("  ", e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
