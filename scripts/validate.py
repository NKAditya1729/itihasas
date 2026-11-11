"""Read-only checks for `make check` (CLAUDE.md §7.1–7.3, 7.5). Exits non-zero on any error.

1 schema   every sarga file against schema/sarga.schema.json
2 mūla     sha256 of every verse's lines equals data/meta/mula_hashes.json
3 re-join  every stored padaccheda re-joins to its mūla; same line count
5 hygiene  NFC; padaccheda lines Devanagari only (schema pattern); mūla lines with
           characters outside Sanskrit Devanagari must carry the invalid_char flag
B status   padaccheda_status agrees with the presence of a split; a corrected verse has
           its approved correction record (CLAUDE.md §12)
B flags    every verse listed in data/meta/mula_flags.json carries its flag
B corr.    a corrected verse holds exactly an approved correction of data/meta/corrections.json,
           its source lines are untouched (check 2), and its metre is that of the corrected text
Checks 3 (re-join) reads the corrected text where one exists.
4 layers   a verse with padārtha passes vrtools.padartha.check_layers: one entry per pada whose
           analysis fits its form, qualifier agreement, anvaya and vyākhyā coverage (§7.4),
           no Latin letters (§7.5)
"""
from __future__ import annotations

import json
import sys
import unicodedata
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from vrtools.build import correction_errors, mula_hash, status_errors, text_lines  # noqa: E402
from vrtools.normalize import invalid_chars  # noqa: E402
from vrtools.padartha import check_layers  # noqa: E402
from vrtools.sandhi import check_rejoin  # noqa: E402


def main() -> int:
    schema = json.loads((ROOT / "schema" / "sarga.schema.json").read_text())
    validator = jsonschema.Draft202012Validator(schema)
    hashes = json.loads((ROOT / "data" / "meta" / "mula_hashes.json").read_text())
    wanted = {}
    for e in json.loads((ROOT / "data" / "meta" / "mula_flags.json").read_text()):
        wanted.setdefault(e["id"], []).append(e["flag"])
    approved = {e["id"]: e for e in json.loads((ROOT / "data" / "meta" / "corrections.json").read_text())}
    errors, n_verses, n_pada, n_layers, n_exceptions, seen = [], 0, 0, 0, 0, set()
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
            errors += status_errors(v) + correction_errors(v, approved)
            seen.add(v["id"])
            errors += [f"{v['id']}: flag {flag} from mula_flags.json is missing (run scripts/flag_mula.py)"
                       for flag in wanted.get(v["id"], []) if flag not in v["review"]["flags"]]
            if v["padartha"]:
                n_layers += 1
                errors += [f"{v['id']}: {e}" for e in check_layers(text_lines(v), v)["errors"]]
                if v.get("padaccheda_status") != "reviewed":
                    errors.append(f"{v['id']}: has padārtha but its padaccheda is not reviewed")
            if v["padaccheda_lines"]:
                n_pada += 1
                declared = v.get("padaccheda_status") == "reviewed" and (v.get("rejoin_note") or "").strip()
                n_exceptions += bool(declared)
                if not declared and not check_rejoin(text_lines(v), v["padaccheda_lines"])["ok"]:
                    errors.append(f"{v['id']}: stored padaccheda does not re-join")
    errors += [f"{vid}: listed in mula_flags.json but not in the data" for vid in sorted(set(wanted) - seen)]
    errors += [f"{vid}: listed in corrections.json but not in the data" for vid in sorted(set(approved) - seen)]
    print(f"checked {n_verses} verses, {n_pada} with padaccheda, {n_layers} with padārtha, "
          f"{n_exceptions} declared re-join exceptions; {len(errors)} errors")
    for e in errors[:50]:
        print("  ", e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
