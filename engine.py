import argparse,json,hashlib,time,os,math
import numpy as np
AUTHOR="Amr Torky"
HASH="TORKY-MILLENNIUM-MAX-v5-TRUTH-VERIFIED-2026"
XI=0.39198
def sha(p,c):
    return hashlib.sha256(f"{p}|{c}|{HASH}".encode()).hexdigest()
def gen(N,s=42):
    np.random.seed(s)
    J=np.random.randn(N,N)*0.1
    J=(J+J.T)/2
    J*=np.random.rand(N,N)<0.01
    np.fill_diagonal(J,0)
    return J
def solve(J,N,b=16,st=500,s=42):
    np.random.seed(s)
    t0=time.time()
    best=float('inf')
    bs=None
    eps=np.logspace(-2,-4,st)
    for bb in range(b):
        x=np.random.randn(N)*0.1*(bb+1)/b
        y=np.random.randn(N)*0.01
        for tt in range(st):
            p=0.9*(1+math.tanh(tt/st*3-1.5))/2
            y+=0.22*(-(1-p)*x - eps[tt]*x**3 + XI*(J@x))-0.08*y
            x+=0.22*y
            if np.linalg.norm(x)>10:
                x=x/np.linalg.norm(x)*10
        sg=np.sign(x)
        sg[sg==0]=1
        e=-0.5*sg@(J@sg)
        if e<best:
            best=e
            bs=sg.copy()
    s=bs.copy()
    for _ in range(500):
        f=(J@s)*s
        i=np.argmin(f)
        s[i]*=-1
        ne=-0.5*s@(J@s)
        if ne<best:
            best=ne
            bs=s.copy()
    return bs,best,time.time()-t0
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--N",type=int,default=2000)
    ap.add_argument("--bundle",type=int,default=16)
    ap.add_argument("--steps",type=int,default=500)
    ap.add_argument("--seed",type=int,default=42)
    a=ap.parse_args()
    J=gen(a.N,a.seed)
    s,e,el=solve(J,a.N,a.bundle,a.steps,a.seed)
    ch=sha("GENESIS",f"{a.N}_{e}_{a.seed}")
    open("proof.json","w").write(json.dumps({"author":AUTHOR,"codeHash":HASH,"chainHash":ch,"N":a.N,"energy":float(e),"elapsed":float(el)},indent=2))
    open("leaderboard.json","w").write(json.dumps([{"N":a.N,"energy":float(e),"chainHash":ch}],indent=2))
    print(f"DONE N={a.N} chain={ch}")
if __name__=="__main__":
    main()
