import numpy as np
import matplotlib.pyplot as plt

k=1

#Funcion lambda para el campo electrico
Fx = lambda x,y,px,py,q: k*q*(x-px)/np.power((x-px)**2+(y-py)**2,3/2)
Fy = lambda x,y,px,py,q: k*q*(y-py)/np.power((x-px)**2+(y-py)**2,3/2)
#Funcion lambda para calcular el potencial electrico
Phi = lambda x,y,px,py,q: k*q/np.power((x-px)**2+(y-py)**2,0.5)


#Limites de la graficacion
e_min = -10
e_max = 10

#Calculamos los puntos donde va a estar el campo vectorial
res = 20
x0 = np.linspace(e_min,e_max,res)
x1 = np.linspace(e_min,e_max,res)
X,Y = np.meshgrid(x0,x1) 


#Calculamos los puntos donde vamos a calcular el potencial
res_p = 100 #Deben ser mas para no perder resolución del campo escalar
x0p = np.linspace(e_min,e_max,res_p)
x1p = np.linspace(e_min,e_max,res_p)

Xp,Yp = np.meshgrid(x0p,x1p)

#Posición de las particulas
part_pos = np.array([
    [-5,0],
    [5,0]
])

#Carga de cada particula
q = [-1,1]

#Calculamos el campo electrico individual producido por cada particula
Ftx = [Fx(X,Y,part_pos[i,0],part_pos[i,1],q[i]) for i in range(len(part_pos))]
Fty = [Fy(X,Y,part_pos[i,0],part_pos[i,1],q[i]) for i in range(len(part_pos))]

#Calculamos el potencial individual producido por cada particula
Ftphi = [Phi(Xp,Yp,part_pos[i,0],part_pos[i,1],q[i]) for i in range(len(part_pos))]

#Creamos la lista del campo electrico total(inicialmente en 0)
sFtx = np.zeros_like(Ftx[0])
sFty = np.zeros_like(Ftx[0])
#Creamos la lista del potencial escalar(inicialmente en 0)
sFtphi = np.zeros_like(Ftphi[0])

#Sumamos las contribuciones de cada particula
for i in range(len(part_pos)):
    sFtx += Ftx[i]
    sFty += Fty[i]
    sFtphi += Ftphi[i]

#Calculamos la magnitud del campo electrico en cada punto para normalizar los vectores
norm = np.sqrt(sFtx**2+sFty**2)

#Normalizamos los vectores
sFtx = sFtx/norm
sFty = sFty/norm


plt.figure(figsize=(7,7))
plt.axis("off")
plt.pcolormesh(Xp,Yp,sFtphi,cmap="berlin") #Mostramos el potencial
plt.quiver(X,Y,sFtx,sFty,color="white") #Mostramos los vectores del campo electrico
plt.savefig("campo_electrico_5.png",dpi=300)
plt.show()