let SFXT = null;

function sfxTarget() {
  const a = ac();
  if (!a) return null;
  if (!SFXT || SFXT.a !== a) SFXT = { a, out: BUS.fx, rev: null, nb: null };
  return SFXT;
}

function sfxRev(t) {
  if (t.rev) return t.rev;
  const a = t.a;
  const len = Math.floor(a.sampleRate * 2.4);
  const buf = a.createBuffer(2, len, a.sampleRate);
  for (let c = 0; c < 2; c++) {
    const d = buf.getChannelData(c);
    for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / len, 3.2);
  }
  const cv = a.createConvolver();
  cv.buffer = buf;
  const lp = a.createBiquadFilter();
  lp.type = 'lowpass';
  lp.frequency.value = 4200;
  cv.connect(lp).connect(t.out);
  t.rev = cv;
  return cv;
}

function sfxNoiseBuf(t) {
  if (t.nb) return t.nb;
  const a = t.a;
  const len = Math.floor(a.sampleRate * 3);
  const buf = a.createBuffer(1, len, a.sampleRate);
  const d = buf.getChannelData(0);
  for (let i = 0; i < len; i++) d[i] = Math.random() * 2 - 1;
  t.nb = buf;
  return buf;
}

function sfxOut(t, g, wet) {
  g.connect(t.out);
  if (wet) {
    const s = t.a.createGain();
    s.gain.value = wet;
    g.connect(s).connect(sfxRev(t));
  }
}

function tone(f, f2, dur, type, vol, delay, wet, lpf) {
  const t = sfxTarget();
  if (!t) return;
  const a = t.a;
  const t0 = a.currentTime + (delay || 0);
  const o = a.createOscillator();
  const g = a.createGain();
  o.type = type || 'sine';
  o.frequency.setValueAtTime(f, t0);
  if (f2) o.frequency.exponentialRampToValueAtTime(f2, t0 + dur);
  g.gain.setValueAtTime(0.0001, t0);
  g.gain.exponentialRampToValueAtTime(vol, t0 + Math.min(0.012, dur * 0.2));
  g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
  if (lpf) {
    const fl = a.createBiquadFilter();
    fl.type = 'lowpass';
    fl.frequency.value = lpf;
    o.connect(fl).connect(g);
  } else o.connect(g);
  sfxOut(t, g, wet);
  o.start(t0);
  o.stop(t0 + dur + 0.05);
}

function noise(dur, vol, f0, f1, delay, q, wet, type, att) {
  const t = sfxTarget();
  if (!t) return;
  const a = t.a;
  const t0 = a.currentTime + (delay || 0);
  const s = a.createBufferSource();
  s.buffer = sfxNoiseBuf(t);
  s.loop = true;
  const bp = a.createBiquadFilter();
  bp.type = type || 'bandpass';
  bp.Q.value = q || 1.2;
  bp.frequency.setValueAtTime(f0, t0);
  bp.frequency.exponentialRampToValueAtTime(f1, t0 + dur);
  const g = a.createGain();
  g.gain.setValueAtTime(0.0001, t0);
  g.gain.exponentialRampToValueAtTime(vol, t0 + dur * (att || 0.2));
  g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
  s.connect(bp).connect(g);
  sfxOut(t, g, wet);
  s.start(t0, Math.random() * 2);
  s.stop(t0 + dur + 0.05);
}

function bell(f, dur, vol, delay, wet) {
  [[1, 1], [2.76, 0.42], [5.4, 0.2], [8.93, 0.08]].forEach(([r, v], i) => tone(f * r, f * r * 0.998, dur / (1 + i * 0.7), 'sine', vol * v, delay, wet));
}

function clunk(vol, delay, wet) {
  tone(78, 36, 0.34, 'sine', vol, delay, wet);
  tone(190, 90, 0.12, 'triangle', vol * 0.5, delay);
  [[310, 0.16], [523, 0.1], [847, 0.06], [1330, 0.04]].forEach(([f, v]) => tone(f, f * 0.99, 0.22, 'square', vol * v * 0.5, delay, wet, 3200));
  noise(0.05, vol * 0.7, 4000, 1500, delay, 0.7, 0.05);
}

let lastLogSfx = 0;

const sfxSynth = {
  tick() { noise(0.02, 0.05, 3800, 2400, 0, 1.5); tone(2100, 1500, 0.025, 'sine', 0.03); },
  click() { noise(0.018, 0.045, 3200, 1800, 0, 1.2); tone(1250, 760, 0.04, 'triangle', 0.035); },
  chevron() {
    tone(150, 210, 0.22, 'sawtooth', 0.04, 0, 0, 900);
    clunk(0.5, 0.2, 0.22);
    tone(1760, 1760, 0.35, 'sine', 0.03, 0.26, 0.3);
  },
  fail() {
    noise(0.9, 0.26, 3000, 200, 0, 0.8, 0.2, 'bandpass', 0.05);
    tone(240, 50, 0.8, 'sawtooth', 0.09, 0, 0.2, 1400);
    tone(246, 52, 0.8, 'sawtooth', 0.07, 0.02, 0.2, 1400);
    tone(60, 30, 0.7, 'sine', 0.4, 0.05);
    clunk(0.25, 0.55, 0.3);
  },
  kawoosh() {
    noise(0.7, 0.28, 120, 900, 0, 0.9, 0.3, 'bandpass', 0.7);
    noise(1.3, 0.5, 300, 3400, 0.15, 0.55, 0.45, 'bandpass', 0.3);
    tone(55, 26, 1.8, 'sine', 0.6, 0, 0.15);
    tone(110, 880, 1.0, 'sine', 0.06, 0.25, 0.4);
    tone(112, 892, 1.0, 'sine', 0.05, 0.25, 0.4);
    noise(1.8, 0.2, 5200, 1600, 0.55, 2.5, 0.6, 'bandpass', 0.15);
    for (let i = 0; i < 9; i++) tone(900 + Math.random() * 2400, 400 + Math.random() * 600, 0.14, 'sine', 0.02, 0.7 + i * 0.13 + Math.random() * 0.08, 0.5);
  },
  shutdown() {
    noise(1.0, 0.32, 3200, 140, 0, 0.7, 0.35, 'bandpass', 0.1);
    tone(200, 38, 0.95, 'sawtooth', 0.07, 0, 0.2, 1200);
    tone(70, 28, 1.1, 'sine', 0.45, 0.05, 0.15);
    noise(0.5, 0.18, 1800, 500, 0.7, 1.5, 0.5);
  },
  iris() {
    const t = sfxTarget();
    if (!t) return;
    const a = t.a;
    const t0 = a.currentTime;
    const o = a.createOscillator();
    const g = a.createGain();
    const fl = a.createBiquadFilter();
    const lfo = a.createOscillator();
    const lg = a.createGain();
    o.type = 'sawtooth';
    o.frequency.setValueAtTime(95, t0);
    o.frequency.linearRampToValueAtTime(150, t0 + 0.7);
    fl.type = 'lowpass';
    fl.frequency.value = 800;
    lfo.frequency.value = 16;
    lg.gain.value = 0.04;
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(0.06, t0 + 0.08);
    g.gain.setValueAtTime(0.06, t0 + 0.6);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.8);
    lfo.connect(lg).connect(g.gain);
    o.connect(fl).connect(g);
    sfxOut(t, g, 0.2);
    o.start(t0); lfo.start(t0);
    o.stop(t0 + 0.9); lfo.stop(t0 + 0.9);
    noise(0.65, 0.16, 1400, 500, 0, 2, 0.15);
    clunk(0.45, 0.68, 0.3);
  },
  chime() {
    bell(880, 1.1, 0.08, 0, 0.35);
    bell(1320, 1.3, 0.06, 0.12, 0.4);
  },
  ok() { bell(1046, 0.7, 0.05, 0, 0.3); },
  warn() {
    tone(520, 520, 0.16, 'triangle', 0.08, 0, 0.2, 2200);
    tone(390, 390, 0.26, 'triangle', 0.08, 0.17, 0.25, 2200);
  },
  alert() {
    tone(880, 880, 0.12, 'square', 0.05, 0, 0.2, 2600);
    tone(660, 660, 0.12, 'square', 0.05, 0.14, 0.2, 2600);
    tone(880, 880, 0.2, 'square', 0.05, 0.28, 0.25, 2600);
  },
  pulse() {
    tone(740, 700, 0.3, 'sawtooth', 0.075, 0, 0.3, 2400);
    tone(496, 470, 0.34, 'sawtooth', 0.075, 0.4, 0.3, 2400);
    tone(70, 55, 0.28, 'sine', 0.2, 0);
    tone(70, 55, 0.28, 'sine', 0.2, 0.4);
  }
};

const SFXB = {};
let sfxLoading = false;

function sfxLoad() {
  if (sfxLoading || typeof SFX_DATA === 'undefined' || !AC) return;
  sfxLoading = true;
  Object.keys(SFX_DATA).forEach(k => {
    const s = atob(SFX_DATA[k]);
    const u = new Uint8Array(s.length);
    for (let i = 0; i < s.length; i++) u[i] = s.charCodeAt(i);
    AC.decodeAudioData(u.buffer, b => { SFXB[k] = b; }, () => {});
  });
}

function sfxPlay(k) {
  const t = sfxTarget();
  if (!t) return false;
  const b = SFXB[k];
  if (!b) return false;
  const s = t.a.createBufferSource();
  s.buffer = b;
  s.playbackRate.value = 1 + (Math.random() - 0.5) * 0.05;
  s.connect(t.out);
  s.start();
  return true;
}

const sfx = {};
Object.keys(sfxSynth).forEach(k => { sfx[k] = () => { if (!sfxPlay(k)) sfxSynth[k](); }; });

function humOn() {
  const t = sfxTarget();
  if (!t || humNodes) return;
  const a = t.a;
  const g = a.createGain();
  g.gain.setValueAtTime(0, a.currentTime);
  g.gain.linearRampToValueAtTime(0.06, a.currentTime + 1.5);
  const o1 = a.createOscillator();
  const o2 = a.createOscillator();
  const o3 = a.createOscillator();
  const lfo = a.createOscillator();
  const lg = a.createGain();
  const lp = a.createBiquadFilter();
  const trem = a.createOscillator();
  const tg = a.createGain();
  const mix = a.createGain();
  o1.type = 'sine'; o1.frequency.value = 60;
  o2.type = 'triangle'; o2.frequency.value = 120;
  o3.type = 'sawtooth'; o3.frequency.value = 180;
  lp.type = 'lowpass'; lp.frequency.value = 420;
  lfo.frequency.value = 0.35; lg.gain.value = 4;
  trem.frequency.value = 0.18; tg.gain.value = 0.25;
  mix.gain.value = 0.75;
  lfo.connect(lg).connect(o2.frequency);
  trem.connect(tg).connect(mix.gain);
  o3.connect(lp);
  o1.connect(mix); o2.connect(mix); lp.connect(mix);
  mix.connect(g);
  sfxOut(t, g, 0.18);
  const s = a.createBufferSource();
  s.buffer = sfxNoiseBuf(t);
  s.loop = true;
  const nf = a.createBiquadFilter();
  nf.type = 'lowpass'; nf.frequency.value = 260;
  const ng = a.createGain();
  ng.gain.value = 0.35;
  s.connect(nf).connect(ng).connect(g);
  o1.start(); o2.start(); o3.start(); lfo.start(); trem.start(); s.start();
  humNodes = { a, g, list: [o1, o2, o3, lfo, trem, s] };
}

