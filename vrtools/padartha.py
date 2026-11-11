"""Checks on the generated layers of one verse (Stage B, Step 4d; CLAUDE.md §7.3–§7.5).

``check_layers(lines, verse)`` returns {"errors", "unverified", "vyakhya_used_padas"}.

1. The padaccheda re-joins to the text (``lines``: the corrected text where one exists).
2. Every pada of the padaccheda has exactly one padārtha entry, in verse order.
3. Each entry is an indeclinable, a nominal or a finite verb, with the fields of its kind,
   and **its analysis fits the form**: the case and number (or tense, person and number)
   must be among those the vidyut word list gives for that form. A form the word list does
   not know (a name, a rare compound) is listed under "unverified", not failed. Where
   the word list wrongly rejects a correct form (an ārṣa form such as शंसत् for अशंसत्),
   the entry carries a "fit_note" saying why; it is then listed, not failed.
4. A qualifier (``anvita``) agrees with what it qualifies in case, number and gender.
5. The anvaya has every pada exactly once; any other word stands in parentheses.
6. The vyākhyā (§5.4) reuses at least 80% of the significant padas (bold words), has 3–7
   sentences, is not a chain of dash glosses, and keeps its words separate (no avagraha,
   no sandhi consonant at a word end, no anusvāra before a vowel or a pause). No Sanskrit
   field has Latin letters. The rest of §5.4 (real clauses, connectors, one or two
   stretching constructions, short compounds) is the reviewer's to judge.

The word list over-generates (it knows च also as a noun form), so it can only say that an
analysis is impossible, never that it is the right one. That judgment is the reviewer's.
"""
from __future__ import annotations

import functools
import math
import os
import re
from collections import Counter
from pathlib import Path

from .sandhi import check_rejoin, fold, junction, norm, to_slp1

DATA = Path(os.environ.get("VIDYUT_DATA", Path(__file__).resolve().parent.parent / "cache" / "vidyut-data"))

LINGA = {"पुं": "puM", "स्त्री": "strI", "नपुं": "napuMsaka"}
VIBHAKTI = {"प्रथमा": "praTamA", "द्वितीया": "dvitIyA", "तृतीया": "tftIyA", "चतुर्थी": "caturTI", "पञ्चमी": "paYcamI",
            "षष्ठी": "zazWI", "सप्तमी": "saptamI", "सम्बोधन": "samboDanam"}
VACANA = {"एक": "eka", "द्वि": "dvi", "बहु": "bahu"}
PURUSHA = {"प्रथम": "praTama", "मध्यम": "maDyama", "उत्तम": "uttama"}
LAKARA = {"लट्": "la~w", "लिट्": "li~w", "लुट्": "lu~w", "लृट्": "lf~w", "लोट्": "lo~w", "लङ्": "la~N",
          "विधिलिङ्": "viDili~N", "आशीर्लिङ्": "ASIrli~N", "लुङ्": "lu~N", "लृङ्": "lf~N"}
NO_LINGA = {"अस्मद्", "युष्मद्"}                 # the personal pronouns have no gender
CASE_FIELDS = ("linga", "vibhakti", "lakara", "purusha")
MIN_REUSE, MIN_SENTENCES, MAX_SENTENCES, MAX_DASH_GLOSSES = 0.8, 3, 7, 1

_DANDA = re.compile(r"[।॥]")
_PUNCT = re.compile(r"[।॥,;:?!—–\"“”'‘’()\[\]]")
_LATIN = re.compile(r"[A-Za-z]")
_BOLD = re.compile(r"\*\*(.+?)\*\*")
_NASAL = {**{c: "N" for c in "kKgG"}, **{c: "Y" for c in "cCjJ"}, **{c: "R" for c in "wWqQ"},
          **{c: "n" for c in "tTdD"}, **{c: "m" for c in "pPbB"}}


@functools.cache
def _kosha():
    from vidyut.kosha import Kosha
    return Kosha(str(DATA / "kosha"))


def _lookup(slp: str) -> list:
    """Word-list entries for a pausal form (the list writes -s / -r for visarga, -m for ṃ,
    and the class nasal before a stop)."""
    forms = [slp[:-1] + "s", slp[:-1] + "r"] if slp.endswith("H") else [slp]
    forms += [f[:-1] + "m" for f in forms if f.endswith("M")]
    forms += [re.sub(r"M(?=([kKgGcCjJwWqQtTdDpPbB]))", lambda m: _NASAL[m.group(1)], f) for f in forms]
    out = []
    for f in dict.fromkeys(forms):
        out += _kosha().get(f)
    return out


def _nominal_readings(slp: str) -> set[tuple[str, str]]:
    return {(str(e.vibhakti), str(e.vacana)) for e in _lookup(slp) if "Subanta" in type(e).__name__}


def _verb_readings(slp: str) -> set[tuple[str, str, str]]:
    return {(str(e.lakara), str(e.purusha), str(e.vacana)) for e in _lookup(slp) if "Tinanta" in type(e).__name__}


def _plain(pada: str) -> str:
    return to_slp1(pada.replace("-", ""))


def _key(deva: str) -> str:
    """Comparison key of a word: SLP1, hyphens dropped, nasal spelling folded, final m = ṃ."""
    s = fold(to_slp1(deva.replace("-", "")))
    return s[:-1] + "M" if s.endswith("m") else s


def _final(s: str) -> str:
    return s[:-1] + "M" if s.endswith("m") else s


def _keys(pada: str) -> set[str]:
    """Every way a pada may be written as one word: its members joined with compound
    sandhi (वाक्-विदाम् → वाग्विदाम्) or simply put together."""
    members = [to_slp1(m) for m in pada.split("-") if m]
    joined = {""}
    for i, m in enumerate(members):
        joined = {norm(new) for acc in joined for new, _ in junction(acc, m, members[i - 1] if i else "", True, False)}
    return {_final(fold(j)) for j in joined} | {_key(pada)}


def padas_of(pada_lines: list[str]) -> list[str]:
    return [p for line in pada_lines for p in _DANDA.sub(" ", line).split()]


def _kind(e: dict) -> str:
    if e.get("avyaya") is True:
        return "avyaya"
    return "verb" if "lakara" in e or "purusha" in e else "nominal"


def _entry_errors(e: dict) -> list[str]:
    pada, kind, errs = e.get("pada", "?"), _kind(e), []
    if not (e.get("artha") or "").strip():
        errs.append(f"{pada}: no artha")
    if kind == "avyaya":
        extra = [f for f in CASE_FIELDS if f in e]
        if extra:
            errs.append(f"{pada}: an avyaya carries no {', '.join(extra)}")
        return errs
    need = {"verb": {"dhatu": None, "lakara": LAKARA, "purusha": PURUSHA, "vacana": VACANA},
            "nominal": {"pratipadika": None, "linga": LINGA, "vibhakti": VIBHAKTI, "vacana": VACANA}}[kind]
    for field, allowed in need.items():
        value = e.get(field)
        if field == "linga" and value is None and e.get("pratipadika") in NO_LINGA:
            continue
        if not value:
            errs.append(f"{pada}: {kind} entry without {field}")
        elif allowed is not None and value not in allowed:
            errs.append(f"{pada}: {field} “{value}” is not one of {' / '.join(allowed)}")
    return errs


def _fit_errors(e: dict, unverified: list[str]) -> list[str]:
    """Is the stated analysis possible for the form?"""
    pada, kind = e["pada"], _kind(e)
    slp = _plain(pada)
    if (e.get("fit_note") or "").strip():      # a declared exception (an ārṣa form, a stem the list lacks):
        unverified.append(pada)                # not failed, but listed for the reviewer and the scholar
        return []
    if kind == "nominal":
        readings = _nominal_readings(slp) or _nominal_readings(to_slp1(pada.split("-")[-1]))
        if not readings:
            if _verb_readings(slp):
                return [f"{pada}: analysed as a nominal, but the word list knows this form only as a verb"]
            unverified.append(pada)
            return []
        want = (VIBHAKTI[e["vibhakti"]], VACANA[e["vacana"]])
        if want not in readings:
            return [f"{pada}: the form cannot be {e['vibhakti']} {e['vacana']}"]
        return []
    if kind == "verb":
        readings = _verb_readings(slp)
        if not readings and e.get("upasarga"):          # the word list has no prefixed forms: try the bare verb
            for k in range(1, len(slp) - 2):
                readings = _verb_readings(slp[k:])
                if readings:
                    break
        if not readings:
            if _nominal_readings(slp):
                return [f"{pada}: analysed as a verb, but the word list knows this form only as a nominal"]
            unverified.append(pada)
            return []
        want = (LAKARA[e["lakara"]], PURUSHA[e["purusha"]], VACANA[e["vacana"]])
        if want not in readings:
            return [f"{pada}: the form cannot be {e['lakara']} {e['purusha']} {e['vacana']}"]
    return []


def _agreement_errors(entries: list[dict]) -> list[str]:
    by_key = {}
    for e in entries:
        for k in _keys(e["pada"]):
            by_key.setdefault(k, e)
    errs = []
    for e in entries:
        target = e.get("anvita")
        if not target:
            continue
        t = by_key.get(_key(target))
        if t is None:
            errs.append(f"{e['pada']}: anvita “{target}” is not a pada of this verse")
        elif _kind(e) != "nominal" or _kind(t) != "nominal":
            errs.append(f"{e['pada']}: anvita links two nominals; “{target}” or this pada is not one")
        elif any(e.get(f) != t.get(f) for f in ("vibhakti", "vacana")) or (e.get("linga") and t.get("linga") and e["linga"] != t["linga"]):
            errs.append(f"{e['pada']}: does not agree with {target} in case, number and gender")
    return errs


def _anvaya_errors(padas: list[str], anvaya: str) -> list[str]:
    outside = re.sub(r"\([^)]*\)", " ", anvaya)
    if "(" in outside or ")" in outside:
        return ["anvaya: unbalanced parentheses"]
    tokens = [t for t in _PUNCT.sub(" ", outside).split() if t]
    left, missing, errs = list(tokens), [], []
    for p in padas:                                   # each pada takes one token that writes it
        keys = _keys(p)
        hit = next((t for t in left if _key(t) in keys), None)
        if hit is None:
            missing.append(p)
        else:
            left.remove(hit)
    extra = list(dict.fromkeys(left))
    if missing:
        errs.append(f"anvaya: pada(s) missing or too few: {' '.join(missing)}")
    if extra:
        errs.append(f"anvaya: word(s) that are not padas of the verse must stand in parentheses: {' '.join(extra)}")
    return errs


_NON_PAUSAL = set("rszSgGdDbBqQjJcCKTPWhyvl")      # a word cannot end in these when it stands alone


def _sandhi_errors(vyakhya: str) -> list[str]:
    """§5.4 rule 2: words stay separate. What a machine can see: an avagraha, a word that ends
    in a sandhi consonant (श्रेष्ठश् च), an anusvāra before a vowel or a pause (श्रेष्ठं अस्ति).
    Vowel sandhi between two words (मुनिर्महान्, चास्ति) is left to the reviewer."""
    errs = []
    if "ऽ" in vyakhya:
        errs.append("vyākhyā: external sandhi (avagraha ऽ): keep the words separate")
    for chunk in re.split(r"[।॥?!,;:—–]", vyakhya.replace("**", "")):
        words = [w for w in _PUNCT.sub(" ", chunk).split() if w]
        for i, w in enumerate(words):
            s = to_slp1(w)
            if s[-1:] in _NON_PAUSAL:
                errs.append(f"vyākhyā: external sandhi: “{w}” does not end in a pausal sound")
            elif s.endswith("M") and (i + 1 == len(words) or to_slp1(words[i + 1])[:1] in "aAiIuUfFxXeEoO"):
                errs.append(f"vyākhyā: external sandhi: anusvāra in “{w}” before a vowel or a pause (write म्)")
    return errs


def _vyakhya_report(entries: list[dict], vyakhya: str) -> tuple[list[str], list[str]]:
    used = [w for chunk in _BOLD.findall(vyakhya) for w in _PUNCT.sub(" ", chunk).split()]
    bold = [fold(to_slp1(w)) for w in used]
    errs, missing, significant = [], [], [e for e in entries if _kind(e) != "avyaya"]
    for e in significant:
        members = [fold(to_slp1(m)) for m in e["pada"].split("-") if m]
        hit = sum(any(m[:max(2, len(m) - 2)] in b for b in bold) for m in members)
        if hit < math.ceil(len(members) / 2):
            missing.append(e["pada"])
    if significant and (len(significant) - len(missing)) / len(significant) < MIN_REUSE:
        errs.append(f"vyākhyā: reuses only {len(significant) - len(missing)} of {len(significant)} significant padas "
                    f"(not found in bold: {' '.join(missing)})")
    sentences = [s for s in re.split(r"[।॥?!]", vyakhya.replace("**", "")) if s.strip()]
    if not MIN_SENTENCES <= len(sentences) <= MAX_SENTENCES:
        errs.append(f"vyākhyā: {len(sentences)} sentences (should be {MIN_SENTENCES}–{MAX_SENTENCES})")
    dash_glosses = len(re.findall(r"[—–-]\s*अर्थात्", vyakhya))
    if dash_glosses > MAX_DASH_GLOSSES:               # §5.4 rule 1: prose, not a chain of "X — अर्थात् Y —"
        errs.append(f"vyākhyā: {dash_glosses} dash glosses with अर्थात् (explain a word inside the sentence: X इत्युक्ते Y)")
    errs += _sandhi_errors(vyakhya)
    return errs, used


def check_layers(lines: list[str], v: dict) -> dict:
    errors, unverified, used = [], [], []
    pada_lines, entries = v.get("padaccheda_lines") or [], v.get("padartha") or []
    r = check_rejoin(lines, pada_lines) if pada_lines else {"ok": False, "failures": [{"reason": "no padaccheda"}]}
    if not r["ok"]:
        f = r["failures"][0]
        errors.append(f"padaccheda does not re-join to the text ({f.get('reason')}"
                      + (f": expected …{f['expected']}, got …{f['got']}" if "expected" in f else "") + ")")
    padas = padas_of(pada_lines)
    listed = [e.get("pada", "") for e in entries]
    if listed != padas:
        want, have = Counter(padas), Counter(listed)
        for p in dict.fromkeys(padas):
            if have[p] < want[p]:
                errors.append(f"{p}: no padārtha entry")
        for p in dict.fromkeys(listed):
            if have[p] > want[p]:
                errors.append(f"{p}: padārtha entry for a word that is not a pada of the padaccheda")
        if want == have:
            errors.append("padārtha entries are not in verse order")
    for e in entries:
        errs = _entry_errors(e)
        errors += errs or _fit_errors(e, unverified)
        for field in ("pada", "artha", "vigraha", "fit_note"):
            if _LATIN.search(e.get(field) or ""):
                errors.append(f"{e.get('pada', '?')}: Latin letters in {field}")
    if not any("entry without" in x or "is not one of" in x for x in errors):
        errors += _agreement_errors([e for e in entries if e.get("pada")])
    if v.get("anvaya"):
        errors += _anvaya_errors(padas, v["anvaya"])
        if _LATIN.search(v["anvaya"]):
            errors.append("anvaya: Latin letters")
    if v.get("vyakhya_sa"):
        errs, used = _vyakhya_report([e for e in entries if e.get("pada")], v["vyakhya_sa"])
        errors += errs
        if _LATIN.search(v["vyakhya_sa"]):
            errors.append("vyākhyā: Latin letters")
    return {"errors": errors, "unverified": unverified, "vyakhya_used_padas": used}


SEED_FLAGS = ("seed_disagreement", "compound_boundaries_unknown", "avagraha_mismatch")   # settled by a sarga review


def merge_verse(v: dict, draft: dict, gen: dict, verdict: str) -> dict:
    """Write a reviewed draft (padaccheda, padārtha, anvaya, vyākhyā) into a verse. Nothing
    is written unless every check passes. Returns the check result."""
    from .build import text_lines
    from .seed import groups_for
    lines = text_lines(v)
    result = check_layers(lines, draft)
    if result["errors"]:
        raise ValueError(f"{v['id']}: " + "; ".join(result["errors"]))
    v["padaccheda_lines"] = list(draft["padaccheda_lines"])
    v["groups"] = groups_for(lines, v["padaccheda_lines"])
    v["padaccheda_status"] = "reviewed"
    v["padartha"], v["anvaya"], v["vyakhya_sa"] = draft["padartha"], draft["anvaya"], draft["vyakhya_sa"]
    v["vyakhya_used_padas"] = result["vyakhya_used_padas"]
    v["speaker"], v["context_note_sa"] = draft.get("speaker"), draft.get("context_note_sa")
    review = v["review"]
    review["auto_checks"] = {"rejoin": True, "coverage": True, "padartha_fit": True, "metre": bool(v["metre"]["ok"]),
                             "schema": True, "unverified_forms": result["unverified"]}
    review["agent_review"] = verdict
    review["flags"] = [f for f in review["flags"] if f not in SEED_FLAGS]
    v["gen"] = dict(gen)
    return result
