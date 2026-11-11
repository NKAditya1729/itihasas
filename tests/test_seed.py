from vrtools.dcs import parse_dcs, pausal_candidates
from vrtools.seed import seed_verse

DCS = """# id = R.1.1.1
tapaH	tapas	pos=n,comp=y
svADyAya	svADyAya	pos=n,comp=y
niratam	niram	pos=va,g=m,c=2,n=s,f=part
tapasvI	tapasvin	pos=n,g=m,c=1,n=s
vAc	vAc	pos=n,comp=y
vidAm	vid	pos=a,g=m,c=6,n=p
varam	vara	pos=a,g=m,c=2,n=s
nAradam	nArada	pos=n,g=m,c=2,n=s
paripapracCa	paripracC	pos=v,p=3,n=s,l=lit
vAlmIkiH	vAlmIki	pos=n,g=m,c=1,n=s
muni	muni	pos=n,comp=y
puMgavam	puMgava	pos=n,g=m,c=2,n=s

# id = R.1.1.2
ko	ka	pos=n,g=m,c=1,n=s
nv	nu	pos=i
asmin	idam	pos=n,g=m,c=7,n=s
sAmpratam	sAMpratam	pos=i
loke	loka	pos=n,g=m,c=7,n=s
guRavAn	guRavat	pos=a,g=m,c=1,n=s
kaH	ka	pos=n,g=m,c=1,n=s
ca	ca	pos=i
vIryavAn	vIryavat	pos=a,g=m,c=1,n=s
Darma	Darma	pos=n,comp=y
jYaH	jYa	pos=a,g=m,c=1,n=s
ca	ca	pos=i
kftajYaH	kftajYa	pos=a,g=m,c=1,n=s
ca	ca	pos=i
satya	satya	pos=a,comp=y
vAkyaH	vAkya	pos=n,g=m,c=1,n=s
dfQa	dfQa	pos=a,comp=y
vrataH	vrata	pos=n,g=m,c=1,n=s
"""
VR_1_1_1 = ["तपः स्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।", "नारदं परिपप्रच्छ वाल्मीकिर्मुनिपुङ्गवम् ॥"]
VR_1_1_2 = ["को न्वस्मिन्साम्प्रतं लोके गुणवान्कश्च वीर्यवान् ।", "धर्मज्ञश्च कृतज्ञश्च सत्यवाक्यो दृढव्रतः ॥"]


def test_parse_dcs_marks_compound_members():
    d = parse_dcs(DCS)
    assert list(d) == ["1.1.1", "1.1.2"]
    w = d["1.1.1"][0]
    assert (w["form"], w["lemma"], w["comp"]) == ("tapaH", "tapas", True)
    assert d["1.1.1"][2]["comp"] is False and d["1.1.1"][2]["tags"]["c"] == "2"


def test_pausal_restores_sandhi_forms_kept_by_dcs():
    assert pausal_candidates({"form": "ko", "lemma": "ka", "tags": {"pos": "n", "c": "1"}, "comp": False})[0] == "kaH"
    assert pausal_candidates({"form": "nv", "lemma": "nu", "tags": {"pos": "i"}, "comp": False})[0] == "nu"
    assert pausal_candidates({"form": "vAc", "lemma": "vAc", "tags": {"pos": "n"}, "comp": True})[0] == "vAk"
    assert pausal_candidates({"form": "manas", "lemma": "manas", "tags": {"pos": "n"}, "comp": True})[0] == "manaH"


def test_pausal_keeps_genuine_forms_first():
    assert pausal_candidates({"form": "varam", "lemma": "vara", "tags": {"pos": "a", "c": "2"}, "comp": False})[0] == "varam"
    assert pausal_candidates({"form": "aho", "lemma": "aho", "tags": {"pos": "i"}, "comp": False}) == ["aho"]


def test_seed_from_dcs_gives_pausal_padaccheda_in_mula_spelling():
    r = seed_verse(VR_1_1_1, parse_dcs(DCS)["1.1.1"])
    assert r["ok"]
    assert r["padaccheda_lines"] == ["तपः-स्वाध्याय-निरतम् तपस्वी वाक्-विदाम् वरम् ।",
                                     "नारदम् परिपप्रच्छ वाल्मीकिः मुनि-पुङ्गवम् ॥"]


def test_seed_restores_ko_and_nv():
    r = seed_verse(VR_1_1_2, parse_dcs(DCS)["1.1.2"])
    assert r["ok"]
    assert r["padaccheda_lines"][0] == "कः नु अस्मिन् साम्प्रतम् लोके गुणवान् कः च वीर्यवान् ।"
    # DCS keeps कृतज्ञ as one lexical word
    assert r["padaccheda_lines"][1] == "धर्म-ज्ञः च कृतज्ञः च सत्य-वाक्यः दृढ-व्रतः ॥"


def test_groups_align_sandhi_tokens_to_padas_for_the_toggle():
    r = seed_verse(VR_1_1_2, parse_dcs(DCS)["1.1.2"])
    line0 = [x for x in r["groups"][0] if not isinstance(x, str)]
    assert line0[0][:2] == ["को", "कः"]
    assert line0[1][:2] == ["न्वस्मिन्साम्प्रतं", "नु अस्मिन् साम्प्रतम्"]
    assert [g[:2] for g in line0[2:]] == [["लोके", "लोके"], ["गुणवान्कश्च", "गुणवान् कः च"], ["वीर्यवान्", "वीर्यवान्"]]
    assert r["groups"][0][-1] == " ।"


def test_groups_carry_compound_hyphen_across_a_space():
    r = seed_verse(VR_1_1_1, parse_dcs(DCS)["1.1.1"])
    items = [x for x in r["groups"][0] if not isinstance(x, str)]
    assert items[0][:2] == ["तपः", "तपः-"]
    assert items[1][:2] == ["स्वाध्यायनिरतं", "स्वाध्याय-निरतम्"]


def test_seed_fails_cleanly_on_a_different_verse():
    r = seed_verse(VR_1_1_1, parse_dcs(DCS)["1.1.2"])
    assert not r["ok"] and r["failures"]


def test_seed_window_finds_the_run_of_words_for_a_regrouped_verse():
    from vrtools.seed import seed_window
    d = parse_dcs(DCS)
    r = seed_window(VR_1_1_2, d["1.1.1"] + d["1.1.2"])
    assert r["ok"] and r["padaccheda_lines"][0].startswith("कः नु अस्मिन्")
    assert r["window"] == [12, 30]


def test_seed_window_prefers_the_exact_word_list():
    from vrtools.seed import seed_window
    r = seed_window(VR_1_1_1, parse_dcs(DCS)["1.1.1"])
    assert r["ok"] and r["window"] == [0, 12]


def test_pausal_restores_initial_a_written_as_avagraha():
    # DCS 6.40.2: वालिपुत्रोऽङ्गदोऽब्रवीत् → 'Ngado 'bravIt
    assert pausal_candidates({"form": "'Ngado", "lemma": "aNgada", "tags": {"pos": "n", "c": "1"}, "comp": False})[0] == "aNgadaH"
    assert pausal_candidates({"form": "'bravIt", "lemma": "brU", "tags": {"pos": "v"}, "comp": False})[0] == "abravIt"


def test_in_stem_compound_member_drops_its_n():
    # DCS 6.40.2: vAlin putraH for वालिपुत्रः
    assert "vAli" in pausal_candidates({"form": "vAlin", "lemma": "vAlin", "tags": {"pos": "n"}, "comp": True})


def test_natva_alternative_for_dcs_forms_without_retroflex_n():
    # VR.1.75.22 अतिकर्मणः, VR.1.72.2 अप्रमेयाणि
    assert "atikarmaRaH" in pausal_candidates({"form": "atikarmanaH", "lemma": "atikarman", "tags": {"pos": "n"}, "comp": False})
    assert "aprameyARi" in pausal_candidates({"form": "aprameyAni", "lemma": "aprameya", "tags": {"pos": "a"}, "comp": False})
    # blocked by an intervening dental (t): no ṇatva in रक्षितानि? (r … t … n)
    assert all("R" not in c for c in pausal_candidates({"form": "rakzitAni", "lemma": "rakz", "tags": {"pos": "va"}, "comp": False}))
