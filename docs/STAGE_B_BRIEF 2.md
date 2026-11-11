# Stage B brief: review, then pilot (Fable 5.2, high effort)

> Saved 2026-11-11 from Aditya's message. One correction, made on his
> instruction the same day: the project folder is
> `~/Documents/Mac Mini Downloads/Ramayana website`, not
> `~/Documents/Ramayana website` as first written. The text below uses the
> corrected path; nothing else is changed.

## 0. Where to work (do this before anything else)
The project folder is: `~/Documents/Mac Mini Downloads/Ramayana website`
(the folder names contain spaces, so quote the path).

1. `cd "$HOME/Documents/Mac Mini Downloads/Ramayana website"`
2. Prove it is the right folder. All four must be true:
   - `git remote -v` shows `NKAditya1729/itihasas`
   - `CLAUDE.md` exists at the top level
   - `docs/STAGE_A_REPORT.md` exists
   - the folder `cache/dharmamitra/` exists (it is git-ignored and
     exists only in the original working copy)
3. If the folder is missing or any check fails: STOP and tell me what
   you found. You may run one search, for folders named
   "Ramayana website" under my home folder, and report the paths.
   Do not pick one yourself. Do not clone a fresh copy from GitHub.
   Do not create a new folder.
4. Once confirmed, every command and every file you read or write
   stays inside this folder. Do not open, search or change anything
   else on this Mac (not `sarala-vedanta`, not `vedantic-archive`,
   not other projects).
5. Run `git status` and `make check`. Expected: a clean tree on
   `main`, about 140 tests passing, 645 sargas, 23,589 verses. If
   anything differs, report it and STOP.

## 1. What this project is
A static website, इतिहासाः, for learning Sanskrit through the Valmiki
Ramayana. Every verse will have: the mūla, a padaccheda (sandhi-split)
toggle, padārtha in simple Sanskrit, anvaya, and a simple-Sanskrit
explanation that reuses the verse's own words. No English for now.
- Live site: https://nkaditya1729.github.io/itihasas/ramayanam/
- Repo: https://github.com/NKAditya1729/itihasas (public; every push
  to `main` redeploys the site)
- Done so far (Stage A, by Opus 5.5): the full text from Sanskrit
  Wikisource, the reader site, and machine-seeded padaccheda for
  15,311 verses. Nothing else has been generated.
- Your job now: review Stage A, fix what I approve, then write the
  full pilot for Bāla sarga 1.

## 2. Read these, in this order, and nothing else yet
1. `CLAUDE.md` (the project rules; §5 writing rules, §7 checks,
   §10 skills)
2. `progress/HANDOFF.md`
3. `docs/STAGE_A_REPORT.md`
4. `docs/DECISIONS.md`
5. `docs/EXISTING_DESIGN.md` and `docs/SKILLS.md`
Then save this brief as `docs/STAGE_B_BRIEF.md` and send me a summary
of at most 12 lines: the folder you confirmed, where the project
stands, and your plan for Step 2. Change nothing else before I reply.

## 3. How to work with me
I am on my phone, away from the Mac.
- Keep every message short. Put the conclusion first.
- When you need a decision, ask ONE question with 2 to 4 numbered
  options and your recommendation. Then wait.
- Never decide these yourself; always ask: anything about the mūla
  text, which source to trust, the site's look, file or folder
  layout, deleting or renaming anything, installing new tools,
  calling any outside service, merging or pushing to `main`.
- If this brief and `CLAUDE.md` disagree, this brief wins. If
  neither covers a situation, STOP and ask. Do not improvise.
- Do only the step you are on. Do not start the next step early,
  and do not "tidy up" things nobody asked for.
- End every step with three lines: Done / Please check / Next.
  Update `progress/HANDOFF.md` at every STOP.

## 4. Hard rules
- Branch: create `stage-b` from `main` and work only there. Commit
  often. Push the branch if you like. Never push or merge to `main`
  without my explicit word.
- Never edit the mūla. If a verse looks wrong (example: the space in
  तपः स्वाध्यायनिरतं, VR.1.1.1), add the flag `mula_suspect` with a
  note and leave the text alone.
- No new calls to the Dharmamitra service. Its terms are not
  confirmed. Use only what is in `cache/dharmamitra/`.
- No fetching of IIT Kanpur or valmikiramayan.net pages in this
  session.
- Load skills per `CLAUDE.md` §10, only when a step needs them.

## 5. Plan change (replaces CLAUDE.md §11 Stage B and C)
An outside review of the Stage A samples found that passing the
re-join check does not mean a split is correct. So padaccheda will
NOT be fixed for the whole epic first. It is finalised sarga by
sarga, together with padārtha, anvaya and vyākhyā, with the machine
seeds used only as hints. Update `CLAUDE.md` §11 to say this.

Wrong splits that currently pass (from the report's own samples):
- VR.1.60.12 सक्रोधः shown as सः क्रोधः (should be स-क्रोधः)
- VR.6.70.22 सविस्फुलिङ्गं सज्वालं shown as सः विस्फुलिङ्गम् सः ज्वालम्
- VR.7.36.8 भो shown as भः (should be भोः)
- VR.2.24.34 आनृण्यतां shown as आनृण्य ताम् (one word)
- VR.3.24.6 नोऽभयं shown as नो भयम् (should be नः अभयम्)
- VR.6.104.24 प्रशस्य-एनम्: a hyphen between two separate words
Confirm each of these yourself before relying on it.

## 6. Step 2: review (read-only; write only the review file)
Write `docs/STAGE_B_REVIEW.md` with three lists: must-fix,
should-fix, optional. Each item: what is wrong, one example, the
proposed fix, the files touched. Cover:
a. The re-join checker, `vrtools/sandhi.py`. Probe it with wrong
   splits of your own. Judge the four loosenesses at the end of
   report §4, especially ignored avagraha and स versus सः.
b. True error rate. Take 100 random passing verses from each seed
   source (DCS, Dharmamitra), with a fixed random seed so it can be
   repeated. Judge each split yourself. Report the percentage wrong
   and the error types.
c. The hyphen logic for DCS seeds, and every Dharmamitra verse where
   a standalone सः may really be the prefix स-.
d. The crosswalk thresholds, on a sample of 50 verses.
e. The mūla: the 71 verses with stray characters, and the metre
   failures outside Ayodhyā 48–88. List them with a proposed
   handling. Do not fix them.
STOP. Send me the top five must-fix items in the message and wait.

## 7. Step 3: only after I approve
a. Apply only the items I approved, test-first.
b. Site labelling: add a per-verse `padaccheda_status` (`seed` or
   `reviewed`). Show an असमीक्षितम् mark on seed-only splits, using
   existing styles. Hide the Padaccheda toggle on verses with no
   split.
c. Run `make check` and build the site locally.
STOP. Tell me what changed and wait for my word to merge to `main`.

## 8. Step 4: pilot, Bāla sarga 1 only (100 verses)
State now: 74 verses have a seed split (29 with no compound marks,
17 disputed) and 26 have none.
a. Finalise the padaccheda for all 100 verses by `CLAUDE.md` §5.1.
b. Write padārtha, anvaya and sarala vyākhyā by §5.2 to §5.4, then
   the sarga summary (§5.5) and a sarga title.
c. Generator and reviewer are separate sub-agents (§10.3). One fix
   round; a second failure becomes a flag for me.
d. Add one automated check: every pada in the padaccheda has a
   padārtha entry whose grammatical analysis fits its form. This is
   the check that catches errors like सः क्रोधः.
e. Run `make check`. Record reviewer verdicts. Put flagged verses in
   `review/queue.md`.
f. Show me verses 1 to 5 in the message first. After my OK, finish
   the sarga, mark it as pilot, and STOP for my review and
   Swamiji's. Do not start sarga 2.

## 9. Not in this session
- Ayodhyā 48–88 (the half-split sargas): write only a one-page
  options note, `docs/AYODHYA_PRESPLIT_OPTIONS.md`.
- Fixing mūla typos, search, English layers, the Mahābhārata, any
  redesign of the site.
