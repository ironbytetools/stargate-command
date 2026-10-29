import sys
src, dst = sys.argv[1:3]
s = open(src, encoding='utf-8').read()
assert s.count('0.9.17') == 4, s.count('0.9.17')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('<title>Stargate Command 0.9.17</title>', '<title>Stargate Command 0.9.18</title>')
rep('BUILD 0.9.17', 'BUILD 0.9.18', 2)
rep("const BUILD_VER = '0.9.17';", "const BUILD_VER = '0.9.18';")

CORE = r'''
const OP_COST = 60;
const OP_COST_STEP = 20;
const OP_MS = 390000;
const OP_UPKEEP = 10;
const OP_UPKEEP_LV = 3;
const OP_GUARD = 4;
const OP_REPL = 20;
const OP_EV_MS = 120000;
const OP_EVP = { low: 0.15, med: 0.25, high: 0.35 };
const RV_P = 0.5;
const OP_YIELD = {
  'Temperate forest': { sup: 45 },
  'Arid desert': { sup: 15, nq: 1 },
  'Frozen tundra': { sup: 15, rp: 30 },
  'Ocean archipelago': { sup: 30, rp: 15 },
  'Volcanic highlands': { sup: 10, nq: 2 },
  'Jungle lowlands': { sup: 30, rp: 10 },
  'Mountain plateau': { sup: 15, rp: 10, nq: 1 },
  'Ancient ruins field': { rp: 45 }
};
function opScale(w) { return 1 + 0.25 * (w.level - 1); }
function opOn(w) { return !!(w && state.outposts && state.outposts[w.id]); }
function opCount() { return Object.keys(state.outposts || {}).length; }
function opCost() { return OP_COST + OP_COST_STEP * opCount(); }
function opUpkeep(w) { return OP_UPKEEP + OP_UPKEEP_LV * (w.level - 1); }
function opYieldOf(w) {
  const y = OP_YIELD[w.type] || { sup: 25 };
  const k = opScale(w);
  return { sup: Math.round((y.sup || 0) * k), rp: Math.round((y.rp || 0) * k), nq: Math.round((y.nq || 0) * k) };
}
function opYieldText(y) {
  const p = [];
  if (y.sup) p.push(y.sup + ' SUP');
  if (y.rp) p.push(y.rp + ' RP');
  if (y.nq) p.push(y.nq + ' NAQ');
  return p.join(' // ') || 'NOTHING';
}
function opCands() {
  return state.worlds.filter(w => w.kind === 'normal' && !w.stronghold && w.status === 'explored' && !opOn(w) && !fobOn(w));
}
function opEstablish(wid) {
  const w = world(wid);
  if (!w || opOn(w) || w.kind !== 'normal' || w.stronghold || w.status !== 'explored') return;
  const c = opCost();
  if (state.res.supplies < c) return;
  state.res.supplies -= c;
  if (!state.outposts) state.outposts = {};
  state.outposts[wid] = { guard: OP_GUARD, next: Date.now() + OP_MS, dry: false, down: false, ev: null, last: null };
  sfx.chime();
  log(`An outpost was established on ${wname(w)} (${w.type}): ${OP_GUARD} security personnel. Cost ${c} supplies. Output ${opYieldText(opYieldOf(w))} per ${fmt(OP_MS)}, upkeep ${opUpkeep(w)} supplies.`, 'ok');
  renderAll();
}
function opAbandon(wid) {
  if (!state.outposts || !state.outposts[wid]) return;
  if (state.opConfirm !== wid) { state.opConfirm = wid; renderRoom(); return; }
  state.opConfirm = null;
  delete state.outposts[wid];
  log(`The outpost on ${wname(world(wid))} was abandoned.`, 'warn');
  renderAll();
}
function opReplace(wid) {
  const f = state.outposts && state.outposts[wid];
  if (!f || f.guard >= OP_GUARD || state.res.supplies < OP_REPL) return;
  state.res.supplies -= OP_REPL;
  f.guard++;
  log(`A security officer was posted to the outpost on ${wname(world(wid))}. Cost ${OP_REPL} supplies.`, 'ok');
  renderAll();
}
function opLost(w, why) {
  delete state.outposts[w.id];
  sfx.fail();
  log(`The outpost on ${wname(w)} was overrun. ${why} The site must be built again.`, 'alert');
}
const OP_EVS = {
  raid: {
    title: 'RAID',
    text: w => `Goa'uld scouts are probing the outpost on ${wname(w)}.`,
    a: w => ({ label: 'REINFORCE', cost: Math.round(40 * opScale(w)), tip: 'Spend supplies to drive them off' }),
    b: { label: 'HOLD', tip: 'The garrison fights alone and may take losses' }
  },
  trader: {
    title: 'TRADER',
    text: w => `A trader has reached the outpost on ${wname(w)} with salvage and star charts.`,
    a: w => ({ label: 'TRADE', cost: Math.round(50 * opScale(w)), tip: 'Pay supplies for research points' }),
    b: { label: 'DECLINE', tip: 'Send the trader on' }
  },
  cache: {
    title: 'SITE FOUND',
    text: w => `Sensors on the outpost at ${wname(w)} picked up a buried site nearby.`,
    a: w => ({ label: 'SURVEY', cost: Math.round(20 * opScale(w)), tip: 'Send a survey party' }),
    b: { label: 'IGNORE', tip: 'Leave it' }
  },
  quake: {
    title: 'TREMORS',
    text: w => `Tremors damaged the generator at the outpost on ${wname(w)}.`,
    a: w => ({ label: 'REPAIR', cost: Math.round(50 * opScale(w)), tip: 'Spend supplies to keep output running' }),
    b: { label: 'WAIT', tip: 'Output is paused for one interval' }
  }
};
function opEvWeights(w) {
  return {
    raid: { low: 1, med: 2, high: 3 }[w.hazard] || 1,
    trader: w.env === 'Scattered settlements, old roads' ? 4 : 1,
    cache: ['Ancient ruins field', 'Mountain plateau', 'Arid desert'].includes(w.type) ? 3 : 1,
    quake: w.env === 'Seismic activity, unstable ground' ? 4 : 0.5
  };
}
function opPickEv(w) {
  const wt = opEvWeights(w);
  const ks = Object.keys(wt);
  let r = Math.random() * ks.reduce((a, k) => a + wt[k], 0);
  for (const k of ks) { r -= wt[k]; if (r <= 0) return k; }
  return ks[0];
}
function opChoose(wid, ch, auto) {
  const w = world(wid);
  const f = state.outposts && state.outposts[wid];
  if (!w || !f || !f.ev) return;
  const k = f.ev.k;
  const sc = opScale(w);
  const A = OP_EVS[k].a(w);
  if (ch === 'a' && state.res.supplies < A.cost) return;
  f.ev = null;
  const nm = wname(w);
  if (k === 'raid') {
    if (ch === 'a') {
      state.res.supplies -= A.cost;
      log(`The outpost on ${nm} was reinforced and drove the raiders off. Cost ${A.cost} supplies.`, 'ok');
    } else {
      const n = Math.min(f.guard, Math.floor(Math.random() * 3));
      f.guard -= n;
      if (f.guard <= 0) { opLost(w, auto ? 'The raid went unanswered.' : 'The garrison fell.'); renderAll(); return; }
      log(`The garrison on ${nm} held${auto ? ' alone' : ''}. ${n ? n + ' security personnel lost.' : 'No casualties.'}`, n ? 'warn' : 'ok');
    }
  } else if (k === 'trader') {
    if (ch === 'a') {
      const rp = Math.round(80 * sc);
      state.res.supplies -= A.cost;
      state.research += rp;
      log(`Traded ${A.cost} supplies for ${rp} research points at the outpost on ${nm}.`, 'ok');
    } else log(`The trader at ${nm} moved on.`, 'ok');
  } else if (k === 'cache') {
    if (ch === 'a') {
      state.res.supplies -= A.cost;
      const r = Math.random();
      if (r < 0.5) { const rp = Math.round(100 * sc); state.research += rp; log(`The survey party near ${nm} recovered old data: +${rp} research points. Cost ${A.cost} supplies.`, 'ok'); }
      else if (r < 0.8) { const sp = Math.round(80 * sc); state.res.supplies += sp; log(`The survey party near ${nm} found a supply cache: +${sp} supplies. Cost ${A.cost} supplies.`, 'ok'); }
      else { const nq = 1 + w.level; state.res.naquadah += nq; log(`The survey party near ${nm} found a naquadah seam: +${nq} naquadah. Cost ${A.cost} supplies.`, 'ok'); }
    } else log(`The site near ${nm} was left alone.`, 'ok');
  } else if (k === 'quake') {
    if (ch === 'a') { state.res.supplies -= A.cost; log(`The generator on ${nm} was repaired. Cost ${A.cost} supplies.`, 'ok'); }
    else { f.down = true; log(`The outpost on ${nm} will skip its next delivery.`, 'warn'); }
  }
  renderAll();
}
function opTick() {
  if (!state.started || !state.outposts) return;
  const now = Date.now();
  let ch = false;
  Object.keys(state.outposts).forEach(id => {
    const w = world(id);
    const f = state.outposts[id];
    if (!w) { delete state.outposts[id]; return; }
    if (f.ev && now >= f.ev.until) { opChoose(id, 'b', true); ch = true; if (!state.outposts[id]) return; }
    if (now >= f.next) {
      f.next = now + OP_MS;
      const upk = opUpkeep(w);
      if (state.res.supplies < upk) {
        if (!f.dry) log(`The outpost on ${wname(w)} could not be supplied (${upk} supplies upkeep) and delivered nothing.`, 'warn');
        f.dry = true;
      } else {
        state.res.supplies -= upk;
        f.dry = false;
        if (f.down) { f.down = false; f.last = null; log(`The outpost on ${wname(w)} delivered nothing this interval.`, 'warn'); }
        else {
          const y = opYieldOf(w);
          state.res.supplies += y.sup;
          state.research += y.rp;
          state.res.naquadah += y.nq;
          f.last = y;
        }
        if (!f.ev && Math.random() < (OP_EVP[w.hazard] || 0.2)) {
          const k = opPickEv(w);
          f.ev = { k, until: now + OP_EV_MS };
          sfx.fail();
          log(`OUTPOST ${OP_EVS[k].title}: ${OP_EVS[k].text(w)} Decide in the Off-World Operations room within ${fmt(OP_EV_MS)}.`, k === 'raid' ? 'alert' : 'warn');
        }
      }
      ch = true;
    }
  });
  if (ch) renderAll();
}
function opEvHtml(id, f) {
  const w = world(id);
  const E = OP_EVS[f.ev.k];
  const A = E.a(w);
  const can = state.res.supplies >= A.cost;
  return `<div class="dispatch-row" style="text-align:left"><div><b class="warn">${E.title}</b> <span class="dim">decide in <span data-eta="${f.ev.until}">${fmt(Math.max(0, f.ev.until - Date.now()))}</span></span><div class="mrow">${E.text(w)}</div></div></div>`
    + `<div class="controls" style="margin:6px 0 12px;justify-content:flex-start"><button onclick="opChoose('${id}','a')" ${can ? '' : 'disabled'} title="${A.tip}">${A.label} // ${A.cost} SUP</button><button onclick="opChoose('${id}','b')" title="${E.b.tip}">${E.b.label}</button></div>`;
}
function opLeftHtml() {
  const ids = Object.keys(state.outposts || {});
  let tot = 0;
  let h = '';
  ids.forEach(id => {
    const w = world(id);
    const f = state.outposts[id];
    if (!w) return;
    tot += opUpkeep(w);
    const st = f.ev ? '<span class="warn">EVENT</span>' : (f.dry ? '<span class="warn">UNSUPPLIED</span>' : '<span class="ok">ACTIVE</span>');
    h += `<div class="staff-row nob"><span><b>${wname(w)}</b> <span class="dim">${sysOf(w.level).star} // ${w.type}</span></span>${st}</div>`;
    if (f.ev) h += opEvHtml(id, f);
    h += `<div class="res-row"><span>Garrison</span><span>${f.guard} / ${OP_GUARD} FIT</span></div>`;
    h += `<div class="res-row"><span>Output</span><span>${opYieldText(opYieldOf(w))}${f.down ? ' // <span class="warn">PAUSED</span>' : ''}</span></div>`;
    h += `<div class="res-row"><span>Next delivery</span><span data-eta="${f.next}">${fmt(Math.max(0, f.next - Date.now()))}</span></div>`;
    h += `<div class="res-row"><span>Upkeep</span><span>${opUpkeep(w)} SUP / ${fmt(OP_MS)} // ${w.hazard.toUpperCase()} HAZARD</span></div>`;
    h += `<div class="controls" style="margin:6px 0 12px;justify-content:flex-start"><button onclick="opReplace('${id}')" ${f.guard < OP_GUARD && state.res.supplies >= OP_REPL ? '' : 'disabled'}>POST 1 // ${OP_REPL} SUP</button><button onclick="opAbandon('${id}')">${state.opConfirm === id ? 'CONFIRM ABANDON' : 'ABANDON'}</button></div>`;
  });
  return `<h2>Outposts <span class="dim">${ids.length}${ids.length ? ' // UPKEEP ' + tot + ' SUP' : ''}</span></h2>${h || '<p class="dim">No outposts yet. Pick an explored world to build one.</p>'}`;
}
function opRightHtml() {
  const cand = opCands();
  let h = '';
  cand.forEach(w => {
    h += `<div class="staff-row nob"><span><b>${wname(w)}</b> <span class="dim">${sysOf(w.level).star} // ${w.type} // ${w.hazard.toUpperCase()} HAZARD</span></span></div>`;
    h += `<div class="controls" style="margin:0 0 12px;justify-content:flex-start"><button onclick="opEstablish('${w.id}')" ${state.res.supplies >= opCost() ? '' : 'disabled'}>BUILD // ${opCost()} SUP // ${opYieldText(opYieldOf(w))}</button></div>`;
  });
  return `<h2>Outpost sites <span class="dim">${cand.length}</span></h2>${h || '<p class="dim">Explore regular worlds to unlock outpost sites.</p>'}<p class="dim small help">Outposts are small bases on explored regular worlds. The world type sets the output, delivered through the gate every ${fmt(OP_MS)} after upkeep, and higher levels pay more. Each outpost after the first costs ${OP_COST_STEP} more. A random event comes up now and then; answer it here before the timer runs out or the default applies.</p>`;
}
function revisitEvent(w, was, yl) {
  if (!was || !w || w.kind !== 'normal' || w.stronghold || Math.random() >= RV_P) return '';
  const sc = opScale(w);
  const wt = {
    cache: 2 + (w.type === 'Arid desert' ? 1 : 0),
    data: 1 + (['Ancient ruins field', 'Mountain plateau'].includes(w.type) ? 3 : 0),
    trader: 1 + (w.env === 'Scattered settlements, old roads' ? 3 : 0),
    patrol: w.hazard === 'high' ? 3 : (w.hazard === 'med' ? 1 : 0.3)
  };
  const ks = Object.keys(wt);
  let r = Math.random() * ks.reduce((a, k) => a + wt[k], 0);
  let k = ks[0];
  for (const x of ks) { r -= wt[x]; if (r <= 0) { k = x; break; } }
  const ty = w.type.toLowerCase();
  if (k === 'cache') {
    const v = Math.round(35 * sc);
    state.res.supplies += v; yl.supplies = (yl.supplies || 0) + v;
    return ` Revisit: in the ${ty} the team found an abandoned supply cache. +${v} supplies.`;
  }
  if (k === 'data') {
    const v = Math.round(45 * sc);
    state.research += v; yl.research = (yl.research || 0) + v;
    return ` Revisit: a second look at the ${ty} turned up recoverable data. +${v} research points.`;
  }
  if (k === 'trader') {
    const v = 1 + (sc >= 1.5 ? 1 : 0);
    state.res.naquadah += v; yl.naquadah = (yl.naquadah || 0) + v;
    return ` Revisit: local traders swapped naquadah for field rations. +${v} naquadah.`;
  }
  const v = Math.min(state.res.supplies, Math.round(20 * sc));
  state.res.supplies -= v; yl.supplies = (yl.supplies || 0) - v;
  return ` Revisit: a Goa'uld patrol forced the team to drop gear and run. ${v} supplies lost.`;
}
'''
rep("function fobTick() {", CORE + "\nfunction fobTick() {")

rep("  return Object.keys(state.fobs || {}).length > 0 || state.worlds.some(w => w.stronghold && w.status === 'captured');",
    "  return Object.keys(state.fobs || {}).length > 0 || opCount() > 0 || state.worlds.some(w => w.stronghold && w.status === 'captured');")

rep("return `<div class=\"rgrid\"><div>${left}</div><div>${right}</div></div>`;\n}\n\nfunction dipTick",
    "return `<div class=\"rgrid\"><div>${left}${opLeftHtml()}</div><div>${right}${opRightHtml()}</div></div>`;\n}\n\nfunction dipTick")

rep("        if (w.status !== 'captured') w.status = 'explored';\n        if (w.kind === 'lab')",
    "        const rvWas = w.status === 'explored';\n        if (w.status !== 'captured') w.status = 'explored';\n        if (w.kind === 'lab')")
rep("        msg += glExplore(w);\n        msg += facLead(w, t, m.lid);",
    "        msg += glExplore(w);\n        msg += revisitEvent(w, rvWas, yl);\n        msg += facLead(w, t, m.lid);")

rep("  if (fobOn(w)) b.push('<span class=\"badge ok\">FOB</span>');", "  if (fobOn(w)) b.push('<span class=\"badge ok\">FOB</span>');\n  if (opOn(w)) b.push('<span class=\"badge ok\">OUTPOST</span>');")

rep("    return nb ? `${nb} BASE${nb === 1 ? '' : 'S'} ACTIVE` : 'NO BASES YET';",
    """    const no = opCount();
    const oe = Object.keys(state.outposts || {}).filter(id => state.outposts[id].ev).length;
    if (oe) return `<span class="warn">${oe} OUTPOST EVENT${oe === 1 ? '' : 'S'}</span>`;
    return nb || no ? `${nb} BASE${nb === 1 ? '' : 'S'} // ${no} OUTPOST${no === 1 ? '' : 'S'}` : 'NO BASES YET';""")

rep("  fobTick();\n", "  fobTick();\n  opTick();\n")

rep("    fac: { pts: state.fac.pts,", """    outposts: Object.keys(state.outposts || {}).reduce((o, k) => {
      const f = state.outposts[k];
      o[k] = { guard: f.guard, dry: !!f.dry, down: !!f.down, nextLeft: Math.max(0, f.next - now), ev: f.ev ? { k: f.ev.k, left: Math.max(0, f.ev.until - now) } : null, last: f.last || null };
      return o;
    }, {}),
    fac: { pts: state.fac.pts,""")
rep("  state.selVeh = [];\n  state.vehicles = (d.vehicles", """  state.outposts = {};
  Object.keys(d.outposts || {}).forEach(k => {
    const f = d.outposts[k];
    const w = world(k);
    if (!w || !f) return;
    state.outposts[k] = { guard: Math.max(0, Math.min(OP_GUARD, f.guard | 0)), dry: !!f.dry, down: !!f.down, next: now + (f.nextLeft | 0), ev: f.ev && OP_EVS[f.ev.k] ? { k: f.ev.k, until: now + (f.ev.left | 0) } : null, last: f.last || null };
  });
  state.selVeh = [];
  state.vehicles = (d.vehicles""")

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
