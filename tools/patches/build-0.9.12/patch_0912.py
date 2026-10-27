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


# version
assert s.count('0.9.11') == 4, s.count('0.9.11')
rep('<title>Stargate Command 0.9.11</title>', '<title>Stargate Command 0.9.12</title>')
rep('BUILD 0.9.11', 'BUILD 0.9.12', 2)
rep("const BUILD_VER = '0.9.11';", "const BUILD_VER = '0.9.12';")

# CSS: drop old grid/relay rules, add device rules
a = s.index('.rxgrid { display: grid;')
b = s.index('.rxout.over {')
b = s.index('\n', b) + 1
s = s[:a] + s[b:]
rep('#rxgame .controls button { min-width: 84px; }\n', '')
marker = '#comgame { padding: 0; background: radial-gradient'
assert s.count(marker) == 1
s = s.replace(marker, part('rx_device.css') + marker)

# JS: replace from rxGenNode up to the poll interval, keep preset button + panel helpers
a = s.index('function rxGenNode(size) {')
m1 = s.index('function rxPresetButtons() {')
m2 = s.index('function rxRender() {')
z = s.index('setInterval(rxPoll, 1000);')
mid = s[m1:m2]
new = part('rx_a.js') + '\n' + part('rx_b.js') + '\n' + part('rx_c.js') + '\n' + mid
s = s[:a] + new + s[z:]
# constants only used by the old relay puzzle
rep('const RX_NODE_TIER = 5;\nconst RX_NODE_ZPM = 7;\n', '')

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
