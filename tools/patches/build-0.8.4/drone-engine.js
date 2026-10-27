(function () {
const $d = id => document.getElementById('dr_' + id);

const CELL = 100;
const HAZ = {
  low: { size: 5, haze: 1, label: 'LOW' },
  med: { size: 7, haze: 0.85, label: 'MEDIUM' },
  high: { size: 9, haze: 0.7, label: 'HIGH' }
};
const TIERS = [
  { sight: 1, zoom: 2.0, speed: 14 },
  { sight: 1, zoom: 2.5, speed: 18 },
  { sight: 1, zoom: 3.0, speed: 22 },
  { sight: 2, zoom: 3.5, speed: 28 },
  { sight: 2, zoom: 4.0, speed: 34 },
  { sight: 3, zoom: 5.0, speed: 42 }
];
const THEMES = [
  { k: 'tundra', n: 'FROZEN TUNDRA', sky: ['#7f9bb0', '#d4e3ee'], ground: ['#d3dee6', '#8ea2b1'], ridge: ['#aebfcc', '#8fa3b3', '#6f8496'], rid: 1.2, feats: ['rock', 'spike', 'rock'], fc: ['#6b7d8c', '#9fb2c0'], moons: [{ az: 0.9, el: 0.28, r: 0.05, col: '#e8eef4' }], temp: -24, o2: 20.8, pr: 0.96, rad: 0.11, g: 0.98 },
  { k: 'desert', n: 'ARID DESERT', sky: ['#b99468', '#efd5a8'], ground: ['#cba26a', '#9c7440'], ridge: ['#d6b887', '#c29f6a', '#a98250'], rid: 0.55, feats: ['dune', 'rock', 'spike'], fc: ['#a47a45', '#7d5a2f'], moons: [{ az: -0.7, el: 0.34, r: 0.035, col: '#f3e6cf' }, { az: -0.45, el: 0.22, r: 0.022, col: '#d9c3a0' }], temp: 41, o2: 21.4, pr: 1.01, rad: 0.18, g: 1.03 },
  { k: 'forest', n: 'DENSE FOREST', sky: ['#6f97aa', '#bad4dd'], ground: ['#436541', '#27401f'], ridge: ['#7ea08f', '#587a67', '#3f5f4a'], rid: 0.9, feats: ['tree', 'tree', 'rock'], fc: ['#2a4a2a', '#1d351e'], moons: [{ az: 2.1, el: 0.18, r: 0.12, col: '#c9d6e8' }], temp: 17, o2: 22.6, pr: 1.04, rad: 0.09, g: 0.94 },
  { k: 'ruins', n: 'ANCIENT RUINS', sky: ['#7a8795', '#c4cbd2'], ground: ['#706c60', '#47443b'], ridge: ['#9ea5ab', '#7f868c', '#626a70'], rid: 0.6, feats: ['pillar', 'rock', 'pillar'], fc: ['#8d897b', '#605c50'], moons: [{ az: 0.3, el: 0.4, r: 0.04, col: '#e8e4d8' }], spire: true, temp: 12, o2: 19.9, pr: 0.99, rad: 0.14, g: 1.01 },
  { k: 'volcanic', n: 'VOLCANIC BASALT', sky: ['#3a2224', '#c06a40'], ground: ['#3b3836', '#1d1b1a'], ridge: ['#5a3a34', '#3f2a27', '#2a1c1b'], rid: 1.7, feats: ['spike', 'rock', 'rock'], fc: ['#26211f', '#4a4340'], moons: [{ az: -1.5, el: 0.2, r: 0.16, col: '#ff9a5a' }], glow: true, temp: 58, o2: 19.4, pr: 1.12, rad: 0.31, g: 1.12 }
];
const BANDS = [
  { id: 'PINPOINT', max: 30, travel: '1:00', yield: '100%', intel: 'one extra intel tier', cls: 'ok' },
  { id: 'GOOD', max: 80, travel: '1:30', yield: '90%', intel: 'full intel', cls: 'ok' },
  { id: 'ROUGH', max: 160, travel: '2:00', yield: '80%', intel: 'one intel tier fewer', cls: 'warn' },
  { id: 'POOR', max: 99999, travel: '3:00', yield: '70%', intel: 'no intel', cls: 'bad' }
];
const TEAMS = [
  { n: 'EXPLORATION TEAM 1', col: '#7ffbff', roles: ['L', 'S', 'Sc', 'Li'] },
  { n: 'RECON TEAM 1', col: '#6dffb0', roles: ['L', 'Sn', 'R'] },
  { n: 'ASSAULT TEAM 1', col: '#ff9a7a', roles: ['L', 'Rf', 'G', 'Gr'] }
];
let haz = 'med';
let tier = 0;
let cfg = null;
let active = false;
let feed = null;
let G = null;
let thermal = false;
let yaw = 0;
let pitch = 0;
let zoom = 1;
let lockP = 0;
let aimInfo = null;
let drag = null;
let lowFx = false;
let modeSel = 'rescue';
let snd = null;
let lastZoom = 1;
let lastServo = 0;

function rnd(a, b) { return a + Math.random() * (b - a); }
function sightR() { return TIERS[tier].sight; }
const keys = {};
function wrapA(a) { while (a > Math.PI) a -= 2 * Math.PI; while (a < -Math.PI) a += 2 * Math.PI; return a; }
function hash(i) { const s = Math.sin(i * 127.1 + G.seed * 311.7) * 43758.5453; return s - Math.floor(s); }
function noise1(x) { const i = Math.floor(x); const f = x - i; const u = f * f * (3 - 2 * f); return hash(i) * (1 - u) + hash(i + 1) * u; }

function newGame() {
  const H = HAZ[haz];
  const n = H.size;
  const WS = n * CELL;
  const th = THEMES[cfg.theme];
  const night = cfg.night;
  const tm = cfg.team;
  const hurt = cfg.hurt;
  G = { n, WS, th, night, tm, hurtSet: new Set(hurt), seed: Math.random() * 100, mark: null, markMode: false, done: false, found: false, feats: [], stars: [], guess: null, linkLost: false, clockEnd: performance.now() + cfg.remain, t0: performance.now(), lastT: performance.now(), dt: 0.016, vx: 0, vy: 0, speed: 0, alt: 9, edge: false, trail: [], gate: { x: WS / 2, y: WS - 50 }, mode: modeSel, expo: 0, simT: 0, str: 0, inCone: false, contacts: [], obs: [], spotted: false, tagged: 0 };
  G.cam = { x: G.gate.x, y: G.gate.y };
  if (modeSel === 'rescue') { do { G.px = rnd(0.08, 0.92) * WS; G.py = rnd(0.08, 0.92) * WS; } while (Math.hypot(G.px - G.cam.x, G.py - G.cam.y) < 2.6 * CELL); }
  else buildSite();
  G.exp = document.createElement('canvas');
  G.exp.width = 260;
  G.exp.height = 260;
  for (let cy = -2; cy < n + 2; cy++) for (let cx = -2; cx < n + 2; cx++) {
    for (let k = 0; k < 9; k++) {
      const type = th.feats[Math.floor(Math.random() * th.feats.length)];
      G.feats.push({ x: (cx + Math.random()) * CELL, y: (cy + Math.random()) * CELL, type, s: rnd(0.7, 1.4), c: th.fc[Math.floor(Math.random() * 2)] });
    }
  }
  for (let i = 0; i < 90; i++) G.stars.push({ az: rnd(-Math.PI, Math.PI), el: rnd(0.02, 0.9), s: rnd(0.6, 1.8) });
  yaw = 0;
  pitch = 0.04;
  zoom = 1;
  lockP = 0;
  render();
  drawTeamView();
  $d('zv').style.display = 'none';
}

function buildSite() {
  const WS = G.WS;
  const sx = rnd(0.3, 0.7) * WS;
  const sy = rnd(0.18, 0.4) * WS;
  G.px = sx;
  G.py = sy;
  G.site = { x: sx, y: sy };
  const dark = ['#3b4048', '#565c66'];
  const add = (x, y, type, s2, col) => G.feats.push({ x, y, type, s: s2, c: col });
  const R = 62;
  const segs = 44;
  for (let i = 0; i < segs; i++) {
    const a = i / segs * 2 * Math.PI;
    if (Math.abs(wrapA(a - Math.PI)) < 0.35) continue;
    add(sx + Math.sin(a) * R, sy - Math.cos(a) * R, 'wall', 1, dark[i % 2]);
  }
  for (let i = 0; i < 4; i++) { const a = rnd(0, 6.28); const r = rnd(10, 40); add(sx + Math.sin(a) * r, sy - Math.cos(a) * r, 'hut', 1, '#4a4f58'); }
  add(sx, sy - 22, 'gate', 1, '#8c96a3');
  const dx = sx + rnd(-16, 16);
  const dy = sy + rnd(-8, 20);
  for (let i = 0; i < 4; i++) add(dx + rnd(-4, 4), dy + rnd(-4, 4), 'crate', 1, '#5d636d');
  add(sx - 52, sy - 52, 'tower', 0.5, '#3b4048');
  add(sx + 52, sy + 52, 'tower', 0.5, '#3b4048');
  const mk = o => { o.tagged = false; o.dw = 0; o.n = 0; G.contacts.push(o); return o; };
  mk({ kind: 'struct', label: 'WATCHTOWER', x: sx - 52, y: sy - 52, z: 0, hgt: 9, hot: false });
  mk({ kind: 'struct', label: 'WATCHTOWER', x: sx + 52, y: sy + 52, z: 0, hgt: 9, hot: false });
  mk({ kind: 'struct', label: 'SUPPLY DEPOT', x: dx, y: dy, z: 0, hgt: 3.5, hot: false });
  const D = { low: 5, med: 7, high: 9 }[haz];
  const P = { low: 1, med: 2, high: 3 }[haz];
  const Gc = D - 2 - P;
  const addObs = (o, z) => { o.known = false; o.z = z; o.head = o.base || 0; const ct = mk({ kind: 'def', label: 'HOSTILE', x: o.x, y: o.y, z, hgt: 1.8, hot: true }); o.def = ct; G.obs.push(o); };
  [[-52, -52], [52, 52]].forEach(t => addObs({ kind: 'tower', x: sx + t[0], y: sy + t[1], r: 75, half: 0.75, base: Math.atan2(t[0], -t[1]), amp: 1.0, w: 0.35, ph: rnd(0, 6) }, 9));
  for (let i = 0; i < Gc; i++) { const a = rnd(0, 6.28); const r = rnd(8, 46); addObs({ kind: 'guard', x: sx + Math.sin(a) * r, y: sy - Math.cos(a) * r, r: 52, half: 0.62, base: a, amp: 1.2, w: rnd(0.4, 0.7), ph: rnd(0, 6) }, 0); }
  for (let i = 0; i < P; i++) { const Rp = 95 + i * 22; addObs({ kind: 'patrol', x: sx, y: sy - Rp, r: 56, half: 0.55, R: Rp, om: (i % 2 ? -1 : 1) * 8 / Rp, ph: rnd(0, 6.28) }, 0); }
}

function hideHint() { $d('hint').style.display = 'none'; }

function toggleMode() {
  thermal = !thermal;
  $d('bmode').textContent = thermal ? 'THERMAL' : 'OPTICAL';
  $d('bmode').classList.toggle('on', thermal);
  sfxClick();
  if (G && G.found) drawTeamView();
}

function sweepR() { return (sightR() + 0.5) * CELL * HAZ[haz].haze * (1 + (G.alt - 9) / 50); }

function confirmRecon() { if (G.done) return; G.done = true; render(); }

function toggleMark() { G.markMode = !G.markMode; render(); }

function confirmFix() {
  if (G.done) return;
  if (G.found) G.guess = { x: G.px, y: G.py };
  else if (G.mark) G.guess = G.mark;
  else return;
  G.done = true;
  render();
}

function mouseLook() {
  try { const f = $d('feed'); if (f.requestPointerLock) f.requestPointerLock(); } catch (e) {}
}

function step(now) {
  const dt = Math.min(0.05, Math.max(0.001, (now - G.lastT) / 1000));
  G.lastT = now;
  G.dt = dt;
  const live = !G.done && !G.linkLost;
  const T = TIERS[tier];
  const lk = 1.5 * dt / Math.pow(zoom, 0.7);
  if (keys.ArrowLeft) yaw = wrapA(yaw - lk);
  if (keys.ArrowRight) yaw = wrapA(yaw + lk);
  if (keys.ArrowUp) pitch = Math.min(0.55, pitch + 0.9 * dt / Math.pow(zoom, 0.7));
  if (keys.ArrowDown) pitch = Math.max(-0.45, pitch - 0.9 * dt / Math.pow(zoom, 0.7));
  let fz = 0;
  let fx = 0;
  if (live) {
    if (keys.w) fz += 1;
    if (keys.s) fz -= 1;
    if (keys.d) fx += 1;
    if (keys.a) fx -= 1;
    if (keys.e) G.alt = Math.min(24, G.alt + 10 * dt);
    if (keys.q) G.alt = Math.max(4, G.alt - 10 * dt);
  }
  const top = T.speed * (keys.Shift ? 1.8 : 1);
  const len = Math.hypot(fx, fz) || 1;
  const tvx = (fx || fz) ? (Math.sin(yaw) * fz + Math.cos(yaw) * fx) / len * top : 0;
  const tvy = (fx || fz) ? (-Math.cos(yaw) * fz + Math.sin(yaw) * fx) / len * top : 0;
  const a = Math.min(1, dt * 2.6);
  G.vx += (tvx - G.vx) * a;
  G.vy += (tvy - G.vy) * a;
  let nx = G.cam.x + G.vx * dt;
  let ny = G.cam.y + G.vy * dt;
  G.edge = false;
  if (nx < 0 || nx > G.WS) { nx = Math.max(0, Math.min(G.WS, nx)); G.vx = 0; G.edge = true; }
  if (ny < 0 || ny > G.WS) { ny = Math.max(0, Math.min(G.WS, ny)); G.vy = 0; G.edge = true; }
  G.cam.x = nx;
  G.cam.y = ny;
  G.speed = Math.hypot(G.vx, G.vy);
  G.simT += dt;
  if (G.mode === 'recon') {
    let inC = 0;
    let warn = false;
    G.obs.forEach(o => {
      if (o.kind === 'patrol') {
        const an = o.ph + G.simT * o.om;
        o.x = G.site.x + Math.sin(an) * o.R;
        o.y = G.site.y - Math.cos(an) * o.R;
        o.head = o.om > 0 ? an + Math.PI / 2 : an - Math.PI / 2;
      } else o.head = o.base + Math.sin(G.simT * o.w + o.ph) * o.amp;
      o.def.x = o.x;
      o.def.y = o.y;
      const ddx = G.cam.x - o.x;
      const ddy = G.cam.y - o.y;
      const d = Math.hypot(ddx, ddy);
      const r = o.r * (G.night ? 0.75 : 1);
      if (d < sweepR() * 1.25) o.known = true;
      const aoff = Math.abs(wrapA(Math.atan2(ddx, -ddy) - o.head));
      if (d < r && aoff < o.half) inC = Math.max(inC, 1.4 - d / r);
      else if (d < r * 1.35 && aoff < o.half + 0.3) { warn = true; o.known = true; }
    });
    G.inCone = inC > 0;
    G.warn = warn && inC === 0;
    if (inC > 0 && live) {
      const spd01 = G.speed / (T.speed * 1.8);
      const altN = (G.alt - 4) / 20;
      G.expo += dt * (0.05 + 0.10 * spd01 + 0.06 * altN) * inC;
    } else if (live) G.expo = Math.max(0, G.expo - dt * 0.30);
    if (G.expo >= 1 && live) { G.expo = 1; G.spotted = true; G.linkLost = true; G.done = true; render(); }
  }
  let str = Math.max(0, Math.min(1, 1 - Math.hypot(G.px - nx, G.py - ny) / (G.WS * 0.95)));
  if (haz === 'high') str = Math.max(0, Math.min(1, str + (noise1(G.simT * 2) * 2 - 1) * 0.07));
  G.str = G.found ? 1 : str;
  const lt = G.trail[G.trail.length - 1];
  if (!lt || Math.hypot(lt.x - nx, lt.y - ny) > 8) { G.trail.push({ x: nx, y: ny }); if (G.trail.length > 400) G.trail.shift(); }
  const ec = G.exp.getContext('2d');
  const sc = 260 / G.WS;
  ec.fillStyle = 'rgba(20,70,95,0.55)';
  ec.beginPath();
  ec.arc(nx * sc, ny * sc, sweepR() * sc, 0, 7);
  ec.fill();
}

function drawRadar(now) {
  const cv = $d('radar');
  const c = cv.getContext('2d');
  const S = 260;
  const sc = S / G.WS;
  c.fillStyle = '#04101a';
  c.fillRect(0, 0, S, S);
  c.drawImage(G.exp, 0, 0);
  c.strokeStyle = '#12354b';
  c.lineWidth = 1;
  c.strokeRect(0.5, 0.5, S - 1, S - 1);
  c.fillStyle = '#6f93a8';
  c.font = '10px monospace';
  c.textAlign = 'center';
  c.fillText('N', S / 2, 11);
  const gx = G.gate.x * sc;
  const gy = G.gate.y * sc;
  c.strokeStyle = '#6f93a8';
  c.beginPath(); c.moveTo(gx, gy - 5); c.lineTo(gx + 5, gy); c.lineTo(gx, gy + 5); c.lineTo(gx - 5, gy); c.closePath(); c.stroke();
  c.fillText('GATE', gx, gy + 16);
  if (G.mode === 'recon') {
    c.strokeStyle = 'rgba(255,107,107,0.6)';
    c.setLineDash([4, 4]);
    c.beginPath(); c.arc(G.site.x * sc, G.site.y * sc, 70 * sc, 0, 7); c.stroke();
    c.setLineDash([]);
    c.fillStyle = '#ff8a7a';
    c.fillText('TARGET SITE', G.site.x * sc, G.site.y * sc - 76 * sc);
    G.obs.forEach(o => {
      if (!o.known && !G.done) return;
      const r = o.r * (G.night ? 0.75 : 1) * sc;
      c.fillStyle = 'rgba(255,90,70,0.2)';
      c.beginPath();
      c.moveTo(o.x * sc, o.y * sc);
      c.arc(o.x * sc, o.y * sc, r, o.head - o.half - Math.PI / 2, o.head + o.half - Math.PI / 2);
      c.closePath();
      c.fill();
    });
    G.contacts.forEach(ct => {
      if (!ct.tagged && !G.done) return;
      c.fillStyle = ct.kind === 'def' ? '#ff6b6b' : '#ffd36b';
      if (ct.kind === 'def') { c.beginPath(); c.arc(ct.x * sc, ct.y * sc, 3, 0, 7); c.fill(); } else c.fillRect(ct.x * sc - 3, ct.y * sc - 3, 6, 6);
    });
  }
  if (G.trail.length > 1) {
    c.strokeStyle = 'rgba(127,251,255,0.35)';
    c.beginPath();
    G.trail.forEach((p, i) => { if (i) c.lineTo(p.x * sc, p.y * sc); else c.moveTo(p.x * sc, p.y * sc); });
    c.stroke();
  }
  const dx = G.cam.x * sc;
  const dy = G.cam.y * sc;
  c.strokeStyle = 'rgba(127,251,255,0.35)';
  c.setLineDash([3, 4]);
  c.beginPath(); c.arc(dx, dy, sweepR() * sc, 0, 7); c.stroke();
  c.setLineDash([]);
  const half = (70 * Math.PI / 180) / 2 / zoom;
  c.fillStyle = 'rgba(127,251,255,0.16)';
  c.beginPath();
  c.moveTo(dx, dy);
  c.arc(dx, dy, sweepR() * sc, yaw - half - Math.PI / 2, yaw + half - Math.PI / 2);
  c.closePath();
  c.fill();
  c.save();
  c.translate(dx, dy);
  c.rotate(yaw);
  c.fillStyle = '#7ffbff';
  c.beginPath(); c.moveTo(0, -7); c.lineTo(5, 6); c.lineTo(0, 3); c.lineTo(-5, 6); c.closePath(); c.fill();
  c.restore();
  if (G.mark) {
    const mx = G.mark.x * sc;
    const my = G.mark.y * sc;
    c.strokeStyle = '#6dffb0';
    c.lineWidth = 2;
    c.beginPath(); c.moveTo(mx - 7, my); c.lineTo(mx + 7, my); c.moveTo(mx, my - 7); c.lineTo(mx, my + 7); c.stroke();
    c.lineWidth = 1;
  }
  if (G.mode === 'rescue' && (G.found || G.done)) {
    const tx = G.px * sc;
    const ty = G.py * sc;
    c.strokeStyle = '#6dffb0';
    c.lineWidth = 2;
    c.beginPath(); c.arc(tx, ty, 8, 0, 7); c.stroke();
    c.lineWidth = 1;
    c.fillStyle = '#6dffb0';
    c.fillText('TEAM', tx, ty - 12);
  }
  c.textAlign = 'left';
}

function maxVis() { return (sightR() + 1.6) * CELL * HAZ[haz].haze * (G.night ? 0.8 : 1); }
function detRange() { return sweepR() * (thermal ? 1 : (G.night ? 0.19 : 0.62)); }

function project(fx, fy, camX, camY) {
  const dx = fx - camX;
  const dy = fy - camY;
  const dist = Math.hypot(dx, dy);
  const bearing = Math.atan2(dx, -dy);
  const rel = wrapA(bearing - yaw);
  return { dist, rel, dz: dist * Math.cos(rel), bearing };
}

function mix(a, b, t) {
  const pa = [1, 3, 5].map(i => parseInt(a.substr(i, 2), 16));
  const pb = [1, 3, 5].map(i => parseInt(b.substr(i, 2), 16));
  return 'rgb(' + pa.map((v, i) => Math.round(v + (pb[i] - v) * t)).join(',') + ')';
}

function drawFeed(now) {
  const cv = $d('cv');
  const c = cv.getContext('2d');
  const W = cv.width;
  const H = cv.height;
  const th = G.th;
  const night = G.night;
  const gliding = G.speed > 1.5;
  const sp = Math.min(1, G.speed / (TIERS[tier].speed * 1.8));
  const camX = G.cam.x;
  const camY = G.cam.y;
  const fov = 70 * Math.PI / 180;
  const f = (W / 2) / Math.tan(fov / 2 / zoom);
  const bob = gliding && !lowFx ? Math.sin(now * 0.02) * 3 * sp : 0;
  const hy = H / 2 + Math.tan(pitch) * f + bob;
  const camH = G.alt;
  const mv = maxVis();
  const skyA = night ? ['#02040a', '#101a30'] : th.sky;
  const grA = night ? [mix(th.ground[0], '#02040a', 0.8), mix(th.ground[1], '#02040a', 0.85)] : th.ground;

  const sg = c.createLinearGradient(0, Math.min(hy, H) - 400, 0, Math.max(1, hy));
  sg.addColorStop(0, skyA[0]);
  sg.addColorStop(1, skyA[1]);
  c.fillStyle = sg;
  c.fillRect(0, 0, W, H);

  if (night) {
    c.fillStyle = '#ffffff';
    G.stars.forEach(st => {
      const sx = W / 2 + Math.tan(wrapA(st.az - yaw)) * f;
      const sy = hy - Math.tan(st.el) * f;
      if (sx > 0 && sx < W && sy > 0 && sy < hy) { c.globalAlpha = 0.5 + 0.4 * Math.sin(now * 0.003 + st.az * 9); c.fillRect(sx, sy, st.s, st.s); }
    });
    c.globalAlpha = 1;
  }
  th.moons.forEach(m => {
    const sx = W / 2 + Math.tan(wrapA(m.az - yaw)) * f;
    const sy = hy - Math.tan(m.el) * f;
    const r = Math.tan(m.r) * f;
    if (sx > -r && sx < W + r) {
      c.globalAlpha = night ? 1 : 0.55;
      c.fillStyle = m.col;
      c.beginPath(); c.arc(sx, sy, r, 0, 7); c.fill();
      c.fillStyle = 'rgba(0,0,0,0.12)';
      c.beginPath(); c.arc(sx - r * 0.3, sy - r * 0.2, r * 0.3, 0, 7); c.fill();
      c.globalAlpha = 1;
    }
  });
  if (th.glow) {
    const gx = W / 2 + Math.tan(wrapA(-0.2 - yaw)) * f;
    const gr = c.createRadialGradient(gx, hy, 4, gx, hy, 260 * zoom);
    gr.addColorStop(0, 'rgba(255,120,40,0.55)');
    gr.addColorStop(1, 'rgba(255,120,40,0)');
    c.fillStyle = gr;
    c.fillRect(0, 0, W, hy + 20);
  }

  th.ridge.forEach((col, li) => {
    const amp = th.rid * (0.05 + li * 0.04);
    const base = night ? mix(col, '#02040a', 0.82) : col;
    c.fillStyle = base;
    c.beginPath();
    c.moveTo(0, hy + 4);
    for (let x = 0; x <= W; x += 4) {
      const az = yaw + Math.atan((x - W / 2) / f);
      const par = (camX * 0.0004 + camY * 0.0003) * (li + 1);
      const v = noise1(az * (2.4 + li * 1.6) + li * 17 + par) * 0.65 + noise1(az * (7 + li * 3) + li * 5 + par) * 0.35;
      c.lineTo(x, hy - Math.tan(amp * (0.15 + v)) * f);
    }
    c.lineTo(W, hy + 4);
    c.closePath();
    c.fill();
  });
  if (th.spire) {
    const sx = W / 2 + Math.tan(wrapA(0.55 - yaw)) * f;
    const sh = Math.tan(0.12) * f;
    c.fillStyle = night ? '#0b1118' : '#6a727a';
    c.fillRect(sx - 5 * zoom, hy - sh, 10 * zoom, sh + 4);
    c.fillStyle = '#7ffbff';
    c.globalAlpha = 0.6 + 0.4 * Math.sin(now * 0.004);
    c.fillRect(sx - 3 * zoom, hy - sh - 8 * zoom, 6 * zoom, 10 * zoom);
    c.globalAlpha = 1;
  }

  const gg = c.createLinearGradient(0, hy, 0, H);
  gg.addColorStop(0, grA[0]);
  gg.addColorStop(1, grA[1]);
  c.fillStyle = gg;
  c.fillRect(0, Math.max(0, hy), W, H - Math.max(0, hy));

  const list = G.feats.map(ft => Object.assign({ p: project(ft.x, ft.y, camX, camY) }, ft)).filter(ft => ft.p.dist < mv && ft.p.dz > 4 && Math.abs(ft.p.rel) < (fov / 2 / zoom) + 0.35);
  list.sort((a, b) => b.p.dist - a.p.dist);
  list.forEach(ft => {
    const sx = W / 2 + Math.tan(ft.p.rel) * f;
    const by = hy + (camH / ft.p.dz) * f;
    const sc = (1 / ft.p.dz) * f * ft.s * 0.3;
    c.globalAlpha = Math.max(0.12, Math.min(1, 1.15 - ft.p.dist / mv));
    c.fillStyle = night ? mix(ft.c, '#02040a', 0.75) : ft.c;
    if (ft.type === 'tree') { c.beginPath(); c.moveTo(sx, by - 46 * sc); c.lineTo(sx + 12 * sc, by); c.lineTo(sx - 12 * sc, by); c.fill(); }
    else if (ft.type === 'rock') { c.beginPath(); c.ellipse(sx, by - 5 * sc, 11 * sc, 6 * sc, 0, 0, 7); c.fill(); }
    else if (ft.type === 'pillar') { c.fillRect(sx - 4 * sc, by - 34 * sc, 8 * sc, 34 * sc); c.fillRect(sx - 6 * sc, by - 36 * sc, 12 * sc, 4 * sc); }
    else if (ft.type === 'spike') { c.beginPath(); c.moveTo(sx, by - 26 * sc); c.lineTo(sx + 4 * sc, by); c.lineTo(sx - 4 * sc, by); c.fill(); }
    else if (ft.type === 'wall') { c.fillRect(sx - 14 * sc, by - 12 * sc, 28 * sc, 12 * sc); }
    else if (ft.type === 'hut') { c.fillRect(sx - 16 * sc, by - 14 * sc, 32 * sc, 14 * sc); c.beginPath(); c.moveTo(sx - 19 * sc, by - 14 * sc); c.lineTo(sx, by - 26 * sc); c.lineTo(sx + 19 * sc, by - 14 * sc); c.fill(); }
    else if (ft.type === 'crate') { c.fillRect(sx - 5 * sc, by - 8 * sc, 10 * sc, 8 * sc); }
    else if (ft.type === 'tower') { c.fillRect(sx - 6 * sc, by - 60 * sc, 12 * sc, 60 * sc); c.fillRect(sx - 12 * sc, by - 66 * sc, 24 * sc, 7 * sc); }
    else if (ft.type === 'gate') { c.strokeStyle = c.fillStyle; c.lineWidth = Math.max(2, 3 * sc); c.beginPath(); c.ellipse(sx, by - 22 * sc, 18 * sc, 22 * sc, 0, 0, 7); c.stroke(); }
    else { c.beginPath(); c.ellipse(sx, by - 4 * sc, 26 * sc, 7 * sc, 0, 0, 7); c.fill(); }
  });
  c.globalAlpha = 1;

  const fg = c.createLinearGradient(0, hy - 30, 0, hy + 60);
  const fogc = night ? '30,45,70' : '220,228,232';
  fg.addColorStop(0, 'rgba(' + fogc + ',0)');
  fg.addColorStop(0.45, 'rgba(' + fogc + ',' + (haz === 'low' ? 0.16 : (haz === 'med' ? 0.34 : 0.5)) + ')');
  fg.addColorStop(1, 'rgba(' + fogc + ',0)');
  c.fillStyle = fg;
  c.fillRect(0, hy - 30, W, 90);

  if (night && !thermal) {
    c.fillStyle = 'rgba(0,4,16,0.45)';
    c.fillRect(0, 0, W, H);
  }
  if (thermal) {
    c.filter = 'grayscale(1) contrast(1.35) brightness(' + (night ? 1.7 : 0.72) + ')';
    c.drawImage(cv, 0, 0);
    c.filter = 'none';
  }

  const tp = project(G.px, G.py, camX, camY);
  const det = detRange();
  aimInfo = null;
  if (G.mode === 'recon') reconFeed(c, W, H, hy, camX, camY, camH, f, fov, det);
  if (G.mode === 'rescue' && tp.dist <= det && tp.dz > 4 && Math.abs(tp.rel) < fov / 2 / zoom + 0.2) {
    const sx = W / 2 + Math.tan(tp.rel) * f;
    const by = hy + (camH / tp.dz) * f;
    const k = 1 - tp.dist / det;
    const gy = by - 1.5 * f / tp.dz;
    if (thermal) {
      const r = Math.max(10, (5 * f / tp.dz) * (0.6 + k));
      const g = c.createRadialGradient(sx, gy, 1, sx, gy, r);
      g.addColorStop(0, 'rgba(255,255,230,0.95)');
      g.addColorStop(0.35, 'rgba(255,170,40,0.7)');
      g.addColorStop(1, 'rgba(255,60,0,0)');
      c.fillStyle = g;
      c.beginPath(); c.arc(sx, gy, r, 0, 7); c.fill();
    } else {
      const u = f / tp.dz;
      c.globalAlpha = 0.35 + 0.6 * k;
      c.strokeStyle = '#e8e8e8';
      c.lineWidth = Math.max(1.5, 0.9 * u);
      c.beginPath();
      c.moveTo(sx, by);
      c.bezierCurveTo(sx - 4 * u, by - 9 * u, sx + 5 * u, by - 20 * u, sx, by - 30 * u);
      c.stroke();
      c.fillStyle = '#ff5030';
      c.beginPath(); c.arc(sx, by - 1, Math.max(2, 1.4 * u), 0, 7); c.fill();
      c.globalAlpha = 1;
    }
    aimInfo = { sx, sy: gy, dist: tp.dist };
  }
  if (G.mode === 'rescue' && tp.dist < 85) teamFigs(c, W, hy, camX, camY, f);

  const cx = W / 2;
  const cyy = H / 2;
  let locking = false;
  if (G.mode === 'rescue') {
    if (aimInfo && !G.done && !G.found && !G.linkLost) locking = Math.hypot(aimInfo.sx - cx, aimInfo.sy - cyy) < 46;
    if (!G.done && !G.found && !G.linkLost) {
      if (locking) lockP = Math.min(1, lockP + G.dt / 1.1); else lockP = Math.max(0, lockP - G.dt / 0.6);
      if (lockP >= 1) { G.found = true; showTeam(); sfxLock(); render(); }
    }
  } else {
    const live2 = !G.done && !G.linkLost;
    const onAim = live2 && aimInfo && Math.hypot(aimInfo.sx - cx, aimInfo.sy - cyy) < 46;
    lockP = 0;
    G.contacts.forEach(ct => { if (!(onAim && aimInfo.contact === ct)) ct.dw = Math.max(0, ct.dw - G.dt / 0.6); });
    if (onAim) {
      const ct = aimInfo.contact;
      locking = true;
      ct.dw = Math.min(1, ct.dw + G.dt / 0.8);
      lockP = ct.dw;
      if (ct.dw >= 1) { ct.tagged = true; G.tagged++; ct.n = G.tagged; lockP = 0; sfxLock(); }
    }
  }

  if (gliding && !lowFx) {
    c.strokeStyle = 'rgba(200,230,255,' + (0.35 * sp) + ')';
    c.lineWidth = 1;
    for (let i = 0; i < 46; i++) {
      const a = Math.random() * 6.283;
      const r1 = 120 + Math.random() * 160;
      const r2 = r1 + 30 + 120 * sp * Math.random();
      c.beginPath();
      c.moveTo(cx + Math.cos(a) * r1, cyy + Math.sin(a) * r1 * 0.7);
      c.lineTo(cx + Math.cos(a) * r2, cyy + Math.sin(a) * r2 * 0.7);
      c.stroke();
    }
  }

  c.strokeStyle = G.found ? '#6dffb0' : (locking ? '#ffd36b' : 'rgba(127,251,255,0.9)');
  c.lineWidth = 1.5;
  c.beginPath(); c.arc(cx, cyy, 46, 0, 7); c.stroke();
  c.beginPath();
  c.moveTo(cx - 62, cyy); c.lineTo(cx - 20, cyy); c.moveTo(cx + 20, cyy); c.lineTo(cx + 62, cyy);
  c.moveTo(cx, cyy - 62); c.lineTo(cx, cyy - 20); c.moveTo(cx, cyy + 20); c.lineTo(cx, cyy + 62);
  c.stroke();
  if (lockP > 0 && !G.found) {
    c.strokeStyle = '#ffd36b';
    c.lineWidth = 4;
    c.beginPath(); c.arc(cx, cyy, 54, -Math.PI / 2, -Math.PI / 2 + lockP * 2 * Math.PI); c.stroke();
  }

  c.fillStyle = 'rgba(0,12,20,0.55)';
  c.fillRect(0, 0, W, 34);
  const deg = ((yaw * 180 / Math.PI) % 360 + 360) % 360;
  c.font = '13px monospace';
  c.textAlign = 'center';
  const ppd = W / 70 * zoom;
  for (let d = -60; d <= 60; d += 5) {
    const a = Math.round(deg / 5) * 5 + d;
    const x = cx + (a - deg) * ppd;
    if (x < 0 || x > W) continue;
    const an = ((a % 360) + 360) % 360;
    c.strokeStyle = '#7ffbff';
    c.lineWidth = 1;
    c.beginPath(); c.moveTo(x, 34); c.lineTo(x, an % 15 === 0 ? 24 : 29); c.stroke();
    if (an % 45 === 0) { c.fillStyle = '#7ffbff'; c.fillText({ 0: 'N', 45: 'NE', 90: 'E', 135: 'SE', 180: 'S', 225: 'SW', 270: 'W', 315: 'NW' }[an], x, 17); }
  }
  c.fillStyle = '#ffd36b';
  c.beginPath(); c.moveTo(cx, 36); c.lineTo(cx - 5, 44); c.lineTo(cx + 5, 44); c.fill();
  const slab = G.mode === 'recon' ? 'SITE' : 'SIG';
  if (!G.found && haz !== 'high') {
    const so = haz === 'med' ? (noise1(camX * 0.012 + camY * 0.017 + 50) * 2 - 1) * 0.45 : 0;
    const sb = Math.atan2(G.px - camX, -(G.py - camY)) + so;
    const sd = wrapA(sb - yaw) * 180 / Math.PI;
    if (Math.abs(sd) * ppd < W / 2 - 14) {
      const x = cx + sd * ppd;
      c.fillStyle = '#ff7a50';
      c.beginPath(); c.moveTo(x, 34); c.lineTo(x - 6, 22); c.lineTo(x + 6, 22); c.fill();
      c.fillText(slab, x, 12);
    } else {
      c.fillStyle = '#ff7a50';
      c.textAlign = sd < 0 ? 'left' : 'right';
      c.fillText(sd < 0 ? '< ' + slab : slab + ' >', sd < 0 ? 8 : W - 8, 24);
    }
  }
  hudMeters(c, W, H);
  c.textAlign = 'left';
  c.fillStyle = '#7ffbff';
  c.font = '14px monospace';
  c.fillText('DRONE 1  CAM 1  ' + (thermal ? 'THERMAL' : (night ? 'LOW LIGHT' : 'OPTICAL')), 12, H - 38);
  c.fillText('ZOOM ' + zoom.toFixed(1) + 'x  HDG ' + String(Math.round(deg)).padStart(3, '0') + '  PITCH ' + (pitch >= 0 ? '+' : '') + Math.round(pitch * 180 / Math.PI), 12, H - 16);
  c.textAlign = 'right';
  const left = Math.max(0, G.clockEnd - now) / 1000;
  c.fillStyle = left < 30 ? '#ff6b6b' : '#7ffbff';
  c.fillText('WORMHOLE ' + Math.floor(left / 60) + ':' + String(Math.floor(left % 60)).padStart(2, '0'), W - 12, H - 38);
  c.fillStyle = G.found ? '#6dffb0' : (locking ? '#ffd36b' : '#7ffbff');
  c.fillText(G.edge ? 'SURVEY AREA LIMIT' : (G.found ? 'TARGET ACQUIRED' : (locking ? 'LOCKING ' + Math.round(lockP * 100) + '%' : (aimInfo ? (aimInfo.label || 'HEAT SIGNATURE') : 'SEARCHING'))), W - 12, H - 16);
  c.textAlign = 'left';
  if (Math.floor(now / 600) % 2 === 0) { c.fillStyle = '#ff4040'; c.beginPath(); c.arc(W - 70, 56, 5, 0, 7); c.fill(); c.fillStyle = '#ffb0b0'; c.font = '12px monospace'; c.fillText('REC', W - 58, 60); }

  if (thermal) {
    c.globalCompositeOperation = 'screen';
    c.fillStyle = 'rgba(0,40,55,0.35)';
    c.fillRect(0, 0, W, H);
    c.globalCompositeOperation = 'source-over';
  }
  const ng = lowFx ? 60 : (gliding ? 1000 : 380);
  c.fillStyle = 'rgba(255,255,255,0.14)';
  for (let i = 0; i < ng; i++) c.fillRect(Math.random() * W, Math.random() * H, rnd(1, gliding && !lowFx ? 24 : 3), 1);

  if (G.linkLost) {
    c.fillStyle = '#05080c';
    c.fillRect(0, 0, W, H);
    for (let i = 0; i < 2600; i++) { c.fillStyle = 'rgba(255,255,255,' + Math.random() * 0.5 + ')'; c.fillRect(Math.random() * W, Math.random() * H, rnd(1, 30), 1); }
    c.fillStyle = '#ff6b6b';
    c.font = '34px monospace';
    c.textAlign = 'center';
    c.fillText(G.spotted ? 'DRONE LOST' : 'LINK LOST', W / 2, H / 2 - 6);
    c.font = '15px monospace';
    c.fillText(G.spotted ? 'SPOTTED BY DEFENDERS // SURVEY ENDED' : 'WORMHOLE CLOSED // REDIAL TO RECONNECT', W / 2, H / 2 + 24);
    c.textAlign = 'left';
  }
  updateAudio(gliding, sp, locking);
}

function seg(c, x, y, v, col, n) {
  for (let i = 0; i < n; i++) { c.fillStyle = i < Math.round(v * n) ? col : 'rgba(127,251,255,0.18)'; c.fillRect(x + i * 13, y, 10, 8); }
}

function hudMeters(c, W, H) {
  if (G.mode === 'recon' && G.expo > 0.04) {
    const vg = c.createRadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, H * 0.85);
    vg.addColorStop(0, 'rgba(255,40,30,0)');
    vg.addColorStop(1, 'rgba(255,40,30,' + (0.12 + G.expo * 0.5) + ')');
    c.fillStyle = vg;
    c.fillRect(0, 0, W, H);
  }
  c.textAlign = 'left';
  c.font = '12px monospace';
  const sc2 = G.str;
  c.fillStyle = '#7ffbff';
  c.fillText(G.mode === 'recon' ? 'SITE' : 'SIGNAL', 12, 64);
  seg(c, 84, 56, sc2, sc2 > 0.66 ? '#6dffb0' : (sc2 > 0.33 ? '#ffd36b' : '#7ffbff'), 12);
  c.fillStyle = '#cfeaf5';
  c.fillText(Math.round(sc2 * 100) + '%' + (haz === 'high' && !G.found ? ' NOISY' : ''), 84 + 12 * 13 + 4, 64);
  if (G.mode === 'recon') {
    c.fillStyle = G.expo > 0.5 ? '#ff6b6b' : '#7ffbff';
    c.fillText('EXPOSURE', 12, 82);
    seg(c, 84, 74, G.expo, '#ff6b6b', 12);
    c.fillStyle = '#cfeaf5';
    c.fillText('CONTACTS ' + G.tagged + '/' + G.contacts.length, 12, 100);
    if (G.inCone) { c.fillStyle = '#ff6b6b'; c.textAlign = 'center'; c.font = '13px monospace'; c.fillText('IN DEFENDER VIEW', W / 2, 62); c.textAlign = 'left'; }
    else if (G.warn) { c.fillStyle = '#ffd36b'; c.textAlign = 'center'; c.font = '13px monospace'; c.fillText('DEFENDER NEARBY', W / 2, 62); c.textAlign = 'left'; }
  }
}

function reconFeed(c, W, H, hy, camX, camY, camH, f, fov, det) {
  const cx = W / 2;
  const cyy = H / 2;
  let best = null;
  let bd = 1e9;
  const list = G.contacts.map(ct => ({ ct, p: project(ct.x, ct.y, camX, camY) })).filter(o => o.p.dz > 4 && Math.abs(o.p.rel) < fov / 2 / zoom + 0.2);
  list.sort((a, b) => b.p.dist - a.p.dist);
  list.forEach(o => {
    const ct = o.ct;
    const p = o.p;
    if (!(p.dist <= det && (ct.hot || !thermal))) return;
    const sx = W / 2 + Math.tan(p.rel) * f;
    const u = f / p.dz;
    const base = hy + ((camH - ct.z) / p.dz) * f;
    const h = ct.hgt * u;
    const sy = base - h * 0.5;
    if (ct.kind === 'def') {
      if (thermal && h < 26) {
        const g = c.createRadialGradient(sx, sy, 1, sx, sy, 16);
        g.addColorStop(0, 'rgba(255,200,90,0.6)');
        g.addColorStop(1, 'rgba(255,90,0,0)');
        c.fillStyle = g;
        c.beginPath(); c.arc(sx, sy, 16, 0, 7); c.fill();
      }
      drawFig(c, sx, base, h, 'J', 'stand', thermal ? 'hot' : 'opt', '#d9dde4aa');
    }
    if (ct.tagged) {
      const m = Math.max(12, h * 0.62);
      c.strokeStyle = '#ff6b6b';
      c.lineWidth = 2;
      c.beginPath();
      [[-1, -1], [1, -1], [1, 1], [-1, 1]].forEach(k => { c.moveTo(sx + k[0] * m, sy + k[1] * (m * 0.5) - k[1] * 0); c.lineTo(sx + k[0] * m * 0.5, sy + k[1] * m * 0.5); });
      c.stroke();
      c.fillStyle = '#ff6b6b';
      c.font = '11px monospace';
      c.textAlign = 'center';
      c.fillText(String(ct.n), sx, sy - m * 0.5 - 4);
      c.textAlign = 'left';
    }
    const dd = Math.hypot(sx - cx, sy - cyy);
    if (!ct.tagged && dd < 70 && dd < bd) { bd = dd; best = { sx, sy, dist: p.dist, label: ct.kind === 'def' ? 'HOSTILE' : ct.label, contact: ct }; }
  });
  aimInfo = best;
}

function teamFigs(c, W, hy, camX, camY, f) {
  const tm = G.tm;
  const n = tm.roles.length;
  const items = [];
  tm.roles.forEach((role, i) => {
    const ox = (i - (n - 1) / 2) * 3.4;
    const oy = Math.sin(i * 2.1) * 1.6;
    const p = project(G.px + ox, G.py + oy, camX, camY);
    if (p.dz < 3) return;
    items.push({ i, role, p });
  });
  items.sort((a, b) => b.p.dist - a.p.dist);
  items.forEach(it => {
    const sx = W / 2 + Math.tan(it.p.rel) * f;
    const base = hy + (G.alt / it.p.dz) * f;
    const h = 1.8 * f / it.p.dz;
    const hurt = G.hurtSet.has(it.i);
    const med = G.hurtSet.size > 0 && it.i === medicIdx();
    drawFig(c, hurt ? sx - h * 0.4 : sx, base, hurt ? h * 0.85 : h, it.role, hurt ? 'prone' : (med ? 'kneel' : 'stand'), thermal ? 'hot' : 'opt', tm.col + 'aa');
  });
}

function drawFig(c, x, y, h, role, pose, mode, edge) {
  if (h < 3) return;
  c.save();
  c.translate(x, y);
  c.scale(h, h);
  const lw = 1 / h;
  const hot = mode === 'hot';
  const body = hot ? '#fff3cf' : '#0c141c';
  if (hot) { c.shadowColor = 'rgba(255,150,40,0.95)'; c.shadowBlur = Math.min(16, 4 + h * 0.08); }
  const prone = pose === 'prone';
  const kneel = pose === 'kneel';
  const armed = !prone;
  const sh = kneel ? 0.16 : 0;
  if (prone) { c.translate(0, -0.11); c.rotate(Math.PI / 2); }
  c.lineCap = 'round';
  c.lineJoin = 'round';
  const passes = hot ? [0] : [2.2 * lw, 0];
  passes.forEach(g => {
    const col = g > 0 ? edge : body;
    c.fillStyle = col;
    c.strokeStyle = col;
    const poly = pts => { c.beginPath(); pts.forEach((p, i) => { if (i) c.lineTo(p[0], p[1] + 0); else c.moveTo(p[0], p[1]); }); c.closePath(); c.fill(); if (g > 0) { c.lineWidth = g * 2; c.stroke(); } };
    const limb = (ax, ay, bx, by, w) => { c.lineWidth = w + g * 2; c.beginPath(); c.moveTo(ax, ay); c.lineTo(bx, by); c.stroke(); };
    const ell = (ex, ey, rx, ry) => { c.beginPath(); c.ellipse(ex, ey, rx + g, ry + g, 0, 0, 7); c.fill(); };
    const U = y2 => y2 + sh;
    if (kneel) {
      limb(-0.02, -0.34, -0.12, -0.05, 0.085);
      limb(-0.12, -0.05, -0.2, -0.03, 0.06);
      ell(-0.22, -0.02, 0.06, 0.025);
      limb(0.02, -0.34, 0.14, -0.2, 0.085);
      limb(0.14, -0.2, 0.12, -0.03, 0.07);
      ell(0.15, -0.015, 0.05, 0.025);
    } else {
      limb(-0.02, -0.5, -0.06, -0.26, 0.085);
      limb(-0.06, -0.26, -0.075, -0.03, 0.07);
      limb(0.02, -0.5, 0.07, -0.26, 0.085);
      limb(0.07, -0.26, 0.09, -0.03, 0.07);
      ell(-0.07, -0.015, 0.045, 0.025);
      ell(0.1, -0.015, 0.05, 0.025);
    }
    const armor = role !== 'Sc' && role !== 'Li';
    poly([[-0.12, U(-0.84)], [0.11, U(-0.84)], [0.1 + (armor ? 0.015 : 0), U(-0.5)], [-0.09 - (armor ? 0.015 : 0), U(-0.5)]]);
    limb(0.0, U(-0.84), 0.0, U(-0.88), 0.05);
    ell(0.01, U(-0.925), 0.058, 0.068);
    if (role === 'Sc') { ell(0.0, U(-0.955), 0.06, 0.035); }
    else if (role === 'Li') { poly([[-0.05, U(-0.965)], [0.07, U(-0.975)], [0.12, U(-0.945)], [0.02, U(-0.94)], [-0.05, U(-0.93)]]); }
    else if (role === 'R' || role === 'Sn') { ell(0.01, U(-0.955), 0.115, 0.02); ell(0.01, U(-0.975), 0.06, 0.04); }
    else if (role === 'J') { poly([[-0.07, U(-0.93)], [-0.03, U(-1.13)], [0.05, U(-1.13)], [0.075, U(-0.93)]]); poly([[-0.075, U(-0.92)], [0.09, U(-0.92)], [0.09, U(-0.89)], [-0.075, U(-0.89)]]); }
    else { c.beginPath(); c.ellipse(0.01, U(-0.935), 0.075 + g, 0.062 + g, 0, Math.PI, 2 * Math.PI); c.closePath(); c.fill(); poly([[0.03, U(-0.935)], [0.1, U(-0.925)], [0.1, U(-0.915)], [0.03, U(-0.92)]]); }
    if (role === 'Sc') poly([[-0.12, U(-0.62)], [-0.2, U(-0.6)], [-0.19, U(-0.5)], [-0.1, U(-0.5)]]);
    else if (role !== 'J') poly([[-0.12, U(-0.82)], [-0.2, U(-0.8)], [-0.21, U(-0.56)], [-0.1, U(-0.54)]]);
    if (role === 'L') limb(-0.17, U(-0.82), -0.22, U(-1.08), 0.012);
    if (armor && role !== 'J') poly([[0.08, U(-0.62)], [0.125, U(-0.62)], [0.125, U(-0.52)], [0.08, U(-0.52)]]);
    if (!armed) { limb(0.03, U(-0.8), 0.14, U(-0.7), 0.055); limb(-0.04, U(-0.8), 0.05, U(-0.68), 0.05); return; }
    if (role === 'J') {
      limb(0.03, U(-0.8), 0.2, U(-0.68), 0.055);
      limb(-0.04, U(-0.8), 0.12, U(-0.62), 0.05);
      limb(0.22, U(-1.02), 0.22, -0.01, 0.022);
      poly([[0.19, U(-1.02)], [0.25, U(-1.02)], [0.22, U(-1.15)]]);
      return;
    }
    limb(0.03, U(-0.8), 0.11, U(-0.68), 0.055);
    limb(0.11, U(-0.68), 0.22, U(-0.66), 0.05);
    limb(-0.04, U(-0.8), 0.04, U(-0.66), 0.05);
    limb(0.04, U(-0.66), 0.14, U(-0.65), 0.045);
    if (role === 'Sn') { limb(-0.12, U(-0.7), 0.48, U(-0.64), 0.03); limb(0.0, U(-0.73), 0.12, U(-0.72), 0.025); limb(0.4, U(-0.64), 0.43, U(-0.55), 0.012); }
    else if (role === 'G') { limb(-0.1, U(-0.7), 0.36, U(-0.64), 0.055); poly([[0.04, U(-0.64)], [0.12, U(-0.64)], [0.12, U(-0.55)], [0.04, U(-0.55)]]); }
    else if (role === 'Gr') { limb(-0.14, U(-0.76), 0.32, U(-0.68), 0.065); ell(0.3, U(-0.68), 0.04, 0.04); }
    else if (role === 'Sc') { poly([[0.18, U(-0.7)], [0.27, U(-0.7)], [0.27, U(-0.6)], [0.18, U(-0.6)]]); limb(0.27, U(-0.66), 0.33, U(-0.78), 0.012); }
    else if (role === 'Li') { poly([[0.16, U(-0.74)], [0.26, U(-0.72)], [0.26, U(-0.6)], [0.16, U(-0.62)]]); }
    else limb(-0.1, U(-0.7), 0.34, U(-0.65), 0.035);
  });
  c.restore();
}

function showTeam() {
  $d('zv').style.display = 'block';
  drawTeamView();
}

const ROLE_N = { L: 'LEAD', S: 'SOLDIER', Sc: 'SCIENTIST', Li: 'LINGUIST', Sn: 'SNIPER', R: 'RECON', Rf: 'RIFLEMAN', G: 'GUNNER', Gr: 'GRENADIER' };

function drawTeamView() {
  const cv = $d('tv');
  if (!cv || !G) return;
  const c = cv.getContext('2d');
  const W = cv.width;
  const H = cv.height;
  const th = G.th;
  const hz = 92;
  const hot = thermal;
  if (hot) {
    c.fillStyle = '#0a1013';
    c.fillRect(0, 0, W, H);
    const gg = c.createLinearGradient(0, hz, 0, H);
    gg.addColorStop(0, '#1a252b');
    gg.addColorStop(1, '#0d1519');
    c.fillStyle = gg;
    c.fillRect(0, hz, W, H - hz);
  } else {
    const sk = G.night ? ['#02040a', '#101a30'] : th.sky;
    const gr = G.night ? [mix(th.ground[0], '#02040a', 0.8), mix(th.ground[1], '#02040a', 0.85)] : th.ground;
    const sg = c.createLinearGradient(0, 0, 0, hz);
    sg.addColorStop(0, sk[0]);
    sg.addColorStop(1, sk[1]);
    c.fillStyle = sg;
    c.fillRect(0, 0, W, hz);
    const gg = c.createLinearGradient(0, hz, 0, H);
    gg.addColorStop(0, gr[0]);
    gg.addColorStop(1, gr[1]);
    c.fillStyle = gg;
    c.fillRect(0, hz, W, H - hz);
  }
  const tm = G.tm;
  const n = tm.roles.length;
  const wts = tm.roles.map((r, i) => G.hurtSet.has(i) ? 1.4 : 1);
  const tot = wts.reduce((a, b) => a + b, 0);
  const gy = 130;
  let acc = 0;
  let standing = 0;
  const med = G.hurtSet.size > 0 ? medicIdx() : -1;
  tm.roles.forEach((role, i) => {
    const w = W * wts[i] / tot;
    const cx = acc + w / 2;
    acc += w;
    const hurt = G.hurtSet.has(i);
    if (!hurt) standing++;
    c.fillStyle = 'rgba(0,0,0,0.35)';
    c.beginPath(); c.ellipse(cx, gy + 2, hurt ? 40 : 22, 5, 0, 0, 7); c.fill();
    const hh = hurt ? 88 : 106;
    drawFig(c, hurt ? cx - 0.47 * hh : cx - 0.07 * hh, gy, hh, role, hurt ? 'prone' : (i === med ? 'kneel' : 'stand'), hot ? 'hot' : 'opt', tm.col + 'bb');
    if (hurt) {
      c.fillStyle = '#ff4d4d';
      const px = cx - 0.47 * hh + 0.66 * hh;
      const py = gy - 0.11 * hh;
      c.fillRect(px - 2.5, py - 8, 5, 16);
      c.fillRect(px - 8, py - 2.5, 16, 5);
    }
    c.font = '9px monospace';
    c.textAlign = 'center';
    c.fillStyle = hurt ? '#ff6b6b' : '#cfeaf5';
    c.fillText(hurt ? 'INJURED' : (i === med ? 'MEDIC' : ROLE_N[role] || role), cx, H - 4);
  });
  c.textAlign = 'left';
  $d('zvt').textContent = 'ZOOM VIEW // ' + tm.n + ' // ' + standing + ' STANDING' + (G.hurtSet.size > 0 ? ', ' + G.hurtSet.size + ' INJURED' : ', NONE INJURED');
}

function drawTele(now) {
  const th = G.th;
  const fromGate = Math.hypot(G.cam.x - G.gate.x, G.cam.y - G.gate.y);
  const link = Math.max(18, Math.round(96 - fromGate / CELL * 6));
  const wh = Math.max(0, (G.clockEnd - now) / 1000);
  const cells = [
    ['TEMP', (th.temp + rnd(-0.4, 0.4) - (G.night ? 6 : 0)).toFixed(1) + ' C', ''],
    ['ATMOS O2', (th.o2 + rnd(-0.05, 0.05)).toFixed(1) + '%', th.o2 < 20 ? 'warn' : ''],
    ['PRESSURE', (th.pr + rnd(-0.003, 0.003)).toFixed(2) + ' ATM', ''],
    ['RADIATION', (th.rad + rnd(-0.005, 0.005)).toFixed(2) + ' mSv', th.rad > 0.15 ? 'warn' : ''],
    ['GRAVITY', th.g.toFixed(2) + ' G', ''],
    ['WIND', Math.round(rnd(4, 22)) + ' KPH', ''],
    ['ALTITUDE', G.alt.toFixed(0) + ' M', ''],
    ['SPEED', G.speed.toFixed(0) + ' M/S', ''],
    ['LINK', link + '%', link < 45 ? 'warn' : ''],
    ['FROM GATE', fromGate.toFixed(0) + ' M', ''],
    ['WORMHOLE', Math.floor(wh / 60) + ':' + String(Math.floor(wh % 60)).padStart(2, '0'), wh < 30 ? 'bad' : ''],
    ['TERRAIN', th.n + (G.night ? ' // NIGHT' : ' // DAY'), '']
  ];
  $d('tele').innerHTML = cells.map(x => '<div class="t"><div class="k">' + x[0] + '</div><div class="v ' + x[2] + '">' + x[1] + '</div></div>').join('');
  $d('sigbar').style.width = Math.round(G.str * 100) + '%';
  const rr = G.mode === 'recon' ? 'SITE RANGE' : (G.found ? 'TEAM LOCATED' : (haz === 'high' ? 'NO BEARING // STRENGTH ONLY' : 'BEARING ON COMPASS'));
  $d('rxs').textContent = rr + ' // ' + Math.round(G.str * 100) + '%';
  $d('rxs').className = G.found ? 'ok' : 'warn';
  if (G.mode === 'recon') {
    const dd = G.contacts.filter(x => x.kind === 'def');
    const st = G.contacts.filter(x => x.kind === 'struct');
    $d('rcon').innerHTML = '<div class="row"><span>Defenders tagged</span><b>' + dd.filter(x => x.tagged).length + ' / ' + dd.length + '</b></div><div class="row"><span>Structures tagged</span><b>' + st.filter(x => x.tagged).length + ' / ' + st.length + '</b></div><div class="row"><span>Exposure</span><b class="' + (G.expo > 0.5 ? 'bad' : '') + '">' + Math.round(G.expo * 100) + '%</b></div>';
  }
}

function resultHtml() {
  if (G.mode === 'recon') {
    const tot = G.contacts.length;
    const pct = G.tagged / tot;
    const b = pct >= 1 ? { id: 'FULL PICTURE', red: 15, cls: 'ok', extra: 'defender count and positions revealed' } : (pct >= 0.7 ? { id: 'GOOD', red: 10, cls: 'ok', extra: 'defender count revealed' } : (pct >= 0.4 ? { id: 'PARTIAL', red: 5, cls: 'warn', extra: 'none' } : { id: 'POOR', red: 0, cls: 'bad', extra: 'none' }));
    const red = G.spotted ? Math.floor(b.red / 2) : b.red;
    const title = G.spotted ? 'DRONE LOST // SPOTTED' : (G.linkLost ? 'WORMHOLE CLOSED // SURVEY ENDED' : 'SURVEY COMPLETE');
    return '<div class="result"><h2>' + title + '</h2><div class="row"><span>Contacts tagged</span><b class="' + b.cls + '">' + G.tagged + ' / ' + tot + ' // ' + b.id + '</b></div><div class="row"><span>Enemy strength estimate</span><span>-' + red + '%' + (G.spotted ? ' (halved, drone lost)' : '') + '</span></div><div class="row"><span>Intel</span><span>' + (G.spotted ? 'none' : b.extra) + '</span></div><div class="row"><span>Defenders alerted</span><b class="' + (G.spotted ? 'bad' : 'ok') + '">' + (G.spotted ? 'YES // ambush chance up' : 'NO') + '</b></div><div class="row"><span>Drone</span><span>' + (G.spotted ? 'lost' : 'recovered') + '</span></div></div>';
  }
  const g = G.guess;
  const dist = G.found ? 0 : (g ? Math.hypot(g.x - G.px, g.y - G.py) : 99999);
  const b = BANDS.find(x => dist <= x.max);
  const label = dist === 99999 ? 'NO FIX' : (G.found ? 'TARGET LOCKED' : Math.round(dist) + ' M OFF');
  return '<div class="result"><h2>CONTACT ' + (G.linkLost ? 'LOST // FIX AS MARKED' : 'ESTABLISHED') + '</h2><div class="row"><span>Position fix</span><b class="' + b.cls + '">' + b.id + ' // ' + label + '</b></div><div class="row"><span>Assist travel time</span><span>' + b.travel + '</span></div><div class="row"><span>Rescued team yield</span><span>' + b.yield + '</span></div><div class="row"><span>Assist intel</span><span>' + b.intel + '</span></div></div>';
}

function render() {
  const T = TIERS[tier];
  const rc = G.mode === 'recon';
  $d('sh').textContent = 'RADAR // SURVEY AREA ' + G.WS + ' M SQUARE // ' + (rc ? 'ASSAULT RECON // ' : '') + 'HAZARD ' + HAZ[haz].label;
  $d('stier').innerHTML = '<div class="row"><span>DRONE TIER ' + tier + (tier === 0 ? ' (BASIC)' : '') + '</span><span class="dim">THERMAL RANGE ' + Math.round((T.sight + 0.5) * CELL * HAZ[haz].haze) + ' M // ZOOM ' + T.zoom.toFixed(1) + 'x // ' + T.speed + ' M/S</span></div>';
  $d('srx').innerHTML = '<div class="row"><span>RECEIVER</span><b id="dr_rxs" class="warn"></b></div><div class="meter"><i id="dr_sigbar" style="width:0%"></i></div><div id="dr_rcon"></div>';
  $d('radar').className = G.markMode ? 'mk' : '';
  let s;
  if (rc) {
    s = '<div class="ctl"><button onclick="DRONE.confirmRecon()" ' + (G.done ? 'disabled' : '') + '>END SURVEY</button></div>';
    s += '<div class="note">The dashed red ring on the radar is the stronghold. Defenders are heat signatures, so thermal finds them from farther away. Structures are cold and only show in optical, so you have to get closer. Hold the reticle on a contact to tag it. Red wedges on the radar are what the defenders can see, and they appear once your sensors reach them.</div>';
    s += '<div class="note">An amber DEFENDER NEARBY warning and a slow tick sound when you close on a defender view. Staying inside a wedge builds exposure. Hovering low and slowly builds it slowly, and boosting or flying high builds it fast. At 100% the drone is shot down, the survey ends with what you tagged, and the defenders are alerted.</div>';
    s += '<div class="note">' + (haz === 'low' ? 'Low hazard: 5 defenders, 1 patrol, and the SITE marker points straight at the compound.' : (haz === 'med' ? 'Medium hazard: 7 defenders, 2 patrols, and the SITE marker is off by up to about 25 degrees.' : 'High hazard: 9 defenders, 3 patrols, no SITE marker, heavy haze.')) + (G.night ? ' Night: optical sees only a fraction of its day range, and defenders see about 25% less far. Thermal is unaffected.' : '') + '</div>';
  } else {
    s = '<div class="ctl"><button class="' + (G.markMode ? 'on' : '') + '" onclick="DRONE.toggleMark()" ' + (G.done || G.found || G.linkLost ? 'disabled' : '') + '>' + (G.markMode ? 'MARKING: CLICK THE RADAR' : 'PLACE FIX MARKER') + '</button><button onclick="DRONE.confirmFix()" ' + ((G.found || G.mark) && !G.done ? '' : 'disabled') + '>CONFIRM FIX</button></div>';
    s += '<div class="note">Fly with WASD. The dashed ring is how far this drone sees, the shaded area is what you have already covered, and there are no sectors. Follow the SIG marker on the compass and the signal strength bar, go thermal, zoom in, and hold the reticle on the heat signature until it locks.</div>';
    s += '<div class="note">' + (haz === 'low' ? 'Low hazard: the SIG marker points straight at the team.' : (haz === 'med' ? 'Medium hazard: the SIG marker can be off by up to about 25 degrees and drifts as you move, so two bearings from different spots cross near the team. There is haze.' : 'High hazard: no SIG marker and heavy haze. Only the signal strength reading rises as you close in, and it is noisy.')) + (G.night ? ' Night: optical sees only a fraction of its day range. Thermal is unaffected.' : '') + '</div>';
    s += '<div class="note">Fix is scored by distance: within 30 M Pinpoint, 80 M Good, 160 M Rough, further Poor. A locked target is always Pinpoint. If you cannot lock, place a marker on the radar. If the wormhole closes first, the link drops and you are scored on the marker you had placed, otherwise Poor.</div>';
  }
  if (G.done) s += resultHtml() + '<div class="ctl"><button onclick="DRONE.finish()">' + (rc ? 'FILE SURVEY' : 'CONTINUE') + '</button></div>';
  $d('sbody').innerHTML = s;
}

function beep(freq, dur, vol, type) {
  if (!snd || !snd.on) return;
  const o = snd.ctx.createOscillator();
  const g = snd.ctx.createGain();
  o.type = type || 'sine';
  o.frequency.value = freq;
  g.gain.setValueAtTime(vol, snd.ctx.currentTime);
  g.gain.exponentialRampToValueAtTime(0.0001, snd.ctx.currentTime + dur);
  o.connect(g);
  g.connect(snd.ctx.destination);
  o.start();
  o.stop(snd.ctx.currentTime + dur);
}

function sfxClick() { beep(900, 0.06, 0.05, 'square'); }
function sfxLock() { beep(660, 0.12, 0.08); setTimeout(() => beep(990, 0.25, 0.08), 120); }

function updateAudio(gliding, sp, locking) {
  if (!snd || !snd.on) return;
  const haze = { low: 0.01, med: 0.025, high: 0.05 }[haz];
  let st = haze + (G.found ? 0 : 0.01) + (gliding ? 0.03 * sp : 0);
  if (G.linkLost) st = 0.2;
  if (G.found) st = 0.004;
  snd.ng.gain.value = lowFx ? st * 0.5 : st;
  snd.bp.frequency.value = G.found ? 1400 : 2400;
  snd.rg.gain.value = G.linkLost ? 0 : (gliding ? 0.05 + 0.04 * sp : 0.02);
  snd.rot.frequency.value = 58 + (gliding ? 22 * sp : 0);
  if (locking && !G.found) {
    const nowT = performance.now();
    if (!snd.lt || nowT - snd.lt > 160) { snd.lt = nowT; beep(380 + lockP * 700, 0.06, 0.05); }
  }
  if (!G.done && !G.linkLost) {
    const nowP = performance.now();
    const warn = G.mode === 'recon' && G.expo > 0.05;
    const gap = warn ? 700 - G.expo * 550 : (G.found ? 1e9 : 1500 - G.str * 1350);
    if (!snd.pt || nowP - snd.pt > gap) {
      snd.pt = nowP;
      if (warn) beep(210, 0.08, 0.06, 'square'); else if (!G.found) beep(480 + G.str * 520, 0.05, 0.045, 'sine');
    }
  }
  if (G.mode === 'recon' && G.warn && !G.done && !G.linkLost) {
    const nw = performance.now();
    if (!snd.wt || nw - snd.wt > 800) { snd.wt = nw; beep(330, 0.07, 0.05, 'triangle'); }
  }
  if (Math.abs(zoom - lastZoom) > 0.01) {
    const nowT = performance.now();
    if (nowT - lastServo > 90) { lastServo = nowT; beep(zoom > lastZoom ? 520 : 440, 0.05, 0.03, 'triangle'); }
    lastZoom = zoom;
  }
}

function checkClock(now) {
  if (G.linkLost || G.done) return;
  if (now >= G.clockEnd) {
    G.linkLost = true;
    G.guess = G.found ? { x: G.px, y: G.py } : (G.mark || null);
    G.done = true;
    render();
  }
}

function loop(now) {
  if (!active) return;
  requestAnimationFrame(loop);
  if (!G) return;
  checkClock(now);
  step(now);
  drawFeed(now);
  drawRadar(now);
  if (!loop.last || now - loop.last > 250) { loop.last = now; drawTele(now); }
}

function medicIdx() {
  const h = [...G.hurtSet][0];
  const n = G.tm.roles.length;
  if (h === undefined) return -1;
  for (let k = h + 1; k < n; k++) if (!G.hurtSet.has(k)) return k;
  for (let k = h - 1; k >= 0; k--) if (!G.hurtSet.has(k)) return k;
  return -1;
}

function ensureAudio() {
  if (snd) return snd;
  try {
    if (typeof ac !== 'function' || !ac() || !BUS) return null;
    const ctx = AC;
    const out = BUS.fx;
    const len = ctx.sampleRate * 2;
    const buf = ctx.createBuffer(1, len, ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < len; i++) d[i] = Math.random() * 2 - 1;
    const ns = ctx.createBufferSource();
    ns.buffer = buf;
    ns.loop = true;
    const bp = ctx.createBiquadFilter();
    bp.type = 'bandpass';
    bp.frequency.value = 2400;
    bp.Q.value = 0.6;
    const ng = ctx.createGain();
    ng.gain.value = 0;
    ns.connect(bp);
    bp.connect(ng);
    ng.connect(out);
    ns.start();
    const rot = ctx.createOscillator();
    rot.type = 'sawtooth';
    rot.frequency.value = 62;
    const lfo = ctx.createOscillator();
    lfo.frequency.value = 14;
    const lg = ctx.createGain();
    lg.gain.value = 0.5;
    const rg = ctx.createGain();
    rg.gain.value = 0;
    const lp = ctx.createBiquadFilter();
    lp.type = 'lowpass';
    lp.frequency.value = 420;
    lfo.connect(lg);
    lg.connect(rg.gain);
    rot.connect(lp);
    lp.connect(rg);
    rg.connect(out);
    rot.start();
    lfo.start();
    snd = { ctx, out, ng, bp, rg, rot, lfo, ns, on: true };
    return snd;
  } catch (e) { return null; }
}

function stopAudio() {
  if (!snd) return;
  try {
    snd.ng.gain.value = 0;
    snd.rg.gain.value = 0;
    snd.ns.stop();
    snd.rot.stop();
    snd.lfo.stop();
    snd.ng.disconnect();
    snd.rg.disconnect();
  } catch (e) {}
  snd = null;
}

function beep(freq, dur, vol, type) {
  if (!snd || !snd.on) return;
  const o = snd.ctx.createOscillator();
  const g = snd.ctx.createGain();
  o.type = type || 'sine';
  o.frequency.value = freq;
  g.gain.setValueAtTime(vol, snd.ctx.currentTime);
  g.gain.exponentialRampToValueAtTime(0.0001, snd.ctx.currentTime + dur);
  o.connect(g);
  g.connect(snd.out);
  o.start();
  o.stop(snd.ctx.currentTime + dur);
}

function summary() {
  if (G.mode === 'recon') return { mode: 'recon', tagged: G.tagged, total: G.contacts.length, spotted: G.spotted, linkLost: G.linkLost };
  const g = G.guess;
  const dist = G.found ? 0 : (g ? Math.hypot(g.x - G.px, g.y - G.py) : 99999);
  return { mode: 'rescue', dist, found: G.found, linkLost: G.linkLost, marked: !!g };
}

function stop() {
  active = false;
  for (const k in keys) keys[k] = false;
  drag = null;
  try { if (document.pointerLockElement === feed) document.exitPointerLock(); } catch (e) {}
  stopAudio();
  document.getElementById('drone').hidden = true;
}

function start(c) {
  cfg = c;
  haz = c.hazard;
  tier = c.tier;
  modeSel = c.mode;
  thermal = false;
  $d('bmode').textContent = 'OPTICAL';
  $d('bmode').classList.remove('on');
  $d('hint').style.display = '';
  $d('title').textContent = c.title;
  $d('sub').textContent = c.sub;
  document.getElementById('drone').hidden = false;
  active = true;
  newGame();
  ensureAudio();
  requestAnimationFrame(loop);
}

function finish() {
  if (!active || !G || !G.done) return;
  const s = summary();
  const f = cfg.onDone;
  stop();
  if (f) f(s);
}

function abort() {
  if (!active) return;
  const f = cfg.onAbort;
  stop();
  if (f) f();
}

function linkLost() {
  if (!active || !G || G.done) return;
  G.linkLost = true;
  G.guess = G.found ? { x: G.px, y: G.py } : (G.mark || null);
  G.done = true;
  render();
}

function init() {
  feed = $d('feed');
  feed.addEventListener('pointerdown', e => { if (e.target.closest('.hint') || e.target.closest('.zv')) return; drag = { x: e.clientX, y: e.clientY }; feed.classList.add('drag'); feed.setPointerCapture(e.pointerId); });
  feed.addEventListener('pointermove', e => {
    if (!drag) return;
    const dx = e.clientX - drag.x;
    const dy = e.clientY - drag.y;
    drag = { x: e.clientX, y: e.clientY };
    yaw = wrapA(yaw + dx * 0.0042 / zoom);
    pitch = Math.max(-0.45, Math.min(0.55, pitch + dy * 0.0035 / zoom));
  });
  feed.addEventListener('pointerup', () => { drag = null; feed.classList.remove('drag'); });
  feed.addEventListener('pointercancel', () => { drag = null; feed.classList.remove('drag'); });
  feed.addEventListener('wheel', e => { e.preventDefault(); zoom = Math.max(1, Math.min(TIERS[tier].zoom, zoom * (e.deltaY < 0 ? 1.12 : 1 / 1.12))); }, { passive: false });
  window.addEventListener('keydown', e => {
    if (!active) return;
    e.stopImmediatePropagation();
    const k = e.key.length === 1 ? e.key.toLowerCase() : e.key;
    if (k.startsWith('Arrow') || k === ' ' || k === 'Tab') e.preventDefault();
    keys[k] = true;
    if ('wasdqe'.indexOf(k) >= 0 || k.startsWith('Arrow')) hideHint();
    if (k === 't' && !e.repeat) toggleMode();
  }, true);
  window.addEventListener('keyup', e => {
    if (!active) return;
    e.stopImmediatePropagation();
    keys[e.key.length === 1 ? e.key.toLowerCase() : e.key] = false;
  }, true);
  window.addEventListener('blur', () => { for (const k in keys) keys[k] = false; });
  document.addEventListener('pointerlockchange', () => { $d('bml').classList.toggle('on', document.pointerLockElement === feed); });
  document.addEventListener('mousemove', e => {
    if (!active || document.pointerLockElement !== feed) return;
    yaw = wrapA(yaw + e.movementX * 0.0028 / zoom);
    pitch = Math.max(-0.45, Math.min(0.55, pitch - e.movementY * 0.0025 / zoom));
  });
  $d('radar').addEventListener('pointerdown', e => {
    if (!active || !G || !G.markMode || G.done || G.found || G.linkLost) return;
    const r = e.currentTarget.getBoundingClientRect();
    G.mark = { x: (e.clientX - r.left) / r.width * G.WS, y: (e.clientY - r.top) / r.height * G.WS };
    G.markMode = false;
    render();
  });
}

init();

window.DRONE = {
  start, stop, finish, abort, linkLost, hideHint, toggleMode, mouseLook, toggleMark, confirmFix, confirmRecon,
  isActive: () => active,
  themes: THEMES.length
};
})();
