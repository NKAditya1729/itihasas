# Handoff — Stage B, stopped after Step 2 (2026-11-11)

**Read first:** `docs/STAGE_B_BRIEF.md` (the working instructions; it overrides
CLAUDE.md §11), then `docs/STAGE_B_REVIEW.md`.

- Project folder: `~/Documents/Mac Mini Downloads/Ramayana website`
- Repository: https://github.com/NKAditya1729/itihasas · branch **`stage-b`**
  (local only, not pushed; `main` is untouched and is what the live site serves)
- Live site: https://nkaditya1729.github.io/itihasas/ramayanam/

## Where things stand
- Step 0–1 done: folder verified, documents read, brief saved.
- **Step 2 done (read-only review).** `docs/STAGE_B_REVIEW.md` holds must-fix
  M1–M5, should-fix S1–S7, optional O1–O5, and appendices with the verse ids.
  No code, data or mūla was changed. `make check`: 140 passed, 23,615 verses,
  0 errors.
- **Waiting for Aditya** to say which review items are approved.

## Next (only after approval)
- Step 3: apply the approved items test-first; add `padaccheda_status` and the
  असमीक्षितम् mark; hide the toggle where there is no split; update CLAUDE.md
  §11 (brief §5); `make check`; build the site locally; STOP before any merge.
- Step 4: pilot, Bāla sarga 1 only. **Open question for the pilot:** VR.1.1.100
  has lost letters on Wikisource (`त् क्षत्रियो…`); VR.1.1.9, 1.1.45 and 1.1.1
  have typos. Aditya must rule on how to treat them before those verses are
  explained.
- Also owed: `docs/AYODHYA_PRESPLIT_OPTIONS.md` (one page, options only).

## Rules that are easy to forget
- Never edit the mūla; flag `mula_suspect` instead.
- No calls to Dharmamitra, IIT Kanpur or valmikiramayan.net. Re-seeding uses
  `cache/dharmamitra/` and `sources/upstream/` only (both git-ignored).
- Never push or merge to `main` without Aditya's explicit word.
- The review's measurements were run from memory; no script files were added.
  The sample draw is reproducible (seed 20261111, review Appendix A).

## State of the data (unchanged from Stage A)
- `data/vr/{k}/{sss}.json` (645 files), meta in `data/meta/`, fix queue in
  `queue/padaccheda_fix.jsonl` (10,609 lines).
- Pipeline: ingest_vulgate → crosswalk → seed_dcs → seed_dharmamitra →
  crosscheck_seeds → check_rejoin; `make check`; `make site` → `site/`.
- Local preview: launch config `ramayana-site` (port 4180) serves `site/`.
