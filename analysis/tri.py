import numpy as np
def geom(rho0,t,a):
    s=rho0+t
    disc=4*(a+t)**2-3*s*s
    if disc<0: return None
    d=(s+np.sqrt(disc))/2
    return d
def sector_curve(p,n=300):
    rho0,t,a=p[:3]
    d=geom(rho0,t,a)
    if d is None: return None
    s=rho0+t
    L=np.array([d*0.5,d*np.sqrt(3)/2]); T=np.array([s,0.])
    u=(L-T)/np.linalg.norm(L-T); Tp=T+u*t
    a1=np.arctan2(Tp[1]-T[1],Tp[0]-T[0])       # in (0,pi)
    ang=np.linspace(np.pi,a1,n)                # sweep from tip back around to tangent pt
    tooth=T[None,:]+t*np.c_[np.cos(ang),np.sin(ang)]
    b0=np.arctan2(Tp[1]-L[1],Tp[0]-L[0]); b1=np.radians(60)
    ang2=np.linspace(b0,b1,n)
    lobe=L[None,:]+a*np.c_[np.cos(ang2),np.sin(ang2)]
    return tooth,lobe,d,L,T,Tp
def full_curve(p):
    r=sector_curve(p)
    if r is None: return None
    sec=np.vstack([r[0],r[1]])
    pts=[]
    for k in range(3):
        for sgn in (1,-1):
            ang=np.radians(120*k+p[3]); c,s_=np.cos(ang),np.sin(ang)
            xs=sec[:,0]; ys=sgn*sec[:,1]
            pts.append(np.c_[c*xs-s_*ys, s_*xs+c*ys])
    return np.vstack(pts)
