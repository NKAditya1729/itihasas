"""Parse one Wikisource sarga page (wikitext) into verses.

The parser never edits the Sanskrit text of a verse: it removes wiki markup,
cuts the page into verses at the printed verse markers, and replaces each
marker by ॥ (the marker itself is kept in ``src_ref``). Anything it drops
(pasted residue after a marker, text after the colophon) is logged verbatim in
``anomalies``. Spelling and spacing are left for ``vrtools.normalize``.
"""
from __future__ import annotations

import re

DEVA_DIGITS = "०१२३४५६७८९"
_NUM = r"[0-9०-९]+"
# ॥१-५-१॥ · ॥ १॥ · ।। २.१००.१ ।। · ॥५.२५॥ · || 3 ||
MARK = re.compile(
    rf"(?:॥|।।|\|\|)\s*(?P<num>{_NUM}(?:\s*[-.]\s*{_NUM}){{0,2}})\s*(?:॥|।।|\|\|)")
BARE_END = re.compile(r"(?:॥|।।|\|\|)\s*$")
DEVA = re.compile(r"[ऀ-ॿ]")
LETTER = re.compile(r"[ऄ-हऽ-्ॐ-ॣॲ-ॿ]")  # not digits/daṇḍas
QUOTES = "”’“‘\"'"
RENUMBER_THRESHOLD = 3   # duplicate / out-of-order numbers in one sarga


def to_int(s: str) -> int:
    return int(s.translate(str.maketrans(DEVA_DIGITS, "0123456789")))


def strip_markup(text: str) -> str:
    text = re.split(r"^==\s*स्रोतः\s*==", text, maxsplit=1, flags=re.M)[0]
    prev = None
    while prev != text:  # innermost templates first, so nested ones go too
        prev, text = text, re.sub(r"\{\{[^{}]*\}\}", "", text)
    text = re.sub(r"\[\[[^\]]*\]\]", "", text)            # files, categories, wiki links
    text = re.sub(r"\[https?://[^\]]*\]", "", text)        # external links
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("'''", "").replace("''", "")
    return text


def _is_colophon(line: str) -> bool:
    return line.startswith(("इति", "इत्या")) and "सर्ग" in line


def _parts(num: str) -> tuple[list[int], str]:
    sep = "-" if "-" in num else "." if "." in num else ""
    return [to_int(p) for p in re.split(r"\s*[-.]\s*", num.strip())], sep


class _Sarga:
    def __init__(self, kanda: int, sarga: int):
        self.kanda, self.sarga = kanda, sarga
        self.out = {"source_heading": None, "colophon": None, "verses": [], "anomalies": []}
        self.pending: list[str] = []
        self.pending_flags: list[str] = []
        self.seen: dict[int, int] = {}
        self.last_n = 0

    def anomaly(self, **a):
        self.out["anomalies"].append({"kanda": self.kanda, "sarga": self.sarga, **a})

    def close(self, ref: str | None, n: int | None):
        lines, flags = self.pending[:], self.pending_flags[:]
        self.pending.clear()
        self.pending_flags.clear()
        if not lines:
            self.anomaly(type="empty_verse", src_ref=ref)
            return
        if n is None:
            n, flags = self.last_n, flags + ["unnumbered"]
            self.anomaly(type="unnumbered", after=self.last_n, text=lines[0])
        count = self.seen.get(n, 0)
        suffix = "" if count == 0 else "abcdefghijklmnopqrstuvwxyz"[min(count, 26) - 1]
        if count and "unnumbered" not in flags:
            self.anomaly(type="duplicate_number", n=n, src_ref=ref)
        if not count and n > self.last_n + 1:
            self.anomaly(type="gap", n=n, missing=list(range(self.last_n + 1, n)))
        elif not count and n <= self.last_n:
            self.anomaly(type="out_of_order", n=n, after=self.last_n)
        self.seen[n] = count + 1
        self.last_n = max(self.last_n, n)
        half = len(lines) == 1 and "।" not in lines[0].rstrip("॥ ")
        self.out["verses"].append({"n": n, "suffix": suffix, "src_ref": ref, "lines": lines,
                                   "half": half, "flags": flags})

    def feed(self, line: str):
        if self.pending and BARE_END.search(self.pending[-1]):
            self.pending_flags.append("inner_double_danda")
        pos = 0
        for m in MARK.finditer(line):
            parts, sep = _parts(m.group("num"))
            if len(parts) == 2 and sep == "-":   # a k-s sarga marker inside the text
                self.anomaly(type="sarga_marker_in_text", text=line)
                continue
            if pos and not LETTER.search(line[pos:m.start()]):
                # a second marker right after the first (॥ १६ ॥१-३४-१६॥)
                self.anomaly(type="double_marker", src_ref=m.group(0).strip(), n=parts[-1])
                pos = m.end()
                continue
            self.pending.append(line[pos:m.start()] + "॥")
            ref = m.group(0).strip()
            if len(parts) == 3 and parts[:2] != [self.kanda, self.sarga]:
                self.anomaly(type="ref_mismatch", src_ref=ref)
            elif len(parts) == 2 and parts[0] not in (self.sarga, self.kanda):
                self.anomaly(type="ref_mismatch", src_ref=ref)
            self.close(ref, parts[-1])
            pos = m.end()
        if pos:
            rest = line[pos:].strip()
            if rest:
                self.anomaly(type="residue_after_marker", text=rest)
            return
        self.pending.append(line)

    def finish(self):
        if self.pending:
            self.close(None, None)
        broken = sum(a["type"] in ("duplicate_number", "out_of_order") for a in self.out["anomalies"])
        if broken >= RENUMBER_THRESHOLD:
            for i, v in enumerate(self.out["verses"], 1):
                v["n"], v["suffix"] = i, ""
                v["flags"] = sorted(set(v["flags"] + ["renumbered"]))
            self.anomaly(type="renumbered_sarga", reason=f"{broken} duplicate/out-of-order printed numbers",
                         printed=[v["src_ref"] for v in self.out["verses"]])
        return self.out


def _clean_lines(wikitext: str) -> list[str]:
    lines = []
    for raw in strip_markup(wikitext).split("\n"):
        line = raw.strip().strip(QUOTES).strip()
        if line and DEVA.search(line):
            lines.append(line)
    return lines


def parse_sarga(wikitext: str, kanda: int, sarga: int) -> dict:
    main = _Sarga(kanda, sarga)
    lines = _clean_lines(wikitext)
    after: list[str] = []
    for i, line in enumerate(lines):
        if _is_colophon(line):
            if main.pending:
                main.close(None, None)
            main.out["colophon"] = line
            after = lines[i + 1:]
            break
        if not main.out["verses"] and not main.pending and "सर्गः" in line and line.startswith("श्री"):
            main.out["source_heading"] = line
        elif re.match(r"^==.*==$", line):
            main.anomaly(type="section_heading", text=line)
        else:
            main.feed(line)
    out = main.finish()
    if out["colophon"] is None:
        main.anomaly(type="missing_colophon")
    out["appendix"] = None
    if after and "प्रक्षिप्त" in after[0]:
        app = _Sarga(kanda, sarga)
        for line in after[1:]:
            if _is_colophon(line):
                app.out["colophon"] = line
            else:
                app.feed(line)
        out["appendix"] = {"heading": after[0], **app.finish()}
        out["anomalies"] += [{**a, "in_appendix": True} for a in out["appendix"].pop("anomalies")]
    else:
        for line in after:
            main.anomaly(type="text_after_colophon", text=line)
    return out
