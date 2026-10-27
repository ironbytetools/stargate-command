import re, sys

src = open('base085.html', encoding='utf-8').read()


def rep(old, new, count=1):
    global src
    n = src.count(old)
    if n != count:
        print('MISMATCH', n, 'expected', count, 'for', old[:100])
        sys.exit(1)
    src = src.replace(old, new)


rep('<title>Stargate Command 0.8.4</title>', '<title>Stargate Command 0.8.5</title>')
rep('BUILD 0.8.4</div>', 'BUILD 0.8.5</div>', 2)

m = re.search(r'<div class="controls" style="margin:0"><button onclick="openMenu\(\)">MENU</button>.*?id="fsbtn" onclick="toggleFullscreen\(\)">FULL SCREEN</button></div>', src)
if not m:
    print('MISSING header controls')
    sys.exit(1)
tools = m.group(0)
btns = re.findall(r'<button id="(?:helpbtn|mute|fsbtn)".*?</button>', tools)
if len(btns) != 3:
    print('MISSING tool buttons', len(btns))
    sys.exit(1)
src = src.replace(tools, '<div class="controls" style="margin:0"><button onclick="openMenu()">MENU</button></div>')

rep('''    <div class="title" style="font-size:16px">GAME MENU</div>
    <div class="sub">SAVE AND EXIT</div>
''', '''    <div class="title" style="font-size:16px">GAME MENU</div>
    <div class="sub">OPTIONS, SAVE AND EXIT</div>
    <div class="panel" style="margin-bottom:10px"><h2>Options</h2><div class="controls"><button onclick="openSettings()">SETTINGS</button>''' + ''.join(btns) + '''</div></div>
''')
rep('<button onclick="closeMenu()">RETURN TO GAME</button><button onclick="openSettings()">SETTINGS</button><button onclick="toTitle()">EXIT TO TITLE SCREEN</button>',
    '<button onclick="closeMenu()">RETURN TO GAME</button><button onclick="toTitle()">EXIT TO TITLE SCREEN</button>')

rep('#dcwrap { max-width: calc((100vh - 250px) * 800 / 560); margin: 0 auto; }', '#dcwrap { max-width: calc((var(--vh, 100vh) - 250px) * 800 / 560); margin: 0 auto; }')
rep('.scroll.mdetail { max-height: 64vh; }', '.scroll.mdetail { max-height: calc(var(--vh, 100vh) * 0.64); }')

css = '''
:root { --vh: 950px; }
html { overflow-x: hidden; }
#fit { position: relative; width: 100%; overflow: hidden; }
#stage { position: absolute; left: 0; top: 0; transform-origin: 0 0; }
'''
i = src.index('</style>')
src = src[:i] + css + src[i:]

rep('<body>\n<header>', '<body>\n<div id="fit"><div id="stage">\n<header>')
rep('</main>\n<div id="comgame" hidden>', '</main>\n</div></div>\n<div id="comgame" hidden>')

rep('const N = 39;\n', '''const N = 39;
const FIT = { s: 1, W: 1500, H: { gate: 1120, base: 1000 }, min: 0.6, max: 1.6 };
''')

rep("  const h = sm.getBoundingClientRect().bottom - pad - m.getBoundingClientRect().top - $('smpanel').offsetHeight - 8;\n",
    "  const h = (sm.getBoundingClientRect().bottom - m.getBoundingClientRect().top) / FIT.s - pad - $('smpanel').offsetHeight - 8;\n")
rep("  const top = m.getBoundingClientRect().top + window.scrollY;\n  const v = Math.max(480, window.innerHeight - top) + 'px';\n",
    "  const top = (m.getBoundingClientRect().top + window.scrollY) / FIT.s;\n  const v = Math.max(480, window.innerHeight / FIT.s - top) + 'px';\n")

rep("  if (name === 'gate') { renderStarmap(); state.worlds.forEach(w => { w.fresh = false; }); }\n}\n",
    "  if (name === 'gate') { renderStarmap(); state.worlds.forEach(w => { w.fresh = false; }); }\n  fitScreen();\n}\n")

fit_js = '''
function fitScreen() {
  const st = $('stage');
  const fit = $('fit');
  if (!st || !fit) return;
  const gate = document.body.classList.contains('gv');
  let wc = FIT.W;
  st.style.width = wc + 'px';
  st.style.transform = 'scale(1)';
  const h = gate ? st.offsetHeight : FIT.H.base;
  const s = Math.max(FIT.min, Math.min(FIT.max, window.innerWidth / wc, window.innerHeight / h));
  if (window.innerWidth / s < wc) { wc = window.innerWidth / s; st.style.width = wc + 'px'; }
  FIT.s = s;
  st.style.transform = 'scale(' + s + ')';
  st.style.left = Math.max(0, (window.innerWidth - wc * s) / 2) + 'px';
  fit.style.height = (st.offsetHeight * s) + 'px';
  fitStarmap();
}

window.addEventListener('resize', fitScreen);
if (window.ResizeObserver) new ResizeObserver(() => { const st = $('stage'); if (st) $('fit').style.height = (st.offsetHeight * FIT.s) + 'px'; }).observe($('stage'));

loadSettings();
'''
rep('\nloadSettings();\n', fit_js)
rep('showTitle();\nrenderAll();\n', 'showTitle();\nrenderAll();\nfitScreen();\n')

open('out085.html', 'w', encoding='utf-8').write(src)
print('ok', len(src))
