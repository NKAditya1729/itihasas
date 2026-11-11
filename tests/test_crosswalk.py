from vrtools.crosswalk import align_sarga, ce_key

# CE text is IAST (GRETIL), vulgate is Devanagari (Wikisource)
CE = [
    {"uid": "CE-1-001-001", "k": 1, "s": 1, "v": 1, "lines": [["tapaḥsvādhyāyanirataṃ tapasvī vāgvidāṃ varam"],
                                                            ["nāradaṃ paripapraccha vālmīkir munipuṃgavam"]]},
    {"uid": "CE-1-001-002", "k": 1, "s": 1, "v": 2, "lines": [["ko nv asmin sāmprataṃ loke guṇavān kaś ca vīryavān"],
                                                            ["dharmajñaś ca kṛtajñaś ca satyavākyo dṛḍhavrataḥ"]]},
    {"uid": "CE-1-001-003", "k": 1, "s": 1, "v": 3, "lines": [["cāritreṇa ca ko yuktaḥ sarvabhūteṣu ko hitaḥ"],
                                                            ["vidvān kaḥ kaḥ samarthaś ca kaś caikapriyadarśanaḥ"]]},
]
VU = [
    {"id": "VR.1.1.1", "lines": ["तपः स्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।", "नारदं परिपप्रच्छ वाल्मीकिर्मुनिपुङ्गवम् ॥"]},
    # variant reading: धृढ for दृढ
    {"id": "VR.1.1.2", "lines": ["को न्वस्मिन्साम्प्रतं लोके गुणवान्कश्च वीर्यवान् ।", "धर्मज्ञश्च कृतज्ञश्च सत्यवाक्यो धृढव्रतः ॥"]},
    # only the first half is in the CE
    {"id": "VR.1.1.3", "lines": ["चारित्रेण च को युक्तः सर्वभूतेषु को हितः ।", "रामः सीता लक्ष्मणश्च वनं गच्छन्ति सत्वरम् ॥"]},
    # not in the CE
    {"id": "VR.1.1.4", "lines": ["अयं श्लोकः समीक्षितग्रन्थे नास्ति कुत्रापि ।", "इति ज्ञात्वा पठन्तु सर्वे सरलं वचः ॥"]},
]


def test_ce_key():
    assert ce_key(CE[0]) == "1.1.1"


def test_identical_verse_is_same():
    links = align_sarga(VU, CE)
    assert links["VR.1.1.1"]["ce"] == "1.1.1" and links["VR.1.1.1"]["relation"] == "same"


def test_one_letter_variant_is_still_same():
    assert links_for("VR.1.1.2") == ("1.1.2", "same")


def test_half_shared_verse_is_partial():
    assert links_for("VR.1.1.3") == ("1.1.3", "partial")


def test_verse_without_counterpart_is_absent():
    assert links_for("VR.1.1.4") == (None, "absent")


def links_for(vid):
    link = align_sarga(VU, CE)[vid]
    return link["ce"], link["relation"]


def test_sarga_map_finds_the_ce_sarga_by_shared_half_verses():
    from vrtools.crosswalk import map_sargas
    other = [{**c, "s": 7, "uid": c["uid"].replace("001", "007", 1)} for c in CE[:1]]
    ce_by_sarga = {(1, 1): CE, (1, 7): other}
    vu_sargas = {(1, 1): VU[1:3], (1, 2): VU[3:]}
    m = map_sargas(vu_sargas, ce_by_sarga)
    assert m[(1, 1)] == [(1, 1)]
    assert m[(1, 2)] == []


def test_short_half_verse_match_is_not_partial():
    ce = [{"uid": "CE-1-001-001", "k": 1, "s": 1, "v": 1, "lines": [["rāmo rājā"], ["iti"]]}]
    vu = [{"id": "VR.1.1.9", "lines": ["अयं श्लोकः समीक्षितग्रन्थे नास्ति ।", "इति ॥"]}]
    assert align_sarga(vu, ce)["VR.1.1.9"]["relation"] == "absent"
