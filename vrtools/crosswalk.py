"""Verse crosswalk: vulgate (Wikisource) ↔ Baroda Critical Edition (GRETIL, via hms-cap).

Used internally only, to pick the DCS analysis for a vulgate verse; no CE text
is published. Both texts are compared in normalised SLP1 (``sandhi.norm``).

relation:
  same     whole verse similarity ≥ SAME (variant readings of a few letters allowed)
  partial  at least one half-verse matches a CE half-verse ≥ HALF
  variant  whole-verse similarity ≥ VARIANT
  absent   no counterpart in the candidate CE sargas
"""
from __future__ import annotations

import re
from difflib import SequenceMatcher

from vidyut.lipi import Scheme, transliterate

from .sandhi import fold as norm, to_slp1

SAME, HALF, VARIANT = 0.85, 0.85, 0.6
MIN_HALF = 10   # a half-verse shorter than this (normalised letters) cannot make a link


def ce_key(ce: dict) -> str:
    return f"{ce['k']}.{ce['s']}.{ce['v']}"


def _ce_text(ce: dict) -> tuple[str, list[str]]:
    halves = [norm(transliterate(" ".join(line), Scheme.Iast, Scheme.Slp1)) for line in ce["lines"]]
    return "".join(halves), halves


def _vu_text(lines: list[str]) -> tuple[str, list[str]]:
    halves = [norm(to_slp1(h)) for h in re.split(r"[।॥]", " ".join(lines)) if norm(to_slp1(h))]
    return "".join(halves), halves


def _ratio(a: str, b: str) -> float:
    sm = SequenceMatcher(None, a, b, autojunk=False)
    return sm.ratio() if sm.real_quick_ratio() >= VARIANT and sm.quick_ratio() >= VARIANT else 0.0


def align_sarga(vu_verses: list[dict], ce_verses: list[dict]) -> dict[str, dict]:
    ce = [(ce_key(c), *_ce_text(c)) for c in ce_verses]
    out = {}
    for v in vu_verses:
        whole, halves = _vu_text(v["lines"])
        best_key, best = None, 0.0
        for key, text, _ in ce:
            r = _ratio(whole, text)
            if r > best:
                best_key, best = key, r
        if best >= SAME:
            out[v["id"]] = {"ce": best_key, "relation": "same", "score": round(best, 3)}
            continue
        half_key, half_best = None, 0.0
        for h in (h for h in halves if len(h) >= MIN_HALF):
            for key, _, ce_halves in ce:
                for ch in ce_halves:
                    r = _ratio(h, ch)
                    if r > half_best:
                        half_key, half_best = key, r
        if half_best >= HALF:
            out[v["id"]] = {"ce": half_key, "relation": "partial", "score": round(half_best, 3)}
        elif best >= VARIANT:
            out[v["id"]] = {"ce": best_key, "relation": "variant", "score": round(best, 3)}
        else:
            out[v["id"]] = {"ce": None, "relation": "absent", "score": round(best, 3)}
    return out


KEY_LEN, MIN_HITS, MIN_SHARE = 10, 2, 0.15


def _keys(half: str) -> set[str]:
    return {half[:KEY_LEN], half[-KEY_LEN:]}


def map_sargas(vu_sargas: dict[tuple[int, int], list[dict]],
               ce_by_sarga: dict[tuple[int, int], list[dict]]) -> dict[tuple[int, int], list[tuple[int, int]]]:
    """For each vulgate sarga, the CE sargas of the same kāṇḍa that share half-verses with it.

    A half-verse is matched by its first or last KEY_LEN normalised characters, so a variant
    in the middle of a line still counts. A CE sarga is linked if it has at least MIN_HITS
    hits and at least MIN_SHARE of the vulgate sarga's half-verses.
    """
    index: dict[str, set[tuple[int, int]]] = {}
    for key, verses in ce_by_sarga.items():
        for c in verses:
            for h in _ce_text(c)[1]:
                for k in _keys(h):
                    index.setdefault(f"{key[0]}|{k}", set()).add(key)
    out = {}
    for (k, s), verses in vu_sargas.items():
        hits: dict[tuple[int, int], int] = {}
        n = 0
        for v in verses:
            for h in _vu_text(v["lines"])[1]:
                if len(h) < MIN_HALF:
                    continue
                n += 1
                found = set().union(*(index.get(f"{k}|{key}", set()) for key in _keys(h)))
                for ce in found:
                    hits[ce] = hits.get(ce, 0) + 1
        out[(k, s)] = sorted(ce for ce, c in hits.items() if c >= max(MIN_HITS, MIN_SHARE * n))
    return out
