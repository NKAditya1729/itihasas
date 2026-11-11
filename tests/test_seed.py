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


def test_pausal_review_fixes():
    # tAMs (DCS) is tān before s; tAv is tau before a vowel; sa (nom.) is saḥ
    assert pausal_candidates({"form": "tAMs", "lemma": "tad", "tags": {"pos": "n", "c": "2", "n": "p"}, "comp": False})[0] == "tAn"
    assert pausal_candidates({"form": "tAv", "lemma": "tad", "tags": {"pos": "n", "c": "1", "n": "d"}, "comp": False})[0] == "tO"
    assert pausal_candidates({"form": "sa", "lemma": "tad", "tags": {"pos": "n", "g": "m", "c": "1", "n": "s"}, "comp": False})[0] == "saH"
    assert pausal_candidates({"form": "rAma", "lemma": "rAma", "tags": {"pos": "n", "g": "m", "c": "8", "n": "s"}, "comp": False})[0] == "rAma"


def test_seed_window_finds_a_start_with_vowel_sandhi():
    from vrtools.seed import seed_window
    w = lambda f, comp=False, **t: {"form": f, "lemma": f, "tags": t, "comp": comp}
    words = [w("x"), w("y"), w("na", pos="i"), w("api", pos="i"), w("rAmaH", pos="n"), w("vanam", pos="n"), w("gataH", pos="va")]
    r = seed_window(["नापि रामो वनं गतः ।"], words)
    assert r["ok"] and r["window"] == [2, 7]


def test_mula_spelling_ignores_the_final_m():
    r = seed_verse(VR_1_1_2, parse_dcs(DCS)["1.1.2"])
    assert "साम्प्रतम्" in r["padaccheda_lines"][0]


def test_dcs_prefix_sa_is_a_compound_member():
    # DCS gives the prefix of सलीलम् as a separate indeclinable "sa"
    d = parse_dcs("# id = R.1.66.9\nsa\tsa\tpos=i\nlIlam\tlIlam\tpos=i\nidam\tidam\tpos=n,g=n,c=2,n=s\nabravIt\tbrU\tpos=v,p=3,n=s,l=impf\n")
    r = seed_verse(["सलीलमिदमब्रवीत् ॥"], d["1.66.9"])
    assert r["ok"] and r["padaccheda_lines"] == ["स-लीलम् इदम् अब्रवीत् ॥"]


def test_untagged_sa_prefers_sah():
    assert pausal_candidates({"form": "sa", "lemma": "sa", "tags": {}, "comp": False})[0] == "saH"


def test_untagged_sa_seed_comes_out_as_sah_and_passes_the_check():
    from vrtools.sandhi import check_rejoin
    w = lambda f: {"form": f, "lemma": f, "tags": {}, "comp": False}
    r = seed_verse(["स तच्छ्रुत्वा ।"], [w("sa"), w("tat"), w("SrutvA")])
    assert r["ok"] and r["padaccheda_lines"] == ["सः तत् श्रुत्वा ।"]
    assert check_rejoin(["स तच्छ्रुत्वा ।"], r["padaccheda_lines"])["ok"]


# ---- Stage B review, M2: avagraha in seeding ------------------------------------

def _w(form, comp=False, **tags):
    return {"form": form, "lemma": form, "tags": tags, "comp": comp}


def test_seed_accepts_a_printed_avagraha_and_aligns_the_groups():
    r = seed_verse(["रामोऽब्रवीद्वचः ।"], [_w("rAmaH", pos="n", c="1", n="s", g="m"), _w("abravIt", pos="v"), _w("vacaH", pos="n")])
    assert r["ok"] and r["padaccheda_lines"] == ["रामः अब्रवीत् वचः ।"]
    assert [g[:2] for g in r["groups"][0] if not isinstance(g, str)] == [["रामोऽब्रवीद्वचः", "रामः अब्रवीत् वचः"]]


def test_seed_rejects_an_elided_a_that_the_mula_does_not_print():
    # VR.6.69.78: ते स्वस्थाः must not be seeded as ते अस्वस्थाः
    r = seed_verse(["ते स्वस्था वानराः ।"], [_w("te", pos="n"), _w("asvasTAH", pos="a"), _w("vAnarAH", pos="n")])
    assert not r["ok"]


def test_seed_takes_a_compound_without_printed_avagraha():
    r = seed_verse(["रक्षोधिपतेः ।"], [_w("rakzaH", comp=True, pos="n"), _w("aDipateH", pos="n")])
    assert r["ok"] and r["padaccheda_lines"] == ["रक्षः-अधिपतेः ।"]


# ---- Stage B review, M4: pausal forms follow the DCS morphology -------------------

def _d(form, lemma, **tags):
    return {"form": form, "lemma": lemma, "tags": tags, "comp": False}


def test_no_visarga_is_invented_for_a_dative_or_a_vocative():
    # VR.1.67.1 रामाय इति was seeded as रामायः इति; VR.2.34.6 व्याघ्र (voc.)
    assert pausal_candidates(_d("rAmAya", "rAma", pos="n", g="m", c="4", n="s")) == ["rAmAya"]
    assert pausal_candidates(_d("vyAGra", "vyAGra", pos="n", g="m", c="8", n="s")) == ["vyAGra"]


def test_a_stem_nominative_singular_still_prefers_the_visarga():
    assert pausal_candidates(_d("rAma", "rAma", pos="n", g="m", c="1", n="s"))[0] == "rAmaH"


def test_locative_and_pronominal_plural_in_a_come_from_e():
    # VR.7.32.39 युगान्त इव ← युगान्ते; VR.7.108.19 सर्व एव ← सर्वे; VR.2.105.24 उदित आदित्ये ← उदिते
    assert pausal_candidates(_d("yugAnta", "yugAnta", pos="n", g="m", c="7", n="s"))[0] == "yugAnte"
    assert pausal_candidates(_d("sarva", "sarva", pos="n", g="m", c="1", n="p"))[0] == "sarve"
    assert pausal_candidates(_d("udita", "udi", pos="va", g="m", c="7", n="s", f="part"))[0] == "udite"


def test_consonant_stem_forms_in_a_keep_both_readings():
    # राज्ञ इति ← राज्ञः (gen. sg. of rājan)
    assert pausal_candidates(_d("rAjYa", "rAjan", pos="n", g="m", c="6", n="s")) == ["rAjYa", "rAjYaH"]


def test_feminine_long_a_follows_case_and_number():
    # VR.5.13.8 आर्याया हृदयम् (gen.), VR.7.89.3 विद्रुता (acc. pl.), VR.2.26.14 सर्वा (nom. sg.)
    assert pausal_candidates(_d("AryAyA", "Arya", pos="a", g="f", c="6", n="s"))[0] == "AryAyAH"
    assert pausal_candidates(_d("vidrutA", "vidru", pos="va", g="f", c="2", n="p", f="part"))[0] == "vidrutAH"
    assert pausal_candidates(_d("sarvA", "sarva", pos="n", g="f", c="1", n="s")) == ["sarvA"]
    assert pausal_candidates(_d("tapasA", "tapas", pos="n", g="n", c="3", n="s")) == ["tapasA"]
    assert pausal_candidates(_d("mahAtejA", "mahAtejas", pos="a", g="m", c="1", n="s"))[0] == "mahAtejAH"
    assert pausal_candidates(_d("devA", "deva", pos="n", g="m", c="1", n="p"))[0] == "devAH"


def test_final_t_written_n_before_a_nasal_is_restored():
    # VR.3.43.38 यन्मां, VR.3.56.11 पातयेन्नाशयेत, VR.1.55.24 आसीन्महात्मनः, VR.4.36.11 कश्चिन्न, VR.3.22.17 जनस्थानान्महानादम्
    assert pausal_candidates(_d("yan", "yad", pos="n", g="n", c="1", n="s"))[0] == "yat"
    assert pausal_candidates(_d("pAtayen", "pAtay", pos="v", p="3", n="s", l="vidhilin"))[0] == "pAtayet"
    assert pausal_candidates(_d("AsIn", "as", pos="v", p="3", n="s", l="lan"))[0] == "AsIt"
    assert pausal_candidates(_d("kaScin", "kaScit", pos="n", g="m", c="1", n="s"))[0] == "kaScit"
    assert pausal_candidates(_d("janasTAnAn", "janasTAna", pos="n", g="n", c="5", n="s"))[0] == "janasTAnAt"


def test_a_genuine_final_n_is_left_alone():
    # VR.6.71.96 तान्मोघान्: acc. pl. of tad; a plural verb; an n-stem
    assert pausal_candidates(_d("tAn", "tad", pos="n", g="m", c="2", n="p")) == ["tAn"]
    assert pausal_candidates(_d("aBavan", "BU", pos="v", p="3", n="p", l="lan")) == ["aBavan"]
    assert pausal_candidates(_d("rAjan", "rAjan", pos="n", g="m", c="8", n="s")) == ["rAjan"]


def test_seed_restores_t_before_a_nasal_and_keeps_it_elsewhere():
    r = seed_verse(["यन्मां भवेत् ।"], [_d("yan", "yad", pos="n", g="n", c="1", n="s"), _d("mAm", "mad", pos="n", c="2", n="s"),
                                        _d("Bavet", "BU", pos="v", p="3", n="s", l="vidhilin")])
    assert r["ok"] and r["padaccheda_lines"] == ["यत् माम् भवेत् ।"]
    r = seed_verse(["तान्मोघान् ।"], [_d("tAn", "tad", pos="n", g="m", c="2", n="p"), _d("moGAn", "moGa", pos="a", g="m", c="2", n="p")])
    assert r["ok"] and r["padaccheda_lines"] == ["तान् मोघान् ।"]


def test_sh_written_ch_after_t_is_restored():
    # VR.1.57.7 तच्छ्रुत्वा was seeded as तत् छ्रुत्वा
    assert pausal_candidates(_d("CrutvA", "Sru", pos="vi"))[0] == "SrutvA"
    r = seed_verse(["तच्छ्रुत्वा ।"], [_d("tac", "tad", pos="n", g="n", c="2", n="s"), _d("CrutvA", "Sru", pos="vi")])
    assert r["ok"] and r["padaccheda_lines"] == ["तत् श्रुत्वा ।"]
    # a genuine छ stays
    assert pausal_candidates(_d("Cattram", "Cattra", pos="n", g="n", c="1", n="s")) == ["Cattram"]


def test_genuine_final_o_is_kept():
    # VR.7.36.8 भो was seeded as भः; Dharmamitra vocatives (महाबाहो) became -अः
    assert pausal_candidates(_w("Bo"))[0] == "BoH"
    assert pausal_candidates(_d("Bo", "Bo", pos="i"))[0] == "BoH"
    assert pausal_candidates(_w("bAho"))[0] == "bAho"
    assert pausal_candidates(_w("aTo"))[0] == "aTo"
    assert pausal_candidates(_d("aTo", "aTo", pos="i")) == ["aTo"]
    r = seed_verse(["भो महाबाहो शृणु ।"], [_w("Bo"), _w("mahAbAho"), _w("SfRu")])
    assert r["ok"] and r["padaccheda_lines"] == ["भोः महाबाहो शृणु ।"]


def test_no_and_so_are_nah_and_sah():
    # VR.3.24.6: DCS form "no", lemma mad (नः); untagged Dharmamitra "no" / "so"
    assert pausal_candidates(_d("no", "mad", pos="n", c="6", n="p"))[0] == "naH"
    assert pausal_candidates(_w("no"))[0] == "naH"
    assert pausal_candidates(_w("so"))[0] == "saH"
    assert pausal_candidates(_d("no", "no", pos="i")) == ["no"]


def test_seed_keeps_a_hiatus_at_the_pada_break():
    # VR.1.67.1: … रामाय | इति … (pāda break after 8 syllables; the mūla prints no sandhi there)
    words = [_d("Danur", "Danus", pos="n", g="n", c="2", n="s"), _d("darSaya", "darSay", pos="v", p="2", n="s", l="lot"),
             _d("rAmAya", "rAma", pos="n", g="m", c="4", n="s"), _d("iti", "iti", pos="i"), _d("ha", "ha", pos="i"),
             _d("uvAca", "vac", pos="v", p="3", n="s", l="lit"), _d("pArTivam", "pArTiva", pos="n", g="m", c="2", n="s")]
    r = seed_verse(["धनुर्दर्शय रामाय इति होवाच पार्थिवम् ॥"], words)
    assert r["ok"] and r["padaccheda_lines"] == ["धनुः दर्शय रामाय इति ह उवाच पार्थिवम् ॥"]


def test_consonant_stem_participle_keeps_its_visarga_reading():
    # गच्छत इति ← गच्छतः (gen. sg. of the present participle): not an a-stem form
    assert pausal_candidates(_d("gacCata", "gam", pos="va", g="m", c="6", n="s", f="part")) == ["gacCata", "gacCataH"]
