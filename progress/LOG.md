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
