# Human review queue

Verses that the reviewer sub-agent flagged for a scholar's decision, and (once a sarga
is complete) the 10% sample of CLAUDE.md §7.9. Set `review.human` to `approved` or
`changes` in the sarga file when a verse has been looked at.

## Bāla-kāṇḍa, sarga 1 (pilot)

Reviewer verdicts for verses 1–5: 1 pass · 2 pass · 3 flag · 4 flag · 5 pass (after one fix round).
Full notes: `review/drafts/VR.1.1.review.json`.

| Verse | Point | What the draft shows | Alternative | Reviewer's advice |
|---|---|---|---|---|
| VR.1.1.3 | एकप्रियदर्शनः | karmadhāraya: एकः (अद्वितीयः) प्रियदर्शनः; gloss यस्य दर्शनं सर्वेषां प्रियम्, तादृशः अद्वितीयः | bahuvrīhi: एकम् (सदा) प्रियं दर्शनं यस्य सः | keep the draft for a beginner; the gloss adds सर्वेषाम्, which the word does not say |
| VR.1.1.4 | कस्य with बिभ्यति | षष्ठी, explained as कस्मात् (epic genitive for the ablative) | construe कस्य जातरोषस्य with संयुगे | keep the draft |
| VR.1.1.4 | gender of संयुग | नपुं (Monier-Williams) | पुं (Amarakośa, Apte) | leans to पुं; decide once for the whole work |
| VR.1.1.4 | अनसूयकः | not hyphenated; vigraha न असूयकः | — | record that नञ्-compounds are not hyphenated (§5.1 says "every member boundary") |

Points where the draft departs from the worked examples of CLAUDE.md (reviewer: the draft is right):
- VR.1.1.1 `वाक्-विदाम्` is hyphenated (the §4 example leaves वाग्विदाम् whole).
- VR.1.1.1 `मुनि-पुङ्गवम्`: vigraha मुनिः पुङ्गवः इव (the example has मुनिषु पुङ्गवः).
- VR.1.1.2 anvaya: the fourth च stands in parentheses (the §5.6 example has it outside).
- VR.1.1.2 glosses are in the pada's own case (धर्मं जानन्), not finite clauses (धर्मं जानाति इति).
