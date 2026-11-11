"""Encoding-level normalisation of mūla lines (CLAUDE.md §2).

Only typing conventions are changed, never letters: NFC; ASCII colon used as
visarga → ः; |, ||, ।। → ।, ॥; one space before a daṇḍa; whitespace runs → one
space; no space before avagraha; zero-width characters removed. Anusvāra and
homorganic nasals are left exactly as the source has them. Every change is
counted in the returned log.
"""
from __future__ import annotations

import re
import unicodedata

ZERO_WIDTH = re.compile("[​‌‍﻿­]")
COLON_VISARGA = re.compile(r"(?<=[ऀ-ॿ]):")
AVAGRAHA_SPACE = re.compile(r"(?<=[ऀ-ॿ])\s+ऽ")

_CONS = "कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह"
_VOICED = "गघजझडढदधबभयरलवहनमङञण"
_VOWELS = "अआइईउऊऋॠऌएऐओऔ"
# signs that sandhi has been undone inside a printed line:
#   -म् + consonant (saṃhitā writes anusvāra), -ः + vowel / voiced consonant / च
_PRESPLIT = (re.compile(rf"म्\s+[{_CONS}]"), re.compile(rf"ः\s+[{_VOWELS}{_VOICED}च]"))


def normalize_line(line: str) -> tuple[str, dict]:
    log: dict[str, int] = {}

    def sub(name: str, pattern: re.Pattern, repl: str, text: str) -> str:
        new, n = pattern.subn(repl, text)
        if n:
            log[name] = log.get(name, 0) + n
        return new

    s = unicodedata.normalize("NFC", line)
    s = sub("zero_width", ZERO_WIDTH, "", s)
    s = sub("colon_visarga", COLON_VISARGA, "ः", s)
    s = s.replace("।।", "॥").replace("||", "॥").replace("|", "।")
    s = sub("avagraha_space", AVAGRAHA_SPACE, "ऽ", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s*([।॥])", r" \1", s).strip()
    return s, log


# Sanskrit Devanagari: candrabindu/anusvāra/visarga, vowels (incl. ॠ ऌ ॡ), consonants,
# avagraha, Sanskrit vowel signs, virāma, ॐ, daṇḍas, digits; plus space and hyphen.
ALLOWED = re.compile(
    "[\u0901-\u0903\u0905-\u090C\u090F\u0910\u0913-\u0939\u093D-\u0944\u0947\u0948"
    "\u094B-\u094D\u0950\u0960-\u0963\u0964-\u096F \\-]")


def invalid_chars(line: str) -> list[str]:
    """Characters outside the Sanskrit Devanagari set (source typos, Latin, …)."""
    return sorted({ch for ch in line if not ALLOWED.match(ch)})


def is_presplit(lines: list[str]) -> bool:
    """True if a verse shows sandhi undone inside its printed lines."""
    return any(p.search(l) for l in lines for p in _PRESPLIT)
