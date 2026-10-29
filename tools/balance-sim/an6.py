import json,sys,statistics as st
rs=[]
for f in sys.argv[1:]: rs+=json.load(open(f))
n=len(rs); print('sessions',n,'errs',sum(len(r['errs']) for r in rs))
cl=[r['lvT'].get('cleared') for r in rs if r['lvT'].get('cleared')]
print('cleared',len(cl),'median',round(st.median(cl),1),'range',round(min(cl)),round(max(cl)))
dur={i:[] for i in range(1,6)}
for r in rs:
    t=r['lvT']; prev=0
    for i,k in enumerate(['2','3','4','5','cleared'],1):
        if k in t: dur[i].append(t[k]-prev); prev=t[k]
print('level minutes',{i:round(st.median(v),0) for i,v in dur.items() if v})
for lv in range(1,6):
    a=[(e['p'],e['won']) for r in rs for e in r['ev'] if e['k']=='assault' and e['lvl']==lv]
    if a: print(' L%d assaults %d est %.2f win %.2f'%(lv,len(a),sum(p for p,w in a)/len(a),sum(w for p,w in a)/len(a)))
m=lambda key,k: round(st.mean([r[key].get(k,0) for r in rs]))
print('inc',{k:m('inc',k) for k in ['explore','logistics','fob','tk','spoils']})
print('spent',{k:m('spent',k) for k in ['assault','raise','gear','fob','lab','gateSup']})
print('end sup/rp',round(st.mean([r['sup'] for r in rs])),round(st.mean([r['research'] for r in rs])))
print('raids unanswered',round(st.mean([r['stats']['raidsUnanswered'] for r in rs]),1),'overruns',round(st.mean([r['stats']['fobOverrun'] for r in rs]),2),'fob stock max',round(st.mean([r['stats']['fobStockMax'] for r in rs])))
v=[r['tierT'].get('g4') for r in rs if r.get('tierT') and r['tierT'].get('g4')]
if v: print('Reactor I minute',round(st.median(v)))
for L in ['1','2','3','4','5']:
    a=[r['lvAvg'][L] for r in rs if L in r['lvAvg']]
    if a: print(' stock L'+L,round(st.mean([x['sup']/x['n'] for x in a])),round(st.mean([x['rp']/x['n'] for x in a])))
for L in range(1,6):
    pts=[s for r in rs for s in r['series'] if s[5]==L]
    if pts: print(' power<40 L%d %.2f'%(L,sum(1 for s in pts if s[2]<40)/len(pts)))
