from scripts.seed_dharmamitra import verse_text, words_of


def test_words_of_drops_tokens_without_letters():
    # Dharmamitra emits "/" at line breaks (VR.1.2.42, VR.1.8.16)
    ws = words_of("udāra_vṛtta_artha_padaiḥ_manoramaiḥ_  / tadā_asya_")
    assert [w["form"] for w in ws] == ["udAra", "vftta", "arTa", "padEH", "manoramEH", "tadA", "asya"]


def test_verse_text_is_iast_without_dandas():
    assert verse_text(["रामः ।", "सीता ॥"]) .split() == ["rāmaḥ", "sītā"]


def test_classify_seed_comparison():
    from scripts.crosscheck_seeds import classify
    assert classify(["rAmaH", "vanam"], ["rAmaH", "vanam"]) == "agree"
    assert classify(["kftajYaH"], ["kfta", "jYaH"]) == "granularity_only"
    assert classify(["puNgavam"], ["puMgavam"]) == "agree"                      # spelling of the nasal only
    assert classify(["SokaH", "ca", "kilakAlena", "gacCatA", "hi", "apagacCati", "rAmaH"], ["rAmaH"]) == "dharmamitra_incomplete"
    assert classify(["rAma", "iti"], ["rAmaH", "iti"]) == "disagree"
