import json,sys,statistics as st
rs=[]
for f in sys.argv[1:]: rs+=json.load(open(f))
n=len(rs); print('sessions',n)
def med(x): x=[v for v in x if v is not None]; return (st.median(x) if x else None)
print('level reached (min): ',{k:(med([r['lvT'].get(k) for r in rs]), min([r['lvT'].get(k) for r in rs if r['lvT'].get(k)] or [0]), max([r['lvT'].get(k) for r in rs if r['lvT'].get(k)] or [0])) for k in ['2','3','4','5','cleared']})
for L in ['2','3','4','5']:
    pass
d=[]
for r in rs:
    t=r['lvT']; d.append([t.get('2'),(t.get('3') or 0)-(t.get('2') or 0),(t.get('4') or 0)-(t.get('3') or 0),(t.get('5') or 0)-(t.get('4') or 0)])
print('minutes spent on L1..L4 (median):',[med([x[i] for x in d]) for i in range(4)])
tot=lambda k,key: sum(r[key].get(k,0) for r in rs)/n
print('\nINCOME per session (avg), supplies:')
for k in ['explore','logistics','fob','tk','spoils']: print('  ',k, round(tot(k,'inc')))
print('INCOME RP:'); 
for k in ['expRP','fobRP','tkRP','spoilsRP']: print('  ',k, round(tot(k,'inc')))
print('SPEND supplies:')
for k in ['explore','recon','assault','raise','replace','lab','gateSup','gear','fob','tkBuy','tkFee']: print('  ',k, round(tot(k,'spent')))
print('SPEND RP:')
for k in ['gate','arm','veh']: print('  ',k, round(tot(k,'spentRP')))
print('final sup/rp at end (avg):', round(sum(r['sup'] for r in rs)/n), round(sum(r['research'] for r in rs)/n))
print('stats', {k:round(sum(r['stats'].get(k,0) for r in rs)/n,1) for k in rs[0]['stats']})
print('wait', {k:round(sum(r['wait'].get(k,0) for r in rs)/n) for k in rs[0]['wait']})
print('\nAverage stockpile per level (sup / rp / power):')
for L in ['1','2','3','4','5']:
    a=[r['lvAvg'][L] for r in rs if L in r['lvAvg']]
    if a: print('  L'+L, round(sum(x['sup']/x['n'] for x in a)/len(a)), round(sum(x['rp']/x['n'] for x in a)/len(a)), round(sum(x['pw']/x['n'] for x in a)/len(a)))
ae=[(e['p'],e['won']) for r in rs for e in r['ev'] if e['k']=='assault']
if ae:
    print('\nassaults',len(ae),'mean est',round(sum(p for p,w in ae)/len(ae),3),'win rate',round(sum(w for p,w in ae)/len(ae),3))
    for lord in (False,True):
        a=[(e['p'],e['won']) for r in rs for e in r['ev'] if e['k']=='assault' and e['lord']==lord]
        if a: print('  lord' if lord else '  non-lord',len(a),round(sum(p for p,w in a)/len(a),3),round(sum(w for p,w in a)/len(a),3))
    for L in range(1,6):
        a=[(e['p'],e['won']) for r in rs for e in r['ev'] if e['k']=='assault' and e['lvl']==L]
        if a: print('  L%d'%L,len(a),'avg est',round(sum(p for p,w in a)/len(a),2),'win',round(sum(w for p,w in a)/len(a),2))
print('\nlevel-wise avg power wait share estimated from series (power<50%):')
for L in range(1,6):
    pts=[s for r in rs for s in r['series'] if s[5]==L]
    if pts: print('  L%d'%L, 'avg power',round(sum(s[2] for s in pts)/len(pts)),'share<40:',round(sum(1 for s in pts if s[2]<40)/len(pts),2), 'avg FOBs',round(sum(s[6] for s in pts)/len(pts),1),'avg fob stock',round(sum(s[7] for s in pts)/len(pts)))
tmax=[r['done']['t'] if r['done'] else 700 for r in rs]
print('\nwall minutes avg', round(sum(tmax)/n))
