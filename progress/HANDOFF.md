# Handoff — Stage B, Step 4 (pilot) in progress (2026-11-11)

**Read first:** `docs/STAGE_B_BRIEF.md` (the working instructions; it overrides
CLAUDE.md where they differ), `CLAUDE.md` §11–§12, then `docs/STAGE_B_REVIEW.md`.

- Project folder: `~/Documents/Mac Mini Downloads/Ramayana website`
- Repository: https://github.com/NKAditya1729/itihasas · branch **`stage-b`**
  (local only, not pushed; `main` is untouched and is what the live site serves)
- Live site: https://nkaditya1729.github.io/itihasas/ramayanam/

## Where things stand
- Step 2 (review) done: `docs/STAGE_B_REVIEW.md`.
- **Step 3 done on `stage-b`: review items M1–M5 applied, test-first.**
  `make check`: 207 tests pass, 23,615 verses, 15,447 with padaccheda, 0 errors.
  `make site` builds. **Waiting for Aditya's word to merge to `main`.**
- Not applied (by decision D10): should-fix S1–S7 and optional O1–O5 of the review.

## What Step 3 changed
- **Checker v7** (`vrtools/sandhi.py`): avagraha is significant (optional inside a
  compound and after a long ā; also accepted after an anusvāra, उक्तोंऽशुमान्); one
  vowel hiatus is allowed exactly at the pāda break of a unit of ≥16 syllables.
- **Pausal forms** (`vrtools/dcs.py`) follow the DCS case and number: no invented
  visarga on datives; -e restored for locatives and pronominal plurals; -āḥ for
  feminine gen./abl. and acc. pl.; t restored before a nasal; ś restored after t;
  genuine final o kept (भोः, vocatives).
- **Prefix स-** (`vrtools/seed.py`): an untagged Dharmamitra `sa` printed joined to
  the next word in the mūla is the prefix, not सः.
- **`padaccheda_status`** on every verse (`seed` / `reviewed` / null). Seeding
  scripts never touch a `reviewed` verse; `scripts/ingest_vulgate.py` refuses to
  run once any sarga holds reviewed or generated work.
- **Flags:** `data/meta/mula_flags.json` + `scripts/flag_mula.py` (9 `mula_suspect`,
  4 `not_mula`); `avagraha_mismatch` on 32 verses (set by `scripts/check_rejoin.py`).
  No mūla text and no verse count changed.
- **Site:** असमीक्षितम् under every machine split (seen in padaccheda mode); the
  topbar toggle is hidden on a sarga with no split at all (10 sargas). There is
  no per-verse toggle in this reader. Cache-bust `?v=2`.
- **No outside calls:** `scripts/seed_dharmamitra.py` raises unless
  `DHARMAMITRA_ALLOW_NETWORK=1`. The whole re-seed ran from `cache/dharmamitra/`
  and `sources/upstream/`.
- Seeds now: DCS 5,795, Dharmamitra 9,652, none 8,168; fix queue 10,287 lines.
  11 of the 17 errors found in the review's two samples are fixed; the other 6
  need a human reading (sarga review).

## Since Step 3 (2026-11-11)
- `stage-b` was merged to `main` and pushed on Aditya's word.
- Branch `corrections` (merged to `main` on Aditya's word): the reader shows
  `lines_corrected` with a संशोधितम् mark (tap: the Wikisource text); the checks and
  the seeding scripts read the corrected text (`vrtools.build.text_lines`); four
  approved corrections are stored in `data/meta/corrections.json` and applied by
  `scripts/apply_corrections.py` (VR.1.1.1, 1.1.9, 1.1.45, 1.1.100). `lines` is
  untouched; the mūla hashes still pass.

## Step 4 (pilot, Bāla sarga 1): stopped after verses 1–5
- Branch **`pilot-1-1`** (local, not pushed, not merged). `make check`: 279 tests,
  5 verses with padārtha, 0 errors.
- New tooling: `vrtools/padartha.py` (`check_layers`: one padārtha entry per pada
  whose analysis fits its form, qualifier agreement, anvaya and vyākhyā coverage,
  no Latin letters; `merge_verse`), `vrtools.seed.groups_for`,
  `scripts/check_layers.py` (read-only check of a draft), `scripts/merge_layers.py`.
  `make check` runs `check_layers` on every verse that has padārtha.
- Process used (CLAUDE.md §10.3): a generator sub-agent wrote
  `review/drafts/VR.1.1.json`; a separate reviewer sub-agent wrote
  `review/drafts/VR.1.1.review.json` (1 pass, 2 pass, 3 flag, 4 flag, 5 fix → pass
  after the one fix round); flagged points are in `review/queue.md`.
- Verses 1–5 are merged into `data/vr/1/001.json` with
  `padaccheda_status: reviewed`. **Waiting for Aditya's OK on verses 1–5** before
  verses 6–100, the sarga summary and the title. Do not start sarga 2.
- Open questions put to Aditya: gender of संयुग (पुं or नपुं, for the whole work);
  reading of एकप्रियदर्शनः; नञ्-compounds unhyphenated; whether CLAUDE.md §4/§5.6
  examples should be brought into line with the pilot (वाक्-विदाम्, the fourth च).
- `gen.model` is left empty in the data (no model identifier in pushed files).
- The reader's अध्ययनसाहाय्यम् panel (written in Stage A) has not yet been looked
  at in a browser with real data.

## Open, in order
1. Aditya's answer on verses 1–5; then verses 6–100 in batches of 20–40 with the
   same generator / reviewer process, `summary_sa`, the sarga title, 10% sample
   into `review/queue.md`, mark the sarga as pilot, STOP.
2. **Duplicate files:** something on this Mac creates copies named "… 2.py",
   "… 3.json" whenever git switches branch. Five were pushed to `main` by mistake
   (`tests/test_status 2.py`, `scripts/flag_mula 2.py`, `data/meta/mula_flags 2.json`,
   `docs/STAGE_B_BRIEF 2.md`, `docs/STAGE_B_REVIEW 2.md`); more sit untracked.
   Aditya has been asked whether to delete them. Until then: never `git add -A`;
   stage exact paths.
3. Owed: `docs/AYODHYA_PRESPLIT_OPTIONS.md` (one page, options only).

## Known limits of the Step 3 fixes (from the independent code review)
- At a pāda break a bare form can still pass where the mūla has an irregular
  hiatus for a visarga form (VR.6.83.29 `भूत`, VR.7.78.19 `श्वेत`, VR.4.53.7 `प्राज्ञ`,
  VR.6.35.13 `पक्ष`). They stay `seed`.
- A compound that runs over a line break inside a unit would be seeded without
  its hyphen and then cleared by `check_rejoin.py` (found by a probe; no stored
  verse is known to be affected). The 6 verses queued as `stored_padaccheda_fails`
  are source slips: a stray or doubled daṇḍa (VR.1.2.27, 1.2.28, 1.34.18, 7.8.5)
  and two typos (VR.2.57.11, 6.24.6).
- Untagged Dharmamitra words in -o are kept as -o (vocatives, अहो, गो-); a
  sandhied nominative that Dharmamitra failed to split would pass as -o.
- Where the mūla lacks an avagraha that the grammar expects, the right DCS split
  is rejected and a Dharmamitra split may be shown instead (e.g. VR.2.100.25);
  all such verses carry `avagraha_mismatch`.

## Rules that are easy to forget
- Never edit `lines`; corrections go in `lines_corrected` after approval (§12).
- No calls to Dharmamitra, IIT Kanpur or valmikiramayan.net.
- Never push or merge to `main` without Aditya's explicit word.

## Pipeline (all offline)
`apply_corrections.py` → `seed_dcs.py` → `seed_dharmamitra.py` → `crosscheck_seeds.py` →
`check_rejoin.py` → `flag_mula.py` → `make check` → `make site`. (`ingest_vulgate.py` and `crosswalk.py`
come first on a fresh build only.)
