import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
assert s.count('0.9.0') == 4, s.count('0.9.0')
s = s.replace('0.9.0', '0.9.1')
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)

rep(r"""function dipTick() {""", r"""const FOB_COST = 100;
const FOB_SUP = 100;
const FOB_RP = 50;
const FOB_MS = 390000;
const FOB_CAP_SUP = 1000;
const FOB_CAP_RP = 500;
const FOB_GUARD = 10;
const FOB_HOLD = 6;
const FOB_HEAL_MS = 120000;
const FOB_ROLES = ['Garrison Commander', 'Scientist', 'Archeologist', 'Doctor', 'Medic', 'Medic'];

function fobOn(w) { return !!(w && state.fobs && state.fobs[w.id]); }
function lordWorld(lv) { return state.worlds.find(x => x.level === lv && x.lord) || null; }
function lordAlive(w) { const l = lordWorld(w.level); return !!l && l.status !== 'captured'; }
function fobStaffNew() { return FOB_ROLES.map(r => ({ role: r, name: freshSurname() })); }

function fobEstablish(wid) {
  const w = world(wid);
  if (!w || !w.stronghold || w.status !== 'captured' || fobOn(w) || state.res.supplies < FOB_COST) return;
  state.res.supplies -= FOB_COST;
  const now = Date.now();
  if (!state.fobs) state.fobs = {};
  state.fobs[wid] = { staff: fobStaffNew(), guard: FOB_GUARD, wnd: 0, dead: 0, stock: { sup: 0, rp: 0 }, next: now + FOB_MS, heal: 0, rt: now + RAID_CHECK_MS };
  const f = state.fobs[wid];
  sfx.chime();
  log(`A Forward Operating Base was established on ${wname(w)}: ${f.staff[0].role} ${f.staff[0].name}, a scientist, an archeologist, a doctor, two medics and ${FOB_GUARD} security personnel. Cost ${FOB_COST} supplies. It produces ${FOB_SUP} supplies and ${FOB_RP} research points every ${fmt(FOB_MS)}; a Tel'tak collects the stockpile.`, 'ok');
  renderAll();
}

function fobReplace(wid) {
  const f = state.fobs && state.fobs[wid];
  if (!f || f.dead < 1) return;
  const cost = f.dead * REPLACE_COST;
  if (state.res.supplies < cost) return;
  state.res.supplies -= cost;
  f.guard += f.dead;
  log(`${f.dead} security personnel were posted to ${wname(world(wid))} as replacements. Cost ${cost} supplies.`, '');
  f.dead = 0;
  renderAll();
}

function fobRecall(wid) {
  if (!state.fobs || !state.fobs[wid]) return;
  if (state.fobConfirm !== wid) { state.fobConfirm = wid; renderRoom(); return; }
  state.fobConfirm = null;
  const f = state.fobs[wid];
  delete state.fobs[wid];
  delete state.dipl.alerts[wid];
  log(`The Forward Operating Base on ${wname(world(wid))} was recalled. The stockpile of ${f.stock.sup} supplies and ${f.stock.rp} research points was abandoned.`, 'warn');
  renderAll();
}

function fobOverrun(w) {
  const f = state.fobs[w.id];
  delete state.fobs[w.id];
  delete state.dipl.alerts[w.id];
  w.status = 'unexplored';
  w.treaty = false;
  sfx.fail();
  log(`The Forward Operating Base on ${wname(w)} was overrun. ${w.lord || 'The System Lord'}'s forces retook the stronghold and the stockpile of ${f.stock.sup} supplies and ${f.stock.rp} research points is lost. The stronghold must be assaulted again.`, 'alert');
  renderAll();
}

function fobRaid(w) {
  const f = state.fobs && state.fobs[w.id];
  if (!f) return;
  const strong = f.guard >= FOB_HOLD;
  const lo = strong ? 0 : 2;
  const hi = strong ? 2 + Math.floor((w.level - 1) / 2) : 5;
  const n = Math.min(f.guard, lo + Math.floor(Math.random() * (hi - lo + 1)));
  let wd = 0;
  let kl = 0;
  for (let i = 0; i < n; i++) { if (Math.random() < 0.7) wd++; else kl++; }
  f.guard -= n;
  f.wnd += wd;
  f.dead += kl;
  f.rt = Date.now() + RAID_CHECK_MS;
  if (f.guard <= 0) { fobOverrun(w); return; }
  const loss = n ? ` ${wd} wounded and ${kl} killed.` : ' No casualties.';
  log(`No team answered the raid on ${wname(w)}. The garrison ${strong ? 'drove the attackers off' : 'barely held'} with ${f.guard} fit defenders left.${loss}`, strong ? 'warn' : 'alert');
  renderAll();
}

function fobTick() {
  if (!state.started || !state.fobs) return;
  const now = Date.now();
  let ch = false;
  Object.keys(state.fobs).forEach(id => {
    const w = world(id);
    const f = state.fobs[id];
    if (!w) { delete state.fobs[id]; return; }
    if (now >= f.next) {
      f.next = now + FOB_MS;
      if (f.stock.sup < FOB_CAP_SUP || f.stock.rp < FOB_CAP_RP) {
        f.stock.sup = Math.min(FOB_CAP_SUP, f.stock.sup + FOB_SUP);
        f.stock.rp = Math.min(FOB_CAP_RP, f.stock.rp + FOB_RP);
        ch = true;
        if (f.stock.sup >= FOB_CAP_SUP && f.stock.rp >= FOB_CAP_RP) log(`The stockpile on ${wname(w)} is full. Production is paused until a Tel'tak collects it.`, 'warn');
      }
    }
    if (f.wnd > 0) {
      if (!f.heal) f.heal = now + FOB_HEAL_MS;
      else if (now >= f.heal) { f.wnd--; f.guard++; f.heal = f.wnd > 0 ? now + FOB_HEAL_MS : 0; ch = true; }
    } else f.heal = 0;
    if (lordAlive(w) && now >= f.rt) {
      f.rt = now + RAID_CHECK_MS;
      if (!state.dipl.alerts[id] && Math.random() < TREATY.hold.raidP) {
        state.dipl.alerts[id] = now + RAID_ALERT_MS;
        sfx.fail();
        log(`RAID ALERT: ${w.lord || 'Goa\'uld'} forces are attacking the Forward Operating Base on ${wname(w)}. Send a Security or Assault team through the gate within ${fmt(RAID_ALERT_MS)} (mission type DEFEND) or the garrison fights alone.`, 'alert');
        ch = true;
      }
    }
  });
  if (ch) renderAll();
}

function fobHtml() {
  const F = state.fobs || {};
  const ids = Object.keys(F);
  const cand = state.worlds.filter(w => w.stronghold && w.status === 'captured' && !F[w.id]);
  let h = '<h2>Forward Operating Bases</h2>';
  if (!ids.length && !cand.length) return h + `<p class="dim small help">Capture a stronghold to build a base there. A base costs ${FOB_COST} supplies, holds ${FOB_GUARD} security personnel and a small science staff, and makes ${FOB_SUP} supplies and ${FOB_RP} research points every ${fmt(FOB_MS)}.</p>`;
  ids.forEach(id => {
    const w = world(id);
    const b = F[id];
    const al = state.dipl.alerts[id];
    const st = al ? `<span class="warn">RAID <span data-eta="${al}">${fmt(al - Date.now())}</span></span>` : '<span class="ok">SECURE</span>';
    const full = b.stock.sup >= FOB_CAP_SUP && b.stock.rp >= FOB_CAP_RP;
    h += `<div class="staff-row nob"><span><b>${wname(w)}</b> <span class="dim">${sysOf(w.level).star}</span></span>${st}</div>`;
    h += `<div class="res-row"><span>Garrison</span><span>${b.guard} / ${FOB_GUARD} FIT${b.wnd ? ' // ' + b.wnd + ' WOUNDED' : ''}${b.dead ? ' // ' + b.dead + ' LOST' : ''}</span></div>`;
    h += `<div class="res-row"><span>Stockpile</span><span>${b.stock.sup} / ${FOB_CAP_SUP} SUP // ${b.stock.rp} / ${FOB_CAP_RP} RP</span></div>`;
    h += `<div class="res-row"><span>Next output</span>${full ? '<span class="warn">STOCKPILE FULL</span>' : `<span data-eta="${b.next}">${fmt(Math.max(0, b.next - Date.now()))}</span>`}</div>`;
    h += `<div class="res-row"><span>Raid check</span>${lordAlive(w) ? `<span data-eta="${b.rt}">${fmt(Math.max(0, b.rt - Date.now()))}</span>` : '<span class="ok">ENDED // LORD DEFEATED</span>'}</div>`;
    h += `<div class="dim small" style="margin:4px 0">${b.staff.map(m => m.role + ' ' + m.name).join(' // ')}</div>`;
    h += `<div class="controls" style="margin:6px 0 12px;justify-content:flex-start"><button onclick="fobReplace('${id}')" ${b.dead && state.res.supplies >= b.dead * REPLACE_COST ? '' : 'disabled'}>REPLACE ${b.dead} // ${b.dead * REPLACE_COST} SUP</button><button onclick="fobRecall('${id}')">${state.fobConfirm === id ? 'CONFIRM RECALL' : 'RECALL BASE'}</button></div>`;
  });
  cand.forEach(w => {
    h += `<div class="staff-row"><span><b>${wname(w)}</b> <span class="dim">${sysOf(w.level).star} // captured</span></span><button onclick="fobEstablish('${w.id}')" ${state.res.supplies >= FOB_COST ? '' : 'disabled'}>ESTABLISH // ${FOB_COST} SUP</button></div>`;
  });
  h += `<p class="dim small help">A base makes ${FOB_SUP} supplies and ${FOB_RP} research points every ${fmt(FOB_MS)} until its stockpile holds ${FOB_CAP_SUP} and ${FOB_CAP_RP}. A Tel'tak sent to the world collects everything. While the System Lord of that level lives, the base is raided: answer with a Defend mission, or the garrison fights alone. Wounded recover slowly; killed are replaced for ${REPLACE_COST} supplies each. If every defender falls the stronghold is lost.</p>`;
  return h;
}

function dipTick() {""")

rep("""    if (!w || !w.treaty || w.level !== state.level) { delete state.dipl.alerts[wid]; return; }""",
"""    const fb = fobOn(w);
    if (!w || (!w.treaty && !fb) || w.level !== state.level || (fb && !lordAlive(w))) { delete state.dipl.alerts[wid]; return; }""")
rep("""        log('Shields absorbed the raid on ' + wname(w) + '. The treaty holds.', 'ok');
        renderAll();
      } else treatyLose(""", """        log('Shields absorbed the raid on ' + wname(w) + '. ' + (fb ? 'The base is untouched.' : 'The treaty holds.'), 'ok');
        renderAll();
      } else if (fb) {
        delete state.dipl.alerts[wid];
        fobRaid(w);
      } else treatyLose(""")

rep("""      delete state.dipl.alerts[w.id];
      state.dipl.raid[w.id] = Date.now() + RAID_CHECK_MS;
      mev(lid, `Raid on ${wname(w)} repelled. Treaty holds.`);
      log(`${names.join(', ')} repelled the raid on ${wname(w)}. The treaty holds.`, 'ok');""",
"""      delete state.dipl.alerts[w.id];
      if (fobOn(w)) {
        state.fobs[w.id].rt = Date.now() + RAID_CHECK_MS;
        mev(lid, `Raid on the base at ${wname(w)} repelled.`);
        log(`${names.join(', ')} repelled the raid on the base at ${wname(w)}.`, 'ok');
      } else {
        state.dipl.raid[w.id] = Date.now() + RAID_CHECK_MS;
        mev(lid, `Raid on ${wname(w)} repelled. Treaty holds.`);
        log(`${names.join(', ')} repelled the raid on ${wname(w)}. The treaty holds.`, 'ok');
      }""")

rep("  facPay();\n  if (state.gate", "  facPay();\n  fobTick();\n  if (state.gate")

rep("""function tkWorlds() { return state.worlds.filter(w => w.kind === 'normal' && w.status === 'explored'); }""",
    """function tkWorlds() { return state.worlds.filter(w => (w.kind === 'normal' && w.status === 'explored') || fobOn(w)); }""")
rep("""  mev(x.lid, `Arrived at ${w ? wname(w) : 'the world'}. Cargo loading.`);""",
"""  if (w && fobOn(w)) {
    const f = state.fobs[w.id];
    x.load = { sup: f.stock.sup, rp: f.stock.rp };
    f.stock.sup = 0;
    f.stock.rp = 0;
    mev(x.lid, `Arrived at ${wname(w)}. Loaded ${x.load.sup} supplies and ${x.load.rp} research points from the base.`);
    renderAll();
  } else mev(x.lid, `Arrived at ${w ? wname(w) : 'the world'}. Cargo loading.`);""")
rep("""  const y = w ? tkYield(w) : 0;
  state.res.supplies += y;""", """  const y = x.load ? x.load.sup : (w ? tkYield(w) : 0);
  const ry = x.load ? x.load.rp : 0;
  x.load = null;
  state.res.supplies += y;
  state.research += ry;""")
rep("mresult(x.lid, null, { supplies: y });", "mresult(x.lid, null, ry ? { supplies: y, research: ry } : { supplies: y });")
rep("with ${y} supplies.`);", "with ${y} supplies${ry ? ' and ' + ry + ' research points' : ''}.`);")
rep("with ${y} supplies.`, 'ok');", "with ${y} supplies${ry ? ' and ' + ry + ' research points' : ''}.`, 'ok');")
rep("""${known ? HAZ_LABEL[w.hazard] + ' hazard, ' + tkYield(w) + ' supplies' : 'hazard unknown'}""",
    """${fobOn(w) ? 'FOB stockpile ' + state.fobs[w.id].stock.sup + ' supplies, ' + state.fobs[w.id].stock.rp + ' RP' : known ? HAZ_LABEL[w.hazard] + ' hazard, ' + tkYield(w) + ' supplies' : 'hazard unknown'}""")

rep("""<div style="margin-top:14px">${lgHtml()}</div>`;""", """<div style="margin-top:14px">${lgHtml()}${fobHtml()}</div>`;""")

rep("""  if (w.lord && w.intel >= 2) b.push(""", """  if (fobOn(w)) b.push('<span class="badge ok">FOB</span>');
  if (w.lord && w.intel >= 2) b.push(""")

rep("""Spoils: ${bs} supplies and ${br} research points.`;""", """Spoils: ${bs} supplies and ${br} research points.${Object.keys(state.fobs || {}).some(id => { const x = world(id); return x && x.level === w.level; }) ? ' Raids on the bases in this system have ended.' : ''}`;""")

rep("    dipl: { alerts: {}, raid: {} },\n", "    dipl: { alerts: {}, raid: {} },\n    fobs: {},\n")
rep("    fac: { pts: state.fac.pts, freeRepl", """    fobs: Object.keys(state.fobs || {}).reduce((o, k) => {
      const f = state.fobs[k];
      o[k] = { staff: f.staff.map(m => Object.assign({}, m)), guard: f.guard, wnd: f.wnd, dead: f.dead, stock: Object.assign({}, f.stock), nextLeft: Math.max(0, f.next - now), healLeft: f.heal ? Math.max(0, f.heal - now) : 0, rtLeft: Math.max(0, f.rt - now) };
      return o;
    }, {}),
    fac: { pts: state.fac.pts, freeRepl""")
rep("  state.vp = vpLoad(d.vp);\n", """  state.vp = vpLoad(d.vp);
  state.fobs = {};
  Object.keys(d.fobs || {}).forEach(k => {
    const f = d.fobs[k];
    if (!world(k) || !f || !Array.isArray(f.staff)) return;
    state.fobs[k] = { staff: f.staff, guard: f.guard | 0, wnd: f.wnd | 0, dead: f.dead | 0, stock: { sup: (f.stock && f.stock.sup) | 0, rp: (f.stock && f.stock.rp) | 0 }, next: now + (f.nextLeft || 0), heal: f.healLeft ? now + f.healLeft : 0, rt: now + (f.rtLeft || RAID_CHECK_MS) };
  });
""")

rep("  B1: ['SELECTING A DESTINATION'", """  FB1: ['FORWARD OPERATING BASE', 'A captured stronghold can host a Forward Operating Base from the Quartermaster room: 100 supplies buys a Garrison Commander, a science and medical staff and 10 security personnel. The base makes 100 supplies and 50 research points every 6:30 until its stockpile is full, and a Tel\\'tak sent to that world collects it. While the System Lord of that level lives, the base is raided about every quarter hour: answer with a Defend mission, or the garrison fights alone and may lose people. If every defender falls, the stronghold is lost.'],
  B1: ['SELECTING A DESTINATION'""")
rep("    LD1: () => state.level >= 1,", "    FB1: () => state.worlds.some(w => w.stronghold && w.status === 'captured'),\n    LD1: () => state.level >= 1,")

rep(""".dispatch-row button, .staff-row button, .res-row button { min-width: 112px; }""",
""".dispatch-row button, .staff-row button, .res-row button { width: 230px; min-width: 230px; flex: none; white-space: nowrap; padding: 0 10px; }
.dispatch-row button.mid, .staff-row button.mid, .res-row button.mid { width: auto; }
.controls { justify-content: flex-start; }
.res-row select, .staff-row select { width: 230px; min-width: 230px; flex: none; }
.controls button { min-height: var(--ctl-sm); min-width: 230px; padding: 0 10px; font-size: var(--fs-sm); white-space: nowrap; }""")
rep("""TIER ${mt + 1} // ${rp} RP // ${sup} SUP // ${fmt(T.ms)}</button>""", """${rp} RP // ${sup} SUP // ${fmt(T.ms)}</button>""")
rep("""<button style="white-space:nowrap" ${!labCanStart() || state.research < rp || state.res.supplies < sup ? 'disabled' : ''} onclick="startVpartResearch('${t}','${p}')">${VP_ROM[e.r]} // ${rp} RP""", """<button ${!labCanStart() || state.research < rp || state.res.supplies < sup ? 'disabled' : ''} onclick="startVpartResearch('${t}','${p}')">${rp} RP""")

rep("CONVERT NAQUADAH +15 POWER</button", "NAQUADAH +15 POWER</button")

rep(".mpfoot button { min-height: 0; padding: 4px 12px; }", ".mpfoot button { min-height: var(--ctl-sm); min-width: 170px; padding: 0 10px; font-size: var(--fs-sm); white-space: nowrap; }")

open(dst, 'w', encoding='utf-8').write(s)
print('ok')
