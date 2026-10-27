
def repl_fn(name, new):
    global h
    i = h.index('function ' + name + '(')
    j = h.index('\nfunction ', i + 10)
    k = h.index('\n}\n', i)
    assert k < j + 3
    h = h[:i] + new.rstrip('\n') + h[k + 2:]

repl_fn('missionLogHtml', '''function missionLogHtml() {
  const list = state.missions.slice().reverse();
  const act = list.filter(r => r.state === 'active');
  const kinds = Object.keys(KLABEL).filter(k => list.some(r => r.kind === k));
  const keys = ['active'].concat(kinds);
  const sel = tabSel('mlog', keys, act.length ? 'active' : (kinds[0] || 'active'));
  const items = keys.map(k => k === 'active'
    ? { k, name: 'ACTIVE', sub: act.length + ' RUNNING', cls: act.length ? 'warn' : 'dim' }
    : { k, name: KLABEL[k].toUpperCase(), sub: list.filter(r => r.kind === k).length + ' LOGGED', cls: 'ok' });
  let h = '<h2>Mission log</h2>';
  if (!list.length) return h + '<p class="dim">No missions logged yet.</p>';
  h += tabCardsHtml('mlog', items, sel);
  const shown = sel === 'active' ? act : list.filter(r => r.kind === sel);
  if (!shown.length) return h + '<p class="dim">No active missions.</p>';
  return h + '<div class="scroll">' + shown.map(r => `<div class="staff-row"><span><button class="mid" onclick="openMissionLog('${r.id}')">${r.id}</button> <span class="dim">${KLABEL[r.kind]} // ${r.world}</span></span><span class="${r.state === 'active' ? 'warn' : 'ok'}">${r.state === 'active' ? 'ACTIVE' : 'CLOSED'}</span></div>`).join('') + '</div>';
}
''')

repl_fn('factionsHtml', '''function factionsHtml() {
  const list = Object.keys(FACTIONS).filter(facKnown);
  let h = '<h2>Faction relations</h2>';
  if (!list.length) return h + '<p class="dim">No factions contacted yet. Survey worlds to find them.</p>';
  const keys = list.map((n, i) => 'f' + i);
  const sel = tabSel('fac', keys, keys[0]);
  h += tabCardsHtml('fac', list.map((n, i) => { const tt = facTier(n); return { k: 'f' + i, name: n.toUpperCase(), sub: tt ? FAC_TIERS[tt] : 'UNMET', cls: tt >= 2 ? 'ok' : 'dim' }; }), sel);
  const n = list[+sel.slice(1)];
  const F = FACTIONS[n];
  const t = facTier(n);
  const p = facPts(n);
  const nx = t < 4 ? `${p} / ${FAC_AT[t]} to ${FAC_TIERS[t + 1]}` : 'Maximum standing';
  const cur = t >= 2 ? F.perk[t - 2] : '<span class="dim">No benefit yet</span>';
  const up = t < 2 ? F.perk[0] + ' (at Partner)' : (t < 4 ? F.perk[t - 1] + ' (at ' + FAC_TIERS[t + 1] + ')' : '');
  const pay = t >= 4 ? `<div class="ok mrow">Pays ${F.pay[1]} ${F.pay[0] === 'research' ? 'research' : 'supplies'} in <span data-eta="${state.fac.next[n] || 0}">${fmt(Math.max(0, (state.fac.next[n] || 0) - Date.now()))}</span></div>` : '';
  return h + `<div class="dispatch-row"><div><b>${n}</b> <span class="${t >= 2 ? 'ok' : 'dim'}">${t ? FAC_TIERS[t] : 'UNMET'}</span> <span class="dim">${nx}</span><div class="mrow">${cur}</div>${up ? `<div class="dim mrow">Next: ${up}</div>` : ''}${pay}</div></div>`;
}
''')

repl_fn('glPanelHtml', '''function glPanelHtml() {
  let h = '<h2>Glyph decoding</h2><p class="dim small">Inscriptions turn up on Exploration missions. Decode one here (a Linguist must be on station) to learn where its artifact lies, then send an Exploration team to recover it. Both artifacts of a level unlock that level\\'s bonus.</p>';
  h += '<div class="res-row"><span>Artifacts collected</span><span>' + glCount() + ' / 10</span></div>';
  h += '<div class="res-row"><span>' + GL_RELIC + '</span><span class="' + (glAll() ? 'ok' : 'dim') + '">' + (glAll() ? 'ON DISPLAY // +10% camaraderie gain, +5% research' : '○ COLLECT ALL 10') + '</span></div>';
  const keys = [1, 2, 3, 4, 5].map(l => 'l' + l);
  let def = 'l1';
  for (let l = 1; l <= 5; l++) if (!glDone(l)) { def = 'l' + l; break; }
  const sel = tabSel('gl', keys, def);
  const items = [1, 2, 3, 4, 5].map(l => { const c = (glArt(l * 2 - 1).c ? 1 : 0) + (glArt(l * 2).c ? 1 : 0); return { k: 'l' + l, name: 'LEVEL ' + l, sub: (glDone(l) ? 'BONUS ACTIVE' : c + ' / 2'), cls: glDone(l) ? 'ok' : (c ? 'warn' : 'dim') }; });
  h += tabCardsHtml('gl', items, sel);
  const lv = +sel.slice(1);
  h += '<div class="res-row"><span>Level ' + lv + ' bonus</span><span class="' + (glDone(lv) ? 'ok' : 'dim') + '">' + (glDone(lv) ? GL_LEVEL_BONUS[lv] : '○ ' + GL_LEVEL_BONUS[lv]) + '</span></div>';
  h += glRowHtml(lv * 2 - 1) + glRowHtml(lv * 2);
  return h;
}
''')

rep("function pickTab(room, key) { roomTab[room] = key; renderRoom(); }",
    "function pickTab(room, key) {\n  roomTab[room] = key;\n  if (room === 'barros') { const f = state.teams.find(x => x.type === key); if (f) state.editTeam = f.id; }\n  renderRoom();\n}")

rep("  const roster = state.teams.map(t => ",
    "  const rkeys = Object.keys(TYPES);\n  const rsel = roomTab.barros && !state.teams.some(x => x.type === roomTab.barros) ? roomTab.barros : (et ? et.type : rkeys[0]);\n  const ritems = rkeys.map(k => ({ k, name: TYPES[k].name.toUpperCase(), sub: teamCount(k) + ' TEAM' + (teamCount(k) === 1 ? '' : 'S'), cls: teamCount(k) ? 'ok' : 'dim' }));\n  const roster = tabCardsHtml('barros', ritems, rsel) + (state.teams.filter(t => t.type === rsel).map(t => ")
rep("</div></div>`).join('');\n  const keys = Object.keys(TYPES);", "</div></div>`).join('') || '<p class=\"dim\">No teams of this type.</p>');\n  const keys = Object.keys(TYPES);")

rep("    let any = false;\n    ARM_ITEMS.filter(i => !i.alien || i.id === 'staff').forEach(it => {\n      if (!A.done[it.id]) return;",
    "    let any = false;\n    const SL = [['w', 'WEAPONS'], ['a', 'ARMOR'], ['p', 'PACKS'], ['o', 'OPTICS'], ['x', 'DEVICES']];\n    const slc = s => ARM_ITEMS.filter(i => (i.slot || 'x') === s && A.done[i.id] && (!i.alien || i.id === 'staff' || i.id === 'heal')).length;\n    const ssel = tabSel('armsl', SL.map(s => s[0]), 'w');\n    h += tabCardsHtml('armsl', SL.map(s => ({ k: s[0], name: s[1], sub: slc(s[0]) + ' RESEARCHED', cls: slc(s[0]) ? 'ok' : 'dim' })), ssel);\n    ARM_ITEMS.filter(i => !i.alien || i.id === 'staff').forEach(it => {\n      if (!A.done[it.id] || (it.slot || 'x') !== ssel) return;")
rep("    if (A.done.heal) {\n      any = true;", "    if (A.done.heal && ssel === 'x') {\n      any = true;")
rep("<p class=\"dim\">Nothing researched yet. Research gear in the Lab.</p>", "<p class=\"dim\">Nothing researched in this category yet. Research gear in the Lab.</p>")
