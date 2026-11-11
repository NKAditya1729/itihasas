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
