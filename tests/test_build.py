from vrtools.build import make_sarga, mula_hash
from vrtools.parse import parse_sarga

PAGE = """'''श्रीमद्वाल्मीकियरामायणे बालकाण्डे प्रथमः सर्गः ॥१-१॥'''
तपः स्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।
नारदं परिपप्रच्छ वाल्मीकिर्मुनिपुङ्गवम् ॥१-१-१॥

को न्वस्मिन्साम्प्रतं लोके गुणवान्कश्च वीर्यवान् ।
धर्मज्ञश्च कृतज्ञश्च सत्यवाक्यो दृढव्रतः ॥१-१-२॥

को न्वस्मिन्साम्प्रतं लोके गुणवान्कश्च वीर्यवान् ।
धर्मज्ञश्च कृतज्ञश्च सत्यवाक्यो दृढव्रतः ॥१-१-२॥

एतत् इच्छामि अहम् श्रोतुम् परम् कौतूहलम् हि मे ।
महर्षे त्वम् समर्थोऽसि ज्ञातुम् एवम् विधम् नरम् ॥१-१-३॥

इत्यार्षे श्रीमद्रामायणे वाल्मीकीये आदिकाव्ये बालकाण्डे प्रथमः सर्गः ॥१-१॥
"""
REV = {"revid": 123, "timestamp": "2026-04-01T10:09:26Z", "title": "रामायणम्/बालकाण्डम्/सर्गः १"}


def sarga():
    return make_sarga(parse_sarga(PAGE, 1, 1), 1, 1, REV)


def test_sarga_header_fields():
    s = sarga()
    assert (s["schema_version"], s["work"], s["kanda"], s["kanda_name"], s["sarga"]) == \
        (1, "VR", 1, "बालकाण्डम्", 1)
    assert s["colophon"].startswith("इत्यार्षे")
    assert s["verse_count"] == 4
    assert s["provenance"]["text"] == "sa.wikisource rev 123 (2026-04-01T10:09:26Z)"
    assert s["status"]["mula"] == "done" and s["status"]["padaccheda"] == "pending"


def test_verse_ids_use_printed_numbers_and_suffixes():
    assert [v["id"] for v in sarga()["verses"]] == ["VR.1.1.1", "VR.1.1.2", "VR.1.1.2a", "VR.1.1.3"]


def test_verse_lines_are_normalised_and_logged():
    v = sarga()["verses"][0]
    assert v["lines"] == ["तपः स्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।",
                          "नारदं परिपप्रच्छ वाल्मीकिर्मुनिपुङ्गवम् ॥"]
    assert v["src_ref"] == "॥१-१-१॥"


def test_metre_is_recorded():
    assert sarga()["verses"][0]["metre"] == {"name": "अनुष्टुप्", "syllables": 32, "ok": True,
                                             "checked_by": "vidyut.chandas+vrtools.metre"}


def test_presplit_verse_is_flagged():
    flags = [v["review"]["flags"] for v in sarga()["verses"]]
    assert "source_presplit" in flags[3] and "source_presplit" not in flags[0]


def test_later_layers_are_empty_placeholders():
    v = sarga()["verses"][0]
    assert v["padaccheda_lines"] is None and v["groups"] is None
    assert v["padartha"] == [] and v["anvaya"] is None and v["vyakhya_sa"] is None
    assert v["en_simple"] is None and v["en_mixed"] is None


def test_mula_hash_depends_only_on_lines():
    v = sarga()["verses"][0]
    assert mula_hash(v["lines"]) == mula_hash(list(v["lines"]))
    assert mula_hash(v["lines"]) != mula_hash(v["lines"][:1])


def test_verse_with_non_sanskrit_sign_is_flagged_but_not_edited():
    page = "ब्राह्मणैः क्षत्ऺित्रयैर्वैश्यैः स्वकर्मनिरतैः सदा ।\nजितेन्द्रियैर्महोत्साहैर्वृतामार्यैः सहस्रशः ॥ ४२॥\n"
    v = make_sarga(parse_sarga(page, 2, 100), 2, 100, REV)["verses"][0]
    assert "क्षत्ऺित्रयैर्वैश्यैः" in v["lines"][0]
    assert "invalid_char" in v["review"]["flags"]
