import sys
src, dst = sys.argv[1:3]
s = open(src, encoding='utf-8').read()
assert s.count('0.9.3') == 4, s.count('0.9.3')
s = s.replace('0.9.3', '0.9.4')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


def region(start, end, new):
    global s
    i = s.index(start)
    j = s.index(end, i)
    assert s.count(start) == 1
    s = s[:i] + new + s[j:]


# ---------- rooms: Off-World Operations ----------
rep("const ROOM_ORDER = ['gate', 'brief', 'barracks', 'quarter', 'med', 'lab', 'arm', 'motor', 'arch'];",
    """ROOMS.ops = { name: 'Off-World Operations', lvl: 'LEVEL 22', desc: 'Forward Operating Bases on captured strongholds: garrisons, stockpiles, raid status and new bases.' };
const ROOM_ORDER = ['gate', 'brief', 'barracks', 'quarter', 'med', 'lab', 'arm', 'motor', 'arch', 'ops'];

function opsOpen() {
  return Object.keys(state.fobs || {}).length > 0 || state.worlds.some(w => w.stronghold && w.status === 'captured');
}

function roomList() {
  return ROOM_ORDER.filter(k => k !== 'ops' || opsOpen());
}""")

rep("Buy researched equipment here and issue it to teams in the Barracks. Tel'tak cargo ships are kept here.",
    "Buy researched equipment here and issue it to teams in the Barracks.")
rep("desc: 'Supplies, reactor power and naquadah stores.'",
    "desc: \"Supplies, reactor power and naquadah stores. Air Force Logistics requests, rescues and Tel'tak supply runs are handled here.\"")

rep("""  if (k === 'barracks') return `${n} TEAM${n === 1 ? '' : 'S'} // ${n - away.length} HOME`;""",
    """  if (k === 'barracks') return `${n} TEAM${n === 1 ? '' : 'S'} // ${n - away.length} HOME`;
  if (k === 'ops') {
    const nb = Object.keys(state.fobs || {}).length;
    const rd = Object.keys(state.dipl.alerts).filter(id => state.fobs && state.fobs[id]).length;
    if (rd) return `<span class="danger">${rd} RAID${rd === 1 ? '' : 'S'} INBOUND</span>`;
    return nb ? `${nb} BASE${nb === 1 ? '' : 'S'} ACTIVE` : 'NO BASES YET';
  }""")

rep("""  if (k === 'quarter') return `SUPPLIES ${state.res.supplies}${Object.keys(state.lg.units).length ? ' // INBOUND' : ''}`;""",
    """  if (k === 'quarter') {
    const sh = state.arm.ships;
    const aw = sh.filter(x => x.status === 'away').length;
    return `SUPPLIES ${state.res.supplies}${Object.keys(state.lg.units).length ? ' // INBOUND' : ''}${sh.length ? " // TEL'TAK " + (sh.length - aw) + ' / ' + sh.length : ''}`;
  }""")

rep("""  if (k === 'arm') {
    const st = Object.values(state.arm.stock).reduce((a, b) => a + b, 0);
    const sh = state.arm.ships;
    const aw = sh.filter(x => x.status === 'away').length;
    return `STOCK ${st}${sh.length ? " // TEL'TAK " + (sh.length - aw) + ' / ' + sh.length : ''}`;
  }""", """  if (k === 'arm') {
    const st = Object.values(state.arm.stock).reduce((a, b) => a + b, 0);
    return `STOCK ${st}`;
  }""")

rep("state.arm.ships.filter(x => x.status === 'away').forEach(x => chips.push(['arm',",
    "state.arm.ships.filter(x => x.status === 'away').forEach(x => chips.push(['quarter',")
rep("$('map').innerHTML = ROOM_ORDER.map(k => {", "$('map').innerHTML = roomList().map(k => {")
rep("const roomSig = ROOM_ORDER.map(cardStatus).join('|')", "const roomSig = roomList().map(cardStatus).join('|')")
rep("  if (state.room === 'quarter') renderRoom();", "  if (state.room === 'quarter' || state.room === 'ops') renderRoom();")
rep("  if (!ROOMS[state.room]) state.room = 'gate';", "  if (!ROOMS[state.room] || (state.room === 'ops' && !opsOpen())) state.room = 'gate';")
rep("  else if (k === 'quarter') body = quarterRoomHtml();", "  else if (k === 'quarter') body = quarterRoomHtml();\n  else if (k === 'ops') body = opsRoomHtml();")
rep("from the Quartermaster room: 100 supplies", "from the Off-World Operations room: 100 supplies")

rep("""<div class="rgrid"><div>${stores}</div><div>${power}</div></div><div style="margin-top:14px">${lgHtml()}${fobHtml()}</div>`;""",
    """<div class="rgrid"><div>${stores}${lgHtml()}${tkHtml()}</div><div>${power}</div></div>`;""")

# ---------- FOB panel becomes the Off-World Operations room ----------
region("function fobHtml() {", "\nfunction dipTick() {", r"""function opsRoomHtml() {
  const F = state.fobs || {};
  const ids = Object.keys(F);
  const cand = state.worlds.filter(w => w.stronghold && w.status === 'captured' && !F[w.id]);
  const help = `<p class="dim small help">A base makes ${FOB_SUP + FOB_PERK_SUP} supplies and ${FOB_RP + FOB_PERK_RP} research points every ${fmt(FOB_MS)} until its stockpile holds ${FOB_CAP_SUP} and ${FOB_CAP_RP}. A Tel'tak sent to the world collects everything; a Logistic Truck sent with an Exploration team collects one payout. The scientist and archeologist add ${FOB_PERK_RP} RP and ${FOB_PERK_SUP} supplies to each output. While the System Lord of that level lives, the base is raided: answer with a Defend mission, or the garrison fights alone. Wounded recover slowly; killed are replaced for ${REPLACE_COST} supplies each. If every defender falls the stronghold is lost.</p>`;
  let hb = '';
  ids.forEach(id => {
    const w = world(id);
    const b = F[id];
    const al = state.dipl.alerts[id];
    const st = al ? `<span class="warn">RAID <span data-eta="${al}">${fmt(al - Date.now())}</span></span>` : '<span class="ok">SECURE</span>';
    const full = b.stock.sup >= FOB_CAP_SUP && b.stock.rp >= FOB_CAP_RP;
    hb += `<div class="staff-row nob"><span><b>${wname(w)}</b> <span class="dim">${sysOf(w.level).star}</span></span>${st}</div>`;
    hb += `<div class="res-row"><span>Garrison</span><span>${b.guard} / ${FOB_GUARD} FIT${b.wnd ? ' // ' + b.wnd + ' WOUNDED' : ''}${b.dead ? ' // ' + b.dead + ' LOST' : ''}</span></div>`;
    hb += `<div class="res-row"><span>Stockpile</span><span>${b.stock.sup} / ${FOB_CAP_SUP} SUP // ${b.stock.rp} / ${FOB_CAP_RP} RP</span></div>`;
    hb += `<div class="res-row"><span>Next output</span>${full ? '<span class="warn">STOCKPILE FULL</span>' : `<span data-eta="${b.next}">${fmt(Math.max(0, b.next - Date.now()))}</span>`}</div>`;
    hb += `<div class="res-row"><span>Raid check</span>${lordAlive(w) ? `<span data-eta="${b.rt}">${fmt(Math.max(0, b.rt - Date.now()))}</span>` : '<span class="ok">ENDED // LORD DEFEATED</span>'}</div>`;
    hb += `<div class="dim small" style="margin:4px 0;text-align:left">${b.staff.map(m => m.role + ' ' + m.name).join(' // ')}</div>`;
    hb += `<div class="controls" style="margin:6px 0 12px;justify-content:flex-start"><button onclick="fobReplace('${id}')" ${b.dead && state.res.supplies >= b.dead * REPLACE_COST ? '' : 'disabled'}>REPLACE ${b.dead} // ${b.dead * REPLACE_COST} SUP</button><button onclick="fobRecall('${id}')">${state.fobConfirm === id ? 'CONFIRM RECALL' : 'RECALL BASE'}</button></div>`;
  });
  let hc = '';
  cand.forEach(w => {
    hc += `<div class="staff-row"><span><b>${wname(w)}</b> <span class="dim">${sysOf(w.level).star} // captured</span></span><button onclick="fobEstablish('${w.id}')" ${state.res.supplies >= FOB_COST ? '' : 'disabled'}>ESTABLISH // ${FOB_COST} SUP</button></div>`;
  });
  const left = `<h2>Active bases <span class="dim">${ids.length}</span></h2>${hb || '<p class="dim">No base established yet. Pick a captured stronghold to build one.</p>'}`;
  const right = `<h2>Available sites <span class="dim">${cand.length}</span></h2>${hc || '<p class="dim">Every captured stronghold already has a base.</p>'}${help}`;
  return `<div class="rgrid"><div>${left}</div><div>${right}</div></div>`;
}
""")

# ---------- Tel'tak: Quartermaster ----------
rep("function pickTkWorld(v) { state.tkPick = v; renderRoom(); }",
    """const TKUI = { open: null };
function tkDest(x) {
  const w = x && x.dest ? world(x.dest) : null;
  return w && tkWorlds().includes(w) ? w : null;
}
function tkOpen(id) { TKUI.open = TKUI.open === id ? null : id; renderRoom(); }
function tkPickDest(id, wid) {
  const x = state.arm.ships.find(q => q.id === id);
  if (!x || x.status !== 'home') return;
  x.dest = wid;
  TKUI.open = null;
  renderRoom();
}
function tkWorldInfo(w) {
  const tail = fobOn(w) ? 'FOB STOCKPILE ' + state.fobs[w.id].stock.sup + ' SUP // ' + state.fobs[w.id].stock.rp + ' RP' : (w.intel >= 3 ? HAZ_LABEL[w.hazard] + ' HAZARD // ' + tkYield(w) + ' SUP' : 'HAZARD UNKNOWN');
  return tkLy(w) + ' LY // ' + fmt(tkRoundMs(w)) + ' ROUND TRIP // ' + tail;
}
function tkHtml() {
  const A = state.arm;
  let h = `<h2>Tel'tak Supply Runs</h2>`;
  ['tk1', 'tk2'].forEach(id => {
    const it = armItem(id);
    if (A.done[id] && !A.ships.some(x => x.id === id)) h += `<div class="staff-row"><span><b>${it.name}</b><br><span class="dim">Restored. Ready to enter service.</span></span><button ${state.res.supplies < it.sup ? 'disabled' : ''} onclick="buyArm('${id}')">PUT IN SERVICE // ${it.sup} SUP</button></div>`;
  });
  if (!A.ships.length) return h + `<p class="dim">No Tel'tak in service. Recover a wreck from a stronghold and restore it in the Lab.</p>`;
  const wl = tkWorlds();
  A.ships.forEach(x => {
    const home = x.status === 'home';
    const w = tkDest(x);
    const open = TKUI.open === x.id && home;
    h += `<div class="staff-row nob"><span><b>${tkName(x)}</b> ${tkStatus(x)}</span>${home ? `<button ${w && state.res.supplies >= TK_FEE ? '' : 'disabled'} onclick="sendTeltak('${x.id}')">SEND // ${TK_FEE} SUP</button>` : ''}</div>`;
    if (home) h += `<div class="res-row"><span>Destination</span><button class="tkd" onclick="tkOpen('${x.id}')">${open ? 'CLOSE LIST' : (w ? wname(w).toUpperCase() : (wl.length ? 'CHOOSE DESTINATION' : 'NO EXPLORED WORLDS'))}</button></div>`;
    if (open) {
      h += '<div class="scroll tklist">';
      wl.forEach(q => {
        h += `<div class="staff-row"><span><b>${wname(q)}</b><br><span class="dim">${tkWorldInfo(q)}</span></span>${w === q ? '<span class="ok">SELECTED</span>' : `<button onclick="tkPickDest('${x.id}','${q.id}')">SELECT</button>`}</div>`;
      });
      h += '</div>';
    }
  });
  return h + `<p class="dim small help">A run brings back the world's maximum supply roll (${TK_BASE} times the world's hazard multiplier), with no carry cap. Travel is 2 minutes per light year, round trip. About 1 run in 5 is delayed 1 to 3 minutes. Tel'tak ships are never ambushed. A ship remembers its last destination.</p>`;
}""")

rep("  const w = state.tkPick ? world(state.tkPick) : null;\n", "  const w = x ? tkDest(x) : null;\n")

# Armory loses the Tel'tak tab
i = s.index("function armoryRoomHtml(here) {")
j = s.index("\nfunction renderRoom() {", i)
fn = s[i:j]
a1 = fn.index("  const sel = tabSel('armory', ['stock', 'tk'], 'stock');")
a2 = fn.index("  let h = tabCardsHtml('armory', items, sel);") + len("  let h = tabCardsHtml('armory', items, sel);")
fn = fn[:a1] + "  const sel = 'stock';\n  let h = '';" + fn[a2:]
b1 = fn.index("  } else {\n    ['tk1', 'tk2'].forEach")
b2 = fn.index("  return h;\n}", b1)
fn = fn[:b1] + "  }\n" + fn[b2:]
s = s[:i] + fn + s[j:]

# ---------- Mission Briefing: tall panel, one brief at a time ----------
region("function renderBriefs() {", "\nfunction briefOpen(mid) {", r"""const BRN = { i: 0 };

function briefStep(d) {
  BRN.i = Math.max(0, Math.min(state.briefs.length - 1, BRN.i + d));
  renderBriefs();
}

function renderBriefs() {
  const el = $('briefs');
  if (!el || !state.briefs) return;
  const on = state.logTab === 'brief';
  $('log').hidden = on;
  el.hidden = !on;
  $('lt-log').classList.toggle('on', !on);
  $('lt-brief').classList.toggle('on', on);
  const unread = on ? 0 : Math.max(0, state.briefs.length - state.briefRead);
  $('lt-n').innerHTML = unread ? `<span class="nb">${unread} NEW</span>` : '';
  if (on) state.briefRead = state.briefs.length;
  const n = state.briefs.length;
  if (BRN.i >= n) BRN.i = Math.max(0, n - 1);
  let h;
  if (!n) h = '<div class="dim">No briefings yet. The base computer files one when a mission ends.</div>';
  else {
    const b = state.briefs[BRN.i];
    h = `<div class="bnav"><button onclick="briefStep(1)" ${BRN.i >= n - 1 ? 'disabled' : ''}>◀ BACK</button><span class="bcount">BRIEF ${n - BRN.i} / ${n}${BRN.i === 0 ? ' // NEWEST' : ''}</span><button onclick="briefStep(-1)" ${BRN.i <= 0 ? 'disabled' : ''}>NEXT ▶</button></div>`
      + `<div class="bf ${b.cls || ''}"><div class="bh">[${b.t}] BASE COMPUTER // ${b.title}</div><div>${b.body}</div>${b.mid ? `<div class="controls"><button onclick="briefOpen('${b.mid}')">OPEN MISSION LOG</button></div>` : ''}</div>`;
  }
  if (el.__h !== h) { el.__h = h; el.innerHTML = h; }
}
""")

rep("  state.briefs.unshift({ t: clock(), title, body, cls: cls || '', mid: mid || '' });\n  if (state.briefs.length > 60) state.briefs.pop();",
    "  state.briefs.unshift({ t: clock(), title, body, cls: cls || '', mid: mid || '' });\n  if (BRN.i > 0) BRN.i++;\n  if (state.briefs.length > 60) { state.briefs.pop(); BRN.i = Math.min(BRN.i, 59); }")
rep("  if (k === 'brief') state.briefRead = state.briefs.length;\n  renderBriefs();\n}",
    "  if (k === 'brief') { state.briefRead = state.briefs.length; BRN.i = 0; }\n  renderBriefs();\n  fitScreen();\n}")

rep("#briefs .bf .bh .badge { margin-left: 8px; }",
    """#briefs .bf .bh .badge { margin-left: 8px; }
#briefs .bf { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
#briefs .bnav { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 10px; padding-bottom: 10px; border-bottom: 1px solid var(--steel-dim); }
#briefs .bcount { color: var(--steel); letter-spacing: 0.14em; font-size: var(--fs-sm); }
body:not(.gv) #briefs:not([hidden]) { height: 290px; }
body.gv .panel.wide { display: flex; flex-direction: column; }
body.gv #briefs:not([hidden]) { flex: 1 1 auto; height: auto; min-height: 110px; }
.tkact { display: inline-flex; gap: 8px; align-items: center; justify-content: flex-end; flex-wrap: wrap; }
.tkact .tkd { max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.tklist { margin: 4px 0 10px 10px; border-left: 2px solid var(--steel-dim); padding-left: 10px; }""")

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
