#Nota al lector, muy importante leer

# E S T A B A    A B U R R I D O



#Nota menos importante
#Añadi un typing mas estricto en los argumentos en las funciones
#Mas velocidad, mas felicidad, quejas a diosito

import numpy as np
import math
from typing import List,Dict

#Clase que aloje la simulación en si misma
class Simulator():
    def __init__(self,
        N:int,dim:int,v_mean:list[float],std:float,min_g:float,max_g:float,
        sigma:float,
        epsilon:float,
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
        self.vel = np.array(
            [[np.random.normal(self.v_mean[i],self.std) for i in range(self.dim)] for i in range(self.N)])


        #Los siguientes arrays son solo para guardar la informacion de la simulacion
        self.history_positions = []
        self.history_velocity = []
        self.history_forces = []
        self.temperatures = []
    
        #Lo siguiente es para el potencial de Lennard-Jones
        self.sigma = sigma
        self.epsilon = epsilon


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
                        args_q[frozenset([p_idx,idx])] = [r,fp]
        return ft
    #Nota al lector interesado: 
    #Esta funcion da un salto de dt en la simulacion, unico argumento necesario
    def SimulatorStep(self,dt:float):

        args_parts = {}
        forces_tat = self.history_forces[-1]
        new_positions = self.positions + self.vel*dt + 0.5*forces_tat*dt**2/self.mp

        new_positions[new_positions<self.min_g]=self.max_g-1
        new_positions[new_positions>self.max_g]=self.min_g+1

        #Velocidad v(t+dt/2) necesaria para el algoritmo velocity verlet
        vel_mid = self.vel+0.5*forces_tat*dt/self.mp
        forces_tat_next = []

        for i in range(self.N):            
            #Calculamos las nuevas fuerzas
            forces_t_next = np.array(self.CalcForces(new_positions,i,args_parts))
            forces_tat_next.append(forces_t_next)
               
        forces_tat_next = np.array(forces_tat_next)
        new_vel = vel_mid+0.5*forces_tat_next*dt/self.mp


        #Añadimos a los arrays con toda la informacion
        self.history_forces.append(forces_tat_next)
        self.history_positions.append(new_positions)
        self.history_velocity.append(new_vel)

        #Actualizamos las variables
        self.positions = np.array(new_positions)
        self.vel = np.array(new_vel)

    #Funcion necesaria para iniciar todas las variables
    #Ya que el algoritmo de velocity verlet necesita un valor previo para las fuerzas
    #IMPORTANTE: LA SIMULACION NO VA A INICIAR SI NO SE EFECTUA ESTA FUNCION
    def InitSimul(self):
        if len(self.history_forces)==0:
            all_forces = []
            args_init = {}
            for i in range(self.N):
                all_forces.append(np.array(self.CalcForces(self.positions,i,args_init)))
            self.history_forces.append(np.array(all_forces))
        else:
            print("Las fuerzas iniciales ya fueron calculadas")
    #Las funciones que siguen son solo para el post-iteracion
    def GetNormalizedForces(self):
        n_h = np.array(self.history_forces)
        return n_h/np.linalg.norm(n_h,axis=2,keepdims=True)
    def GetNormalizedVelocity(self):
        n_hv = np.array(self.history_velocity)
        return n_hv/np.linalg.norm(n_hv,axis=2,keepdims=True)
    def GetTotalTemperatures(self):
        va = np.array(self.history_velocity)
        va2 = np.sum([va[:,:,i]**2 for i in range(self.dim)],axis=0)
        vp =  np.mean(va2,axis=1)
        return self.mp*vp/(self.dim*self.kb)
