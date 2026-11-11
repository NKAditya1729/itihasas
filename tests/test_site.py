import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    out = tmp_path_factory.mktemp("site")
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_site.py"), "--out", str(out)], check=True)
    return out


def test_itihasas_home_links_the_ramayana(site):
    home = (site / "index.html").read_text()
    assert "इतिहासाः" in home and 'href="ramayanam/"' in home
    assert (site / ".nojekyll").exists()


def test_reader_back_link_goes_to_the_itihasas_home(site):
    assert 'href="../" class="archive-back">← इतिहासाः' in (site / "ramayanam" / "index.html").read_text()


def test_shell_and_assets_are_present(site):
    site = site / "ramayanam"
    for f in ["index.html", "aadharah.html", "base.css", "vr.css", "vr.js", "favicon.svg", ".nojekyll",
              "vendor/sanscript-1.3.3.js", "assets/fonts/TiroDevanagariSanskrit-Regular.ttf"]:
        if f == ".nojekyll":
            continue
        assert (site / f).exists(), f


def test_base_css_is_the_unchanged_vsn_stylesheet(site):
    vsn = ROOT / "web" / "from-sarala-vedanta" / "vsn.css"   # vendored, unchanged
    assert (site / "ramayanam" / "base.css").read_bytes() == vsn.read_bytes()


def test_every_sarga_file_and_the_index_are_copied(site):
    site = site / "ramayanam"
    index = json.loads((site / "data" / "vr" / "index.json").read_text())
    assert len(index["sargas"]) == 645
    for x in index["sargas"]:
        assert (site / "data" / "vr" / str(x["k"]) / f"{x['s']:03d}.json").exists()


def test_path_urls_are_thin_shells_opening_the_reader(site):
    assert 'location.replace("../#VR.1")' in (site / "ramayanam" / "1" / "index.html").read_text()
    shell = (site / "ramayanam" / "6" / "128" / "index.html").read_text()
    assert 'location.replace("../../#VR.6.128")' in shell
    assert 'href="../../#VR.6.128"' in shell   # works without JavaScript too


# ---- Stage B review, M1: machine splits are marked as unreviewed ---------------------

def test_published_verses_carry_padaccheda_status(site):
    d = json.loads((site / "ramayanam" / "data" / "vr" / "1" / "001.json").read_text())
    assert all("padaccheda_status" in v for v in d["verses"])
    assert all((v["padaccheda_status"] is None) == (v["groups"] is None) for v in d["verses"])


def test_reader_marks_seed_splits_and_shows_the_mark_only_in_pada_mode(site):
    js = (site / "ramayanam" / "vr.js").read_text()
    css = (site / "ramayanam" / "vr.css").read_text()
    assert "padaccheda_status !== 'reviewed'" in js and "असमीक्षितम्" in js
    assert ".pada-seed{display:none}" in css and "body.pada .pada-seed{display:block}" in css


def test_reader_hides_the_toggle_on_a_sarga_without_any_split(site):
    js = (site / "ramayanam" / "vr.js").read_text()
    assert "$('#pada-toggle').hidden" in js
    assert "#pada-toggle[hidden]{display:none}" in (site / "ramayanam" / "vr.css").read_text()


def test_shell_and_reader_ask_for_the_new_files(site):
    shell = (site / "ramayanam" / "index.html").read_text()
    assert "vr.js?v=3" in shell and "vr.css?v=3" in shell
    assert "'?v=3'" in (site / "ramayanam" / "vr.js").read_text()


# ---- approved corrections on the site (CLAUDE.md §12.5) -------------------------------

def test_reader_shows_the_corrected_text_with_a_mark_and_the_source_text_on_tap(site):
    js = (site / "ramayanam" / "vr.js").read_text()
    css = (site / "ramayanam" / "vr.css").read_text()
    assert "v.lines_corrected || v.lines" in js and "संशोधितम्" in js and "corr-orig" in js
    assert "aria-expanded" in js and ".corr-mark" in css
    assert "vr.js?v=3" in (site / "ramayanam" / "index.html").read_text() and "'?v=3'" in js


def test_published_data_carries_the_corrections_beside_the_untouched_source(site):
    d = json.loads((site / "ramayanam" / "data" / "vr" / "1" / "001.json").read_text())
    v = next(x for x in d["verses"] if x["id"] == "VR.1.1.100")
    assert v["lines"][1].startswith("त् क्षत्रियो") and v["lines_corrected"][1].startswith("स्यात् क्षत्रियो")
    assert v["correction"]["approved_by"] == "Aditya"
