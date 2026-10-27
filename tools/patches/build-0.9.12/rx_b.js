const RXC = { a: 'var(--accent)', g: 'var(--glow, #bff)', ok: 'var(--ok, #5dffa0)', bad: 'var(--danger, #ff5a5a)', dim: 'var(--dim, #6a8796)', warn: 'var(--warn, #ffb84a)', st: 'var(--steel, #4a6a7a)', bg: '#04101a' };
function rxT(x, y, txt, col, size, anchor, extra) {
  return `<text x="${x}" y="${y}" style="fill:${col || RXC.a};font-size:${size || 13}px;text-anchor:${anchor || 'start'};font-family:inherit;letter-spacing:.06em" ${extra || ''}>${txt}</text>`;
}
function rxR(x, y, w, h, fill, stroke, extra) {
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="3" style="fill:${fill || 'none'};stroke:${stroke || 'none'};stroke-width:2${(extra || '').includes('onpointerdown') ? ';cursor:pointer' : ''}" ${extra || ''}/>`;
}
function rxRand(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
function rxAdj(d) {
  const st = (RXG.shift ? 8 : 2) * d;
  rxKnobSet(RXG.sel, RXG.kn[RXG.sel] + st);
}

// ---------- 1. Conduit sudoku ----------
RX_INIT.grid = () => ({ g: rxGenGrid(), cur: 0 });
RX_BTN.grid = b => {
  const p = RXG.p;
  const n = p.g.n;
  let c = p.cur % n;
  let r = Math.floor(p.cur / n);
  if (b === 'left') c = (c + n - 1) % n;
  else if (b === 'right') c = (c + 1) % n;
  else if (b === 'up') r = (r + n - 1) % n;
  else if (b === 'down') r = (r + 1) % n;
  else if (b === 'sel') { rxGridSet((p.g.cells[p.cur] + 1) % (RX_GRID_MAX + 1)); return; }
  else if (b === 'alt') { rxGridSet(0); return; }
  p.cur = r * n + c;
};
RX_NUM.grid = n => rxGridSet(n);
function rxGridSet(v) {
  const p = RXG.p;
  if (p.g.fixed[p.cur]) { sfx.fail(); return; }
  p.g.cells[p.cur] = v;
  sfx.tick();
  if (rxGridCheck(p.g).solved) rxStageDone();
}
function rxGridPick(k) {
  if (!RXG || RXG.k !== 'grid' || RXG.trans || RXG.done) return;
  RXG.p.cur = k;
  rxDraw();
}
RX_DRAW.grid = () => {
  const p = RXG.p;
  const g = p.g;
  const c = rxGridCheck(g);
  const cs = 60;
  const ox = 130;
  const oy = 60;
  let h = '';
  for (let i = 0; i < g.n; i++) {
    for (let j = 0; j < g.n; j++) {
      const k = i * g.n + j;
      const x = ox + j * (cs + 4);
      const y = oy + i * (cs + 4);
      const fill = g.fixed[k] ? 'rgba(127,251,255,.14)' : 'rgba(0,0,0,.35)';
      const stroke = c.bad.has(k) ? RXC.bad : (p.cur === k ? RXC.g : RXC.st);
      h += rxR(x, y, cs, cs, fill, stroke, `onpointerdown="rxGridPick(${k})"`);
      if (p.cur === k) h += rxR(x - 3, y - 3, cs + 6, cs + 6, 'none', RXC.a);
      if (g.cells[k]) h += rxT(x + cs / 2, y + 41, g.cells[k], c.bad.has(k) ? RXC.bad : (g.fixed[k] ? RXC.g : RXC.a), 30, 'middle', 'pointer-events="none"');
    }
    h += rxT(ox + g.n * (cs + 4) + 8, oy + i * (cs + 4) + 36, g['rsum' + i] + '/' + g.rs[i], c.rowOk[i] ? RXC.ok : RXC.dim, 15);
  }
  for (let j = 0; j < g.n; j++) h += rxT(ox + j * (cs + 4) + cs / 2, oy + g.n * (cs + 4) + 20, g['csum' + j] + '/' + g.cs[j], c.colOk[j] ? RXC.ok : RXC.dim, 15, 'middle');
  return h;
};
RX_HELP.grid = ['SET EVERY CONDUIT TO 1-5.', 'NO VALUE REPEATS IN A ROW OR COLUMN.', 'EACH ROW AND COLUMN MUST ADD UP', 'TO ITS TARGET.', 'ARROWS MOVE // NUMBER KEYS SET', 'SEL CYCLES // ALT CLEARS', 'BRIGHT CONDUITS ARE LOCKED.'];

// ---------- 2. Power balance (three knobs) ----------
function rxEff(i) { return RXG.kn[i] + 0.2 * (RXG.kn[(i + 2) % 3] - 50); }
RX_INIT.knobs = () => {
  const sol = [rxRand(25, 75), rxRand(25, 75), rxRand(25, 75)];
  RXG.kn = [rxRand(5, 95), rxRand(5, 95), rxRand(5, 95)];
  const tgt = sol.map((v, i) => v + 0.2 * (sol[(i + 2) % 3] - 50));
  RXG.hold = 0;
  return { tgt };
};
RX_TICK.knobs = () => {
  const p = RXG.p;
  const ok = p.tgt.every((t, i) => Math.abs(rxEff(i) - t) <= 3);
  RXG.hold = ok ? RXG.hold + 1 : 0;
  if (RXG.hold >= 15) rxStageDone();
};
RX_BTN.knobs = b => {
  if (b === 'left') RXG.sel = (RXG.sel + 2) % 3;
  else if (b === 'right' || b === 'sel') RXG.sel = (RXG.sel + 1) % 3;
  else if (b === 'up') rxAdj(1);
  else if (b === 'down') rxAdj(-1);
};
RX_NUM.knobs = n => { if (n <= 3) RXG.sel = n - 1; };
RX_DRAW.knobs = () => {
  const p = RXG.p;
  const nm = RX_USEKN.knobs;
  let h = '';
  for (let i = 0; i < 3; i++) {
    const x = 90 + i * 150;
    const top = 60;
    const ht = 220;
    const eff = Math.max(0, Math.min(100, rxEff(i)));
    const ok = Math.abs(rxEff(i) - p.tgt[i]) <= 3;
    const yOf = v => top + ht - v / 100 * ht;
    h += rxR(x, top, 50, ht, 'rgba(0,0,0,.4)', RXG.sel === i ? RXC.g : RXC.st);
    h += rxR(x + 1, yOf(p.tgt[i] + 3), 48, (6 / 100) * ht, 'rgba(93,255,160,.28)', RXC.ok);
    h += rxR(x + 8, yOf(eff), 34, top + ht - yOf(eff), ok ? 'rgba(93,255,160,.55)' : 'rgba(127,251,255,.4)', 'none');
    h += `<path d="M${x - 8} ${yOf(eff)} l10 -6 v12 z" style="fill:${ok ? RXC.ok : RXC.a}"/>`;
    h += rxT(x + 25, top + ht + 24, nm[i], RXG.sel === i ? RXC.g : RXC.a, 14, 'middle');
    h += rxT(x + 25, top + ht + 42, Math.round(rxEff(i)) + ' / ' + Math.round(p.tgt[i]), ok ? RXC.ok : RXC.dim, 13, 'middle');
  }
  h += rxT(530, 120, 'HOLD', RXC.dim, 12, 'end');
  h += rxR(520, 130, 14, 150, 'none', RXC.st);
  h += rxR(520, 280 - 150 * RXG.hold / 15, 14, 150 * RXG.hold / 15, RXC.ok, 'none');
  return h;
};
RX_HELP.knobs = ['TURN THE THREE KNOBS TO MATCH THE GREEN BANDS.', 'EACH OUTPUT IS ALSO NUDGED BY THE', 'KNOB BEFORE IT (LAB BY GATE, SHLD BY LAB,', 'GATE BY SHLD).', 'HOLD ALL THREE IN BAND FOR A MOMENT.', 'DRAG OR SCROLL A KNOB // ARROWS: LEFT-RIGHT', 'PICK A KNOB, UP-DOWN TURNS IT.'];

// ---------- 3. Phase match ----------
RX_INIT.phase = () => {
  const tgt = [rxRand(20, 85), rxRand(20, 85), rxRand(10, 90)];
  RXG.kn = tgt.map(t => { let v; do { v = rxRand(5, 95); } while (Math.abs(v - t) < 20); return v; });
  RXG.hold = 0;
  return { tgt, tol: [4, 4, 5] };
};
function rxPhaseLamps() {
  const p = RXG.p;
  return p.tgt.map((t, i) => Math.abs(RXG.kn[i] - t) <= p.tol[i]);
}
RX_TICK.phase = () => {
  RXG.hold = rxPhaseLamps().every(Boolean) ? RXG.hold + 1 : 0;
  if (RXG.hold >= 15) rxStageDone();
};
RX_BTN.phase = RX_BTN.knobs;
RX_NUM.phase = RX_NUM.knobs;
function rxWave(k, x0, w, cy) {
  const amp = 14 + k[0] * 0.7;
  const f = 1 + k[1] * 0.03;
  const ph = k[2] / 100 * Math.PI * 2;
  let d = '';
  for (let x = 0; x <= w; x += 4) {
    const y = cy - amp * Math.sin(x / w * f * Math.PI * 2 + ph);
    d += (x ? 'L' : 'M') + (x0 + x) + ' ' + y.toFixed(1);
  }
  return d;
}
RX_DRAW.phase = () => {
  const p = RXG.p;
  const lamps = rxPhaseLamps();
  let h = rxR(40, 56, 480, 200, 'rgba(0,0,0,.4)', RXC.st);
  for (let i = 1; i < 6; i++) h += `<line x1="${40 + i * 80}" y1="56" x2="${40 + i * 80}" y2="256" style="stroke:${RXC.st};opacity:.3"/>`;
  h += `<line x1="40" y1="156" x2="520" y2="156" style="stroke:${RXC.st};opacity:.4"/>`;
  h += `<path d="${rxWave(p.tgt, 40, 480, 156)}" style="fill:none;stroke:${RXC.warn};stroke-width:2;stroke-dasharray:5 4;opacity:.8"/>`;
  h += `<path d="${rxWave(RXG.kn, 40, 480, 156)}" style="fill:none;stroke:${lamps.every(Boolean) ? RXC.ok : RXC.a};stroke-width:3"/>`;
  const nm = RX_USEKN.phase;
  for (let i = 0; i < 3; i++) {
    const x = 100 + i * 140;
    h += `<circle cx="${x - 40}" cy="292" r="8" style="fill:${lamps[i] ? RXC.ok : RXC.bad};opacity:${lamps[i] ? 1 : .6}"/>`;
    h += rxT(x - 24, 297, nm[i] + ' ' + (RXG.sel === i ? '<' : ''), RXG.sel === i ? RXC.g : RXC.a, 14);
  }
  h += rxR(40, 322, 480, 12, 'none', RXC.st);
  h += rxR(40, 322, 480 * RXG.hold / 15, 12, RXC.ok, 'none');
  h += rxT(40, 352, 'MATCH THE DASHED SIGNAL', RXC.dim, 12);
  return h;
};
RX_HELP.phase = ['MATCH THE BRIGHT WAVE TO THE DASHED ONE.', 'AMP SETS HEIGHT, FRQ SETS HOW MANY WAVES,', 'PHS SLIDES THE WAVE SIDEWAYS.', 'ALL THREE LAMPS GREEN, THEN HOLD STEADY.', 'DRAG OR SCROLL A KNOB // ARROWS: LEFT-RIGHT', 'PICK A KNOB, UP-DOWN TURNS IT.'];

// ---------- 4. Pipe routing ----------
const RX_PW = 5;
const RX_PH = 4;
function rxRot(m, d) { return d > 0 ? (((m << 1) | (m >> 3)) & 15) : (((m >> 1) | ((m & 1) << 3)) & 15); }
function rxPipePower(p) {
  const pw = new Set();
  const s = p.rs * RX_PW;
  if (!(p.m[s] & 8)) return pw;
  pw.add(s);
  const q = [s];
  while (q.length) {
    const i = q.pop();
    const c = i % RX_PW;
    const r = (i - c) / RX_PW;
    const mk = p.m[i];
    const nb = [];
    if ((mk & 1) && r > 0) nb.push([i - RX_PW, 4]);
    if ((mk & 2) && c < RX_PW - 1) nb.push([i + 1, 8]);
    if ((mk & 4) && r < RX_PH - 1) nb.push([i + RX_PW, 1]);
    if ((mk & 8) && c > 0) nb.push([i - 1, 2]);
    nb.forEach(([j, need]) => { if ((p.m[j] & need) && !pw.has(j)) { pw.add(j); q.push(j); } });
  }
  return pw;
}
function rxPipeSolved(p) {
  const pw = rxPipePower(p);
  return p.outs.every(ro => { const i = ro * RX_PW + RX_PW - 1; return pw.has(i) && (p.m[i] & 2); });
}
function rxPipeGen() {
  for (let tries = 0; tries < 200; tries++) {
    const rs = rxRand(0, RX_PH - 1);
    const outs = rxShuffle([0, 1, 2, 3]).slice(0, 3).sort((a, b) => a - b);
    const m = new Array(RX_PW * RX_PH).fill(0);
    let ok = true;
    for (const ro of outs) {
      let c = 0;
      let r = rs;
      const vis = new Set([r * RX_PW + c]);
      let guard = 0;
      while (!(c === RX_PW - 1 && r === ro) && guard++ < 40) {
        const opts = [];
        if (c < RX_PW - 1) opts.push([1, 0], [1, 0], [1, 0]);
        if (r > 0 && !(c === RX_PW - 1 && ro > r)) opts.push([0, -1]);
        if (r < RX_PH - 1 && !(c === RX_PW - 1 && ro < r)) opts.push([0, 1]);
        const cand = opts.filter(([dc, dr]) => !vis.has((r + dr) * RX_PW + c + dc));
        if (!cand.length) { ok = false; break; }
        const [dc, dr] = cand[Math.floor(Math.random() * cand.length)];
        const a = r * RX_PW + c;
        const b = (r + dr) * RX_PW + c + dc;
        m[a] |= dc === 1 ? 2 : (dr === -1 ? 1 : 4);
        m[b] |= dc === 1 ? 8 : (dr === -1 ? 4 : 1);
        vis.add(b);
        r += dr;
        c += dc;
      }
      if (!ok || !(c === RX_PW - 1 && r === ro)) { ok = false; break; }
    }
    if (!ok) continue;
    m[rs * RX_PW] |= 8;
    outs.forEach(ro => { m[ro * RX_PW + RX_PW - 1] |= 2; });
    const shapes = [1, 5, 3, 7];
    for (let i = 0; i < m.length; i++) if (!m[i]) m[i] = shapes[rxRand(0, 3)];
    const sol = m.slice();
    for (let i = 0; i < m.length; i++) for (let t = rxRand(0, 3); t > 0; t--) m[i] = rxRot(m[i], 1);
    const p = { m, rs, outs, cur: rs * RX_PW, sol };
    if (!rxPipeSolved(p)) return p;
  }
  return { m: new Array(RX_PW * RX_PH).fill(5), rs: 0, outs: [0, 1, 2], cur: 0 };
}
RX_INIT.pipe = () => rxPipeGen();
function rxPipeRot(d) {
  const p = RXG.p;
  p.m[p.cur] = rxRot(p.m[p.cur], d);
  sfx.tick();
  if (rxPipeSolved(p)) rxStageDone();
}
RX_BTN.pipe = b => {
  const p = RXG.p;
  let c = p.cur % RX_PW;
  let r = Math.floor(p.cur / RX_PW);
  if (b === 'left') c = Math.max(0, c - 1);
  else if (b === 'right') c = Math.min(RX_PW - 1, c + 1);
  else if (b === 'up') r = Math.max(0, r - 1);
  else if (b === 'down') r = Math.min(RX_PH - 1, r + 1);
  else if (b === 'sel') { rxPipeRot(1); return; }
  else if (b === 'alt') { rxPipeRot(-1); return; }
  p.cur = r * RX_PW + c;
};
RX_NUM.pipe = () => {};
function rxPipeTap(k) {
  if (!RXG || RXG.k !== 'pipe' || RXG.trans || RXG.done || RXG.info) return;
  RXG.p.cur = k;
  rxPipeRot(1);
  if (RXG) rxDraw();
}
RX_DRAW.pipe = () => {
  const p = RXG.p;
  const pw = rxPipePower(p);
  const ts = 78;
  const ox = 90;
  const oy = 46;
  const mid = ts / 2;
  const dirs = [[1, mid, 0, 0, -mid], [2, mid, 0, mid, 0], [4, mid, 0, 0, mid], [8, mid, 0, -mid, 0]];
  let h = '';
  for (let i = 0; i < p.m.length; i++) {
    const c = i % RX_PW;
    const r = (i - c) / RX_PW;
    const x = ox + c * ts;
    const y = oy + r * ts;
    const on = pw.has(i);
    h += rxR(x + 1, y + 1, ts - 2, ts - 2, 'rgba(0,0,0,.35)', p.cur === i ? RXC.g : RXC.st, `onpointerdown="rxPipeTap(${i})"`);
    const col = on ? RXC.g : RXC.dim;
    const cx = x + mid;
    const cy = y + mid;
    let n = 0;
    for (const [bit, , , dx, dy] of dirs) {
      if (p.m[i] & bit) {
        n++;
        const ex = bit === 2 ? mid : (bit === 8 ? -mid : 0);
        const ey = bit === 4 ? mid : (bit === 1 ? -mid : 0);
        h += `<line x1="${cx}" y1="${cy}" x2="${cx + ex}" y2="${cy + ey}" style="stroke:${col};stroke-width:10;stroke-linecap:butt;pointer-events:none"/>`;
      }
    }
    h += `<circle cx="${cx}" cy="${cy}" r="${n === 1 ? 9 : 7}" style="fill:${col};pointer-events:none"/>`;
    if (p.cur === i) h += rxR(x - 2, y - 2, ts + 4, ts + 4, 'none', RXC.a);
  }
  const sy = oy + p.rs * ts + mid;
  h += `<line x1="46" y1="${sy}" x2="${ox}" y2="${sy}" style="stroke:${RXC.g};stroke-width:10"/>`;
  h += rxR(14, sy - 22, 34, 44, 'rgba(127,251,255,.18)', RXC.a);
  h += rxT(31, sy + 4, 'PWR', RXC.g, 11, 'middle');
  const nm = ['GATE', 'LAB', 'SHLD'];
  p.outs.forEach((ro, k) => {
    const i = ro * RX_PW + RX_PW - 1;
    const on = pw.has(i) && (p.m[i] & 2);
    const y = oy + ro * ts + mid;
    h += `<line x1="${ox + RX_PW * ts}" y1="${y}" x2="${ox + RX_PW * ts + 18}" y2="${y}" style="stroke:${on ? RXC.ok : RXC.dim};stroke-width:10"/>`;
    h += rxR(ox + RX_PW * ts + 18, y - 16, 44, 32, on ? 'rgba(93,255,160,.2)' : 'rgba(0,0,0,.4)', on ? RXC.ok : RXC.st);
    h += rxT(ox + RX_PW * ts + 40, y + 4, nm[k], on ? RXC.ok : RXC.dim, 11, 'middle');
  });
  return h;
};
RX_HELP.pipe = ['ROTATE THE TILES SO POWER REACHES', 'ALL THREE OUTPUTS: GATE, LAB, SHIELDS.', 'POWER FLOWS FROM THE PWR BLOCK ON THE LEFT.', 'ARROWS MOVE THE CURSOR.', 'SEL ROTATES CLOCKWISE, ALT COUNTER-CLOCKWISE.', 'TAP A TILE TO ROTATE IT.', 'LIT PIPES ARE CARRYING POWER.'];

// ---------- 5. Breaker sequence ----------
RX_INIT.breaker = () => {
  const L = RXG.evt ? 4 : 5;
  const seq = [];
  while (seq.length < L) {
    const v = rxRand(0, 4);
    if (seq.length && seq[seq.length - 1] === v) continue;
    seq.push(v);
  }
  return { seq, mode: 'show', t: 0, inp: 0, err: 0, cur: 0, fl: -1, flt: 0 };
};
function rxBreakerLit(p) {
  if (p.mode !== 'show') return -1;
  const i = Math.floor((p.t - 8) / 7);
  if (p.t < 8 || i >= p.seq.length) return -1;
  return (p.t - 8) % 7 < 5 ? p.seq[i] : -1;
}
RX_TICK.breaker = () => {
  const p = RXG.p;
  if (p.flt > 0) p.flt--;
  if (p.mode === 'show') {
    p.t++;
    if (p.t >= 8 + p.seq.length * 7 + 3) { p.mode = 'input'; p.inp = 0; }
  } else if (p.mode === 'err') {
    p.err--;
    if (p.err <= 0) { p.mode = 'show'; p.t = 0; p.inp = 0; }
  }
};
function rxBreaker(n) {
  const p = RXG.p;
  if (p.mode !== 'input') return;
  p.fl = n - 1;
  p.flt = 3;
  if (n - 1 === p.seq[p.inp]) {
    p.inp++;
    sfx.tick();
    if (p.inp >= p.seq.length) rxStageDone();
  } else {
    p.mode = 'err';
    p.err = 12;
    p.inp = 0;
    sfx.fail();
  }
}
RX_NUM.breaker = n => rxBreaker(n);
RX_BTN.breaker = b => {
  const p = RXG.p;
  if (b === 'left') p.cur = (p.cur + 4) % 5;
  else if (b === 'right') p.cur = (p.cur + 1) % 5;
  else if (b === 'sel') rxBreaker(p.cur + 1);
};
function rxBreakerTap(n) {
  if (!RXG || RXG.k !== 'breaker' || RXG.trans || RXG.done || RXG.info) return;
  rxBreaker(n);
  rxDraw();
}
RX_DRAW.breaker = () => {
  const p = RXG.p;
  const lit = rxBreakerLit(p);
  let h = '';
  for (let i = 0; i < 5; i++) {
    const x = 50 + i * 94;
    const on = lit === i || (p.flt > 0 && p.fl === i);
    const bad = p.mode === 'err';
    const col = bad ? RXC.bad : (on ? RXC.ok : RXC.dim);
    h += `<circle cx="${x + 30}" cy="100" r="16" style="fill:${on || bad ? col : 'rgba(0,0,0,.5)'};stroke:${col};stroke-width:2;opacity:${bad ? .8 : 1}"/>`;
    h += rxR(x, 140, 60, 120, 'rgba(0,0,0,.45)', p.cur === i ? RXC.g : RXC.st, `onpointerdown="rxBreakerTap(${i + 1})"`);
    h += rxR(x + 12, on ? 150 : 200, 36, 50, on ? 'rgba(93,255,160,.5)' : 'rgba(127,251,255,.2)', RXC.a, 'pointer-events="none"');
    h += rxT(x + 30, 284, i + 1, p.cur === i ? RXC.g : RXC.a, 18, 'middle');
  }
  const msg = p.mode === 'show' ? 'WATCH THE SEQUENCE' : (p.mode === 'err' ? 'WRONG // REPLAYING' : 'REPEAT IT // BREAKER ' + (p.inp + 1) + ' OF ' + p.seq.length);
  h += rxT(280, 328, msg, p.mode === 'err' ? RXC.bad : RXC.g, 15, 'middle');
  for (let i = 0; i < p.seq.length; i++) h += `<circle cx="${280 - (p.seq.length - 1) * 10 + i * 20}" cy="346" r="5" style="fill:${i < p.inp ? RXC.ok : 'none'};stroke:${RXC.dim}"/>`;
  return h;
};
RX_HELP.breaker = ['WATCH THE BREAKERS LIGHT UP IN ORDER.', 'THEN FLIP THEM IN THE SAME ORDER.', 'KEYS 1-5 FLIP THE BREAKERS, OR TAP THEM.', 'A MISTAKE REPLAYS THE SAME SEQUENCE.', 'LEFT-RIGHT AND SEL ALSO WORK.'];

// ---------- 6. Load shedding ----------
const RX_SHED = ['LIFE SUPPORT', 'GATE CORE', 'LABORATORY', 'DEFENCE GRID', 'SENSOR ARRAY', 'COMMS RELAY', 'LIGHTING'];
RX_INIT.shed = () => {
  for (;;) {
    const load = RX_SHED.map((_, i) => (i < 2 ? rxRand(3, 5) : rxRand(2, 9)));
    const others = rxShuffle([2, 3, 4, 5, 6]);
    const keep = others.slice(0, rxRand(1, 3));
    const cap = load[0] + load[1] + keep.reduce((a, i) => a + load[i], 0);
    const all = load.reduce((a, b) => a + b, 0);
    if (all >= cap + 4) return { load, cap, on: RX_SHED.map(() => true), cur: 2 };
  }
};
function rxShedTotal(p) { return p.load.reduce((a, v, i) => a + (p.on[i] ? v : 0), 0); }
function rxShedToggle(i) {
  const p = RXG.p;
  p.cur = i;
  if (i < 2) { sfx.fail(); return; }
  p.on[i] = !p.on[i];
  sfx.tick();
  const t = rxShedTotal(p);
  if (t <= p.cap && t >= p.cap - 2) rxStageDone();
}
RX_BTN.shed = b => {
  const p = RXG.p;
  if (b === 'up') p.cur = (p.cur + 6) % 7;
  else if (b === 'down') p.cur = (p.cur + 1) % 7;
  else if (b === 'sel') rxShedToggle(p.cur);
};
RX_NUM.shed = n => rxShedToggle(n + 1);
function rxShedTap(i) {
  if (!RXG || RXG.k !== 'shed' || RXG.trans || RXG.done || RXG.info) return;
  rxShedToggle(i);
  if (RXG) rxDraw();
}
RX_DRAW.shed = () => {
  const p = RXG.p;
  const tot = rxShedTotal(p);
  let h = '';
  for (let i = 0; i < 7; i++) {
    const y = 52 + i * 40;
    const on = p.on[i];
    h += rxR(30, y, 340, 34, 'rgba(0,0,0,.35)', p.cur === i ? RXC.g : RXC.st, `onpointerdown="rxShedTap(${i})"`);
    h += rxT(42, y + 22, (i < 2 ? '■ ' : '') + RX_SHED[i], on ? RXC.a : RXC.dim, 14, 'start', 'pointer-events="none"');
    h += rxR(200, y + 10, p.load[i] * 11, 14, on ? 'rgba(127,251,255,.45)' : 'rgba(127,251,255,.1)', 'none', 'pointer-events="none"');
    h += rxT(352, y + 22, i < 2 ? 'LOCKED' : (on ? 'ON' : 'OFF'), i < 2 ? RXC.warn : (on ? RXC.ok : RXC.dim), 12, 'end', 'pointer-events="none"');
  }
  const gx = 430;
  const gt = 56;
  const gh = 270;
  const mx = p.load.reduce((a, b) => a + b, 0);
  const yOf = v => gt + gh - v / mx * gh;
  h += rxR(gx, gt, 44, gh, 'rgba(0,0,0,.4)', RXC.st);
  h += rxR(gx + 1, yOf(p.cap), 42, yOf(p.cap - 2) - yOf(p.cap), 'rgba(93,255,160,.3)', RXC.ok);
  const okc = tot > p.cap ? RXC.bad : (tot >= p.cap - 2 ? RXC.ok : RXC.warn);
  h += rxR(gx + 8, yOf(tot), 28, gt + gh - yOf(tot), okc, 'none', 'opacity=".55"');
  h += rxT(gx + 22, gt + gh + 22, 'LOAD ' + tot, okc, 14, 'middle');
  h += rxT(gx + 22, gt - 8, 'CAP ' + p.cap, RXC.ok, 13, 'middle');
  h += rxT(520, 150, 'FIT', RXC.dim, 11, 'middle') + rxT(520, 164, 'IN THE', RXC.dim, 11, 'middle') + rxT(520, 178, 'GREEN', RXC.dim, 11, 'middle');
  return h;
};
RX_HELP.shed = ['THE REACTOR CANNOT CARRY EVERY SYSTEM.', 'SWITCH SYSTEMS OFF UNTIL THE LOAD SITS IN', 'THE GREEN BAND JUST UNDER THE CAP.', 'LIFE SUPPORT AND THE GATE CORE ARE LOCKED ON.', 'UP-DOWN MOVE // SEL TOGGLES // KEYS 1-5', 'TOGGLE THE FIVE SWITCHABLE SYSTEMS.'];
