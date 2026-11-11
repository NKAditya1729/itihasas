"""Turn a parsed Wikisource page into the per-sarga record of CLAUDE.md §4."""
from __future__ import annotations

import hashlib

from .metre import identify
from .normalize import invalid_chars, is_presplit, normalize_line

KANDA_NAMES = {1: "बालकाण्डम्", 2: "अयोध्याकाण्डम्", 3: "अरण्यकाण्डम्", 4: "किष्किन्धाकाण्डम्",
               5: "सुन्दरकाण्डम्", 6: "युद्धकाण्डम्", 7: "उत्तरकाण्डम्"}
PRESPLIT_SARGA_SHARE = 0.3


def mula_hash(lines: list[str]) -> str:
    return hashlib.sha256("\n".join(lines).encode()).hexdigest()


CHECKED_BY = "vidyut.chandas+vrtools.metre"
CORRECTION_KEYS = ("what", "evidence", "approved_by", "date")


def text_lines(v: dict) -> list[str]:
    """The text every later layer is written for and checked against: the approved
    correction where one exists (CLAUDE.md §12), otherwise the Wikisource text."""
    return v.get("lines_corrected") or v["lines"]


def apply_correction(v: dict, entry: dict) -> None:
    """Store an approved correction beside the untouched ``lines`` and recompute the metre
    for the corrected text (the result for the source text is kept in ``metre_source``)."""
    new, record = entry["lines_corrected"], entry["correction"]
    if len(new) != len(v["lines"]):
        raise ValueError(f"{v['id']}: the line count of the correction differs from the source")
    if new == v["lines"]:
        raise ValueError(f"{v['id']}: the correction is the same as the source text")
    if not all(record.get(k) for k in CORRECTION_KEYS):
        raise ValueError(f"{v['id']}: the correction record needs what, evidence, approved_by and date")
    if "metre_source" not in v:
        v["metre_source"] = {**{k: x for k, x in v["metre"].items() if k != "of"}, "of": "lines"}
    v["lines_corrected"], v["correction"] = list(new), {k: record[k] for k in CORRECTION_KEYS}
    v["metre"] = {**identify(v["lines_corrected"]), "checked_by": CHECKED_BY, "of": "lines_corrected"}


def correction_errors(v: dict, approved: dict[str, dict]) -> list[str]:
    """A correction in the data must be exactly an approved one, and every approved one
    must be in the data (``approved``: id → entry of data/meta/corrections.json)."""
    entry, vid = approved.get(v["id"]), v["id"]
    if "lines_corrected" not in v:
        return [f"{vid}: approved correction not applied (run scripts/apply_corrections.py)"] if entry else []
    if not entry:
        return [f"{vid}: lines_corrected is not in data/meta/corrections.json"]
    if v["lines_corrected"] != entry["lines_corrected"] or v.get("correction") != entry["correction"]:
        return [f"{vid}: lines_corrected differs from the approved correction"]
    metre = identify(v["lines_corrected"])
    if any(v["metre"].get(k) != x for k, x in metre.items()):
        return [f"{vid}: the metre was not recomputed for the corrected text"]
    return []


def padaccheda_status(v: dict) -> str | None:
    """None without a split; "reviewed" once a split has been finalised in a sarga review
    (never downgraded); otherwise "seed" (a machine split, shown as असमीक्षितम्)."""
    if not v.get("padaccheda_lines"):
        return None
    return "reviewed" if v.get("padaccheda_status") == "reviewed" else "seed"


def status_errors(v: dict) -> list[str]:
    """Consistency of the Stage B fields of one verse (for scripts/validate.py)."""
    errors, status = [], v.get("padaccheda_status")
    if v.get("padaccheda_lines") and not status:
        errors.append(f"{v['id']}: padaccheda without padaccheda_status")
    if status and not v.get("padaccheda_lines"):
        errors.append(f"{v['id']}: padaccheda_status is {status} but there is no padaccheda")
    if "lines_corrected" in v and not (v.get("correction") or {}).get("approved_by"):
        errors.append(f"{v['id']}: lines_corrected without an approved correction record")
    return errors


def add_flag(v: dict, flag: str, note: str = "") -> None:
    """Add a review flag (once) and its note to review.notes (once)."""
    review = v["review"]
    if flag not in review["flags"]:
        review["flags"].append(flag)
    entry = f"{flag}: {note}" if note else ""
    notes = review.get("notes") or ""
    if entry and entry not in notes:
        notes = f"{notes} | {entry}" if notes else entry
    review["notes"] = notes


def set_flag_note(v: dict, flag: str, note: str) -> None:
    """Like add_flag, but the note replaces any earlier note of the same flag."""
    review = v["review"]
    kept = [n for n in (review.get("notes") or "").split(" | ") if n and not n.startswith(flag + ": ")]
    review["notes"] = " | ".join(kept)
    add_flag(v, flag, note)


def has_reviewed_work(sarga: dict) -> bool:
    """True if a sarga file holds anything a re-ingest must not throw away: a reviewed
    padaccheda, a generated layer, or an approved correction."""
    verses = sarga["verses"] + (sarga["appendix"]["verses"] if sarga.get("appendix") else [])
    return any(v.get("padaccheda_status") == "reviewed" or v.get("padartha") or v.get("anvaya")
               or v.get("vyakhya_sa") or "lines_corrected" in v for v in verses)


def make_verse(p: dict, vid: str) -> dict:
    lines, norm = [], {}
    for raw in p["lines"]:
        line, log = normalize_line(raw)
        lines.append(line)
        for k, n in log.items():
            norm[k] = norm.get(k, 0) + n
    flags = list(p["flags"]) + (["source_presplit"] if is_presplit(lines) else [])
    bad = sorted({ch for line in lines for ch in invalid_chars(line)})
    if bad:
        flags.append("invalid_char")
    return {
        "id": vid, "n": p["n"], "src_ref": p["src_ref"], "half": p["half"],
        "lines": lines, "norm": norm, **({"invalid_chars": bad} if bad else {}),
        "padaccheda_lines": None, "groups": None, "padaccheda_status": None,
        "metre": {**identify(lines), "checked_by": CHECKED_BY},
        "speaker": None, "context_note_sa": None, "crosswalk": None,
        "padartha": [], "anvaya": None, "vyakhya_sa": None, "vyakhya_used_padas": [],
        "en_simple": None, "en_mixed": None,
        "review": {"auto_checks": {}, "agent_review": None, "human": "pending", "flags": flags, "notes": ""},
        "gen": {"model": "", "date": "", "prompt_version": ""},
    }


def _verses(parsed: dict, prefix: str) -> list[dict]:
    return [make_verse(p, f"{prefix}.{p['n']}{p['suffix']}") for p in parsed["verses"]]


def make_sarga(parsed: dict, kanda: int, sarga: int, rev: dict) -> dict:
    verses = _verses(parsed, f"VR.{kanda}.{sarga}")
    presplit = sum("source_presplit" in v["review"]["flags"] for v in verses)
    flags = ["source_presplit"] if verses and presplit / len(verses) >= PRESPLIT_SARGA_SHARE else []
    appendix = None
    if parsed.get("appendix"):
        a = parsed["appendix"]
        appendix = {"heading": a["heading"], "colophon": a["colophon"],
                    "verses": _verses(a, f"VR.{kanda}.{sarga}A")}
    return {
        "schema_version": 1, "work": "VR",
        "kanda": kanda, "kanda_name": KANDA_NAMES[kanda], "sarga": sarga,
        "title": None, "source_heading": parsed["source_heading"], "colophon": parsed["colophon"],
        "summary_sa": None, "context_in_sa": None,
        "verse_count": len(verses),
        "provenance": {"text": f"sa.wikisource rev {rev['revid']} ({rev['timestamp']})",
                       "page": rev["title"], "padaccheda_seed": None},
        "flags": flags,
        "verses": verses,
        "appendix": appendix,
        "status": {"mula": "done", "padaccheda": "pending", "padartha": "pending", "anvaya": "pending",
                   "vyakhya": "pending", "human_review": "pending"},
    }
