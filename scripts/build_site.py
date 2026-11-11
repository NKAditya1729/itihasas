"""Build the static site into site/ (or --out DIR).

site/                                           the इतिहासाः site
  index.html                                    (web/home.html)
  ramayanam/                                    the Rāmāyaṇa reader:
  index.html, aadharah.html, vr.js, vr.css      (web/)
  base.css, favicon.svg, assets/, vendor/       (web/from-sarala-vedanta/, unchanged)
  data/vr/index.json, data/vr/{k}/{sss}.json    (data/vr/)
  {k}/index.html, {k}/{s}/index.html            thin shells → reader hash routes
  .nojekyll
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web"
DESIGN = WEB / "from-sarala-vedanta"

SHELL = """<!doctype html>
<html lang="sa"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — श्रीमद्वाल्मीकिरामायणम्</title><link rel="canonical" href="{target}">
<meta http-equiv="refresh" content="0; url={target}">
<script>location.replace("{target}");</script></head>
<body><p><a href="{target}">{title}</a></p></body></html>
"""
DIG = str.maketrans("0123456789", "०१२३४५६७८९")


def build(site: Path) -> None:
    if site.exists():
        shutil.rmtree(site)
    site.mkdir(parents=True)
    shutil.copy2(WEB / "home.html", site / "index.html")
    (site / ".nojekyll").write_text("")
    out = site / "ramayanam"
    out.mkdir()
    for f in ["index.html", "aadharah.html", "vr.js", "vr.css"]:
        shutil.copy2(WEB / f, out / f)
    shutil.copy2(DESIGN / "vsn.css", out / "base.css")
    shutil.copy2(DESIGN / "favicon.svg", out / "favicon.svg")
    shutil.copytree(DESIGN / "assets", out / "assets")
    shutil.copytree(DESIGN / "vendor", out / "vendor")
    shutil.copytree(ROOT / "data" / "vr", out / "data" / "vr")
    index = json.loads((ROOT / "data" / "vr" / "index.json").read_text())
    names = {x["k"]: x["name"] for x in index["kandas"]}
    for k, name in names.items():
        (out / str(k)).mkdir(exist_ok=True)
        (out / str(k) / "index.html").write_text(SHELL.format(title=name, target=f"../#VR.{k}"))
    for x in index["sargas"]:
        d = out / str(x["k"]) / str(x["s"])
        d.mkdir(parents=True, exist_ok=True)
        title = f"{names[x['k']]} · सर्गः {str(x['s']).translate(DIG)}"
        (d / "index.html").write_text(SHELL.format(title=title, target=f"../../#{x['id']}"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "site"))
    build(Path(ap.parse_args().out))


if __name__ == "__main__":
    main()
