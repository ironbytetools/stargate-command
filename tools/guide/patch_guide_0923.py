s = open('build_guide.py', encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


rep('BUILD = "0.9.22"', 'BUILD = "0.9.23"')
rep('content: "BUILD 0.9.22  //  TRAINING COPY"', 'content: "BUILD 0.9.23  //  TRAINING COPY"')
rep('["Assault cooldown","20 minutes after any assault"]', '["Assault cooldown","15 minutes after any assault"]')
open('build_guide.py', 'w', encoding='utf-8').write(s)
print('ok')
