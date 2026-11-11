# Stage B review of Stage A (Step 2 of `docs/STAGE_B_BRIEF.md`)

Fable 5.2, 2026-11-11. Branch `stage-b`. Read-only review: no code, data or
mūla was changed. Every number below was measured on the repository as it
stands at commit `65512c4` (+ the brief), with scripts run from memory (no
files written). `make check` before the review: 140 tests passed, 23,615
verses, 0 errors.

## Summary

1. **Passing the re-join check does not mean a split is right.** In two
   fixed-seed samples of 100 passing verses each, **8% of DCS seeds and 9% of
   Dharmamitra seeds have a wrong letter or a wrong word boundary** (95%
   interval roughly 4–16% each). That is about **1,300 of the 15,311 seeded
   verses**. On top of that, about 9 in 10 Dharmamitra seeds show compounds
   with spaces instead of hyphens (already flagged), and 6% of DCS seeds have
   a hyphen fault only.
2. All six wrong splits named in the brief are confirmed (§1).
3. The checker is a sound *phonological* test and nothing more. It cannot
   tell a word from a non-word, a hyphen from a space, or स- from सः, and it
   ignores avagraha in both directions (§2).
4. Most of the errors fall into a few mechanical classes that can be fixed or
   flagged from data already on disk, with no outside calls (§3, must-fix).
5. The mūla has more source damage than Stage A reported, **including in the
   pilot sarga**: VR.1.1.100 has lost letters on Wikisource, and four
   commentary sentences are stored as verses in Ayodhyā (§6).
6. The crosswalk thresholds are sound: 43 of 43 sampled links are right (§5).

## Must-fix

Each item: what is wrong · one example · proposed fix · files touched.

### M1. The site shows machine seeds as if they were final
- **Wrong:** 15,311 seed splits are shown with no mark; about 1,300 contain a
  real error (§4) and 9,533 have no compound marks.
- **Example:** VR.1.60.12 स्रुवमुद्यम्य सक्रोधः is shown as `सः क्रोधः`.
- **Fix:** as the brief's Step 3b: per-verse `padaccheda_status` (`seed` /
  `reviewed`), an असमीक्षितम् mark on seed-only splits using existing styles,
  no toggle on verses without a split. Rewrite `CLAUDE.md` §11 (brief §5).
- **Files:** `schema/sarga.schema.json`, `scripts/validate.py`,
  `vrtools/build.py`, `web/` reader script and CSS (additive, existing
  tokens), `tests/test_build.py`, `tests/test_site.py`, `CLAUDE.md`,
  `data/vr/*/*.json` (new field only).

### M2. The checker ignores avagraha (looseness a)
- **Wrong:** `norm` deletes ऽ, so an elided अ can be dropped or invented.
  All six probes pass: `ततो धर्मः` ← `ततः अधर्मः`, `वने भयम्` ← `वने अभयम्`,
  `रामोऽब्रवीत्` ← `रामः ब्रवीत्`.
- **Measured:** with avagraha made significant, **39 passing seeds fail**
  (Appendix B). 9 have ऽ in the mūla but no अ in the split; several invert
  the meaning. 30 elide an अ where the mūla prints no ऽ: 2 are wrong splits,
  the rest are mūla spellings without ऽ (उपयातोसि, रक्षोधिपतेः).
- **Example:** VR.1.35.4 शुभजलोऽगाधः → `शुभ-जलः गाधः` (should be अगाधः);
  VR.6.69.78 ते स्वस्थाः → `ते अस्वस्थाः`; VR.6.83.22 ऽधर्मः → `धर्मः`.
  VR.3.24.6 नोऽभयं → `नो भयम्`: here DCS follows the Critical Edition
  reading (नो भयम्, "danger has come"), so either the split or the printed ऽ
  is wrong. The verse needs `mula_suspect`, not a silent pass.
- **Fix:** the joiner emits `'` wherever it elides अ after ए/ओ/अः, and `norm`
  keeps `'` in the mūla. Optional ऽ / ऽऽ after a long ā from a+a (तथाऽऽतिथ्यं)
  is accepted. Inside a compound (hyphen) the ऽ stays optional. A mūla that
  lacks an expected ऽ fails the gate and gets `mula_suspect` (the split is
  then reviewed by hand; the mūla is not touched).
- **Files:** `vrtools/sandhi.py`, `tests/test_rejoin.py`; checker version 5;
  re-seed from caches (`scripts/seed_dcs.py`, `scripts/seed_dharmamitra.py`,
  `scripts/check_rejoin.py`), which rewrites `data/vr`, `data/meta`, `queue/`.

### M3. Dharmamitra's prefix स- is always read as the pronoun सः (looseness "स versus सः")
- **Wrong:** Dharmamitra returns `sa` for both. `pausal_candidates` turns
  every one into सः, and सः + consonant re-joins to स, so the check passes.
  5 of the 9 errors in the Dharmamitra sample are this.
- **Measured:** 1,801 standalone सः in 1,629 Dharmamitra seeds. In **395
  verses** (Appendix C) the mūla prints स joined to a following
  consonant-initial word with no space (सलक्ष्मणम्, ससैन्यः, सलीलम्), which
  is how the prefix is printed; the pronoun is printed apart (`स ददर्श`). All
  12 I spot-checked are the prefix.
- **Example:** VR.6.20.12 देवैरपि सगन्धर्वैः → `देवैः अपि सः गन्धर्वैः`.
- **Fix:** when seeding from Dharmamitra, a `sa` that falls inside one
  unspaced mūla token before a consonant becomes the compound member `स-`.
  A `sa` printed apart stays सः. Uttara-kāṇḍa lines printed with few spaces
  are the risk; the verses stay `seed` status either way.
- **Files:** `vrtools/seed.py`, `scripts/seed_dharmamitra.py`,
  `tests/test_seed.py`, `tests/test_dharmamitra.py`; re-seed from
  `cache/dharmamitra/` only (no API call).

### M4. Wrong pausal forms chosen for DCS and Dharmamitra words (loosenesses b and d)
The search may pick any listed alternative that re-joins, and the list is
wrong in five ways. About **370 verses** (Appendix D); 7 of the 8 DCS sample
errors are these.
| Class | Verses | Example |
|---|---|---|
| Visarga added against the DCS morphology, to bridge a hiatus at a pāda break | 91 | VR.1.67.1 रामाय इति → `रामायः इति`; VR.1.35.21 `अप्रतिरूपायः` |
| Feminine genitive/ablative left without visarga | 80 | VR.5.13.8 आर्याया हृदयम् → `आर्याया` (आर्यायाः) |
| Final त् left as न् before a nasal | 129 | VR.3.43.38 यन्मां → `यन् माम्` (यत्); VR.3.56.11 `पातयेन्` |
| श् left as छ् after त् | 32 | VR.1.57.7 `तत् छ्रुत्वा` (श्रुत्वा) |
| Genuine final ओ turned into अः | 46 + bug | VR.7.36.8 भो → `भः`; `महाबाहो` → `महाबाहः`, `विष्णो` → `विष्णः` |
- **Cause of the last row:** `GENUINE_O` in `vrtools/dcs.py` is written
  `"bho", "atho"`, but the forms are SLP1 (`Bo`, `aTo`), so the entries never
  match; Dharmamitra words carry no tags, so vocatives in -ओ are not
  protected either.
- **Fix:** (1) allow "no sandhi" at one pāda break inside a printed line as a
  junction outcome, and stop offering form + ḥ unless the DCS case/number
  allows it; (2) prefer -āḥ for feminine case 5/6 singular; (3) for a final
  n before a nasal offer the -t form first when the lemma is not n-final
  (verbs, तद्/यद्/एतद्, -चित्); (4) restore श् after a restored त्;
  (5) write `GENUINE_O` in SLP1 and keep a Dharmamitra final -o when the
  joined text still matches.
- **Files:** `vrtools/dcs.py`, `vrtools/sandhi.py`, `vrtools/seed.py`,
  `tests/test_seed.py`, `tests/test_rejoin.py`; re-seed from caches.
- **Note:** the report (§7.5) rejected the pāda-break pause because it would
  rescue few *failures*. The cost is on the other side: without it, 91 seeds
  *pass* with an invented visarga.

### M5. Non-verse text and damaged text inside the mūla (flags only; your decision)
Nothing here is a parser fault; Wikisource has it this way. No text should be
changed without your word. Proposed flags only.
| What | Where | Proposed handling |
|---|---|---|
| A commentary sentence numbered as a verse | VR.2.90.5 `वसिष्ठसाहचर्य्यादिति भावः`, VR.2.93.5, VR.2.97.27, VR.2.106.15 | flag `not_mula`; you decide whether they leave the verse list (this changes the count 23,589) |
| Page heading and reciter credit inside the first verse | VR.6.44.1 (`०४४ इन्द्रजिता…`, `(श्रीराम-…वचनम्)`) | flag `mula_suspect`; you decide whether the parser may move such lines to `source_heading` |
| Two verses stored as one (source marker without closing ॥) | VR.1.26.4, VR.1.31.14, VR.3.73.41 | flag `mula_suspect`; you decide whether the parser may split at `॥१-२६-१३` |
| **Pilot sarga:** letters lost | VR.1.1.100 line 2 `त् क्षत्रियो भूमिपतित्वमीयात्` (the start of the pāda, स्या-, is missing on Wikisource) | flag `mula_suspect`; **the pilot needs your ruling before this verse can be explained** |
| **Pilot sarga:** typos | VR.1.1.9 `श्रीमाञ्छ्त्रुनिबर्हणः`; VR.1.1.45 `दण्डकारण्यवासीनाम्`; VR.1.1.1 `तपः स्वाध्यायनिरतं` (space inside a compound) | flag `mula_suspect` with a note |
- **Files:** `data/vr/…` (flags and notes only), `schema/sarga.schema.json`
  (two new flag names), `scripts/validate.py`.

## Should-fix

### S1. Hyphen logic for DCS seeds
The hyphen is taken straight from DCS `comp=y`, with one special case (`sa`).
| Fault | Verses | Example | Fix |
|---|---|---|---|
| Prefix सु printed as a separate pada | 260 DCS, 501 Dharmamitra | VR.1.41.13 `सु दुःखितः` | treat `su` (DCS pos `i`) as a member: `सु-दुःखितः` |
| Negative अ printed as a separate pada | 12 DCS, 85 Dharmamitra | VR.4.67.16 `अ संस्पृष्ट्वा` | member `अ-` |
| Suffix shown as a compound member | 84 | VR.3.13.6 `लोल-त्वम्`, `तीक्ष्ण-ताम्`; VR.2.18.2 `विनीत-वत्` | merge -त्व/-ता/-वत् into one pada. Dharmamitra does the same with a space: VR.6.101.52 `महत् त्वस्य` |
| Hyphen across a space printed in the mūla | 60 | VR.5.16.9 `चतुर्दश-सहस्राणि`; VR.1.1.1 `तपः-स्वाध्याय-निरतम्` (right split, mūla space suspect) | keep, and add `mula_suspect` or drop the hyphen: needs a rule from you |
| DCS marks a non-member as `comp=y` | 1 found | VR.6.104.24 `प्रशस्य-एनम्` (an absolutive) | never hyphenate after an absolutive or finite verb |
| Compound member missing its mark in DCS | not countable by machine | VR.4.19.7 `राम वित्रासितान्` | left to sarga review |
- **Files:** `vrtools/dcs.py`, `vrtools/seed.py`, `scripts/seed_dharmamitra.py`, `tests/test_seed.py`.
- The checker itself cannot help: it treats a hyphen and a space alike, so
  `रामः-वनम्-गतः` and `मुनि पुङ्गवम्` both pass. The Step 4d padārtha check
  is the right place to catch this.

### S2. The checker accepts non-words and unsplit text (looseness c)
- `आनृण्य ताम्`, `परि पप्रच्छ`, `गुण वान्`, `तत्रा सीत्`, `ना अस्ति`,
  `मह-ऋषिः` and a whole unsplit line all pass; so does `शापितासि` left whole
  (VR.2.21.46).
- A word-list test was tried (vidyut kośa, already in `cache/vidyut-data`):
  it flags 22–24% of seeded verses, mostly sound words (केचित्, परिवार्य,
  rare verb forms), and it misses `सः क्रोधः` because both are words. **Not
  usable as a gate.**
- **Fix:** no change to the gate. Add the Step 4d check (each pada has a
  padārtha entry whose analysis fits its form) and keep the kośa lookup as an
  optional reviewer hint (O2).

### S3. ए + vowel may join as अय् (lets one wrong seed pass)
- VR.4.59.11 मयाऽऽहार → `मे आहार` (should be `मया आहार`). Only this verse
  relies on the rule. **Fix:** drop the `ay` outcome for final ए (keep the
  hiatus); keep `av` for final ओ. **Files:** `vrtools/sandhi.py`, tests.

### S4. Stray characters vanish from the comparison
- `norm` drops `.`, `|` and digits from the mūla, and the metre reader drops
  every non-ASCII leftover, so `मे.द्य` (VR.2.73.6) passes as `मेद्य` and is
  seeded as `मे अद्य`. **Fix:** a verse flagged `invalid_char` is not
  seeded; it waits for the mūla ruling (§6). **Files:** `scripts/seed_*.py`.

### S5. Accusative plurals in -āḥ (already noted in report §7.6)
- VR.7.89.3 `विद्रुता` for विद्रुताः; sample verse VR.2.30.23 the reverse
  (`विद्धाः` for the singular विद्धा). Covered by M4 if the DCS case and
  number are used for every -ā / -āḥ choice. **Files:** `vrtools/dcs.py`.

### S6. Report corrections
- §1 lists 71 verses with stray characters; §7.12 says 89. The data has 71.
- §7.13 says 1,115 metre failures; the data has 1,116.
- Add this review's error rates next to the "re-join pass rate" table so the
  pass rate is not read as accuracy. **Files:** `docs/STAGE_A_REPORT.md`
  (a dated correction note, not a rewrite).

### S7. Metre recogniser misses common long metres
- 95 of the 259 failures outside Ayodhyā 48–88 are long-metre verses the
  checker does not know (mixed 11/12-syllable upajāti, verses printed two
  pādas per line, six-line verses). They hide the real defects such as
  VR.1.1.100. **Fix:** recognise mixed triṣṭubh–jagatī upajāti and two-line
  printing. **Files:** `vrtools/metre.py`, `tests/test_metre.py`.

## Optional

- **O1. Crosswalk label `absent`.** 6 of 7 sampled `absent` verses with a
  best score of 0.50–0.60 do have a loose Critical Edition counterpart (same
  first pāda). No wrong padaccheda can come of it, because a DCS seed must
  still re-join. A fourth relation ("pāda shared") would make the internal
  record truer. `vrtools/crosswalk.py`.
- **O2. Kośa hint.** Store "pada not in the vidyut word list" as a reviewer
  hint per verse (never a gate). New small module + test.
- **O3. Seed disagreement count** (2,305) will be stale after M2–M4; rerun
  `scripts/crosscheck_seeds.py` (from cache).
- **O4. Published `crosswalk.ce` numbers.** Harmless, but D1b says no CE
  badges; consider dropping the field from the published JSON.
- **O5.** Record the two sample draws of §4 as a test fixture so the error
  rate can be re-measured after each fix.

---

## 1. The six wrong splits named in the brief: all confirmed

| Verse | Stored split | Seed | Checker | Cause |
|---|---|---|---|---|
| VR.1.60.12 | `सः क्रोधः` for सक्रोधः | Dharmamitra | passes | M3 |
| VR.6.70.22 | `सः विस्फुलिङ्गम् सः ज्वालम्` | Dharmamitra | passes | M3 |
| VR.7.36.8 | `भः` for भो | Dharmamitra (which returned `bho`) | passes | M4, `GENUINE_O` bug |
| VR.2.24.34 | `आनृण्य ताम्` for आनृण्यताम् | Dharmamitra | passes | S1 (suffix), S2 |
| VR.3.24.6 | `नो भयम्` for नोऽभयम् | DCS (CE reads नो भयम्) | passes | M2 |
| VR.6.104.24 | `प्रशस्य-एनम्` | DCS (`praSasya` is marked `comp=y` in DCS itself) | passes | S1 |

## 2. Probing the checker (`vrtools/sandhi.py`)

52 wrong or doubtful splits of my own were run through `check_rejoin`.
**Rejected correctly (12):** wrong vowel length, a wrong nasal (`तान्` for
`तां`, `अहन्` for `अहम्`), a dropped visarga before a sibilant, a non-pausal
ending (`तद्`), an inflected compound member (`राजा-पुत्रः`), `च एव` for
`चेव`, `सः हम्` for सोऽहम्.
**Accepted wrongly (the classes that matter):**

| Class | Probe that passes | Item |
|---|---|---|
| Avagraha dropped | `नोऽभयं` ← `नः भयम्`; `लोकेऽस्मिन्` ← `लोके स्मिन्` | M2 |
| Avagraha invented | `ततो धर्मः` ← `ततः अधर्मः`; `रामो विद्वान्` ← `रामः अविद्वान्` | M2 |
| Prefix as pronoun, pronoun as prefix | `सलक्ष्मणं` ← `सः लक्ष्मणम्`; `स रामो` ← `स-रामः` | M3 |
| One word cut in two | `आनृण्य ताम्`, `परि पप्रच्छ`, `गुण वान्` | S2 |
| Words not split at all | a whole line as one pada; `रामोवनम्` | S2 |
| Hyphen and space interchangeable | `प्रशस्य-एनम्`, `रामः-वनम्-गतः`, `मुनि पुङ्गवम्` | S1 |
| Visarga invented or lost | `सीताः गच्छति`, `भः राम` | M4 |
| Vowel-sandhi non-words | `तत्रा सीत्`, `ना अस्ति`, `ना इति`, `मह-ऋषिः` | S2 |
| Sandhi form kept as the pada | `एतन् न`, `तत् छ्रुत्वा`, `अस्मिन् नेव` | M4 |
| Stray signs ignored | `रामः १२` = `रामः`; `राम.ः` = `रामः` | S4 |

Some accepted joins are true ambiguities that only the meaning settles
(`राम इति` ← रामः / रामे; `तान्नृपान्` ← तान् / तात्). No checker can decide
those; they belong to the sarga review.

**Verdict on the four loosenesses of report §4:**
- (a) avagraha ignored: **real, fix now** (M2). Few verses, but the errors
  invert meanings.
- (b) DCS alternatives let the search choose: **real, the largest DCS error
  source** (M4).
- (c) non-words pass: **real and not fixable in the joiner** (S2). The
  padārtha-fit check of Step 4d and the sarga review are the remedy.
- (d) the morphology-preferred form is kept without proof: **real but
  small** once M4 uses case and number properly (S5).
- "स versus सः": the pausal rule is right for the pronoun; the fault is in
  seeding (M3).

## 3. Where the errors come from (measured on all 15,311 seeds)

| Class | Source | Verses | Item |
|---|---|---|---|
| Compound members shown with spaces | Dharmamitra | 9,533 flagged (about 9 in 10 have a compound) | known; sarga review |
| सु as a separate pada | both | 761 | S1 |
| Prefix स- as सः | Dharmamitra | 395 | M3 |
| त् left as न् | DCS | 129 | M4 |
| Visarga invented | DCS | 91 | M4 |
| अ as a separate pada | both | 97 | S1 |
| Suffix hyphenated | DCS | 84 | S1 |
| Feminine visarga missing | DCS | 80 | M4 |
| Hyphen across a mūla space | DCS | 60 | S1 |
| Final ओ → अः | Dharmamitra | 46 | M4 |
| Avagraha mismatch | both | 39 | M2 |
| छ् for श् | DCS | 32 | M4 |
Classes overlap in a few verses. Errors that need the meaning (wrong vowel
split such as `तया आदत्त वरा` for तया दत्तवरा, VR.4.51.18) cannot be counted
by machine; the samples put them at about 2–4% of verses.

## 4. True error rate (two samples of 100)

**Method.** `random.Random(20261111)`; first `sample(sorted DCS-seeded ids,
100)`, then with the same generator `sample(sorted Dharmamitra-seeded ids,
100)`. The ids are in Appendix A. I read every verse and judged each pada
against the mūla (§5.1 of `CLAUDE.md`). A verse is "wrong" if any pada has a
wrong letter or a wrong word boundary. Hyphen faults are counted apart.
Lexicalised compounds left whole (महात्मनः) are not counted. This is one
reader's judgment without a commentary; three doubtful cases are marked.

| | DCS (n=100) | Dharmamitra (n=100) |
|---|---|---|
| Wrong letter or word boundary | **8** | **9** |
| Hyphen fault only | 6 | about 90 (compounds with spaces; flagged) |
| Fully right as displayed | 86 | about 10 |

**DCS, wrong (8):** VR.1.35.21 `अप्रतिरूपायः`; VR.1.67.1 `रामायः`;
VR.2.30.23 `विद्धाः` (सा विद्धा); VR.3.43.38 `यन् माम्`; VR.3.56.11
`पातयेन्`; VR.3.70.19 `तन् मे`; VR.5.13.8 `आर्याया`; VR.2.21.46 `शापितासि`
left unsplit.
**DCS, hyphen only (6):** VR.1.41.13, VR.2.18.2, VR.7.91.5 (`सु` apart);
VR.4.19.7 `राम वित्रासितान्`; VR.3.13.6 `लोल-त्वम्`; VR.5.16.9
`चतुर्दश-सहस्राणि`.
**Dharmamitra, wrong (9):** prefix स- as सः in VR.2.92.36, VR.5.3.5,
VR.6.20.12, VR.6.71.44, VR.7.18.29; VR.4.51.18 `तया आदत्त वरा` (तया
दत्तवरा); VR.6.101.52 `महत् त्वस्य`; VR.7.2.19 `त्व सदृशम्` (तु असदृशम्);
VR.5.13.68 `तदा आर्या वदनम्` (तत्; doubtful).
**Judged right but worth a second look:** VR.2.90.3 `जगाम अनु पुरोहितम्`;
VR.3.69.45 `क्षुधा आर्तस्य`; VR.1.11.6 `शान्ता-भर्तारम्` (right; the mūla
prints a space).

## 5. Crosswalk thresholds (sample of 50)

Fixed seed 20261111, stratified toward the thresholds, half-split verses
excluded: 12 `same` with score 0.85–0.90, 6 `same` ≥ 0.90, 12 `partial` with
half-verse score 0.85–0.92, 6 `partial` ≥ 0.92, 7 `variant`, 7 `absent` with
a best score of 0.50–0.60. Each vulgate verse was read against its linked
Critical Edition verse.

| Stratum | n | Link right | Note |
|---|---|---|---|
| `same`, 0.85–0.90 | 12 | 12 | each differs from the CE by 1–3 words, e.g. VR.7.13.7 |
| `same`, ≥ 0.90 | 6 | 6 | |
| `partial`, 0.85–0.92 | 12 | 12 | 5 are really the same verse with variants (VR.5.35.22) |
| `partial`, ≥ 0.92 | 6 | 6 | |
| `variant` | 7 | 7 | |
| `absent`, 0.50–0.60 | 7 | (6 have a loose counterpart) | O1 |

No change needed to 0.85 / 0.85 / 0.6. A wrong link could only waste a DCS
attempt, never produce a wrong split, because the seed must still re-join.
About 180 `absent` verses have a best score of 0.5 or more.

## 6. The mūla (listed, not fixed)

### 6a. The 71 verses with stray characters (ids in Appendix E)
| Kind | Verses | Example | Proposed handling |
|---|---|---|---|
| U+093A, a stray vowel sign typed inside a word | 37 (Ayodhyā 91–119, Uttara) | VR.2.92.1 `अभिजगाम ऺह` | one reviewed rule "ignore U+093A when displaying"; text stays; flag `mula_suspect` |
| Latin letters left from a transliteration (L, J, C, O, Y, E) | 17 (Ayodhyā 52–87) | VR.2.55.13 `काLइन्दीम्` | part of the Ayodhyā half-split problem; see `AYODHYA_PRESPLIT_OPTIONS.md` (to be written) |
| An editor's gloss or variant in brackets | 10 | VR.2.7.27 `आशीविष(=सर्प)`; VR.7.23.51 `प्रहस्तो (प्रहसो)` | move the bracket to a source note on your approval |
| Punctuation: `!` `;` `,`, and `.` for avagraha | 5 | VR.2.73.6 `मे.द्य`; VR.7.25.25 `सा हृता,` | flag; correct only from a printed edition |
| U+0946 (short e) for ै | 1 | VR.5.44.4 `नभश्चॆव` | flag |
| Heading text inside the verse | 1 | VR.6.44.1 | M5 |
Until ruled on, none of these verses should be seeded or explained (S4).

### 6b. Metre failures outside Ayodhyā 48–88: 259 verses (ids in Appendix F)
| Kind | Verses | Example | Proposed handling |
|---|---|---|---|
| Long metre the checker does not know (includes the damaged VR.1.1.100) | 95 | VR.1.19.22, VR.2.2.54 (mixed 11/12) | S7; most are probably sound, not checked one by one |
| Half-split verses in other sargas | 41 | VR.3.14.8 | Ayodhyā options note |
| Śloka with one or two syllables too many or too few | 60 | VR.1.22.3 `राजा दशरस्तदा` (दशरथस्तदा); VR.1.44.3 `याताश्च च देववत्` | flag `mula_suspect`; compare with a printed edition later |
| Śloka length, even-pāda cadence broken | 28 | VR.1.1.45 `दण्डकारण्यवासीनाम्`; VR.1.14.38 `सर्वाणि ब्राह्मणाः` (sound epic licence) | flag only the typos; mark the rest `metre_irregular` |
| Stray character (6a) | 18 | VR.2.91.28 | 6a |
| Śloka read as a mātrā metre | 10 | VR.1.1.9 `श्रीमाञ्छ्त्रुनिबर्हणः` | flag `mula_suspect` |
| Commentary sentence stored as a verse | 4 | VR.2.90.5 | M5 |
| Two verses stored as one | 3 | VR.1.26.4 | M5 |
In Bāla sarga 1 the failures are VR.1.1.9, VR.1.1.45 and VR.1.1.100; all
three are source typos or damage, confirmed in `cache/wikisource/`.

## 7. What was not reviewed
- The 8,304 verses with no seed and the fix queue (out of scope by brief §5).
- The reader site's code, beyond what Step 3b will touch.
- Dharmamitra's terms of use (still unconfirmed; no call was made).
- No IIT Kanpur or valmikiramayan.net page was fetched, so the mūla
  findings rest on metre, spelling and the Critical Edition text only.

---

## Appendix A. The two samples of §4

Verse ids are given without the `VR.` prefix throughout the appendices.

**DCS (100):** 1.11.6, 1.17.19, 1.24.7, 1.29.8, 1.35.21, 1.41.13, 1.51.13, 1.58.13, 1.59.3, 1.62.27, 1.67.1, 2.4.1, 2.4.20, 2.8.16, 2.18.2, 2.20.15, 2.21.46, 2.30.3, 2.30.23, 2.90.3, 2.93.10, 2.96.22, 2.97.17, 2.103.4, 2.103.25, 2.108.15, 2.111.31, 2.118.41, 3.1.16, 3.7.12, 3.11.58, 3.13.6, 3.18.11, 3.23.20, 3.37.10, 3.43.38, 3.45.14, 3.45.16, 3.54.9, 3.55.19, 3.56.11, 3.56.26, 3.58.18, 3.69.45, 3.70.19, 4.8.36, 4.12.31, 4.18.55, 4.19.7, 4.32.21, 4.40.2, 4.40.53, 4.40.60, 4.47.13, 4.54.4, 4.55.12, 5.6.20, 5.13.8, 5.16.9, 5.22.14, 5.23.12, 5.24.43, 5.34.26, 5.44.2, 5.46.13, 5.48.53, 5.55.20, 5.58.66, 5.61.6, 5.63.1, 5.65.10, 5.68.8, 5.68.22, 6.38.7, 6.39.21, 6.44.23, 6.65.30, 6.66.30, 6.76.51, 6.82.6, 6.92.38, 6.97.5, 6.99.18, 6.101.36, 6.106.13, 6.107.63, 6.113.12, 7.1.39, 7.4.4, 7.5.18, 7.18.21, 7.20.24, 7.27.28, 7.44.15, 7.61.23, 7.62.19, 7.70.15, 7.88.1, 7.91.5, 7.91.8

**Dharmamitra (100):** 1.1.94, 1.40.4, 1.40.19, 1.42.19, 1.43.7, 1.50.23, 1.52.4, 1.69.18, 2.1.36, 2.3.49, 2.4.21, 2.5.26, 2.6.2, 2.12.21, 2.17.20, 2.18.23, 2.21.5, 2.92.36, 2.97.22, 3.47.43, 3.56A.8, 3.60.6, 3.61.19, 3.68.12, 3.75.25, 4.1.20, 4.1.56, 4.11.51, 4.11.62, 4.33.46, 4.40.43, 4.42.33, 4.45.1, 4.46.19, 4.51.18, 4.62.4, 4.67.16, 5.1.54, 5.1.79, 5.1.127, 5.2.57, 5.3.5, 5.4.24, 5.11.45, 5.13.68, 5.19.10, 5.31.13, 5.35.51, 5.37.13, 5.38.9, 5.43.11, 5.46.28, 5.47.21, 5.56.1, 5.62.8, 5.65.22, 6.4.85, 6.19.37, 6.20.12, 6.22.38, 6.24.18, 6.30.35, 6.32.42, 6.39.26, 6.42.45, 6.53.13, 6.54.35, 6.67.118, 6.68.7, 6.71.44, 6.72.12, 6.76.86, 6.85.26, 6.87.20, 6.101.52, 6.109.21, 6.111.58, 6.118.7, 6.127.32, 7.2.19, 7.9.45, 7.11.43, 7.14.1, 7.18.7, 7.18.29, 7.25.19, 7.25.32, 7.26.22, 7.30.44, 7.31.8, 7.31.32, 7.32.4, 7.34.23, 7.35.46, 7.50.11, 7.55.15, 7.57.15, 7.72.2, 7.74.15, 7.76.4


To redraw:
```python
rng = random.Random(20261111)
dcs_ids = rng.sample(sorted(ids of verses with seed.source == "dcs" and a padaccheda), 100)
dm_ids  = rng.sample(sorted(ids of verses with seed.source == "dharmamitra" and a padaccheda), 100)
```

## Appendix B. Seeds that fail when avagraha is significant (M2): 39

**ऽ in the mūla, no अ in the split (9):** 1.35.4, 3.24.6, 4.59.11, 6.83.22, 7.30.36, 7.34.2, 7.49.17, 7.63.19, 7.91.24

**Split elides an अ, mūla prints no ऽ (30):** 1.13.15, 1.41.5, 2.39.18, 2.73.6, 2.91.5, 2.91.25, 2.99.42, 2.100.25, 2.102.11, 2.110.23, 2.117.14, 5.10.12, 5.44.10, 5.44.16, 6.17.7, 6.35.37, 6.48.5, 6.59.2, 6.59.33, 6.59.36, 6.59.72, 6.59.99, 6.59.103, 6.59.140, 6.60.76, 6.62.4, 6.67.66, 6.69.78, 6.73.57, 7.15.22

Of the 30, the split is wrong in 1.13.15 (`ये अव्यग्राः` for ये व्यग्राः) and 6.69.78 (`ते अस्वस्थाः`), and doubtful in 6.48.5; in the others the mūla lacks an ऽ that the grammar expects (twelve are रक्षोधिप-, inside a compound).

## Appendix C. Dharmamitra seeds where सः is joined in the mūla to a following consonant (M3): 395

1.1.84, 1.11.12, 1.13.25, 1.15.9, 1.17.36, 1.18.32, 1.21.1, 1.21.12, 1.22.1, 1.25.3, 1.25.18, 1.27.3, 1.29.25, 1.36.16, 1.41.11, 1.45.20, 1.45.28, 1.55.3, 1.55.8, 1.57.20, 1.60.7, 1.60.12, 1.65.40, 1.66.9, 1.67.16, 1.72.23, 1.73.22, 1.77.14, 1.77.19, 2.2.50, 2.4.34, 2.5.6, 2.5.19, 2.6.28, 2.7.28, 2.12.93, 2.12.106, 2.13.5, 2.15.8, 2.16.4, 2.19.11, 2.20.6, 2.22.1, 2.22.6, 2.25.12, 2.28.9, 2.32.43, 2.33.25, 2.34.18, 2.34.56, 2.36.1, 2.36.24, 2.37.21, 2.37.26, 2.37.27, 2.39.25, 2.40.15, 2.40.51, 2.41.7, 2.41.21, 2.43.6, 2.43.14, 2.44.24, 2.44.29, 2.45.5, 2.46.14, 2.46.15, 2.46.34, 2.47.10, 2.63.49, 2.89.18, 2.91.36, 2.92.36, 2.93.1, 2.96.31, 2.101.6, 2.104.14, 2.106.26, 2.112.7, 2.113.22, 2.114.7, 3.1.6, 3.1.22, 3.2.7, 3.2.10, 3.3.13, 3.7.20, 3.8.10, 3.11.3, 3.11.89, 3.13.10, 3.16.34, 3.18.26, 3.19.9, 3.20.24, 3.21.8, 3.21.17, 3.22.18, 3.22.23, 3.23.23, 3.24.5, 3.24.19, 3.24.24, 3.25.22, 3.25.23, 3.26.13, 3.26.24, 3.26.28, 3.28.15, 3.28.30, 3.31.49, 3.35.11, 3.38.33, 3.39.21, 3.39.25, 3.41.16, 3.41.18, 3.51.10, 3.51.45, 3.52.25, 3.52.32, 3.53.11, 3.54.22, 3.58.7, 3.58.8, 3.60.33, 3.63.2, 3.65.7, 3.67.14, 3.71.15, 3.72.4, 4.1.4, 4.3.14, 4.5.28, 4.8.13, 4.9.17, 4.12.41, 4.16.24, 4.16.38, 4.19.4, 4.26.6, 4.27.37, 4.28.11, 4.28.41, 4.28.42, 4.28.57, 4.29.24, 4.30.39, 4.31.50, 4.32.22, 4.33.32, 4.38.12, 4.39.8a, 4.41.11, 4.43.62, 4.46.14, 4.47.3, 4.47.5, 4.59.18, 4.67.47, 5.1.73, 5.3.5, 5.7.15, 5.7.17, 5.10.40, 5.13.59, 5.18.16, 5.26.23, 5.26.28, 5.26.39, 5.27.37, 5.30.15, 5.34.36, 5.36.27, 5.37.64, 5.37.68, 5.38.26, 5.38.40, 5.38.69, 5.39.37, 5.39.43, 5.41.9, 5.46.11, 5.46.41, 5.47.5, 5.47.11, 5.47.17, 5.47.33, 5.48.3, 5.49.7, 5.51.31, 5.53.4, 5.54.38, 5.54.50, 5.56.18, 5.56.39, 5.56.49, 5.56.51, 5.58.55, 5.59.9, 5.59.16, 5.60.4, 5.62.25, 5.67.9, 5.67.37, 6.4.57, 6.7.24, 6.9.22, 6.14.21, 6.19.21, 6.19.29, 6.19.34, 6.20.12, 6.20.24, 6.21.19, 6.21.28, 6.21.29, 6.21.31, 6.22.1, 6.22.75, 6.23.15, 6.24.41, 6.26.13, 6.26.28, 6.29.15, 6.29.23, 6.31.21, 6.38.9, 6.38.20, 6.40.1, 6.40.25, 6.41.7, 6.42.3, 6.42.36, 6.44.32, 6.46.18, 6.47.10, 6.47.24, 6.48.21, 6.49.4, 6.50.33, 6.56.30, 6.56.37, 6.58.1, 6.58.21, 6.58.61, 6.59.21, 6.60.47, 6.60.79, 6.61.4, 6.64.30, 6.65.48, 6.66.9, 6.67.23, 6.67.71, 6.70.22, 6.70.47, 6.71.44, 6.71.106, 6.72.4, 6.72.9, 6.72.10, 6.73.58, 6.73.66, 6.74.67, 6.74.68, 6.74.70, 6.76.24, 6.76.54, 6.77.6, 6.77.8, 6.78.3, 6.78.19, 6.84.16, 6.85.19, 6.85.24, 6.85.25, 6.88.10, 6.90.12, 6.90.71, 6.90.73, 6.90.74, 6.91.22, 6.91.23, 6.91.28, 6.92.1, 6.92.11, 6.92.19, 6.92.39, 6.92.47, 6.94.36, 6.95.16, 6.97.33, 6.98.8, 6.98.16, 6.98.26, 6.99.7, 6.100.21, 6.100.56, 6.102.65, 6.106.24, 6.107.47, 6.107.48, 6.107.59, 6.108.8, 6.108.31, 6.111.90, 6.111.124, 6.112.6, 6.113.51, 6.114.18, 6.114.31, 6.115.8, 6.116.1, 6.117.5, 6.120.17, 6.121.30, 6.122.21, 6.123.38, 6.123.56, 6.124.8, 6.124.14, 6.125.7, 6.125.29, 6.127.4, 6.127.12, 6.127.13, 6.127.28, 6.128.59, 6.128.62, 6.128.97, 7.1.4, 7.6.66, 7.7.28, 7.7.53, 7.9.29, 7.11.17, 7.11.46, 7.11.49, 7.14.4, 7.15.6, 7.16.14, 7.17.10, 7.18.29, 7.18.33, 7.18.35, 7.22.18, 7.22.22, 7.22.26, 7.25.16, 7.26.18, 7.28.38, 7.29.42, 7.30.31, 7.31.21, 7.31.30, 7.31.34, 7.32.11, 7.32.16, 7.32.35, 7.32.45, 7.32.48, 7.32.73, 7.34.28, 7.34.32, 7.35.33, 7.35.53, 7.35.64, 7.36.47, 7.36.50, 7.36.55, 7.37.15, 7.38.24, 7.53.8, 7.54.14, 7.67.16, 7.67.21, 7.71.7, 7.76.41, 7.79.19, 7.81.17, 7.93.1, 7.96.10, 7.98.23, 7.101.3, 7.106.10, 7.106.17, 7.106.18, 7.107.13, 7.109.6, 7.109.10, 7.109.13, 7.109.15, 7.110.2, 7.111.8

## Appendix D. Other mechanical classes (M4, S1)

**visarga added against the DCS morphology (91):** 1.14.24, 1.20.1, 1.21.7, 1.28.20, 1.29.8, 1.35.21, 1.35.22, 1.36.26, 1.37.11, 1.39.1, 1.45.7, 1.56.15, 1.59.17, 1.60.4, 1.61.4, 1.61.9, 1.63.4, 1.67.1, 1.70.16, 1.73.11, 2.1.5, 2.6.19, 2.20.36, 2.26.14, 2.28.21, 2.34.6, 2.36.21, 2.36.23, 2.39.14, 2.45.28, 2.93.10, 2.101.5, 2.105.24, 2.109.15, 2.112.4, 2.117.4, 3.5.14, 3.17.4, 3.23.20, 3.28.2, 3.39.7, 3.56.6, 3.57.7, 3.60.2, 4.10.33, 4.11.2, 4.11.16, 4.14.21, 4.20.26, 4.26.10, 4.30.68, 4.37.14, 4.45.3, 4.67.20, 5.6.34, 5.9.31, 5.11.30, 5.14.13, 5.35.38, 5.40.22, 5.61.3, 5.61.4, 6.4.14, 6.25.7, 6.44.23, 6.48.28, 6.65.46, 6.71.30, 6.75.4, 6.85.34, 6.89.52, 6.90.81, 6.102.24, 6.107.31, 6.120.15, 7.4.10, 7.19.20, 7.23.28, 7.28.42, 7.32.39, 7.34.19, 7.46.17, 7.60.11, 7.78.15, 7.90.13, 7.97.7, 7.97.24, 7.100.7, 7.100.9, 7.107.14, 7.108.19

**feminine genitive/ablative without visarga (80):** 1.3.12, 1.3.32, 1.22.11, 1.26.10, 1.35.13, 1.36.26, 1.37.18, 1.37.31, 1.38.20, 1.46.13, 1.64.10, 2.7.18, 2.8.20, 2.9.8, 2.13.4, 2.14.11, 2.19.23, 2.20.27, 2.21.22, 2.22.18, 2.24.21, 2.39.32, 2.42.29, 2.46.17, 2.92.22, 2.96.17, 2.119.12, 3.20.4, 3.42.21, 3.49.1, 3.52.26, 3.54.17, 3.57.4, 3.61.17, 3.64.10, 3.72.5, 3.74.1, 3.74.4, 4.1.5, 4.1.71, 4.1.72, 4.8.10, 4.9.11, 4.11.26, 4.34.14, 4.38.4, 4.51.17, 4.52.8, 5.2.55, 5.13.8, 5.15.51, 5.15.52, 5.16.14, 5.16.23, 5.22.23, 5.24.42, 5.25.12, 5.26.5, 5.27.6, 5.27.44, 5.33.22, 5.33.27, 5.36.32, 5.42.11, 5.54.6, 5.58.119, 5.66.7, 6.1.11, 6.1.18, 6.3.4, 6.5.5, 6.32.26, 6.34.4, 6.75.49, 6.81.5, 6.111.20, 6.113.12, 6.125.8, 7.12.1, 7.50.7

**final t left as n before a nasal (129):** 1.1.77, 1.4.3, 1.4.20, 1.8.2, 1.15.13, 1.18.39, 1.25.5, 1.28.13, 1.29.21, 1.36.14, 1.45.39, 1.46.23, 1.48.15, 1.54.10, 1.55.24, 1.56.20, 1.57.5, 1.59.8, 1.61.8, 1.61.10, 1.61.20, 1.66.22, 1.66.25, 1.67.18, 1.69.14, 1.71.7, 2.9.16, 2.14.61, 2.17.13, 2.18.16, 2.19.15, 2.19.25, 2.21.37, 2.25.32, 2.25.33, 2.26.25, 2.33.31, 2.36.17, 2.41.15, 2.46.28, 2.90.13, 2.90.16, 2.91.5, 2.94.5, 2.98.6, 2.98.7, 2.98.8, 2.100.19, 2.100.25, 2.100.39, 2.100.58, 2.110.30, 2.111.9, 2.111.11, 2.115.4, 2.116.6, 2.117.2, 2.118.25, 2.118.40, 3.1.10, 3.4.17, 3.4.19, 3.11.65, 3.11.92, 3.16.6, 3.22.17, 3.28.20, 3.33.5, 3.38.5, 3.43.28, 3.43.38, 3.46.38, 3.53.14, 3.54.1, 3.54.17, 3.56.11, 3.57.22, 3.61.15, 3.65.15, 3.68.6, 3.69.4, 3.70.19, 3.71.31, 3.73.22, 4.1.8, 4.7.8, 4.9.8, 4.13.16, 4.15.22, 4.18.4, 4.18.42, 4.22.13a, 4.22.16, 4.25.16, 4.30.76, 4.32.3, 4.36.11, 4.37.15, 4.38.16, 4.40.59, 4.40.70, 4.41.1, 4.42.53, 4.43.60, 4.45.3, 5.1.167, 5.9.53, 5.39.38, 5.68.5, 5.68.21, 6.22.67, 6.28.19, 6.41.47, 6.59.100, 6.65.55, 6.71.96, 6.73.61, 6.75.4, 6.89.15, 6.90.81, 6.90.94, 6.95.6, 6.99.19, 6.101.45, 6.128.25, 6.128.61, 7.21.45, 7.78.30, 7.110.3

**ch for sh after t (32):** 1.2.33, 1.12.15, 1.15.6, 1.15.15, 1.19.1, 1.20.1, 1.23.9, 1.37.9, 1.41.24, 1.51.10, 1.51.12, 1.56.5, 1.57.7, 1.58.8, 1.60.19, 1.76.6, 2.93.24, 2.115.4, 3.4.28, 3.5.41, 3.6.21, 3.9.19, 3.35.1, 3.39.1, 3.53.25, 3.70.3, 4.18.34, 4.18.40, 4.22.18, 4.48.21, 4.53.20, 6.30.2

**final o turned into aH (Dharmamitra) (46):** 1.11.16, 1.15.19, 1.17.20, 1.29.7, 1.34.13, 1.61.22, 1.68.9, 1.72.25, 2.7.5, 2.32.38, 3.23.28, 3.24.21, 3.43.12, 3.45.4, 3.49.24, 4.3.14, 4.11.82, 4.22.21, 4.24.4, 4.25.41, 5.3.17, 5.4.15, 6.7.8, 6.40.23, 6.41.5, 6.58.41, 6.83.43, 6.88.40, 6.102.18, 6.105.27, 6.107.49, 6.113.40, 6.116.6, 6.116.22, 7.11.33, 7.17.39, 7.20.12, 7.21.1, 7.21.32, 7.22.23, 7.23.22, 7.30.7, 7.36.8, 7.59.6, 7.71.7, 7.100.13

**su as a separate pada (DCS) (260):** 1.1.10, 1.1.50, 1.3.10, 1.6.20, 1.7.13, 1.9.8, 1.10.5, 1.12.1, 1.13.8, 1.13.10, 1.13.35, 1.14.19, 1.20.19, 1.20.26, 1.26.7, 1.33.6, 1.33.20, 1.33.21, 1.34.3, 1.35.1, 1.35.2, 1.39.19, 1.40.1, 1.41.13, 1.42.2, 1.45.15, 1.47.18, 1.48.15, 1.49.18, 1.51.18, 1.55.6, 1.56.8, 1.56.17, 1.57.8, 1.59.8, 1.60.26, 1.62.21, 1.63.2, 1.64.1, 1.64.13, 1.65.1, 1.65.19, 1.67.18, 1.69.2, 1.72.24, 2.6.3, 2.8.23, 2.9.8, 2.9.48, 2.15.4, 2.18.2, 2.23.5, 2.24.14, 2.29.19, 2.31.28, 2.32.17, 2.39.17, 2.39.18, 2.39.41, 2.40.5, 2.41.8, 2.91.15, 2.91.77, 2.97.25, 2.100.17, 2.102.13, 2.102.21, 2.102.24, 2.102.37, 2.104.6, 2.105.2, 2.105.7, 2.105.22, 2.111.9, 2.112.11, 2.112.17, 2.112.22, 2.113.14, 2.117.6, 2.118.44, 2.119.14, 3.1.13, 3.2.9, 3.3.2, 3.4.19, 3.5.43, 3.17.9, 3.17.11, 3.18.2, 3.22.20, 3.23.4, 3.24.7, 3.24.8, 3.24.30, 3.28.6, 3.28.21, 3.33.22, 3.39.10, 3.39.12, 3.41.4, 3.42.5, 3.44.9, 3.45.24, 3.46.38, 3.49.1, 3.52.19, 3.61.15, 3.66.12, 3.68.19, 3.68.37, 3.69.4, 3.69.48, 3.73.45, 3.74.5, 3.74.15, 3.74.23, 3.75.23, 4.9.5, 4.10.15, 4.10.17, 4.12.16, 4.16.15, 4.23.2, 4.23.22, 4.26.10, 4.34.3, 4.42.37, 4.43.25, 4.43.50, 4.48.9, 4.58.23, 4.62.3, 4.66.13, 5.1.4, 5.1.136, 5.1.172, 5.2.4, 5.2.9, 5.6.9, 5.7.3, 5.7.16, 5.9.24, 5.10.30, 5.10.51, 5.12.5, 5.14.3, 5.14.34, 5.15.8, 5.15.42, 5.20.19, 5.30.3, 5.37.3, 5.37.12, 5.38.56, 5.41.6, 5.42.44, 5.54.44, 5.55.2, 5.57.39, 5.58.9, 5.58.85, 5.64.32, 6.1.4, 6.1.5, 6.3.18, 6.6.17, 6.7.4, 6.9.18, 6.9.21, 6.16.20, 6.17.40, 6.22.79, 6.29.21, 6.41.18, 6.41.39, 6.41.90, 6.43.38, 6.48.28, 6.50.48, 6.55.14, 6.56.1, 6.57.26, 6.57.31, 6.58.5, 6.58.22, 6.58.47, 6.59.33, 6.63.37, 6.67.3, 6.67.4, 6.67.55, 6.67.151, 6.67.165, 6.71.13, 6.74.66, 6.76.45, 6.76.59, 6.76.70, 6.79.2, 6.80.15, 6.80.34, 6.81.6, 6.81.8, 6.82.5, 6.82.8, 6.84.11, 6.88.32, 6.88.49, 6.89.49, 6.92.9, 6.92.68, 6.96.23, 6.97.1, 6.98.18, 6.99.8, 6.100.12, 6.102.34, 6.102.55, 6.102.70, 6.103.7, 6.103.16, 6.107.1, 6.108.7, 6.108.27, 6.112.2, 6.114.36, 6.123.41, 6.126.1, 6.126.12, 6.127.2, 7.7.13, 7.9.23, 7.9.27, 7.11.2, 7.17.3, 7.25.9, 7.29.15, 7.31.12, 7.45.11, 7.46.4, 7.47.1, 7.52.3, 7.52.7, 7.61.7, 7.65.39, 7.68.10, 7.70.1, 7.75.13, 7.77.8, 7.81.14, 7.83.6, 7.84.3, 7.84.8, 7.89.4, 7.90.18, 7.91.5, 7.97.22, 7.99.11, 7.100.23, 7.105.17

**su as a separate pada (Dharmamitra) (501):** 1.1.36, 1.1.90, 1.6.9, 1.7.1, 1.7.16, 1.11.12, 1.11.18, 1.11.24, 1.11.26, 1.13.6, 1.13.11, 1.13.14, 1.13.17, 1.13.18, 1.13.22, 1.13.25, 1.13.37, 1.14.16, 1.14.18, 1.14.26, 1.14.53, 1.17.23, 1.18.46, 1.18.54, 1.20.6, 1.22.9, 1.22.23, 1.23.22, 1.26.16, 1.26.31, 1.27.20, 1.27.22, 1.29.12, 1.29.31, 1.30.22, 1.32.2, 1.32.10, 1.32.12, 1.48.18, 1.48.28, 1.52.17, 1.55.8, 1.63.25, 1.67.26, 1.68.18, 1.70.34, 1.71.8, 1.73.37, 1.74.4, 1.74.6, 1.75.24, 1.77.10, 2.6.6, 2.7.20, 2.9.42, 2.9.65, 2.12.19, 2.12.70, 2.12.109, 2.14.6, 2.15.33, 2.15.39, 2.15.42, 2.16.3, 2.16.12, 2.16.16, 2.16.41, 2.18.19, 2.19.34, 2.21.51, 2.21.52, 2.22.14, 2.26.5, 2.27.22, 2.28.10, 2.31.14, 2.31.16, 2.32.27, 2.33.4, 2.34.60, 2.36.3, 2.36.26, 2.37.10, 2.45.26, 2.70.26, 2.89.11, 2.90.23, 2.91.35, 2.91.51, 2.92.6, 2.93.6, 2.95.18, 2.100.21, 2.100.43, 2.100.45, 2.103.28, 2.114.31, 3.3.13, 3.3.21, 3.4.1, 3.4.9, 3.4.11, 3.7.20, 3.7.24, 3.8.13, 3.9.2, 3.10.12, 3.11.1, 3.12.16, 3.18.17, 3.20.11, 3.22.18, 3.23.8, 3.25.31, 3.27.13, 3.28.18, 3.31.48, 3.32.3, 3.32.25, 3.34.2, 3.34.16, 3.34.20, 3.39.11, 3.44.14, 3.44.21, 3.49.16, 3.49.36, 3.52.20, 3.52.21, 3.52.41, 3.54.23, 3.54.30, 3.55.26, 3.55.28, 3.56.22, 3.59.27, 3.60.31, 3.61.12, 3.62.20, 3.63.9, 3.66.15, 3.69.26, 3.73.32, 4.1.21, 4.1.41, 4.1.77, 4.1.125, 4.3.14, 4.5.16, 4.5.18, 4.8.13, 4.8.17, 4.10.35, 4.11.35, 4.11.89, 4.16.20, 4.16.39, 4.18.38, 4.18.65, 4.19.4, 4.19.16, 4.20.15, 4.24.28, 4.25.24, 4.25.38, 4.27.30, 4.28.41, 4.30.12, 4.30.44, 4.31.36, 4.33.19, 4.33.29, 4.35.6, 4.35.19, 4.35.20, 4.36.2, 4.37.28, 4.40.35, 4.40.36, 4.40.50, 4.41.7, 4.41.22, 4.41.44, 4.42.30, 4.46.7, 4.46.9, 4.52.26, 4.57.16, 4.58.36, 4.59.12, 5.1.32, 5.1.72, 5.1.166, 5.1.193, 5.2.15, 5.2.24, 5.2.28, 5.2.47, 5.2.56, 5.3.4, 5.3.39, 5.4.29, 5.5.9, 5.5.14, 5.5.17, 5.5.21, 5.7.7, 5.9.10, 5.9.18, 5.9.36, 5.9.65, 5.9.66, 5.10.17, 5.11.42, 5.14.41, 5.14.46, 5.20.11, 5.20.22, 5.21.25, 5.22.26, 5.25.18, 5.27.47, 5.27.53, 5.29.2, 5.30.4, 5.32.13, 5.36.41, 5.39.24, 5.42.4, 5.43.6, 5.48.36, 5.49.4, 5.49.9, 5.54.40, 5.56.3, 5.58.128, 5.58.156, 5.61.15, 5.62.21, 5.64.20, 5.65.14, 5.65.22, 5.67.21, 5.68.7, 6.3.11, 6.4.8, 6.4.42, 6.4.77, 6.4.113, 6.5.1, 6.5.13, 6.6.15, 6.7.3, 6.7.15, 6.8.6, 6.8.9, 6.9.15, 6.11.27, 6.11.29, 6.14.20, 6.15.11, 6.15.12, 6.17.13, 6.18.37, 6.22.76, 6.22.88, 6.24.22, 6.25.18, 6.26.7, 6.27.41, 6.30.14, 6.31.3, 6.31.9, 6.32.9, 6.33.9, 6.34.17, 6.38.9, 6.40.3, 6.41.28, 6.41.72, 6.43.1, 6.43.10, 6.43.11, 6.43.16, 6.44.4, 6.44.33, 6.48.19, 6.49.19, 6.50.55, 6.50.65, 6.51.3, 6.51.4, 6.51.8, 6.51.9, 6.52.2, 6.52.23, 6.52.38, 6.53.5, 6.53.17, 6.53.21, 6.55.18, 6.55.28, 6.56.3, 6.56.16, 6.57.39, 6.58.2, 6.58.4, 6.58.10, 6.58.61, 6.59.8, 6.59.47, 6.59.99, 6.60.67, 6.61.7, 6.61.13, 6.62.13, 6.62.20, 6.65.23, 6.65.38, 6.66.20, 6.67.5, 6.67.99, 6.67.157, 6.69.12, 6.69.26, 6.71.11, 6.71.116, 6.72.4, 6.72.9, 6.72.10, 6.73.6, 6.73.32, 6.73.38, 6.73.50, 6.76.38, 6.76.39, 6.79.20, 6.81.3, 6.83.13, 6.86.11, 6.86.15, 6.88.2, 6.88.21, 6.88.54, 6.90.23, 6.90.32, 6.90.55, 6.91.28, 6.92.35, 6.93.10, 6.93.20, 6.94.41, 6.97.9, 6.97.31, 6.98.9, 6.98.21, 6.98.24, 6.100.23, 6.100.36, 6.100.39, 6.101.26, 6.101.43, 6.101.44, 6.101.46, 6.102.39, 6.102.42, 6.103.2, 6.103.9, 6.104.1, 6.105.28, 6.107.17, 6.107.20, 6.107.28, 6.108.9, 6.111.34, 6.111.91, 6.112.12, 6.113.33, 6.115.15, 6.117.26, 6.118.6, 6.118.18, 6.119.36, 6.120.3, 6.125.29, 6.125.37, 6.125.45, 6.127.12, 6.127.13, 6.127.48, 6.128.13, 6.128.66, 7.2.17, 7.3.11, 7.7.24, 7.9.24, 7.9.31, 7.10.2, 7.11.26, 7.11.52, 7.12.9, 7.13.9, 7.15.3, 7.15.43, 7.17.20, 7.18.18, 7.19.4, 7.19.7, 7.19.11, 7.19.15, 7.20.21, 7.21.10, 7.21.21, 7.21.46, 7.22.23, 7.23.4, 7.23.7, 7.23.42, 7.23.47, 7.24.18, 7.26.2, 7.27.5, 7.27.32, 7.27.45, 7.28.3, 7.28.30, 7.29.23, 7.30.20, 7.30.37, 7.30.46, 7.30.48, 7.31.21, 7.32.35, 7.38.18, 7.38.26, 7.40.3, 7.41.16, 7.43.12, 7.44.4, 7.45.13, 7.46.2, 7.48.11, 7.51.3, 7.51.10, 7.52.19, 7.53.24, 7.53.26, 7.55.20, 7.56.5, 7.57.13, 7.61.5, 7.61.16, 7.65.32, 7.66.14, 7.68.20, 7.69.9, 7.71.6, 7.71.9, 7.72.6, 7.72.16, 7.73.14, 7.73.18, 7.75.14, 7.76.4, 7.76.6, 7.76.9, 7.76.17, 7.77.16, 7.78.10, 7.78.18, 7.79.20, 7.80.5, 7.80.17, 7.84.6, 7.84.16, 7.87.4, 7.87.5, 7.89.5, 7.90.6, 7.90.19, 7.91.15, 7.91.23, 7.92.9, 7.93.4, 7.93.9, 7.93.12, 7.93.14, 7.94.21, 7.95.9, 7.96.4, 7.96.16, 7.98.20, 7.100.16, 7.100.22, 7.101.7, 7.101.13, 7.101.14, 7.102.6, 7.102.8, 7.109.22, 7.110.15

**a as a separate pada (DCS) (12):** 1.41.26, 1.42.9, 2.22.8, 2.22.10, 2.22.26, 3.49.13, 3.54.15, 3.72.10, 4.18.5, 4.20.25, 5.24.5, 6.63.4

**a as a separate pada (Dharmamitra) (85):** 1.6.7, 1.6.14, 1.6.15, 1.14.11, 1.14.21, 1.25.18, 1.36.11, 1.45.35, 1.65.6, 2.2.37, 2.4.30, 2.10.20, 2.12.112, 2.13.12, 2.14.64, 2.15.48, 2.19.11, 2.20.42, 2.20.47, 2.27.12, 2.38.7, 2.39.29, 2.99.37, 2.101.9, 2.103.7, 2.118.37, 3.5.6, 3.23.22, 3.28.7, 3.37.3, 3.40.10, 3.40.14, 3.52.39, 3.54.24, 3.61.8, 4.1.33, 4.1.109, 4.3.28, 4.18.43, 4.24.28, 4.27.36, 4.31.13, 4.35.9, 4.35.16, 4.53.12, 4.65.30, 4.67.16, 5.2.3, 5.3.36, 5.3.43, 5.7.17, 5.12.8, 5.13.40, 5.16.19, 5.30.13, 5.55.8, 5.58.146, 5.63.6, 6.7.2, 6.12.34, 6.15.12, 6.19.21, 6.34.25, 6.41.2, 6.43.40, 6.46.14, 6.55.13, 6.58.41, 6.59.5, 6.67.10, 6.73.67, 6.80.22, 6.82.11, 6.88.28, 6.88.50, 6.108.17, 6.111.21, 6.118.14, 6.118.18, 7.10.31, 7.16.22, 7.27.18, 7.34.27, 7.73.8, 7.84.16

**suffix hyphenated (DCS) (84):** 1.1.18, 1.2.40, 1.3.10, 1.17.1, 1.20.2, 1.29.9, 1.58.16, 2.2.38, 2.7.23, 2.8.25, 2.18.2, 2.23.37, 2.26.2, 2.38.1, 2.42.18, 2.64.5, 2.72.14, 2.94.17, 2.95.15, 2.98.2, 2.100.66, 2.106.34, 2.109.5, 2.109.31, 2.112.6, 2.115.14, 2.115.19, 2.117.5, 3.1.13, 3.6.9, 3.6.10, 3.9.4, 3.9.8, 3.11.59, 3.11.93, 3.13.6, 3.17.14, 3.18.2, 3.29.20, 3.42.27, 3.52.6, 3.57.17, 3.66.4, 4.2.17, 4.9.3, 4.18.17, 4.25.7, 4.42.24, 4.54.20, 4.56.24, 4.61.2, 5.10.12, 5.22.16, 5.23.4, 5.25.14, 5.34.25, 5.37.15, 5.44.11, 5.48.35, 5.51.26, 5.64.5, 6.17.16, 6.17.35, 6.49.12, 6.63.6, 6.65.55, 6.71.10, 6.82.3, 6.108.25, 7.3.19, 7.4.10, 7.13.31, 7.23.11, 7.26.43, 7.32.18, 7.35.3, 7.47.18, 7.68.19, 7.83.6, 7.84.15, 7.87.19, 7.87.26, 7.89.8, 7.90.4

**hyphen across a space printed in the mula (DCS) (60):** 1.1.1, 1.1.17, 1.1.43, 1.3.16, 1.4.29, 1.11.6, 1.37.20, 2.6.19, 2.15.7, 2.26.17, 2.52.50, 2.56.8, 2.64.5, 2.65.22, 2.72.14, 2.81.9, 2.82.11, 2.88.12, 2.91.59, 2.92.33, 2.100.76, 2.102.6, 2.108.8, 3.29.28, 3.40.12, 3.43.7, 3.54.1, 4.14.11, 4.19.3, 4.20.12, 4.21.2, 4.26.9, 4.26.14, 4.35.7, 5.16.9, 5.37.16, 5.44.19, 5.46.2, 6.17.52, 6.45.1, 6.49.29, 6.57.10, 6.60.22, 6.64.2, 6.69.67, 6.83.14, 6.87.14, 6.88.64, 6.93.31, 6.93.32, 6.94.14, 6.96.3, 6.96.21, 6.111.33, 6.117.14, 6.120.24, 6.126.40, 6.128.32, 7.11.13, 7.65.25

## Appendix E. Verses with stray characters: 71

**U+093A stray vowel sign (37):** 2.91.19, 2.91.27, 2.91.63, 2.92.1, 2.92.11, 2.92.15, 2.93.17, 2.94.24, 2.95.8, 2.97.3, 2.97.26, 2.97.29, 2.98.9, 2.99.7, 2.100.42, 2.101.7, 2.103.3, 2.105.6, 2.105.30, 2.106.14, 2.106.18, 2.106.19, 2.106.20, 2.109.20, 2.110.8, 2.111.1, 2.112.28, 2.113.2, 2.114.13, 2.119.3, 2.119.21, 7.16.48, 7.16.49, 7.35.52, 7.36.7, 7.60.18, 7.85.14

**Latin letters (17):** 2.52.99, 2.55.13, 2.55.15, 2.55.19, 2.55.21, 2.56.14, 2.56.31, 2.58.7, 2.58.8, 2.63.9, 2.65.2, 2.70.4, 2.71.10, 2.75.3, 2.75.51, 2.87.4, 2.87.8

**bracketed gloss or variant (10):** 2.7.27, 2.9.46, 2.52.28, 2.55.5, 2.91.28, 2.116.7, 7.22.15, 7.23.51, 7.25.34, 7.49.23

**punctuation, and U+0946 in 5.44.4 (6):** 2.52.9, 2.52.43, 2.73.6, 5.44.4, 7.18.27, 7.25.25

**heading text inside the verse (1):** 6.44.1

## Appendix F. Metre failures outside Ayodhyā 48–88: 259

**long metre the checker does not know (95):** 1.1.100, 1.17.37, 1.19.22, 2.2.54, 2.12.106, 2.16.46, 2.27.22, 2.32.42, 2.36.32, 2.43.21, 2.46.34, 2.112.31, 2.116.25, 3.15.13, 3.23.34, 3.40.27, 3.45.40, 3.47.50, 3.56A.25, 3.56A.26, 3.63.6, 3.67.29, 3.75.29, 4.2.29, 4.3.39, 4.5.30, 4.6.27, 4.24.40, 4.27.48, 4.28.27, 4.30.85, 4.31.3, 4.53.26, 4.56.17, 5.1.212, 5.16.29, 5.21.34, 5.28.13, 5.32.14, 5.41.9, 5.47.1, 5.47.15, 5.47.17, 5.47.30, 5.47.37, 5.48.5, 5.48.6, 5.48.9, 5.53.44, 6.11.30, 6.11.31, 6.12.28, 6.12.39, 6.14.3, 6.14.4, 6.14.21, 6.20.22, 6.20.25, 6.29.29, 6.31.45, 6.32.44, 6.33.38, 6.40.14, 6.54.37, 6.58.61, 6.59.94, 6.59.130, 6.60.96, 6.62.4, 6.63.57, 6.63.58, 6.67.94, 6.67.144, 6.67.171, 6.69.96, 6.72.19, 6.73.4, 6.73.74, 6.80.43, 6.82.28, 6.86.35, 6.91.29, 6.93.39, 6.99.51, 6.101.56, 6.107.67, 6.119.39, 7.1.41, 7.5.45, 7.7.54, 7.8.28, 7.11.52, 7.29.41, 7.86.21, 7.93.19

**half-split verse (other sargas) (41):** 1.14.46, 1.31.19, 3.14.8, 3.14.9, 3.14.12, 3.14.13, 3.14.14, 3.14.15, 3.14.16, 3.14.17, 3.14.19, 3.14.20, 3.14.21, 3.14.24, 3.14.25, 3.14.26, 3.14.27, 3.14.28, 3.14.31, 3.14.32, 3.14.33, 3.14.34, 3.14.35, 3.14.36, 3.15.2, 3.15.3, 3.15.5, 3.15.6, 3.15.8, 3.15.10, 3.15.12, 3.15.15, 3.15.16, 3.15.18, 3.15.20, 3.15.24, 3.15.27, 3.15.28, 3.15.31, 6.117.25, 6.117.33

**sloka with one or two syllables too many or too few (60):** 1.7.3, 1.9.10, 1.13.39, 1.14.58, 1.18.6, 1.18.23, 1.18.58, 1.21.3, 1.22.3, 1.22.18, 1.25.17, 1.30.10, 1.32.20, 1.44.3, 1.64.4, 1.65.23, 2.16.3, 2.91.31, 2.96.13, 2.98.16, 2.100.22, 2.102.30, 2.103.15, 2.104.8, 2.113.18, 2.114.6, 3.11.72, 3.14.6, 3.14.18, 3.15.17, 3.35.9, 3.55.1, 4.7.16, 4.18.26, 4.46.16, 5.4.20, 5.9.45, 6.44.6, 6.56.19, 6.81.4, 6.101.47, 7.1.40, 7.5.25, 7.5.27, 7.8.1, 7.11.5, 7.13.9, 7.17.32, 7.21.14, 7.27.40, 7.35.56, 7.36.51, 7.46.11, 7.57.2, 7.76.49, 7.77.12, 7.78.21, 7.86.5, 7.92.9, 7.111.10

**sloka length, even-pada cadence broken (28):** 1.1.45, 1.14.38, 1.14.40, 1.40.25, 2.15.6, 2.91.24, 2.93.2, 2.103.32, 2.106.35, 5.3.40, 5.4.19, 5.18.13, 5.63.33, 6.33.14, 6.43.34, 6.53.26, 7.6.24, 7.7.16, 7.16.4, 7.25.28, 7.25.35, 7.29.39, 7.29.40, 7.34.42, 7.35.65, 7.36.25, 7.55.13, 7.111.1

**stray character (18):** 2.7.27, 2.9.46, 2.91.28, 2.92.11, 2.93.17, 2.100.42, 2.105.6, 2.106.19, 2.116.7, 2.119.3, 5.44.4, 6.44.1, 7.16.48, 7.16.49, 7.22.15, 7.23.51, 7.25.34, 7.36.7

**sloka read as a matra metre (10):** 1.1.9, 2.99.20, 2.112.2, 2.116.26, 6.24.6, 6.44.9, 6.56.2, 6.105.10, 7.6.35, 7.49.20

**commentary sentence stored as a verse (4):** 2.90.5, 2.93.5, 2.97.27, 2.106.15

**two verses stored as one (3):** 1.26.4, 1.31.14, 3.73.41
