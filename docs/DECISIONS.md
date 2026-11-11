# Decisions

Answers given by Aditya on 2026-11-11, before Phase 1.

| # | Question | Answer | Notes |
|---|---|---|---|
| D1 | Recension / base text | **Live Sanskrit Wikisource vulgate**, fetched via the MediaWiki API, pinned per page by revision id (`cache/wikisource/`). | **Deviation from CLAUDE.md §2**: the brief named `Ramayana_Book/san/*_all.json` as the acquisition route. That copy turned out to be an older, half-split text (~43% of verses have sandhi undone, e.g. `एतत् इच्छामि अहम् श्रोतुम्`; typos such as `धृढव्रतः`). Live Wikisource has the saṃhitā text. Ramayana_Book is kept only as a count cross-check. Same edition family and licence. |
| D1b | Show CE crosswalk badges? | **No.** | Crosswalk is still computed internally (Phase 2a) for DCS seeding; no CE badge or CE text on the site. |
| D1c | Ayodhyā sargas that are half-split even on Wikisource (41 of 119, ≈1,180 verses) | **Keep exactly as Wikisource has them and flag** each verse `source_presplit`; list them in the Stage A report. | Correcting them from a public-domain print (Nirnaya Sagar 1930) is a later, reviewed task. The machine never writes the mūla. |
| D2 | Uttara Kāṇḍa | **Include as the 7th kāṇḍa, marked** with a short note on its index page. | |
| D3 | Samāsa hyphens in padaccheda view | **Show hyphens**, as on the existing Viṣṇusahasranāma page. | |
| D4 | Badges | **Metre badge only for non-Anuṣṭup verses**; **speaker badge from Phase 3**. | No metre badge on Anuṣṭup verses; no CE badge. |
| D5 | Verse numbering | **Wikisource printed numbers.** Skips/duplicates get suffixes (`VR.6.25.12a`) and go to `data/meta/anomalies.json`; original marker kept in `src_ref`. | |
| D6 | Deploy target | **Separate repo** built from this folder (`Ramayana website`), own GitHub Pages site, linked from the `sarala-vedanta` hub. | Repo name and push wait for Aditya's go-ahead. |
| D7 | Site content licence | **CC BY-SA 4.0**, attribution to Wikisource contributors and DCS (CC BY 4.0) on an आधाराः page. Code MIT. | |

## Other deviations / implementation choices

- **Word-aligned padaccheda.** The existing Padaccheda toggle (see `EXISTING_DESIGN.md`) swaps per-word spans `[sandhi, pada]`, not whole lines. Each verse therefore also stores `groups`: per line, a list of `[sandhi_form, pada_form, flag]` triples. `lines` and `padaccheda_lines` remain exactly as in CLAUDE.md §4 and are derivable from `groups`.
- **Routing.** One reader shell with hash routing (`#VR.1.1`, `#VR.1.1.5`), as `vsn.js` does. The path URLs of CLAUDE.md §3 (`/ramayanam/1/`, `/ramayanam/1/1/`) are generated as thin shells that open the same reader at the right hash, so both forms work.
- **Python 3.12** via `uv` (the system Python is 3.15, too new for some wheels).
