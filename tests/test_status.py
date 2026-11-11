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
