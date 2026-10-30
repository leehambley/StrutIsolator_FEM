import json,numpy as np,matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PIL import Image
import io,sys
d=json.load(open("/mnt/user-data/uploads/StrutIsolator_FEM/fem_surface.json"))
P=np.array(d["pts"]);T0=np.array(d["tris"]);T=T0[P[T0][:,:,1].mean(1)<0.5]
EXAG=8.0
def render(case,title,force,fn):
    D=np.array(d[case]["d"]);V=np.array(d[case]["vm"]);vmax=np.percentile(V,97)
    cm=plt.get_cmap("turbo");frames=[]
    ts=list(np.linspace(0,1,14))+list(np.linspace(1,0,14))[1:-1]
    for t in ts:
        X=P+D*EXAG*t
        tri=X[T];n=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);n/= (np.linalg.norm(n,axis=1,keepdims=True)+1e-12)
        light=np.array([0.4,-0.5,0.8]);light/=np.linalg.norm(light)
        sh=0.55+0.45*np.abs(n@light)
        c=cm(np.clip(V[T].mean(1)*t/vmax,0,1))[:,:3]*sh[:,None]
        fig=plt.figure(figsize=(6.4,5.2),dpi=100);ax=fig.add_subplot(111,projection="3d")
        pc=Poly3DCollection(tri,facecolors=c,edgecolors="none");ax.add_collection3d(pc)
        ax.set_xlim(-45,45);ax.set_ylim(-45,45);ax.set_zlim(-62,-2);ax.set_box_aspect((1,1,.67));ax.set_position([-0.15,-0.1,1.3,1.2])
        ax.view_init(elev=32,azim=75);ax.set_axis_off()
        fig.suptitle(title,fontsize=11,y=0.97)
        fig.text(0.5,0.05,"housing travel %.1f mm (shown x%d)  |  force %.0f N  |  colour = stress (blue low, red high)"%(t,EXAG,force*t),ha="center",fontsize=8.5)
        b=io.BytesIO();fig.savefig(b,format="png");plt.close(fig);b.seek(0)
        frames.append(Image.open(b).convert("P",palette=Image.ADAPTIVE))
    frames[0].save(fn,save_all=True,append_images=frames[1:],duration=90,loop=0)
render("axial","Original rubber (cut in half): housing pushed straight up (axial)",592,"gif/axial.gif")
render("radial","Original rubber (cut in half): housing pushed sideways (radial)",840,"gif/radial.gif")
