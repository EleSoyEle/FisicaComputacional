import numpy as np
import matplotlib.pyplot as plt



k=1

Fx = lambda x,y,px,py,q: q*(x-px)/np.power((x-px)**2+(y-py)**2,3/2)
Fy = lambda x,y,px,py,q: q*(y-py)/np.power((x-px)**2+(y-py)**2,3/2)



e_min = -10
e_max = 10
res = 20
x0 = np.linspace(e_min,e_max,res)
x1 = np.linspace(e_min,e_max,res)


X,Y = np.meshgrid(x0,x1)

part_pos = np.array([
    [-5,0],
    [5,0],
])

q = [1,-1]

Ftx = [Fx(X,Y,part_pos[i,0],part_pos[i,1],q[i]) for i in range(len(part_pos))]
Fty = [Fy(X,Y,part_pos[i,0],part_pos[i,1],q[i]) for i in range(len(part_pos))]

sFtx = np.zeros_like(Ftx[0])
sFty = np.zeros_like(Ftx[0])

for i in range(len(part_pos)):
    sFtx += Ftx[i]
    sFty += Fty[i]


norm = np.sqrt(sFtx**2+sFty**2)

sFtx = sFtx/norm
sFty = sFty/norm


#plt.axis("off")
plt.quiver(X,Y,sFtx,sFty)
plt.scatter(part_pos[:,0],part_pos[:,1])
plt.show()