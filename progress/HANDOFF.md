# Handoff — end of Stage A (2026-11-11)

Stage A is complete and stopped at Gate A. Read `docs/STAGE_A_REPORT.md` first.

Next: **Stage B** (fresh session, Fable 5.2, CLAUDE.md §11): review the repo as a reviewer, write `docs/STAGE_B_REVIEW.md` (must-fix / should-fix / optional), apply must-fix only after Aditya approves, then Phase 2b (resolve `queue/padaccheda_fix.jsonl` by §5.1).

State:
- Data: `data/vr/{k}/{sss}.json` (645 files), meta in `data/meta/`, fix queue in `queue/padaccheda_fix.jsonl` (10,609 lines).
- Pipeline (all idempotent): ingest_vulgate → crosswalk → seed_dcs → seed_dharmamitra → crosscheck_seeds → check_rejoin; `make check`; `make site` → `site/` (git-ignored).
- Caches: `cache/wikisource/` (committed, the pinned base text), `cache/dharmamitra/` (git-ignored; needed to rerun without calling the API), `cache/vidyut-data/` (git-ignored; `uv run python -c "import vidyut; vidyut.download_data('cache/vidyut-data')"`), `sources/upstream/` (git-ignored clones; commits in `sources/sources.json`).
- Local preview: launch config `ramayana-site` (port 4180) serves `site/`.
- Not done, waiting for Aditya: create the separate GitHub repo (D6) and deploy; confirm Dharmamitra's terms before publishing its output.
