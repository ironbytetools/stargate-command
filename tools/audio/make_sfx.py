import numpy as np, subprocess, wave, os
from scipy import signal
SR=44100
rng=np.random.default_rng(7)
def T(d): return np.arange(int(d*SR))/SR
def sos(x,kind,f,order=3):
    return signal.sosfilt(signal.butter(order,f,kind,fs=SR,output='sos'),x)
def bp(x,lo,hi): return sos(x,'bandpass',[lo,hi],2)
def lp(x,f): return sos(x,'lowpass',f)
def hp(x,f): return sos(x,'highpass',f)
def wn(d): return rng.standard_normal(int(d*SR))
def ex(d,tau,att=0.002):
    t=T(d); e=np.exp(-t/tau); a=np.minimum(1,t/att) if att>0 else 1; return e*a
def put(buf,x,at):
    i=int(at*SR); n=min(len(x),len(buf)-i)
    if n>0: buf[i:i+n]+=x[:n]
def modal(freqs,taus,amps,d,detune=0.004):
    t=T(d); y=np.zeros_like(t)
    for f,tau,a in zip(freqs,taus,amps):
        f=f*(1+rng.uniform(-detune,detune)); y+=a*np.sin(2*np.pi*f*t+rng.uniform(0,6))*np.exp(-t/tau)
    return y
def thud(f0,f1,d,tau):
    t=T(d); ph=2*np.pi*(f1*t+(f0-f1)*0.06*(1-np.exp(-t/0.06))); return np.sin(ph)*np.exp(-t/tau)*np.minimum(1,t/0.003)
def room(x,rt=0.5,wet=0.25,bright=3500):
    n=int(rt*SR*1.5); t=np.arange(n)/SR
    ir=lp(rng.standard_normal(n),bright)*np.exp(-t/(rt/6.9*1.0)); ir[:int(.004*SR)]*=0
    y=signal.fftconvolve(x,ir)[:len(x)+n]
    y/= (np.abs(ir).sum()**0.5+1e-9)/np.sqrt(len(ir)) if False else 1
    wetsig=y/ (np.sqrt((ir**2).sum())+1e-9)*0.35
    out=np.zeros(len(wetsig)); out[:len(x)]+=x*(1-wet); out+=wetsig*wet*np.max(np.abs(x))/ (np.max(np.abs(wetsig))+1e-9)*1.0
    return out
def servo(d,f0,f1,teeth=0,lpf=1500):
    t=T(d); f=np.linspace(f0,f1,len(t))*(1+0.01*lp(wn(d),8)*8); ph=2*np.pi*np.cumsum(f)/SR
    y=sum(np.sin(k*ph)/k**0.9 for k in range(1,9))
    if teeth: y*=1+0.45*np.sin(2*np.pi*teeth*t)
    return lp(y,lpf)*0.4+bp(wn(d),500,2500)*0.12
def hiss(d,lo,hi,tau,att=0.004):
    return bp(wn(d),lo,hi)*ex(d,tau,att)
def beep(f,d,harm=2):
    t=T(d); y=sum(np.sin(2*np.pi*f*k*t)/k**1.5 for k in range(1,harm+1))
    e=np.minimum(1,t/0.004)*np.minimum(1,(d-t)/0.012); return bp(np.tanh(y*1.4),400,5000)*e
def clicks(times,d,gain=1):
    y=np.zeros(int(d*SR))
    for tt,g in times:
        c=hp(wn(0.02),1500)*ex(0.02,0.003,0.0005)*g*gain; c+=modal([2100,3300],[0.004,0.003],[g*.6,g*.4],0.02)*gain; put(y,c,tt)
    return y
def fin(x,peak=0.8):
    x=x-np.mean(x); return x/(np.abs(x).max()+1e-9)*peak
S={}
d=0.25; y=clicks([(0,1)],d); y+=modal([140],[0.02],[0.6],d); S['click']=fin(room(y,0.25,0.12),0.5)
y=clicks([(0,.7)],0.2); S['tick']=fin(y,0.32)
d=2.0; y=np.zeros(int(d*SR))
put(y,servo(0.3,180,260,teeth=0,lpf=900)*np.minimum(1,T(.3)/.1)*np.minimum(1,(0.3-T(.3))/.08)*0.45,0)
put(y,clicks([(0.05+i*0.045,0.4) for i in range(5)],0.5),0)
at=0.3
put(y,thud(90,36,0.7,0.16)*1.0,at); put(y,modal([210,367,611,980,1540,2300],[.14,.11,.09,.06,.04,.03],[.5,.35,.3,.2,.12,.08],0.6)*0.8,at)
put(y,hp(wn(0.015),1500)*ex(0.015,0.004,0.0005)*1.0,at); put(y,hiss(0.45,2200,7500,0.12)*0.25,at+0.02)
S['chevron']=fin(room(y,0.9,0.22),0.85)
d=2.4; y=np.zeros(int(d*SR))
put(y,hiss(1.2,1500,7000,0.4,0.01)*0.5,0)
put(y,servo(1.0,230,55,lpf=1100)*np.linspace(1,0,int(1.0*SR))**1.2*0.7,0.05)
put(y,thud(70,30,0.6,0.15)*0.8,0.85); put(y,modal([180,310,520,860],[.2,.16,.1,.06],[.4,.3,.2,.1],0.8)*0.5,0.85)
S['fail']=fin(room(y,1.0,0.25),0.8)
d=4.2; y=np.zeros(int(d*SR)); t=T(d)
n=wn(d); c=np.exp(np.interp(t,[0,0.5,1.3,3.0],[np.log(160),np.log(900),np.log(2600),np.log(700)]))
rush=np.zeros(len(t)); blk=1024; zi=None
for k in range(0,len(t),blk):
    cc=c[k]; s=signal.butter(2,[cc*0.6,min(cc*1.7,20000)],'bandpass',fs=SR,output='sos')
    if zi is None: zi=signal.sosfilt_zi(s)*0
    seg,zi=signal.sosfilt(s,n[k:k+blk],zi=zi); rush[k:k+blk]=seg
amp=np.interp(t,[0,0.12,0.6,1.1,2.2,4.2],[0,0.5,1.0,0.8,0.25,0])
swirl=1+0.35*lp(wn(d),6)/ (lp(wn(d),6).std()+1e-9)*0.4
y+=rush*amp*np.clip(swirl,0.4,1.6)*1.2
put(y,thud(55,24,2.0,0.55)*1.1,0.12)
put(y,hp(wn(1.3),3500)*(rng.random(int(1.3*SR))<0.012)*ex(1.3,0.5,0.001)*1.0,0.9)
put(y,modal([312,468,744,1100],[1.2,1.0,.8,.6],[.12,.1,.08,.05],2.5)*0.8,0.3)
S['kawoosh']=fin(room(y,1.6,0.3),0.9)
d=2.6; y=np.zeros(int(d*SR)); t=T(d)
n=wn(d); c=np.exp(np.interp(t,[0,0.5,1.2,2.2],[np.log(2600),np.log(900),np.log(220),np.log(100)]))
rush=np.zeros(len(t)); zi=None
for k in range(0,len(t),blk):
    cc=c[k]; s=signal.butter(2,[cc*0.6,min(cc*1.7,20000)],'bandpass',fs=SR,output='sos')
    if zi is None: zi=signal.sosfilt_zi(s)*0
    seg,zi=signal.sosfilt(s,n[k:k+blk],zi=zi); rush[k:k+blk]=seg
y+=rush*np.interp(t,[0,0.1,0.7,1.6,2.6],[0.2,1.0,0.6,0.15,0])*1.0
put(y,thud(60,28,1.0,0.22)*0.9,0.04); put(y,thud(45,26,0.5,0.15)*0.8,1.15)
S['shutdown']=fin(room(y,1.3,0.28),0.85)
d=2.0; y=np.zeros(int(d*SR)); t=T(d)
m=servo(1.05,68,112,teeth=24,lpf=1000)*np.minimum(1,T(1.05)/0.15)*np.minimum(1,(1.05-T(1.05))/0.1)
put(y,m,0.02); put(y,bp(wn(1.0),700,2600)*np.minimum(1,T(1.0)/0.2)*np.minimum(1,(1.0-T(1.0))/0.1)*0.22,0.05)
put(y,clicks([(0.1+0.1*i-0.004*i*i,0.45) for i in range(10)],1.2),0)
at=1.08; put(y,modal([118,205,340,590,880,1330],[.3,.22,.16,.1,.07,.05],[.6,.5,.35,.25,.15,.1],1.0)*1.0,at); put(y,thud(80,34,0.6,0.15)*1.1,at); put(y,hp(wn(0.02),1200)*ex(0.02,0.004,0.0004),at)
S['iris']=fin(room(y,0.9,0.22),0.85)
y=np.zeros(int(0.5*SR)); put(y,beep(1050,0.09),0); put(y,beep(1400,0.13),0.14); S['chime']=fin(room(y,0.3,0.12),0.5)
S['ok']=fin(room(beep(1250,0.07),0.2,0.1),0.4)
y=np.zeros(int(0.7*SR))
for i in range(2): put(y,bp(np.tanh(2*np.sign(np.sin(2*np.pi*330*T(0.17)))+0.0)*np.minimum(1,T(.17)/.005)*np.minimum(1,(.17-T(.17))/.02),250,3200),i*0.26)
S['warn']=fin(room(y,0.35,0.15),0.55)
y=np.zeros(int(0.6*SR))
for i in range(3): put(y,beep(920,0.09,3),i*0.17)
S['alert']=fin(room(y,0.3,0.12),0.5)
d=1.0; t=T(d); f=np.exp(np.interp(t,[0,0.45,0.9],[np.log(500),np.log(780),np.log(560)])); ph=2*np.pi*np.cumsum(f)/SR
y=sum(np.sin(k*ph+0.3*k)/k**0.8 for k in range(1,9)); y=np.tanh(y*0.9)
e=np.minimum(1,t/0.05)*np.minimum(1,np.maximum(0,(0.95-t))/0.18+0.0); y=bp(y,300,5200)*e
S['pulse']=fin(room(y,0.9,0.3),0.75)
S['pulse']=S['pulse'][:int(1.25*SR)]*np.minimum(1,(1.25-T(1.25))/0.3)
gain={'click':.5,'tick':.35,'chevron':1,'fail':.9,'kawoosh':1,'shutdown':.9,'iris':.9,'chime':.5,'ok':.4,'warn':.6,'alert':.55,'pulse':.7}
os.makedirs('sfx',exist_ok=True)
reel=[]
for k,x in S.items():
    x=(x*gain[k]).astype(np.float32)
    with wave.open(f'sfx/{k}.wav','wb') as w: w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((x*32767).astype(np.int16).tobytes())
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'sfx/{k}.wav','-ac','1','-b:a','80k',f'sfx/{k}.mp3'],check=True)
    reel.append(x); reel.append(np.zeros(int(.6*SR),dtype=np.float32)); print(k,round(len(x)/SR,2),os.path.getsize(f'sfx/{k}.mp3'))
r=np.concatenate(reel)
with wave.open('reel2.wav','wb') as w: w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((r*32767).astype(np.int16).tobytes())
