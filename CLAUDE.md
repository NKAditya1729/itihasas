# CLAUDE.md — श्रीमद्वाल्मीकिरामायणम् · सरलसंस्कृतपाठः (Valmiki Ramayana Sanskrit Reader)

## 0. Mission
Build a complete, static Sanskrit reader of the Vālmīki Rāmāyaṇa for learners: "learn Sanskrit through the story". The text is arranged as कण्डः → सर्गः → श्लोकः and reads as one continuous story. Each verse has these layers:
1. मूलश्लोकः: Devanagari, sandhi-joined (as in the base text).
2. पदच्छेदः: sandhi-split form. The existing **Padaccheda toggle** switches mūla ⇄ padaccheda and back.
3. पदार्थः: every pada, with its meaning in **simple Sanskrit** (no English).
4. अन्वयः: prose order.
5. सरलसंस्कृतव्याख्या: a short story-style explanation in simple Sanskrit that **reuses the verse's own padas** and stays consistent with the previous verses.
English is deferred. Leave reserved fields for it but generate nothing. Build the pipeline for reuse: the Mahābhārata comes next.

## 1. Relationship to the existing site (do not redesign)
- The existing site is **Vedanta Pathashala** (`NKAditya1729/sarala-vedanta`, GitHub Pages: https://nkaditya1729.github.io/sarala-vedanta/). It follows the Advaita Sharada (advaitasharada.sringeri.net) look. Repo root: `index.html`, `favicon.svg`, `.nojekyll`, `images/`, plus one folder per text: `mandukya-1/`, `maitreyi/`, `madhu/`, `brahmasutra-1/`, `manasollasa/`, `sanatsujatiya/`, `vishnu-sahasranama/`. The README says `mandukya-1/` is "built from the builder's out-mandukya-1-b1", and `maitreyi/` and `madhu/` are copies from `NKAditya1729/vedantic-archive` `public/source-text/sarala*/`. So pages are pre-built, and a separate builder exists.
- **Phase 0 (mandatory):** clone `sarala-vedanta` and `vedantic-archive` and find the builder. Inventory and document in `docs/EXISTING_DESIGN.md`:
  - CSS files and design tokens
  - fonts
  - header/nav and sidebar layout
  - the अध्ययनसाहाय्यम् panel markup
  - the **Padaccheda toggle** (its DOM, classes, JS and data attributes)
  - how padārtha / anvaya / vyākhyā are currently rendered
  - how pages are generated
  Ask the user for the builder location if you cannot find it.
- Reuse those CSS and JS components as they are. New UI should only *compose* existing components: a kāṇḍa index, a sarga index, a continuous verse list, and the per-verse expandable panel with पदार्थः / अन्वयः / सरलव्याख्या tabs. Any new style must use existing tokens. Do not add a framework. Keep the site static (plain HTML, CSS, vanilla JS), as now.
- Deploy target: either a new folder `ramayanam/` inside `sarala-vedanta`, or a sibling repo linked from its index. **Ask the user** (open decision D6).

## 2. Sources, acquisition, provenance
| Role | Source | How to get it | Licence → action |
|---|---|---|---|
| **Base mūla** | Sanskrit Wikisource vulgate (`https://sa.wikisource.org/wiki/रामायणम्/बालकाण्डम्/सर्गः_१` …) | `git clone https://github.com/svenkatreddy/Ramayana_Book` → `san/*_all.json`; pin the commit in `sources/sources.json`. Optionally re-fetch sargas via the MediaWiki API to diff. | CC BY-SA 4.0 → attribute; site content licensed CC BY-SA 4.0 |
| Base caveat | Kiṣkindhā 11, Yuddha 25, Yuddha 31 restored from IITK in Ramayana_Book | Diff against Wikisource page history or a PD scan (Nirnaya Sagar 1930, archive.org) | Set `provenance` per verse; flag for review |
| Crosswalk / CE | GRETIL Rāmāyaṇa TEI-XML (Tokunaga/Smith) | `https://gretil.sub.uni-goettingen.de/` (Ramayana → TEI XML); IDs like `1.001.001a` | CC BY-NC-SA 4.0 → **internal use only, never publish CE text** |
| **Padaccheda seed** | DCS CoNLL-U | `git clone https://github.com/OliverHellwig/sanskrit` → `dcs/data/conllu/files/Rāmāyaṇa*`; also `https://github.com/ambuda-org/dcs` `ramayanam.txt` | CC BY 4.0 → attribute "Oliver Hellwig, DCS 2010–2024" |
| Prior art | `https://github.com/hms-cap/Ramayana` (`etl/ingest_vulgate.py`, `etl/crosswalk.py`, `etl/meter.py`, `etl/ingest_dcs.py`) | Read; reuse ideas/code with MIT attribution | MIT |
| Private cross-check | IITK `https://www.valmiki.iitk.ac.in/sloka?field_kanda_tid=1&language=dv&field_sarga_value=1`; valmikiramayan.net | Polite, cached, rate-limited fetch (≤1 req/2 s) to `cache/` (git-ignored) | No reuse grant → **never publish**; compare only |

Write `sources/sources.json` (URL, commit/date, licence, use). Write a site "आधाराः / Sources" page with the attributions: Wikisource contributors (CC BY-SA 4.0), DCS (CC BY 4.0), and "generated explanations reviewed by …".

### Normalisation rules (`scripts/normalize.py`)
- Unicode **NFC**. Devanagari only in content fields. Use `।` (U+0964) and `॥` (U+0965), never `|` or `||`. Keep avagraha `ऽ`. Convert stray Latin digits in verse numbers to Devanagari for display; store integers in data.
- Anusvāra vs. homorganic nasal: store the base text as is (e.g. पुङ्गवम्). Do not "fix" it. Record any optional display normalisation as a setting.
- Verse ID: `VR.{kanda}.{sarga}.{shloka}` (e.g. `VR.1.1.1`), using the **Wikisource/Ramayana_Book numbering**. Keep the original marker (`॥१-१-१॥`) in `src_ref`. For sub-numbered or duplicated numbers, use suffixes `VR.6.25.12a` and log them in `data/meta/anomalies.json`.
- Split into **pādas** where the text gives half-verse breaks (`।`). Anuṣṭup = 2 lines × 2 pādas of 8 syllables. Six-pāda verses keep 3 lines (`lines: [..3]`). Treat half-ślokas as their own entries and flag them `half: true`.
- Non-Anuṣṭup metres (triṣṭubh, upajāti and others, common at sarga ends): keep their line structure and record `metre`.
- Colophon (`इत्यार्षे श्रीमद्रामायणे …सर्गः ॥`): store as `sarga.colophon`, not as a verse. Sarga title: derive a short Sanskrit title (see §5) and keep any source heading in `source_heading`.
- Validate counts per sarga against Ramayana_Book's `scripts/validate-content.js` totals. Write `data/meta/counts.json` with per-kāṇḍa sargas and verses. Expected sargas: 77/119/75/67/68/128/111 = 645, and about 23,334 verses.

## 3. Information architecture
- URLs (static):
  - `/ramayanam/` → kāṇḍa index
  - `/ramayanam/1/` → sarga index for Bāla (sarga number, title, verse count, layer-completion badge)
  - `/ramayanam/1/1/` → sarga reader
  - `#VR.1.1.1` → verse anchor
- Pages are thin HTML shells. The reader loads `data/vr/{k}/{sss}.json` (e.g. `data/vr/1/001.json`) with `fetch`, and IntersectionObserver lazily renders the expanded panels.
- Navigation:
  - prev/next sarga, crossing kāṇḍa boundaries
  - kāṇḍa → sarga breadcrumbs
  - "jump to verse"
  - a sticky global Padaccheda toggle, which sets all verses, plus the per-verse toggle
- Reading flow: verses appear one after another. Clicking a verse opens a panel below it with tabs **पदार्थः · अन्वयः · सरलव्याख्या**. Show the metre name and speaker as small badges if D4 = yes.
- Search: a build-time index (`data/search/{k}.json`) of mūla and padaccheda tokens, normalised to SLP1 via vidyut-lipi, so users can search in Devanagari or plain Roman. Load it on demand per kāṇḍa.

## 4. Data schema (one file per sarga)
```json
{
  "schema_version": 1,
  "work": "VR",
  "kanda": 1, "kanda_name": "बालकाण्डम्",
  "sarga": 1,
  "title": "नारदवाल्मीकिसंवादः — संक्षेपरामायणम्",
  "source_heading": null,
  "colophon": "इत्यार्षे श्रीमद्रामायणे वाल्मीकीये आदिकाव्ये बालकाण्डे प्रथमः सर्गः ॥१-१॥",
  "summary_sa": "नारदः वाल्मीकये रामस्य गुणान् सम्पूर्णं रामचरितं च संक्षेपेण वदति ।",
  "context_in_sa": "(पूर्वसर्गस्य सारः — प्रथमसर्गे रिक्तम्)",
  "verse_count": 100,
  "provenance": {"text": "sa.wikisource via Ramayana_Book@<commit>", "padaccheda_seed": "DCS|dharmamitra|llm"},
  "verses": [ { "...": "see verse object" } ],
  "status": {"mula": "done", "padaccheda": "done", "padartha": "draft", "anvaya": "draft", "vyakhya": "draft", "human_review": "pending"}
}
```
Verse object:
```json
{
  "id": "VR.1.1.1",
  "n": 1,
  "src_ref": "॥१-१-१॥",
  "lines": ["तपः स्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।", "नारदं परिपप्रच्छ वाल्मीकिर्मुनिपुङ्गवम् ॥"],
  "padaccheda_lines": ["तपः-स्वाध्याय-निरतम् तपस्वी वाग्विदाम् वरम् ।", "नारदम् परिपप्रच्छ वाल्मीकिः मुनि-पुङ्गवम् ॥"],
  "metre": {"name": "अनुष्टुप्", "checked_by": "vidyut.chandas", "ok": true},
  "speaker": null,
  "context_note_sa": "वाल्मीकिः नारदं प्रश्नं पृच्छति ।",
  "crosswalk": {"ce": "1.1.1", "relation": "same"},
  "padartha": [
    {"pada": "तपः-स्वाध्याय-निरतम्", "pratipadika": "तपःस्वाध्यायनिरत", "linga": "पुं", "vibhakti": "द्वितीया", "vacana": "एक",
     "vigraha": "तपसि स्वाध्याये च निरतः, तम्", "artha": "तपसि वेदपठने च सदा संलग्नम्", "anvita": "नारदम्"},
    {"pada": "तपस्वी", "pratipadika": "तपस्विन्", "linga": "पुं", "vibhakti": "प्रथमा", "vacana": "एक", "artha": "तपः कुर्वन्, तपोयुक्तः", "anvita": "वाल्मीकिः"},
    {"pada": "वाग्विदाम्", "pratipadika": "वाग्विद्", "linga": "पुं", "vibhakti": "षष्ठी", "vacana": "बहु", "vigraha": "वाचं विदन्ति इति वाग्विदः, तेषाम्", "artha": "वचनज्ञानां जनानाम्"},
    {"pada": "वरम्", "pratipadika": "वर", "linga": "पुं", "vibhakti": "द्वितीया", "vacana": "एक", "artha": "श्रेष्ठम्", "anvita": "नारदम्"},
    {"pada": "नारदम्", "pratipadika": "नारद", "linga": "पुं", "vibhakti": "द्वितीया", "vacana": "एक", "artha": "नारदमुनिम्"},
    {"pada": "परिपप्रच्छ", "dhatu": "प्रच्छ्", "upasarga": "परि", "lakara": "लिट्", "purusha": "प्रथम", "vacana": "एक", "artha": "पृष्टवान्"},
    {"pada": "वाल्मीकिः", "pratipadika": "वाल्मीकि", "linga": "पुं", "vibhakti": "प्रथमा", "vacana": "एक", "artha": "वाल्मीकिमुनिः"},
    {"pada": "मुनि-पुङ्गवम्", "pratipadika": "मुनिपुङ्गव", "linga": "पुं", "vibhakti": "द्वितीया", "vacana": "एक", "vigraha": "मुनिषु पुङ्गवः", "artha": "मुनिश्रेष्ठम्", "anvita": "नारदम्"}
  ],
  "anvaya": "तपस्वी वाल्मीकिः तपःस्वाध्यायनिरतं वाग्विदां वरं मुनिपुङ्गवं नारदं परिपप्रच्छ ।",
  "vyakhya_sa": "वाल्मीकिः नाम एकः मुनिः आसीत् । सः **तपस्वी** आसीत् । **नारदः** अपि महान् मुनिः । नारदः सदा **तपसि** **स्वाध्याये** च **निरतः** । सः **वाग्विदां वरः** — वचनं जानतां सर्वेषां मध्ये श्रेष्ठः । सः **मुनिपुङ्गवः** — मुनीनां श्रेष्ठः । तादृशं नारदं **वाल्मीकिः** एकं प्रश्नं **परिपप्रच्छ** — पृष्टवान् ।",
  "vyakhya_used_padas": ["तपस्वी", "नारदः", "तपसि", "स्वाध्याये", "निरतः", "वाग्विदां", "वरः", "मुनिपुङ्गवः", "वाल्मीकिः", "परिपप्रच्छ"],
  "en_simple": null,
  "en_mixed": null,
  "review": {"auto_checks": {"rejoin": true, "coverage": true, "metre": true, "schema": true},
             "agent_review": "pass", "human": "pending", "flags": [], "notes": ""},
  "gen": {"model": "", "date": "", "prompt_version": "v1"}
}
```
Rules: `padaccheda_lines` must have the same line count as `lines`. `padartha` is in verse order and covers every pada in `padaccheda_lines`; indeclinables like च, नु, तु, हि get an entry with `"avyaya": true`. `en_simple` and `en_mixed` stay `null` until Phase 4.

## 5. Content-generation guidelines

### 5.1 पदच्छेदः
- Space = pada boundary. Hyphen `-` = samāsa member boundary, display-optional (D3). Restore each pada's **pausal form**: final `म्` (not `ं`), visarga `ः` (not र्/ओ/स्), the original vowels split out of vowel sandhi (वाल्मीकिर्मुनि → वाल्मीकिः मुनि; को न्वस्मिन् → कः नु अस्मिन्).
- Keep compound-internal sandhi inside a member, but split at member boundaries: तपःस्वाध्याय → तपः-स्वाध्याय. Avagraha: एषोऽब्रवीत् → एषः अब्रवीत्.
- Keep the `।` / `॥` positions identical to the mūla.
- **Re-joinability is mandatory.** Applying external sandhi to the padaccheda, with hyphens removed, must reproduce the mūla after normalising anusvāra and nasals (§7).
- Priority of sources: DCS form (via crosswalk) → Dharmamitra `unsandhied` → Claude. When two disagree, flag it. Never edit the mūla to make a split pass.

### 5.2 पदार्थः (simple Sanskrit)
- Use the commonest synonym or short paraphrase, in the **same vibhakti and vacana** as the pada (वरम् → श्रेष्ठम्; परिपप्रच्छ → पृष्टवान्). Prefer everyday words; avoid rare kośa words.
- Compounds get a one-line simple vigraha. Verbs get धातु + उपसर्ग + लकार + पुरुष/वचन, then a simple equivalent (often a क्तवतु/क्त form or लट्).
- Proper names: give a short identifier (कौसल्या → रामस्य माता). Vocatives: "हे …, (सम्बोधनम्)".
- No English. No doctrinal glosses.

### 5.3 अन्वयः
- Vocatives first. Then kartṛ with its viśeṣaṇas, then karma with its viśeṣaṇas, then other kārakas (करण, सम्प्रदान, अपादान, अधिकरण), then kriyā. Put each viśeṣaṇa immediately before its viśeṣya.
- Put supplied (adhyāhāra) words in parentheses: (अस्ति), (सः). Indeclinables like च, नु, इति stay with what they connect.
- In questions, put the interrogative where natural prose puts it.
- Use joined forms, with minimal sandhi (only obligatory internal and compound sandhi). Every pada of the verse must appear exactly once, plus any supplied words.

### 5.4 सरलसंस्कृतव्याख्या
- Write 3–8 short sentences, each 4–10 words, in लट् or simple past (क्तवतु or लङ्), with minimal external sandhi.
- **Reuse every significant pada** (nouns, verbs, adjectives) of the verse, bolded with `**…**`, in its original form or the form the new sentence needs. Gloss hard words in apposition with "— अर्थात् …".
- Continue the story: open with a link to the previous verse, using `context_in_sa` and the previous verse's `vyakhya_sa`. Name the speaker in dialogues ("नारदः वदति — …").
- Add nothing the verse does not say beyond minimal connective context. No philosophy, no commentary debates, no other recensions or later works.
- **Do not repeat the padārtha.** Use the verse's words in natural connected sentences, and gloss with "अर्थात्" at most 2–3 hard words per verse (ruling of 2026-11-11, see §5.7).

### 5.5 Sarga summary
After a sarga is finished, write `summary_sa` (2–4 simple sentences). The next sarga's `context_in_sa` = the previous `summary_sa` plus the last 3 verses' vyākhyā. This is how the story context carries forward.

### 5.6 Second worked example (VR.1.1.2)
- mūla: को न्वस्मिन् साम्प्रतं लोके गुणवान् कश्च वीर्यवान् । धर्मज्ञश्च कृतज्ञश्च सत्यवाक्यो दृढव्रतः ॥
- padaccheda: कः नु अस्मिन् साम्प्रतम् लोके गुणवान् कः च वीर्यवान् । धर्म-ज्ञः च कृत-ज्ञः च सत्य-वाक्यः दृढ-व्रतः ॥
- padārtha:
  - कः: कः पुरुषः
  - नु: (प्रश्ने) खलु
  - अस्मिन् लोके: एतस्मिन् जगति
  - साम्प्रतम्: इदानीम्
  - गुणवान्: सद्गुणैः युक्तः
  - वीर्यवान्: पराक्रमी
  - धर्म-ज्ञः: धर्मं जानाति इति
  - कृत-ज्ञः: अन्यैः कृतम् उपकारं स्मरति इति
  - सत्य-वाक्यः: सत्यं वदति इति
  - दृढ-व्रतः: स्वनियमे स्थिरः
- speaker: वाल्मीकिः (to नारदम्).
- anvaya: (हे नारद,) साम्प्रतम् अस्मिन् लोके गुणवान् कः नु (अस्ति)? वीर्यवान् च कः? धर्मज्ञः च कृतज्ञः च सत्यवाक्यः दृढव्रतः च (कः)?
- vyākhyā: वाल्मीकिः नारदं पृच्छति — "**अस्मिन् लोके** **साम्प्रतम्** अर्थात् इदानीं **गुणवान्** **कः** अस्ति? **वीर्यवान्** **कः**? **धर्मज्ञः** **कृतज्ञः** च कः? **सत्यवाक्यः** — सदा सत्यं वदति, **दृढव्रतः** — स्वनियमं न त्यजति — तादृशः पुरुषः कः?"

### 5.7 Rulings from the pilot (Aditya, 2026-11-11)
These were decided on verses 1–5 of VR.1.1 and hold for every verse. Where the
worked examples of §4 and §5.6 differ, **these rulings win**.

**Padaccheda (§5.1)**
- Hyphenate at every member boundary, with each member in its pausal form:
  `वाक्-विदाम्`, `महा-ऋषे`, `कृत-ज्ञः`, `एवम्-विधम्`.
- A नञ्-compound is **not** hyphenated (`अनसूयकः`, `अदीनात्मा` → `अदीन-आत्मा`): अ / अन्
  is not a pada. Its vigraha is still given (न असूयकः).

**Padārtha (§5.2)**
- **A gloss must be simpler than the word.** If the word is already simple
  (देवाः, इच्छामि, ज्ञातुम्), give a short paraphrase, never a rarer synonym
  (not सुराः, वाञ्छामि, अवगन्तुम्).
- The gloss stays in the pada's own vibhakti and vacana (धर्मज्ञः → धर्मं जानन्);
  the clause form (धर्मं जानाति इति) belongs in the vigraha.
- **Gender:** follow the **Amarakośa first, then Apte**. So संयुग is पुं.
- **नु** is glossed as a question particle (प्रश्नार्थकम् अव्ययम्), not as खलु.
- A word the gloss supplies beyond the pada stands in round brackets:
  एकप्रियदर्शनः → यस्य दर्शनं (सर्वेषां) प्रियम्, तादृशः अद्वितीयः.
- A vocative gloss has the form `हे …, (सम्बोधनम्)`.
- An epic usage is recorded as the form requires and explained in the gloss:
  कस्य (with बिभ्यति) is षष्ठी, gloss कस्य पुरुषस्य (कस्मात् इति अर्थः).
- Compounds of the व्याघ्रादि kind are explained as such: मुनिपुङ्गवः = मुनिः पुङ्गवः इव.
- एकप्रियदर्शनः is read as एकः (अद्वितीयः) प्रियदर्शनः.

**Anvaya (§5.3)**
- Every pada exactly once. Anything supplied, even a च, stands in parentheses.

**Vyākhyā (§5.4): do not repeat the padārtha**
- Tell the verse in natural, connected sentences that use the verse's own
  words. It is a retelling, not a word list.
- Use "— अर्थात् …" for **at most 2–3 hard words per verse** (`make check`
  fails on more than three). The other words are explained by the padārtha.
- A word before a pause (dash, comma, daṇḍa, question mark) or before a vowel
  ends in म्, not in anusvāra.

## 6. Pipeline and phases
- **Phase 0 – Inspect.** Do §1 and write `docs/EXISTING_DESIGN.md`. Set up the Python env (`uv init`; `uv add vidyut dharmamitra-sanskrit-grammar indic-transliteration jsonschema`). Download vidyut data per its docs.
- **Phase 1 – Mūla.**
  - `scripts/ingest_vulgate.py` reads Ramayana_Book JSON and writes per-sarga files with `lines` and colophons.
  - `normalize.py`, then `counts.json`.
  - Metre scan with `vidyut.chandas`; list non-Anuṣṭup verses and anomalies.
  - Build all kāṇḍa, sarga and reader pages and deploy. **The whole Rāmāyaṇa readable = milestone 1.**
- **Phase 2 – Padaccheda.**
  - `scripts/ingest_gretil.py` and `scripts/crosswalk.py`: align vulgate verses to CE verse IDs by normalised string similarity per sarga. Follow hms-cap's approach.
  - `scripts/seed_dcs.py`: CoNLL-U → padaccheda for `same` / `partial` verses.
  - `scripts/seed_dharmamitra.py`: batch the rest (cache responses, respect rate limits).
  - `scripts/check_rejoin.py` on everything. Failures go to a Claude adjudication queue (`queue/padaccheda_fix.jsonl`) with both candidates, the IITK gloss line (private cache), and the instruction "do not change the mūla".
  - Deploy the toggle for all verses = milestone 2.
- **Phase 3 – Padārtha + anvaya + vyākhyā.**
  - **Pilot: VR.1.1 (100 verses) only**, then stop for user / Swamiji review and revise this file's §5 rules.
  - Then go sarga by sarga in order, so story context is preserved. One generator sub-agent per sarga writes the draft. A separate reviewer sub-agent checks it against §5 and §7 and returns a diff or flags. The main agent merges, runs the checks and commits.
  - Never generate a sarga before its predecessor's `summary_sa` exists.
- **Phase 4 – English layers** (`en_simple`, `en_mixed`), later and only on request.
- **Phase 5 – Mahābhārata.**
  - Keep everything work-agnostic: `work` = `MB`, IDs `MB.{parvan}.{adhyaya}.{shloka}`, the same schema and scripts with configs in `works/vr.yaml` and `works/mb.yaml`.
  - The BORI e-text cannot be redistributed. Pick an openly licensed vulgate first.

### Resumability
- `progress/state.json`: per sarga `{phase, layer, status, attempts, last_error, commit}`.
- Every script is idempotent. It skips verses whose layer is `done` and whose input hash is unchanged. Write after each verse batch.
- Work in batches of about 20–40 verses per generation call, never splitting a sentence that spans verses. Keep the `context_in_sa` chain.
- `progress/LOG.md` is a human-readable diary.

## 7. Validation and QA (run `make check`; CI must pass)
1. **Schema:** `jsonschema` against `schema/sarga.schema.json`.
2. **Mūla integrity:** the hash of `lines` equals the ingest hash. No generator may change the mūla.
3. **Re-join:** sandhi-join(padaccheda without hyphens) == mūla, after normalising anusvāra ↔ म्/nasal, spaces and daṇḍa spacing. Use the `vidyut.sandhi` rules plus a small custom joiner. Log any mismatch with its position.
4. **Coverage:**
   - the multiset of padas in `padartha` equals the padas in `padaccheda`
   - every pada occurs in `anvaya` (hyphens stripped)
   - ≥80% of significant padas (non-avyaya) occur in `vyakhya_sa` (`vyakhya_used_padas` is recomputed, not trusted)
5. **Language hygiene:** no Latin letters in Sanskrit fields; NFC; only valid Devanagari ranges; sentence length limit in vyākhyā.
6. **Metre:** `vidyut.chandas` on the mūla. Flag unexpected metres, since they usually mean a typo or a wrong line split.
7. **Cross-checks (private):** DCS lemma vs. `padartha.pratipadika`; the IITK English gloss list as a word-boundary sanity check. Disagreements become `flags`.
8. **Reviewer agent:** checks grammar (vibhakti agreement in vyākhyā), consistency with the previous verses, and that there is no extra content.
9. **Human review:** sample 10% per sarga, plus every flagged verse, in `review/queue.md`. Set `review.human` to `approved` or `changes`, and show a small "समीक्षितम्" badge on the site.

Known LLM failure modes to look for:
- wrong splits (vowel-sandhi ambiguity, visarga restoration, compound vs. separate words)
- "improved" or hallucinated mūla, and verses from another recension
- wrong vibhakti or agreement in prose
- English leaking into Sanskrit fields
- doctrinal digressions

## 8. Build, deploy, performance
- Commits: `vr(1.1): padaccheda`, `vr(1.1): padartha+anvaya+vyakhya [pilot]`, `tools: …`. Make one commit per sarga per layer.
- Build: `scripts/build_site.py` writes static pages into the deploy folder. GitHub Pages serves them; keep `.nojekyll`.
- Performance: per-sarga JSON (expect about 100–400 KB with all layers; gzip-served), lazy panel rendering, and per-kāṇḍa search shards. Total data is about 50–120 MB. Keep repo assets small, and do not commit `cache/`.

## 9. Open decisions (ask the user before Phase 1, record answers in `docs/DECISIONS.md`)
- D1 Recension: Wikisource vulgate as base (recommended) or IITK numbering? Show CE crosswalk badges?
- D2 Include Uttara Kāṇḍa (recommended: yes, as 7th kāṇḍa, marked)?
- D3 Show samāsa hyphens in the padaccheda view, or spaces only (hyphens kept in data)?
- D4 Show metre name and speaker badges?
- D5 Verse numbering when sources differ: the Wikisource numbering, with alternates in `src_ref`?
- D6 Deploy inside `sarala-vedanta/ramayanam/` or as a separate repo?
- D7 Site content licence: CC BY-SA 4.0 (required by the Wikisource base)?

## 10. Skills and review structure

### 10.1 Skills inventory (Phase 0, before any other work)
- List every installed skill and plugin. Read the description of each one.
- Write `docs/SKILLS.md`: a table of skill → what it does → which phase of this
  project uses it → "use" or "skip, because …".
- If the Matt Pocock skills are installed, run their one-time repo setup skill
  first (issue tracker, labels, domain docs), then use them as below.
- Load a skill only when its phase starts. Do not load all skills at once.

### 10.2 Which skills to use where (use the installed equivalents)
- Planning: a grilling/interview skill to resolve the open decisions in §9 with
  the user; a spec skill to turn each phase into a written spec; a tickets or
  wayfinder skill to break Phases 1–3 into tracked, resumable tickets.
- Building scripts (ingest, normalize, crosswalk, re-join checker, validators,
  site builder): test-driven development. Write the failing test first. The
  re-join checker and coverage checker need tests built from real verses,
  including known hard cases (avagraha, visarga, vowel sandhi, compounds).
- Debugging: a systematic-debugging/diagnosis skill, never guess-and-patch.
- Code review: run a code-review skill on every script change before commit.
  For the validators and the crosswalk, use a multi-reviewer or review-council
  skill if one is installed.
- Completion: a verification-before-completion skill. Never report a phase or
  a sarga as done without the output of `make check` shown.
- Session ends: a handoff skill, writing to `progress/HANDOFF.md`.
- Domain vocabulary: a domain-modeling skill to keep a glossary (kāṇḍa, sarga,
  pada, padaccheda, anvaya, …) in `CONTEXT.md` so terms stay consistent.

### 10.3 Content review (the installed skills do not cover this)
Code-review skills check code, not Sanskrit. Content review follows this
project's own rules:
- Generator and reviewer are always separate sub-agents. The reviewer gets the
  mūla, the draft, §5 and §7, and no access to the generator's reasoning.
- The reviewer returns a per-verse verdict (pass / fix / flag-for-human) with
  the rule number it relies on. Fixes go back to the generator once; a second
  failure becomes a human-review flag, not a third attempt.
- If a skill-creation skill is installed, package §5 and §7 as a project skill
  `ramayana-content-review` after the pilot, so every reviewer sub-agent loads
  the same checklist.
- No sarga is committed until: automated checks pass, reviewer verdicts are
  recorded in `review`, and flagged verses are in `review/queue.md`.

## 11. Stages, models and stop gates

This project runs in three stages. Do only the stage you are told to do,
and stop at its gate. Do not continue into the next stage on your own.

### Stage A: Phases 0, 1 and 2a (run on Opus 5.5, high effort)
Scope:
- Phase 0: existing-site inspection and the skills inventory (§10.1).
- Confirm open decisions D1–D7 (§9) with the user before Phase 1.
- Phase 1: complete mūla ingested, normalised, counted, published.
- Phase 2a: crosswalk, DCS seeding, Dharmamitra seeding, the re-join
  checker with its tests, and the check run over every verse.
Not in scope:
- Do NOT resolve verses that fail the re-join check or where the seed
  sources disagree. Write them to `queue/padaccheda_fix.jsonl` with both
  candidates and the failure position, and leave them.
- Do NOT generate padārtha, anvaya or vyākhyā for any verse.

Gate A: write `docs/STAGE_A_REPORT.md` and stop. It must contain:
1. Sargas and verses per kāṇḍa, and every anomaly logged.
2. Crosswalk results: verses matched to the Critical Edition exactly,
   partly, not at all.
3. Padaccheda seeding: count from DCS, count from Dharmamitra, and the
   re-join pass rate for each.
4. The re-join checker's normalisation rules, stated exactly, and the
   list of hard cases it is tested on.
5. 30 random verses (mūla and padaccheda side by side) and 30 verses
   from the failure queue.
6. Answers recorded for D1–D7, and any deviation from this file.
7. Known problems and anything you were unsure about.

### Stage B and after (replaces the earlier Stage B and C; decided 2026-11-11)

The working instructions for Stage B are in `docs/STAGE_B_BRIEF.md`. Where
that brief and this file disagree, the brief wins.

**Why the plan changed.** The Stage B review (`docs/STAGE_B_REVIEW.md`) found
that passing the re-join check does not mean a split is correct: about 8–9%
of the passing machine seeds have a wrong letter or word boundary. So the
padaccheda is **not** fixed for the whole epic first.

- **Machine seeds are hints only.** Every seeded verse carries
  `padaccheda_status: "seed"` and the site marks it असमीक्षितम्.
  `queue/padaccheda_fix.jsonl` is not resolved in bulk.
- **Padaccheda is finalised sarga by sarga**, together with padārtha, anvaya
  and vyākhyā (§5.1–§5.5), by a generator and a separate reviewer (§10.3). A
  verse becomes `padaccheda_status: "reviewed"` only then. Seeding scripts
  never overwrite a `reviewed` verse.
- **Order of work:** review of Stage A → approved fixes → pilot VR.1.1 (100
  verses, all layers) → stop for the user's and Swamiji's review → then sarga
  by sarga as in §6, never starting a sarga before its predecessor's
  `summary_sa` exists.
- **Gates.** Stop after the review, after the approved fixes (before any
  merge to `main`), after verses 1–5 of the pilot, and after the pilot sarga.
  Never push or merge to `main` without the user's explicit word.
- **Outside services.** No new calls to Dharmamitra until its terms are
  confirmed; re-seeding uses `cache/dharmamitra/` only
  (`scripts/seed_dharmamitra.py` refuses to call the network unless
  `DHARMAMITRA_ALLOW_NETWORK=1`).

## 12. Damaged or doubtful mūla (ruling of 2026-11-11)

The Wikisource text has typos, lost letters, stray characters and a few lines
that are not verses. The rule:

1. **`lines` always holds the Wikisource text, untouched.** No script and no
   generator may change it (§7.2 still checks its hash).
2. A verse that looks wrong gets the flag `mula_suspect` and a note in
   `review.notes`. A line that is not a verse at all (a commentary sentence
   numbered as a verse) gets `not_mula`. A machine split that disagrees with
   the printed avagraha gets `avagraha_mismatch`. Flags that must survive a
   re-ingest are listed in `data/meta/mula_flags.json` and applied by
   `scripts/flag_mula.py`.
3. **A correction goes in a new field `lines_corrected`** (same shape as
   `lines`), with
   `correction: {"what": …, "evidence": …, "approved_by": …, "date": …}`.
4. **No correction is applied without the user's approval, verse by verse.**
   Propose it with the Wikisource text, the proposed text, the evidence and
   the metre result; then wait.
5. On the site a corrected verse shows the corrected text with a small mark;
   the original stays visible on tap.
6. Padaccheda, padārtha, anvaya and vyākhyā of a corrected verse are written
   for `lines_corrected`, and the re-join check runs against it.

7. **How a correction is stored.** Approved corrections live in
   `data/meta/corrections.json` (one entry per verse: `id`, `lines_corrected`,
   `correction`); `scripts/apply_corrections.py` writes them into the sarga
   files. `make check` fails if the data holds a correction that is not in that
   file, or the reverse. `metre` then describes the corrected text
   (`"of": "lines_corrected"`) and `metre_source` keeps the result for the
   Wikisource text. Use `vrtools.build.text_lines(v)` wherever a script needs
   "the text of the verse".

Verse fields added in Stage B: `padaccheda_status` (`"seed"`, `"reviewed"` or
`null` when there is no split), `lines_corrected`, `correction` and
`metre_source` (absent until a correction is approved).

Approved so far (Aditya, 2026-11-11): VR.1.1.1 (space inside a compound),
VR.1.1.9, VR.1.1.45, VR.1.1.100.
