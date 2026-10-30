import sys; sys.path.insert(0,'.')
from load import load
import numpy as np
from scipy.interpolate import splprep,splev
from scipy.spatial import cKDTree
def data():
    P,N,F=load()
    R=np.load('R.npy'); pl=np.load('plane.npy'); c0=pl[3:]
    Q=(P-c0)@R.T
    C=np.array([-2.1,-2.12])
    x=Q[:,0]-C[0]; y=Q[:,1]-C[1]; w=Q[:,2]; r=np.hypot(x,y)
    sel=(r>38)&(w>-60.5)
    return r[sel],w[sel]
def medians(rr,ww):
    pts=[]
    for b in np.arange(-59.0,-10.0,1.0):
        k=(ww>=b)&(ww<b+1.0); pts.append((np.median(rr[k]),np.median(ww[k])))
    cen=np.array([40.5,-9.0])
    ang=np.arctan2(ww-cen[1],rr-cen[0]); rad=np.hypot(rr-cen[0],ww-cen[1])
    for a0 in np.radians(np.arange(-20,89,3.0)):
        k=(ang>=a0)&(ang<a0+np.radians(3))&(rad>5)
        if k.sum()>50: pts.append((np.median(rr[k]),np.median(ww[k])))
    pts=np.array(pts)
    wall=pts[pts[:,1]<-9.5]; wall=wall[np.argsort(wall[:,1])]
    sh=pts[(pts[:,1]>=-9.5)&(pts[:,0]>43)]; sh=sh[np.argsort(np.arctan2(sh[:,1]-cen[1],sh[:,0]-cen[0]))]
    seq=np.vstack([wall,sh]); keep=[0]
    for i in range(1,len(seq)):
        if seq[i,1]>seq[keep[-1],1]-0.05: keep.append(i)
    seq=seq[keep]
    return np.vstack([seq,[[43.5,0.0],[42.5,0.0]]])
if __name__=='__main__':
    rr,ww=data(); seq=medians(rr,ww)
    sub=np.c_[rr,ww][::7]; tr=None
    for sf in (0.0005,0.002,0.005,0.012):
        wts=np.ones(len(seq)); wts[-2:]=4
        tck,u=splprep([seq[:,0],seq[:,1]],w=wts,s=len(seq)*sf,k=3)
        uu=np.linspace(0,1,5000); S=np.array(splev(uu,tck)).T
        d,_=cKDTree(S).query(sub)
        dd=np.array(splev(uu,tck,der=1)).T
        print(f's/n={sf} ncoef {len(tck[1][0])} rms {np.sqrt((d**2).mean()):.3f} p95 {np.percentile(d,95):.3f} zmono {(np.diff(S[:,1])>-1e-6).all()} rmax {S[:,0].max():.3f} end {S[-1].round(2)} endtan {(dd[-1]/np.hypot(*dd[-1])).round(3)} starttan {(dd[0]/np.hypot(*dd[0])).round(3)}')
