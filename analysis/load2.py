import numpy as np
def load(path='/mnt/user-data/uploads/1009_02_mesh.ply'):
    with open(path,'rb') as f: data=f.read()
    i=data.index(b'end_header\n')+11
    nv=2026571; nf=4039396
    V=np.frombuffer(data,dtype='<f4',count=nv*6,offset=i).reshape(nv,6)
    dt=np.dtype([('n','u1'),('a','<u4'),('b','<u4'),('c','<u4')])
    F=np.frombuffer(data,dtype=dt,count=nf,offset=i+nv*24)
    return V[:,:3].astype(float),V[:,3:].astype(float),np.stack([F['a'],F['b'],F['c']],1)
