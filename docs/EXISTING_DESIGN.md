# Existing design: inventory (Phase 0)

Inspected 2026-11-11. Local checkouts, all in `~/Documents/Mac Mini Downloads/`:

| Folder | Remote | HEAD | Role |
|---|---|---|---|
| `sarala-vedanta/` | `NKAditya1729/sarala-vedanta` | `3114af6` | The deployed hub site (GitHub Pages). Pre-built static folders. |
| `vedantic-archive-deploy/`, `vedantic-archive-antigravity/` | `NKAditya1729/vedantic-archive` | `2d5c4f1`, `2b93a83` | Astro site; source of `maitreyi/`, `madhu/` (`public/source-text/sarala*/`). |
| `vedanta-pathashala-antigravity/` | `NKAditya1729/vedanta-pathashala` (private) | `d9537463` | **The builder** for `mandukya-1/` (`out-mandukya-1-b1`, `scripts/build-*.mjs`, Node 22, no npm deps). |
| `vedanta-pathashala-review/` | — | — | Review workspace (specs, reviews, tools). |

## Which existing page to reuse

The hub has two families of reader:

1. **Heavy study reader** (`mandukya-1/`, `maitreyi/`, `madhu/`): `unit-reader.js` (69 KB), `maitreyi-reader.js`, `reader.css`, `style.css`, `maitreyi.css`, live source loading from Advaita Sharada, lexicon, grammar index. 42–60 MB per folder. Built by the private builder.
2. **Light verse reader** (`vishnu-sahasranama/`, `sanatsujatiya/`, `manasollasa/`, `brahmasutra-1/`): one `index.html` shell, one CSS (`vsn.css` 15 KB), one script (`vsn.js` 8 KB), `data/index.json` + one JSON per unit, `vendor/sanscript-1.3.3.js`, `assets/fonts/`. 1.6–8.5 MB per folder.

**The Rāmāyaṇa reader reuses family 2** (`vishnu-sahasranama/`) as its base: it is already a verse reader with the same Padaccheda toggle, script selector, font-size buttons, sidebar verse navigation and hash routing, and `vsn.css` already carries the अध्ययनसाहाय्यम् classes (`.study`, `.study-tabs`, `.st-block`, `.vy-block`, `.sec`) used by family 1. Nothing new needs to be invented for the per-verse panel.

## Design tokens (`vsn.css` `:root`)

```
--bg:#faf7f2  --paper:#fff  --side:#f3eae5  --ink:#2b2118  --muted:#6b5d4f  --line:#e4dcd0
--accent:#7a1f1f  --tint:#f3e6e0  --mula-bg:#f6ece7  --saffron:#b54510  --teal:#009688  --blue:#26408b
--font-size:20px  --header-height:54px (86px under 900px)  --shadow:0 15px 45px #2b211821
```

## Fonts

- `Tiro Devanagari Sanskrit` (`assets/fonts/TiroDevanagariSanskrit-Regular.ttf`, OFL), body `16px/2.05`; fallbacks Noto Serif Devanagari, Kohinoor Devanagari.
- `Gentium Book Plus` (`gentium-book-plus-400-latin.woff2`) when `body[data-script=iast]`.
- System Noto Serif / MN fonts for Kannada, Telugu, Tamil, Malayalam.

## Header / layout

- `header.topbar > .topbar-inner`: `#menu` (☰, mobile only), `a.archive-back` ("← वेदान्तव्याख्यादीपिका", links `../`), `span.page-name`, `.tools` with `#pada-toggle`, `select#script` (देवनागरी / IAST / ಕನ್ನಡ / తెలుగు / தமிழ் / മലയാളം), `#size-down`, `#size-up`.
- `.layout` grid `240px | 1fr`, max 1152px. `aside#sidebar.sidebar > .side-inner` (sticky): `p.side-title`, `nav#unit-list.unit-list` of `a.lesson-link` (`.active`), and for the active unit `div.verse-nav` of verse-number links; `div.side-credits` for sources.
- `main#reading`: `nav.vy-chips#chips` (sticky chip bar, `.chip-row button[aria-pressed]`), `#status`, `#content`.
- Under 900px the sidebar becomes an off-canvas drawer (`.sidebar.open`).

## Padaccheda toggle (exact mechanism)

- Button: `<button id="pada-toggle" class="reader-toggle" aria-pressed="false" title="सन्धिपाठः / पदच्छेदः">पदच्छेदः</button>`.
- JS: toggles `body.pada` and `aria-pressed`; stored in `localStorage` key `vsn-pada`.
- **Data model is word-aligned.** Each sandhi group is a triple `[sandhi_form, pada_form, marked]` rendered as
  `<span class="w[ m]"><span class="sj">…</span><span class="pd">…</span></span>`. Plain strings (spaces, daṇḍas, verse numbers) are rendered as text.
- CSS: `.w>.pd{display:none}`, `body.pada .w>.sj{display:none}`, `body.pada .w>.pd{display:inline}`; `.w.m` (doubtful split) gets a dotted underline in pada mode.
- Hyphens inside the `pd` form mark compound members (`भूत-भव्य-भवत्-प्रभुः`).

Consequence for this project: the reader needs, per verse line, an **alignment** of each saṃhitā group to its padaccheda, not two independent strings. The schema keeps `lines` and `padaccheda_lines` as specified in CLAUDE.md §4 and adds a derived `groups` array per line in the shape above (see DECISIONS / deviations).

## Verse rendering

- `div.mula-box#v-{n}` (centered, `font-size: calc(var(--font-size)*1.12)`, weight 600), optional `span.uvaca` speaker line, each line `span.vl` (block).
- `p.colophon` for the colophon; `h1.chapter-heading` + `p.chapter-sub` for the unit title.
- `nav.unit-pager` prev / next.
- Display-only transliteration with `Sanscript.t()` over text nodes; anything inside `[data-no-transliterate]` is skipped. Data always stays Devanagari.

## अध्ययनसाहाय्यम् panel (how padārtha / anvaya / vyākhyā render today)

- Family 1 (`unit-reader.js`): `mulaLayers()` builds sections in order **अन्वयः** (`clauseProse(m.anvayah)`), **पदार्थः** (`glossaryProse(m.padarthah)`; a gloss row is `padam` + `paryayah|meaning|saralah_arthah`), व्याकरणपरिचयः (sandhi, samāsa cards, pada grammar), **सरलार्थः** (`m.saralarthah`). Adhyāhāra shown as `[word] · अध्याहृतम्`.
- Markup is `details.vy-block.st-block > summary` + `.sec` blocks with `.sec-head`; the drawer variant is `.study > .study-head + .study-tabs(button[aria-pressed]) + .study-body`.
- For the Rāmāyaṇa: a per-verse `details.vy-block.st-block` under each `mula-box`, with a `.chip-row.study-tabs` of three buttons **पदार्थः · अन्वयः · सरलव्याख्या**, bodies as `.sec`. Rendered lazily (IntersectionObserver) as CLAUDE.md §3 requires. Empty layers in Stage A show nothing (no placeholder text), so Stage A pages are mūla + padaccheda only.

## How pages are generated

- Family 1: private builder `vedanta-pathashala` (`node scripts/build-live-runtime.mjs`) → `out-*` → copied into `sarala-vedanta/<folder>/`.
- Family 2: static shell + JSON copied into `sarala-vedanta/<folder>/`; the JSON is produced per text by a conversion script; the reader script is hand-written.
- The hub `sarala-vedanta/index.html` lists texts as `section.text > .text-head + ul.parts > li > a.part > span.num + span.name + span.note`. A Rāmāyaṇa row will be added there in the same shape (D6).

## Plan for this project's site (Stage A)

- `site/ramayanam/`: copy of the family-2 shell, `vsn.css` reused unchanged as `vr.css` base plus a small additive section (kāṇḍa / sarga index grids, verse panel) using only the tokens above; `vr.js` derived from `vsn.js`.
- Routing kept as hash routing like `vsn.js` (`#VR.1.1`, `#VR.1.1.5`) so one shell serves all 645 sargas; CLAUDE.md §3's path URLs (`/ramayanam/1/1/`) are generated as thin redirect shells (see DECISIONS).
- Data: `data/vr/{k}/{sss}.json` per sarga, `data/vr/index.json` for navigation.
