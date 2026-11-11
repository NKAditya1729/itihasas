"""Parser tests, built from real Wikisource snippets (cache/wikisource)."""
from vrtools.parse import parse_sarga

BALA = """{{header
 | title      = [[../]]
 | section    = बालकाण्डम्
}}
[[File:Kanda 1 BK-005.ogg|thumb|पञ्चमः सर्गः श्रूयताम्|center]]
{{रामायणम्/बालकाण्डम्}}
<poem>
'''श्रीमद्वाल्मीकियरामायणे बालकाण्डे पञ्चमः सर्गः ॥१-५॥'''

सर्वा पूर्वमियं  येषामासीत् कृत्स्ना वसुंधरा ।
प्रजापतिमुपादाय नृपाणां जयशालिनाम् ॥१-५-१॥

येषां स सगरो नाम सागरो येन खानितः ।
षष्टिपुत्रसहस्राणि यं यान्तं  पर्यवारयन् ॥१-५-२॥

'''इत्यार्षे श्रीमद्रामायणे वाल्मीकीये आदिकाव्ये बालकाण्डे पञ्चमः सर्गः ॥१-५॥'''

</poem>
==स्रोतः==
पाठकौ घनपाठी वि.श्रीरामः । [https://example.org अत्र] उपलभ्यते ।
"""

AYODHYA_PRE = """{{header
 | section    = अयोध्याकाण्डम्
}}
<div class="verse">
<pre>
जटिलं चीरवसनं प्राञ्जलिं पतितं भुवि ।
ददर्श रामो दुर्दर्शं युगान्ते भास्करं यथा ।। २.१००.१ ।।

कथञ्चिदभिविज्ञाय विवर्णवदनं कृशम् ।
भ्रातरं भरतं राम: परिजग्राह बाहुना ।। २.१००.२ ।।

कच्चित् सौम्य न ते राज्यं भ्रष्टं बालस्य शाश्वतम् ।। २.१००.३ ।।
</pre>
</div>
"""

ARANYA = """'''श्रीमद्वाल्मीकियरामायणे अरण्यकाण्डे पञ्चमः सर्गः ॥३-५॥'''
<div class="verse">
<pre>
हत्वा तु तं भीमबलं विराधं राक्षसं वने।
ततः सीतां परिष्वज्य समाश्वास्य च वीर्यवान्॥ १॥

अब्रवीद् भ्रातरं रामो लक्ष्मणं दीप्ततेजसम्।
कष्टं वनमिदं दुर्गं न च स्मो वनगोचराः॥ २॥

ते चापि पौरा नृपतेर्वचस्त-
च्छ्रुत्वा तदा लाभमिवेष्टमाशु ।
नरेन्द्रमामन्त्र्य गृहाणि गत्वा
देवान् समानर्चुरतीव हृष्टाः ॥ ३॥
</pre>
</div>

'''इति वाल्मीकि रामायणे आदि काव्ये अरण्यकाण्डे पञ्चमः सर्गः ॥३-५॥'''
"""

UTTARA = """<poem><span style="font-size: 14pt; line-height:  170%">
सुकेशं धार्मिकं दृष्ट्वा वरलब्धं च राक्षसम् ।
ग्रामणीर्नाम गन्धर्वो विश्वावसुसमप्रभः ।। ७.५.१ ।।	<br>
तस्य देववती नाम द्वितीया श्रीरिवात्मजा ।
त्रिषु लोकेषु विख्याता रूपयौवनशालिनी ।
तां सुकेशाय धर्मेण ददौ रक्षःश्रियं यथा ।। ७.५.२ ।।	<br>
तक्षं तक्षशिलायां तु पुष्कलं पुष्कलावते ।	[http://puranastudy.freeoda.com/x.htm तक्ष-पुष्कलोपरि टिप्पणी]
गन्धर्वदेशे रुचिरे गान्धारविषये च सः ।। ७.५.३ ।।	<br>
इत्यार्षे श्रीमद्रामायणे वाल्मीकीये आदिकाव्ये श्रीमदुत्तरकाण्डे पञ्चमः सर्गः ।। ५ ।।	<br>
</span></poem>
[[वर्गः:रामायणम्/उत्तरकाण्डम्]]"""


def test_kandasarga_verse_markers_become_verses_with_printed_numbers():
    s = parse_sarga(BALA, 1, 5)
    assert [v["n"] for v in s["verses"]] == [1, 2]
    assert s["verses"][0]["src_ref"] == "॥१-५-१॥"


def test_marker_is_removed_from_last_line_and_replaced_by_double_danda():
    v = parse_sarga(BALA, 1, 5)["verses"][0]
    assert v["lines"] == ["सर्वा पूर्वमियं  येषामासीत् कृत्स्ना वसुंधरा ।",
                          "प्रजापतिमुपादाय नृपाणां जयशालिनाम् ॥"]


def test_heading_and_colophon_are_not_verses():
    s = parse_sarga(BALA, 1, 5)
    assert s["source_heading"] == "श्रीमद्वाल्मीकियरामायणे बालकाण्डे पञ्चमः सर्गः ॥१-५॥"
    assert s["colophon"] == "इत्यार्षे श्रीमद्रामायणे वाल्मीकीये आदिकाव्ये बालकाण्डे पञ्चमः सर्गः ॥१-५॥"
    assert len(s["verses"]) == 2


def test_source_section_after_poem_is_ignored():
    s = parse_sarga(BALA, 1, 5)
    assert all("उपलभ्यते" not in l for v in s["verses"] for l in v["lines"])


def test_dotted_markers_and_pre_blocks():
    s = parse_sarga(AYODHYA_PRE, 2, 100)
    assert [v["n"] for v in s["verses"]] == [1, 2, 3]
    assert s["verses"][1]["src_ref"] == "।। २.१००.२ ।।"
    assert s["verses"][1]["lines"][1] == "भ्रातरं भरतं राम: परिजग्राह बाहुना ॥"


def test_single_line_verse_is_flagged_half():
    v = parse_sarga(AYODHYA_PRE, 2, 100)["verses"][2]
    assert v["lines"] == ["कच्चित् सौम्य न ते राज्यं भ्रष्टं बालस्य शाश्वतम् ॥"]
    assert v["half"] is True


def test_number_only_markers():
    s = parse_sarga(ARANYA, 3, 5)
    assert [v["n"] for v in s["verses"]] == [1, 2, 3]
    assert s["verses"][1]["src_ref"] == "॥ २॥"
    assert s["colophon"].startswith("इति वाल्मीकि रामायणे")


def test_long_metre_keeps_its_four_printed_lines():
    v = parse_sarga(ARANYA, 3, 5)["verses"][2]
    assert len(v["lines"]) == 4
    assert v["lines"][0] == "ते चापि पौरा नृपतेर्वचस्त-"
    assert v["half"] is False


def test_uttara_style_with_br_tabs_and_three_line_verse():
    s = parse_sarga(UTTARA, 7, 5)
    assert [v["n"] for v in s["verses"]] == [1, 2, 3]
    assert len(s["verses"][1]["lines"]) == 3
    assert s["colophon"].endswith("पञ्चमः सर्गः ।। ५ ।।")


def test_external_links_are_stripped_from_verse_text():
    v = parse_sarga(UTTARA, 7, 5)["verses"][2]
    assert v["lines"][0] == "तक्षं तक्षशिलायां तु पुष्कलं पुष्कलावते ।"


def test_duplicate_number_gets_suffix_and_anomaly():
    txt = "क ख ग ।\nघ ङ च ॥ १॥\n\nछ ज झ ।\nञ ट ठ ॥ १॥\n\nड ढ ण ।\nत थ द ॥ २॥\n"
    s = parse_sarga(txt, 4, 9)
    assert [(v["n"], v["suffix"]) for v in s["verses"]] == [(1, ""), (1, "a"), (2, "")]
    assert any(a["type"] == "duplicate_number" and a["n"] == 1 for a in s["anomalies"])


def test_gap_in_numbers_is_logged():
    txt = "क ख ।\nग घ ॥ १॥\n\nङ च ।\nछ ज ॥ ३॥\n"
    s = parse_sarga(txt, 4, 9)
    assert any(a["type"] == "gap" and a["missing"] == [2] for a in s["anomalies"])


def test_marker_from_other_sarga_is_logged():
    txt = "क ख ।\nग घ ॥१-६-१॥\n"
    s = parse_sarga(txt, 1, 5)
    assert any(a["type"] == "ref_mismatch" for a in s["anomalies"])


def test_text_after_last_marker_is_kept_and_flagged_unnumbered():
    txt = "क ख ।\nग घ ॥ १॥\n\nङ च ।\nछ ज ॥\n"
    s = parse_sarga(txt, 4, 9)
    assert s["verses"][-1]["lines"] == ["ङ च ।", "छ ज ॥"]
    assert "unnumbered" in s["verses"][-1]["flags"]


# --- behaviours found by running the parser over all 645 pages -------------

def test_stray_double_danda_inside_a_verse_does_not_split_it():
    # 1.1.84: the source prints ॥ where । belongs
    txt = ("ततोऽग्निवचनात् सीतां ज्ञात्वा विगतकल्मषाम् ।\nकर्मणा तेन महता त्रैलोक्यं सचराचरम् ॥१-१-८३॥\n\n"
           "सदेवर्षिगणं तुष्टं राघवस्य महात्मनः ॥\nबभौ रामः सम्प्रहृष्टः पूजितः सर्वदेवतैः ॥१-१-८४॥\n")
    s = parse_sarga(txt, 1, 1)
    assert [v["n"] for v in s["verses"]] == [83, 84]
    assert s["verses"][1]["lines"][0] == "सदेवर्षिगणं तुष्टं राघवस्य महात्मनः ॥"
    assert "inner_double_danda" in s["verses"][1]["flags"]


def test_pasted_residue_after_a_marker_is_dropped_and_logged():
    # 7.6.8: a fragment of the previous line is pasted after the marker
    txt = ("बाधन्ते समरोद्धर्षा ये च तेषां पुरःसराः ।\t\n"
           "अशिवं वपुरास्थाय जहि वै देवकण्टकान् ।। ७.६.८ ।।धन्ते समरोद्धर्षा ये च तेषां पुरःसराः ।\t\n\n"
           "क ख ग ।\nघ ङ च ।। ७.६.९ ।।\n")
    s = parse_sarga(txt, 7, 6)
    assert s["verses"][1]["lines"] == ["क ख ग ।", "घ ङ च ॥"]
    assert any(a["type"] == "residue_after_marker" and a["text"].startswith("धन्ते") for a in s["anomalies"])


def test_doubled_marker_leaves_nothing_in_the_next_verse():
    # 1.34.16: ॥ १६ ॥१-३४-१६॥
    txt = ("शनैर्विसृज्यते संध्या नभो नेत्रैरिवावृतम् ।\nनक्षत्रतारागहनं ज्योतिर्भिरवभासते ॥ १६ ॥१-३४-१६॥\n\n"
           "उत्तिष्ठते च शीतांशुः शशी लोकतमोनुदः ।\nह्लादयन् प्राणिनां लोके मनांसि प्रभया स्वया ॥१-३४-१७॥\n")
    s = parse_sarga(txt, 1, 34)
    assert [v["n"] for v in s["verses"]] == [16, 17]
    assert s["verses"][1]["lines"][0] == "उत्तिष्ठते च शीतांशुः शशी लोकतमोनुदः ।"


def test_praksipta_passage_after_colophon_becomes_an_appendix():
    txt = ("क ख ।\nग घ॥ ३६॥\n\n"
           "इत्यार्षे श्रीमद्रामायणे वाल्मीकीये आदिकाव्ये अरण्यकाण्डे षट्पञ्चाशः सर्गः ॥३-५६॥\n\n"
           "५६अ प्रक्षिप्तः\n\n\nप्रवेशितायां सीतायां लङ्कां प्रति पितामहः।\nतदा प्रोवाच देवेन्द्रं परितुष्टं शतक्रतुम्॥ १॥\n")
    s = parse_sarga(txt, 3, 56)
    assert len(s["verses"]) == 1
    assert s["appendix"]["heading"] == "५६अ प्रक्षिप्तः"
    assert s["appendix"]["verses"][0]["lines"][0] == "प्रवेशितायां सीतायां लङ्कां प्रति पितामहः।"
    assert not any(a["type"] == "text_after_colophon" for a in s["anomalies"])


def test_colophon_wrapped_in_curly_quotes_is_recognised():
    txt = "क ख ।\nग घ॥ ७०॥\n\n”’इत्यार्षे श्रीमद्रामायणे वाल्मीकीये आदिकाव्ये युद्धकाण्डे द्व्यधिकशततमः सर्गः ॥ १०२ ॥”’\n"
    s = parse_sarga(txt, 6, 102)
    assert s["colophon"] == "इत्यार्षे श्रीमद्रामायणे वाल्मीकीये आदिकाव्ये युद्धकाण्डे द्व्यधिकशततमः सर्गः ॥ १०२ ॥"
    assert len(s["verses"]) == 1


def test_systematically_broken_numbering_is_replaced_by_position():
    # 1.29: ॥१-२९-२५॥ printed again and again
    txt = "".join(f"क{i} ख ।\nग घ ॥१-२९-{n}॥\n\n" for i, n in
                  enumerate(["२५", "२", "२५", "२५", "२५", "६"]))
    s = parse_sarga(txt, 1, 29)
    assert [v["n"] for v in s["verses"]] == [1, 2, 3, 4, 5, 6]
    assert all(v["suffix"] == "" and "renumbered" in v["flags"] for v in s["verses"])
    assert s["verses"][0]["src_ref"] == "॥१-२९-२५॥"
    assert any(a["type"] == "renumbered_sarga" for a in s["anomalies"])


def test_missing_colophon_is_logged():
    s = parse_sarga("क ख ।\nग घ॥ १॥\n", 5, 61)
    assert any(a["type"] == "missing_colophon" for a in s["anomalies"])


def test_wiki_indentation_colons_are_markup_not_text():
    # VR.1.2.42: continuation pādas are indented with ":" / "::" in the wikitext
    txt = "उदारवृत्तार्थपदैर्मनोरमै-\n::स्तदास्य रामस्य चकार कीर्तिमान् ।\nसमाक्षरैः श्लोकशतैर्यशस्विनो\n:::यशस्करं काव्यमुदारदर्शनः ॥१-२-४२॥\n"
    v = parse_sarga(txt, 1, 2)["verses"][0]
    assert v["lines"][1] == "स्तदास्य रामस्य चकार कीर्तिमान् ।"
    assert v["lines"][3] == "यशस्करं काव्यमुदारदर्शनः ॥"
