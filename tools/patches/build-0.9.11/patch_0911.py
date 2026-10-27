import json
import sys
src, dst = sys.argv[1:3]
s = open(src, encoding='utf-8').read()
assert s.count('0.9.10') == 4, s.count('0.9.10')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('<title>Stargate Command 0.9.10</title>', '<title>Stargate Command 0.9.11</title>')
rep('BUILD 0.9.10', 'BUILD 0.9.11', 2)
rep("const BUILD_VER = '0.9.10';", "const BUILD_VER = '0.9.11';")

GL = ['Earth', 'Andromeda', 'Aquarius', 'Aquila', 'Aries', 'Auriga', 'Bootes', 'Cancer', 'Canis Major', 'Canis Minor',
      'Capricornus', 'Cassiopeia', 'Centaurus', 'Cepheus', 'Cetus', 'Corona Borealis', 'Corvus', 'Crater', 'Cygnus',
      'Delphinus', 'Draco', 'Eridanus', 'Gemini', 'Hercules', 'Hydra', 'Leo', 'Lepus', 'Libra', 'Lyra', 'Ophiuchus',
      'Orion', 'Pegasus', 'Perseus', 'Pisces', 'Sagittarius', 'Scorpius', 'Taurus', 'Ursa Major', 'Virgo']
assert len(GL) == 39

CHAT = [
    ('Gen. Hammond', None, [
        'Remind the teams that borrowed equipment still needs a requisition.',
        'Someone is leaving coffee rings on the briefing table again.',
        'Headquarters wants a report on last week\'s report.',
        'I would like one quiet mission before the end of the quarter.']),
    ('Col. Carter', 'carter', [
        'Power readings are within tolerance. Mostly.',
        'I have three ideas for the reactor, and only one of them is loud.',
        'The gate is fine. It is whatever is on the other side that worries me.',
        'Has anyone seen my good soldering iron?']),
    ('Dr. Lee', 'lee', [
        'For the record, I did not touch the calibration. It was like that when I arrived.',
        'The coffee machine on Level 19 is making that noise again.',
        'If the lab smells like burnt toast, that is a feature.']),
    ('Dr. Jackson', 'jackson', [
        'I found a typo in a three-thousand-year-old inscription. Scribes were people too.',
        'Does anyone know where the good dictionaries went?',
        'This glyph looks familiar. That is either very good news or very bad news.']),
]
chat_js = json.dumps([{'who': w, 'perm': p, 'lines': l} for w, p, l in CHAT], ensure_ascii=False)

block = """
const EG_GL = %s;
const EG_CHAT = %s;
let egNext = 0;
const egRecent = [];

function egTick() {
  if (!state.started || !$('titlescreen').hidden || TOUR.on) return;
  if (RXG || CTG || HPG || (typeof COMG !== 'undefined' && COMG) || DRONE.isActive() || state.incoming) return;
  const now = Date.now();
  if (!egNext) { egNext = now + 240000 + Math.random() * 240000; return; }
  if (now < egNext) return;
  egNext = now + 480000 + Math.random() * 420000;
  const pool = [];
  EG_CHAT.forEach(c => { if (!c.perm || state.perm[c.perm]) c.lines.forEach(l => pool.push(c.who + ': ' + l)); });
  const fresh = pool.filter(t => !egRecent.includes(t));
  const pick = (fresh.length ? fresh : pool)[Math.floor(Math.random() * (fresh.length ? fresh : pool).length)];
  if (!pick) return;
  egRecent.push(pick);
  if (egRecent.length > 6) egRecent.shift();
  log(pick, '');
}

function egDial(wid) {
  const w = wid ? world(wid) : null;
  if (!w || !state.eg) return;
  const e = state.eg;
  if (!e.worlds[wid]) {
    e.worlds[wid] = 1;
    log('Address readout: ' + wname(w) + ' // ' + w.addr.slice(0, ADDR_LEN - 1).map(g => EG_GL[g] || '?').join(', ') + ' // point of origin ' + EG_GL[0] + '. Lock confirmed.', '');
  }
  if (e.last === wid) e.n++;
  else { e.last = wid; e.n = 1; }
  if (e.n === 5) log('Col. Carter: Fifth dial to ' + wname(w) + ' in a row. The gate does not get tired, but I am starting to.', '');
  if (state.banners && state.banners[w.level] && !e.sec[w.level]) {
    e.sec[w.level] = 1;
    log('Address record: ' + wname(w) + ' and the rest of the ' + sysOf(w.level).star + ' system are now in the permanent record.', 'ok');
  }
}

setInterval(egTick, 1000);
""" % (json.dumps(GL), chat_js)

rep("for (let i = 0; i < N; i++) GLYPHS.push(makeGlyph(i));\n", "for (let i = 0; i < N; i++) GLYPHS.push(makeGlyph(i));\n" + block)

rep('<g id="dccg${i}" class="dccg"><rect', '<g id="dccg${i}" class="dccg"><title>${EG_GL[i]}</title><rect')
rep("    log(`Chevron 7 locked. Wormhole established to ${state.planet}.`, 'ok');\n", "    log(`Chevron 7 locked. Wormhole established to ${state.planet}.`, 'ok');\n    egDial(state.dest);\n")
rep("    mini: miniFresh(),\n    chevrons: 0,", "    mini: miniFresh(),\n    eg: { worlds: {}, last: null, n: 0, sec: {} },\n    chevrons: 0,")
rep("    groups: state.groups,\n", "    groups: state.groups,\n    eg: state.eg,\n")
rep("  state.groups = d.groups || [];\n  ensureTags();\n", "  state.groups = d.groups || [];\n  ensureTags();\n  state.eg = Object.assign({ worlds: {}, last: null, n: 0, sec: {} }, d.eg || {});\n")

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
