# Stage C reviewer instructions (prompt_version stage-c-1)

You review a draft of generated layers for verses of the Vālmīki Rāmāyaṇa. You did not write
it and you see no reasoning of its writer: judge only the text. Project folder (quote it):
`~/Documents/Mac Mini Downloads/Ramayana website`.

## Read first
1. `CLAUDE.md` §4, **§5 in full (5.1–5.7)** and **§7**. These are the rules you apply.
2. `review/drafts/stage-c-examples.json`: five verses of the pilot (the quality bar).
3. The sarga file named in your task: `context_in_sa` and `working_notes.sarga_map`.
4. `data/meta/names.json`.
5. The verse text: `uv run python scripts/show_verses.py VR.<k>.<s> <first> <last>` (the
   machine padaccheda shown there is an unreviewed hint, not a reference).
6. The draft file named in your task, and run `uv run python scripts/check_layers.py <draft>`.

## Check every verse, word by word
- Padaccheda (§5.1, §5.7): every split and pausal form right; hyphens at every member
  boundary; no wrong vowel-sandhi or visarga restoration; daṇḍas as printed; a `rejoin_note`
  only where the printed text truly cannot be re-joined, and its reason right.
- Padārtha (§5.2, §5.7): stem, gender (Amarakośa, then Apte), case, number; verb analysis;
  gloss simpler than the word and in its case; vigraha correct; anvita right; ārṣa forms
  labelled; names per names.json (full identifier at first use in the sarga).
- Anvaya (§5.3): every pada once; supplied words in brackets; order; agreement.
- Vyākhyā (§5.4 rules 1–10, brief §7): grammar and agreement of every sentence; narrative
  first; only needed definitions; ≤2 इत्युक्ते, ≤1 इति आशयः; every significant pada bold;
  3–7 sentences; nothing added beyond the verse except connecting context; continuity with
  the previous verse and the sarga map; for a sentence across verses, says which verse
  completes it.
- Speaker and context note match the verse.

## Verdict per verse
- `pass`: no error (style preferences are not errors).
- `fix`: a definite error. Give the rule number and the exact correction in `fixes`
  (field, wrong text → right text), so the generator can apply it without guessing.
- `flag`: a point a human scholar must decide (a doubtful reading, a gender you cannot
  confirm, a genuine choice between two analyses). Say what to decide.

Write ONLY the file named in your task: `{"VR.k.s.n": {"verdict": "pass"|"fix"|"flag",
"rules": ["§5.x …"], "note": "…", "fixes": [ … ]}, …}`. Do not edit any other file. No
network access. Report in at most 8 lines: counts of pass / fix / flag, and the main faults.
