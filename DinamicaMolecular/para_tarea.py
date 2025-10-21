import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

L = 10
n = 10

parts = np.random.uniform(-L,L,(n,3))

v_std = 0.5
v_parts = np.random.normal(0,v_std,(n,3))

hist_p = [
    parts.round(4)
]
hist_v = [
    v_parts.round(4)
]
dt = 0.1
m=1
kb=1
hist_e = [
    np.mean(1/2*m*np.sum(v_parts**2,axis=-1))
]
hist_T = [
    2/3*hist_e[0]/kb
]
def MRU_step():
    new_state_v = []
    new_state_p = []
    for i in range(len(parts)):
        vn_part_i = np.copy(hist_v[-1][i])
        pn_part_i = np.copy(hist_p[-1][i])
        pn_part_i[0] += vn_part_i[0]*dt
        pn_part_i[1] += vn_part_i[1]*dt
        pn_part_i[2] += vn_part_i[2]*dt

        pn_part_i[pn_part_i<-L]=L-1
        pn_part_i[pn_part_i>L]=-L+1

        new_state_v.append(vn_part_i.round(4))
        new_state_p.append(pn_part_i.round(4))

    hist_p.append(new_state_p)
    hist_v.append(new_state_v)
    hist_e.append(np.mean(1/2*m*np.sum(np.array(new_state_v)**2,axis=-1)))
    hist_T.append(2/3*hist_e[-1]/kb)


steps = 10
for step in range(steps):
    MRU_step()

hist_e = np.array(hist_e).round(4)
hist_T = np.array(hist_T).round(4)

with open("pos_vel.txt","w") as file:
    for i in range(len(hist_p)):
        text_line = "S:{} T:{} Ecp: {} \n".format(i,hist_T[i],hist_e[i])
        for j in range(len(hist_p[i])):
            text_line += "P:{} \n".format(j)
            text_line += "{} {} {} , {} {} {} \n".format(hist_p[i][j][0],hist_p[i][j][1],hist_p[i][j][2],hist_v[i][j][0],hist_v[i][j][1],hist_v[i][j][2])
        file.write(text_line)
        print(text_line)
