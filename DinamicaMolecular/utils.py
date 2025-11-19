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
        self.history_Ep = []
    
        #Lo siguiente es para el potencial de Lennard-Jones
        self.sigma = sigma
        self.epsilon = epsilon


    #Nota al lector interesado: args_q es un diccionario importante
    #Contiene los datos acerca de las distancias y las fuerzas de cada par de particulas

    #Nota adicional: Usamos frozenset para que no haya orden en los indices
    def CalcForces(self,particles:np.typing.NDArray[np.float64],idx:int,args_q:Dict):
        ft = list()
        ac_pots = []
        for p_idx in range(self.N):
            if not idx == p_idx:
                try:
                    r = args_q[frozenset([p_idx,idx])][0]
                    fp = args_q[frozenset([p_idx,idx])][1]

                    ft = [fp*(particles[idx][i]-particles[p_idx][i])/r for i in range(self.dim)]
                except KeyError:
                    r = math.sqrt(sum([(particles[idx][i]-particles[p_idx][i])**2 for i in range(self.dim)]))
                    ac_pots.append(self.GetLennardJonesPotentialValue(r))
                    if not r < 1e-4:
                        sigma_s_r = self.sigma/r
                        fp = 4*self.epsilon/self.sigma*(12*(sigma_s_r)**13-6*sigma_s_r**6)

                        ft = [fp*(particles[idx][i]-particles[p_idx][i])/r for i in range(self.dim)]
                        args_q[frozenset([p_idx,idx])] = [r,fp]
        return ft,ac_pots
    def GetLennardJonesPotentialValue(self,r:float):
        if not r==0.0:
            return 4*self.epsilon*((self.sigma/r)**12-(self.sigma/r)**6)
        else:
            return 0.0
    #Nota al lector interesado: 
    #Esta funcion da un salto de dt en la simulacion, unico argumento necesario
    def SimulatorStep(self,dt:float):

        args_parts = {}
        forces_tat = self.history_forces[-1]
        new_positions = self.positions + self.vel*dt + 0.5*forces_tat*dt**2/self.mp

        #Hacemos el cambio de coordenadas en caso de salir de la caja
        #Si se va por un lado, sale por el otro
        new_positions[new_positions<self.min_g]=self.max_g-1 
        new_positions[new_positions>self.max_g]=self.min_g+1

        #Velocidad v(t+dt/2) necesaria para el algoritmo velocity-verlet
        vel_mid = self.vel+0.5*forces_tat*dt/self.mp
        forces_tat_next = []

        all_pots = []
        for i in range(self.N):            
            #Calculamos las nuevas fuerzas
            fc,pots = self.CalcForces(new_positions,i,args_parts)
            forces_t_next = np.array(fc)
            forces_tat_next.append(forces_t_next)
            all_pots = all_pots + pots
        forces_tat_next = np.array(forces_tat_next)
        new_vel = vel_mid+0.5*forces_tat_next*dt/self.mp

        
        #Añadimos a los arrays con toda la informacion
        self.history_forces.append(forces_tat_next)
        self.history_positions.append(new_positions)
        self.history_velocity.append(new_vel)
        self.history_Ep.append(sum(all_pots))

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
            all_pots = []
            for i in range(self.N):
                fc,pots = self.CalcForces(self.positions,i,args_init)
                all_forces.append(np.array(fc))
                all_pots = all_pots + pots
            self.history_forces.append(np.array(all_forces))
            self.history_Ep.append(sum(all_pots))
        else:
            print("Las fuerzas iniciales ya fueron calculadas")
    #Las funciones que siguen son solo para el post-iteracion
    def GetNormalizedForces(self):
        n_h = np.array(self.history_forces)
        return n_h/np.linalg.norm(n_h,axis=2,keepdims=True)
    #Velocidad normalizada por peticion de Rommel
    def GetNormalizedVelocity(self):
        n_hv = np.array(self.history_velocity)
        return n_hv/np.linalg.norm(n_hv,axis=2,keepdims=True)
    #Temperaturas en todo instante de tiempo
    def GetTotalTemperatures(self):
        va = np.array(self.history_velocity)
        va2 = np.sum([va[:,:,i]**2 for i in range(self.dim)],axis=0)
        vp =  np.mean(va2,axis=1)
        return self.mp*vp/(self.dim*self.kb)
    #Energia potencial a lo largo de los pasos
    def GetAllPotentialEnergy(self):
        p_e = np.array(self.history_Ep)
        return p_e
    #Energia cinetica a lo largo de los pasos
    def GetAllKineticEnergy(self):
        va = np.array(self.history_velocity)
        vp2i = np.sum(va**2,axis=2)
        vt = np.sum(vp2i,axis=1)
        Ek = 0.5*self.mp*vt
        return Ek
    def MakePovrayVideo(self,idx):
        povfile = "particles.pov"
        with open(povfile, "w") as f:
            f.write("#include \"colors.inc\" \n")
            f.write("camera {location <75,75,75> look_at <0,0,0> } \n ")
            f.write("light_source { <0,0,100> color White }\n\n ")

            for part_i in range(self.N):
                pos_part = self.history_positions[idx][part_i]
                str_a = f'sphere {{ <{pos_part[0]},{pos_part[1]},{pos_part[2]}>, 1 texture {{ pigment {{ color Blue }} }} }} \n'
                f.write(str_a)
            
    #Comentario: No se añadio una funcion que calcule la energia total por dos motivos
    # 1. Es constante
    # 2. Es redundante
    #Cuando se use este simulador, en caso de querer obtener la energia total, se recomienda
    #que al final de la ejecucion de la simulacion obtener la energia cinetica y potencial
    #las funciones dadas arriba, posteriormente sumar
    
#Funcion para calcular desbordes en los datos
def RemoveE(data):
    #Calcular Q1, Q3 y el IQR
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1
    
    #Definir los límites
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    
    #Identificar y reemplazar los desbordes por NaN
    outlier_mask = (data < limite_inferior) | (data > limite_superior)
    data[outlier_mask] = np.nan
    
    #Rellenar los valores NaN con la mediana de los datos normales restantes
    mediana_valida = np.nanmedian(data)
    data = np.nan_to_num(data, nan=mediana_valida)
    
    return data