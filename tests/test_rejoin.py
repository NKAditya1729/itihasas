"""Re-join checker: sandhi-join(padaccheda) must reproduce the mūla (CLAUDE.md §7.3).

Positive cases are real verse fragments. Negative cases are wrong splits that a
too-loose checker would let through.
"""
import pytest

from vrtools.sandhi import check_rejoin, fold, norm, to_slp1


def ok(mula, pada):
    return check_rejoin([mula], [pada])["ok"]


# ---- normalisation -----------------------------------------------------------

def test_norm_drops_spaces_hyphens_avagraha_and_dandas():
    assert norm(to_slp1("समर्थोऽसि ज्ञातुम् ॥")) == "samarTosijYAtum"
    assert norm(to_slp1("को न्वस्मिन् ।")) == norm(to_slp1("को-न्वस्मिन्"))


def test_norm_treats_homorganic_nasal_and_anusvara_alike():
    assert fold(to_slp1("मुनिपुङ्गवम्")) == fold(to_slp1("मुनिपुंगवम्"))
    assert fold(to_slp1("सम्प्रहृष्टः")) == fold(to_slp1("संप्रहृष्टः"))


def test_norm_keeps_word_final_m_before_pause():
    assert norm(to_slp1("वरम्")) != norm(to_slp1("वरं"))


# ---- positive: real junctions ---------------------------------------------------

@pytest.mark.parametrize("mula,pada", [
    # VR.1.1.1 (compounds, visarga + voiced, final म्)
    ("तपः स्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।", "तपः-स्वाध्याय-निरतम् तपस्वी वाक्-विदाम् वरम् ।"),
    ("नारदं परिपप्रच्छ वाल्मीकिर्मुनिपुङ्गवम् ॥", "नारदम् परिपप्रच्छ वाल्मीकिः मुनि-पुङ्गवम् ॥"),
    # VR.1.1.2 (aH + voiced → o, u + vowel → v, n + k, aH + c → śc)
    ("को न्वस्मिन्साम्प्रतं लोके गुणवान्कश्च वीर्यवान् ।", "कः नु अस्मिन् साम्प्रतम् लोके गुणवान् कः च वीर्यवान् ।"),
    ("धर्मज्ञश्च कृतज्ञश्च सत्यवाक्यो दृढव्रतः ॥", "धर्म-ज्ञः च कृत-ज्ञः च सत्य-वाक्यः दृढ-व्रतः ॥"),
    # avagraha: aH + a
    ("महर्षे त्वं समर्थोऽसि ज्ञातुमेवंविधं नरम् ॥", "महर्षे त्वम् समर्थः असि ज्ञातुम् एवंविधम् नरम् ॥"),
    # vowel sandhi a + e → ai, a + i → e
    ("श्रुत्वा चैतत्त्रिलोकज्ञो वाल्मीकेर्नारदो वचः ।", "श्रुत्वा च एतत् त्रि-लोक-ज्ञः वाल्मीकेः नारदः वचः ।"),
    ("श्रूयतामिति चामन्त्र्य प्रहृष्टो वाक्यमब्रवीत् ॥", "श्रूयताम् इति च आमन्त्र्य प्रहृष्टः वाक्यम् अब्रवीत् ॥"),
    # t + l → ll; a + ā → ā
    ("अयोध्या नाम नगरी तत्रासील्लोकविश्रुता ।", "अयोध्या नाम नगरी तत्र आसीत् लोक-विश्रुता ।"),
    # i + vowel → y; final n doubled after a short vowel
    ("इत्युक्त्वा स महातेजा अस्मिन्नेव वने वसन् ।", "इति उक्त्वा सः महा-तेजाः अस्मिन् एव वने वसन् ।"),
    # t + ś → cch; saḥ + consonant → sa
    ("स तच्छ्रुत्वा वचस्तस्य ।", "सः तत् श्रुत्वा वचः तस्य ।"),
    # aH + other vowel → a (hiatus); iH + vowel → r
    ("राम इति ततो मुनिरुवाच ।", "रामः इति ततः मुनिः उवाच ।"),
    # n + c → ṃśc
    ("तांश्च सर्वान् ।", "तान् च सर्वान् ।"),
    # 1.1.84-style stray ॥ inside the verse is just a pause
    ("सदेवर्षिगणं तुष्टं राघवस्य महात्मनः ॥", "स-देव-ऋषि-गणम् तुष्टम् राघवस्य महा-आत्मनः ॥"),
])
def test_real_junctions_rejoin(mula, pada):
    assert ok(mula, pada)


def test_two_line_verse():
    r = check_rejoin(["तपः स्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।", "नारदं परिपप्रच्छ वाल्मीकिर्मुनिपुङ्गवम् ॥"],
                     ["तपः-स्वाध्याय-निरतम् तपस्वी वाक्-विदाम् वरम् ।", "नारदम् परिपप्रच्छ वाल्मीकिः मुनि-पुङ्गवम् ॥"])
    assert r["ok"] and r["failures"] == []


def test_sandhi_across_a_line_break_without_danda():
    # 4-pāda verse printed one pāda per line; a word runs over the break (वचस्त- / च्छ्रुत्वा)
    mula = ["ते चापि पौरा नृपतेर्वचस्त-", "च्छ्रुत्वा तदा लाभमिवेष्टमाशु ।"]
    pada = ["ते च अपि पौराः नृपतेः वचः", "तत् श्रुत्वा तदा लाभम् इव इष्टम् आशु ।"]
    assert check_rejoin(mula, pada)["ok"]


# ---- negative: wrong splits must fail ------------------------------------------

@pytest.mark.parametrize("mula,pada", [
    ("नारदं परिपप्रच्छ वाल्मीकिर्मुनिपुङ्गवम् ॥", "नारदम् परिपप्रच्छ वाल्मीकि मुनि-पुङ्गवम् ॥"),   # lost visarga
    ("को न्वस्मिन्साम्प्रतं लोके ।", "कः न अस्मिन् साम्प्रतम् लोके ।"),                          # wrong vowel
    ("को न्वस्मिन्साम्प्रतं लोके ।", "कः नु अस्मिन् लोके ।"),                                    # missing word
    ("को न्वस्मिन्साम्प्रतं लोके ।", "कः नु अस्मिन् साम्प्रतम् च लोके ।"),                       # extra word
    ("ततो रामेति ।", "ततः रामः इति ।"),                       # रामः इति gives राम इति, not रामेति
    ("स तच्छ्रुत्वा ।", "सः तत् शृत्वा ।"),                   # wrong letter
    ("कश्च ।", "कः तु ।"),                                    # wrong particle
    ("वरम् ।", "वरः ।"),                                      # wrong ending
    # half-split source: the mūla is not saṃhitā, so the join cannot reproduce it
    ("एतत् इच्छामि अहम् श्रोतुम् ।", "एतत् इच्छामि अहम् श्रोतुम् ।"),
])
def test_wrong_splits_fail(mula, pada):
    assert not ok(mula, pada)


def test_failure_reports_line_and_position():
    r = check_rejoin(["को न्वस्मिन्साम्प्रतं लोके ।"], ["कः न अस्मिन् साम्प्रतम् लोके ।"])
    f = r["failures"][0]
    assert f["line"] == 0 and f["pos"] == 3          # "kon|v…" expected, "kon|A…" joined
    assert "expected" in f and "got" in f


def test_line_count_mismatch_fails():
    r = check_rejoin(["क ।", "ख ॥"], ["क ख ॥"])
    assert not r["ok"] and r["failures"][0]["reason"] == "line_count"


def test_danda_positions_must_match():
    r = check_rejoin(["रामः ।"], ["रामः ॥"])
    assert not r["ok"] and r["failures"][0]["reason"] == "danda"


# ---- review findings (2026-11-11): the checker was too loose ---------------------

@pytest.mark.parametrize("mula,pada", [
    ("तांश्च ।", "तांः च ।"),                 # visarga after anusvāra is not a word ending
    ("तां ददर्श ।", "तान् ददर्श ।"),          # final n stays n before d; ṃ can only come from m
    ("सीतां ध्यायन्तीम् ।", "सीतान् ध्यायन्तीम् ।"),
    ("स तच्छ्रुत्वा ।", "स तत् श्रुत्वा ।"),   # स is not a pausal form (सः)
    ("नारदं परिपप्रच्छ ।", "नारदं परिपप्रच्छ ।"),   # pausal form ends in म्, not ं
    ("वाल्मीकिर्मुनिः ।", "वाल्मीकिर् मुनिः ।"),   # र् is not a pausal ending
    ("वाग्विदाम् ।", "वाग्-विदाम् ।"),
    ("रामर्गच्छति ।", "रामः गच्छति ।"),         # aḥ → ar only for r-stems (punar, antar …)
    ("नररस्ति ।", "नरः अस्ति ।"),
    ("नदी अत्र ।", "नदी अत्र ।"),              # unjoined ī + vowel is not saṃhitā (unless a dual)
    ("वने इति ।", "वने इति ।"),
    ("भोर्गच्छ ।", "भोः गच्छ ।"),              # bhoḥ drops its visarga
    ("तावगायताम् ।", "ताउ अगायताम् ।"),
])
def test_review_wrong_splits_fail(mula, pada):
    assert not ok(mula, pada)


@pytest.mark.parametrize("mula,pada", [
    ("तान्ददर्श ।", "तान् ददर्श ।"),
    ("तान्ददर्श ।", "ताम् ददर्श ।"),          # optional homorganic nasal for final m (parasavarṇa)
    ("तां ददर्श ।", "ताम् ददर्श ।"),
    ("किन्नु ।", "किम् नु ।"),                 # m before a nasal may be written as that nasal
    ("अहम्माम् ।", "अहम् माम् ।"),
    ("पुनर्गच्छति ।", "पुनः गच्छति ।"),        # r-stem
    ("अन्तर्गतः ।", "अन्तः-गतः ।"),
    ("भो गच्छ ।", "भोः गच्छ ।"),
    ("तावगायताम् ।", "तौ अगायताम् ।"),
])
def test_review_correct_joins_pass(mula, pada):
    assert ok(mula, pada)


def test_non_pausal_failure_names_the_word():
    r = check_rejoin(["स तच्छ्रुत्वा ।"], ["स तत् श्रुत्वा ।"])
    assert r["failures"][0]["reason"] == "non_pausal" and r["failures"][0]["word"] == "स"


def test_r_stem_written_with_anusvara_is_still_an_r_stem():
    # VR.2.30.14 वनान्तर्वनगोचरा, padaccheda spelled अंतः
    assert ok("वनान्तर्वनगोचरा ।", "वन-अंतः-वन-गोचरा ।")


# ---- Stage B review, M2: avagraha is significant ---------------------------------

@pytest.mark.parametrize("mula,pada", [
    ("अग्रतो नोऽभयं प्राप्तम् ।", "अग्रतः नः भयम् प्राप्तम् ।"),   # ऽ printed, अ dropped (VR.3.24.6)
    ("रामोऽब्रवीत् ।", "रामः ब्रवीत् ।"),
    ("लोकेऽस्मिन् ।", "लोके स्मिन् ।"),
    ("ततो धर्मः ।", "ततः अधर्मः ।"),                              # अ invented where no ऽ is printed
    ("वने भयम् ।", "वने अभयम् ।"),
    ("ते स्वस्था वानराः ।", "ते अस्वस्थाः वानराः ।"),              # VR.6.69.78
    ("रक्षोधिपतेः ।", "रक्षः अधिपतेः ।"),                          # between two words the ऽ is required
])
def test_avagraha_mismatch_fails(mula, pada):
    assert not ok(mula, pada)


@pytest.mark.parametrize("mula,pada", [
    ("सोऽहम् ।", "सः अहम् ।"),
    ("लोकेऽस्मिन् ।", "लोके अस्मिन् ।"),
    ("रामोऽब्रवीत् ।", "रामः अब्रवीत् ।"),
    ("तथाऽऽतिथ्यं चकार ।", "तथा आतिथ्यम् चकार ।"),   # ऽऽ after a long ā from ā + ā (VR.1.49.18)
    ("यथाऽसति ।", "यथा असति ।"),                    # ऽ after a long ā from ā + a (VR.2.106.4)
    ("तथातिथ्यम् ।", "तथा आतिथ्यम् ।"),              # and no ऽ there is equally fine
    ("रक्षोधिपतेः ।", "रक्षः-अधिपतेः ।"),            # inside a compound the ऽ is optional
    ("रक्षोऽधिपतेः ।", "रक्षः-अधिपतेः ।"),
    ("पुनरपि ।", "पुनः अपि ।"),                      # r-stem: no elision, no ऽ
])
def test_avagraha_agreement_passes(mula, pada):
    assert ok(mula, pada)


def test_loose_avagraha_mode_reports_what_the_old_checker_accepted():
    # used only to tell "split and printed ऽ disagree" from any other failure
    assert check_rejoin(["ततो धर्मः ।"], ["ततः अधर्मः ।"], avagraha=False)["ok"]
    assert not check_rejoin(["ततो धर्मः ।"], ["ततः धर्मम् ।"], avagraha=False)["ok"]
