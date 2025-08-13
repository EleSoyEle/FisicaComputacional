import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

#Funcion a integrar
funcs_and_dom = [
    [lambda x:1/(x-1)**3,-2,-1],
    [lambda x:1/np.sqrt(x+1),0,3],
    [lambda x:1/(1+x**2),1,np.sqrt(3)],
    [lambda x:np.sin(x)**2,0,np.pi],
]


def integrar_aleatorio(func,num_points,a,b,comparar=False):
    #En caso de que no busquemos grafica para comparar
    if not comparar:
        #Generamos los puntos aleatorios y evaluamos
        random_points = np.random.uniform(a,b,num_points)
        y = func(random_points)
        prom = np.mean(y) #Calculamos el promedio
        return prom*(b-a) #Multiplicamos por delta x
    #en caso de que si busquemos grafica para comparar
    else:
        s = 0 #Valor inicial de la suma
        hist = [] #Historial para la grafica
        for p in range(1,num_points+1):
            pa = np.random.uniform(a,b) #Generamos un punto aleatorio
            s += func(pa)
    
            prom = s/p*(b-a) #Calculamos el promedio y multiplicamos por delta x
            hist.append(prom) #Añadimos al array de calculos pasados para n puntos
        #Graficamos 
        sp = range(1,num_points+1)
        plt.grid()
        plt.plot(sp,hist)
        plt.plot(sp,np.ones_like(sp)*quad(f,a,b)[0]) #Quad es la integral con scipy
        plt.savefig("figura{}.png".format(num_points))
        plt.show()
        return prom

n=int(1e7)
for i,obj in enumerate(funcs_and_dom):
    func,a,b = obj[0],obj[1],obj[2]
    res = integrar_aleatorio(func,n,a,b,False)
    print("El valor de la integral {} es {}".format(i,res))