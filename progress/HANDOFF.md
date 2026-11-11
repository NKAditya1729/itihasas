# Handoff — Stage C: building the whole Rāmāyaṇa (updated 2026-11-11)

**Read first:** the Stage C brief (Aditya's message; its rules are summarised here), `CLAUDE.md` §4, §5, §7, §10.3,
§12, then this file, `progress/state.json` and `progress/ORDER.md`. Resume from §0 of the brief: check the remote,
the caches, a clean `main`, `make check`; then take the next unticked sarga in `ORDER.md`. Never redo a ticked sarga.

## Where things stand
- **Done:** VR.1.1 (pilot; corrections 15, 29, 65, 84) and VR.1.2–1.5 (Stage C, all layers; rules D17, D18 from 1.3 on).
- **STOP:** checkpoint after Bāla 3–5 (brief §9): time and tokens reported, with savings proposals and a per-kāṇḍa
  projection. Waiting for Aditya's word before VR.1.6. After that, run without asking (brief §9), with an audit file
  every 10 sargas.
- Pending Aditya: the rule-A correction VR.1.4.6 (`review/mula_queue.md`); checker fixes v8, v9 (CONVENTION_LOG 6, 7).

## How a sarga is made (Stage C)
- Coordinator: preflight, the sarga map (`working_notes.sarga_map` in the sarga file), `context_in_sa`.
- Generators (≤20 verses each, `review/drafts/stage-c-generator.md`, examples in `review/drafts/stage-c-examples.json`)
  write `review/drafts/VR.k.s.bN.json` and self-check with `scripts/check_layers.py`.
- Separate reviewers (`review/drafts/stage-c-reviewer.md`) write `…bN.review.json`; one fix round, then a second pass
  (pass / flag). Combine to `review/drafts/VR.k.s.json` (+ `.review.json`, with title and summary_sa), then
  `scripts/merge_layers.py`, `make check`, queue entries, ORDER tick, LOG line, state.json, commit `vr(k.s): all layers
  [stage-c]`, merge to `main`, push. At most three sub-agents at a time.
- Hand-kept files: `data/meta/names.json`, `docs/CONVENTION_LOG.md` (cases §5 does not cover; raise at checkpoints),
  `review/mula_queue.md` (Class A/B mūla), `review/linga_queue.md`, `review/queue.md`.

## Rules that are easy to forget
- Never edit `lines`. Class A corrections only under all four conditions of brief §8; otherwise Class B (flag + queue).
- No calls to Dharmamitra, IIT Kanpur, valmikiramayan.net or any other service; the only network use is `git push`.
- No changes to the design, schema, checker or pipeline beyond a test-first bug fix (report it).
- Never `git add -A` here; " 2"/" 3" duplicates are ignored, 5 tracked ones remain.

---

# Handoff — Stage B: pilot of Bāla sarga 1 complete, waiting for review (2026-11-11)

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

## Step 4 (pilot, Bāla sarga 1): COMPLETE (2026-11-11)
- **All 100 verses of VR.1.1 have every layer** (reviewed padaccheda, padārtha,
  anvaya, expository vyākhyā per CLAUDE.md §5.4), the sarga title and
  `summary_sa`; the sarga is marked `pilot`. Merged to `main` and live on
  Aditya's word ("complete the first 100 verses and go live").
- `make check`: 296 tests; 100 verses with padārtha; 11 declared re-join
  exceptions; 0 errors.
- Process: five generator sub-agents (drafts in `review/drafts/VR.1.1*.json`),
  five separate reviewer sub-agents (`*.review.json`), one fix round per batch and
  a final review pass. Final verdicts: 74 pass, 26 flag. Flags, exceptions, the
  doubtful source readings and a 10% sample are in `review/queue.md`.
- **STOP here for Aditya's and Swamiji's review. Do not start sarga 2.**

## Open, in order
1. **Aditya's decisions** (all listed in `review/queue.md` §1): corrections for
   VR.1.1.15, 29, 65, 84, 85 and the stray spaces in 17, 43, 57 (none applied;
   all flagged `mula_suspect`); whether padārtha identifiers may go beyond what
   sarga 1 tells; the duplicate "… 2" / "… 3" files (12 listed; nothing deleted;
   never `git add -A` in this folder).
2. Swamiji's review of the 26 flagged verses and the kośa genders.
3. After that: package §5 and §7 as the project skill `ramayana-content-review`
   (CLAUDE.md §10.3), then sarga 2 (its `context_in_sa` = this sarga's
   `summary_sa` + the vyākhyā of verses 98–100).
4. Owed: `docs/AYODHYA_PRESPLIT_OPTIONS.md` (one page, options only).

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
