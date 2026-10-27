import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
assert s.count('0.8.8') == 3
s = s.replace('0.8.8', '0.8.9')
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:60])
    s = s.replace(a, b)

rep("""function assistMsFor(t) {
  const b = t && t.mission ? fixBandOf(t.mission) : null;
  return b ? Math.round(b.assistMs * fastMul()) : assistMs();
}""", """const RESC_TIERS = [
  { n: 1, name: 'Rescuer', pay: 25 },
  { n: 3, name: 'Lifeline', pay: 50 },
  { n: 6, name: 'Guardian', pay: 75 },
  { n: 10, name: 'Sentinel', pay: 100 },
  { n: 15, name: 'Angel of the Gate', pay: 150 }
];
const RESC_CUT = 0.05;
function rescTier(t) { let k = 0; RESC_TIERS.forEach((x, i) => { if ((t.rescues || 0) >= x.n) k = i + 1; }); return k; }
function rescTitle(t) { const k = rescTier(t); return k ? RESC_TIERS[k - 1].name : ''; }
function rescCut(teams) { return RESC_CUT * Math.max(0, ...(teams || []).map(rescTier)); }
function rescRow(t) {
  const k = rescTier(t);
  const nx = RESC_TIERS[k];
  return `${t.rescues || 0}${k ? ' // ' + RESC_TIERS[k - 1].name.toUpperCase() + ' // -' + Math.round(k * RESC_CUT * 100) + '% ASSIST TRAVEL' : ''}${nx ? ' // NEXT AT ' + nx.n : ''}`;
}
function rescAward(a, lid) {
  const k0 = rescTier(a);
  a.rescues = (a.rescues || 0) + 1;
  const k1 = rescTier(a);
  if (k1 <= k0) return;
  const T = RESC_TIERS[k1 - 1];
  state.res.supplies += T.pay;
  state.research += T.pay;
  const msg = `${a.name} earned the title ${T.name} (${T.n} rescue${T.n === 1 ? '' : 's'}). +${T.pay} supplies and +${T.pay} research points. Assist travel now ${Math.round(k1 * RESC_CUT * 100)}% faster.`;
  log(msg, 'ok');
  if (lid) mev(lid, msg);
}

function assistMsFor(t, teams) {
  const b = t && t.mission ? fixBandOf(t.mission) : null;
  const ms = b ? Math.round(b.assistMs * fastMul()) : assistMs();
  return Math.round(ms * (1 - rescCut(teams)));
}""")

rep("""    a.eta = Date.now() + assistMsFor(t);""", """    a.eta = Date.now() + assistMsFor(t, teams);""")
rep("""  later(() => resolveAssist(gmid), assistMsFor(t));""", """  later(() => resolveAssist(gmid), assistMsFor(t, teams));""")
rep("""      a.rescues = (a.rescues || 0) + 1;
      a.mission.camMult = mult;""", """      rescAward(a, glid);
      a.mission.camMult = mult;""")
rep("""    <div class="res-row"><span>Rescues performed</span><span>${t.rescues || 0}</span></div>""", """    <div class="res-row"><span>Rescues performed</span><span>${rescRow(t)}</span></div>""")
rep("""    `Rescues performed: ${t.rescues || 0}   Times rescued: ${t.rescued || 0}`""", """    `Rescues performed: ${t.rescues || 0}${rescTitle(t) ? ' (' + rescTitle(t) + ')' : ''}   Times rescued: ${t.rescued || 0}`""")
i = s.index("Travel ${fmt(assistMsFor(assistTarget))}")
s = s[:i] + "Travel ${fmt(assistMsFor(assistTarget, sel))}" + s[i+len("Travel ${fmt(assistMsFor(assistTarget))}"):]
assert "assistMsFor(assistTarget))" not in s
rep("""const VEH_TIME_CAP = 0.5;
""", """const VEH_TIME_CAP = 0.5;
const BUILD_VER = '0.8.9';
const VP_PARTS = { truck: ['armor', 'engine', 'cargo'], drone: ['armor', 'engine', 'sensors'], atv: ['armor', 'engine', 'cargo'] };
const VP_NAMES = { armor: 'Armor', engine: 'Engine', cargo: 'Cargo', sensors: 'Sensors' };
const VP_SHORT = { truck: 'Truck', drone: 'Drone', atv: 'ATV' };
const VP_ROM = ['I', 'II', 'III'];
const VP_RP = [75, 150, 225];
const VP_RSUP = [25, 50, 75];
const VP_BUY = [25, 50, 75];
const VP_MS = [180000, 360000, 540000];
const VP_ENGINE = { truck: 0.05, drone: 0.05, atv: 0.10 };
const VP_CARGO = 0.05;
const VP_SENS = 0.03;
const VP_REPAIR_CUT = 0.33;
const VP_LOSS_CUT = 0.08;
""")

rep("""    (v.parts || []).forEach(pt => Object.keys(pt.fx || {}).forEach(k => { fx[k] = (fx[k] || 0) + pt.fx[k]; }));
""", """    (v.parts || []).forEach(pt => Object.keys(pt.fx || {}).forEach(k => { fx[k] = (fx[k] || 0) + pt.fx[k]; }));
    const E = vpFx(v.type);
    Object.keys(E).forEach(k => { fx[k] += E[k]; });
""")

rep("""function vehOf(id) { return state.vehicles.find(x => x.id === id); }
""", """function vehOf(id) { return state.vehicles.find(x => x.id === id); }

function vpNew() {
  const o = {};
  Object.keys(VP_PARTS).forEach(t => { o[t] = {}; VP_PARTS[t].forEach(p => { o[t][p] = { r: 0, b: 0 }; }); });
  return o;
}
function vpLoad(d) {
  const o = vpNew();
  Object.keys(o).forEach(t => Object.keys(o[t]).forEach(p => {
    const s = d && d[t] && d[t][p];
    if (!s) return;
    const r = Math.max(0, Math.min(3, (s.r | 0)));
    o[t][p].r = r;
    o[t][p].b = Math.max(0, Math.min(r, (s.b | 0)));
  }));
  return o;
}
function vpLv(t, p) { return state.vp && state.vp[t] && state.vp[t][p] ? state.vp[t][p].b : 0; }
function vpFx(t) {
  return {
    yield: VP_PARTS[t].includes('cargo') ? VP_CARGO * vpLv(t, 'cargo') : 0,
    cut: VP_PARTS[t].includes('sensors') ? VP_SENS * vpLv(t, 'sensors') : 0,
    time: VP_ENGINE[t] * vpLv(t, 'engine')
  };
}
function vehRepairFree(v) { return vpLv(v.type, 'armor') >= 3; }
function vehRepairCost(v) { return vehRepairFree(v) ? 0 : VEH_REPAIR_COST; }
function vehRepairMs(v) { return vehRepairFree(v) ? 0 : Math.round(VEH_REPAIR_MS * (1 - VP_REPAIR_CUT * vpLv(v.type, 'armor'))); }
function vehLossP(v) { return Math.max(0, VEH_LOSS_P - VP_LOSS_CUT * vpLv(v.type, 'armor')); }
function vpEffect(t, p) {
  if (p === 'armor') return 'Each level: repair time -' + Math.round(VP_REPAIR_CUT * 100) + '% (free at III), failed-assault loss -' + Math.round(VP_LOSS_CUT * 100) + ' pts.';
  if (p === 'engine') return 'Each level: mission time -' + Math.round(VP_ENGINE[t] * 100) + '%.';
  if (p === 'cargo') return 'Each level: yield +' + Math.round(VP_CARGO * 100) + '%.';
  return 'Each level: ambush -' + Math.round(VP_SENS * 100) + ' pts.';
}
function vpRunning(t, p) { return state.lab.projs.find(x => x.kind === 'vpart' && x.vt === t && x.pt === p); }
function vpLevels() {
  let n = 0;
  Object.keys(state.vp).forEach(t => Object.keys(state.vp[t]).forEach(p => { n += state.vp[t][p].r; }));
  return n;
}
function vpTotal() { return Object.keys(VP_PARTS).reduce((a, t) => a + VP_PARTS[t].length * 3, 0); }

function startVpartResearch(t, p) {
  const e = state.vp[t] && state.vp[t][p];
  if (!e || e.r >= 3 || e.r > e.b || !labCanStart() || vpRunning(t, p)) return;
  const rp = labCost(VP_RP[e.r]);
  const sup = labCost(VP_RSUP[e.r]);
  if (state.research < rp || state.res.supplies < sup) return;
  state.research -= rp;
  state.res.supplies -= sup;
  addProj({ kind: 'vpart', vt: t, pt: p, lv: e.r + 1, total: VP_MS[e.r], left: VP_MS[e.r] });
  sfx.chime();
  log(`Research started: ${VEH[t].name} ${VP_NAMES[p]} ${VP_ROM[e.r]}. Cost ${rp} research points and ${sup} supplies.`, 'ok');
  renderAll();
}

function buyVpart(t, p) {
  const e = state.vp[t] && state.vp[t][p];
  if (!e || e.b >= e.r || state.res.supplies < VP_BUY[e.b]) return;
  const c = VP_BUY[e.b];
  state.res.supplies -= c;
  e.b++;
  sfx.chime();
  log(`${VEH[t].name} ${VP_NAMES[p]} ${VP_ROM[e.b - 1]} fitted for ${c} supplies. It applies to every ${VP_SHORT[t].toLowerCase()}.`, 'ok');
  renderAll();
}

function vpHtml(k) {
  let h = '<h2 style="margin-top:14px">Vehicle parts</h2>';
  VP_PARTS[k].forEach(p => {
    const e = state.vp[k][p];
    let act;
    if (e.b >= 3) act = '<span class="ok">MAX</span>';
    else if (e.r > e.b) act = `<button onclick="buyVpart('${k}','${p}')" ${state.res.supplies < VP_BUY[e.b] ? 'disabled' : ''}>${VP_ROM[e.b]} // ${VP_BUY[e.b]} SUP</button>`;
    else if (vpRunning(k, p)) act = '<span class="warn">RESEARCHING</span>';
    else act = `<span class="dim">○ LAB: ${VP_ROM[e.r]}</span>`;
    h += `<div class="staff-row nob"><span><b>${VP_NAMES[p]}</b> <span class="dim">LEVEL ${e.b} / 3</span></span><span>${act}</span></div><div class="dim small" style="padding:0 0 6px;border-bottom:1px solid var(--steel-dim);text-align:left">${vpEffect(k, p)}</div>`;
  });
  return h;
}

function labVpHtml() {
  let h = '';
  Object.keys(VP_PARTS).forEach(t => VP_PARTS[t].forEach(p => {
    const e = state.vp[t][p];
    const run = vpRunning(t, p);
    let act;
    if (run) act = `<span class="warn">RESEARCHING <span data-lab="${run.id}">${fmt(projRealLeft(run))}</span></span>`;
    else if (e.r >= 3 && e.b >= 3) act = '<span class="ok">ALL FITTED</span>';
    else if (e.r > e.b) act = '<span class="ok">READY // BUY IN THE MOTOR POOL</span>';
    else {
      const rp = labCost(VP_RP[e.r]);
      const sup = labCost(VP_RSUP[e.r]);
      act = `<button style="white-space:nowrap" ${!labCanStart() || state.research < rp || state.res.supplies < sup ? 'disabled' : ''} onclick="startVpartResearch('${t}','${p}')">${VP_ROM[e.r]} // ${rp} RP // ${sup} SUP // ${fmt(VP_MS[e.r])}</button>`;
    }
    h += `<div class="staff-row nob"><span><b>${VP_SHORT[t]}: ${VP_NAMES[p]}</b> <span class="dim">LEVEL ${e.b} / 3 FITTED</span></span><span>${act}</span></div><div class="dim small" style="padding:0 0 6px;border-bottom:1px solid var(--steel-dim);text-align:left">${vpEffect(t, p)}</div>`;
  }));
  return h;
}
""")

rep("""      v.status = 'damaged';
      v.hit = false;
      mev(m.lid, `${vehName(v)} damaged in the ambush.`);
      log(`${vehName(v)} returned damaged. Repair costs ${VEH_REPAIR_COST} supplies and takes ${fmt(VEH_REPAIR_MS)}.`, 'warn');
""", """      v.hit = false;
      if (vehRepairFree(v)) {
        v.status = 'home';
        mev(m.lid, `${vehName(v)} damaged in the ambush. Armor III repaired it at no cost.`);
        log(`${vehName(v)} returned damaged and was repaired at no cost by Armor III.`, 'ok');
      } else {
        v.status = 'damaged';
        mev(m.lid, `${vehName(v)} damaged in the ambush.`);
        log(`${vehName(v)} returned damaged. Repair costs ${vehRepairCost(v)} supplies and takes ${fmt(vehRepairMs(v))}.`, 'warn');
      }
""")

rep("""    if (Math.random() < VEH_LOSS_P) {""", """    if (Math.random() < vehLossP(v)) {""")

rep("""  if (!v || v.status !== 'damaged' || state.res.supplies < VEH_REPAIR_COST) return;
  state.res.supplies -= VEH_REPAIR_COST;
  v.status = 'repairing';
  v.eta = Date.now() + VEH_REPAIR_MS;
  later(() => vehRepairDone(id), VEH_REPAIR_MS);
  log(`${vehName(v)} repair started: ${fmt(VEH_REPAIR_MS)}.`, '');
""", """  if (!v || v.status !== 'damaged' || state.res.supplies < vehRepairCost(v)) return;
  state.res.supplies -= vehRepairCost(v);
  const ms = vehRepairMs(v);
  if (ms <= 0) {
    v.status = 'home';
    v.eta = 0;
    log(`${vehName(v)} repaired at no cost.`, 'ok');
    renderAll();
    return;
  }
  v.status = 'repairing';
  v.eta = Date.now() + ms;
  later(() => vehRepairDone(id), ms);
  log(`${vehName(v)} repair started: ${fmt(ms)}.`, '');
""")

rep("""<button onclick="repairVehicle('${v.id}')" ${state.res.supplies < VEH_REPAIR_COST ? 'disabled' : ''}>REPAIR ${VEH_REPAIR_COST}</button>""", """<button onclick="repairVehicle('${v.id}')" ${state.res.supplies < vehRepairCost(v) ? 'disabled' : ''}>REPAIR ${vehRepairCost(v)}</button>""")

rep("""repair costs ${VEH_REPAIR_COST} supplies. A failed assault can lose them.</p>`;""", """repair costs ${VEH_REPAIR_COST} supplies, less with Armor parts. A failed assault can lose them. Parts are researched in the Lab, then fitted here.</p>`;""")

rep("""  return h;
}

function missionToken() {""", """  h += vpHtml(k);
  return h;
}

function missionToken() {""")

rep("""function projLabel(p) { return p.kind === 'gate' ?""", """function projLabel(p) { return p.kind === 'vpart' ? (VP_SHORT[p.vt] + ' ' + VP_NAMES[p.pt]).toUpperCase() + ' ' + VP_ROM[p.lv - 1] : p.kind === 'gate' ?""")

rep("""function projName(p) {
  const m = state.malps.find(x => x.id === p.malpId);
  return p.kind === 'gate' ?""", """function projName(p) {
  const m = state.malps.find(x => x.id === p.malpId);
  if (p.kind === 'vpart') return VEH[p.vt].name + ': ' + VP_NAMES[p.pt] + ' ' + VP_ROM[p.lv - 1];
  return p.kind === 'gate' ?""")

rep("""  if (p.kind === 'arm') return 'arm';
  if (p.tier === 4""", """  if (p.kind === 'arm' || p.kind === 'vpart') return 'arm';
  if (p.tier === 4""")

rep("""  if (p.kind === 'gate') {
    const T = GATE_TIERS[p.tier - 1];
    removeProj(p);""", """  if (p.kind === 'vpart') {
    state.vp[p.vt][p.pt].r = Math.max(state.vp[p.vt][p.pt].r, p.lv);
    removeProj(p);
    sfx.chime();
    log(`Research complete: ${VEH[p.vt].name} ${VP_NAMES[p.pt]} ${VP_ROM[p.lv - 1]}. Fit it in the Motor Pool for ${VP_BUY[p.lv - 1]} supplies.${note || ''}`, 'ok');
    renderAll();
    return;
  }
  if (p.kind === 'gate') {
    const T = GATE_TIERS[p.tier - 1];
    removeProj(p);""")

rep("""    { k: 'alien', name: 'ALIEN TECH',""", """    { k: 'veh', name: 'VEHICLE PARTS', sub: running('vpart') ? 'RESEARCHING' : vpLevels() + ' / ' + vpTotal() + ' LEVELS', cls: running('vpart') ? 'warn' : (vpLevels() ? 'ok' : 'dim') },
    { k: 'alien', name: 'ALIEN TECH',""")

rep("""  } else if (sel === 'arm') right += labArmHtml();""", """  } else if (sel === 'arm') right += labArmHtml();
  else if (sel === 'veh') right += labVpHtml();""")

rep("""    vehicles: [],
    selVeh: [],
    vehSeq: 0,""", """    vehicles: [],
    vp: vpNew(),
    selVeh: [],
    vehSeq: 0,""")

rep("""    vehSeq: state.vehSeq,
""", """    vehSeq: state.vehSeq,
    vp: state.vp,
""")

rep("""    fmt: 1,
    savedAt:""", """    fmt: 1,
    build: BUILD_VER,
    savedAt:""")

rep("""  state.vehSeq = d.vehSeq || 0;""", """  state.vehSeq = d.vehSeq || 0;
  state.vp = vpLoad(d.vp);""")

rep("""#titlescreen, #menu, #settings {
  position: fixed;""", """#titlescreen, #menu, #settings, #xfer {
  position: fixed;""")
rep("""#settings { z-index: 120; background: rgba(2, 6, 12, 0.96); }
#titlescreen[hidden], #menu[hidden], #settings[hidden] { display: none; }""", """#settings { z-index: 120; background: rgba(2, 6, 12, 0.96); }
#xfer { z-index: 130; background: #02060c; }
#titlescreen[hidden], #menu[hidden], #settings[hidden], #xfer[hidden] { display: none; }""")

rep("""<div id="tour" hidden>
  <div id="tourhi" hidden></div>""", """<div id="xfer" hidden>
  <div class="titlebox">
    <div class="title" style="font-size:16px">SAVE FILES</div>
    <div class="sub">EXPORT AND IMPORT</div>
    <div class="panel" id="xferbody"></div>
    <input type="file" id="xferfile" accept=".json,application/json" hidden onchange="xferRead(this)">
  </div>
</div>
<div id="tour" hidden>
  <div id="tourhi" hidden></div>""")

rep(""": ''}<button onclick="openSettings()">SETTINGS</button></div>""", """: ''}<button onclick="openSettings()">SETTINGS</button><button onclick="openXfer()">SAVE FILES</button></div>""")

rep("""    <h2 style="margin-top:16px">Keyboard shortcuts</h2>${keys}""", """    <h2 style="margin-top:16px">Save files</h2><div class="controls" style="justify-content:flex-start"><button onclick="openXfer()">EXPORT / IMPORT SAVES</button></div>
    <h2 style="margin-top:16px">Keyboard shortcuts</h2>${keys}""")

rep("""    if (!$('settings').hidden) closeSettings();
    else if (state.started""", """    if (!$('xfer').hidden) closeXfer();
    else if (!$('settings').hidden) closeSettings();
    else if (state.started""")
rep("""  if (!$('settings').hidden) return;
  const k = e.key.toLowerCase();""", """  if (!$('settings').hidden || !$('xfer').hidden) return;
  const k = e.key.toLowerCase();""")

rep("""function toggleFullscreen() {""", """let xferState = { items: [], msg: '' };

function buildNum(s) {
  const a = String(s || '0').split('.');
  return (parseInt(a[0], 10) || 0) * 1000000 + (parseInt(a[1], 10) || 0) * 1000 + (parseInt(a[2], 10) || 0);
}

function vetSave(d) {
  if (!d || typeof d !== 'object' || d.fmt !== 1) return { ok: false, why: 'NOT A VALID SAVE' };
  const good = Array.isArray(d.teams) && Array.isArray(d.worlds) && Array.isArray(d.usedNames) && d.res && typeof d.res === 'object' && d.meta && typeof d.meta === 'object' && d.seqs && typeof d.seqs === 'object' && typeof d.savedAt === 'string' && typeof d.steps === 'number' && d.target !== undefined && d.planet !== undefined && d.level >= 1 && d.logs !== undefined;
  if (!good) return { ok: false, why: 'SAVE DATA INCOMPLETE' };
  if (buildNum(d.build) > buildNum(BUILD_VER)) return { ok: false, why: 'BLOCKED // MADE IN BUILD ' + d.build + ', NEWER THAN ' + BUILD_VER };
  return { ok: true, old: buildNum(d.build) < buildNum(BUILD_VER) };
}

function xferInfo(d) {
  const when = new Date(d.savedAt).toLocaleString([], { hour12: false });
  return `LEVEL ${d.meta.level} // ${d.meta.supplies} SUPPLIES // ${d.meta.teams} TEAMS // ${when}`;
}

function xferDownload(name, obj) {
  try {
    const b = new Blob([JSON.stringify(obj)], { type: 'application/json' });
    const u = URL.createObjectURL(b);
    const a = document.createElement('a');
    a.href = u;
    a.download = name;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(u), 4000);
    return true;
  } catch (e) { return false; }
}

function exportSlots(list) {
  if (state.started) autosaveNow();
  const saves = {};
  list.forEach(sl => { const d = readSave(sl); if (d) saves[sl] = d; });
  const keys = Object.keys(saves);
  if (!keys.length) { xferState.msg = 'NOTHING TO EXPORT'; renderXfer(); return; }
  const stamp = new Date().toISOString().slice(0, 10);
  const name = list.length === 1 ? 'sgc-command-' + (list[0] === 'auto' ? 'autosave' : 'slot-' + list[0]) + '-' + stamp + '.json' : 'sgc-command-saves-' + stamp + '.json';
  const ok = xferDownload(name, { sgcSaveBundle: 1, build: BUILD_VER, exportedAt: new Date().toISOString(), saves });
  xferState.msg = ok ? 'EXPORTED ' + keys.length + ' SAVE' + (keys.length === 1 ? '' : 'S') + ' TO ' + name : 'EXPORT FAILED IN THIS BROWSER';
  renderXfer();
}

function xferRead(inp) {
  const f = inp.files && inp.files[0];
  inp.value = '';
  if (!f) return;
  if (f.size > 30000000) { xferState = { items: [], msg: 'THAT FILE IS TOO LARGE TO BE A SAVE' }; renderXfer(); return; }
  const r = new FileReader();
  r.onload = () => xferParse(String(r.result), f.name);
  r.onerror = () => { xferState = { items: [], msg: 'THE FILE COULD NOT BE READ' }; renderXfer(); };
  r.readAsText(f);
}

function xferParse(txt, fname) {
  let o;
  try { o = JSON.parse(txt); } catch (e) { xferState = { items: [], msg: 'THAT FILE IS NOT A SAVE FILE' }; renderXfer(); return; }
  let ent = [];
  if (o && o.sgcSaveBundle === 1 && o.saves && typeof o.saves === 'object') ent = Object.keys(o.saves).slice(0, 8).map(k => [k, o.saves[k]]);
  else if (o && o.fmt === 1) ent = [[String(o.label || 'imported'), o]];
  if (!ent.length) { xferState = { items: [], msg: 'NO SAVES FOUND IN THAT FILE' }; renderXfer(); return; }
  const free = SAVE_SLOTS.filter(sl => !slotInfo(sl));
  const used = new Set();
  const items = ent.map(([k, d]) => ({ key: k, d, v: vetSave(d), target: '' }));
  items.forEach(it => { if (it.v.ok && SAVE_SLOTS.includes(it.key) && free.includes(it.key) && !used.has(it.key)) { it.target = it.key; used.add(it.key); } });
  items.forEach(it => { if (it.v.ok && !it.target) { it.target = free.find(s => !used.has(s)) || ''; if (it.target) used.add(it.target); } });
  xferState = { items, msg: '', file: fname };
  renderXfer();
}

function xferSet(i, v) {
  if (xferState.items[i]) xferState.items[i].target = v;
  renderXfer();
}

function xferImport() {
  const picks = xferState.items.filter(it => it.v.ok && it.target);
  const seen = new Set();
  for (const it of picks) {
    if (seen.has(it.target)) { xferState.msg = 'TWO SAVES CHOSE THE SAME SLOT. NOTHING WAS IMPORTED.'; renderXfer(); return; }
    seen.add(it.target);
  }
  let n = 0;
  picks.forEach(it => {
    if (slotInfo(it.target)) return;
    if (storeSet(it.target, JSON.stringify(Object.assign({}, it.d, { label: it.target })))) { n++; it.done = true; }
  });
  xferState.items = xferState.items.filter(it => !it.done);
  xferState.msg = n ? 'IMPORTED ' + n + ' SAVE' + (n === 1 ? '' : 'S') + '. USE RESUME ON THE TITLE SCREEN TO PLAY ' + (n === 1 ? 'IT' : 'THEM') + '.' : 'NOTHING WAS IMPORTED';
  if (!$('titlescreen').hidden) renderTitle();
  if (!$('menu').hidden) renderMenu();
  renderXfer();
}

function renderXfer() {
  const rows = SAVE_SLOTS.map(sl => {
    const d = readSave(sl);
    return `<div class="dispatch-row"><div><b>${slotName(sl)}</b><div class="dim mrow">${d ? xferInfo(d) : 'EMPTY'}</div></div><button ${d ? '' : 'disabled'} onclick="exportSlots(['${sl}'])">EXPORT</button></div>`;
  }).join('');
  const any = SAVE_SLOTS.some(sl => readSave(sl));
  const free = SAVE_SLOTS.filter(sl => !slotInfo(sl));
  const items = xferState.items.map((it, i) => {
    const nm = SAVE_SLOTS.includes(it.key) ? slotName(it.key) : 'SAVE';
    if (!it.v.ok) return `<div class="dispatch-row"><div><b>${nm}</b><div class="warn mrow">${it.v.why}</div></div><span class="dim">SKIPPED</span></div>`;
    const opts = '<option value="">DO NOT IMPORT</option>' + free.map(sl => `<option value="${sl}"${it.target === sl ? ' selected' : ''}>${slotName(sl)}</option>`).join('');
    return `<div class="dispatch-row"><div><b>${nm}</b><div class="dim mrow">${xferInfo(it.d)} // ${it.d.build ? 'BUILD ' + it.d.build : 'EARLIER BUILD'}${it.v.old ? ' // UPGRADED ON LOAD' : ''}</div></div><select class="msel" onchange="xferSet(${i},this.value)">${opts}</select></div>`;
  }).join('');
  const canImp = xferState.items.some(it => it.v.ok && it.target);
  $('xferbody').innerHTML = `<h2>Export</h2>${rows}
    <div class="controls" style="margin-top:10px"><button ${any ? '' : 'disabled'} onclick="exportSlots(SAVE_SLOTS)">EXPORT ALL SAVES</button></div>
    <h2 style="margin-top:16px">Import</h2>
    <p class="dim small">Imports go into empty slots only. Saves from a newer build are blocked. Saves from an earlier build are accepted and upgraded when loaded.</p>
    <div class="controls" style="justify-content:flex-start"><button onclick="document.getElementById('xferfile').click()">CHOOSE SAVE FILE</button>${canImp ? '<button onclick="xferImport()">IMPORT</button>' : ''}</div>
    ${xferState.file ? `<p class="dim small">FILE // ${xferState.file.replace(/[<>&"]/g, '')}</p>` : ''}
    ${items}
    ${free.length || !xferState.items.length ? '' : '<p class="warn small">No empty slots to import into.</p>'}
    ${xferState.msg ? `<p class="ok small">${xferState.msg.replace(/[<>&]/g, '')}</p>` : ''}
    <div class="controls" style="margin-top:14px"><button onclick="closeXfer()">CLOSE</button></div>`;
}

function openXfer() { xferState = { items: [], msg: '' }; renderXfer(); $('xfer').hidden = false; }
function closeXfer() { $('xfer').hidden = true; }

function toggleFullscreen() {""")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
