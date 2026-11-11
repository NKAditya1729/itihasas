# Stage C generator instructions (prompt_version stage-c-1)

You write the padaccheda, padārtha, anvaya, sarala vyākhyā and speaker for a batch of verses
of the Vālmīki Rāmāyaṇa, to the standard of the pilot sarga (VR.1.1). Project folder (quote
it, it has spaces): `~/Documents/Mac Mini Downloads/Ramayana website`.

## Read first (all of it)
1. `CLAUDE.md` §4 (verse object) and **§5 in full (5.1–5.7: these are law)**, and §7.4–7.5.
2. `review/drafts/stage-c-examples.json`: five pilot verses with every layer (two list-style,
   three narrative). Match their register, length and format. Copy no sentences. They predate §5.4 rules 11–13:
   where they use more इत्युक्ते or end on a gloss sentence, the rules win.
3. The sarga file `data/vr/<k>/<sss>.json`: its `context_in_sa` (story so far) and
   `working_notes.sarga_map` (speaker, addressee, event and sentence grouping for every verse,
   written by the coordinator). Follow the map; if you think it is wrong, say so in `note`.
4. `data/meta/names.json`: identifiers for names (full identifier at a name's first use in the
   sarga, the bare name afterwards; reuse these, add new ones in your report).
5. For register only: a few `"sd"` entries of `cache/ashtadhyayi/sutrartha.txt` (the style of
   Sanskrit explanation the vyākhyā follows: separate words, real clauses, terms defined in
   running prose). Copy nothing from it.
6. The verse text: `uv run python scripts/show_verses.py VR.<k>.<s> <first> <last>`. The text
   shown is the text you explain (an approved correction where one exists). The machine
   padaccheda shown there is a **hint only**: check every word yourself.

## Rules that are easy to miss
- Never change the verse text. The padaccheda must re-join to it (§5.1, §7.3), with the same
  `।` / `॥` positions (a stray `। ॥` is kept as printed). If the printed text cannot be
  re-joined from a correct split (two words left unjoined, an impossible sandhi, a stray
  letter), give the correct split and a `rejoin_note` on the verse saying exactly why.
- Hyphens per §5.7 (every member boundary, each member pausal; नञ् not split; prefixes that are
  not words not split; proper names, fixed terms, taddhitas whole).
- Padārtha: one entry per pada in verse order; gloss simpler than the word, in its own case;
  vigraha for every compound; verbs with dhatu, upasarga, lakara, purusha, vacana; indeclinables
  `"avyaya": true`; `anvita` for every qualifier; gender by the Amarakośa first, then Apte. If
  you are unsure of a gender, say so in your report (the word goes to the gender queue).
- An epic (ārṣa) form is analysed as the form requires and labelled `आर्षप्रयोगः` / `आर्षं रूपम्`
  in the gloss, as the pilot does. If the word list rejects a correct form, add `fit_note`.
- Anvaya: every pada exactly once; anything supplied in round brackets; vocatives first.
- Vyākhyā (§5.4, rules 1–13): narrate the event first; define only what a learner would not
  know; every significant pada in `**bold**`; 3–7 sentences; words kept separate (no external
  sandhi, no avagraha); nothing beyond the verse except connecting context.
  - The caps (two इत्युक्ते, one इति आशयः) are **limits, not targets**: aim for **under one
    इत्युक्ते per verse on average** across your batch. Explain a word where it is used, inside
    the story sentence; **never end with stand-alone gloss sentences** ("X इत्युक्ते Y ।" at the end).
  - **No remarks about the verse itself** in the vyākhyā: not its metre, not "this verse
    completes the sentence", not "अस्मिन् श्लोके …". Where a sentence spans verses (see the map),
    at most one short linking clause (e.g. "… इति सः अग्रे वदति"); the anvaya marks the link in
    brackets ("(… इति अग्रिमेण श्लोकेन सम्बन्धः)"). Each verse keeps its own padārtha.
  - **Agreement:** every finite verb and participle in the vyākhyā and anvaya agrees with its
    subject in number and gender; check duals (तौ … उच्येते, not उच्यते).
- Long metres: same layers. The metre is shown by the site; do not mention it in the vyākhyā.
- `speaker`: who speaks the verse (null for plain narration), as in the map.
- `context_note_sa`: one short sentence of what happens in the verse.
- No English in any Sanskrit field. No network access of any kind.

## Output
Write ONLY the file named in your task: `{"sarga": "VR.k.s", "gen": {"model": "claude-opus-5-5 (Opus 5.5), high effort", "date": "<today>", "prompt_version": "stage-c-1", "process": "generator and reviewer sub-agents, one fix round; CLAUDE.md §5.4 rules 11–13 (D18)"}, "verses": [ {"id", "padaccheda_lines", "padartha", "anvaya", "vyakhya_sa", "speaker", "context_note_sa", optional "rejoin_note"} … ]}`.
Then run `uv run python scripts/check_layers.py <your file>` and fix every error until it
prints OK for every verse (a verse listed with forms "not in the word list" is fine). Do not
edit any other file. Report back in at most 15 lines: verses written, checker result, each
rejoin_note / fit_note, new name identifiers, genders you were unsure of, and anything in the
text or the map you think is wrong.
