import sys
src, dst = sys.argv[1:3]
s = open(src, encoding='utf-8').read()
assert s.count('0.9.8') == 4, s.count('0.9.8')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('<title>Stargate Command 0.9.8</title>', '<title>Stargate Command 0.9.9</title>')
rep('BUILD 0.9.8', 'BUILD 0.9.9', 2)
rep("const BUILD_VER = '0.9.8';", "const BUILD_VER = '0.9.9';")

rep("function grpOf(t) { return (state.groups || []).find(g => g.ids.includes(t.id)); }",
    """function grpOf(t) { return (state.groups || []).find(g => g.ids.includes(t.id)); }
function grpsOf(t) { return (state.groups || []).filter(g => g.ids.includes(t.id)); }
const TAGP = { exp: 'EXP', rec: 'REC', asl: 'ASL', dip: 'DIP', sec: 'SEC' };
function tagClean(v) { return String(v || '').toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 5); }
function tagTaken(tag, skip) { return state.teams.some(t => t !== skip && t.tag === tag) || (state.groups || []).some(g => g !== skip && g.tag === tag); }
function uniqTag(prefix, n) {
  for (let i = Math.max(1, n); i < 100; i++) {
    const tg = prefix + String(i).padStart(2, '0');
    if (!tagTaken(tg)) return tg;
  }
  for (let i = 1; i < 100; i++) {
    const tg = prefix + String(i).padStart(2, '0');
    if (!tagTaken(tg)) return tg;
  }
  return Math.random().toString(36).slice(2, 7).toUpperCase().padEnd(5, 'X');
}
function ensureTags() {
  state.teams.forEach(t => { t.tag = tagClean(t.tag); if (t.tag.length !== 5 || state.teams.some(x => x !== t && x.tag === t.tag)) t.tag = ''; });
  state.teams.filter(t => !t.tag).forEach(t => { const mm = /(\\d+)\\s*$/.exec(t.name); t.tag = uniqTag(TAGP[t.type] || 'TEM', mm ? +mm[1] : 1); });
  const gs = state.groups || [];
  gs.forEach(g => { g.tag = tagClean(g.tag); if (g.tag.length !== 5 || gs.some(x => x !== g && x.tag === g.tag) || state.teams.some(x => x.tag === g.tag)) g.tag = ''; });
  gs.filter(g => !g.tag).forEach((g, i) => { g.tag = uniqTag('GRP', gs.indexOf(g) + 1); });
}
function setTeamTag(tid, v) {
  const t = state.teams.find(x => x.id === tid);
  const tg = tagClean(v);
  if (!t) return;
  if (tg.length !== 5) log('A tag must be exactly 5 letters or digits.', 'warn');
  else if (tagTaken(tg, t)) log('Tag ' + tg + ' is already in use.', 'warn');
  else t.tag = tg;
  renderAll();
}
function setGroupTag(gid, v) {
  const g = (state.groups || []).find(x => x.id === gid);
  const tg = tagClean(v);
  if (!g) return;
  if (tg.length !== 5) log('A tag must be exactly 5 letters or digits.', 'warn');
  else if (tagTaken(tg, g)) log('Tag ' + tg + ' is already in use.', 'warn');
  else g.tag = tg;
  renderAll();
}
function sentGroupTags(teams) {
  const ids = teams.map(t => t.id);
  return (state.groups || []).filter(g => g.ids.length > 1 && g.ids.every(id => ids.includes(id))).map(g => g.tag);
}""")

rep("return g.ids.length > 0; });", "return true; });")
rep("if (!g.ids.includes(g.lead)) g.lead = g.ids[0];", "g.lead = g.ids.includes(g.lead) ? g.lead : (g.ids[0] || null);")

a = s.index('function newGroup(tid) {')
b = s.index('function renameGroup(gid, v) {')
s = s[:a] + s[b:]

a = s.index('function groupBoxHtml(t) {')
b = s.index('function mpStep(n)')
new_box = r"""function createGroup() {
  const n = cleanName(($('gn_name') || {}).value || '');
  const tg = tagClean(($('gn_tag') || {}).value || '');
  if (tg.length !== 5) { log('A tag must be exactly 5 letters or digits.', 'warn'); renderAll(); return; }
  if (tagTaken(tg)) { log('Tag ' + tg + ' is already in use.', 'warn'); renderAll(); return; }
  state.grpSeq = (state.grpSeq || 0) + 1;
  const id = 'g' + state.grpSeq;
  state.groups = (state.groups || []).concat([{ id, name: n || 'Group ' + state.grpSeq, tag: tg, lead: null, ids: [] }]);
  state.editGroup = id;
  renderAll();
}

function selGroup(gid) {
  state.editGroup = state.editGroup === gid ? null : gid;
  renderAll();
}

function groupToggle(gid, tid) {
  const g = (state.groups || []).find(x => x.id === gid);
  if (!g || !state.teams.some(t => t.id === tid)) return;
  if (g.ids.includes(tid)) g.ids = g.ids.filter(x => x !== tid);
  else g.ids.push(tid);
  grpPrune();
  renderAll();
}

function deleteGroup(gid) {
  state.groups = (state.groups || []).filter(x => x.id !== gid);
  if (state.editGroup === gid) state.editGroup = null;
  renderAll();
}

function groupsPanelHtml() {
  grpPrune();
  const gs = state.groups || [];
  let h = '<h2 style="margin-top:12px">Linked groups</h2>';
  gs.forEach(g => {
    const ts = grpTeams(g);
    const open = state.editGroup === g.id;
    const st = ts.length < 2 ? '<span class="dim">Add at least two teams to form the group.</span>' : (grpReady(g) ? '<span class="ok">READY AS A GROUP</span>' : '<span class="warn">UNAVAILABLE // ' + ts.filter(x => !teamReady(x)).map(x => x.tag).join(', ') + ' not ready</span>');
    h += `<div class="dispatch-row"><div><b>${g.tag}</b> <span class="dim">${g.name} // ${ts.map(x => x.tag).join(', ') || 'no teams'}</span><div class="mrow">${st}</div></div><button onclick="selGroup('${g.id}')">${open ? 'CLOSE' : 'EDIT'}</button></div>`;
    if (open) {
      h += `<div class="dispatch-row"><div><input class="nm tn" maxlength="26" value="${g.name}" onchange="renameGroup('${g.id}', this.value)"> <input class="nm" maxlength="5" style="width:80px;text-transform:uppercase" value="${g.tag}" onchange="setGroupTag('${g.id}', this.value)"></div><button onclick="deleteGroup('${g.id}')">DELETE GROUP</button></div>`;
      state.teams.forEach(t => {
        const inG = g.ids.includes(t.id);
        h += `<div class="mprow"><span class="mpic">${TYPES[t.type].name[0]}</span><span class="mpg"><b>${t.tag}</b> <span class="dim">${t.name}${t.status === 'away' ? ' // away' : ''}${grpsOf(t).length > (inG ? 1 : 0) ? ' // also in ' + grpsOf(t).filter(x => x !== g).map(x => x.tag).join(', ') : ''}</span></span><button class="${inG ? 'on' : ''}" onclick="groupToggle('${g.id}', '${t.id}')">${inG ? '✓ IN GROUP' : 'ADD'}</button></div>`;
      });
    }
  });
  const sq = (state.grpSeq || 0) + 1;
  h += `<div class="dispatch-row"><div><input class="nm tn" id="gn_name" maxlength="26" value="Group ${sq}"> <input class="nm" id="gn_tag" maxlength="5" style="width:80px;text-transform:uppercase" value="${uniqTag('GRP', sq)}"></div><button onclick="createGroup()">CREATE GROUP</button></div>`;
  h += '<p class="dim small help">Name a group and give it a 5-character tag, then pick its teams from the list. A team can be in any number of groups. A group is added to a mission as one asset and is unavailable while any member is away.</p>';
  return h;
}

"""
s = s[:a] + new_box + s[b:]

rep("(et ? groupBoxHtml(et) : '')", "groupsPanelHtml()")

rep("""    const groups = (state.groups || []).filter(x => grpReady(x) && grpTeams(x).every(t => mtypeOk(t, mt)));
    const inG = new Set([].concat(...groups.map(x => x.ids)));""",
"""    const allG = (state.groups || []).filter(x => x.ids.length > 1 && grpTeams(x).every(t => mtypeOk(t, mt)));
    const groups = allG.filter(grpReady);
    const blocked = allG.filter(x => !grpReady(x));
    const memN = {};
    (state.groups || []).forEach(x => x.ids.forEach(id => { memN[id] = (memN[id] || 0) + 1; }));
    const inG = new Set([].concat(...groups.map(x => x.ids)).filter(id => memN[id] === 1));""")

rep("""mpRow('G', x.name, 'GROUP // ' + ts.map(t => t.name).join(', ')""", """mpRow('G', x.tag + ' ' + x.name, 'GROUP // ' + ts.map(t => t.tag).join(', ')""")
rep("""        .concat(teams.map(t => mpRow(TYPES[t.type].name[0], t.name,""", """        .concat(blocked.map(x => { const ts = grpTeams(x); return mpRow('G', x.tag + ' ' + x.name, 'GROUP // UNAVAILABLE // ' + ts.filter(t => !teamReady(t)).map(t => t.tag).join(', ') + ' not ready', false, `togGroup('${x.id}')`, true); }))
        .concat(teams.map(t => mpRow(TYPES[t.type].name[0], t.tag + ' ' + t.name,""")

rep("return { id: 't' + (++teamSeq), type, name: T.name + ' Team ' + (count + 1), members,",
    "return { id: 't' + (++teamSeq), type, name: T.name + ' Team ' + (count + 1), tag: (TAGP[type] || 'TEM') + String(count + 1).padStart(2, '0'), members,")
rep("  const t = makeTeam(type, teamCount(type));\n  state.teams.push(t);",
    "  const t = makeTeam(type, teamCount(type));\n  t.tag = uniqTag(TAGP[type] || 'TEM', teamCount(type) + 1);\n  state.teams.push(t);")

rep("""<div class="res-row"><span>Type</span><span>${TYPES[t.type].name} // ${TYPES[t.type].branch}</span></div>""",
    """<div class="res-row"><span>Tag</span><span><input class="nm" maxlength="5" style="width:80px;text-transform:uppercase" value="${t.tag}" onchange="setTeamTag('${t.id}', this.value)"></span></div>
    <div class="res-row"><span>Groups</span><span>${grpsOf(t).map(x => x.tag).join(', ') || 'none'}</span></div>
    <div class="res-row"><span>Type</span><span>${TYPES[t.type].name} // ${TYPES[t.type].branch}</span></div>""")

rep("  const names = g.teams.map(t => t.name);\n  const vsel", "  const names = g.teams.map(t => t.name);\n  const gtags = sentGroupTags(g.teams);\n  const vsel")
rep("t.mission = { mid: missionToken(), worldId: w.id, kind: 'assault', ids, p, lid: alid, vg };",
    "t.mission = { mid: missionToken(), worldId: w.id, kind: 'assault', mt: g.mt, gtags, ids, p, lid: alid, vg };")
rep("t.mission = { mid, gid, dip: g.mt === 'dip',", "t.mission = { mid, gid, mt: g.mt, gtags, dip: g.mt === 'dip',")

rep("  state.groups = d.groups || [];\n", "  state.groups = d.groups || [];\n  ensureTags();\n")

a = s.index('function dcMissionRows() {')
b = s.index('function dcMissions() {')
new_rows = r"""function dcMissionRows() {
  const rows = [];
  const seen = {};
  state.teams.filter(t => t.status === 'away' && t.mission).forEach(t => {
    const m = t.mission;
    const key = m.gid || m.gmid || (m.ids ? m.ids.join(',') : null) || t.id;
    const eta = m.due ? -1 : (m.overdue ? -2 : (m.due0 && !m.recall && !m.paused ? (Date.now() >= m.due0 ? -3 : m.due0) : t.eta));
    if (seen[key]) {
      const r = seen[key];
      r.n++;
      r.eta = r.eta === -2 || eta === -2 ? -2 : (r.eta === -3 || eta === -3 ? -3 : (r.eta === -1 ? eta : (eta === -1 ? r.eta : Math.min(r.eta, eta))));
      return;
    }
    const ab = m.mt ? m.mt.toUpperCase() : (m.dip ? 'DIP' : m.def ? 'DEF' : m.kind === 'assault' ? 'ASL' : m.kind === 'assist' ? 'AST' : t.type === 'exp' ? 'EXP' : 'REC');
    const grouped = !!(m.gtags && m.gtags.length);
    const r = { n: 1, grouped, tags: grouped ? m.gtags.slice() : [t.tag || t.name.slice(0, 5).toUpperCase()], ab, eta };
    seen[key] = r;
    rows.push(r);
  });
  return rows.map(r => {
    const nm = r.grouped ? r.tags.slice(0, 2).join('/') + (r.tags.length > 2 ? ' +' + (r.tags.length - 2) : '') : r.tags[0] + (r.n > 1 ? ' +' + (r.n - 1) : '');
    const e = r.eta === -2 ? 'OVER' : r.eta === -3 ? 'LATE' : r.eta === -1 ? 'DUE' : fmt(r.eta - Date.now());
    return [nm, r.ab, e, r.eta === -2];
  });
}

"""
s = s[:a] + new_rows + s[b:]
rep('id="dcmt${r}" x="92"', 'id="dcmt${r}" x="140"')

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
