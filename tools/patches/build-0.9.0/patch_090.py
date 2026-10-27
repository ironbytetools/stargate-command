import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
assert s.count('0.8.10') == 4
s = s.replace('0.8.10', '0.9.0')
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70])
    s = s.replace(a, b)

rep("""const AMBUSH_MIN_MS = 60000;""", """const LORDS = [
  { n: 'Apophis', d: 'A serpent-god of old Earth myth, he commands the largest Jaffa host in the nearby systems.' },
  { n: 'Cronus', d: 'A Goa\\'uld who styles himself a Titan, he guards his territory jealously and answers every probe with force.' },
  { n: 'Yu', d: 'The oldest of the System Lords, he rules by patience and wears down rivals over centuries.' },
  { n: "Ba'al", d: 'Cunning and ambitious, he never fights on a single front and always has another plan running.' },
  { n: 'Anubis', d: 'A banished System Lord whose research reaches beyond Goa\\'uld technology: the last and most dangerous of the five.' }
];
const LORD_FEE = 1.5;
const LORD_DIFF = 1.1;
const LORD_BONUS_SUP = 100;
const LORD_BONUS_RP = 200;

function tagLords(list) {
  for (let lv = 1; lv <= MAX_LEVEL; lv++) {
    const holds = list.filter(w => w.level === lv && w.stronghold);
    if (!holds.length || holds.some(w => w.lord)) continue;
    let b = holds[0];
    holds.forEach(w => { if (w.diff >= b.diff) b = w; });
    b.lord = LORDS[lv - 1].n;
  }
}

const AMBUSH_MIN_MS = 60000;""")

rep("""  glTag(list);
}""", """  tagLords(list);
  glTag(list);
}""")

rep("""function upgradeWorlds(list) {
  const by = {};""", """function upgradeWorlds(list) {
  tagLords(list);
  const by = {};""")

rep("""function assaultCost(w) { return Math.round(ASSAULT_BASE * Math.pow(ASSAULT_MULT, w.level - 1)); }""", """function assaultCost(w) { return Math.round(ASSAULT_BASE * Math.pow(ASSAULT_MULT, w.level - 1) * (w.lord ? LORD_FEE : 1)); }""")

rep("""function effDiff(w) { return w.diff * (facPerk("Tok'ra") >= 3 ? 0.9 : 1); }""", """function effDiff(w) { return Math.min(100, w.diff * (w.lord ? LORD_DIFF : 1) * (facPerk("Tok'ra") >= 3 ? 0.9 : 1)); }""")

rep("""        if (cooldownLeft() > 0) g.reasons.push('Assault cooldown active.');
""", """        if (cooldownLeft() > 0) g.reasons.push('Assault cooldown active.');
        if (w.lord) {
          if (holdsLeft().some(x => x.id !== w.id && !x.treaty)) g.reasons.push(`${w.lord} holds this stronghold. Capture the system's other strongholds first.`);
          if (!w.recon) g.reasons.push(`Open the gate to ${wname(w)} and fly the drone recon (DRONE key) before assaulting ${w.lord}.`);
        }
""")

rep("""    msg += ' The world is now peaceful: ambushes no longer occur there.';
""", """    msg += ' The world is now peaceful: ambushes no longer occur there.';
    if (w.lord) {
      const bs = LORD_BONUS_SUP * w.level;
      const br = LORD_BONUS_RP * w.level;
      state.res.supplies += bs;
      state.research += br;
      msg += ` ${w.lord} has fallen. Spoils: ${bs} supplies and ${br} research points.`;
    }
""")

rep("""' All personnel unharmed.'}`);""", """' All personnel unharmed.'}${win && w.lord ? ' ' + w.lord + ' has fallen.' : ''}`);""")

rep("""<span>The final stronghold has fallen.${last""", """<span>${LORDS[lv - 1].n} has fallen.${last""")

rep("""  if (w.status === 'captured') b.push('<span class="badge ok">CAPTURED</span>');
  else if (w.stronghold && w.intel >= 2) b.push('<span class="badge danger">STRONGHOLD</span>');""", """  if (w.status === 'captured') b.push('<span class="badge ok">CAPTURED</span>');
  else if (w.stronghold && w.intel >= 2) b.push('<span class="badge danger">STRONGHOLD</span>');
  if (w.lord && w.intel >= 2) b.push(w.status === 'captured' ? `<span class="badge ok">${w.lord.toUpperCase()} DEFEATED</span>` : `<span class="badge danger">SYSTEM LORD: ${w.lord.toUpperCase()}</span>`);""")

rep("""const BRIEF_NOTES = {
""", """const BRIEF_NOTES = {
  LD1: ['SYSTEM LORD // APOPHIS', LORDS[0].d + ' He holds the last stronghold in Alpha Centauri. It cannot be assaulted until every other stronghold in the system has fallen, its defenses are 10% stronger, the assault fee is 1.5 times normal, and a drone recon must be flown first. Survey strongholds to learn which one is his.'],
  LD2: ['SYSTEM LORD // CRONUS', LORDS[1].d + " He holds the last stronghold in Barnard's Star under the same conditions: other strongholds first, defenses 10% stronger, assault fee 1.5 times, drone recon required."],
  LD3: ['SYSTEM LORD // YU', LORDS[2].d + ' He holds the last stronghold in Sirius under the same conditions: other strongholds first, defenses 10% stronger, assault fee 1.5 times, drone recon required.'],
  LD4: ["SYSTEM LORD // BA'AL", LORDS[3].d + ' He holds the last stronghold in Epsilon Eridani under the same conditions: other strongholds first, defenses 10% stronger, assault fee 1.5 times, drone recon required.'],
  LD5: ['SYSTEM LORD // ANUBIS', LORDS[4].d + ' He holds the last stronghold in Tau Ceti under the same conditions: other strongholds first, defenses 10% stronger, assault fee 1.5 times, drone recon required.'],
""")

rep("""    C7: () => state.level > 1,
""", """    C7: () => state.level > 1,
    LD1: () => state.level >= 1,
    LD2: () => state.level >= 2,
    LD3: () => state.level >= 3,
    LD4: () => state.level >= 4,
    LD5: () => state.level >= 5,
""")

open(dst, 'w', encoding='utf-8').write(s)
print('ok')
