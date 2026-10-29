import sys
src, dst = sys.argv[1:3]
s = open(src, encoding='utf-8').read()
assert s.count('0.9.19') == 4, s.count('0.9.19')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('<title>Stargate Command 0.9.19</title>', '<title>Stargate Command 0.9.22</title>')
rep('BUILD 0.9.19', 'BUILD 0.9.22', 2)
rep("const BUILD_VER = '0.9.19';", "const BUILD_VER = '0.9.22';")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
