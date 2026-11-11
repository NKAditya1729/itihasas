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
GENUINE_O = {"aho", "aTo", "o"}              # SLP1; particles that really end in o
PRONOUNS = {"tad", "yad", "etad", "kim", "idam", "adas", "enad"}
T_BEFORE_NASAL_LEMMAS = {"tad", "yad", "etad"}


def parse_dcs(text: str) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    cur = None
    for line in text.splitlines():
        if line.startswith("# id = R."):
            cur = out.setdefault(line.split("R.", 1)[1].strip(), [])
        elif line and not line.startswith("#") and cur is not None:
            form, lemma, tags = line.split("\t")
            t = dict(kv.split("=", 1) for kv in tags.split(",") if "=" in kv)
            comp = t.get("comp") == "y" or (form == "sa" and t.get("pos") == "i")   # prefix sa- (सलीलम्)
            cur.append({"form": form, "lemma": lemma, "tags": t, "comp": comp})
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
    if f.startswith("C") and lemma.startswith("S"):   # ś written ch after a final t: tac CrutvA
        return _pausal({**w, "form": "S" + f[1:]})
    if f == "Bo":                                 # bhoḥ (its visarga drops before voiced sounds)
        return ["BoH", "Bo"]
    if f in ("no", "so") and lemma not in ("no", "so") or (f in ("no", "so") and not tags):
        return [f[:-1] + "aH", f]                 # naḥ, saḥ (the particle no = na + u has lemma no)
    if f in ("sa", "eza") and not w["comp"] and tags.get("pos") != "i":
        return [f + "H", f]                       # saḥ / eṣaḥ (sa, eṣa only before a consonant)
    last = f[-1]
    if len(f) > 2 and f[-2] == "M" and last in "sSz":   # tAMs ← tān before s
        return [f[:-2] + "n"]
    if f[-2:] in ("Av", "Ay"):                          # tAv ← tau, tAy ← tai before a vowel
        return [f[:-2] + ("O" if last == "v" else "E"), f[:-1] + ("u" if last == "v" else "i")]
    if last == "o":
        if f in GENUINE_O or (tags.get("pos") == "i" and lemma == f) or (tags.get("c") == "8" and lemma.endswith("u")):
            return [f]
        if not tags:      # an untagged (Dharmamitra) word is already unsandhied: -o is a vocative, go-, aho …
            return [f, f[:-1] + "aH"]
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
    if last == "n" and len(f) > 2 and not w["comp"] and not lemma.endswith("n") and _t_before_nasal(f, lemma, tags):
        return [f[:-1] + "t", f]                  # yan mAm ← yat; the join decides (t + nasal → n)
    if w["comp"] and f.endswith("n") and lemma.endswith("n"):
        return [f[:-1], f]                        # an/in-stems lose n in compounds
    if last in "aAiIuUeE" and not w["comp"] and tags.get("pos") in ("n", "a", "va", "v"):
        # visarga (or final e) lost before a vowel / voiced sound; the morphology says which forms are possible
        c, n, g = tags.get("c"), tags.get("n"), tags.get("g")
        nom = c == "1"
        if c and tags.get("pos") != "v":
            # a participle is tagged with its root as lemma; in the cases where a consonant
            # stem ends in -aḥ (gen./abl. sg., nom./acc. pl.) a form in -a is not an a-stem form
            cons_stem_ah = (c in ("5", "6") and n == "s") or (c in ("1", "2", "8") and n == "p")
            a_stem = lemma.endswith("a") or lemma in PRONOUNS or (tags.get("pos") == "va" and not cons_stem_ah)
            if last == "a" and a_stem:
                if nom and n == "s" and g != "n":
                    return [f + "H", f]
                if (c == "7" and n == "s") or (nom and n == "p"):
                    return [f[:-1] + "e", f]      # yugAnta iva ← yugānte; sarva eva ← sarve
                if c == "8":
                    return [f, f + "H"]           # the vulgate often has a nominative where the CE has a vocative
                return [f]                        # dative …: an a-stem has no other form in -aḥ
            if last == "A":
                if ((c in ("1", "8") and n == "p" and g != "n") or (c == "2" and n == "p" and g == "f")
                        or (c in ("5", "6") and n == "s" and g == "f") or (nom and n == "s" and lemma.endswith("as"))):
                    return [f + "H", f]
                if c == "3" or (c in ("1", "8") and n == "s"):
                    return [f]                    # instrumental; nom./voc. sg. (sītā, rājā)
        visarga_first = ((last == "a" and nom and n == "s" and (g or "m") == "m")
                         or (last == "A" and c in ("1", "8") and n == "p" and g != "n")
                         or (last in "iu" and nom and n == "s" and g in ("m", "f")))
        return [f + "H", f] if visarga_first else [f, f + "H"]
    return [f]


def _t_before_nasal(f: str, lemma: str, tags: dict) -> bool:
    """Can this n-final DCS form be a final t assimilated to a following nasal?"""
    c, n = tags.get("c"), tags.get("n")
    if tags.get("pos") == "v":
        return tags.get("p") == "3" and n == "s"                  # AsIn ← āsīt, pAtayen ← pātayet
    if lemma in T_BEFORE_NASAL_LEMMAS:
        return tags.get("g") == "n" and n == "s" and c in ("1", "2")   # yan ← yat (never tān, acc. pl.)
    if lemma.endswith(("cit", "cid")) or f.endswith("cin"):
        return True                                               # kaScin ← kaścit
    return c == "5" and n == "s" and f.endswith("An")             # janasTAnAn ← -āt
