import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


L = 10 #longitud de la caja
n = 10 #Numero de particula

#Posición de cada particula
parts = np.random.uniform(-L,L,(n,3))

v_std = 0.5 #Desviacion estandar de la velocidad
v_parts = np.random.normal(0,v_std,(n,3)) #Velocidad de cada particula

hist_p = [
    parts.round(4)
]
v_cm = np.sum(v_parts,axis=0)/(n) #Calculamos la velocidad del centro de masa
vc = v_parts-v_cm #Restamos la velocidad para que la velocidad del centro de masa sea 0
hist_v = [
    vc.round(4) 
]

dt = 1 #Intervalo de tiempo
m=1 #Masa de las particulas
kb=1 #Constante de Boltzmann
hist_e = [
    np.mean(1/2*m*np.sum(v_parts**2,axis=-1)) #Calculamos la energia promedio
]
hist_T = [
    2/3*hist_e[0]/kb #Calculamos la temperatura promedio
]
correcciones_m = [
    [v_cm,np.sum(vc,axis=0)/(n)] #Añadimos las correcciones
]

def MRU_step():
    #Arrays con los estados nuevos
    new_state_v = []
    new_state_p = []
    for i in range(len(parts)):
        #Copiamos la informacion  del ultimo estado
        vn_part_i = np.copy(hist_v[-1][i])
        pn_part_i = np.copy(hist_p[-1][i])
        #Actualizamos con MRU
        pn_part_i[0] += vn_part_i[0]*dt
        pn_part_i[1] += vn_part_i[1]*dt
        pn_part_i[2] += vn_part_i[2]*dt

        #Verificamos condiciones de frontera
        pn_part_i[pn_part_i<-L]=L-1
        pn_part_i[pn_part_i>L]=-L+1

        new_state_v.append(vn_part_i.round(4))
        new_state_p.append(pn_part_i.round(4))

    hist_p.append(new_state_p)
    #Calculamos la velocidad del centro de masa
    v_cm = np.sum(new_state_v,axis=0)/(n)
    e1 = [v_cm]
    #Hacemos la correcion
    vc = new_state_v-v_cm
    e1.append(np.sum(vc,axis=0)/(n))
    correcciones_m.append(e1) #Añadimos la correcion calculada
    hist_v.append(vc)
    hist_e.append(np.mean(1/2*m*np.sum(np.array(vc)**2,axis=-1)))
    hist_T.append(2/3*hist_e[-1]/kb)


steps = 10
for step in range(steps):
    MRU_step()

#Redondeamos los decimales
hist_e = np.array(hist_e).round(4)
hist_T = np.array(hist_T).round(4)
correcciones_m = np.array(correcciones_m).round(7)

#Escribimos en cada archivo
with open("pos_vel.txt","w") as file,open("temp_e.txt","w") as pfile,open("correcciones.txt","w") as cfile:
    for i in range(len(hist_p)):
        text_line = "S:{}\n".format(i)
        for j in range(len(hist_p[i])):
            text_line += "P:{} \n".format(j)
            text_line += "{} {} {} , {} {} {} \n".format(hist_p[i][j][0],hist_p[i][j][1],hist_p[i][j][2],hist_v[i][j][0],hist_v[i][j][1],hist_v[i][j][2])
        file.write(text_line)
        print(text_line)
        pfile.write("Energia: {}, Temperatura {} \n".format(hist_e[i],hist_T[i]))
        cfile.write("Momento anterior: {} \nMomento nuevo: {} \n \n".format(correcciones_m[i][0],correcciones_m[i][1]))