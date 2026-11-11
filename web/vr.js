/* श्रीमद्वाल्मीकिरामायणम् reader, derived from the Viṣṇusahasranāma page's vsn.js.
   Routes: #            → kāṇḍa index
           #VR.1        → sarga index of a kāṇḍa
           #VR.1.1      → sarga reader
           #VR.1.1.5    → verse (also #VR.1.1.2a, #VR.3.56A.1 for the prakṣipta appendix) */
(() => {
  const DIG = '०१२३४५६७८९';
  const deva = n => String(n).replace(/\d/g, d => DIG[d]);
  const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const $ = s => document.querySelector(s);
  const store = {
    get(k, d) { try { const v = localStorage.getItem('vr-' + k); return v === null ? d : JSON.parse(v); } catch { return d; } },
    set(k, v) { try { localStorage.setItem('vr-' + k, JSON.stringify(v)); } catch { /* private mode */ } }
  };
  const state = { pada: store.get('pada', false), script: store.get('script', 'devanagari'), size: store.get('size', 20),
    route: null, sarga: null };
  const ANUSHTUP = 'अनुष्टुप्';
  let index = null;
  const cache = {};
  const load = f => (cache[f] = cache[f] || fetch('data/' + f + '?v=5').then(r => { if (!r.ok) throw new Error(f); return r.json(); }));
  const sargaFile = (k, s) => `vr/${k}/${String(s).padStart(3, '0')}.json`;
  const kanda = k => index.kandas.find(x => x.k === k);

  /* ---------- routes ---------- */
  function parseHash() {
    const h = decodeURIComponent(location.hash.slice(1));
    const m = /^VR\.(\d+)(?:\.(\d+)(A)?(?:\.(\d+[a-z]?))?)?$/.exec(h);
    if (!m || !kanda(+m[1])) return { view: 'home' };
    if (!m[2]) return { view: 'kanda', k: +m[1] };
    const s = +m[2];
    if (!index.sargas.some(x => x.k === +m[1] && x.s === s)) return { view: 'kanda', k: +m[1] };
    return { view: 'sarga', k: +m[1], s, verse: m[4] ? `VR.${m[1]}.${s}${m[3] || ''}.${m[4]}` : null };
  }

  /* ---------- verse text ---------- */
  function item(x) {
    if (typeof x === 'string') return esc(x);
    const [sj, pd, m] = x;
    return `<span class="w${m ? ' m' : ''}"><span class="sj">${esc(sj)}</span><span class="pd">${esc(pd)}</span></span>`;
  }
  const nobreak = h => h.replace(/ ([।॥])/g, ' $1');   // display only: a daṇḍa never wraps alone
  function vlines(v) {
    if (v.groups) return v.groups.map(l => `<span class="vl">${nobreak(l.map(item).join(''))}</span>`).join('');
    return (v.lines_corrected || v.lines).map(l => `<span class="vl">${nobreak(esc(l))}</span>`).join('');
  }
  /* an approved correction (lines_corrected) is what is shown; the mark opens the source text */
  function corrected(v) {
    if (!v.lines_corrected) return '';
    return '<button type="button" class="sarga-note corr-mark" aria-expanded="false">संशोधितम्</button>' +
      `<span class="sarga-note corr-orig" hidden>विकिस्रोतसि पाठः —<br>${v.lines.map(l => nobreak(esc(l))).join('<br>')}</span>`;
  }
  function badges(v) {
    let h = '';
    if (v.speaker) h += `<span class="uvaca">${esc(v.speaker)}</span>`;
    if (v.metre && v.metre.name && v.metre.name !== ANUSHTUP) h += `<span class="metre-badge">${esc(v.metre.name)}</span>`;
    return h;
  }
  const num = v => v.id.split('.').pop();
  /* a machine split (padaccheda_status "seed") is marked until a sarga review has finalised it */
  const SEED_MARK = '<span class="sarga-note pada-seed" title="यन्त्रकृतः पदच्छेदः — अद्यापि न समीक्षितः">असमीक्षितम्</span>';
  function verse(v) {
    const pending = v.groups ? '' : '<span class="sarga-note pada-pending">पदच्छेदः सज्जीक्रियते</span>';
    const seed = v.groups && v.padaccheda_status !== 'reviewed' ? SEED_MARK : '';
    return `<div class="mula-box" id="${esc(v.id)}">${badges(v)}${vlines(v)}${pending}${seed}${corrected(v)}` +
      `<a class="verse-ref" href="#${esc(v.id)}">${deva(num(v))}</a></div>${study(v)}`;
  }

  /* ---------- per-verse अध्ययनसाहाय्यम् (rendered when opened) ---------- */
  const TABS = [['padartha', 'पदार्थः'], ['anvaya', 'अन्वयः'], ['vyakhya', 'सरलव्याख्या']];
  const has = v => ({ padartha: v.padartha && v.padartha.length, anvaya: !!v.anvaya, vyakhya: !!v.vyakhya_sa });
  function study(v) {
    const h = has(v);
    if (!TABS.some(([t]) => h[t])) return '';
    return `<details class="vy-block st-block" data-verse="${esc(v.id)}"><summary>अध्ययनसाहाय्यम्</summary></details>`;
  }
  const bold = s => esc(s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>');
  function studyBody(v, tab) {
    if (tab === 'padartha') return v.padartha.map(p => `<p class="pd-row"><b>${esc(p.pada)}</b>${esc(p.artha || '')}` +
      `${p.vigraha ? ` <span class="muted">(${esc(p.vigraha)})</span>` : ''}</p>`).join('');
    if (tab === 'anvaya') return `<p>${esc(v.anvaya)}</p>`;
    return `<p>${bold(v.vyakhya_sa)}</p>`;
  }
  function openStudy(d) {
    const v = state.sarga.byId[d.dataset.verse], h = has(v);
    const tabs = TABS.filter(([t]) => h[t]);
    const cur = d.dataset.tab || tabs[0][0];
    d.dataset.tab = cur;
    d.innerHTML = `<summary>अध्ययनसाहाय्यम्</summary><div class="chip-row study-tabs">` +
      tabs.map(([t, label]) => `<button data-tab="${t}" aria-pressed="${t === cur}">${label}</button>`).join('') +
      `</div><div class="sec">${studyBody(v, cur)}</div>`;
    d.open = true;
    transliterate(d);
  }

  /* ---------- views ---------- */
  function home() {
    const rows = index.kandas.map(x => `<li><a class="part" href="#VR.${x.k}"><span class="num">${deva(x.k)}</span>` +
      `<span class="name">${esc(x.name)}</span><span class="note">${deva(x.sargas)} सर्गाः · ${deva(x.verses)} श्लोकाः →</span></a></li>`).join('');
    return `<h1 class="chapter-heading">श्रीमद्वाल्मीकिरामायणम्</h1>` +
      `<p class="chapter-sub">कथया संस्कृतम् — मूलश्लोकाः, पदच्छेदः, पदार्थः, अन्वयः, सरलसंस्कृतव्याख्या च।</p>` +
      `<section class="text"><div class="text-head"><h2>काण्डानि</h2><p>सप्त काण्डानि · ${deva(index.sargas.length)} सर्गाः</p></div><ul class="parts">${rows}</ul></section>`;
  }
  /* Stage C: a sarga with generated layers carries a standing note; a finished one a mark on the index */
  const generated = st => !!st && ['padartha', 'anvaya', 'vyakhya'].some(l => st[l] && st[l] !== 'pending');
  const complete = st => !!st && st.padaccheda === 'reviewed' && ['padartha', 'anvaya', 'vyakhya'].every(l => st[l] === 'draft' || st[l] === 'done');
  function kandaView(k) {
    const kd = kanda(k);
    const rows = index.sargas.filter(x => x.k === k).map(x => `<li><a class="part" href="#${x.id}"><span class="num">${deva(x.s)}</span>` +
      `<span class="name">${esc(x.title || x.incipit + '…')}</span><span class="note">${deva(x.verses)} श्लोकाः${complete(x.status) ? ' · ✓ सम्पूर्णः' : ''} →</span></a></li>`).join('');
    const note = k === 7 ? '<p class="sarga-note">उत्तरकाण्डम् — सप्तमं काण्डम्; युद्धकाण्डात् परं रामस्य उत्तरकथा।</p>' : '';
    return `<h1 class="chapter-heading">${esc(kd.name)}</h1><p class="chapter-sub">${deva(kd.sargas)} सर्गाः · ${deva(kd.verses)} श्लोकाः</p>${note}` +
      `<section class="text"><ul class="parts">${rows}</ul></section>`;
  }
  function sargaView(d) {
    let h = `<h1 class="chapter-heading">${esc(d.kanda_name)} · सर्गः ${deva(d.sarga)}</h1>`;
    h += `<p class="chapter-sub">${d.title ? esc(d.title) + ' · ' : ''}${deva(d.verse_count)} श्लोकाः</p>`;
    if (d.flags.includes('source_presplit')) h += '<p class="sarga-note">अस्य सर्गस्य मूलपाठः स्रोतसि अंशतः पदच्छेदरूपेण दत्तः; शोधनं पश्चात् भविष्यति।</p>';
    if (generated(d.status)) h += '<p class="sarga-note">अस्य सर्गस्य पदच्छेदः, पदार्थः, अन्वयः, सरलव्याख्या च यन्त्रेण लिखिताः; विदुषां समीक्षा अद्यापि अपेक्षिता।</p>';
    h += d.verses.map(verse).join('');
    if (d.colophon) h += `<p class="colophon">${esc(d.colophon)}</p>`;
    if (d.appendix) {
      h += `<p class="appendix-head">${esc(d.appendix.heading)}</p>` + d.appendix.verses.map(verse).join('');
      if (d.appendix.colophon) h += `<p class="colophon">${esc(d.appendix.colophon)}</p>`;
    }
    return h + pager(d.kanda, d.sarga);
  }
  function pager(k, s) {
    const i = index.sargas.findIndex(x => x.k === k && x.s === s), prev = index.sargas[i - 1], next = index.sargas[i + 1];
    const label = x => `${kanda(x.k).name.replace('काण्डम्', '')} ${deva(x.s)}`;
    return `<nav class="unit-pager">${prev ? `<a href="#${prev.id}">← ${esc(label(prev))}</a>` : '<span></span>'}` +
      `<a href="#VR.${k}">${esc(kanda(k).name)}</a>${next ? `<a href="#${next.id}">${esc(label(next))} →</a>` : '<span></span>'}</nav>`;
  }

  /* ---------- sidebar ---------- */
  function sidebar(r) {
    const k = r.k || 1;
    $('#kanda-pick').innerHTML = index.kandas.map(x => `<option value="${x.k}"${x.k === k ? ' selected' : ''}>${esc(x.name)}</option>`).join('');
    $('#unit-list').innerHTML = `<div class="lesson-list">` + index.sargas.filter(x => x.k === k).map(x =>
      `<a class="lesson-link${r.view === 'sarga' && x.s === r.s ? ' active' : ''}" href="#${x.id}" title="सर्गः ${deva(x.s)}">${deva(x.s)}</a>`).join('') + '</div>';
    $('#verse-list').innerHTML = r.view === 'sarga' && state.sarga
      ? `<p class="side-title">श्लोकाः</p><div class="verse-nav">${state.sarga.data.verses.map(v => `<a href="#${esc(v.id)}">${deva(num(v))}</a>`).join('')}</div>` : '';
    transliterate($('#sidebar'));
  }

  /* ---------- render ---------- */
  async function render(r) {
    const status = $('#status'), content = $('#content');
    status.hidden = false;
    let html, title;
    if (r.view === 'sarga') {
      let d;
      try { d = await load(sargaFile(r.k, r.s)); } catch { status.innerHTML = '<p>पाठः न लब्धः। पुनः प्रयतताम्।</p>'; return; }
      const all = d.verses.concat(d.appendix ? d.appendix.verses : []);
      state.sarga = { data: d, byId: Object.fromEntries(all.map(v => [v.id, v])) };
      $('#pada-toggle').hidden = !all.some(v => v.groups);   // nothing to toggle in a sarga without any split
      html = sargaView(d); title = `${d.kanda_name} · सर्गः ${deva(d.sarga)}`;
      store.set('last', `VR.${r.k}.${r.s}`);
    } else {
      state.sarga = null;
      $('#pada-toggle').hidden = false;
      html = r.view === 'kanda' ? kandaView(r.k) : home();
      title = r.view === 'kanda' ? kanda(r.k).name : '';
    }
    content.innerHTML = html;
    transliterate(content);
    status.hidden = true;
    document.title = title ? `${title} — श्रीमद्वाल्मीकिरामायणम्` : 'श्रीमद्वाल्मीकिरामायणम्';
    sidebar(r);
  }
  function route() {
    const r = parseHash();
    closeMenu();
    const same = state.route && r.view === 'sarga' && state.route.view === 'sarga' && r.k === state.route.k && r.s === state.route.s;
    state.route = r;
    (same ? Promise.resolve() : render(r)).then(() => {
      const el = r.verse && document.getElementById(r.verse);
      if (el) { el.scrollIntoView({ block: 'start', behavior: same ? 'smooth' : 'instant' }); el.classList.add('flash'); setTimeout(() => el.classList.remove('flash'), 1600); }
      else if (!same) window.scrollTo({ top: 0, behavior: 'instant' });
    });
  }

  /* ---------- controls ---------- */
  function bindControls() {
    const pada = $('#pada-toggle');
    const applyPada = () => { document.body.classList.toggle('pada', state.pada); pada.setAttribute('aria-pressed', state.pada); };
    pada.addEventListener('click', () => { state.pada = !state.pada; store.set('pada', state.pada); applyPada(); });
    applyPada();
    const applySize = () => document.documentElement.style.setProperty('--font-size', state.size + 'px');
    $('#size-down').addEventListener('click', () => { state.size = Math.max(15, state.size - 1); store.set('size', state.size); applySize(); });
    $('#size-up').addEventListener('click', () => { state.size = Math.min(30, state.size + 1); store.set('size', state.size); applySize(); });
    applySize();
    const script = $('#script'); script.value = state.script;
    script.addEventListener('change', () => { state.script = script.value; store.set('script', state.script); render(state.route); });
    $('#kanda-pick').addEventListener('change', e => { location.hash = `VR.${e.target.value}`; });
    $('#menu').addEventListener('click', () => { const open = !$('#sidebar').classList.contains('open'); $('#sidebar').classList.toggle('open', open); $('#menu').setAttribute('aria-expanded', open); });
    $('#content').addEventListener('toggle', e => { const d = e.target; if (d.matches('details.st-block') && d.open && !d.querySelector('.sec')) openStudy(d); }, true);
    $('#content').addEventListener('click', e => {
      const m = e.target.closest('.corr-mark');
      if (m) { const o = m.nextElementSibling; o.hidden = !o.hidden; m.setAttribute('aria-expanded', String(!o.hidden)); return; }
      const b = e.target.closest('.study-tabs button'); if (!b) return;
      const d = b.closest('details'); d.dataset.tab = b.dataset.tab; openStudy(d);
    });
    window.addEventListener('hashchange', route);
  }
  function closeMenu() { $('#sidebar').classList.remove('open'); $('#menu').setAttribute('aria-expanded', 'false'); }

  /* display-only transliteration: the data stays in Devanagari */
  function transliterate(root) {
    document.body.dataset.script = state.script;
    if (state.script === 'devanagari' || !window.Sanscript) return;
    const walk = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    while (walk.nextNode()) {
      const n = walk.currentNode;
      if (n.parentElement.closest('[data-no-transliterate],select')) continue;
      if (/[ऀ-ॿ]/.test(n.nodeValue)) n.nodeValue = Sanscript.t(n.nodeValue, 'devanagari', state.script);
    }
  }

  document.addEventListener('DOMContentLoaded', async () => {
    try { index = await load('vr/index.json'); } catch { $('#status').innerHTML = '<p>अनुक्रमणिका न लब्धा।</p>'; return; }
    bindControls(); route();
  });
})();
