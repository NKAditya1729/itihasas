"""Seed padaccheda for one verse from a word list (DCS or Dharmamitra) and build
the word-aligned groups that the Padaccheda toggle shows.

A seed is accepted only if the re-join check reproduces the mūla.
"""
from __future__ import annotations

import re

from .dcs import pausal_candidates
from .sandhi import VOWELS, _end_danda, mula_norm, non_pausal, norm, rejoin, to_deva, to_slp1, units

_STOP_NASAL = {"k": "N", "K": "N", "g": "N", "G": "N", "c": "Y", "C": "Y", "j": "Y", "J": "Y",
               "w": "R", "W": "R", "q": "R", "Q": "R", "t": "n", "T": "n", "d": "n", "D": "n",
               "p": "m", "P": "m", "b": "m", "B": "m"}


def _mula_spelling(word: str, mula_raw: str) -> str:
    """Write a word-internal anusvāra/nasal before a stop the way the mūla writes it."""
    if not re.search(r"[MNYRnm](?=[kKgGcCjJwWqQtTdDpPbB])", word[:-1]):
        return word
    nasal = re.sub(r"M(?=([kKgGcCjJwWqQtTdDpPbB]))", lambda m: _STOP_NASAL[m.group(1)], word)
    anus = re.sub(r"[NYRnm](?=[kKgGcCjJwWqQtTdDpPbB])", "M", word)
    for cand in (word, nasal, anus):
        if cand[:-1] in mula_raw:               # the final म् is usually ं in the mūla
            return cand
    return word


def seed_verse(lines: list[str], words: list[dict], allow_trailing: bool = False) -> dict:
    """words: [{form, lemma, tags, comp}], in verse order (comp=True: a member followed by
    another member of the same compound). With allow_trailing, words after the verse's
    last unit are ignored (``used`` says how many were taken)."""
    alts = [pausal_candidates(w) for w in words]
    sep_after = ["-" if w["comp"] else " " for w in words]
    comp_before = [False] + [s == "-" for s in sep_after[:-1]]   # word i continues word i-1's compound
    mula_raw = to_slp1(" ".join(lines)).replace(" ", "")
    line_words: list[list[int]] = [[] for _ in lines]
    starts: dict[int, int] = {}
    chosen: list[str] = [a[0] for a in alts]
    w0, failures = 0, []
    unit_list = units(lines)
    for ui, unit in enumerate(unit_list):
        line_norm = [mula_norm(to_slp1(lines[i])) for i in unit]
        target = "".join(line_norm)
        # how many words belong to this unit: try every end point, prefer the one that matches
        found = None
        last = ui == len(unit_list) - 1
        ends = range(w0 + 1, len(words) + 1) if (not last or allow_trailing) else [len(words)]
        for w1 in ends:
            r = rejoin(alts[w0:w1], target, comp_before[w0:w1])
            if r["ok"]:
                found = (w1, r)
                break
        if not found:
            r = rejoin(alts[w0:], target, comp_before[w0:])
            failures.append({"reason": "mismatch", "line": unit[0], "pos": r["best"],
                             "expected": target[max(0, r["best"] - 8):r["best"] + 12],
                             "got": r["got"][max(0, r["best"] - 8):r["best"] + 12]})
            break
        w1, r = found
        bounds, acc = [], 0
        for ln in line_norm:
            bounds.append(acc)
            acc += len(ln)
        for j, (st, ci) in enumerate(zip(r["starts"], r["choice"])):
            wi = w0 + j
            chosen[wi] = alts[wi][ci]
            li = max(k for k, b in enumerate(bounds) if b <= st)
            line_words[unit[li]].append(wi)
            starts[wi] = st - bounds[li]
        w0 = w1
    if not failures and allow_trailing:
        words, alts, sep_after, chosen = words[:w0], alts[:w0], sep_after[:w0], chosen[:w0]
    if failures or w0 != len(words):
        if not failures:
            failures.append({"reason": "leftover_words", "count": len(words) - w0})
        return {"ok": False, "failures": failures}
    chosen = [_mula_spelling(w, mula_raw) for w in chosen]
    _mark_sa_prefix(lines, words, line_words, starts, chosen, sep_after)
    pada_lines, groups = [], []
    for i, line in enumerate(lines):
        idx = line_words[i]
        text = "".join(to_deva(chosen[wi]) + (sep_after[wi] if wi != idx[-1] else "") for wi in idx) if idx else ""
        d = _end_danda(line)
        pada_lines.append(text + (" " + d if d else ""))
        if non_pausal(pada_lines[-1]):          # same pausal rule as check_rejoin
            return {"ok": False, "failures": [{"reason": "non_pausal", "line": i, "word": non_pausal(pada_lines[-1])[0]}]}
        groups.append(_groups(line, idx, starts, chosen, sep_after))
    return {"ok": True, "padaccheda_lines": pada_lines, "groups": groups, "words": chosen, "used": w0}


def _token_offsets(line: str) -> tuple[list[str], list[int]]:
    """The printed tokens of a mūla line and where each starts in the line's ``mula_norm`` text."""
    tokens = re.sub(r"\s*[।॥]\s*$", "", line).strip().split()
    offs, acc = [], 0
    for t in tokens:
        offs.append(acc)
        acc += len(mula_norm(to_slp1(t)))
    return tokens, offs


def _mark_sa_prefix(lines, words, line_words, starts, chosen, sep_after) -> None:
    """Dharmamitra returns ``sa`` both for the pronoun सः and for the prefix स-. The mūla
    tells them apart: the pronoun is printed as a word of its own (स ददर्श), the prefix is
    printed joined to its word (सगन्धर्वैः). An untagged ``sa`` followed, inside the same
    printed token, by a consonant-initial word becomes the compound member स-."""
    for i, line in enumerate(lines):
        _, offs = _token_offsets(line)
        token_of = lambda wi: max(k for k, o in enumerate(offs) if o <= starts[wi])
        for a, b in zip(line_words[i], line_words[i][1:]):
            if (not words[a]["tags"] and words[a]["form"] == "sa" and chosen[a] == "saH"
                    and chosen[b][:1] not in VOWELS and offs and token_of(a) == token_of(b)):
                chosen[a], sep_after[a] = "sa", "-"


def seed_window(lines: list[str], words: list[dict]) -> dict:
    """Seed from the exact word list if possible, else from the first contiguous run of
    ``words`` that re-joins to the verse (for verses regrouped against the CE)."""
    r = seed_verse(lines, words)
    if r["ok"]:
        return {**r, "window": [0, len(words)]}
    target = norm(to_slp1(lines[0])) if lines else ""
    for i in range(len(words)):
        if not any(norm(a)[:1] == target[:1] for a in pausal_candidates(words[i])):   # 1st letter is never changed
            continue
        ri = seed_verse(lines, words[i:], allow_trailing=True)
        if ri["ok"]:
            return {**ri, "window": [i, i + ri["used"]]}
    return {**r, "window": None}


def _groups(line: str, idx: list[int], starts: dict[int, int], chosen: list[str], sep_after: list[str]) -> list:
    """[[sandhi token(s), pada text, flag], " ", …, " ।"] for one line."""
    d = _end_danda(line)
    tokens, offs = _token_offsets(line)
    owner: dict[int, list[int]] = {j: [] for j in range(len(tokens))}
    for wi in idx:
        j = max(k for k, o in enumerate(offs) if o <= starts[wi]) if tokens else 0
        owner[j].append(wi)
    merged: list[tuple[list[str], list[int]]] = []
    for j, t in enumerate(tokens):
        if owner[j] or not merged:
            merged.append(([t], owner[j]))
        else:                                   # a token with no word start belongs to the previous group
            merged[-1][0].append(t)
    if merged and not merged[0][1] and len(merged) > 1:
        first = merged.pop(0)
        merged[0] = (first[0] + merged[0][0], merged[0][1])
    items: list = []
    for k, (toks, wis) in enumerate(merged):
        pd = "".join(to_deva(chosen[wi]) + (sep_after[wi] if n < len(wis) - 1 else "") for n, wi in enumerate(wis))
        if wis and sep_after[wis[-1]] == "-" and wis[-1] != idx[-1]:
            pd += "-"                             # compound continues in the next group
        if k:
            items.append(" ")
        items.append([" ".join(toks), pd, 0])
    if d:
        items.append(" " + d)
    return items
