"""Metre identification for one verse.

Syllable weights come from ``vidyut.chandas``. vidyut's metre list has only
vṛtta metres (its data README: jāti metres are not supported), so the śloka
(Anuṣṭup) and mixed Upajāti are checked here:

* Anuṣṭup: 16, 32 or 48 syllables (half, full, six-pāda), and every even pāda has the
  obligatory cadence ⏑ – ⏑ in syllables 5–7. Odd pādas (pathyā and the
  vipulās) are not constrained.
* The śloka check runs first: vidyut's mātrā metres (āryā family) also fit
  many 32-syllable ślokas.
* Upajāti: every pāda 11 syllables, each Indravajrā or Upendravajrā; or every
  pāda 12 syllables, each Vaṃśastha or Indravaṃśā (final syllable anceps).
"""
from __future__ import annotations

import functools
import os
from pathlib import Path

from vidyut.chandas import Chandas
from vidyut.lipi import Scheme, transliterate

DATA = Path(os.environ.get("VIDYUT_DATA", Path(__file__).resolve().parent.parent / "cache" / "vidyut-data"))
ANUSHTUP = "अनुष्टुप्"
UPAJATI = "उपजातिः"
# vidyut's built-in mātrā (jāti) metres; on a śloka-length verse a match here means a
# broken śloka, not an āryā (the Rāmāyaṇa has practically no āryā verses)
MATRA = {"आर्या", "गीति", "उपगीति", "उद्गीति", "आर्यागीति"}
_UPAJATI_11 = ("GGLGGLLGLG", "LGLGGLLGLG")      # Indravajrā, Upendravajrā (anceps dropped)
_UPAJATI_12 = ("LGLGGLLGLGL", "GGLGGLLGLGL")    # Vaṃśastha, Indravaṃśā


@functools.cache
def _chandas() -> Chandas:
    return Chandas(str(DATA / "chandas" / "meters.tsv"))


def _slp1(lines: list[str]) -> str:
    text = ""
    for line in lines:
        line = line.replace("।", "").replace("॥", "").strip()
        if text.endswith("-"):           # word continues on the next printed line
            text = text[:-1] + line
        else:
            text += ("\n" if text else "") + line
    slp1 = transliterate(text, Scheme.Devanagari, Scheme.Slp1)
    # stray non-Sanskrit signs (source typos such as U+093A) would crash vidyut
    return "".join(ch for ch in slp1 if ch.isascii())


def _padas(weights: str, size: int) -> list[str]:
    return [weights[i:i + size] for i in range(0, len(weights), size)]


def _is_anushtup(weights: str) -> bool:
    if len(weights) not in (16, 32, 48):   # half, full and six-pāda ślokas
        return False
    return all(p[4:7] == "LGL" for p in _padas(weights, 8)[1::2])


def _is_upajati(weights: str) -> bool:
    for size, shapes in ((11, _UPAJATI_11), (12, _UPAJATI_12)):
        if len(weights) == 4 * size and all(p[:-1] in shapes for p in _padas(weights, size)):
            return True
    return False


def identify(lines: list[str]) -> dict:
    match = _chandas().classify(_slp1(lines))
    weights = "".join(a.weight for line in match.aksharas for a in line)
    n = len(weights)
    if _is_anushtup(weights):
        return {"name": ANUSHTUP, "syllables": n, "ok": True}
    name = transliterate(match.padya, Scheme.Slp1, Scheme.Devanagari) if match.padya else None
    if name and not (name in MATRA and n in (16, 32, 48)):
        return {"name": name, "syllables": n, "ok": name not in MATRA}   # mātrā metres are suspect
    if _is_upajati(weights):
        return {"name": UPAJATI, "syllables": n, "ok": True}
    if n in (16, 32, 48):  # śloka-length but cadence broken
        return {"name": ANUSHTUP, "syllables": n, "ok": False}
    return {"name": None, "syllables": n, "ok": False}
