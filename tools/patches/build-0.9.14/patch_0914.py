import os
import sys
src, dst = sys.argv[1:3]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()


def part(n):
    return open(os.path.join(here, n), encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:60], s.count(a))
    s = s.replace(a, b)


assert s.count('0.9.13') == 4, s.count('0.9.13')
rep('<title>Stargate Command 0.9.13</title>', '<title>Stargate Command 0.9.14</title>')
rep('BUILD 0.9.13', 'BUILD 0.9.14', 2)
rep("const BUILD_VER = '0.9.13';", "const BUILD_VER = '0.9.14';")

a = s.index('.hpform { background')
b = s.index('.hpfh {')
b = s.index('\n', b) + 1
s = s[:a] + s[b:]
css = '''#hpbody { display: flex; align-items: center; justify-content: center; overflow: hidden; }
#hpfit { position: relative; flex: none; }
#hpdev { position: absolute; left: 0; top: 0; width: 760px; height: 540px; transform-origin: 0 0; border-radius: 14px; overflow: hidden; box-shadow: 0 6px 30px rgba(0, 0, 0, 0.65); user-select: none; -webkit-user-select: none; }
#hpsvg { display: block; }
'''
marker = '#comgame { padding: 0; background: radial-gradient'
assert s.count(marker) == 1
s = s.replace(marker, css + marker)

rep("  HPG.lastOk = right;\n", "  HPG.lastOk = right;\n  HPG.marks = HPG.marks || [];\n  HPG.marks[HPG.idx] = right;\n  HPG.fl = { k: a, ok: right, t: performance.now() + 700 };\n  later(() => { if (HPG) hpDraw(); }, 750);\n")

rep("'That form should have been stamped ' + HP_TYPES[f.k].stamp + '.'", "'That form belonged in the ' + HP_TYPES[f.k].stamp + ' tab.'")
a = s.index('function hpTick() {')
b = s.index('function hpEnd(win) {')
s = s[:a] + s[b:]
a = s.index('function hpRender() {')
b = s.index('function hpPanelHtml() {')
s = s[:a] + part('hp_desk.js') + '\n' + s[b:]
rep("Optional. Stamp the pile of requisitions: 4 stamps by form type, and deny the flawed ones.", "Optional. File the pile of requisitions into the four binder tabs by form type, and deny the flawed ones.")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
