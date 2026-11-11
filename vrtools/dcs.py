"""Digital Corpus of Sanskrit (DCS, Oliver Hellwig, CC BY 4.0; ambuda-org/dcs ramayanam.txt).

Each verse is a block ``# id = R.k.s.v`` followed by ``form<TAB>lemma<TAB>tags``.
Compound members carry ``comp=y``. The DCS form is SLP1 and mostly unsandhied,
but it keeps some final sandhi (``ko`` for kaḥ, ``nv`` for nu) and gives
compound members as bare stems (``vAc``, ``manas``). ``pausal_candidates``
lists the pausal forms such a form can stand for, most likely first; the
re-join check then decides.
"""
from __future__ import annotations

import re

FINAL_STOP = {"g": "k", "d": "t", "q": "w", "b": "p", "j": "k", "c": "k", "l": "t", "D": "t", "G": "k", "B": "p"}
GENUINE_O = {"aho", "atho", "bho", "no", "o"}


def parse_dcs(text: str) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    cur = None
    for line in text.splitlines():
        if line.startswith("# id = R."):
            cur = out.setdefault(line.split("R.", 1)[1].strip(), [])
        elif line and not line.startswith("#") and cur is not None:
            form, lemma, tags = line.split("\t")
            t = dict(kv.split("=", 1) for kv in tags.split(",") if "=" in kv)
            cur.append({"form": form, "lemma": lemma, "tags": t, "comp": t.get("comp") == "y"})
    return out


_NATVA = re.compile(r"([rzfF][aAiIuUfFxXeEoOhyvrkKgGNpPbBmM]*)n(?=[aAiIuUfFxXeEoOnmyv])")


def natva(form: str) -> str:
    """n → ṇ after r/ṣ/ṛ within one word when only vowels, h y v r, gutturals,
    labials or anusvāra intervene (Aṣṭādhyāyī 8.4.1–2)."""
    prev = None
    while prev != form:
        prev, form = form, _NATVA.sub(lambda m: m.group(1) + "R", form, count=1)
    return form


def pausal_candidates(w: dict) -> list[str]:
    alts = _pausal(w)
    extra = [natva(a) for a in alts if natva(a) != a and not w["comp"]]
    return alts + [a for a in extra if a not in alts]


def _pausal(w: dict) -> list[str]:
    f, lemma, tags = w["form"], w["lemma"], w["tags"]
    if f.startswith("'"):                         # initial a elided after e/o: 'bravIt
        return _pausal({**w, "form": "a" + f[1:]})
    if not f:
        return [f]
    last = f[-1]
    if last == "o":
        if f in GENUINE_O or (tags.get("pos") == "i" and lemma == f) or (tags.get("c") == "8" and lemma.endswith("u")):
            return [f]
        return [f[:-1] + "aH", f]
    if last in "rSzs":
        return [f[:-1] + "H"] + ([f] if last == "r" else [])
    if last == "v":
        return [f[:-1] + "u", f[:-1] + "U"]
    if last == "y":
        return [f[:-1] + "i", f[:-1] + "I"]
    if last == "M":
        return [f[:-1] + "m"]
    if last in FINAL_STOP:
        alts = [f[:-1] + FINAL_STOP[last]]
        if last == "c":
            alts.append(f[:-1] + "t")            # tac ca ← tat
        if last == "j":
            alts += [f[:-1] + "w", f[:-1] + "t"]  # rāṭ, taj ← tat
        return alts
    if last == "N":
        return [f[:-1] + "k", f]
    if last == "Y":
        return [f[:-1] + "n", f[:-1] + "t"]
    if f.endswith("nn") and len(f) > 2:
        return [f[:-1]]
    if w["comp"] and f.endswith("n") and lemma.endswith("n"):
        return [f[:-1], f]                        # an/in-stems lose n in compounds
    if last in "aAiIuUeE" and not w["comp"] and tags.get("pos") in ("n", "a", "va", "v"):
        return [f, f + "H"]                       # visarga lost before a vowel / voiced sound
    return [f]
