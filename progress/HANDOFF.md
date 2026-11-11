# Handoff — Stage B, stopped after Step 3 (2026-11-11)

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

## Open, in order
1. **Merge to `main`**: only on Aditya's explicit word.
2. **Three proposed mūla corrections** (not applied; Aditya is checking a printed
   edition): VR.1.1.9 श्रीमाञ्छ्त्रु- → श्रीमाञ्छत्रु-; VR.1.1.45 -वासीनाम् → -वासिनाम्;
   VR.1.1.100 line 2 `त् क्षत्रियो` → `स्यात् क्षत्रियो`. All three pass the metre when
   corrected. VR.1.1.1 (space inside a compound) is flagged only.
3. **Before the first correction is applied** two things must be built
   (CLAUDE.md §12.5–§12.6): the checks must read `lines_corrected` when present
   (`scripts/check_rejoin.py`, `scripts/validate.py`, seed scripts), and the
   reader must show the corrected text with a mark and the original on tap. The
   look of that mark is Aditya's decision.
4. Step 4: pilot, Bāla sarga 1 (now 75 seeds: 46 DCS, 29 Dharmamitra; 25 without).
5. Owed: `docs/AYODHYA_PRESPLIT_OPTIONS.md` (one page, options only).

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
`seed_dcs.py` → `seed_dharmamitra.py` → `crosscheck_seeds.py` → `check_rejoin.py` →
`flag_mula.py` → `make check` → `make site`. (`ingest_vulgate.py` and `crosswalk.py`
come first on a fresh build only.)
