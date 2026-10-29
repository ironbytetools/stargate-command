import sys
src, dst = sys.argv[1:3]
s = open(src, encoding='utf-8').read()
assert s.count('0.9.18') == 4, s.count('0.9.18')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('<title>Stargate Command 0.9.18</title>', '<title>Stargate Command 0.9.19</title>')
rep('BUILD 0.9.18', 'BUILD 0.9.19', 2)
rep("const BUILD_VER = '0.9.18';", "const BUILD_VER = '0.9.19';")

rep(".mc { position: absolute; z-index: 5; display: flex; gap: 6px; }", ".mc { position: absolute; z-index: 5; display: flex; gap: 6px; }\n.mc[hidden] { display: none; }")

rep('<rect x="20" y="62" width="250" height="130" rx="3" class="dccell"/>', '<rect x="20" y="62" width="230" height="130" rx="3" class="dccell"/>')
rep('<text id="dcMsCount" x="262" y="80"', '<text id="dcMsCount" x="242" y="80"')
rep('<line x1="24" y1="86" x2="266" y2="86"', '<line x1="24" y1="86" x2="246" y2="86"')
rep('<text id="dcMsNone" x="145" y="136"', '<text id="dcMsNone" x="135" y="136"')
rep('<text id="dcmt${r}" x="140" y="${y}"', '<text id="dcmt${r}" x="122" y="${y}"')
rep('<text id="dcme${r}" x="262" y="${y}"', '<text id="dcme${r}" x="242" y="${y}"')
rep("const x = 20 + (i % 2) * 129;", "const x = 20 + (i % 2) * 119;", 2)
rep('<rect x="${x}" y="${y}" width="121" height="46" rx="3" class="dccell"/>', '<rect x="${x}" y="${y}" width="111" height="46" rx="3" class="dccell"/>')
rep("sparkPoints(h, x + 66, y + 24, 48, 14)", "sparkPoints(h, x + 58, y + 24, 46, 14)")

open(dst, 'w', encoding='utf-8').write(s)
print('ok')
