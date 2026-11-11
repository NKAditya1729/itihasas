# Glossary (domain terms used in code, data and docs)

| Term | Meaning here | In data / code |
|---|---|---|
| काण्डः kāṇḍa | One of the 7 books (बाल … उत्तर). | `kanda` 1–7 |
| सर्गः sarga | A chapter; 645 in the Wikisource vulgate. | `sarga`; file `data/vr/{k}/{sss}.json` |
| श्लोकः śloka / verse | One numbered verse as printed on Wikisource, whatever its metre. | `verses[]`, id `VR.k.s.n[suffix]` |
| pāda | A quarter-verse. Anuṣṭup: 8 syllables; long metres: 11–12. | — |
| line | One printed line of the verse. Usually a half-verse (2 pādas) ending in । or ॥; long-metre verses are often printed one pāda per line without a daṇḍa. | `lines[]` |
| sandhi unit | Consecutive lines up to one ending in a daṇḍa; sandhi applies inside a unit, not across a daṇḍa. | `sandhi.units()` |
| मूलम् mūla | The verse text exactly as the base source has it (only encoding normalised). Never edited by any generator. | `lines`, hash in `data/meta/mula_hashes.json` |
| half-split source | A Wikisource passage typed with sandhi undone (एतत् इच्छामि अहम्…), i.e. not true saṃhitā. Kept as is and flagged. | flag `source_presplit` |
| पदच्छेदः padaccheda | The verse with every pada in pausal form: spaces between padas, hyphens between compound members. | `padaccheda_lines[]` |
| pausal form | The form a word has before a pause: final म्, visarga ः, original vowels. | — |
| group | One space-separated token of the mūla paired with the padas it contains, for the Padaccheda toggle. | `groups[line][] = [sandhi, pada, flag]` |
| re-join check | Sandhi-joining the padaccheda must reproduce the mūla (after the narrow normalisation in `sandhi.norm`). | `sandhi.check_rejoin` |
| seed | Where a padaccheda came from: `dcs` (Digital Corpus of Sanskrit, via the crosswalk) or `dharmamitra` (ByT5 segmenter). | `seed.source` |
| CE | Baroda Critical Edition (GRETIL). Used internally only. | `crosswalk.ce` |
| crosswalk | Link from a vulgate verse to a CE verse: same / partial / variant / absent. | `crosswalk` |
| prakṣipta appendix | A passage Wikisource prints after a sarga's colophon, marked प्रक्षिप्तः (only 3.56). | `appendix`, ids `VR.3.56A.n` |
| पदार्थः padārtha | Meaning of each pada in simple Sanskrit (Phase 3). | `padartha[]` |
| अन्वयः anvaya | Prose order of the verse (Phase 3). | `anvaya` |
| सरलव्याख्या vyākhyā | Short story-style simple-Sanskrit explanation reusing the verse's padas (Phase 3). | `vyakhya_sa` |
