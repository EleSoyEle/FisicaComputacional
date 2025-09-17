import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


parts = np.array([
    [10,0],
    [0,0],
],"float32")

v_parts = np.array([
    [0,1],
    [0,0],
],"float32")

q = [1,-1]

#Acortar para no colapsar memoria
hist_p = [
    parts
]
hist_v = [
    v_parts
]

def CalcF(pos0,pos,idx=None):
    fx = 0
    fy = 0
    qp = 1
    if idx==None:
        qp=1
    else:
        qp = q[idx]
    for im,p in enumerate(pos):
        if not (p[0]==pos0[0] and p[1]==pos0[1]):
            res = ((pos0[0]-p[0])**2+(pos0[1]-p[1])**2)**(3/2)
            fx += 10*qp*q[im]*(pos0[0]-p[0])/res
            fy += 10*qp*q[im]*(pos0[1]-p[1])/res
    return fx,fy

dt = 0.1

def MRU_step():
    new_state_v = []
    new_state_p = []
    for i in range(len(parts)):
        vn_part_i = np.copy(hist_v[-1][i])
        fx,fy = CalcF(hist_p[-1][i],hist_p[-1],i)
        vn_part_i[0] = hist_v[-1][i][0]+fx*dt
        vn_part_i[1] = hist_v[-1][i][1]+fy*dt

        pn_part_i = np.copy(hist_p[-1][i])
        pn_part_i[0] += vn_part_i[0]*dt
        pn_part_i[1] += vn_part_i[1]*dt

        new_state_v.append(vn_part_i)
        new_state_p.append(pn_part_i)

    #del hist_p[-1]
    #del hist_v[-1]
    hist_p.append(new_state_p)
    hist_v.append(new_state_v)


steps = 1000
for step in range(steps):
    print(hist_p[-1],hist_v[-1])
    MRU_step()


fig = plt.figure()
ax = fig.add_subplot(111)

def animate(i):
    ax.clear()
    ax.scatter([-10,-10,10,10],[10,-10,10,-10])
    for p in range(len(parts)):
        ax.scatter(hist_p[i][p][0],hist_p[i][p][1])
    

ani = FuncAnimation(fig,animate,interval=0.1,frames=len(hist_p))
plt.show()
    