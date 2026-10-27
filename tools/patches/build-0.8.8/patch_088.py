import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
assert s.count('0.8.7') == 3
s = s.replace('0.8.7', '0.8.8')
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
rep("""  const gate = document.body.classList.contains('gv');
  let wc = FIT.W;
  st.style.width = wc + 'px';
  st.style.transform = 'scale(1)';
  const h = gate ? st.offsetHeight : FIT.H.base;
  const s = Math.max(FIT.min, Math.min(FIT.max, window.innerWidth / wc, window.innerHeight / h));
  if (window.innerWidth / s < wc) { wc = window.innerWidth / s; st.style.width = wc + 'px'; }
  FIT.s = s;
  st.style.transform = 'scale(' + s + ')';""",
"""  const gate = document.body.classList.contains('gv');
  const m = $('smbox');
  const dw = $('dcwrap');
  FIT.lock = 0;
  if (m) m.style.maxWidth = '';
  if (dw) dw.style.maxWidth = '';
  st.style.width = FIT.W + 'px';
  st.style.transform = 'scale(1)';
  FIT.s = 1;
  if (gate) fitStarmap();
  const h = gate ? st.offsetHeight : FIT.H.base;
  const s = Math.max(FIT.min, Math.min(FIT.max, window.innerWidth / FIT.W, window.innerHeight / h));
  const wc = window.innerWidth / s;
  if (gate && m) FIT.lock = m.offsetWidth;
  if (gate && dw) dw.style.maxWidth = dw.offsetWidth + 'px';
  st.style.width = wc + 'px';
  FIT.s = s;
  if (gate) fitStarmap();
  st.style.transform = 'scale(' + s + ')';""")
rep("""  if (h > 120) m.style.maxWidth = Math.floor(h * 800 / 560) + 'px';
}""", """  if (h > 120) m.style.maxWidth = Math.floor(h * 800 / 560) + 'px';
  if (FIT.lock) m.style.maxWidth = Math.min(parseFloat(m.style.maxWidth) || 1e9, FIT.lock) + 'px';
}""")

rep("""function missionBuilderHtml() {""", """const MT_SHORT = {
  exp: 'Needs an Exploration team. Recon and Security may join.',
  rec: 'Recon teams only. Surveys the world for intel.',
  asl: 'Known stronghold. Assault, Security, Recon. Exploration recovers tech.',
  def: 'Security or Assault to a treaty world under raid alert.',
  ast: 'Recon, Assault or Security to rescue an overdue team.',
  dip: 'One Diplomat team plus Security to a faction or treaty world.'
};

function grpOf(t) { return (state.groups || []).find(g => g.ids.includes(t.id)); }
function grpTeams(g) { return g.ids.map(id => state.teams.find(x => x.id === id)).filter(Boolean); }
function grpReady(g) { const ts = grpTeams(g); return ts.length > 1 && ts.every(teamReady); }
function grpPrune() {
  state.groups = (state.groups || []).filter(g => { g.ids = g.ids.filter(id => state.teams.some(t => t.id === id)); if (!g.ids.includes(g.lead)) g.lead = g.ids[0]; return g.ids.length > 0; });
}

function newGroup(tid) {
  const t = state.teams.find(x => x.id === tid);
  if (!t || t.status === 'away' || grpOf(t)) return;
  state.grpSeq = (state.grpSeq || 0) + 1;
  state.grpN = state.grpN || {};
  state.grpN[t.type] = (state.grpN[t.type] || 0) + 1;
  state.groups = (state.groups || []).concat([{ id: 'g' + state.grpSeq, name: TYPES[t.type].name + ' Group ' + state.grpN[t.type], lead: t.id, ids: [t.id] }]);
  renderAll();
}

function joinGroup(tid, gid) {
  const t = state.teams.find(x => x.id === tid);
  const g = (state.groups || []).find(x => x.id === gid);
  if (!t || !g || t.status === 'away' || grpOf(t)) return;
  g.ids.push(tid);
  renderAll();
}

function unlinkTeam(tid) {
  const t = state.teams.find(x => x.id === tid);
  const g = t && grpOf(t);
  if (!g || t.status === 'away') return;
  g.ids = g.ids.filter(x => x !== tid);
  grpPrune();
  renderAll();
}

function renameGroup(gid, v) {
  const g = (state.groups || []).find(x => x.id === gid);
  const n = cleanName(v);
  if (g && n) g.name = n;
  renderAll();
}

function groupBoxHtml(t) {
  grpPrune();
  const g = grpOf(t);
  const here = t.status !== 'away';
  let h = `<h2 style="margin-top:12px">Linked group // ${t.name}</h2>`;
  if (g) {
    const ts = grpTeams(g);
    const rd = grpReady(g);
    const st = ts.length < 2 ? '<span class="dim">Link a second team to form the group.</span>' : (rd ? '<span class="ok">LINKED // READY AS A GROUP</span>' : '<span class="warn">BROKEN // a member is away or standing down. Ready members can be sent unlinked.</span>');
    h += `<div class="dispatch-row"><div><input class="nm tn" maxlength="26" value="${g.name}" onchange="renameGroup('${g.id}', this.value)"><div class="dim mrow">${ts.map(x => x.name + (x.id === g.lead ? ' (lead)' : '') + (teamReady(x) ? '' : ' // not ready')).join(', ')}</div><div class="mrow">${st}</div></div><button ${here ? '' : 'disabled'} onclick="unlinkTeam('${t.id}')">UNLINK</button></div>`;
  } else {
    const gs = state.groups || [];
    h += `<div class="controls" style="justify-content:flex-start;flex-wrap:wrap;gap:6px"><button ${here ? '' : 'disabled'} onclick="newGroup('${t.id}')">NEW GROUP</button>${gs.map(x => `<button ${here ? '' : 'disabled'} onclick="joinGroup('${t.id}', '${x.id}')">JOIN ${x.name.toUpperCase()}</button>`).join('')}</div>`;
  }
  h += '<p class="dim small help">Linked teams are added to a mission together as one asset, and other teams, vehicles and a MALP can be added alongside. Link and unlink only while the team is on station.</p>';
  return h;
}

function mpStep(n) { state.mStep = Math.max(0, Math.min(2, n)); renderGate(); }
function mpTab(k) { state.mTab = k; renderGate(); }
function togTeam(id) { if (state.sel.includes(id)) removeTeam(id); else addTeam(id); }
function togVeh(id) { if (state.selVeh.includes(id)) removeVeh(id); else addVeh(id); }
function togMalp(id) { const mp = selMalp(); if (state.withMalp && mp && mp.id === id) removeMalp(); else addMalp(id); }
function togGroup(gid) {
  const g = (state.groups || []).find(x => x.id === gid);
  if (!g || !grpReady(g)) return;
  const ids = g.ids;
  if (ids.every(id => state.sel.includes(id))) state.sel = state.sel.filter(id => !ids.includes(id));
  else ids.forEach(id => { if (!state.sel.includes(id)) state.sel.push(id); });
  renderGate();
}

function repeatLast() {
  const L = state.lastMission;
  if (!L || !MTYPES[L.mt]) return;
  state.mType = L.mt;
  const miss = [];
  state.sel = [];
  L.ids.forEach(id => { const t = state.teams.find(x => x.id === id); if (t && teamReady(t) && mtypeOk(t, L.mt)) state.sel.push(id); else if (t) miss.push(t.name); });
  state.selVeh = [];
  L.veh.forEach(id => { const v = vehOf(id); if (v && v.status === 'home' && state.selVeh.length < VEH_PER_SEND) state.selVeh.push(id); else if (v) miss.push(vehName(v)); });
  state.withMalp = false;
  if (L.malp) {
    const m = state.malps.find(x => x.id === L.malp && x.status === 'home') || state.malps.find(x => x.status === 'home');
    if (m) { state.withMalp = true; state.malpPick = m.id; } else miss.push('MALP');
  }
  state.repeatNote = miss.length ? 'Not available for this send: ' + miss.join(', ') + '.' : '';
  state.mStep = 2;
  renderGate();
}

function mpRow(ic, name, info, on, fn, dis) {
  return `<div class="mprow"><span class="mpic">${ic}</span><span class="mpg"><b>${name}</b> <span class="dim">${info}</span></span><button class="${on ? 'on' : ''}" ${dis && !on ? 'disabled' : ''} onclick="${fn}">${on ? '✓ ADDED' : 'ADD'}</button></div>`;
}

function missionPanelHtml(g, sel, canSend, nt) {
  const mt = state.mType || 'exp';
  const st = state.mStep || 0;
  const mp = selMalp();
  const malpIn = state.withMalp && !!mp;
  const vs = state.selVeh.map(vehOf).filter(v => v && v.status === 'home');
  const steps = ['1 // TYPE', '2 // ASSETS', '3 // REVIEW'];
  let h = `<div class="mpsteps">${steps.map((x, i) => `<button class="${st === i ? 'on' : (i < st ? 'done' : '')}" onclick="mpStep(${i})">${i < st ? '✓ ' : ''}${x}</button>`).join('')}</div><div class="mpbody">`;
  if (st === 0) {
    h += `<div class="mptypes">${Object.keys(MTYPES).map(k => `<div class="mptc${mt === k ? ' on' : ''}" onclick="setMType('${k}')"><b>${MTYPES[k][0]}</b><span>${MT_SHORT[k]}</span></div>`).join('')}</div>`;
  } else if (st === 1) {
    grpPrune();
    const tab = state.mTab || 'teams';
    const groups = (state.groups || []).filter(x => grpReady(x) && grpTeams(x).every(t => mtypeOk(t, mt)));
    const inG = new Set([].concat(...groups.map(x => x.ids)));
    const teams = state.teams.filter(t => !inG.has(t.id) && teamReady(t) && mtypeOk(t, mt));
    const vehs = state.vehicles.filter(v => v.status === 'home');
    const malps = state.malps.filter(m => m.status === 'home');
    const nT = sel.length;
    h += `<div class="mptabs"><button class="${tab === 'teams' ? 'on' : ''}" onclick="mpTab('teams')">TEAMS ${nT ? '// ' + nT : ''}</button><button class="${tab === 'veh' ? 'on' : ''}" onclick="mpTab('veh')">VEHICLES ${vs.length ? '// ' + vs.length : ''}</button><button class="${tab === 'malp' ? 'on' : ''}" onclick="mpTab('malp')">MALPS ${malpIn ? '// 1' : ''}</button></div>`;
    if (tab === 'teams') {
      const rows = groups.map(x => { const ts = grpTeams(x); return mpRow('G', x.name, 'GROUP // ' + ts.map(t => t.name).join(', ') + ' // ' + ts.reduce((a, t) => a + TYPES[t.type].cost, 0) + ' sup', ts.every(t => state.sel.includes(t.id)), `togGroup('${x.id}')`, false); })
        .concat(teams.map(t => mpRow(TYPES[t.type].name[0], t.name, TYPES[t.type].name + (noCam(t) ? '' : ' // CAM ' + t.cam) + ' // ' + TYPES[t.type].cost + ' sup', state.sel.includes(t.id), `togTeam('${t.id}')`, false)));
      h += rows.join('') || `<p class="dim small">No teams on station can go on ${MTYPES[mt][0].toLowerCase()} missions.</p>`;
    } else if (tab === 'veh') {
      const full = state.selVeh.length >= VEH_PER_SEND;
      h += vehs.map(v => mpRow(vehName(v)[0], vehName(v), 'Tier ' + v.tier + ' // ' + vehLabel(v), state.selVeh.includes(v.id), `togVeh('${v.id}')`, full)).join('') || '<p class="dim small">No vehicles in the Motor Pool ready to go.</p>';
      if (vehs.length) h += `<p class="dim small">Up to ${VEH_PER_SEND} vehicles per send.</p>`;
    } else {
      h += malps.map(m => { const t = m.tier || 0; return mpRow('M', 'MALP ' + malpNo(m), 'Tier ' + t + ' // survey tier ' + Math.max(1, t) + ' // ' + Math.round((t ? MALP_TIERS[t - 1].ret : MALP_BASE_RET) * 100) + '% return if ambushed', malpIn && mp.id === m.id, `togMalp('${m.id}')`, false); }).join('') || '<p class="dim small">No MALP on station.</p>';
    }
  } else {
    const rr = (a, b) => `<div class="res-row"><span>${a}</span><span>${b}</span></div>`;
    h += rr('Type', MTYPES[mt][0]) + rr('Destination', destLabel()) + rr('Teams', sel.map(t => t.name).join(', ') || 'None') + rr('Vehicles', vs.map(vehName).join(', ') || 'None') + rr('MALP', malpIn ? 'MALP ' + malpNo(mp) + ' // Tier ' + (mp.tier || 0) : 'None');
    if (state.repeatNote) h += `<p class="small warn">${state.repeatNote}</p>`;
    h += nt;
    if (vs.length) h += `<p class="small dim">Vehicle bonus: ${vehSummary(state.selVeh)}.</p>`;
  }
  h += '</div>';
  const sum = `${sel.length} TEAM${sel.length === 1 ? '' : 'S'} // ${vs.length} VEH${malpIn ? ' // MALP' : ''}`;
  const L = state.lastMission;
  const left = st === 0 ? `<button ${L ? '' : 'disabled'} title="${L ? MTYPES[L.mt][0] + ': ' + L.names.join(', ') : 'No mission sent yet'}" onclick="repeatLast()">↻ REPEAT LAST</button>` : `<button onclick="mpStep(${st - 1})">◀ BACK</button>`;
  const label = sel.length ? `SEND ${sel.length} TEAM${sel.length === 1 ? '' : 'S'}${g.malp ? ' + MALP' : ''}` : (g.malp ? 'SEND MALP' : 'SEND');
  const right = st < 2 ? `<button onclick="mpStep(${st + 1})">NEXT ▶</button>` : `<button class="mpsend" ${canSend ? '' : 'disabled'} onclick="dispatch()">${label}</button>`;
  return h + `<div class="mpfoot">${left}<span class="dim small">${sum}</span>${right}</div>`;
}

function missionBuilderHtml() {""")

rep("""function setMType(k) {
  if (!MTYPES[k]) return;
  state.mType = k;""", """function setMType(k) {
  if (!MTYPES[k]) return;
  state.mType = k;
  state.repeatNote = '';""")

rep("""  d += missionBuilderHtml();
  const assistTarget""", """  const d0 = d;
  const assistTarget""")

rep("""    d += '<p class="small dim help">Pick a mission type, then add the teams to send from the dropdowns. Missions take 2 minutes, plus 1 to 3 more if the group is ambushed. The whole group shares one ambush roll and returns together.</p>';
  }
  const label = sel.length ? `SEND ${sel.length} TEAM${sel.length === 1 ? '' : 'S'}${g.malp ? ' + MALP' : ''}` : (g.malp ? 'SEND MALP' : 'SEND 0 TEAMS');
  d += `<div class="controls"><button ${canSend ? '' : 'disabled'} onclick="dispatch()">${label}</button></div>`;""",
"""    d += '<p class="small dim">Nothing added yet. Add teams in step 2.</p>';
  }
  const nt = d.slice(d0.length);
  d = d0 + missionPanelHtml(g, sel, canSend, nt);""")

rep("""  if (g.malp) launchMalp(w, g.teams);
  state.sel = [];
  state.selVeh = [];
  state.withMalp = false;
  renderAll();""", """  const lmp = g.malp ? selMalp() : null;
  state.lastMission = { mt: g.mt, ids: g.teams.map(t => t.id), names: g.teams.map(t => t.name).concat(vsel.map(id => vehName(vehOf(id)))).concat(lmp ? ['MALP'] : []), veh: vsel.slice(), malp: lmp ? lmp.id : null };
  if (g.malp) launchMalp(w, g.teams);
  state.sel = [];
  state.selVeh = [];
  state.withMalp = false;
  state.mStep = 0;
  state.repeatNote = '';
  renderAll();""")

rep("""  const left = '<h2>Teams</h2>' + roster + '<h2""", """  const left = '<h2>Teams</h2>' + roster + (et ? groupBoxHtml(et) : '') + '<h2""")

rep("""    sel: [],""", """    sel: [],
    groups: [],
    grpSeq: 0,
    grpN: {},
    lastMission: null,
    mStep: 0,
    mTab: 'teams',
    repeatNote: '',""")

rep("""    missions: state.missions,
    missionSeq""", """    missions: state.missions,
    groups: state.groups,
    grpSeq: state.grpSeq,
    grpN: state.grpN,
    lastMission: state.lastMission,
    missionSeq""")

rep("""  state.missions = d.missions || [];""", """  state.missions = d.missions || [];
  state.groups = d.groups || [];
  state.grpSeq = d.grpSeq || 0;
  state.grpN = d.grpN || {};
  state.lastMission = d.lastMission || null;
  state.mStep = 0;
  state.mTab = 'teams';
  state.repeatNote = '';""")

rep(""".mc.layer button { font-size: 11px; letter-spacing: 0.1em; padding: 0 12px; }""", """.mc.layer button { font-size: 11px; letter-spacing: 0.1em; padding: 0 12px; }
.mpsteps { display: flex; gap: 4px; margin: 6px 0 4px; }
.mpsteps button { flex: 1; font-size: 11px; letter-spacing: 0.14em; padding: 4px 6px; min-height: 0; }
.mpsteps button.done { color: var(--ok); }
.mpbody { height: 135px; overflow: auto; border: 1px solid var(--steel); background: rgba(2, 8, 16, 0.6); padding: 6px; }
.mptypes { display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px; }
.mptc { border: 1px solid var(--steel); padding: 5px 7px; cursor: pointer; font-size: 11px; }
.mptc b { display: block; color: var(--accent); letter-spacing: 0.12em; font-weight: normal; margin-bottom: 2px; }
.mptc span { color: #8fb0c6; }
.mptc:hover { background: rgba(var(--accent-rgb), 0.08); }
.mptc.on { border-color: var(--accent); background: rgba(var(--accent-rgb), 0.14); }
.mptabs { display: flex; gap: 4px; margin-bottom: 4px; }
.mptabs button { flex: 1; font-size: 10.5px; letter-spacing: 0.12em; padding: 3px 6px; min-height: 0; }
.mprow { display: flex; align-items: center; gap: 8px; padding: 3px 4px; border-bottom: 1px solid #14253a; font-size: 12px; }
.mprow .mpg { flex: 1; min-width: 0; }
.mprow button { min-height: 0; padding: 2px 8px; font-size: 10.5px; }
.mpic { width: 18px; height: 18px; border: 1px solid currentColor; display: inline-grid; place-items: center; font-size: 9px; flex: none; color: var(--accent); }
.mpfoot { display: flex; justify-content: space-between; align-items: center; gap: 8px; margin-top: 6px; }
.mpfoot button { min-height: 0; padding: 4px 12px; }
.mpsend { font-weight: bold; letter-spacing: 0.16em; }""")

rep("""</head>""", """<style>
nav { flex-wrap: nowrap; }
#strip { flex-wrap: nowrap; overflow-x: auto; overflow-y: hidden; scrollbar-width: thin; }
#strip > * { flex: none; }
.tabcards { grid-template-columns: repeat(auto-fit, minmax(118px, 1fr)); }
body:not(.gv) main { grid-template-columns: 240px minmax(0, 1fr); }
.tcn, .tcs, .cn, .cl, .rcs { display: block; white-space: nowrap; overflow: hidden; min-width: 0; }
.rch, body:not(.gv) .rch { flex-wrap: nowrap; align-items: baseline; min-width: 0; }
.rch .cn { flex: 1 1 auto; }
.rch .cl { flex: none; }
.rch .cn { letter-spacing: 0.13em; }
.staff-row, .res-row { flex-wrap: nowrap; gap: 10px; }
.staff-row > span:first-child { min-width: 0; flex: 1 1 auto; }
.staff-row > span:first-child > b, .staff-row > span:first-child > .tn { white-space: nowrap; }
.res-row > span { white-space: nowrap; overflow: hidden; min-width: 0; flex: 0 1 auto; }
.staff-row > span:last-child { white-space: nowrap; overflow: hidden; min-width: 0; flex: 0 1 auto; }
.staff-row > span:last-child, .res-row > span:last-child { flex-wrap: nowrap; }
.dispatch-row > div:first-child > b { white-space: nowrap; }
.badge, button, .panel h2, .mptc b, .mpg { white-space: nowrap; }
.mpg, .mptc b, button { overflow: hidden; }
</style>
</head>""")
rep("""window.addEventListener('resize', fitScreen);""", """window.addEventListener('resize', fitScreen);
const FIT_SEL = '.tcn, .tcs, .cn, .cl, .rcs, .staff-row > span:last-child, .res-row > span, .badge, .mptc b, .mpg, .panel h2, button';
let fitGid = 0;
const fitGids = new WeakMap();
function fitKey(el) {
  const box = el.closest('.tabcards, .mptypes, .mptabs, .mpsteps, .mpfoot') || (el.closest('.rcard') ? el.closest('.rcard').parentElement : null);
  if (!box) return null;
  if (!fitGids.has(box)) fitGids.set(box, ++fitGid);
  return fitGids.get(box) + '|' + el.tagName + '|' + (el.classList[0] || '');
}
function fitTexts() {
  const els = [...document.querySelectorAll(FIT_SEL)].filter(el => el.offsetParent && !el.closest('svg'));
  els.forEach(el => { if (el.style.fontSize) el.style.fontSize = ''; });
  const need = new Map();
  const grp = {};
  els.forEach(el => {
    const w = el.clientWidth;
    const r = w && el.scrollWidth > w + 1 ? Math.max(0.75, w / el.scrollWidth) : 1;
    need.set(el, r);
    const k = fitKey(el);
    if (k) grp[k] = Math.min(grp[k] || 1, r);
  });
  els.forEach(el => {
    const k = fitKey(el);
    const r = k ? grp[k] : need.get(el);
    if (r >= 1) return;
    const base = parseFloat(getComputedStyle(el).fontSize);
    let f = base * r;
    el.style.fontSize = f.toFixed(2) + 'px';
    while (el.scrollWidth > el.clientWidth + 1 && f > base * 0.72) {
      f -= base * 0.03;
      el.style.fontSize = f.toFixed(2) + 'px';
    }
  });
}
let fitQ = 0;
new MutationObserver(() => { if (fitQ) return; fitQ = requestAnimationFrame(() => { fitQ = 0; fitTexts(); }); }).observe(document.body, { childList: true, subtree: true, characterData: true });
window.addEventListener('resize', () => requestAnimationFrame(fitTexts));""")

rep("""  if (k === 'quarter') return `POWER ${state.res.power} / ${POWER_CAP} // SUPPLIES ${state.res.supplies}${""", """  if (k === 'quarter') return `SUPPLIES ${state.res.supplies}${""")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
