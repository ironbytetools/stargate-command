import sys
src, dst = sys.argv[1:3]
s = open(src, encoding='utf-8').read()
assert s.count('0.9.4') == 4, s.count('0.9.4')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('<title>Stargate Command 0.9.4</title>', '<title>Stargate Command 0.9.5 OS TEST</title>')
rep('BUILD 0.9.4', 'BUILD 0.9.5 // BASE COMPUTER TEST', 2)
rep("const BUILD_VER = '0.9.4';", "const BUILD_VER = '0.9.5';")
rep("const SAVE_KEY = 'sgc-command-save-';", "const SAVE_KEY = 'sgc-os-test-save-';")
rep("const SETTINGS_KEY = 'sgc-command-settings';", "const SETTINGS_KEY = 'sgc-os-test-settings';")

rep("function fitStarmap() {\n  const sm = $('starmap');", "function fitStarmap() {\n  if (window.osLayout) { osLayout(); return; }\n  const sm = $('starmap');")
rep("  if (gate && m) FIT.lock = m.offsetWidth;\n  if (gate && dw) dw.style.maxWidth = dw.offsetWidth + 'px';\n", "")

CSS = r"""
<style id="oscss">
#oswrap { display: none; }
body.gv .panel.wide { display: none !important; }
body.gv #oswrap { display: flex; flex-direction: column; gap: 6px; grid-column: 1 / -1; grid-row: 1 / span 2; height: 960px; padding: 8px; }
#osdesk { position: relative; flex: 1 1 auto; min-height: 0; background: radial-gradient(ellipse at 50% 40%, #0a1d2e, #040b13 70%); border: 1px solid #1d3a52; border-radius: 6px; }
body.gv #osdesk > .win { position: absolute; display: flex; flex-direction: column; grid-column: auto; grid-row: auto; min-height: 0; margin: 0; padding: 0; overflow: hidden; background: #030a12; border: 1px solid #2a7f9a; border-radius: 6px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5); }
.win > .wt { flex: 0 0 26px; display: flex; align-items: center; gap: 10px; padding: 0 6px 0 10px; background: linear-gradient(#10304a, #0a1c2c); border-bottom: 1px solid #1d4660; color: #7ffbff; font: 600 11px monospace; letter-spacing: 0.22em; user-select: none; }
.win > .wt .wts { flex: 1 1 auto; color: #4f7a92; letter-spacing: 0.08em; font-weight: 400; overflow: hidden; white-space: nowrap; }
.win > .wt .wts .sub { margin: 0; font-size: 10px; }
.win > .wt .wtb { display: flex; gap: 4px; }
#osdesk .wt .wtb button { min-height: 18px; height: 18px; min-width: 26px; padding: 0 6px; font-size: 11px; letter-spacing: 0; line-height: 1; }
.win > .wbd { flex: 1 1 auto; min-height: 0; overflow: auto; padding: 4px; position: relative; display: flex; flex-direction: column; }
#dcpanel > .wbd { overflow: hidden; align-items: center; }
body.gv #osdesk #dcwrap { flex: 0 0 auto; margin: 0 auto; max-width: none; }
body.gv #osdesk #ctrlpanel { width: 100%; max-width: 665px; margin: 6px auto 0; }
#starmap > .wbd { padding: 0; background: #02060c; align-items: center; justify-content: center; }
body.gv #osdesk #smwrap { flex: 0 1 auto; width: 100%; min-height: 0; display: flex; flex-direction: column; position: relative; }
body.gv #osdesk #smbox { margin: 0 auto; width: 100%; }
body.gv #osdesk #smpanel { position: static; flex: 1 1 auto; height: auto; margin: 0; border: 0; background: transparent; overflow: auto; padding: 8px 10px; }
#osread .smtop { flex-direction: column; align-items: flex-start; gap: 8px; flex-wrap: wrap; }
body.gv #osread #smpanel .smtop { flex-wrap: wrap; }
#osread .smtop .glyphrow { margin: 0; display: flex; flex-wrap: wrap; gap: 2px; }
#osread .smtop > button { align-self: stretch; }
#osread .intelgrid { grid-template-columns: 1fr; }
#missionpanel > .wbd { padding: 6px 10px; }
#oslog > .wbd .log { height: auto; flex: 1 1 auto; min-height: 0; }
#oslog > .wbd .ltabs { margin: 0 0 6px; }
#ostask { flex: 0 0 38px; display: flex; align-items: center; gap: 6px; padding: 3px 8px; background: linear-gradient(#0c2335, #07131f); border: 1px solid #2a7f9a; border-radius: 6px; }
#ostask .tbstart { color: #7ffbff; font: 700 12px monospace; letter-spacing: 0.2em; padding-right: 14px; border-right: 1px solid #1d4660; margin-right: 4px; }
#ostask button.tbapp { height: 28px; min-height: 28px; padding: 0 14px; font-size: 11px; letter-spacing: 0.12em; opacity: 0.55; }
#ostask button.tbapp.on { opacity: 1; border-color: var(--accent); background: rgba(var(--accent-rgb), 0.14); }
#ostray { margin-left: auto; display: flex; gap: 16px; align-items: center; font-size: 11px; letter-spacing: 0.08em; color: #9fb4c8; }
#ostray b { color: #8ff; font-weight: 600; }
#ostray .osal.ok { color: var(--ok); }
#ostray .osal.danger { color: var(--danger); animation: blink 1s infinite; }
#osboot { position: fixed; inset: 0; z-index: 300; background: #02060c; display: flex; align-items: center; justify-content: center; transition: opacity 0.6s; cursor: pointer; }
#osboot.out { opacity: 0; pointer-events: none; }
#osboot .osb { width: min(560px, 90vw); font: 13px/1.7 monospace; color: #7ffbff; }
#osboot .osl { font-size: 22px; letter-spacing: 0.3em; margin-bottom: 4px; }
#osboot .oss { color: #4f7a92; letter-spacing: 0.14em; margin-bottom: 18px; font-size: 11px; }
#osboot .osm div { color: #9fb4c8; } #osboot .osm div b { color: #7dffb0; font-weight: 600; }
#osboot .osk { margin-top: 14px; color: #4f7a92; font-size: 10px; letter-spacing: 0.14em; }
</style>
"""

JS = r"""
<script id="osmod">
const OS = { built: false, booted: false, st: { dial: 'n', map: 'n', read: 'n', mission: 'n', log: 'n' }, z: 10, sig: '' };
const OS_APPS = [
  { k: 'dial', id: 'dcpanel', name: 'DIALER' },
  { k: 'map', id: 'starmap', name: 'STARMAP' },
  { k: 'read', id: 'osread', name: 'WORLD INTEL' },
  { k: 'mission', id: 'missionpanel', name: 'MISSION PLANNER' },
  { k: 'log', id: 'oslog', name: 'BASE LOG' }
];

function osBar(a) {
  const d = document.createElement('div');
  d.className = 'wt';
  d.innerHTML = `<span class="wtn">${a.name}</span><span class="wts"></span><span class="wtb"><button onclick="osMin('${a.k}')" title="Minimize">_</button><button onclick="osMax('${a.k}')" title="Maximize">&#9633;</button></span>`;
  return d;
}

function osBuild() {
  if (OS.built) return;
  OS.built = true;
  OS.logPanel = document.querySelector('.panel.wide');
  const wrap = document.createElement('div');
  wrap.id = 'oswrap';
  wrap.className = 'panel';
  wrap.innerHTML = '<div id="osdesk"></div><div id="ostask"></div>';
  $('view-gate').appendChild(wrap);
  const desk = $('osdesk');
  const rd = document.createElement('div');
  rd.id = 'osread';
  rd.className = 'win';
  rd.innerHTML = '<div class="wbd"></div>';
  rd.querySelector('.wbd').appendChild($('smpanel'));
  const lg = document.createElement('div');
  lg.id = 'oslog';
  lg.className = 'win';
  lg.innerHTML = '<div class="wbd"></div>';
  const lvl = $('smlevel');
  $('starmap').querySelector('.smhead').remove();
  $('dcpanel').querySelector('h2').remove();
  $('missionpanel').querySelector('h2').remove();
  OS_APPS.forEach(a => {
    const el = $(a.id) || (a.k === 'read' ? rd : lg);
    el.classList.add('win');
    const kids = Array.from(el.children).filter(c => !c.classList.contains('wbd'));
    const bar = osBar(a);
    if (el.querySelector(':scope > .wbd')) el.insertBefore(bar, el.firstChild);
    else {
      const bd = document.createElement('div');
      bd.className = 'wbd';
      kids.forEach(c => bd.appendChild(c));
      el.appendChild(bar);
      el.appendChild(bd);
    }
    desk.appendChild(el);
    el.addEventListener('mousedown', () => { el.style.zIndex = ++OS.z; });
  });
  $('starmap').querySelector('.wts').appendChild(lvl);
  $('osread').querySelector('.wts').textContent = 'SELECTED WORLD';
  const tk = $('ostask');
  tk.innerHTML = '<span class="tbstart">SGC</span>' + OS_APPS.map(a => `<button class="tbapp on" data-k="${a.k}" onclick="osTask('${a.k}')">${a.name}</button>`).join('') + '<span id="ostray"><span class="osal ok" id="osal">ALL CLEAR</span><span>POWER <b id="ospw"></b></span><span>SUPPLIES <b id="ossp"></b></span><span id="osck"></span></span>';
  osPlace(false);
}

function osPlace(g) {
  if (!OS.built) return;
  const tgt = g ? $('oslog').querySelector('.wbd') : OS.logPanel;
  [$('lt-log').parentElement, $('log'), $('briefs')].forEach(p => { if (p.parentElement !== tgt) tgt.appendChild(p); });
}

function osRaise(k) {
  const a = OS_APPS.find(q => q.k === k);
  if (a) $(a.id).style.zIndex = ++OS.z;
}

function osMin(k) {
  OS.st[k] = 'm';
  osLayout();
}

function osMax(k) {
  OS.st[k] = OS.st[k] === 'x' ? 'n' : 'x';
  osRaise(k);
  osLayout();
}

function osTask(k) {
  OS.st[k] = OS.st[k] === 'm' ? 'n' : 'm';
  if (OS.st[k] !== 'm') osRaise(k);
  osLayout();
}

function osLayout() {
  if (!OS.built || !document.body.classList.contains('gv')) return;
  const desk = $('osdesk');
  const W = desk.clientWidth;
  const H = desk.clientHeight;
  if (!W || !H) return;
  const g = 8;
  const tb = 26;
  const ctrl = $('ctrlpanel').offsetHeight + 8;
  const a = Math.min(Math.floor(W * 0.37), 700);
  const b = Math.min(Math.floor(W * 0.46), 800);
  const c = W - a - b - 2 * g;
  const h1 = Math.min(Math.floor(H * 0.72), Math.round((a - 10) * 0.7) + ctrl + tb + 10);
  const hr = Math.floor(h1 * 0.62);
  const R = {
    dial: [0, 0, a, h1],
    map: [a + g, 0, b, h1],
    read: [a + b + 2 * g, 0, c, hr],
    log: [a + b + 2 * g, hr + g, c, H - hr - g],
    mission: [0, h1 + g, a + b + g, H - h1 - g]
  };
  OS_APPS.forEach(ap => {
    const el = $(ap.id);
    const st = OS.st[ap.k];
    const r = st === 'x' ? [0, 0, W, H] : R[ap.k];
    el.style.display = st === 'm' ? 'none' : '';
    el.style.left = r[0] + 'px';
    el.style.top = r[1] + 'px';
    el.style.width = r[2] + 'px';
    el.style.height = r[3] + 'px';
    el.dataset.w = r[2];
    el.dataset.h = r[3];
    const btn = document.querySelector(`.tbapp[data-k="${ap.k}"]`);
    if (btn) btn.classList.toggle('on', st !== 'm');
  });
  const fit = (el, wrapEl, extra, minus) => {
    if (!el || !wrapEl || el.style.display === 'none') return;
    const bw = +el.dataset.w - 10;
    const bh = +el.dataset.h - tb - 10 - extra;
    wrapEl.style.width = Math.max(120, Math.min(bw, Math.floor(bh * 800 / 560))) + 'px';
  };
  fit($('dcpanel'), $('dcwrap'), $('ctrlpanel').offsetHeight + 8);
  const sm = $('starmap');
  if (sm.style.display !== 'none') {
    const bw = +sm.dataset.w - 2;
    const bh = +sm.dataset.h - tb - 2;
    $('smbox').style.maxWidth = Math.max(120, Math.min(bw, Math.floor(bh * 800 / 560))) + 'px';
  }
}

function osTray() {
  if (!OS.built || !state.started) return;
  const al = state.incoming ? ['INCOMING WORMHOLE', 'danger'] : (Object.keys(state.dipl.alerts).length ? ['RAID ALERT ' + Object.keys(state.dipl.alerts).length, 'danger'] : ['ALL CLEAR', 'ok']);
  const sig = al[0] + '|' + state.res.power + '|' + state.res.supplies + '|' + clock();
  if (sig === OS.sig) return;
  OS.sig = sig;
  const e = $('osal');
  e.textContent = al[0];
  e.className = 'osal ' + al[1];
  $('ospw').textContent = state.res.power;
  $('ossp').textContent = state.res.supplies;
  $('osck').textContent = 'SGC ' + clock();
}

function osBoot() {
  if (OS.booted) return;
  OS.booted = true;
  const o = document.createElement('div');
  o.id = 'osboot';
  o.innerHTML = '<div class="osb"><div class="osl">STARGATE COMMAND</div><div class="oss">CHEYENNE MOUNTAIN COMPLEX // BASE COMPUTER</div><div class="osm"></div><div class="osk">CLICK TO SKIP</div></div>';
  document.body.appendChild(o);
  const lines = ['GATE SERVICES', 'DIALING COMPUTER', 'STARMAP DATABASE', 'MISSION PLANNER', 'BASE LOG'];
  const m = o.querySelector('.osm');
  let i = 0;
  const done = () => { clearInterval(t); o.classList.add('out'); setTimeout(() => o.remove(), 700); };
  const t = setInterval(() => {
    if (i < lines.length) { m.insertAdjacentHTML('beforeend', `<div>${lines[i]} ... <b>ONLINE</b></div>`); i++; }
    else {
      m.insertAdjacentHTML('beforeend', '<div>USER GATE TECH ... <b>SESSION OPEN</b></div>');
      clearInterval(t);
      setTimeout(done, 700);
    }
  }, 320);
  o.addEventListener('click', done);
}

const _osShow = showView;
showView = function (name) {
  osBuild();
  osPlace(name === 'gate');
  const r = _osShow.apply(this, arguments);
  if (name === 'gate') { osLayout(); osBoot(); }
  return r;
};

const _osHud = renderHud;
renderHud = function () {
  const r = _osHud.apply(this, arguments);
  osTray();
  return r;
};

window.addEventListener('resize', osLayout);
osBuild();
</script>
"""

rep("</script>\n</body>", "</script>\n" + CSS + JS + "</body>")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
