from utils import Simulator,RemoveE
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import subprocess

#Povray solo va a generar en 3d
dim=3

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
std = 0.5
max_g = 20
min_g = -20

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

#Generamos las imagenes con povray
for i in range(steps):
    simulation.MakePovrayVideo(i)
    command = [
        "povray","+Iparticles.pov","+Orenders/output{}.png".format(i)
    ]
    subprocess.run(command,check=True,capture_output=True,text=True)


#Creamos el gif
command = [
    "ffmpeg","-i","renders/output%d.png","outa.gif"
]
subprocess.run(command,check=True,capture_output=True,text=True)