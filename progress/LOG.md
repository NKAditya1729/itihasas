# Progress log

## 2026-11-11 — Stage A (Opus 5.5)

- Phase 0: found the hub (`sarala-vedanta`), the builder (`vedanta-pathashala-antigravity`), and the light verse reader (`vishnu-sahasranama/`) to reuse. Wrote `docs/EXISTING_DESIGN.md`, `docs/SKILLS.md`.
- Found that Ramayana_Book's Sanskrit is an older half-split copy (~43% of verses); live Wikisource is saṃhitā except 41 Ayodhyā sargas. Fetched all 645 sarga pages (pinned revisions, `cache/wikisource/`).
- D1–D7 answered by Aditya (`docs/DECISIONS.md`).
- Phase 1: parser/normaliser/metre/record builder (TDD), ingest → 645 sargas, 23,589 verses + 26 prakṣipta verses. vidyut.chandas lacks Anuṣṭup, so a śloka check was added on top of its syllable weights.
- Site: static reader on the Viṣṇusahasranāma design; previewed locally (desktop, phone width, IAST, path shells). Not deployed: the new repo waits for Aditya's go-ahead.
- Phase 2a: sandhi joiner + re-join checker (TDD, positive and negative cases), crosswalk (own sarga map; hms-cap's map does not fit Wikisource's sarga boundaries), DCS seeding (pausal restoration, neighbour windows), Dharmamitra seeding (API changed; called directly with IAST).
- Independent review of the checker found it too loose (5 issues) plus seeding bugs; all fixed test-first, checker now version 4, every seed redone.
- Final Stage A numbers: 15,311 / 23,615 verses with padaccheda (DCS 5,778, Dharmamitra 9,533), 10,609 queued. `make check` clean (138 tests). Report: `docs/STAGE_A_REPORT.md`. **Stopped at Gate A.**

## 2026-11-11 — Stage C (claude-opus-5-5, high effort; prompt stage-c-1)

- Start: duplicates moved to the Trash (7 untracked " 2"/" 3" files) and an ignore rule added; 5 tracked duplicates remain (not touched).
- VR.1.1: approved corrections 15, 29, 65, 84 applied (`lines_corrected`); layers of the four verses redone and reviewed (4 pass).
- Site: the pilot note replaced by a standing note on every generated sarga (machine-written, awaiting scholarly review); a ✓ सम्पूर्णः mark on finished sargas in the sarga index; cache-bust v5; `noindex` kept.
- New files: `progress/ORDER.md`, `data/meta/names.json`, `docs/CONVENTION_LOG.md`, `review/mula_queue.md`, `review/linga_queue.md`.
- **VR.1.2** (43 verses): sarga map by the coordinator; 3 generator batches (1–14, 15–30, 31–43) and 3 separate reviewers; one fix round. First pass 33 pass / 9 fix / 1 flag; final 41 pass / 2 flag (9 मिथुन gender; 23 स्वयं प्रभुः). 3 re-join exceptions (26 च ऋषये unjoined, 38 stray र्, 43 two slips), 2 fit_notes. Class B mūla: 27, 28, 38, 43 (flagged, not corrected). `make check`: 281 tests, 0 errors. Time: about 20 minutes wall clock from the first generator to the merge (about 50 with preparation). Sub-agent tokens for VR.1.2: about 1.21 million (≈ 28,000 per verse; generators ≈ 632k, reviewers incl. second passes ≈ 580k), plus the coordinator's own.
- VR.1.2 rulings applied (D17); CLAUDE.md §5.4 rules 11–13 added (D18), generator and reviewer instructions updated.
- Checker fixes, test-first: v8 (a printed line break without a daṇḍa may be a pause), v9 (-oḥ → -or except भोः); `rejoin_parts` so the Padaccheda groups follow the same units. No stored split changed its result.
- VR.1.4.6: rule-A correction (वेदोपबृंह्मण → वेदोपबृह्मण, Critical Edition 1.4.5), pending Aditya.
- **VR.1.3** (39 verses): 2 batches (1–20, 21–39), 2 reviewers, one fix round. First pass 30 pass / 6 fix / 3 flag; final 32 pass / 7 flag (4 of them sentences changed in the fix round). 0 re-join exceptions (the v7 pāda-break hiatus and the v8 pause cover 18, 26, 29), 0 fit_notes. Time: about 23 minutes from preflight to merge. Sub-agent tokens: about 755k (≈ 19,400 per verse; generators 414k, reviewers 340k).
- **VR.1.4** (36 verses): 3 batches (1–13, 14–25, 26–36), 3 reviewers, one fix round. First pass 24 pass / 10 fix / 2 flag; final 34 pass / 2 flag (35, 36: readings). 0 re-join exceptions, 4 fit_notes. Time: about 19 minutes from the first generator to the merge. Sub-agent tokens: about 1.09 million (≈ 30,300 per verse; generators 595k, reviewers 496k).
- **VR.1.5** (23 verses): 2 batches (1–8, 9–23), 2 reviewers, one fix round. First pass 17 pass / 6 fix; final 22 pass / 1 flag (VR.1.5.2 परितः, found by the other batch's reviewer). 0 re-join exceptions, 1 fit_note. Time: about 21 minutes. Sub-agent tokens: about 705k (≈ 30,600 per verse; generators 393k, reviewers 311k).
- **Checkpoint after Bāla 3–5 (brief §9):** measured 141 verses (1.2–1.5) for ≈ 3.76 million sub-agent tokens (≈ 26,700 per verse) and ≈ 0.65 minutes of wall clock per verse including coordination. Per agent the cost is mostly fixed (≈ 140k tokens of reading before the first verse); see the report to Aditya for savings and the per-kāṇḍa projection. STOP.
