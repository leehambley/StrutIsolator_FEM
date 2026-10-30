import sys; sys.path.insert(0,'.')
import numpy as np
from scipy.optimize import least_squares
from scipy.spatial import cKDTree
from bez import prep,bez
pts=prep()[::6]
ts=np.linspace(0,1,1500)
zb=-59.3
def run(n,re):
    # P0=(r0,zb), P1=(r0,z1) vertical tangent, interior free (n-3 pts), P(n-1)=(r_h,0), Pn=(re,0)
    k=n-3
    def build(p):
        r0,z1,rh=p[:3]; inter=p[3:3+2*k].reshape(k,2)
        return np.vstack([[r0,zb],[r0,z1],inter,[rh,0],[re,0]])
    def res(p):
        Pc=build(p); d,_=cKDTree(bez(Pc,ts)).query(pts); return d
    best=None
    for z1 in (-45,-35,-25):
        for rh in (46,50,54):
            ini=[54.85,z1,rh]
            for j in range(k): ini+=[53-3*j,-15+8*j]
            s=least_squares(res,ini,loss='soft_l1',f_scale=0.1,max_nfev=120)
            c=np.sqrt((res(s.x)**2).mean())
            if best is None or c<best[0]: best=(c,build(s.x),np.percentile(res(s.x),95))
    return best
for n,re in ((3,42.5),(4,42.5),(4,43.5)):
    c,Pc,p95=run(n,re)
    print('deg',n,'r_e',re,'rms',round(c,3),'p95',round(p95,3)); print(Pc.round(3)); sys.stdout.flush()
    np.save(f'bezc_{n}_{re}.npy',Pc)
