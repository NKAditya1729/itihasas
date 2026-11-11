"""Phase 2a: seed padaccheda with the Dharmamitra ByT5-Sanskrit segmenter for verses
that DCS could not seed.

The dharmamitra-sanskrit-grammar package (0.1.7) no longer matches the live API
(it sends ``input_sentence``; the API now wants ``texts``) and Devanagari input
comes back garbled, so the endpoint is called directly with IAST input. No
credentials are sent. One request at a time, at least GAP seconds apart; every
response is cached in cache/dharmamitra/ (git-ignored) and reused.

Dharmamitra does not mark compound members, so its padaccheda uses spaces only
and the verse is flagged ``compound_boundaries_unknown``.

Usage: uv run python scripts/seed_dharmamitra.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

import requests
from vidyut.lipi import Scheme, transliterate

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from vrtools.build import mula_hash, text_lines  # noqa: E402
from vrtools.sandhi import CHECKER_VERSION  # noqa: E402
from vrtools.seed import seed_window  # noqa: E402

API = "https://dharmamitra.org/api/tagging/"
CACHE = ROOT / "cache" / "dharmamitra"
BATCH, GAP = 50, 3.0
_last = 0.0


def verse_text(lines: list[str]) -> str:
    return transliterate(" ".join(l.replace("।", " ").replace("॥", " ") for l in lines), Scheme.Devanagari, Scheme.Iast)


def _load_store() -> dict[str, str]:
    """Per-verse cache {iast text: result}, built from every cached response."""
    store = {}
    for f in sorted(CACHE.glob("*.json")):
        d = json.loads(f.read_text())
        store.update(zip(d["texts"], d["results"]))
    return store


_STORE: dict[str, str] | None = None


def segment(texts: list[str]) -> list[str]:
    """Results for ``texts``; only texts never segmented before are sent (≤ BATCH per request)."""
    global _last, _STORE
    if _STORE is None:
        _STORE = _load_store()
    missing = list(dict.fromkeys(t for t in texts if t not in _STORE))
    for i in range(0, len(missing), BATCH):
        _STORE.update(zip(missing[i:i + BATCH], _request(missing[i:i + BATCH])))
    return [_STORE[t] for t in texts]


def _request(texts: list[str]) -> list[str]:
    global _last
    if os.environ.get("DHARMAMITRA_ALLOW_NETWORK") != "1":
        # Stage B: the service's terms of use are not confirmed (docs/STAGE_B_BRIEF.md §4)
        raise RuntimeError(f"{len(texts)} text(s) are not in cache/dharmamitra/ and network calls are off; "
                           "set DHARMAMITRA_ALLOW_NETWORK=1 only with the user's approval")
    key = hashlib.sha256(json.dumps(texts, ensure_ascii=False).encode()).hexdigest()[:20]
    path = CACHE / f"{key}.json"
    for attempt in range(5):
        wait = GAP - (time.monotonic() - _last)
        if wait > 0:
            time.sleep(wait)
        try:
            r = requests.post(API, json={"texts": texts, "mode": "unsandhied", "input_encoding": "auto",
                                         "human_readable_tags": False}, timeout=180)
            _last = time.monotonic()
            if r.status_code in (429, 502, 503, 504):
                time.sleep(30 * (attempt + 1))
                continue
            r.raise_for_status()
            res = r.json()["results"]
            if len(res) != len(texts):
                raise RuntimeError(f"{len(res)} results for {len(texts)} texts")
            path.write_text(json.dumps({"texts": texts, "results": res}, ensure_ascii=False))
            return res
        except requests.RequestException as e:
            _last = time.monotonic()
            print("retry after", e)
            time.sleep(15 * (attempt + 1))
    raise RuntimeError("Dharmamitra: repeated failures")


def words_of(result: str) -> list[dict]:
    out = []
    for tok in re.split(r"[_\s]+", result):
        if any(ch.isalpha() for ch in tok):          # drops "/" line-break markers
            slp = transliterate(tok, Scheme.Iast, Scheme.Slp1)
            out.append({"form": slp, "lemma": slp, "tags": {}, "comp": False})
    return out


def main() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    hashes = json.loads((ROOT / "data" / "meta" / "mula_hashes.json").read_text())
    stats = collections.Counter()
    files = sorted((ROOT / "data" / "vr").glob("*/*.json"))
    docs = {f: json.loads(f.read_text()) for f in files}
    todo = [v for d in docs.values() for v in d["verses"] + (d["appendix"]["verses"] if d["appendix"] else [])
            if v.get("padaccheda_status") != "reviewed"
            and (v.get("seed") or {}).get("source") != "dcs"
            and not ((v.get("seed") or {}).get("source") == "dharmamitra"
                     and v["seed"].get("mula_hash") == mula_hash(text_lines(v))
                     and v["seed"].get("checker") == CHECKER_VERSION)]
    print(len(todo), "verses to seed", flush=True)
    for i in range(0, len(todo), BATCH * 4):           # batches cross sarga boundaries
        chunk = todo[i:i + BATCH * 4]
        for v, res in zip(chunk, segment([verse_text(v["lines"]) for v in chunk])):
            seed = v.get("seed") or {}
            seed["dharmamitra"] = res
            # Dharmamitra was asked about the source text (the cache key); the split must fit the
            # text the verse is read in, i.e. an approved correction where one exists
            r = seed_window(text_lines(v), words_of(res))
            if r["ok"]:
                v["padaccheda_lines"], v["groups"] = r["padaccheda_lines"], r["groups"]
                seed.update({"source": "dharmamitra", "mula_hash": mula_hash(text_lines(v)), "checker": CHECKER_VERSION})
                seed.pop("dharmamitra_failure", None)
                seed.pop("dharmamitra_avagraha_mismatch", None)
                if "compound_boundaries_unknown" not in v["review"]["flags"]:
                    v["review"]["flags"].append("compound_boundaries_unknown")
                stats["ok"] += 1
            else:
                v["padaccheda_lines"], v["groups"] = None, None
                seed.update({"source": None, "dharmamitra_failure": r["failures"][0] if r.get("failures") else None})
                loose = seed_window(text_lines(v), words_of(res), avagraha=False)   # fails only on the avagraha?
                if loose["ok"]:
                    seed["dharmamitra_avagraha_mismatch"] = loose["padaccheda_lines"]
                    stats["avagraha_mismatch"] += 1
                else:
                    seed.pop("dharmamitra_avagraha_mismatch", None)
                stats["fail"] += 1
            v["seed"] = seed
        if (i // (BATCH * 4)) % 20 == 0:
            print(i + len(chunk), "/", len(todo), dict(stats), flush=True)
    for f, d in docs.items():
        f.write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(dict(stats))
    (ROOT / "data" / "meta" / "seed_dharmamitra.json").write_text(json.dumps(dict(stats), indent=1) + "\n")


if __name__ == "__main__":
    main()
