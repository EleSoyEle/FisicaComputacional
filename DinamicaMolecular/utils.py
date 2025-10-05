#Nota al lector, muy importante a leer

# E S T A B A    A B U R R I D O



#Nota menos importante
#Añadi un typing mas estricto en los argumentos en las funciones
#Mas velocidad, mas felicidad, quejas a diosito

import numpy as np
import math
from typing import List,Dict

from script import CalcF

#Clase que aloje la simulación en si misma
class Simulator():
    def __init__(self,
        N:int,dim:int,v_mean:List[float],std:float,min_g:float,max_g:float,
        mp=1,
        kb=1):
        #Informacion de la simulacion
        self.N = N
        self.dim = dim
        self.v_mean = v_mean
        self.std = std
        self.mp = mp
        self.kb = kb
        self.min_g = min_g
        self.max_g = max_g

        #Creamos las posiciones y velocidades iniciales del sistema de particulas
        #En adelante estos arrays van a contener la ultima posición y velocidad calculada
        self.positions = np.random.uniform(self.min_g,self.max_g,size=(self.N,self.dim))
        self.vel = np.array([
            [np.random.normal([self.v_mean[i],self.std]) for i in range(self.dim)]
        ])


        #Los siguientes arrays son solo para guardar la informacion de la simulacion
        self.history_positions = []
        self.history_velocity = []
        self.history_forces = []
        self.temperature = []
    
        #Lo siguiente es para el potencial de Lennard-Jones
        self.sigma = 1
        self.epsilon = 1

    #Nota al lector interesado: args_q es un diccionario importante
    #Contiene los datos acerca de las distancias y las fuerzas de cada par de particulas

    #Nota adicional: Usamos frozenset para que no haya orden en los indices
    def CalcForces(self,particles:np.typing.NDArray[np.float64],idx:int,args_q:Dict):
        ft = list()
        for p_idx in range(self.N):
            if not idx == p_idx:
                try:
                    r = args_q[frozenset([p_idx,idx])][0]
                    fp = args_q[frozenset([p_idx,idx])][1]

                    ft = [fp*(particles[idx][i]-particles[p_idx][i])/r for i in range(self.dim)]
                except KeyError:
                    r = math.sqrt(sum([(particles[idx][i]-particles[p_idx][i])**2 for i in range(self.dim)]))
                    if not r == 0.0:
                        sigma_s_r = self.sigma/r
                        fp = 4*self.epsilon/self.sigma*(12*(sigma_s_r)**13-6*sigma_s_r**6)

                        ft = [fp*(particles[idx][i]-particles[p_idx][i])/r for i in range(self.dim)]
                        args_q[frozenset([p_idx,idx])] = [[r,fp]]
        return ft
    def SimulatorStep(self,dt):
        args_parts = {}
        
        all_positions = []
        all_vel = []
        all_forces = []

        for i in range(self.N):
            #Tomamos la fuerza calculada en el estado anterior
            forces_t = self.history_forces[-1][i]

            #Calculamos la nueva posicion            
            new_position = self.positions[i]+self.vel[i]*dt+0.5*forces_t*dt**2/self.mp

            #Calculamos la velocidad en el instante t+dt/2
            vel_mid = self.vel[i]+0.5*forces_t*dt/self.mp

            #Calculamos las nuevas fuerzas
            forces_t_next = np.array(self.CalcForces(new_position,i,args_parts))

            #Calculamos la velocidad en el instante t+dt
            new_vel =  vel_mid+0.5*forces_t_next*dt/self.mp

            #Añadimos lo calculado a sus respectivos arrays
            all_forces.append(forces_t_next)
            all_positions.append(new_position)
            all_vel.append(new_vel)

        #Añadimos a los arrays con toda la informacion
        self.history_forces.append(all_forces)
        self.history_positions.append(all_positions)
        self.history_velocity.append(all_vel)

    #Funcion necesaria para iniciar todas las variables
    def InitSimul(self):
        all_forces = []
        args_init = {}
        for i in range(self.N):
            all_forces.append(np.array(self.CalcForces(self.positions,i,args_init)))
