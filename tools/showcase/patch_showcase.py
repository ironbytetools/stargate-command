import os
import sys
src, dst = sys.argv[1:3]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()


def part(n):
    return open(os.path.join(here, n), encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)


i = s.index('<script>const AUDIO_DATA')
j = s.index('</script>', i) + len('</script>')
s = s[:i] + '<script>const AUDIO_DATA={};</script>' + s[j:]
import re
s, nt = re.subn(r'<title>Stargate Command [0-9.]+</title>', '<title>Stargate Command Minigame Showcase</title>', s)
assert nt == 1
rep("const SAVE_KEY = 'sgc-command-save-';", "const SAVE_KEY = 'sgc-showcase-save-';")
rep('<head>', '<head>\n<script>window.SC = true;</script>')
rep('function autosaveNow() {\n', 'function autosaveNow() {\n  if (window.SC) return;\n')
rep('function scheduleAutosave() {\n', 'function scheduleAutosave() {\n  if (window.SC) return;\n')
rep('function startIncoming(ret) {\n', 'function startIncoming(ret) {\n  if (window.SC) return;\n')
rep('function egTick() {\n', 'function egTick() {\n  if (window.SC) return;\n')
rep('function rxPoll() {\n', 'function rxPoll() {\n  if (window.SC) return;\n')
rep("w.status !== 'captured' && w.intel < 2) || null;", "w.status !== 'captured' && w.intel < 2) || (window.SC ? { id: -99, intel: 0 } : null);")
rep('const s = atob(AUDIO_DATA[k]);', "const s = atob(AUDIO_DATA[k] || '');")
marker = '#comgame { padding: 0; background: radial-gradient'
assert s.count(marker) == 1
s = s.replace(marker, part('sc.css') + marker)
rep('</body>', '<script>\n' + part('sc.js') + '</script>\n</body>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
