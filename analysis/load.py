import numpy as np
def load(path='/mnt/user-data/uploads/1009_01_mesh.ply'):
    with open(path,'rb') as f:
        data=f.read()
    i=data.index(b'end_header\n')+11
    nv=992626; nf=1962279
    V=np.frombuffer(data,dtype='<f4',count=nv*6,offset=i).reshape(nv,6)
    off=i+nv*24
    dt=np.dtype([('n','u1'),('a','<u4'),('b','<u4'),('c','<u4')])
    F=np.frombuffer(data,dtype=dt,count=nf,offset=off)
    return V[:,:3].astype(float),V[:,3:].astype(float),np.stack([F['a'],F['b'],F['c']],1)
