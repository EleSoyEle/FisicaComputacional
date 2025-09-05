import random
import math

import numpy as np
import matplotlib.pyplot as plt

def MakeRandomNormalNumbers(mean,points):
    #Utilizamos arrays para almacenar los numeros generados
    z_0 = []
    z_1 = []
    for i in range(points):
        u1 = random.uniform(0,1)
        u2 = random.uniform(0,1)
        R = math.sqrt(-2*math.log(u1))
        z_0.append(R*math.cos(2*math.pi*u2)+mean)
        z_1.append(R*math.sin(2*math.pi*u2)+mean)
    return z_0 #,z_1


#Media
m = 0 
#Numero de puntos
points = 10000

#Numero de columnas
columns = int(np.sqrt(points))

random_numb = MakeRandomNormalNumbers(m,points)
plt.grid()
plt.hist(random_numb,columns,edgecolor="black")
plt.xlabel("Valor en el eje x")
plt.ylabel("Frecuencia")
plt.title("Histograma de los números generados")
plt.show()