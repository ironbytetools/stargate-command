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


assert s.count('0.9.12') == 4, s.count('0.9.12')
rep('<title>Stargate Command 0.9.12</title>', '<title>Stargate Command 0.9.13</title>')
rep('BUILD 0.9.12', 'BUILD 0.9.13', 2)
rep("const BUILD_VER = '0.9.12';", "const BUILD_VER = '0.9.13';")

a = s.index('.glcols { display: flex;')
b = s.index('.glhist {')
b = s.index('\n', b) + 1
s = s[:a] + s[b:]
marker = '#comgame { padding: 0; background: radial-gradient'
assert s.count(marker) == 1
s = s.replace(marker, part('gd.css') + marker)

rep("    log(t, 'ok');\n", "    log(t, 'ok');\n    if (GLG) GLG.out = t;\n")
rep("    log('Decoded: ' + ar.name + '. No site could be found; the artifact was recovered from the archive.', 'ok');\n",
    "    log('Decoded: ' + ar.name + '. No site could be found; the artifact was recovered from the archive.', 'ok');\n    if (GLG) GLG.out = 'No site could be found; the artifact was recovered from the archive.';\n")

a = s.index('function glWin() {')
b = s.index('function glRetry() {')
s = s[:a] + s[b:]
a = s.index('function glLibrary() {')
b = s.index('function glHints() {')
s = s[:a] + s[b:]
a = s.index('function glHints() {')
b = s.index('function glGuess3() {')
s = s[:a] + part('gd_a.js') + '\n' + part('gd_b.js') + '\n' + s[b:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
