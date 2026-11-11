"""External sandhi joiner and the re-join check (CLAUDE.md §5.1, §7.3).

Everything works in SLP1 (one character per sound). ``junction`` lists the
possible surface forms when a word follows the text joined so far; the search
in ``rejoin`` keeps every candidate whose normalised form is still a prefix of
the normalised mūla, and succeeds if one candidate equals it exactly.

Normalisation for comparison (``norm``) is deliberately narrow:
  * spaces, hyphens, avagraha, daṇḍas and digits are removed;
  * candrabindu ~ is read as anusvāra M;
  * a nasal before a stop of its own class is read as anusvāra M
    (ङ्क = ंक, ञ्च = ंच, ण्ट = ंट, न्त = ंत, म्प = ंप).
Nothing else is equated: word-final म् before a pause stays म्, visarga stays
visarga, vowel length and every consonant must match.

Junction rules are the regular external sandhi of classical Sanskrit (vowel,
visarga, final consonant). The few optional outcomes allowed are listed at the
rule that produces them.
"""
from __future__ import annotations

import re

from vidyut.lipi import Scheme, transliterate

VOWELS = set("aAiIuUfFxXeEoO")
SHORT = set("aiufx")
HARD = set("kKcCwWtTpPSzs")
NASALS = set("NYRnm")
VOICED = set("gGjJqQdDbB") | NASALS | set("yrlvh")
LONG = {"a": "A", "i": "I", "u": "U", "f": "F", "x": "X"}
SAVARNA = {"a": "aA", "A": "aA", "i": "iI", "I": "iI", "u": "uU", "U": "uU", "f": "fF", "F": "fF"}

_DROP = re.compile(r"[\s\-'।॥|.0-9०-९]")
_HOMORGANIC = re.compile(r"N(?=[kKgG])|Y(?=[cCjJ])|R(?=[wWqQ])|n(?=[tTdD])|m(?=[pPbB])")
_DANDAS = re.compile(r"[।॥]")
PRUNE_SLACK = 3   # a junction can rewrite at most the last 3 characters of the joined text


def to_slp1(deva: str) -> str:
    return transliterate(deva, Scheme.Devanagari, Scheme.Slp1)


def to_deva(slp1: str) -> str:
    return transliterate(slp1, Scheme.Slp1, Scheme.Devanagari)


def norm(slp1: str) -> str:
    s = _DROP.sub("", slp1).replace("~", "M")
    return _HOMORGANIC.sub("M", s)


# ---------------------------------------------------------------------------
def _vowel_vowel(L: str, R: str) -> list[tuple[str, int]]:
    a, b, stem = L[-1], R[0], L[:-1]
    out: list[tuple[str, int]] = []
    if a in "aA":
        if b in "aA":
            out.append((stem + "A" + R[1:], len(stem)))
        elif b in "iI":
            out.append((stem + "e" + R[1:], len(stem)))
        elif b in "uU":
            out.append((stem + "o" + R[1:], len(stem)))
        elif b in "fF":
            out.append((stem + "ar" + R[1:], len(stem)))
        elif b in "eE":
            out.append((stem + "E" + R[1:], len(stem)))
        elif b in "oO":
            out.append((stem + "O" + R[1:], len(stem)))
    elif a in "iIuUfF":
        if b in SAVARNA[a]:
            out.append((stem + LONG[a.lower()] + R[1:], len(stem)))
        else:
            out.append((stem + {"i": "y", "I": "y", "u": "v", "U": "v", "f": "r", "F": "r"}[a] + R, len(L)))
        if a in "IU":        # pragṛhya duals (ī, ū) stay unchanged before a vowel
            out.append((L + R, len(L)))
    elif a in "eo":
        if b == "a":         # e/o + a: the a is elided (avagraha)
            out.append((L + R[1:], len(L)))
        else:                # e/o + other vowel: a + hiatus, or ay/av
            out.append((stem + "a" + R, len(L)))
            out.append((stem + ("ay" if a == "e" else "av") + R, len(L) + 1))
        if a == "e":         # pragṛhya dual e
            out.append((L + R, len(L)))
    elif a in "EO":
        out.append((stem + "A" + R, len(L)))
        out.append((stem + ("Ay" if a == "E" else "Av") + R, len(L) + 1))
    return out


def _visarga(L: str, R: str, left_word: str) -> list[tuple[str, int]]:
    b, prev, stem = R[0], L[-2] if len(L) > 1 else "", L[:-1]
    if left_word in ("saH", "ezaH") and b not in VOWELS:   # sa / eṣa before any consonant
        return [(stem + R, len(L) - 1)]
    if b in VOWELS or b in VOICED:
        if prev == "a":
            out = []
            if b == "a":
                out.append((stem[:-1] + "o" + R[1:], len(L) - 1))
            elif b in VOWELS:
                out.append((stem + R, len(L) - 1))          # aḥ + other vowel → a, hiatus
            else:
                out.append((stem[:-1] + "o" + R, len(L)))    # aḥ + voiced consonant → o
            out.append((stem + "r" + R, len(L)))              # r-stems: punar, antar, prātar
            return out
        if prev == "A":
            return [(stem + R, len(L) - 1)]
        if b == "r":                                          # iḥ/uḥ + r → īr/ūr
            return [(stem[:-1] + LONG.get(prev, prev) + R, len(L) - 1)]
        return [(stem + "r" + R, len(L))]
    if b in "cC":
        return [(stem + "S" + R, len(L))]
    if b in "wW":
        return [(stem + "z" + R, len(L))]
    if b in "tT":
        return [(stem + "s" + R, len(L))]
    if b in "Szs":
        out = [(L + R, len(L)), (stem + b + R, len(L))]       # ḥś or śś
        if len(R) > 1 and R[1] in HARD:                       # visarga may drop before sibilant + hard
            out.append((stem + R, len(L) - 1))
        return out
    return [(L + R, len(L))]                                  # before k kh p ph: stays


def _consonant(L: str, R: str) -> list[tuple[str, int]]:
    a, b, stem = L[-1], R[0], L[:-1]
    n = len(L)
    if a == "m":
        return [(L + R, n)] if b in VOWELS else [(stem + "M" + R, n)]
    if a == "M":
        return [(stem + "m" + R, n)] if b in VOWELS else [(L + R, n)]
    if a in "td":
        if b in VOWELS or b in "gGdDbByrv":
            return [(stem + "d" + R, n)]
        if b in "jJ":
            return [(stem + "j" + R, n)]
        if b in "qQ":
            return [(stem + "q" + R, n)]
        if b == "l":
            return [(stem + "l" + R, n)]
        if b in NASALS:
            return [(stem + "n" + R, n), (stem + "d" + R, n)]
        if b in "cC":
            return [(stem + "c" + R, n)]
        if b in "wW":
            return [(stem + "w" + R, n)]
        if b == "S":
            return [(stem + "cC" + R[1:], n), (stem + "c" + R, n)]
        if b == "h":
            return [(stem + "dD" + R[1:], n), (stem + "d" + R, n)]
        return [(stem + "t" + R, n)]
    if a in "kg":
        if b in NASALS:
            return [(stem + "N" + R, n), (stem + "g" + R, n)]
        if b == "h":
            return [(stem + "gG" + R[1:], n), (stem + "g" + R, n)]
        return [(stem + ("g" if b in VOWELS or b in VOICED else "k") + R, n)]
    if a in "wq":
        if b in NASALS:
            return [(stem + "R" + R, n), (stem + "q" + R, n)]
        return [(stem + ("q" if b in VOWELS or b in VOICED else "w") + R, n)]
    if a in "pb":
        if b in NASALS:
            return [(stem + "m" + R, n), (stem + "b" + R, n)]
        return [(stem + ("b" if b in VOWELS or b in VOICED else "p") + R, n)]
    if a in "nN":
        if b in VOWELS:
            short = len(L) > 1 and L[-2] in SHORT
            return [(L + a + R, n + 1)] if short else [(L + R, n)]   # asminn eva
        if a == "N":
            return [(L + R, n)]
        if b in "cC":
            return [(stem + "MS" + R, n)]
        if b in "wW":
            return [(stem + "Mz" + R, n)]
        if b in "tT":
            return [(stem + "Ms" + R, n)]
        if b in "jJ":
            return [(stem + "Y" + R, n)]
        if b in "qQ":
            return [(stem + "R" + R, n)]
        if b == "l":
            return [(stem + "~l" + R, n)]
        if b == "S":
            return [(stem + "YC" + R[1:], n), (stem + "Y" + R, n)]
        return [(L + R, n)]
    return [(L + R, n)]


def junction(L: str, R: str, left_word: str = "") -> list[tuple[str, int]]:
    """Possible joins of word R onto joined text L: (new text, index where R starts)."""
    if not L:
        return [(R, 0)]
    if not R:
        return [(L, len(L))]
    a, b = L[-1], R[0]
    if a in VOWELS:
        if b in VOWELS:
            return _vowel_vowel(L, R)
        if b == "C":                     # tuk: a short vowel doubles ch; after a long one it may
            return [(L + "c" + R, len(L))] + ([] if a in SHORT else [(L + R, len(L))])
        return [(L + R, len(L))]
    if a == "H":
        return _visarga(L, R, left_word)
    return _consonant(L, R)


# ---------------------------------------------------------------------------
def rejoin(words: list[list[str]], target: str) -> dict:
    """Search joins of ``words`` (each a list of alternative SLP1 forms, first =
    preferred) that reproduce the normalised ``target``.

    Returns {"ok", "starts" (index of each word in target), "choice" (alternative
    index per word), "best": longest matched prefix length, "got": best candidate}.
    """
    states: dict[str, tuple[tuple[int, ...], tuple[int, ...], str]] = {"": ((), (), "")}
    best, got = 0, ""
    for alts in words:
        nxt: dict[str, tuple[tuple[int, ...], tuple[int, ...], str]] = {}
        for acc, (starts, choice, last) in states.items():
            for ci, w in enumerate(alts):
                for new, st in junction(acc, w, last):
                    n = norm(new)
                    keep = n[:max(0, len(n) - PRUNE_SLACK)]
                    if not target.startswith(keep):
                        lcp = _lcp(n, target)
                        if lcp > best:
                            best, got = lcp, n
                        continue
                    cand = (starts + (st,), choice + (ci,), w)
                    if new not in nxt or sum(cand[1]) < sum(nxt[new][1]):
                        nxt[new] = cand
                    if len(keep) > best:
                        best, got = len(keep), n
        states = nxt
        if not states:
            break
    for acc, (starts, choice, _) in sorted(states.items(), key=lambda x: sum(x[1][1])):
        if norm(acc) == target:
            return {"ok": True, "starts": list(starts), "choice": list(choice), "best": len(target), "got": acc}
        lcp = _lcp(norm(acc), target)
        if lcp >= best:
            best, got = lcp, norm(acc)
    return {"ok": False, "starts": [], "choice": [], "best": best, "got": got}


def _lcp(a: str, b: str) -> int:
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    return i


def pada_words(pada_line: str) -> list[str]:
    """SLP1 members of a padaccheda line: spaces separate padas, hyphens compound members."""
    out = []
    for word in _DANDAS.sub(" ", pada_line).split():
        out += [m for m in to_slp1(word).split("-") if m]
    return out


def _end_danda(line: str) -> str:
    m = re.search(r"([।॥])\s*$", line)
    return m.group(1) if m else ""


def units(lines: list[str]) -> list[list[int]]:
    """Group line indexes into sandhi units: a unit ends at a line that ends in a daṇḍa."""
    out, cur = [], []
    for i, line in enumerate(lines):
        cur.append(i)
        if _end_danda(line):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def check_rejoin(mula_lines: list[str], pada_lines: list[str]) -> dict:
    failures = []
    if len(mula_lines) != len(pada_lines):
        return {"ok": False, "failures": [{"reason": "line_count", "mula": len(mula_lines), "pada": len(pada_lines)}]}
    for i, (m, p) in enumerate(zip(mula_lines, pada_lines)):
        if _DANDAS.findall(m) != _DANDAS.findall(p):
            failures.append({"reason": "danda", "line": i})
    if failures:
        return {"ok": False, "failures": failures}
    for unit in units(mula_lines):
        target = norm(to_slp1(" ".join(mula_lines[i] for i in unit)))
        words = [[w] for i in unit for w in pada_words(pada_lines[i])]
        r = rejoin(words, target)
        if not r["ok"]:
            pos = r["best"]
            failures.append({"reason": "mismatch", "line": unit[0], "pos": pos,
                             "expected": target[max(0, pos - 8):pos + 12], "got": r["got"][max(0, pos - 8):pos + 12]})
    return {"ok": not failures, "failures": failures}
