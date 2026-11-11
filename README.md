# इतिहासाः · Itihāsas

A static Sanskrit reader of the Itihāsas — "learn Sanskrit through the story". First text: **श्रीमद्वाल्मीकिरामायणम्** (7 kāṇḍas, 645 sargas, 23,589 verses), with a Padaccheda toggle. Padārtha, anvaya and simple-Sanskrit vyākhyā are added in later stages; the Mahābhārata comes later.

Site: https://nkaditya1729.github.io/itihasas/ · Rāmāyaṇa: https://nkaditya1729.github.io/itihasas/ramayanam/

**Status: Stage A (draft for review).** Read `docs/STAGE_A_REPORT.md` and `progress/HANDOFF.md`; the working rules are in `CLAUDE.md`.

## Sources and licence
- Text: [Sanskrit Wikisource](https://sa.wikisource.org/wiki/रामायणम्) contributors, CC BY-SA 4.0 (pinned revisions in `cache/wikisource/`).
- Padaccheda seeds: Digital Corpus of Sanskrit (Oliver Hellwig, CC BY 4.0, via Ambuda) and the Dharmamitra segmenter; every split is checked by re-joining it with sandhi rules.
- Site content: CC BY-SA 4.0. Code: MIT. Design after the Vedānta Pathaśālā pages (`web/from-sarala-vedanta/`).

## Build
```
uv sync
make check        # tests + data validation
make site         # → site/
```
The GitHub Pages workflow builds `site/` with `python scripts/build_site.py --out _site` on every push to `main`.
