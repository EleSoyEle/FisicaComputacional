import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

L = 100
n = 10

parts = np.random.uniform(-L,L,(n,3))

v_std = 10
v_parts = np.random.normal(0,v_std,(n,3))

#Acortar para no colapsar memoria
hist_p = [
    parts
]
hist_v = [
    v_parts
]


dt = 0.1

def MRU_step():
    new_state_v = []
    new_state_p = []
    for i in range(len(parts)):
        vn_part_i = np.copy(hist_v[-1][i])
        pn_part_i = np.copy(hist_p[-1][i])
        pn_part_i[0] += vn_part_i[0]*dt
        pn_part_i[1] += vn_part_i[1]*dt
        pn_part_i[2] += vn_part_i[2]*dt

        new_state_v.append(vn_part_i)
        new_state_p.append(pn_part_i)

    #del hist_p[-1]
    #del hist_v[-1]
    hist_p.append(new_state_p)
    hist_v.append(new_state_v)


steps = 10
for step in range(steps):
    #print(hist_p[-1],hist_v[-1])
    MRU_step()

with open("pos_vel.txt","w") as file:
    for i in range(len(hist_p)):
        text_line = "S:{} \n".format(i)
        for j in range(len(hist_p[i])):
            text_line += "P:{} \n".format(j)
            text_line += "{} {} {} , {} {} {} \n".format(hist_p[i][j][0],hist_p[i][j][1],hist_p[i][j][2],hist_v[i][j][0],hist_v[i][j][1],hist_v[i][j][2])
        file.write(text_line)
        print(text_line)
