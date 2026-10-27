import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
assert s.count('0.8.9') == 4
s = s.replace('0.8.9', '0.8.10')
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:60])
    s = s.replace(a, b)

rep("""#briefs .bf .controls { margin: 6px 0 0; justify-content: flex-start; }""", """#briefs .bf .controls { margin: 6px 0 0; justify-content: flex-start; }
#briefs .bgrid { display: grid; grid-template-columns: 84px 1fr 84px 1fr; gap: 3px 12px; max-width: 980px; margin-top: 5px; font-size: var(--fs-sm); line-height: 1.45; }
#briefs .bgrid .bk { color: var(--steel); letter-spacing: 0.08em; }
#briefs .bgrid .bf2 { grid-column: 2 / -1; }
#briefs .bf .bh .badge { margin-left: 8px; }""")

rep("""        msg += glExplore(w);
""", """        msg += glExplore(w);
        msg += facLead(w, t, m.lid);
""")

rep("""function facKnown(n) {""", """function facLead(w, t, mid) {
  if (!w || w.kind !== 'normal' || !state.fac) return '';
  const fw = state.worlds.filter(x => x.kind === 'faction' && x.intel < 2 && x.level <= state.level).sort((a, b) => a.level - b.level)[0];
  if (!fw) return '';
  fw.intel = 2;
  const n = fw.faction;
  factionContact(fw, t.name, mid);
  return ` On ${wname(w)} the team met ${n} traders, who gave the address of their home world, ${wname(fw)}. The ${n} are now on the Faction Relations list.`;
}

function facKnown(n) {""")

i = s.index("function briefMission(r) {")
j = s.index("function briefWatch() {")
new = r"""const BRIEF_FIND = /discovered the|seemed open to diplomacy|traders|are now on the|artifact|inscription|Decode it|Research it in the Lab|Zero Point|Atlantis|wreck|recovered|Stronghold confirmed|Thermal|decod|glyph|treaty|standing/i;
const BRIEF_PERS = /injured\.?$|stands down until healed|ambush cost no casualties|^\+\d+ research\.?$/i;

function briefSentences(t) {
  const x = String(t || '').replace(/\b(Col|Maj|Capt|Lt|Dr|Sgt|Cpl|Pvt|Gen|Cmdr|Mr|Ms|Mrs|St)\./g, '$1\u0001');
  return (x.match(/[^.]+\.?/g) || []).map(q => q.replace(/\u0001/g, '.').trim()).filter(Boolean);
}

function briefOutcome(r, inj, cas) {
  if (cas.length) return ['CASUALTIES', 'danger'];
  if (r.overdue) return ['OVERDUE', 'warn'];
  if (inj.length) return ['INJURIES', 'warn'];
  if (r.ambushed) return ['AMBUSHED', 'warn'];
  return ['CLEAN', 'ok'];
}

function briefRows(rows) {
  return '<div class="bgrid">' + rows.map(q => `<div class="bk">${q[0]}</div><div class="${(q[2] || '') + (q[3] ? ' bf2' : '')}">${q[1]}</div>`).join('') + '</div>';
}

function briefMission(r) {
  if (!state.briefs || r.briefed || r.kind === 'tk') return;
  r.briefed = true;
  const y = r.yield || {};
  const w = world(r.worldId);
  const iEnd = r.intelEnd === null ? (w ? w.intel : r.intelStart) : r.intelEnd;
  const injL = aarWho(r, ['injured']);
  const casL = aarWho(r, ['killed', 'captured']);
  const oc = briefOutcome(r, injL, casL);
  const sents = briefSentences(r.result || 'Mission closed.');
  const finds = sents.filter(q => BRIEF_FIND.test(q));
  const main = sents.filter(q => !BRIEF_FIND.test(q) && !BRIEF_PERS.test(q));
  const yl = [];
  if (y.supplies) yl.push(`Supplies ${y.supplies}`);
  if (y.naquadah) yl.push(`Naquadah ${y.naquadah}`);
  if (y.research) yl.push(`Research ${y.research}`);
  if (y.cam) yl.push(`Camaraderie +${y.cam}`);
  if (y.standing) yl.push(`Standing +${y.standing}`);
  const rows = [
    ['TEAM', r.launch.map(c => c.name).join(', ')],
    ['WORLD', r.world],
    ['RESULT', main.join(' ') || 'Mission closed.', '', true]
  ];
  rows.push(['YIELD', yl.length ? yl.join(' // ') : 'None', yl.length ? '' : 'dim']);
  rows.push(['INTEL', iEnd > r.intelStart ? `Tier ${r.intelStart} to ${iEnd}` : `Tier ${iEnd}, no change`, iEnd > r.intelStart ? 'ok' : 'dim']);
  if (injL.length || casL.length) {
    rows.push(['INJURED', aarNames(injL), injL.length ? 'warn' : 'dim']);
    rows.push(['LOST', aarNames(casL), casL.length ? 'danger' : 'dim']);
  } else rows.push(['PERSONNEL', 'No injuries or losses', 'ok', true]);
  if (finds.length) rows.push(['FINDS', finds.join('<br>'), 'ok', true]);
  if (aarEligible(r)) rows.push(['AAR', 'Can be filed from the mission log.', 'dim', true]);
  postBrief(`MISSION COMPLETE // ${r.id} // ${KLABEL[r.kind]}<span class="badge ${oc[1]}">${oc[0]}</span>`, briefRows(rows), '', r.id);
  briefNote('D7');
}

"""
s = s[:i] + new + s[j:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
