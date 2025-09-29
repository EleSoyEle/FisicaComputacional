import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

N = 20

#Tambien va a ayudarnos a delimitar el tamaño de la caja
min_g = -50
max_g = 50

v_p = 5
std = 0.5

parts = np.array([ np.random.uniform(min_g+1,max_g-1,2) for i in range(N)
],"float32")

v_parts = np.array([
    np.random.normal(v_p,std,2) for i in range(N)
],"float32")

q = [1 for i in range(N)]

#Acortar para no colapsar memoria
hist_p = [
    parts
]
hist_v = [
    v_parts
]
mp = 1
kb = 1

Temp = [mp*np.mean(v_parts)**2/(N*kb)]

#Parametros del potencial de Lennard-Jones
sigma = 1
epsilon = 1
def CalcF(pos0,pos,idx=None):
    fx = 0
    fy = 0
    for im,p in enumerate(pos):
        if not idx==im:
            r = ((pos0[0]-p[0])**2+(pos0[1]-p[1])**2)**(1/2)
            if not r==np.zeros_like(r):
                fp = 4*epsilon/sigma*(12*np.power(sigma/r,13)-6*np.power(sigma/r,6))

                fx = fp*(pos0[0]-p[0])/r
                fy = fp*(pos0[1]-p[1])/r
    return fx,fy

dt = 0.1

def MRU_step():
    new_state_v = []
    new_state_p = []
    for i in range(len(parts)):
        vn_part_i = np.copy(hist_v[-1][i])
        fx,fy = CalcF(hist_p[-1][i],hist_p[-1],i)

        pn_part_i = np.copy(hist_p[-1][i])
        pn_part_i[0] += vn_part_i[0]*dt + fx*dt**2/(2*mp)
        pn_part_i[1] += vn_part_i[1]*dt + fy*dt**2/(2*mp)

        fxn,fyn = CalcF(pn_part_i,hist_p[-1],i)

        vn_part_i[0] += (fxn+fx)*dt/(2*mp)
        vn_part_i[1] += (fyn+fy)*dt/(2*mp)


        if min_g > pn_part_i[0]:
            pn_part_i[0] = max_g-1
        if max_g < pn_part_i[0]:
            pn_part_i[0] = min_g+1
        if min_g > pn_part_i[1]:
            pn_part_i[1] = max_g-1
        if max_g < pn_part_i[1]:
            pn_part_i[1] = min_g+1
        
        new_state_v.append(vn_part_i)
        new_state_p.append(pn_part_i)

    #del hist_p[-1]
    #del hist_v[-1]
    hist_p.append(new_state_p)
    hist_v.append(new_state_v)
    Temp.append(mp*np.mean(new_state_v)**2/kb)


steps = 1000
for step in range(steps):
    MRU_step()


hist_p = np.array(hist_p)

fig = plt.figure()
ax = fig.add_subplot(111)

def animate(i):
    ax.clear()
    ax.plot([min_g,min_g,max_g,max_g,min_g],[min_g,max_g,max_g,min_g,min_g])
    ax.text(max_g-10,max_g,"T={}k".format(Temp[i]))
    
    ax.scatter(hist_p[i,:,0],hist_p[i,:,1],c="b")
    
ani = FuncAnimation(fig,animate,interval=0.1,frames=len(hist_p))
plt.show()
    