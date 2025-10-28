from utils import Simulator,RemoveE
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import sys

print("En que dimension quieres visualizar todo?[2,3]")
dim = int(input(":"))
if dim != 3 and dim != 2:
    print("Dimension no valida, saliendo del programa")
    sys.exit()

print("Ingresa el numero de particulas")
N = int(input(":"))

print("Variables extra como masa,velocidad promedio, masa, etc... se van a tomar por defecto")

print("Ingresa el total de frames a calcular")
steps = int(input(":"))
print("Ingresa dt")
dt = float(input(":"))

print("-"*10)
print("\n"*2)
print("Iniciando calculo de simulacion...")
print("\n"*2)

#Parametros de la simulacion
v_mean = [0.0 for i in range(dim)]
std = 1
max_g = 50
min_g = -50

mp = 1
kb = 1
sigma = 1
epsilon = 1

#Creamos simulador
simulation = Simulator(N,dim,v_mean,std,min_g,max_g,sigma,epsilon,mp,kb)
simulation.InitSimul()

#Damos paso a la simulacion por unos cuantos frames
for step in range(steps):
    simulation.SimulatorStep(dt)

normalized_vel = simulation.GetNormalizedVelocity()
hist_p = np.array(simulation.history_positions)
temps = simulation.GetTotalTemperatures()

Ec = simulation.GetAllKineticEnergy()
Ep = simulation.GetAllPotentialEnergy()
Ec_cl = RemoveE(Ec)
Ep_cl = RemoveE(Ep[:-1])
Et = Ec_cl+Ep_cl


sp = range(steps)
plt.title("Energia a lo largo del tiempo")
plt.plot(sp,Ec_cl,label="Energia cinetica")
plt.plot(sp,Ep_cl,label="Energia potencial")
plt.plot(sp,np.ones_like(sp)*Et,label="Energia total")
plt.xlabel("Numero de pasos")
plt.ylabel("Energia(J)")
plt.legend()
plt.show()


if dim==3:
    #from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    def animate(i):
        ax.clear()
        ax.axis("off")
        ax.set_title("$T={}K$".format(round(temps[i],4)))
        ax.set_xlim(min_g,max_g)
        ax.set_ylim(min_g,max_g)
        ax.set_zlim(min_g,max_g)
        ax.quiver(
            hist_p[i,:,0],hist_p[i,:,1],hist_p[i,:,2],
            normalized_vel[i,:,0],normalized_vel[i,:,1],normalized_vel[i,:,2]
            ,color="black",alpha=0.5,length=5)
        ax.scatter(hist_p[i,:,0],hist_p[i,:,1],hist_p[i,:,2],c="blue")

    print("-"*50)
    print("Se va a guardar una animacion, escribe el nombre del archivo")
    
    filename = str(input(":"))
    while not filename.endswith(".mp4"):
        print("Nombre no valido, debe terminar con \".mp4\"")
        filename = str(input(":"))
    
    ani = FuncAnimation(fig,animate,steps,interval=0.1,blit=False)
    #ani.save(filename,writer='ffmpeg',fps=30,dpi=400)
    plt.show()
else:
    fig = plt.figure()
    ax = fig.add_subplot()

    def animate(i):
        ax.clear()
        ax.grid(True)
        ax.set_title("$T={}K$".format(round(temps[i],4)))
        ax.set_xlim(min_g,max_g)
        ax.set_ylim(min_g,max_g)
        ax.quiver(
            hist_p[i,:,0],hist_p[i,:,1],
            normalized_vel[i,:,0],normalized_vel[i,:,1]
            ,color="black",alpha=0.5)
        ax.scatter(hist_p[i,:,0],hist_p[i,:,1],c="blue")

    ani = FuncAnimation(fig,animate,steps,interval=0.1,blit=False)
    plt.show()
