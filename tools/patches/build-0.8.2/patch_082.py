import re, sys

src = open('base.html', encoding='utf-8').read()


def rep(old, new, count=1):
    global src
    n = src.count(old)
    if n != count:
        print('MISMATCH', n, 'for', old[:90])
        sys.exit(1)
    src = src.replace(old, new)


rep('<title>Stargate Command 0.8.1</title>', '<title>Stargate Command 0.8.2</title>')
rep('BUILD 0.8.1</div>', 'BUILD 0.8.2</div>', 2)

rep("    fac: { pts: {}, next: {}, freeRepl: {} },\n", "    fac: { pts: {}, next: {}, freeRepl: {}, met: {} },\n")
rep("    fac: { pts: state.fac.pts, freeRepl: state.fac.freeRepl, nextLeft:", "    fac: { pts: state.fac.pts, freeRepl: state.fac.freeRepl, met: state.fac.met, nextLeft:")
rep("  state.fac = { pts: Object.assign({}, sf.pts), freeRepl: Object.assign({}, sf.freeRepl), next: {} };\n",
    "  state.fac = { pts: Object.assign({}, sf.pts), freeRepl: Object.assign({}, sf.freeRepl), next: {}, met: Object.assign({}, sf.met) };\n"
    "  Object.keys(FACTIONS).forEach(n => { if (!state.fac.met[n] && facKnown(n)) state.fac.met[n] = { t: '', by: '' }; });\n")

rep("function facKnown(n) {",
    "function factionContact(w, by, mid) {\n"
    "  if (!w || w.kind !== 'faction' || !w.faction || !state.fac) return;\n"
    "  if (!state.fac.met) state.fac.met = {};\n"
    "  const n = w.faction;\n"
    "  if (state.fac.met[n]) return;\n"
    "  state.fac.met[n] = { t: clock(), by };\n"
    "  const msg = `${by} discovered the ${n}. The ${n} seemed open to diplomacy.`;\n"
    "  log(msg, 'ok');\n"
    "  if (mid) mev(mid, msg);\n"
    "}\n\n"
    "function facKnown(n) {")

rep("Survey tier ${lvl} received: ${w.name}, ${w.type.toLowerCase()}.`, 'ok');\n",
    "Survey tier ${lvl} received: ${w.name}, ${w.type.toLowerCase()}.`, 'ok');\n  if (w.intel >= 2) factionContact(w, 'The MALP', m.lid);\n")
rep("    w.intel = Math.max(w.intel, op && op.intel5 ? 5 : 4);\n",
    "    w.intel = Math.max(w.intel, op && op.intel5 ? 5 : 4);\n    factionContact(w, t.name, m.lid);\n")
rep("    if (w.intel < tier) w.intel = tier;\n",
    "    if (w.intel < tier) w.intel = tier;\n    if (w.intel >= 2) factionContact(w, ok.map(a => a.name).join(', '), null);\n")
rep("  if (t.type === 'exp') {\n    if (m.forced) {",
    "  if (t.type === 'exp') {\n    if (w.kind === 'faction') {\n      if (w.intel < 2) w.intel = 2;\n      factionContact(w, t.name, m.lid);\n    }\n    if (m.forced) {")

rep("  const n = list[+sel.slice(1)];\n  const F = FACTIONS[n];\n",
    "  const n = list[+sel.slice(1)];\n  const F = FACTIONS[n];\n  const mt = state.fac.met && state.fac.met[n];\n"
    "  const metLine = mt && mt.by ? `<div class=\"dim mrow\">First contact [${mt.t}] // ${mt.by}</div>` : '';\n")
rep("${pay}</div></div>`;\n}", "${pay}${metLine}</div></div>`;\n}")

rep("  return { name: t.name, type: t.type, cam: t.cam, members:", "  return { id: t.id, name: t.name, type: t.type, cam: t.cam, members:")

aar_js = r'''
const AAR_KINDS = ['exp', 'rec', 'assist', 'assault'];
const AAR_CPS = 175 / 60;
const AAR_ACC_MIN = 0.7;
const AAR_ACC_STD = 0.85;
const AAR_ACC_EXC = 0.95;
const AAR_REW = [
  { name: 'ROUGH', sup: 5, rp: 5, cam: 2 },
  { name: 'STANDARD', sup: 10, rp: 10, cam: 4 },
  { name: 'EXCELLENT', sup: 15, rp: 15, cam: 6 }
];
let AARG = null;

function aarEligible(r) { return !!r && r.state === 'closed' && AAR_KINDS.includes(r.kind) && !r.aar; }
function aarEsc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;'); }
function aarNames(a) { return a.length ? a.join(', ') : 'None'; }
function aarWho(r, sts) {
  const out = [];
  (r.ret || []).forEach(c => c.members.forEach(m => { if (sts.includes(m.status)) out.push(m.name); }));
  return out;
}
function aarFields(r) {
  const y = r.yield || {};
  const w = world(r.worldId);
  const iEnd = r.intelEnd === null ? (w ? w.intel : r.intelStart) : r.intelEnd;
  return [
    { k: 'type', label: 'Mission type', hint: 'As shown in the mission log header', exp: KLABEL[r.kind] },
    { k: 'launched', label: 'Launch time', hint: 'Launched, in the summary', exp: r.started },
    { k: 'ended', label: 'Return time', hint: 'Ended, in the summary', exp: r.ended || '' },
    { k: 'teams', label: 'Team', hint: 'Team names separated by commas', exp: r.launch.map(c => c.name).join(', ') },
    { k: 'world', label: 'World', hint: 'World name from the summary', exp: r.world },
    { k: 'inj', label: 'Injuries', hint: 'Names separated by commas, or None', exp: aarNames(aarWho(r, ['injured'])) },
    { k: 'cas', label: 'Casualties', hint: 'Killed or captured, names separated by commas, or None', exp: aarNames(aarWho(r, ['killed', 'captured'])) },
    { k: 'yield', label: 'Yield', hint: 'Supplies 0, Naquadah 0, Research 0 with the log values', exp: `Supplies ${y.supplies || 0}, Naquadah ${y.naquadah || 0}, Research ${y.research || 0}` },
    { k: 'intel', label: 'Intel tier', hint: 'Format: 1 to 3', exp: `${r.intelStart} to ${iEnd}` }
  ];
}
function aarNorm(s) { return String(s || '').toLowerCase().replace(/\s+/g, ' ').trim(); }
function aarDist(a, b) {
  const m = a.length, n = b.length;
  let prev = [];
  for (let j = 0; j <= n; j++) prev.push(j);
  for (let i = 1; i <= m; i++) {
    const cur = [i];
    for (let j = 1; j <= n; j++) cur.push(Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1)));
    prev = cur;
  }
  return prev[n];
}
function aarLen(r) { return aarFields(r).reduce((s, f) => s + Math.max(1, aarNorm(f.exp).length), 0); }
function aarPar(r) { return Math.max(15, Math.round(aarLen(r) / AAR_CPS)); }
function aarScore(r, vals) {
  let dist = 0, len = 0;
  const rows = aarFields(r).map(f => {
    const e = aarNorm(f.exp), v = aarNorm(vals[f.k]);
    const d = aarDist(e, v);
    dist += d;
    len += Math.max(1, e.length);
    return { f, ok: d === 0, typed: vals[f.k] || '' };
  });
  return { acc: Math.max(0, 1 - dist / len), rows };
}
function aarTierOf(acc, secs, par) {
  if (acc >= AAR_ACC_EXC && secs <= par) return 2;
  if (acc >= AAR_ACC_STD && secs <= par * 2) return 1;
  if (acc >= AAR_ACC_MIN) return 0;
  return -1;
}
function aarReset() {
  if (AARG && AARG.iv) clearInterval(AARG.iv);
  AARG = null;
}
function aarOpen(id) {
  const r = mfind(id);
  if (!aarEligible(r)) return;
  aarReset();
  AARG = { id, vals: {}, t0: null, res: null };
  AARG.iv = setInterval(aarTick, 250);
  state.viewMission = id;
  renderRoom();
}
function aarCancel() {
  aarReset();
  renderRoom();
}
function aarTick() {
  const el = $('aartime');
  if (!el || !AARG || AARG.res) return;
  el.textContent = fmt(AARG.t0 ? performance.now() - AARG.t0 : 0);
}
function aarInput(k, v) {
  if (!AARG || AARG.res) return;
  if (AARG.t0 === null) AARG.t0 = performance.now();
  AARG.vals[k] = v;
}
function aarRetry() {
  if (!AARG) return;
  AARG.vals = {};
  AARG.t0 = null;
  AARG.res = null;
  if (!AARG.iv) AARG.iv = setInterval(aarTick, 250);
  renderRoom();
}
function aarSubmit() {
  if (!AARG || AARG.res) return;
  const r = mfind(AARG.id);
  if (!aarEligible(r)) { aarCancel(); return; }
  const sc = aarScore(r, AARG.vals);
  const secs = AARG.t0 === null ? 0 : (performance.now() - AARG.t0) / 1000;
  const par = aarPar(r);
  const tier = AAR_TIERS_SAFE(sc.acc, secs, par);
  AARG.res = { sc, secs, par, tier, cams: [] };
  if (AARG.iv) { clearInterval(AARG.iv); AARG.iv = null; }
  if (tier >= 0) {
    const R = AAR_REW[tier];
    state.res.supplies += R.sup;
    state.research += R.rp;
    r.launch.forEach(c => {
      if (c.type === 'exp' || c.type === 'dip') return;
      const t = state.teams.find(x => x.id === c.id) || state.teams.find(x => x.name === c.name);
      if (t && !noCam(t)) { addCam(t, R.cam); AARG.res.cams.push(t.name); }
    });
    const pct = Math.round(sc.acc * 100);
    r.aar = { tier, acc: pct, secs: Math.round(secs), par };
    const msg = `After-action report filed for ${r.id}: ${R.name}, ${pct}% accurate in ${fmt(secs * 1000)} (par ${fmt(par * 1000)}). +${R.sup} supplies, +${R.rp} research points` + (AARG.res.cams.length ? `, +${R.cam} camaraderie for ${AARG.res.cams.join(', ')}` : '') + '.';
    mev(r.id, msg);
    log(msg, 'ok');
    sfx.chime();
  } else {
    sfx.fail();
  }
  renderAll();
}
function AAR_TIERS_SAFE(acc, secs, par) { return aarTierOf(acc, secs, par); }
function aarFormHtml(r) {
  const fs = aarFields(r);
  const par = aarPar(r);
  let h = `<h2>After-action report // ${r.id}</h2>`;
  if (AARG.res) {
    const R = AARG.res;
    const pct = Math.round(R.sc.acc * 100);
    if (R.tier < 0) {
      h += `<p class="danger">REPORT REJECTED // ${pct}% accurate. A report needs ${Math.round(AAR_ACC_MIN * 100)}% to be accepted. There is no penalty and nothing was spent.</p>`;
    } else {
      const C = AAR_REW[R.tier];
      h += `<p class="ok">REPORT ACCEPTED // ${C.name} // ${pct}% accurate // ${fmt(R.secs * 1000)} against a par of ${fmt(R.par * 1000)}</p>`;
      h += `<div class="mrow ok">+${C.sup} supplies, +${C.rp} research points${R.cams.length ? `, +${C.cam} camaraderie for ${R.cams.join(', ')}` : '. No camaraderie: Exploration teams do not earn it.'}</div>`;
    }
    const bad = R.sc.rows.filter(x => !x.ok);
    if (bad.length) {
      h += '<div class="mrow dim" style="margin-top:6px">Corrections</div>';
      h += bad.map(x => `<div class="mrow warn">${x.f.label}: typed "${aarEsc(x.typed) || '(blank)'}", expected "${aarEsc(x.f.exp)}"</div>`).join('');
    }
    h += '<div class="controls" style="justify-content:flex-start;margin-top:10px">' + (R.tier < 0 ? '<button onclick="aarRetry()">TRY AGAIN</button> ' : '') + `<button onclick="aarCancel()">${R.tier < 0 ? 'CANCEL' : 'DONE'}</button></div>`;
    return h;
  }
  h += '<p class="dim small">Optional. Type the report from the mission details on the right. The clock starts at your first keystroke. Capital letters do not matter.</p>';
  h += `<div class="res-row"><span>TIME <b id="aartime">${fmt(AARG.t0 ? performance.now() - AARG.t0 : 0)}</b></span><span class="dim">PAR ${fmt(par * 1000)}</span></div>`;
  h += fs.map(f => `<div class="aarf"><div class="dim small">${f.label} <span style="opacity:.6">// ${f.hint}</span></div><input class="nm aari" id="aar-${f.k}" autocomplete="off" spellcheck="false" value="${aarEsc(AARG.vals[f.k])}" oninput="aarInput('${f.k}', this.value)"></div>`).join('');
  h += '<div class="controls" style="justify-content:flex-start;margin-top:10px"><button onclick="aarSubmit()">SUBMIT REPORT</button> <button onclick="aarCancel()">CANCEL</button></div>';
  return h;
}

function aarPersRows(r, row) {
  if (r.state !== 'closed' || !(r.ret || []).length) return '';
  return row('Injured', aarNames(aarWho(r, ['injured']))) + row('Killed or captured', aarNames(aarWho(r, ['killed', 'captured'])));
}

'''
aar_js = aar_js.replace("const tier = AAR_TIERS_SAFE(sc.acc, secs, par);", "const tier = aarTierOf(sc.acc, secs, par);")
aar_js = aar_js.replace("function AAR_TIERS_SAFE(acc, secs, par) { return aarTierOf(acc, secs, par); }\n", "")

rep("function briefRoomHtml(here) {", aar_js.lstrip('\n') + "function briefRoomHtml(here) {")

rep("  right = mr ? `<div class=\"scroll mdetail\">${missionDetailHtml(mr)}</div>` : missionLogHtml();\n",
    "  if (AARG && (!mr || mr.id !== AARG.id || (!AARG.res && !aarEligible(mr)))) aarReset();\n"
    "  if (AARG) left = aarFormHtml(mr);\n"
    "  right = mr ? `<div class=\"scroll mdetail\">${missionDetailHtml(mr)}</div>` : missionLogHtml();\n")

rep("function closeMissionLog() { state.viewMission = null; renderRoom(); }",
    "function closeMissionLog() { aarReset(); state.viewMission = null; renderRoom(); }")

rep("<button onclick=\"closeMissionLog()\">BACK</button></div>`;\n",
    "<button onclick=\"closeMissionLog()\">BACK</button></div>`;\n"
    "  if (aarEligible(r)) h += `<div class=\"controls\" style=\"justify-content:flex-start\"><button onclick=\"aarOpen('${r.id}')\" ${AARG && AARG.id === r.id ? 'disabled' : ''}>COMPLETE AAR</button> <span class=\"dim small\">Optional typing report for a reward.</span></div>`;\n"
    "  else if (r.aar) h += row('After-action report', `${AAR_REW[r.aar.tier].name} // ${r.aar.acc}% // ${fmt(r.aar.secs * 1000)}`);\n")
rep("row('Flags', flags) + ", "row('Flags', flags) + aarPersRows(r, row) + ")

old_stats = """  if (r.launch.length) {
    h += '<h2 style="margin-top:10px">Team stats at launch</h2>' + crewHtml(r.launch);
    h += '<h2 style="margin-top:10px">Team stats at return</h2>' + (r.ret.length ? crewHtml(r.ret) : '<p class="dim">Not returned yet.</p>');
  }
"""
rep(old_stats, "")

rep("</style>", ".aarf { margin: 6px 0; }\n.aarf input.nm { width: 100%; }\n</style>")

open('sgc-command-0.8.2.html', 'w', encoding='utf-8').write(src)
print('ok', len(src))
