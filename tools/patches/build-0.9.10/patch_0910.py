import json
import sys
src, dst = sys.argv[1:3]
s = open(src, encoding='utf-8').read()
assert s.count('0.9.9') == 4, s.count('0.9.9')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('<title>Stargate Command 0.9.9</title>', '<title>Stargate Command 0.9.10</title>')
rep('BUILD 0.9.9', 'BUILD 0.9.10', 2)
rep("const BUILD_VER = '0.9.9';", "const BUILD_VER = '0.9.10';")

rep("{ id: 'langford', name: 'Dr. Catherine Langford', role: 'Linguist', room: 'arch', level: 2, cost: 150 }",
    "{ id: 'jackson', name: 'Dr. Daniel Jackson', role: 'Linguist', room: 'arch', level: 2, cost: 150 }")
rep("'Dr. Langford: ", "'Dr. Jackson: ", 3)
rep("  if (state.perm.felger) { state.perm.lee = true; delete state.perm.felger; }\n",
    "  if (state.perm.felger) { state.perm.lee = true; delete state.perm.felger; }\n  if (state.perm.langford) { state.perm.jackson = true; delete state.perm.langford; }\n")
assert 'Langford' not in s and 'langford' not in s.replace("state.perm.langford", "").replace("delete state.perm.langford", "")

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from questions import Q
items = []
for c, q, r, f in Q:
    assert len(f) == 3
    items.append('  { cat: %s, q: %s, real: %s, fake: [%s] }' % (json.dumps(c), json.dumps(q, ensure_ascii=False), json.dumps(r, ensure_ascii=False), ', '.join(json.dumps(x, ensure_ascii=False) for x in f)))
rep("] }\n];\nlet HPG = null;", "] },\n" + ",\n".join(items) + "\n];\nlet HPG = null;")

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s), len(Q))
