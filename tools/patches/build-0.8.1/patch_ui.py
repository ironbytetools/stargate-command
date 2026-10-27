import sys, os
d = os.path.dirname(os.path.abspath(__file__))
src, dst = sys.argv[1], sys.argv[2]
h = open(src, encoding='utf-8').read()

def rep(old, new, count=1):
    global h
    assert h.count(old) == count, (old[:70], h.count(old))
    h = h.replace(old, new)

css = '''
.rico { width: 31px; height: 22px; flex: none; vertical-align: middle; margin-right: 8px; }
.schip .rico { width: 24px; height: 17px; margin-right: 6px; margin-left: -4px; }
.rsec { border: 1px solid var(--steel-dim); background: rgba(8, 17, 29, 0.65); box-shadow: inset 0 0 10px rgba(var(--accent-rgb), 0.08); padding: 10px 12px; min-width: 0; }
.rsec > h2:first-child { margin-top: 0; }
.rcol.narrow { max-width: none; }
.rcol { display: flex; flex-direction: column; gap: 10px; min-width: 0; }
#room > .rbody { display: flex; flex-direction: column; gap: 10px; min-width: 0; }
.rcol > .rsec:last-child { flex: 1 1 auto; }
.staff-row > span:first-child .rico, .res-row > span:first-child .rico, .dispatch-row .rico { margin-right: 8px; }
.staff-row > span:last-child, .res-row > span:last-child, .dispatch-row > div:last-child { display: inline-flex; align-items: center; justify-content: flex-end; flex-wrap: wrap; gap: 4px 8px; text-align: right; }
.staff-row, .res-row, .dispatch-row { align-items: center; min-height: calc(var(--ctl-sm) + 12px); }
button, input.nm, select.msel, .rico { box-sizing: border-box; vertical-align: middle; }
input.nm, select.msel { line-height: normal; }
.addrow, .controls { align-items: center; }
.res-row select.msel { flex: 0 0 190px; width: 190px; }
.staff-row input.nm { width: 190px; }
.rlab { display: inline-block; min-width: 108px; }
@media (min-width: 901px) {
  body:not(.gv) main { grid-template-rows: minmax(0, 1fr) auto; align-items: stretch; }
  body:not(.gv) #view-base > .panel:first-child { align-self: start; }
  body:not(.gv) #room { align-self: stretch; display: flex; flex-direction: column; }
  #room > .rbody { flex: 1 1 auto; }
  #room > .rbody > .rgrid { flex: 1 1 auto; }
  #room > .rbody > .rsec:last-child { flex: 1 1 auto; }
}
'''
i = h.index('</style>')
h = h[:i] + css + h[i:]

rep("$('room').innerHTML = `<h2>${r.name} // ${r.lvl}</h2><p class=\"dim help\">${r.desc}</p>` + strip + body;",
    "$('room').innerHTML = `<h2>${r.name} // ${r.lvl}</h2><p class=\"dim help\">${r.desc}</p>` + strip + '<div class=\"rbody\">' + body + '</div>';\n  sectionize($('room').querySelector('.rbody'));")

rep('<span class="schip"><span class="sdot${m.status === \'injured\' ? \' inj\' : \'\'}"></span><b>${m.name}</b>',
    '<span class="schip">${roleIcon(m.role, m.team && m.team.type, m.status)}<b>${m.name}</b>')
rep('`<div class="staff-row"><span><b>${m.name}</b> <span class="dim">${m.role}${m.team',
    '`<div class="staff-row"><span>${roleIcon(m.role, m.team && m.team.type, m.status)}<b>${m.name}</b> <span class="dim">${m.role}${m.team')
rep('<div class="staff-row"><span><span class="dim">${m.role}</span> <input class="nm"',
    '<div class="staff-row"><span>${roleIcon(m.role, t.type, m.status)}<span class="dim rlab">${m.role}</span><input class="nm"')
rep('h += `<div class="staff-row"><span><b>${p.name}</b> <span class="dim">${p.role}</span></span><span>${act}</span></div>`;',
    'h += `<div class="staff-row"><span>${roleIcon(p.role, \'\', \'ready\')}<b>${p.name}</b> <span class="dim">${p.role}</span></span><span>${act}</span></div>`;')

js = open(os.path.join(d, 'roleico.js'), encoding='utf-8').read() + '\n' + open(os.path.join(d, 'roleicon.js'), encoding='utf-8').read()
rep('function staffStripHtml(list, empty) {', js + '\nfunction staffStripHtml(list, empty) {')
rep("const st = 'font-size:var(--fs-xs);padding:2px 8px;margin-left:10px;min-height:0';", "const st = 'margin-left:10px';")
rep('Stargate Command 0.8.0', 'Stargate Command 0.8.1')
rep('BUILD 0.8.0', 'BUILD 0.8.1', 2)
exec(open(os.path.join(d, 'lists_part.py'), encoding='utf-8').read())
open(dst, 'w', encoding='utf-8').write(h)
