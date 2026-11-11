# Convention log (Stage C)

Cases that `CLAUDE.md` §5 does not cover. Each entry: the case, the closest existing rule
applied, and where. Raised with Aditya at the next checkpoint; nothing here changes §5.

| # | Date | Sarga / verse | Case | Rule applied |
|---|---|---|---|---|
| 1 | 2026-11-11 | VR.1.2.42 | यशस्करम्: a compound whose internal sandhi changes the first member's final (यशः → यशस्, Pāṇini 8.3.46-type). Neither `यशः-करम्` nor `यशस्-करम्` re-joins under the checker. | §5.1 "keep compound-internal sandhi inside a member": the word is kept whole (`यशस्करम्`); vigraha in the padārtha. |
| 2 | 2026-11-11 | VR.1.2.38 | One verse with two speakers (line 1 Brahmā's speech, lines 2–3 narration). The schema has one `speaker`. | §5.6/§4: `speaker` = the one who speaks (ब्रह्मा); the vyākhyā says where the speech ends. |
| 3 | 2026-11-11 | VR.1.2.43 | The poet addressing the listeners (निशामयध्वम्). | `speaker` = "कविः" (nearest to the pilot's naming of speakers by role). |
| 4 | 2026-11-11 | VR.1.2.42, 1.2.36 | मनोरम (मनः रमयति इति) split as an upapada compound: `मनः-रमैः`, `मनः-रमाम्`. | §5.7 "split upapada compounds at every member boundary". Raised because the word is very common and may be felt as one word. |
| 5 | 2026-11-11 | VR.1.2.9 | An ārṣa gender switch: masculine चरन्तम्, अनपायिनम् qualify neuter मिथुनम् (Amarakośa). The checker's agreement test cannot accept an `anvita` across genders, and a `fit_note` exempts only the word-list test. | No checker change. The two entries carry no `anvita`; the gloss states "(मिथुनस्य विशेषणम्; अत्र पुंलिङ्गम् आर्षम्)". The verse is flagged for the human reviewer (मिथुन पुं by Apte is the alternative). Open question for Aditya: should a declared note also exempt the agreement test? **Ruled (D17): मिथुन नपुं, qualifiers marked आर्षप्रयोगः, link in the gloss.** |
| 6 | 2026-11-11 | VR.1.3.24–38 | Checker bug (fixed test-first, CHECKER_VERSION 8): a printed line break without a closing daṇḍa was read as running text, so a pausal म् at the end of line 1 failed. A line break is a half-verse boundary: a pause may stand there. The checker now accepts either sandhi across the break or a pause at it (never where the line ends in a hyphen, मनोरमै- / स्तदा). | Reported at the next checkpoint (bug fix, `vrtools/sandhi.py`, three tests in `tests/test_rejoin.py`). |
| 7 | 2026-11-11 | VR.1.3.20 | Checker bug (fixed test-first, CHECKER_VERSION 9): every -oḥ before a vowel or voiced sound was treated like भोः (visarga dropped), so खरत्रिशिरसोरुत्थानं (-oḥ → -or, regular) failed and a wrong hiatus would have passed. Now only भोः, भगोः, अघोः drop it (8.3.17); any other -oḥ becomes -or. No stored split changed its result. | Reported at the next checkpoint (`vrtools/sandhi.py`, five tests). |
