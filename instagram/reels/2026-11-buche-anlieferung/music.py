# Dezente, rhythmische Instrumentalspur, selbst synthetisiert (keine Fremdrechte).
import numpy as np, wave, sys
SR=44100; BPM=100; BEAT=60/BPM; DUR=30.0
N=int(SR*DUR); t=np.arange(N)/SR
out=np.zeros(N); rng=np.random.default_rng(7)
def f(n): return 440*2**((n-69)/12)
# Am F C G  (MIDI)
chords=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]
roots=[45,41,36,43]
BAR=4*BEAT
def env(n,a,r):
    e=np.ones(n); a=int(a*SR); r=int(r*SR)
    if a: e[:a]=np.linspace(0,1,a)
    if r: e[-r:]*=np.linspace(1,0,r)
    return e
def add(sig,start):
    i=int(start*SR); j=min(N,i+len(sig))
    if i<N: out[i:j]+=sig[:j-i]
pad=np.zeros(N); 
nbars=int(np.ceil(DUR/BAR))
for b in range(nbars):
    ch=chords[b%4]; st=b*BAR; L=int((BAR+0.6)*SR); tt=np.arange(L)/SR
    s=np.zeros(L)
    for n in ch:
        for det in (-0.12,0.12):
            fr=f(n)*2**(det/12/10)
            for h,a in ((1,1),(2,.35),(3,.15),(4,.06)):
                s+=a*np.sin(2*np.pi*fr*h*tt+rng.random()*6)
    s*=env(L,0.5,0.8)*0.018
    i=int(st*SR); j=min(N,i+L); pad[i:j]+=s[:j-i]
out+=pad
def ks(freq,dur,damp=0.996):
    L=int(dur*SR); p=int(SR/freq); buf=rng.uniform(-1,1,p); y=np.zeros(L)
    for k in range(L):
        y[k]=buf[k%p]; buf[k%p]=damp*0.5*(buf[k%p]+buf[(k+1)%p])
    return y*env(L,0.002,0.05)
pl={}
for b in range(nbars):
    ch=chords[b%4]; seq=[ch[0]+12,ch[1]+12,ch[2]+12,ch[1]+12]*2
    for k,n in enumerate(seq):
        st=b*BAR+k*BEAT/2
        if st>=27.6: continue
        if n not in pl: pl[n]=ks(f(n),0.9)
        vel=0.10 if k%2==0 else 0.07
        add(pl[n]*vel,st)
# Bass
for b in range(nbars):
    st=b*BAR
    if st<1.2 or st>=27.6: continue
    L=int(BAR*SR); tt=np.arange(L)/SR
    s=(np.sin(2*np.pi*f(roots[b%4])*tt)+0.3*np.sin(4*np.pi*f(roots[b%4])*tt))*env(L,0.02,0.4)*0.07
    add(s,st)
# Kick + Shaker
kL=int(0.35*SR); kt=np.arange(kL)/SR
fr=45+75*np.exp(-kt*30); kick=np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-kt*9)*0.22
sL=int(0.08*SR); sh=rng.normal(0,1,sL); sh=np.diff(np.concatenate([[0],sh]))*np.exp(-np.arange(sL)/SR*45)*0.025
nb=int(DUR/BEAT)
for k in range(nb):
    st=k*BEAT
    if 1.2<=st<22.8 and k%2==0: add(kick,st)
    if 1.2<=st<22.8: add(sh,st+BEAT/2)
    if 3.0<=st<22.8: add(sh*0.5,st+BEAT/4); add(sh*0.5,st+3*BEAT/4)
# Fades
out*=np.clip(t/0.4,0,1)*np.clip((DUR-t)/2.5,0,1)
# einfacher Hall
d=int(0.11*SR); wet=np.zeros(N)
for g,dl in ((0.35,d),(0.22,int(d*1.7)),(0.12,int(d*2.9))):
    wet[dl:]+=out[:-dl]*g
mix=out+wet
mix=np.tanh(mix*1.4)/1.4
mix/=np.max(np.abs(mix))/0.6
st=np.stack([mix,np.roll(mix,int(0.012*SR))*0.98],1)
w=wave.open(sys.argv[1],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((st*32767).astype(np.int16).tobytes()); w.close()
