import numpy as np
import matplotlib.pyplot as plt

k=1

#Campo electrico
Fx = lambda x,y,px,py,q: k*q*(x-px)/np.power((x-px)**2+(y-py)**2,3/2)
Fy = lambda x,y,px,py,q: k*q*(y-py)/np.power((x-px)**2+(y-py)**2,3/2)
#Potencial electrico
Phi = lambda x,y,px,py,q: k*q/np.power((x-px)**2+(y-py)**2,0.5)


#Limites de la graficacion
e_min = -10
e_max = 10

#Para el campo vectorial
res = 20
x0 = np.linspace(e_min,e_max,res)
x1 = np.linspace(e_min,e_max,res)
X,Y = np.meshgrid(x0,x1)


#Para mostrar el potencial electrico
res_p = 100
x0p = np.linspace(e_min,e_max,res_p)
x1p = np.linspace(e_min,e_max,res_p)

Xp,Yp = np.meshgrid(x0p,x1p)

#Posición de las particulas
part_pos = np.array([
    [-5,0],
    [5,0],
])

#Carga de cada particula
q = [1,-1]

#Calculamos el campo electrico individual
Ftx = [Fx(X,Y,part_pos[i,0],part_pos[i,1],q[i]) for i in range(len(part_pos))]
Fty = [Fy(X,Y,part_pos[i,0],part_pos[i,1],q[i]) for i in range(len(part_pos))]

#Calculamos el potencial individual
Ftphi = [Phi(Xp,Yp,part_pos[i,0],part_pos[i,1],q[i]) for i in range(len(part_pos))]

#Arrays en cero
sFtx = np.zeros_like(Ftx[0])
sFty = np.zeros_like(Ftx[0])
sFtphi = np.zeros_like(Ftphi[0])

#Sumamos cada potencial y campo electrico
for i in range(len(part_pos)):
    sFtx += Ftx[i]
    sFty += Fty[i]
    sFtphi += Ftphi[i]

#Calculamos la norma para normalizar los vectores
norm = np.sqrt(sFtx**2+sFty**2)

#Normalizamos los vectores
sFtx = sFtx/norm
sFty = sFty/norm


#plt.axis("off")
plt.pcolormesh(Xp,Yp,sFtphi) #Mostramos el potencial
plt.quiver(X,Y,sFtx,sFty,color="white") #Mostramos los vectores del campo electrico
plt.scatter(part_pos[:,0],part_pos[:,1],alpha=0.5) #Mostramos puntos donde hay particulas
plt.savefig("campo_electrico.png")
plt.show()