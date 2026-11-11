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
| D6 | Deploy target | **Separate repo** `NKAditya1729/itihasas` (इतिहासाः), own GitHub Pages site: https://nkaditya1729.github.io/itihasas/ with the Rāmāyaṇa at `/ramayanam/`, room for the Mahābhārata. | Created and deployed 2026-11-11 at Aditya's request; not inside sarala-vedanta. |
| D7 | Site content licence | **CC BY-SA 4.0**, attribution to Wikisource contributors and DCS (CC BY 4.0) on an आधाराः page. Code MIT. | |

## Other deviations / implementation choices

- **Word-aligned padaccheda.** The existing Padaccheda toggle (see `EXISTING_DESIGN.md`) swaps per-word spans `[sandhi, pada]`, not whole lines. Each verse therefore also stores `groups`: per line, a list of `[sandhi_form, pada_form, flag]` triples. `lines` and `padaccheda_lines` remain exactly as in CLAUDE.md §4 and are derivable from `groups`.
- **Routing.** One reader shell with hash routing (`#VR.1.1`, `#VR.1.1.5`), as `vsn.js` does. The path URLs of CLAUDE.md §3 (`/ramayanam/1/`, `/ramayanam/1/1/`) are generated as thin shells that open the same reader at the right hash, so both forms work.
- **Python 3.12** via `uv` (the system Python is 3.15, too new for some wheels).

## Stage B decisions (Aditya, 2026-11-11)

| # | Question | Answer | Notes |
|---|---|---|---|
| D8 | Project folder | `~/Documents/Mac Mini Downloads/Ramayana website` | The brief first named `~/Documents/Ramayana website`; corrected the same day. |
| D9 | When is the padaccheda fixed? | **Sarga by sarga**, together with padārtha, anvaya and vyākhyā. Machine seeds are hints only and are marked असमीक्षितम् on the site. | Replaces CLAUDE.md §11 Stage B/C. Reason: `docs/STAGE_B_REVIEW.md` (8–9% of passing seeds are wrong). |
| D10 | Which review items to apply | **M1–M5 only**; M5 as flags, with no change to the text or to verse counts. | Should-fix and optional items of the review are not applied. |
| D11 | Damaged or doubtful mūla | Keep the Wikisource text untouched in `lines`. A correction goes in a new field `lines_corrected`, with `correction` = {what changed, evidence, approved_by, date}. The site shows the corrected text with a small mark; the original stays visible on tap. **No correction is applied without Aditya's approval, verse by verse.** | CLAUDE.md §12. First candidates: VR.1.1.9, 1.1.45, 1.1.100 (proposed, not applied; Aditya is checking a printed edition). |
| D12 | Outside services in Stage B | No new Dharmamitra calls (terms unconfirmed); no IIT Kanpur or valmikiramayan.net fetches. | Re-seeding runs from `cache/dharmamitra/` only. |
| D13 | First mūla corrections | **Approved:** VR.1.1.9 (श्रीमाञ्छ्त्रु- → श्रीमाञ्छत्रु-), VR.1.1.45 (-वासीनाम् → -वासिनाम्), VR.1.1.100 (line 2: स्या- restored), on metre and Critical Edition evidence; VR.1.1.1: the space inside तपःस्वाध्यायनिरतं removed, in the corrected field only. | Stored in `data/meta/corrections.json`; `lines` untouched. The reader shows the corrected text with a संशोधितम् mark; tapping it shows the Wikisource text. VR.1.1.45 has no Critical Edition counterpart (metre and grammar only). |
| D14 | Rulings on pilot verses 1–5 | Keep एकः (अद्वितीयः) प्रियदर्शनः (alternative noted for Swamiji); कस्य with बिभ्यति as it is; **gender: Amarakośa first, then Apte** (संयुग is पुं); नञ्-compounds unhyphenated; a gloss must be simpler than the word; नु is a question particle; **the vyākhyā does not repeat the padārtha** and uses अर्थात् for at most 2–3 hard words. | CLAUDE.md §5.7. `make check` enforces the अर्थात् limit. |
