const RX_PAIRS = {
  evt: ['grid', 'breaker'],
  t4: ['knobs', 'shed'],
  t6: ['pipe', 'breaker'],
  t7: ['knobs', 'phase'],
  zpm: ['pipe', 'phase'],
  off: ['grid']
};
const RX_NAMES = { grid: 'CONDUIT BALANCE', knobs: 'POWER BALANCE', pipe: 'PIPE ROUTING', breaker: 'BREAKER SEQUENCE', phase: 'PHASE MATCH', shed: 'LOAD SHEDDING' };
const RX_USEKN = { knobs: ['GATE', 'LAB', 'SHLD'], phase: ['AMP', 'FRQ', 'PHS'] };
const RX_INIT = {};
const RX_TICK = {};
const RX_BTN = {};
const RX_NUM = {};
const RX_DRAW = {};
const RX_HELP = {};
let RXPARK = null;

function rxManual() {
  if (RXG) return;
  rxOpen();
}

function rxOpen() {
  const r = state.rx;
  const evt = r.evt;
  const node = (!evt && r.node) ? r.node : null;
  const reason = evt ? 'evt' : (node ? 'node' : 'off');
  const key = evt ? 'evt' : (node ? (node.zpm ? 'zpm' : 't' + node.tier) : 'off');
  const stages = RX_PAIRS[key] || ['grid'];
  const si = (RXPARK && RXPARK.key === key) ? Math.min(RXPARK.si, stages.length - 1) : 0;
  RXG = { kind: 'device', evt, reason, node, key, stages, si, done: false, kn: [50, 50, 50], sel: 0, info: false, abort: 0, trans: 0, hold: 0, frame: 0, shift: false, p: null };
  rxStageStart();
  $('rxgame').hidden = false;
  rxBuild();
  rxDraw();
  rxFit();
}

function rxStageStart() {
  RXG.k = RXG.stages[RXG.si];
  RXG.info = false;
  RXG.sel = 0;
  RXG.kn = [50, 50, 50];
  RXG.p = RX_INIT[RXG.k]();
}

function rxClose() {
  RXG = null;
  $('rxgame').hidden = true;
  renderAll();
}

function rxAbandon() {
  if (!RXG) return;
  const r = state.rx;
  if (RXG.reason === 'evt' && !RXG.done) {
    r.evt = false;
    RXPARK = null;
    const boosted = r.preset === 'gate' ? 'gate' : (r.preset === 'lab' ? 'lab' : (r.preset === 'shield' ? 'shield' : null));
    const pool = ['gate', 'lab', 'shield'].filter(k => k !== boosted);
    r.off = pool[Math.floor(Math.random() * pool.length)];
    const msg = {
      gate: 'Gate power regeneration is offline. The gate can still be dialed.',
      lab: 'Lab research is paused.',
      shield: 'Shields are offline. No reduction on ambush injuries or raids.'
    };
    log('Power surge unanswered. ' + msg[r.off] + ' Re-route power at the Quartermaster to restore it.', 'alert');
  } else if (!RXG.done) {
    RXPARK = { key: RXG.key, si: RXG.si };
  } else {
    RXPARK = null;
  }
  rxClose();
}

function rxAbort() {
  if (RXG.reason === 'evt' && !RXG.done) {
    if (RXG.abort > 0) { rxAbandon(); return; }
    RXG.abort = 30;
    sfx.tick();
    rxDraw();
    return;
  }
  rxAbandon();
}

function rxSolved() {
  const r = state.rx;
  const wasOff = r.off;
  r.unlocked = true;
  r.off = null;
  r.evt = false;
  r.count = 0;
  r.target = rxNewTarget();
  RXPARK = null;
  if (RXG.node) {
    if (RXG.node.tier) {
      r.routed = Math.max(r.routed, RXG.node.tier);
      log('Reactor connection routed. Power regeneration is now ' + regenPerMin() + ' per minute at base.', 'ok');
    } else {
      log('The ZPM connection is routed to the reactor.', 'ok');
    }
    r.node = null;
  } else {
    log(wasOff ? 'Power re-routed. ' + RX_OUT[wasOff] + ' is back online.' : 'Power re-routed. The reactor is stable.', 'ok');
  }
  RXG.done = true;
  RXG.info = false;
  sfx.chime();
  rxDraw();
  renderAll();
}

function rxStageDone() {
  if (RXG.trans || RXG.done) return;
  RXG.si++;
  if (RXG.si >= RXG.stages.length) { rxSolved(); return; }
  sfx.chime();
  RXG.trans = 12;
  rxDraw();
}

function rxPreset(id) {
  if (!state.rx.unlocked || !RX_PRESETS[id]) return;
  state.rx.preset = id;
  if (RXG) rxDraw();
  renderAll();
}

function rxBuild() {
  const reason = RXG.reason;
  $('rxtitle').textContent = 'REACTOR CONTROL TABLET';
  $('rxsub').textContent = reason === 'evt' ? 'POWER FLUCTUATION // ANSWER IT OR AN OUTPUT FAILS' : (reason === 'node' ? (RXG.node.zpm ? 'CONNECT THE ZERO POINT MODULE' : 'BRING THE NEW REACTOR TIER ONLINE') : 'RESTORE THE OFFLINE OUTPUT');
  const sides = [['up', '▲'], ['down', '▼'], ['left', '◀'], ['right', '▶'], ['sel', 'SEL'], ['alt', 'ALT'], ['info', 'INFO'], ['abort', 'ABORT']];
  const kn = [0, 1, 2].map(i => `<div class="rxknob" id="rxkn${i}" data-i="${i}"><div class="rxdial" id="rxdial${i}"></div><div class="rxknl" id="rxknl${i}">--</div></div>`).join('');
  $('rxbody').innerHTML = `<div id="rxfit"><div id="rxdev">
    <i class="rxb1"></i><i class="rxb2"></i><i class="rxb3"></i><i class="rxb4"></i><i class="rxcon c1"></i><i class="rxcon c2"></i>
    <div id="rxscr"><svg id="rxsvg" viewBox="0 0 560 380" width="560" height="380"></svg></div>
    <div id="rxside">${sides.map(s => `<button class="rxbt ${s[0]}" onclick="rxBtn('${s[0]}')">${s[1]}</button>`).join('')}</div>
    <div id="rxkeys">${[1, 2, 3, 4, 5].map(n => `<button class="rxk" onclick="rxNum(${n})">${n}</button>`).join('')}</div>
    <div id="rxknobs">${kn}</div>
  </div></div>`;
  [0, 1, 2].forEach(i => {
    const el = $('rxkn' + i);
    el.addEventListener('pointerdown', ev => rxKnobDown(ev, i));
    el.addEventListener('wheel', ev => {
      if (!RX_USEKN[RXG && RXG.k]) return;
      ev.preventDefault();
      rxKnobSet(i, RXG.kn[i] + (ev.deltaY < 0 ? 2 : -2));
    }, { passive: false });
  });
}

function rxKnobDown(ev, i) {
  if (!RXG || !RX_USEKN[RXG.k] || RXG.trans || RXG.done) return;
  ev.preventDefault();
  const el = $('rxkn' + i);
  try { el.setPointerCapture(ev.pointerId); } catch (e) { /* no capture */ }
  const y0 = ev.clientY;
  const v0 = RXG.kn[i];
  RXG.sel = i;
  const mv = e2 => {
    if (!RXG) return;
    const sc = RXG.scale || 1;
    rxKnobSet(i, v0 + (y0 - e2.clientY) / sc * 0.7);
  };
  const up = () => {
    el.removeEventListener('pointermove', mv);
    el.removeEventListener('pointerup', up);
    el.removeEventListener('pointercancel', up);
  };
  el.addEventListener('pointermove', mv);
  el.addEventListener('pointerup', up);
  el.addEventListener('pointercancel', up);
  rxDraw();
}

function rxKnobSet(i, v) {
  if (!RXG || !RX_USEKN[RXG.k] || RXG.trans || RXG.done) return;
  RXG.kn[i] = Math.max(0, Math.min(100, Math.round(v)));
  RXG.sel = i;
  rxDraw();
}

function rxFit() {
  const f = $('rxfit');
  const host = $('rxbody');
  if (!f || !host || !RXG) return;
  const w = host.clientWidth;
  const h = host.clientHeight;
  if (!w || !h) return;
  RXG.fw = w;
  RXG.fh = h;
  const s = Math.min(1.25, w / 720, h / 540);
  RXG.scale = s;
  f.style.width = Math.floor(720 * s) + 'px';
  f.style.height = Math.floor(540 * s) + 'px';
  $('rxdev').style.transform = 'scale(' + s + ')';
}

function rxBtn(b) {
  if (!RXG || RXG.trans) return;
  if (RXG.done) { rxDoneBtn(b); return; }
  if (b === 'info') { RXG.info = !RXG.info; rxDraw(); return; }
  if (b === 'abort') { rxAbort(); return; }
  if (RXG.info) return;
  const f = RX_BTN[RXG.k];
  if (f) f(b);
  if (RXG) rxDraw();
}

function rxNum(n) {
  if (!RXG || RXG.trans) return;
  if (RXG.done) {
    const ks = Object.keys(RX_PRESETS);
    if (ks[n - 1]) rxPreset(ks[n - 1]);
    return;
  }
  if (RXG.info) return;
  const f = RX_NUM[RXG.k];
  if (f) f(n);
  if (RXG) rxDraw();
}

function rxDoneBtn(b) {
  const ks = Object.keys(RX_PRESETS);
  const i = ks.indexOf(state.rx.preset);
  if (b === 'sel' || b === 'abort') { rxAbandon(); return; }
  if (b === 'left' || b === 'up') rxPreset(ks[(i + ks.length - 1) % ks.length]);
  if (b === 'right' || b === 'down') rxPreset(ks[(i + 1) % ks.length]);
}

function rxTick() {
  if (!RXG || $('rxgame').offsetParent === null) return;
  RXG.frame++;
  const host = $('rxbody');
  if (host && (host.clientWidth !== RXG.fw || host.clientHeight !== RXG.fh)) rxFit();
  if (RXG.abort > 0) RXG.abort--;
  if (RXG.trans > 0) {
    RXG.trans--;
    if (!RXG.trans && !RXG.done) rxStageStart();
    rxDraw();
    return;
  }
  if (!RXG.done && !RXG.info) {
    const f = RX_TICK[RXG.k];
    if (f) f();
  }
  if (RXG) rxDraw();
}
setInterval(rxTick, 100);
window.addEventListener('resize', () => { if (RXG) rxFit(); });

document.addEventListener('keydown', e => {
  if (!RXG || $('rxgame').offsetParent === null) return;
  const k = e.key;
  const eat = () => { e.preventDefault(); e.stopImmediatePropagation(); };
  if (k === 'Escape') {
    eat();
    if (RXG.done || RXG.reason !== 'evt') rxAbandon();
    return;
  }
  const map = { ArrowUp: 'up', ArrowDown: 'down', ArrowLeft: 'left', ArrowRight: 'right', Enter: 'sel', ' ': 'sel', Backspace: 'alt', Delete: 'alt', x: 'alt', X: 'alt', '0': 'alt', i: 'info', I: 'info' };
  RXG.shift = e.shiftKey;
  if (map[k]) { eat(); rxBtn(map[k]); return; }
  if (/^[1-5]$/.test(k)) { eat(); rxNum(+k); }
}, true);
