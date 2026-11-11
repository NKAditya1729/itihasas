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
        "padaccheda_lines": None, "groups": None,
        "metre": {**identify(lines), "checked_by": "vidyut.chandas+vrtools.metre"},
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
