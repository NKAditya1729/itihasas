# Human review queue

Verses for the human reviewer (CLAUDE.md §7.9, §10.3): every verse that a reviewer sub-agent flagged, the
declared exceptions, the doubtful source readings, and a 10% sample of the rest. Set `review.human` to
`approved` or `changes` in the sarga file when a verse has been looked at. The reviewers' full notes are in
`review/drafts/*.review.json`.

## Bāla-kāṇḍa, sarga 1 (pilot; all 100 verses)

Reviewer verdicts: 74 pass, 26 flag. Each batch had one fix round and a final review pass.

### 1. Decisions waiting for Aditya

| Verse | Wikisource text | Proposed correction (not applied) | Why |
|---|---|---|---|
| VR.1.1.15 | …तत्त्वज्ञो स्मृतिमान् | …तत्त्वज्ञः स्मृतिमान् | a final ओ before स् is not possible sandhi |
| VR.1.1.29 | शृङ्गवीरपुरे | शृङ्गवेरपुरे | the usual name; so elsewhere in this text |
| VR.1.1.65 | प्रेक्ष्य चास्ति महाबलः | प्रेक्ष्य चास्थि महाबलः | अस्थि (the bones of Dundubhi) is the object of प्रेक्ष्य; the verse is explained as printed |
| VR.1.1.84 | सर्वदेवतैः | सर्वदैवतैः | देवत is not a regular a-stem; the Critical Edition reads दैवतैः |
| VR.1.1.85 | अभ्यषिच्य | अभ्यषिञ्चत् | an augment with ल्यप् is not a possible form; so the Critical Edition |
| VR.1.1.17, 43, 57 | सर्व गुणोपेतः · परम प्रीतः · सोऽभ्य गच्छन् | the space removed (as approved for VR.1.1.1) | a space inside a word or compound |

Also open: the reading of एकप्रियदर्शनः (VR.1.1.3: एकः (अद्वितीयः) प्रियदर्शनः is shown, by ruling; the alternative
is the bahuvrīhi एकम् (सदा) प्रियं दर्शनं यस्य); whether the padārtha may identify persons beyond what sarga 1
itself tells (kept, on CLAUDE.md §5.2: e.g. वाली = सुग्रीवस्य अग्रजः); deletion of the duplicate "… 2" / "… 3" files.

### 2. Declared re-join exceptions

The printed text of these verses cannot be re-joined from a correct padaccheda, so each carries a
`rejoin_note`; `make check` lists them and does not fail them. The reviewers judged each split on its merits.

| Verse | Note |
|---|---|
| VR.1.1.15 | The printed text has तत्त्वज्ञो स्मृतिमान् (a final ओ before स्, which is not possible sandhi); the padaccheda तत्त्व-ज्ञः स्मृतिमान् is right on its merits. A correction तत्त्वज्ञः has been proposed to the owner and is not applied. |
| VR.1.1.32 | The printed text leaves संकाशाः तत्र unjoined (regular sandhi: -संकाशास्तत्र); the padaccheda is right on its merits. |
| VR.1.1.34 | The printed text leaves नैच्छत् राज्यं unjoined (regular sandhi: नैच्छद्राज्यं); the padaccheda is right on its merits. |
| VR.1.1.37 | The printed text leaves आदेशात् राज्यं unjoined (regular sandhi: आदेशाद्राज्यं); the padaccheda is right on its merits. |
| VR.1.1.62 | The printed text leaves प्रणयात् दुःखितेन unjoined (regular sandhi: प्रणयाद्दुःखितेन); the padaccheda is right on its merits. |
| VR.1.1.64 | The printed text leaves सुग्रीवः महापर्वतसन्निभम् unjoined (regular sandhi: सुग्रीवो महा-); the padaccheda is right on its merits. |
| VR.1.1.70 | The printed text leaves सुग्रीववचनात् हत्वा unjoined (regular sandhi: -वचनाद्धत्वा); the padaccheda is right on its merits. |
| VR.1.1.91 | The printed text leaves केचित् द्रक्ष्यन्ति unjoined (regular sandhi: केचिद्द्रक्ष्यन्ति); the padaccheda is right on its merits. |
| VR.1.1.92 | The printed text leaves किञ्चित् नापि unjoined in line 2 (regular sandhi: किञ्चिन्नापि, as line 1 has); the padaccheda is right on its merits. |
| VR.1.1.96 | The printed text leaves राजवंशान् शतगुणान् unjoined (regular sandhi: -वंशाञ्छतगुणान्); the padaccheda is right on its merits. |
| VR.1.1.100 | The printed text leaves वणिक् जनः unjoined (regular sandhi: वणिग्जनः; the Critical Edition has the compound); the padaccheda is right on its merits. |

### 3. Verses flagged by the reviewers (points for Swamiji)

| Verse | Reviewer's note (shortened) |
|---|---|
| VR.1.1.3 | The vyākhyā is unchanged since the third review, where it was found correct on rules 1–7 and grammar; it needs no change. Rule 9: इत्युक्ते once (चारित्रम् इत्युक्ते शोभनम् आचरणम्); इति आशयः once; the rest by यः … सः, यं … सः and चेत्. Rule 10: a verse of questions; विद्वान् is rightly left undefined. Stretching constructions as counted before: two (पृच्छ्यते, दृष्ट्वा). The flag only carries forward the STANDING … |
| VR.1.1.9 | Sound. Point for the scholar: हनु is treated as feminine (vigraha महत्यौ हनू; vyakhya हनू च पुष्टे). This follows the Amarakosa (तत्परा हनुः) as I recall it from memory; Apte gives m. and f. Please confirm against the kosa. Small teaching point: हनु (jaw) is used in the vyakhya without explanation, though the padartha explains it. |
| VR.1.1.10 | No definite error. Padaccheda points for the scholar: (1) अरिम्-दमः: the boundary is right and अरिम् is the first member as it stands in the compound (अरि + मुम् augment before खच्), so it is a principled split, not an accidental re-join; but the म् is not a second-case ending and the vigraha is अरीन् दमयति, so a learner may misread it; the seed kept अरिन्दमः whole. (2) महा-इषु-आसः: correct by the कृत-ज्ञः ruling … |
| VR.1.1.13 | Sound. Point for the scholar: प्रजा-पति-समः splits प्रजापति, which here stands for Brahma and works as a proper name (rule: proper names whole); the draft treats it as a transparent epithet, as it does धनद in verse 19. Decide the convention for name-like epithets. Style suggestion only: यत्र सर्वे जीवाः वसन्ति सः जीवलोकः would have a matched correlative as यस्मिन् सर्वे जीवाः वसन्ति सः जीवलोकः. |
| VR.1.1.15 | The draft is sound and the padaccheda is right on its own merits (तत्त्व-ज्ञः स्मृतिमान्; अदीन-आत्मा as ruled). The one checker error is the known fault of the printed text (तत्त्वज्ञो स्मृतिमान् for तत्त्वज्ञः स्मृतिमान्): the verse needs the mula_suspect flag and an approved lines_corrected (§12) before the re-join check can pass. Small teaching point: दीनम् is used to explain अदीनात्मा without itself being … |
| VR.1.1.19 | Sound. Points for the scholar: (1) the sentence runs from 19cd to 21ab; the anvayas of 19, 20 and 21 mark this with a bracketed pointer (... इति अग्रे सम्बन्धः), and the vyakhyas point forward without telling what follows. This is honest; please confirm it as the convention for multi-verse sentences. (2) धन-देन splits an epithet that works as a name of Kubera (see verse 13). The opening sentence (अस्मिन् श्लोके ... … |
| VR.1.1.25 | Second pass: the rewritten vyākhyā is correct (5 sentences; यदा ... तदा, अतएव, अतः; one stretching construction, पालयन्; प्रस्थितः, अनुसृतवान् rightly formed; तं सुमित्रानन्दवर्धनः इति वदति has the nominative before इति, as it should; all boundaries clean; every significant pada in bold; no gloss formula). No definite error. Counting standard for rule 5 in this batch: I count what the vyākhyā itself introduces; the … |
| VR.1.1.29 | Second pass: the rewritten vyākhyā is correct and now reads as story (5 sentences, one इत्युक्ते; अनुज्ञातवान् rightly formed; नगरं प्रति is gone from the vyākhyā; धर्मात्मा explained by a plain sentence with अतएव). No definite error. STANDING POINT, MŪLA (§12): the text reads शृङ्गवीरपुरे. In the project's own Wikisource cache the town is शृङ्गिबेरपुर about 22 times, शृङ्गवेरपुर 4 times, शृङ्गिवेरपुर 3 times, and … |
| VR.1.1.31 | The prescribed padārtha fix is in (कृत्वा → (आवसथस्य) निर्माणं कृत्वा). The rewritten vyākhyā is good story prose (4 sentences, one इत्युक्ते, gerund and passive sharing the agent in अनुप्राप्य तैः ... कृतः) but has ONE DEFINITE ERROR of agreement in its last sentence: तं सुन्दरं गृहं कृत्वा. गृह in the singular is neuter (Amarakośa: गृहं गेह ..., and गृहाः पुंसि च भूम्न्येव, masculine only in the plural; from … |
| VR.1.1.35 | Second pass: the rewritten vyākhyā is correct (5 sentences; यतः clauses, यः ... तं matched; gerunds प्राप्य and कृत्वा; the heavy आर्याणाम् इत्युक्ते gloss is gone). No definite error. STANDING POINTS FOR THE SCHOLAR. (1) आर्यभावपुरस्कृतः is analysed as a bahuvrīhi, आर्यभावः पुरस्कृतः येन सः. That requires the niṣṭhā to stand last against the general rule (the regular order would be पुरस्कृतार्यभावः; Pāṇini 2.2.36 … |
| VR.1.1.37 | Second pass: vyākhyā correct (the न्यास sentence is now a plain यत् ... तत् clause; one इति आशयः; पित्रा सः ... आदिष्टः, ते पादुके ... दत्ते verified). The one checker error is the known unjoined आदेशात् राज्यं. No definite error. STANDING POINT FOR THE SCHOLAR: अस्य. The draft records it as षष्ठी and glosses एतस्य भरतस्य (भरताय इति अर्थः), a genitive in the sense of the dative, in the manner of the ruling on कस्य … |
| VR.1.1.38 | Second pass: the rewritten vyākhyā is grammatically correct (5 sentences; यत् तेन इष्टं तत् न प्राप्तम् is a sound passive; तं भरताग्रजः इति वदति). No definite error of language. STANDING POINT FOR THE SCHOLAR, with an inconsistency inside the draft that remains: the anvaya rightly joins the present participle उपस्पृशन् to the verb of verse 39, सः ... रामपादौ उपस्पृशन् (नन्दिग्रामे राज्यम् अकरोत्); but the vyākhyā … |
| VR.1.1.40 | The prescribed padārtha fix is in (तु → किन्तु (भरतात् भेदं सूचयति)). Rewritten vyākhyā correct: 6 sentences; आगच्छेयुः, एकाग्रः सन्, one इति उच्यते. No definite error. STANDING POINT FOR THE SCHOLAR: च in नागरस्य जनस्य च. The draft takes नागरस्य as the adjective of जनस्य and leaves च as a loose connective. As far as I recall (from memory) the commentators make च join two groups (the townsmen and the country people, … |
| VR.1.1.42 | Unchanged and correct in all layers (दृष्टौ passive dual, ग्रहीतुम्, क्षिप्यन्ते; इति यावत्; one इति आशयः). No definite error. STANDING POINT FOR THE SCHOLAR: the padārtha of ऐन्द्रम् adds इन्द्रेण दत्तम् to the plain taddhita sense इन्द्रस्य (इदम्). That goes beyond the word and rests on the commentaries and on the later Araṇyakāṇḍa account, where, as I recall (from memory), the bow Agastya hands over is called … |
| VR.1.1.43 | Second pass: the rewritten vyākhyā is correct (5 sentences; द्वौ तूणी गृहीतौ, तौ ... आस्ताम्, तयोः सायकाः ... न क्षीयन्ते; glosses in apposition, no formula). No definite error. STANDING POINTS FOR THE SCHOLAR. (1) तूणी: with the masculine dual अक्षयसायकौ the form can only be the dual of a masculine इ-stem, so the draft's तूणि, पुं, द्वितीया, द्वि is what the form requires. But the Amarakośa, as I recall it (from … |
| VR.1.1.52 | One definite fault remains, in the rewritten vyakhya only. Its last sentence (एवं तौ अपवाह्य सः स्वयम् आश्रमस्य समीपे अतिष्ठत्) tells something the verse does not say: that Ravana himself waited near the hermitage. That is brought in from the fuller story (rule 7: nothing added). In the verse the gerund अपवाह्य depends on जहार of verse 53, as the anvaya rightly shows. The corrected sentence is in fixes. Everything … |
| VR.1.1.57 | No error in any layer; the vyakhya now defines only श्रमणा and शत्रुसूदनः, so the rule 10 point of the first pass is resolved. One point remains for the scholar, on the mula: the printed line reads सोऽभ्य गच्छन्महातेजाः with a stray space inside अभ्यगच्छत्. The padaccheda rightly treats it as one word, and under §12 a correction of the same kind as the one approved for VR.1.1.1 (space removed, no letter changed) … |
| VR.1.1.64 | Second pass. Rewritten vyākhyā correct: 5 sentences; सन्देहे वर्तमाने and दृश्यते स्म; one इत्युक्ते; तस्य कायः, शरीरम्, उत्तमः महापर्वतसन्निभः च आसीत् agrees rightly with कायः. No definite error. Padaccheda right on its merits; the one checker error is the unjoined सुग्रीवः महा… of the print, and the draft still carries no rejoin_note, which vrtools/padartha.py needs before the verse can be merged. POINTS FOR THE … |
| VR.1.1.65 | MŪLA (§12). For the text as printed the draft is sound: अस्ति can only be the finite verb (अस् लट् प्रथम एक), so (सः) महाबलः अस्ति stands as a clause by itself; padaccheda, padārtha, anvaya and the rewritten vyākhyā (4 sentences, one इत्युक्ते, boundaries clean) agree with that reading, and the present अस्ति beside शक्नोति स्म is forced by the print. No checker error, no definite error. But चास्ति is very probably a … |
| VR.1.1.74 | Second pass. Rewritten vyākhyā correct: 5 sentences; दृष्ट्वा and ज्ञायते; वार्ताम् in apposition to प्रवृत्तिम्; सान्त्वितवान्, भग्नम् rightly formed; no इत्युक्ते. No definite error. POINTS FOR THE SCHOLAR: (1) the gloss of अभिज्ञानम् adds (रामस्य अङ्गुलीयकम्); the ring is known only from the Sundarakāṇḍa, not from this sarga (the vyākhyā rightly does not name it). It is a thing, not a person; compare verse 42 … |
| VR.1.1.76 | Second pass. Rewritten vyākhyā correct: 5 sentences, one इत्युक्ते, ये तं बध्नन्ति स्म ते यन्त्रिणः, सोढवान् rightly formed. No definite error. POINTS FOR THE SCHOLAR: (1) the verse has no finite verb; its participle मर्षयन् leans on 77 (… ततः दग्ध्वा … पुनः आयात्). The draft closes the sentence with (अतिष्ठत्) in the anvaya and स्थितः in the vyākhyā, as verse 28 was closed with (अभवत्); the other convention in this … |
| VR.1.1.84 | Mūla सर्वदेवतैः is doubtful: the Critical Edition (local ce.jsonl, CE 1.1.68) reads pūjitaḥ sarvadaivataiḥ. देवत as an a-stem is not a regular word (देवता is स्त्री, instr. देवताभिः; दैवत is नपुं, पुंसि वा, by Amara, from memory). The draft records सर्वदेवत नपुं तृतीया बहु and glosses it honestly (दैवतानि; सर्वाभिः देवताभिः इति अर्थः), and the vyākhyā wisely uses सर्वाः देवताः. Scholar to decide: keep as an epic … |
| VR.1.1.85 | अभ्यषिच्य (augment अ + ल्यप्) is not a possible form by grammar. CE 1.1.66 (local ce.jsonl) reads abhyaṣiñcat sa laṅkāyāṃ; some printed texts have अभिषिच्य च (from memory); the Wikisource reading looks like a mixture of the two. The draft records it the right way for §5.7 (avyaya, अभि + सिच्, ल्यप्, gloss: अभिषिच्य इति अर्थः; आर्षं रूपम्), but the reading is a candidate for mula_suspect (§12). प्रमुमोद is correctly … |
| VR.1.1.88 | पुनः: the anvaya and the vyākhyā take it with समारुह्य (boarded the Puṣpaka again after the halt at the hermitage). By its place in the verse it stands with आख्यायिकां जल्पन् (telling the past events over again), and I believe commentators read it so, but I cannot verify this offline. Both are grammatical and fit the story. Scholar to choose. If it goes with जल्पन्: anvaya = तदा सुग्रीवसहितः (रामः) पुनः आख्यायिकां … |
| VR.1.1.90 | निरामयः / अरोगः: आमय means रोग (Amara: रोगव्याधिगदामयाः, from memory), so the two words are synonyms. The draft separates them by glossing आमयः as पीडा in the vigraha (निर्गतः आमयः (पीडा) यस्मात् सः), which is not the dictionary sense. The commentators separate them as freedom from bodily and from mental illness (from memory; which word is which needs the commentary). Scholar to settle the two glosses. All else … |
| VR.1.1.100 | ईयात्: by Pāṇini the form is the आशीर्लिङ् of इण् (the विधिलिङ् is इयात्), and the draft records it so; but the sense here, and the draft's own gloss प्राप्नुयात्, is optative. The traditional way out is the root ई (read into वी गतिव्याप्ति… in the अदादि list), whose विधिलिङ् is ईयात्; I believe the commentators derive it so (from memory). Scholar to choose: इ, आशीर्लिङ् (a blessing) or ई, विधिलिङ्; the gloss can … |

### 4. Forms the word list does not know (analyses checked by hand by the reviewers)

10: महा-उरस्कः, 22: एनम्, 24: अनुपालयन्, 26: अनुदर्शयन्, 29: शृङ्गवीरपुरे, 44: असुर-रक्षसाम्, 46: विरूपिता, 53: जटायुषम्, 54: जटायुषम्, 59: शंसत्, 69: एनम्, 75: पञ्च, 85: प्रमुमोद, 91: केचित्, 99: महीयते, 100: वाक्-ऋषभत्वम्

### 5. Genders taken from memory of the Amarakośa and Apte (to be verified)

हनु स्त्री (9) · तूणि पुं (43) · तोरण नपुं (74; the Amarakośa allows पुं) · इषु पुं (66) · चारित्र नपुं (3) · भूत नपुं (3) ·
संयत् स्त्री (45) · रण पुं (the Amarakośa allows नपुं) · सिन्धु स्त्री in the sense river (16) · जत्रु नपुं (10) · आश्रम पुं (87) ·
पुष्पक नपुं (88) · संयुग पुं (4, by ruling). No copy of either kośa is in the project folder.

### 6. 10% sample of the verses that passed (fixed seed 20261111)

VR.1.1.7, VR.1.1.14, VR.1.1.21, VR.1.1.28, VR.1.1.33, VR.1.1.50, VR.1.1.58, VR.1.1.62, VR.1.1.78, VR.1.1.80

### Settled by rulings (CLAUDE.md §5.4, §5.7)

Gender by the Amarakośa first, then Apte; नञ्-compounds and prefixes that are not words (दुस्, निस्, वि, प्र) are not
hyphenated; स-, सु-, महा- and upapada compounds are; a gloss must be simpler than the word; नु is a question
particle; the vyākhyā is connected expository prose (rules 1–10).

## Bāla-kāṇḍa, sarga 2 (Stage C; 43 verses)

Reviewer verdicts after one fix round: 41 pass, 2 flag (first pass: 33 pass, 9 fix, 1 flag; all fixes applied and passed on
the second pass). Generator and reviewer were separate sub-agents (claude-opus-5-5, high effort; prompt stage-c-1).

### 1. Flagged by the reviewers (points for Swamiji)

| Verse | Reviewer's note (shortened) |
|---|---|
| VR.1.2.9 | Second pass: no definite error remains. तु → पादपूरणार्थम् अव्ययम् is applied as well. The coordinator's decision stands: चरन्तम् and अनपायिनम् carry no anvita (the checker refuses an anvita across genders), and each gloss ends (मिथुनस्य विशेषणम्; अत्र पुंलिङ्गम् आर्षम्). FOR THE HUMAN: decide the gender of मिथुन here. (a) As dr … |
| VR.1.2.23 | Decide स्वयम् प्रभुः (two padas, as drafted; Dharmamitra; printed text has a space; 'the Lord came himself') or स्वयम्प्रभुः (one compound, DCS; 'self-luminous'). The verse already carries seed_disagreement and §5.1 says to flag it. The draft's choice follows the printed spacing and is consistently carried through padartha, anva … |

**Ruled by Aditya (D17):** VR.1.2.9 मिथुन stays नपुं, the qualifiers marked आर्षप्रयोगः (vyākhyā उच्यते → उच्येते applied); VR.1.2.23 स्वयं प्रभुः stays two words.

### 2. Declared re-join exceptions

| Verse | Note |
|---|---|
| VR.1.2.26 | The printed text leaves च ऋषये unjoined (the joiner gives चर्षये). The hiatus is the optional prakṛtibhāva of ऋत्यकः (6.1.128), which the joiner does not apply; the padaccheda is right on its merits. |
| VR.1.2.38 | The printed third line has a stray र् in भगवान् र्मुनिर्विस्मयमाययौ (flagged mula_suspect, Class B, not corrected); the correct split is भगवान् मुनिः विस्मयम् आययौ, which re-joins to भगवान् मुनिर्विस्मयमाययौ. |
| VR.1.2.43 | The printed text has two slips (flagged mula_suspect, Class B, not corrected): रघुवरकरितं for रघुवरचरितं, and दशशिरसश्क for दशशिरसश्च. Neither printed form is a possible word; the padaccheda gives the evident words (चरितम्, च) and the layers explain the verse in that sense. |

### 3. Doubtful source readings (Class B, not corrected; see `review/mula_queue.md`)

VR.1.2.27 and 28 (a stray । before ॥), VR.1.2.38 (stray र्), VR.1.2.43 (करितं, सश्क).

### 4. Declared word-list exceptions (fit_note)

7: प्रायच्छत, 16: वीक्षतः

### 5. 10% sample of the verses that passed (fixed seed 20261111)

VR.1.2.12, VR.1.2.19, VR.1.2.25, VR.1.2.31

### Also changed in this round: VR.1.1

The four approved corrections VR.1.1.15, 29, 65, 84 are applied (`lines_corrected`); their layers were redone by a
generator and passed a separate reviewer with no fixes. VR.1.1.15 no longer needs its re-join exception. VR.1.1.85
stays flagged, not corrected.

## Bāla-kāṇḍa, sarga 3 (Stage C; 39 verses)

Reviewer verdicts: first pass 30 pass, 6 fix, 3 flag; final 32 pass, 7 flag. Four of the flags (20, 22, 35, 37) are
sentences changed in the fix round (a coordinator's style request and one substitute verb) that the second pass found
wrong; the reviewer's exact corrected sentence is applied and the flag kept, as §5.7 says.

### 1. Flagged by the reviewers (points for Swamiji)

| Verse | Reviewer's note (shortened) |
|---|---|
| VR.1.3.11 | Decide the sense of विश्वामित्र-सहायने. The draft takes सहायन as सहायस्य कर्म (help in guarding the yajña), which has no regular derivation from सहाय. The transparent analysis is सह + अयन = going with Viśvāmitra; the कथाः are then the stories told on that journey, which fits नाना चित्राः कथाः. The yajña in the vyākhyā and the co … |
| VR.1.3.20 | Second pass. Removing the rejoin_note is right: खर-त्रिशिरसोः उत्थानम् re-joins regularly (-सोरुत्थानं), and check_layers is OK. The new उत्तिष्ठति, though, has the wrong pada. In the sense 'set about, strive' (not physically rising), उद् + स्था takes the ātmanepada by 1.3.24 उदोऽनूर्ध्वकर्मणि (मुक्तौ उत्तिष्ठते), so the form is … |
| VR.1.3.22 | Second pass. The reworked first sentence uses मिलति with the genitive (रामलक्ष्मणयोः … मिलति). That is a vernacular construction: मिल् takes सह with the instrumental, or the accusative. The coordinator should apply the corrected sentence below. The rest of the verse is right. Second pass. Clean. फल-मूल-अशनम्, हनूमत्-दर्शनम् righ … |
| VR.1.3.25 | Second pass: unchanged in the draft; kept as flag for the human reviewer. Decide the case of दिशः. The draft takes it as द्वितीया बहु with an action noun ('दिशः (प्रति) प्रस्थापनम्'); with a kṛt noun like प्रस्थापन one would rather expect a genitive, so दिशः may be षष्ठी एक ('the sending towards the quarter(s)', collective). Bot … |
| VR.1.3.28 | Second pass: unchanged in the draft; kept as flag for the human reviewer. Decide the analysis of लङ्का-मलय-दर्शनम्. The draft reads a dvandva (लङ्का च मलयः च), and the vyākhyā has Hanumān, after crossing, see 'लङ्कां मलयं नाम पर्वतं च'. But the Malaya range lies on the mainland; several commentators read the compound as the hill … |
| VR.1.3.35 | Second pass. The reworked first sentence puts both agent and object of the action noun प्रतार (masculine) in the genitive (रामस्य सेनायाः समुद्रस्य प्रतारः). By 2.3.66 only the object takes the genitive and the agent goes to the instrumental. The coordinator should apply the corrected sentence below. The rest of the verse is rig … |
| VR.1.3.37 | Second pass. The padārtha fixes were applied exactly. But Vibhīṣaṇa is still not named outside the compound, and the new first sentence makes 'रावणस्य अनुजस्य' qualify the member बिभीषण inside बिभीषणाभिषेकः. That is an असमर्थ (सापेक्ष) construction. The coordinator should apply the corrected sentence below. The rest of the verse … |

### 2. Declared re-join exceptions

None. 18, 26, 29 leave च + vowel unjoined at a pāda break, which the checker accepts (one hiatus at a pāda break, checker v7); lines without a closing daṇḍa (18, 24–38) are now read with a possible pause at the line break (checker v8).

### 3. Doubtful source readings

VR.1.3.18 and 24–38: line 1 lacks its closing । (kept as printed; Class B, `review/mula_queue.md`).

### 4. Declared word-list exceptions (fit_note)

none

### 5. 10% sample of the verses that passed (fixed seed 20261111)

VR.1.3.12, VR.1.3.19, VR.1.3.27, VR.1.3.34
