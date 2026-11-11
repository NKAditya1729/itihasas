"""Stage B, Step 4d: every pada of the padaccheda has a padārtha entry whose grammatical
analysis fits its form; plus the coverage checks of CLAUDE.md §7.4 and the hygiene of §7.5.

The good case is the worked example of CLAUDE.md §4 (VR.1.1.1)."""
import copy

import pytest

from vrtools.padartha import check_layers

LINES = ["तपःस्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।", "नारदं परिपप्रच्छ वाल्मीकिर्मुनिपुङ्गवम् ॥"]
GOOD = {
    "id": "VR.1.1.1",
    "padaccheda_lines": ["तपः-स्वाध्याय-निरतम् तपस्वी वाक्-विदाम् वरम् ।", "नारदम् परिपप्रच्छ वाल्मीकिः मुनि-पुङ्गवम् ॥"],
    "padartha": [
        {"pada": "तपः-स्वाध्याय-निरतम्", "pratipadika": "तपःस्वाध्यायनिरत", "linga": "पुं", "vibhakti": "द्वितीया", "vacana": "एक",
         "vigraha": "तपसि स्वाध्याये च निरतः, तम्", "artha": "तपसि वेदपठने च सदा संलग्नम्", "anvita": "नारदम्"},
        {"pada": "तपस्वी", "pratipadika": "तपस्विन्", "linga": "पुं", "vibhakti": "प्रथमा", "vacana": "एक", "artha": "तपः कुर्वन्, तपोयुक्तः", "anvita": "वाल्मीकिः"},
        {"pada": "वाक्-विदाम्", "pratipadika": "वाग्विद्", "linga": "पुं", "vibhakti": "षष्ठी", "vacana": "बहु",
         "vigraha": "वाचं विदन्ति इति वाग्विदः, तेषाम्", "artha": "वचनज्ञानां जनानाम्"},
        {"pada": "वरम्", "pratipadika": "वर", "linga": "पुं", "vibhakti": "द्वितीया", "vacana": "एक", "artha": "श्रेष्ठम्", "anvita": "नारदम्"},
        {"pada": "नारदम्", "pratipadika": "नारद", "linga": "पुं", "vibhakti": "द्वितीया", "vacana": "एक", "artha": "नारदमुनिम्"},
        {"pada": "परिपप्रच्छ", "dhatu": "प्रच्छ्", "upasarga": "परि", "lakara": "लिट्", "purusha": "प्रथम", "vacana": "एक", "artha": "पृष्टवान्"},
        {"pada": "वाल्मीकिः", "pratipadika": "वाल्मीकि", "linga": "पुं", "vibhakti": "प्रथमा", "vacana": "एक", "artha": "वाल्मीकिमुनिः"},
        {"pada": "मुनि-पुङ्गवम्", "pratipadika": "मुनिपुङ्गव", "linga": "पुं", "vibhakti": "द्वितीया", "vacana": "एक",
         "vigraha": "मुनिषु पुङ्गवः", "artha": "मुनिश्रेष्ठम्", "anvita": "नारदम्"},
    ],
    "anvaya": "तपस्वी वाल्मीकिः तपःस्वाध्यायनिरतं वाग्विदां वरं मुनिपुङ्गवं नारदं परिपप्रच्छ ।",
    "vyakhya_sa": "वाल्मीकिः नाम एकः मुनिः आसीत् । सः **तपस्वी** आसीत् । **नारदः** अपि महान् मुनिः । नारदः सदा **तपसि** **स्वाध्याये** च **निरतः** । "
                  "सः **वाग्विदां वरः** — वचनं जानतां सर्वेषां मध्ये श्रेष्ठः । सः **मुनिपुङ्गवः** — मुनीनां श्रेष्ठः । "
                  "तादृशं नारदं **वाल्मीकिः** एकं प्रश्नं **परिपप्रच्छ** — पृष्टवान् ।",
}


def errors(v):
    return check_layers(LINES, v)["errors"]


def good():
    return copy.deepcopy(GOOD)


def test_the_worked_example_of_claude_md_passes():
    r = check_layers(LINES, good())
    assert r["errors"] == []
    assert r["vyakhya_used_padas"][:3] == ["तपस्वी", "नारदः", "तपसि"]      # recomputed from the bold words


# ---- one entry per pada, in verse order ------------------------------------------------

def test_a_pada_without_an_entry_is_an_error():
    v = good()
    del v["padartha"][3]
    assert any("वरम्" in e and "no padārtha entry" in e for e in errors(v))


def test_an_entry_for_a_pada_that_is_not_in_the_padaccheda_is_an_error():
    v = good()
    v["padartha"][3]["pada"] = "वरः"
    assert any("वरः" in e and "not a pada of the padaccheda" in e for e in errors(v))


def test_entries_must_follow_the_verse_order():
    v = good()
    v["padartha"][0], v["padartha"][1] = v["padartha"][1], v["padartha"][0]
    assert any("order" in e for e in errors(v))


# ---- the analysis must fit the form ------------------------------------------------------

def test_wrong_case_for_the_form_is_an_error():
    v = good()
    v["padartha"][3]["vibhakti"] = "तृतीया"          # वरम् cannot be instrumental
    assert any("वरम्" in e and "तृतीया" in e for e in errors(v))


def test_wrong_number_for_the_form_is_an_error():
    v = good()
    v["padartha"][2]["vacana"] = "एक"               # विदाम् is plural
    assert any("वाक्-विदाम्" in e for e in errors(v))


def test_wrong_person_or_tense_for_a_verb_is_an_error():
    v = good()
    v["padartha"][5]["purusha"] = "उत्तम"            # पप्रच्छ is 1st/3rd sg. perfect; here उत्तम is allowed by the form
    assert errors(v) == []
    v["padartha"][5]["lakara"] = "लट्"
    assert any("परिपप्रच्छ" in e and "लट्" in e for e in errors(v))


def test_a_noun_analysed_as_a_verb_is_an_error():
    v = good()
    v["padartha"][4] = {"pada": "नारदम्", "dhatu": "नृ", "lakara": "लट्", "purusha": "प्रथम", "vacana": "एक", "artha": "x"}
    assert any("नारदम्" in e for e in errors(v))


def test_an_entry_needs_the_fields_of_its_kind():
    v = good()
    del v["padartha"][4]["vibhakti"]
    assert any("नारदम्" in e and "vibhakti" in e for e in errors(v))
    v = good()
    v["padartha"][4]["linga"] = "masculine"
    assert any("नारदम्" in e and "linga" in e for e in errors(v))


def test_an_indeclinable_carries_no_case():
    lines = ["रामश्च ।"]
    v = {"id": "x", "padaccheda_lines": ["रामः च ।"], "anvaya": "रामः च ।", "vyakhya_sa": None,
         "padartha": [{"pada": "रामः", "pratipadika": "राम", "linga": "पुं", "vibhakti": "प्रथमा", "vacana": "एक", "artha": "दशरथस्य पुत्रः"},
                      {"pada": "च", "avyaya": True, "artha": "अपि"}]}
    assert check_layers(lines, v)["errors"] == []
    v["padartha"][1]["vibhakti"] = "प्रथमा"
    assert any("च" in e and "avyaya" in e for e in check_layers(lines, v)["errors"])


# ---- viśeṣaṇa and viśeṣya agree (this is what catches सः क्रोधः for सक्रोधः) ---------------

def test_a_qualifier_must_agree_with_what_it_qualifies():
    v = good()
    v["padartha"][1]["anvita"] = "नारदम्"            # तपस्वी (nom.) cannot qualify नारदम् (acc.)
    assert any("तपस्वी" in e and "नारदम्" in e and "agree" in e for e in errors(v))


def test_anvita_must_name_a_pada_of_the_verse():
    v = good()
    v["padartha"][3]["anvita"] = "रामम्"
    assert any("वरम्" in e and "रामम्" in e for e in errors(v))


def test_sah_krodhah_for_sakrodhah_is_caught():
    # VR.1.60.12: … स्रुवमुद्यम्य सक्रोधस्त्रिशङ्कुमिदमब्रवीत्. A split सः क्रोधः forces क्रोधः to be glossed
    # as a nominative noun; said to qualify विश्वामित्रः it has no viśeṣya of its own kind, and as a free
    # noun it leaves the sentence with two subjects, which the anvaya rule reports.
    lines = ["सक्रोधस्त्रिशङ्कुमब्रवीत् ॥"]
    v = {"id": "x", "padaccheda_lines": ["सः क्रोधः त्रिशङ्कुम् अब्रवीत् ॥"], "vyakhya_sa": None,
         "anvaya": "सक्रोधः त्रिशङ्कुम् अब्रवीत् ।",
         "padartha": [{"pada": "सः", "pratipadika": "तद्", "linga": "पुं", "vibhakti": "प्रथमा", "vacana": "एक", "artha": "विश्वामित्रः"},
                      {"pada": "क्रोधः", "pratipadika": "क्रोध", "linga": "पुं", "vibhakti": "प्रथमा", "vacana": "एक", "artha": "कोपः"},
                      {"pada": "त्रिशङ्कुम्", "pratipadika": "त्रिशङ्कु", "linga": "पुं", "vibhakti": "द्वितीया", "vacana": "एक", "artha": "त्रिशङ्कुनामकं राजानम्"},
                      {"pada": "अब्रवीत्", "dhatu": "ब्रू", "lakara": "लङ्", "purusha": "प्रथम", "vacana": "एक", "artha": "उक्तवान्"}]}
    assert any("anvaya" in e for e in check_layers(lines, v)["errors"])


# ---- anvaya: every pada once; supplied words in parentheses ---------------------------------

def test_anvaya_must_contain_every_pada():
    v = good()
    v["anvaya"] = "तपस्वी वाल्मीकिः तपःस्वाध्यायनिरतं वाग्विदां मुनिपुङ्गवं नारदं परिपप्रच्छ ।"
    assert any("anvaya" in e and "वरम्" in e for e in errors(v))


def test_a_supplied_word_must_stand_in_parentheses():
    v = good()
    v["anvaya"] = "तपस्वी वाल्मीकिः तपःस्वाध्यायनिरतं वाग्विदां वरं मुनिपुङ्गवं नारदं प्रश्नं परिपप्रच्छ ।"
    assert any("anvaya" in e and "प्रश्नं" in e for e in errors(v))
    v["anvaya"] = "तपस्वी वाल्मीकिः तपःस्वाध्यायनिरतं वाग्विदां वरं मुनिपुङ्गवं नारदं (प्रश्नं) परिपप्रच्छ ।"
    assert errors(v) == []


# ---- vyākhyā: reuses the verse's words; short sentences; no Latin letters ----------------------

def test_vyakhya_must_reuse_most_significant_padas():
    v = good()
    v["vyakhya_sa"] = "वाल्मीकिः नाम एकः मुनिः आसीत् । सः महान् आसीत् । सः एकं प्रश्नं पृष्टवान् ।"
    assert any("vyākhyā" in e and "reuses" in e for e in errors(v))


def test_vyakhya_sentences_are_few_and_short():
    v = good()
    v["vyakhya_sa"] = GOOD["vyakhya_sa"] + " " + " ".join(["सः मुनिः आसीत् ।"] * 6)
    assert any("sentences" in e for e in errors(v))
    v = good()
    v["vyakhya_sa"] = GOOD["vyakhya_sa"].replace("सः **तपस्वी** आसीत् ।", "सः **तपस्वी** आसीत् च सदा वने वसति स्म च फलानि खादति स्म च जलं पिबति स्म च ।")
    assert any("words" in e for e in errors(v))


@pytest.mark.parametrize("field", ["anvaya", "vyakhya_sa"])
def test_no_latin_letters_in_sanskrit_fields(field):
    v = good()
    v[field] = v[field] + " ok"
    assert any("Latin" in e for e in errors(v))


def test_no_latin_letters_in_a_gloss():
    v = good()
    v["padartha"][3]["artha"] = "best"
    assert any("Latin" in e and "वरम्" in e for e in errors(v))


# ---- the padaccheda itself must still re-join ---------------------------------------------------

def test_the_padaccheda_must_rejoin_to_the_text():
    v = good()
    v["padaccheda_lines"][1] = "नारदम् परिपप्रच्छ वाल्मीकि मुनि-पुङ्गवम् ॥"
    v["padartha"][6]["pada"] = "वाल्मीकि"
    assert any("re-join" in e for e in errors(v))


def test_unverified_forms_are_listed_not_failed():
    r = check_layers(LINES, good())
    assert isinstance(r["unverified"], list)          # forms the word list does not know (names, rare compounds)


# ---- merging a reviewed draft into a verse -------------------------------------------------

def _verse():
    return {"id": "VR.1.1.1", "lines": ["तपः स्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।", LINES[1]], "lines_corrected": list(LINES),
            "padaccheda_lines": ["x"], "groups": None, "padaccheda_status": "seed", "padartha": [], "anvaya": None, "vyakhya_sa": None,
            "vyakhya_used_padas": [], "speaker": None, "context_note_sa": None, "metre": {"name": "अनुष्टुप्", "ok": True, "syllables": 32},
            "review": {"auto_checks": {}, "agent_review": None, "human": "pending", "flags": ["mula_suspect", "seed_disagreement"], "notes": ""},
            "gen": {"model": "", "date": "", "prompt_version": ""}, "seed": {"source": "dcs"}}


def test_merge_writes_all_layers_and_marks_the_padaccheda_reviewed():
    from vrtools.padartha import merge_verse
    v = _verse()
    merge_verse(v, {**good(), "speaker": None, "context_note_sa": "वाल्मीकिः नारदं प्रश्नं पृच्छति ।"},
                gen={"model": "m", "date": "2026-11-11", "prompt_version": "pilot-1"}, verdict="pass")
    assert v["padaccheda_status"] == "reviewed" and v["padaccheda_lines"] == GOOD["padaccheda_lines"]
    assert [g[:2] for g in v["groups"][0] if not isinstance(g, str)][0] == ["तपःस्वाध्यायनिरतं", "तपः-स्वाध्याय-निरतम्"]   # aligned to the corrected text
    assert len(v["padartha"]) == 8 and v["anvaya"].startswith("तपस्वी") and "**तपस्वी**" in v["vyakhya_sa"]
    assert v["vyakhya_used_padas"][0] == "तपस्वी"
    assert v["review"]["agent_review"] == "pass" and v["review"]["auto_checks"]["padartha_fit"] is True
    assert v["review"]["flags"] == ["mula_suspect"]            # the seed flag is settled by the review
    assert v["gen"]["prompt_version"] == "pilot-1" and v["lines"][0].startswith("तपः स्वाध्याय")


def test_merge_refuses_a_draft_that_fails_the_checks():
    from vrtools.padartha import merge_verse
    bad = good()
    bad["padartha"][3]["vibhakti"] = "तृतीया"
    v = _verse()
    with pytest.raises(ValueError, match="वरम्"):
        merge_verse(v, bad, gen={"model": "m", "date": "d", "prompt_version": "p"}, verdict="pass")
    assert v["padaccheda_status"] == "seed" and v["padartha"] == []     # nothing was written
