import sys
src, dst = sys.argv[1], sys.argv[2]
h = open(src, encoding='utf-8').read()

def rep(old, new, count=1):
    global h
    assert h.count(old) == count, (old[:60], h.count(old))
    h = h.replace(old, new)

a = h.index('let AC = null;')
b = h.index('function toggleMute()')
seg = h[a:b]
assert seg.count('a.destination') == 3
seg = seg.replace('a.destination', 'BUS.fx')
old_ac = seg[seg.index('function ac() {'):seg.index('function tone(')]
new_ac = '''let BUS = null;

function ctx() {
  if (!AC) {
    const C = window.AudioContext || window.webkitAudioContext;
    if (!C) return null;
    AC = new C();
    BUS = { master: AC.createGain(), music: AC.createGain(), fx: AC.createGain() };
    BUS.music.connect(BUS.master);
    BUS.fx.connect(BUS.master);
    BUS.master.connect(AC.destination);
    applyVol();
  }
  if (AC.state === 'suspended') AC.resume();
  return AC;
}

function ac() {
  if (muted) return null;
  return ctx();
}

function applyVol() {
  if (!BUS) return;
  BUS.master.gain.value = muted ? 0 : settings.vm;
  BUS.music.gain.value = settings.vmu;
  BUS.fx.gain.value = settings.vf;
}

const MUSIC = { title: ['title'], calm: ['emanc', 'hathor'], tense: ['enemy'], win: ['credits'] };
const mus = { on: false, mode: null, cur: null, el: {}, url: {}, idx: {}, since: 0, win: 0 };

function musUrl(k) {
  if (!mus.url[k]) {
    const s = atob(AUDIO_DATA[k]);
    const u = new Uint8Array(s.length);
    for (let i = 0; i < s.length; i++) u[i] = s.charCodeAt(i);
    mus.url[k] = URL.createObjectURL(new Blob([u], { type: 'audio/mpeg' }));
  }
  return mus.url[k];
}

function musEl(k) {
  if (!mus.el[k]) {
    const a = ctx();
    if (!a) return null;
    const el = new Audio(musUrl(k));
    el.preload = 'auto';
    const g = a.createGain();
    g.gain.value = 0;
    a.createMediaElementSource(el).connect(g);
    g.connect(BUS.music);
    el.addEventListener('ended', () => musEnded(k));
    mus.el[k] = { el, g };
  }
  return mus.el[k];
}

function musFade(t, to, sec) {
  const a = AC;
  const g = t.g.gain;
  g.cancelScheduledValues(a.currentTime);
  g.setValueAtTime(g.value, a.currentTime);
  g.linearRampToValueAtTime(to, a.currentTime + sec);
}

function musPlay(k) {
  const t = musEl(k);
  if (!t) return;
  const prev = mus.cur;
  if (prev && prev !== k && mus.el[prev]) {
    const p = mus.el[prev];
    musFade(p, 0, 2.5);
    setTimeout(() => { if (mus.cur !== prev) p.el.pause(); }, 2800);
  }
  mus.cur = k;
  if (prev !== k) { t.el.currentTime = 0; musFade(t, 1, 2.5); }
  else { t.el.currentTime = 0; t.g.gain.cancelScheduledValues(AC.currentTime); t.g.gain.value = 1; }
  t.el.play().catch(() => {});
}

function musWant() {
  if (!state.started) return 'title';
  if (mus.win > Date.now()) return 'win';
  if (state.incoming || overdueTeams().length) return 'tense';
  return 'calm';
}

function musPick(mode) {
  const l = MUSIC[mode];
  const i = (mus.idx[mode] || 0) % l.length;
  mus.idx[mode] = i + 1;
  return l[i];
}

function musEnded(k) {
  if (mus.cur !== k) return;
  if (mus.mode === 'win') { mus.win = 0; mus.mode = null; return; }
  musPlay(musPick(mus.mode));
}

function musTick() {
  if (!mus.on || typeof AUDIO_DATA === 'undefined' || document.hidden) return;
  const want = musWant();
  const now = Date.now();
  if (want !== mus.mode) {
    if (mus.mode !== 'tense' || want === 'win' || now - mus.since > 20000) {
      mus.mode = want;
      mus.since = now;
      musPlay(musPick(want));
    }
  } else if (mus.cur && mus.el[mus.cur] && mus.el[mus.cur].el.paused) {
    mus.el[mus.cur].el.play().catch(() => {});
  }
}

function musWin() { mus.win = Date.now() + 58000; }

function musUnlock() {
  if (mus.on) return;
  mus.on = true;
  ctx();
  musTick();
}

['pointerdown', 'keydown'].forEach(ev => document.addEventListener(ev, musUnlock));
setInterval(musTick, 1000);
document.addEventListener('visibilitychange', () => {
  if (!mus.cur || !mus.el[mus.cur]) return;
  if (document.hidden) mus.el[mus.cur].el.pause();
  else mus.el[mus.cur].el.play().catch(() => {});
});

function setVol(key, v) {
  settings[key] = v / 100;
  saveSettings();
  applyVol();
  const e = $('v-' + key);
  if (e) e.textContent = v;
  if (key === 'vf') sfx.chime();
}

'''
seg = seg.replace(old_ac, new_ac)
h = h[:a] + seg + h[b:]

rep("function toggleMute() {\n  muted = !muted;", "function toggleMute() {\n  muted = !muted;\n  applyVol();")
rep("      sfx.chime();\n      log('Tau Ceti secured.", "      sfx.chime();\n      musWin();\n      log('Tau Ceti secured.")
rep("  sfx.chime();\n  log(`Level ${L} cleared.", "  sfx.chime();\n  musWin();\n  log(`Level ${L} cleared.")
rep("let settings = { accent: 'cyan', text: 'm' };", "let settings = { accent: 'cyan', text: 'm', vm: 0.8, vmu: 0.5, vf: 0.8 };")
rep("    if (d && TEXT_SIZES.some(t => t.id === d.text)) settings.text = d.text;\n",
    "    if (d && TEXT_SIZES.some(t => t.id === d.text)) settings.text = d.text;\n    ['vm', 'vmu', 'vf'].forEach(k => { if (d && typeof d[k] === 'number' && d[k] >= 0 && d[k] <= 1) settings[k] = d[k]; });\n")
rep("function resetSettings() { settings = { accent: 'cyan', text: 'm' }; saveSettings(); applySettings(); renderSettings();",
    "function resetSettings() { settings = { accent: 'cyan', text: 'm', vm: 0.8, vmu: 0.5, vf: 0.8 }; saveSettings(); applySettings(); applyVol(); renderSettings();")
rep("  const keys = SHORTCUTS.map(",
    "  const sl = (key, label) => `<div class=\"res-row\"><span>${label}</span><span style=\"display:flex;align-items:center;gap:10px;flex:1;justify-content:flex-end\"><input type=\"range\" min=\"0\" max=\"100\" value=\"${Math.round(settings[key] * 100)}\" style=\"width:60%;accent-color:var(--accent,#7ffbff)\" oninput=\"setVol('${key}',this.value)\"><b id=\"v-${key}\" style=\"min-width:28px;text-align:right\">${Math.round(settings[key] * 100)}</b></span></div>`;\n  const keys = SHORTCUTS.map(")
rep("    <h2 style=\"margin-top:16px\">Keyboard shortcuts</h2>${keys}",
    "    <h2 style=\"margin-top:16px\">Sound</h2>${sl('vm', 'Master')}${sl('vmu', 'Music')}${sl('vf', 'Effects')}\n    <h2 style=\"margin-top:16px\">Keyboard shortcuts</h2>${keys}")
rep("Stargate Command 0.7.5", "Stargate Command 0.8.0")
rep("BUILD 0.7.5", "BUILD 0.8.0", 2)
open(dst, 'w', encoding='utf-8').write(h)
