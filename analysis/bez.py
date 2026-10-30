import sys; sys.path.insert(0,'.')
from load import load
import numpy as np
from scipy.optimize import least_squares
from scipy.special import comb
def bern(n,t):
    t=np.asarray(t)[:,None]; i=np.arange(n+1)[None,:]
    return comb(n,i)*t**i*(1-t)**(n-i)
def bez(Pc,t): return bern(len(Pc)-1,t)@Pc
def prep():
    P,N,F=load()
    R=np.load('R.npy'); pl=np.load('plane.npy'); c0=pl[3:]
    Q=(P-c0)@R.T
    C=np.array([-2.1,-2.12])
    x=Q[:,0]-C[0]; y=Q[:,1]-C[1]; w=Q[:,2]; r=np.hypot(x,y)
    # profile points: wall + fillet + flat near rim
    m=(r>40)&(w>-60)
    # drop interior hole/lip points: r>40 so none
    rng=np.random.default_rng(5); idx=np.nonzero(m)[0]; idx=rng.choice(idx,40000,replace=False)
    return np.c_[r[idx],w[idx]]
def fit(pts,n,re_fixed=None):
    # control points: P0=(r0,zb) free r; Pn=(re,0) ; Pn-1=(re-h,0). others free. z of P0 fixed -59.3
    zb=-59.3
    ts=np.linspace(0,1,2001)
    def build(p):
        k=n-2   # free interior points P1..P(n-2)
        P0=np.array([p[0],zb]); re=p[1] if re_fixed is None else re_fixed; h=p[2]
        interior=p[3:3+2*k].reshape(k,2)
        return np.vstack([P0,interior,[re-h,0.0],[re,0.0]])
    def res(p):
        Pc=build(p); cur=bez(Pc,ts)
        from scipy.spatial import cKDTree
        d,_=cKDTree(cur).query(pts); 
        return d
    k=n-2
    # initial: from earlier piecewise profile
    ini=[54.83,42.5,6.0]
    xs=np.linspace(0,1,n+1)[1:-2]
    rr=np.interp(xs,[0,.2,.7,1],[54.83,54.8,48,42.5]); zz=np.interp(xs,[0,.2,.7,1],[-59.3,-43,-6,0])
    ini+=list(np.c_[rr,zz].ravel())
    s=least_squares(res,ini,loss='soft_l1',f_scale=0.1,max_nfev=300)
    r_=res(s.x)
    return build(s.x),np.sqrt((r_**2).mean()),np.percentile(r_,95)
if __name__=='__main__':
    pts=prep()
    for n in (4,5,6,7):
        Pc,rms,p95=fit(pts,n)
        print(n,'rms',round(rms,3),'p95',round(p95,3)); print(Pc.round(3))
        np.save(f'bez{n}.npy',Pc)
