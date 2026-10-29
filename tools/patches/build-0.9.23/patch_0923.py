import sys
src, dst = sys.argv[1:3]
s = open(src, encoding='utf-8').read()
assert s.count('0.9.22') == 4, s.count('0.9.22')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('<title>Stargate Command 0.9.22</title>', '<title>Stargate Command 0.9.23</title>')
rep('BUILD 0.9.22', 'BUILD 0.9.23', 2)
rep("const BUILD_VER = '0.9.22';", "const BUILD_VER = '0.9.23';")
rep('const ASSAULT_CD_MS = 20 * 60000;', 'const ASSAULT_CD_MS = 15 * 60000;')
rep("' Assault cooldown started: 20:00.'", "' Assault cooldown started: 15:00.'")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
