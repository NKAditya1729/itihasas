import unicodedata

from vrtools.normalize import normalize_line, is_presplit


def test_ascii_colon_after_devanagari_becomes_visarga():
    # 2.100.2 has राम: with an ASCII colon
    line, log = normalize_line("भ्रातरं भरतं राम: परिजग्राह बाहुना ॥")
    assert line == "भ्रातरं भरतं रामः परिजग्राह बाहुना ॥"
    assert log == {"colon_visarga": 1}


def test_danda_gets_exactly_one_space_before_it():
    assert normalize_line("हत्वा तु तं भीमबलं विराधं राक्षसं वने।")[0] == \
        "हत्वा तु तं भीमबलं विराधं राक्षसं वने ।"
    assert normalize_line("ततः सीतां परिष्वज्य समाश्वास्य च वीर्यवान्॥")[0] == \
        "ततः सीतां परिष्वज्य समाश्वास्य च वीर्यवान् ॥"


def test_internal_whitespace_runs_collapse_to_one_space():
    assert normalize_line("सर्वा पूर्वमियं  येषामासीत् कृत्स्ना वसुंधरा ।")[0] == \
        "सर्वा पूर्वमियं येषामासीत् कृत्स्ना वसुंधरा ।"


def test_ascii_and_doubled_dandas_become_unicode_dandas():
    assert normalize_line("क ख |")[0] == "क ख ।"
    assert normalize_line("क ख ||")[0] == "क ख ॥"
    assert normalize_line("क ख ।।")[0] == "क ख ॥"


def test_space_before_avagraha_is_removed():
    # Uttara pages type सा ऽब्रवीत्
    line, log = normalize_line("इत्युक्तवति तस्मिंस्तु वेदवत्यथ सा ऽब्रवीत् ॥")
    assert line == "इत्युक्तवति तस्मिंस्तु वेदवत्यथ साऽब्रवीत् ॥"
    assert log == {"avagraha_space": 1}


def test_zero_width_characters_are_removed():
    line, log = normalize_line("राम‍ः​ वने ।")
    assert line == "रामः वने ।"
    assert log == {"zero_width": 2}


def test_output_is_nfc():
    decomposed = "क़"  # क + nukta, composes to क़ under NFC
    assert normalize_line(decomposed + " ।")[0] == unicodedata.normalize("NFC", decomposed) + " ।"


def test_anusvara_and_homorganic_nasal_are_left_alone():
    assert normalize_line("नारदं परिपप्रच्छ वाल्मीकिर्मुनिपुङ्गवम् ॥")[0] == \
        "नारदं परिपप्रच्छ वाल्मीकिर्मुनिपुङ्गवम् ॥"
    assert normalize_line("मुनिपुंगवम् ॥")[0] == "मुनिपुंगवम् ॥"


def test_clean_line_has_empty_log():
    assert normalize_line("नारदं परिपप्रच्छ वाल्मीकिर्मुनिपुङ्गवम् ॥")[1] == {}


def test_presplit_detects_undone_sandhi():
    # Ramayana_Book / old Ayodhyā style
    assert is_presplit(["एतत् इच्छामि अहम् श्रोतुम् परम् कौतूहलम् हि मे ।",
                        "महर्षे त्वम् समर्थोऽसि ज्ञातुम् एवम् विधम् नरम् ॥"])
    assert is_presplit(["बहवो दुर्लभाः च एव ये त्वया कीर्तिता गुणाः ।", "x ॥"])


def test_presplit_is_false_for_samhita_text():
    assert not is_presplit(["एतदिच्छाम्यहं श्रोतुं परं कौतूहलं हि मे ।",
                            "महर्षे त्वं समर्थोऽसि ज्ञातुमेवंविधं नरम् ॥"])
    # pāda-final म् before a daṇḍa is normal
    assert not is_presplit(["तपः स्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।",
                            "नारदं परिपप्रच्छ वाल्मीकिर्मुनिपुङ्गवम् ॥"])
