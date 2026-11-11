"""Stage B: padaccheda_status (review M1), mūla flags (M5), no outside calls (brief §4)."""
import json
from pathlib import Path

import jsonschema
import pytest

from vrtools.build import add_flag, make_sarga, padaccheda_status, status_errors
from vrtools.parse import parse_sarga

ROOT = Path(__file__).resolve().parent.parent
PAGE = """'''श्रीमद्वाल्मीकियरामायणे बालकाण्डे प्रथमः सर्गः ॥१-१॥'''
तपः स्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।
नारदं परिपप्रच्छ वाल्मीकिर्मुनिपुङ्गवम् ॥१-१-१॥

इत्यार्षे श्रीमद्रामायणे वाल्मीकीये आदिकाव्ये बालकाण्डे प्रथमः सर्गः ॥१-१॥
"""
REV = {"revid": 123, "timestamp": "2026-04-01T10:09:26Z", "title": "रामायणम्/बालकाण्डम्/सर्गः १"}
SPLIT = ["तपः-स्वाध्याय-निरतम् तपस्वी वाक्-विदाम् वरम् ।", "नारदम् परिपप्रच्छ वाल्मीकिः मुनि-पुङ्गवम् ॥"]


def sarga():
    s = make_sarga(parse_sarga(PAGE, 1, 1), 1, 1, REV)
    s["verses"][0]["crosswalk"] = {"ce": None, "relation": "absent", "score": 0.0}
    return s


def schema_errors(s):
    schema = json.loads((ROOT / "schema" / "sarga.schema.json").read_text())
    return [e.message for e in jsonschema.Draft202012Validator(schema).iter_errors(s)]


# ---- padaccheda_status ---------------------------------------------------------

def test_a_new_verse_has_no_padaccheda_status():
    assert sarga()["verses"][0]["padaccheda_status"] is None


def test_status_is_seed_for_a_machine_split_and_none_without_a_split():
    assert padaccheda_status({"padaccheda_lines": SPLIT}) == "seed"
    assert padaccheda_status({"padaccheda_lines": SPLIT, "padaccheda_status": "seed"}) == "seed"
    assert padaccheda_status({"padaccheda_lines": None, "padaccheda_status": "seed"}) is None


def test_a_reviewed_split_is_never_downgraded():
    assert padaccheda_status({"padaccheda_lines": SPLIT, "padaccheda_status": "reviewed"}) == "reviewed"


def test_schema_accepts_the_three_status_values_only():
    s = sarga()
    for value in (None, "seed", "reviewed"):
        s["verses"][0]["padaccheda_status"] = value
        assert schema_errors(s) == []
    s["verses"][0]["padaccheda_status"] = "final"
    assert schema_errors(s)


def test_schema_requires_the_status_field():
    s = sarga()
    del s["verses"][0]["padaccheda_status"]
    assert any("padaccheda_status" in e for e in schema_errors(s))


def test_status_must_agree_with_the_presence_of_a_split():
    v = sarga()["verses"][0]
    assert status_errors(v) == []
    v["padaccheda_status"] = "seed"
    assert status_errors(v) == ["VR.1.1.1: padaccheda_status is seed but there is no padaccheda"]
    v["padaccheda_lines"], v["padaccheda_status"] = SPLIT, None
    assert status_errors(v) == ["VR.1.1.1: padaccheda without padaccheda_status"]


# ---- correction fields of CLAUDE.md §12 ------------------------------------------

def test_schema_accepts_an_approved_correction_and_rejects_an_unsigned_one():
    s = sarga()
    v = s["verses"][0]
    v["lines_corrected"] = ["तपःस्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।", v["lines"][1]]
    v["correction"] = {"what": "space removed inside the compound", "evidence": "printed edition",
                       "approved_by": "Aditya", "date": "2026-11-11"}
    assert schema_errors(s) == []
    del v["correction"]["approved_by"]
    assert schema_errors(s)


def test_lines_corrected_needs_its_correction_record():
    v = sarga()["verses"][0]
    v["lines_corrected"] = list(v["lines"])
    assert status_errors(v) == ["VR.1.1.1: lines_corrected without an approved correction record"]


# ---- flags ---------------------------------------------------------------------

def test_add_flag_is_idempotent_and_keeps_the_note_once():
    v = sarga()["verses"][0]
    add_flag(v, "mula_suspect", "space inside a compound")
    add_flag(v, "mula_suspect", "space inside a compound")
    assert v["review"]["flags"].count("mula_suspect") == 1
    assert v["review"]["notes"] == "mula_suspect: space inside a compound"
    add_flag(v, "not_mula", "a commentary sentence")
    assert v["review"]["notes"] == "mula_suspect: space inside a compound | not_mula: a commentary sentence"


def test_the_mula_flag_list_names_real_verses_and_known_flags():
    entries = json.loads((ROOT / "data" / "meta" / "mula_flags.json").read_text())
    hashes = json.loads((ROOT / "data" / "meta" / "mula_hashes.json").read_text())
    assert entries and all(e["id"] in hashes and e["flag"] in ("mula_suspect", "not_mula") and e["note"] for e in entries)
    assert {"VR.1.1.100", "VR.2.90.5"} <= {e["id"] for e in entries}


# ---- no outside calls ------------------------------------------------------------

def test_dharmamitra_is_not_called_unless_explicitly_allowed(monkeypatch):
    import scripts.seed_dharmamitra as sd
    monkeypatch.delenv("DHARMAMITRA_ALLOW_NETWORK", raising=False)
    monkeypatch.setattr(sd, "_STORE", {"known": "kno wn"})
    monkeypatch.setattr(sd.requests, "post", lambda *a, **k: pytest.fail("network call attempted"))
    assert sd.segment(["known"]) == ["kno wn"]
    with pytest.raises(RuntimeError, match="DHARMAMITRA_ALLOW_NETWORK"):
        sd.segment(["a text that is not in the cache"])


# ---- avagraha_mismatch flag (review M2) --------------------------------------------

def _verse_with_seed(split, **seed):
    v = sarga()["verses"][0]
    v["padaccheda_lines"], v["seed"] = split, seed
    return v


def test_avagraha_mismatch_is_flagged_even_when_another_source_seeded_the_verse():
    # VR.2.100.25: the mūla prints एकोप्यमात्यो without ऽ; the DCS split एकः अपि is rejected and
    # Dharmamitra's (different) split is shown, so the reviewer must be told
    from scripts.check_rejoin import flag_avagraha
    v = _verse_with_seed(SPLIT, source="dharmamitra", dcs_avagraha_mismatch=["एकः अपि अमात्यः ।"])
    flag_avagraha(v, v["seed"])
    assert "avagraha_mismatch" in v["review"]["flags"] and "एकः अपि अमात्यः" in v["review"]["notes"]


def test_avagraha_flag_is_removed_when_the_mismatch_is_gone():
    from scripts.check_rejoin import flag_avagraha
    v = _verse_with_seed(None, source=None, dcs_avagraha_mismatch=["क ।"])
    flag_avagraha(v, v["seed"])
    flag_avagraha(v, {"source": "dcs"})
    assert "avagraha_mismatch" not in v["review"]["flags"] and v["review"]["notes"] == ""


# ---- findings of the independent code review (2026-11-11) ---------------------------

def test_add_flag_is_idempotent_for_a_note_that_contains_the_separator():
    v = sarga()["verses"][0]
    for _ in range(3):
        add_flag(v, "mula_suspect", "reading a | reading b")
    assert v["review"]["notes"] == "mula_suspect: reading a | reading b"


def test_a_reviewed_verse_keeps_whatever_flags_its_reviewer_left():
    from scripts.check_rejoin import flag_avagraha
    v = _verse_with_seed(SPLIT, source="dcs", dcs_avagraha_mismatch=["क ।"])
    v["padaccheda_status"] = "reviewed"
    flag_avagraha(v, v["seed"])
    assert "avagraha_mismatch" not in v["review"]["flags"]


def test_ingest_refuses_to_rebuild_a_sarga_that_has_reviewed_work():
    from vrtools.build import has_reviewed_work
    s = sarga()
    assert not has_reviewed_work(s)
    s["verses"][0]["padaccheda_status"] = "reviewed"
    assert has_reviewed_work(s)
    s = sarga()
    s["verses"][0]["anvaya"] = "तपस्वी वाल्मीकिः नारदं परिपप्रच्छ ।"
    assert has_reviewed_work(s)


# ---- approved corrections (CLAUDE.md §12; Aditya, 2026-11-11) -------------------------

def test_text_lines_is_the_corrected_text_where_one_exists():
    from vrtools.build import text_lines
    v = sarga()["verses"][0]
    assert text_lines(v) == v["lines"]
    v["lines_corrected"] = ["तपःस्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।", v["lines"][1]]
    assert text_lines(v) == v["lines_corrected"]


RECORD = {"what": "space removed inside the compound", "evidence": "one compound", "approved_by": "Aditya", "date": "2026-11-11"}


def test_apply_correction_keeps_lines_and_records_the_approval_and_the_metre():
    from vrtools.build import apply_correction, mula_hash
    v = sarga()["verses"][0]
    before = mula_hash(v["lines"])
    apply_correction(v, {"id": v["id"], "lines_corrected": ["तपःस्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।", v["lines"][1]], "correction": RECORD})
    assert mula_hash(v["lines"]) == before                       # the Wikisource text is untouched
    assert v["lines_corrected"][0].startswith("तपःस्वाध्यायनिरतं")
    assert v["correction"] == RECORD
    assert v["metre"]["ok"] and v["metre"]["name"] == "अनुष्टुप्" and v["metre"]["of"] == "lines_corrected"
    assert v["metre_source"]["of"] == "lines"                    # what the metre check said of the source text


@pytest.mark.parametrize("entry,message", [
    ({"lines_corrected": ["क ।"], "correction": RECORD}, "line count"),
    ({"lines_corrected": None, "correction": RECORD}, "same as the source"),
    ({"lines_corrected": ["तपःस्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।", None], "correction": {**RECORD, "approved_by": ""}}, "approved_by"),
])
def test_apply_correction_refuses_a_malformed_or_unapproved_entry(entry, message):
    from vrtools.build import apply_correction
    v = sarga()["verses"][0]
    lines = entry["lines_corrected"] or list(v["lines"])
    lines = [l if l is not None else v["lines"][i] for i, l in enumerate(lines)]
    with pytest.raises(ValueError, match=message):
        apply_correction(v, {"id": v["id"], "lines_corrected": lines, "correction": entry["correction"]})


def test_a_correction_in_the_data_must_be_the_approved_one():
    from vrtools.build import apply_correction, correction_errors
    v = sarga()["verses"][0]
    entry = {"id": v["id"], "lines_corrected": ["तपःस्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।", v["lines"][1]], "correction": RECORD}
    assert correction_errors(v, {}) == []                        # no correction: nothing to check
    apply_correction(v, entry)
    assert correction_errors(v, {v["id"]: entry}) == []
    assert correction_errors(v, {}) == [f"{v['id']}: lines_corrected is not in data/meta/corrections.json"]
    v["lines_corrected"][0] = "तपःस्वाध्यायनिरतं तपस्वी वाग्विदां वरः ।"
    assert correction_errors(v, {v["id"]: entry}) == [f"{v['id']}: lines_corrected differs from the approved correction"]


def test_an_approved_correction_missing_from_the_data_is_an_error():
    from vrtools.build import correction_errors
    v = sarga()["verses"][0]
    entry = {"id": v["id"], "lines_corrected": ["तपःस्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।", v["lines"][1]], "correction": RECORD}
    assert correction_errors(v, {v["id"]: entry}) == [f"{v['id']}: approved correction not applied (run scripts/apply_corrections.py)"]


def test_set_flag_note_replaces_the_earlier_note_of_the_same_flag():
    from vrtools.build import set_flag_note
    v = sarga()["verses"][0]
    add_flag(v, "not_mula", "a commentary sentence")
    add_flag(v, "mula_suspect", "proposed, not applied")
    set_flag_note(v, "mula_suspect", "corrected in lines_corrected")
    assert v["review"]["flags"].count("mula_suspect") == 1
    assert v["review"]["notes"] == "not_mula: a commentary sentence | mula_suspect: corrected in lines_corrected"


def test_the_approved_corrections_file_is_well_formed():
    entries = json.loads((ROOT / "data" / "meta" / "corrections.json").read_text())
    assert {e["id"] for e in entries} == {"VR.1.1.1", "VR.1.1.9", "VR.1.1.45", "VR.1.1.100"}
    for e in entries:
        assert set(e["correction"]) == {"what", "evidence", "approved_by", "date"} and e["correction"]["approved_by"] == "Aditya"


def test_the_four_corrected_verses_keep_their_source_text_and_pass_the_metre():
    from vrtools.build import mula_hash
    hashes = json.loads((ROOT / "data" / "meta" / "mula_hashes.json").read_text())
    d = json.loads((ROOT / "data" / "vr" / "1" / "001.json").read_text())
    by = {v["id"]: v for v in d["verses"]}
    for vid in ("VR.1.1.1", "VR.1.1.9", "VR.1.1.45", "VR.1.1.100"):
        v = by[vid]
        assert mula_hash(v["lines"]) == hashes[vid]
        assert v["lines_corrected"] != v["lines"] and v["metre"]["ok"] and v["correction"]["approved_by"] == "Aditya"
    assert by["VR.1.1.1"]["lines_corrected"][0] == "तपःस्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।"
    assert by["VR.1.1.9"]["lines_corrected"][0].endswith("श्रीमाञ्छत्रुनिबर्हणः ।")
    assert by["VR.1.1.45"]["lines_corrected"][1].startswith("ऋषीणामग्निकल्पानां दण्डकारण्यवासिनाम्")
    assert by["VR.1.1.100"]["lines_corrected"][1].startswith("स्यात् क्षत्रियो भूमिपतित्वमीयात्")
    assert sum("lines_corrected" in v for v in d["verses"]) == 4
