from vrtools.metre import identify

VR_1_1_1 = ["तपः स्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।",
            "नारदं परिपप्रच्छ वाल्मीकिर्मुनिपुङ्गवम् ॥"]
# 3.56.36, vaṃśastha
VR_3_56_36 = ["न विन्दते तत्र तु शर्म मैथिली", "विरूपनेत्राभिरतीव तर्जिता ।",
              "पतिं स्मरन्ती दयितं च देवरं", "विचेतनाभूद् भयशोकपीडिता ॥"]
# 3.56a style upajāti (indravajrā / upendravajrā mixed), from 2.3 colophon verse
UPAJATI = ["ते चापि पौरा नृपतेर्वचस्त-", "च्छ्रुत्वा तदा लाभमिवेष्टमाशु ।",
           "नरेन्द्रमामन्त्र्य गृहाणि गत्वा", "देवान् समानर्चुरतीव हृष्टाः ॥"]


def test_ordinary_shloka_is_anushtup_ok():
    m = identify(VR_1_1_1)
    assert m == {"name": "अनुष्टुप्", "syllables": 32, "ok": True}


def test_shloka_missing_a_syllable_is_not_ok():
    broken = ["तपः स्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।", "नारदं परिपप्रच्छ वाल्मीकिर्मुनिपुङ्ग ॥"]
    m = identify(broken)
    assert m["ok"] is False and m["syllables"] == 31


def test_shloka_with_wrong_even_pada_cadence_is_not_ok():
    # even pāda must have ⏑ – ⏑ in syllables 5–7; "वाग्विदां श्रेष्ठः" gives ⏑ – –
    bad = ["तपः स्वाध्यायनिरतं तपस्वी वाग्विदां श्रेष्ठः ।", "नारदं परिपप्रच्छ वाल्मीकिर्मुनिपुङ्गवम् ॥"]
    assert identify(bad)["ok"] is False


def test_six_pada_and_half_shlokas():
    six = VR_1_1_1 + VR_1_1_1[:1]
    assert identify(six) == {"name": "अनुष्टुप्", "syllables": 48, "ok": True}
    assert identify(VR_1_1_1[:1])["name"] == "अनुष्टुप्"


def test_vrtta_metre_is_named_from_vidyut():
    m = identify(VR_3_56_36)
    assert m["name"] == "वंशस्थ" and m["ok"] is True and m["syllables"] == 48


def test_mixed_upajati_is_recognised():
    m = identify(UPAJATI)
    assert m["name"] == "उपजातिः" and m["ok"] is True


def test_unknown_metre_reports_none():
    m = identify(["राम राम राम ।", "सीता ॥"])
    assert m["name"] is None and m["ok"] is False


def test_stray_non_sanskrit_signs_do_not_crash_the_scan():
    # 2.100.42 has क्षत्ऺित्रयैः (U+093A), 5.44.4 has नभश्चॆव (U+0946)
    m = identify(["ब्राह्मणैः क्षत्ऺित्रयैर्वैश्यैः स्वकर्मनिरतैः सदा ।",
                  "प्रदिशश्च नभश्चॆव सहसा समपूर्यत ॥"])
    assert m["name"] in ("अनुष्टुप्", None)


def test_shloka_that_also_fits_a_matra_pattern_is_still_anushtup():
    # VR.1.1.5: vidyut matches upagīti (a mātrā metre) first
    m = identify(["एतदिच्छाम्यहं श्रोतुं परं कौतूहलं हि मे ।",
                  "महर्षे त्वं समर्थोऽसि ज्ञातुमेवंविधं नरम् ॥"])
    assert m == {"name": "अनुष्टुप्", "syllables": 32, "ok": True}


def test_matra_match_on_a_half_split_shloka_is_suspect():
    # VR.2.51.3 (half-split source): undone sandhi adds syllables, vidyut says āryā
    m = identify(["उचितः अयम् जनः सर्वः क्लेशानाम् त्वम् सुख उचितः ।",
                  "गुप्ति अर्थम् जागरिष्यामः काकुत्स्थस्य वयम् निशाम् ॥"])
    assert m["name"] == "आर्या" and m["ok"] is False
