import re
import sys
src, dst = sys.argv[1:3]
s = open(src, encoding='utf-8').read()
assert s.count('0.9.5') == 4, s.count('0.9.5')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('<title>Stargate Command 0.9.5</title>', '<title>Stargate Command 0.9.6</title>')
rep('BUILD 0.9.5', 'BUILD 0.9.6', 2)
rep("const BUILD_VER = '0.9.5';", "const BUILD_VER = '0.9.6';")

pat = re.compile(r'<div id="(comgame|rxgame|glgame|hpgame|ctgame)" hidden>\n  <div class="titlebox">\n(?:    .*\n)+?  </div>\n</div>\n')
blocks = {}


def grab(m):
    blocks[m.group(1)] = m.group(0).rstrip('\n')
    return ''


s = pat.sub(grab, s)
assert sorted(blocks) == ['comgame', 'ctgame', 'glgame', 'hpgame', 'rxgame'], sorted(blocks)

rep('    <div class="panel" id="room"></div>',
    '    <div class="panel" id="room"><div id="roomin"></div>\n' + '\n'.join(blocks[k] for k in ['rxgame', 'glgame', 'hpgame', 'ctgame']) + '\n    </div>')

i = s.index('<div class="panel" id="dcpanel">')
j = s.index('<h2>Dialing computer</h2>', i)
s = s[:j] + blocks['comgame'] + '\n        ' + s[j:]

rep("""  $('room').__h = rh;
  $('room').innerHTML = rh;""", """  $('room').__h = rh;
  $('roomin').innerHTML = rh;""")
rep("""  if ($('room').__h === rh) { HELD.delete('room'); return; }""", """  $('room').dataset.r = k;
  if ($('room').__h === rh) { HELD.delete('room'); return; }""")

rep("""function selectRoom(k) {
  state.room = k;""", """function hpLocked() { return typeof HPG !== 'undefined' && !!HPG && !HPG.res; }
function comLocked() { return typeof COMG !== 'undefined' && !!COMG && !COMG.ended && COMG.phase !== 'drone'; }

function selectRoom(k) {
  if (hpLocked() && k !== 'brief') { log('Finish the requisitions or WALK AWAY before leaving the Briefing Room.', 'warn'); return; }
  state.room = k;""")
rep("""  if (name !== 'gate' && window.DRONE && DRONE.isActive()) return;
  document.body.classList.toggle('gv', name === 'gate');""", """  if (name !== 'gate' && window.DRONE && DRONE.isActive()) return;
  if (name !== 'gate' && comLocked()) { log('Finish the COMM contact or close it before leaving the Gate Room.', 'warn'); return; }
  if (name !== 'base' && hpLocked()) { log('Finish the requisitions or WALK AWAY before leaving the Briefing Room.', 'warn'); return; }
  document.body.classList.toggle('gv', name === 'gate');""")

rep("""  if (!state.started || RXG || (typeof COMG !== 'undefined' && COMG)) return;
  const r = state.rx;
  if (!r || !(r.node || r.evt)) return;""", """  if (!state.started || RXG || (typeof COMG !== 'undefined' && COMG) || hpLocked()) return;
  if (document.body.classList.contains('gv') || state.room !== 'quarter') return;
  const r = state.rx;
  if (!r || !(r.node || r.evt)) return;""")

rep("""  if (document.body.classList.contains('gv') || window.innerWidth <= 900) { if (m.style.minHeight) m.style.minHeight = ''; return; }
  const top = (m.getBoundingClientRect().top + window.scrollY) / FIT.s;
  const v = Math.max(480, window.innerHeight / FIT.s - top) + 'px';
  if (m.style.minHeight !== v) m.style.minHeight = v;""", """  if (m.style.minHeight) m.style.minHeight = '';
  if (document.body.classList.contains('gv') || window.innerWidth <= 900) { if (m.style.height) m.style.height = ''; return; }
  const top = (m.getBoundingClientRect().top + window.scrollY) / FIT.s;
  const v = Math.max(480, window.innerHeight / FIT.s - top) + 'px';
  if (m.style.height !== v) m.style.height = v;""")
rep("""  FIT.lock = 0;
  if (m) m.style.maxWidth = '';""", """  FIT.lock = 0;
  fitMain();
  if (m) m.style.maxWidth = '';""")

css = """
@media (min-width: 901px) {
  body:not(.gv) main { grid-template-rows: minmax(0, 1fr) 250px; align-items: stretch; overflow: hidden; }
  body:not(.gv) #view-base > .panel:first-child { align-self: stretch; min-height: 0; overflow-y: auto; }
  body:not(.gv) #view-base > #room { min-height: 0; overflow: hidden; position: relative; display: flex; flex-direction: column; }
  body.gv main { grid-template-rows: auto 275px; }
  body.gv #missionpanel { min-height: 0; overflow: hidden; display: flex; flex-direction: column; }
  body.gv #missionpanel #dispatch { flex: 1 1 0; min-height: 0; overflow-y: auto; }
  body.gv .panel.wide { min-height: 0; overflow: hidden; }
}
#roomin { flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; }
#roomin > .rbody { flex: 1 1 0; min-height: 0; overflow-y: auto; }
.panel.wide { display: flex; flex-direction: column; }
body:not(.gv) .panel.wide > .log, body.gv .panel.wide > .log { flex: 1 1 0; height: auto; min-height: 0; overflow-y: auto; }
body:not(.gv) .panel.wide > #briefs:not([hidden]), body.gv .panel.wide > #briefs:not([hidden]) { flex: 1 1 0; height: auto; min-height: 0; }
#dcpanel { position: relative; }
#comgame, #rxgame, #glgame, #hpgame, #ctgame { position: absolute; inset: 0; z-index: 30; display: flex; flex-direction: column; align-items: stretch; justify-content: flex-start; overflow: hidden; padding: 12px; background: var(--panel); }
#comgame[hidden], #rxgame[hidden], #glgame[hidden], #hpgame[hidden], #ctgame[hidden] { display: none; }
#comgame > *, #rxgame > *, #glgame > *, #hpgame > *, #ctgame > * { margin: 0; }
#comgame .titlebox, #rxgame .titlebox, #glgame .titlebox, #hpgame .titlebox, #ctgame .titlebox { width: 100%; flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; }
#comgame .titlebox .title, #rxgame .titlebox .title, #glgame .titlebox .title, #hpgame .titlebox .title, #ctgame .titlebox .title { text-align: left; font-size: var(--fs-sm); letter-spacing: 0.22em; color: var(--accent); }
#comgame .titlebox .title::after, #rxgame .titlebox .title::after, #glgame .titlebox .title::after, #hpgame .titlebox .title::after, #ctgame .titlebox .title::after { display: none; }
#comgame .titlebox .sub, #rxgame .titlebox .sub, #glgame .titlebox .sub, #hpgame .titlebox .sub, #ctgame .titlebox .sub { text-align: left; margin-bottom: 8px; }
#combody, #rxbody, #glbody, #hpbody, #ctbody { flex: 1 1 0; min-height: 0; overflow-y: auto; border: 0; box-shadow: none; background: transparent; padding: 0; }
#room:not([data-r="quarter"]) > #rxgame, #room:not([data-r="arch"]) > #glgame, #room:not([data-r="brief"]) > #hpgame, #room:not([data-r="lab"]) > #ctgame { display: none; }
"""
rep('</style>\n</head>', css + '</style>\n</head>')

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
