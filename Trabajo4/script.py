import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

#Funcion a integrar
funcs_and_dom = [
    [lambda x:1/(x-1)**3,-2,-1],
    [lambda x:1/np.sqrt(x+1),0,3],
    [lambda x:1/(1+x**2),1,np.sqrt(3)],
    [lambda x:np.sin(x)**2,0,np.pi],
    [lambda x:np.exp(-x**2/2)/np.sqrt(2*np.pi),3,10]
]

def random_normal(mean,std,pts=1000):
    random_samples_1 = np.random.uniform(0,1,pts)
    random_samples_2 = np.random.uniform(0,1,pts)
    R = np.sqrt(-2*np.log(random_samples_1))
    theta = 2*np.pi*random_samples_2
    z0 = R*np.cos(theta)
    z1 = R*np.sin(theta)
    return z1

def integrar_aleatorio(func,num_points,a,b,comparar=False,dist_mode=0):

    #En caso de que no busquemos grafica para comparar
    if not comparar:
        #Generamos los puntos aleatorios y evaluamos
        random_points = np.random.uniform(a,b,num_points) if dist_mode==0 else np.random.normal(5,1,num_points) if dist_mode == 1 else random_normal(0,1,num_points)
        random_points_d = np.array([rd if a<=rd<=b else 0 for rd in random_points])
        y = func(random_points_d)
        
        prom = np.mean(y) #Calculamos el promedio

        return prom*(b-a) #Multiplicamos por delta x
    #en caso de que si busquemos grafica para comparar
    else:
        s = 0 #Valor inicial de la suma
        hist = [] #Historial para la grafica
        for p in range(1,num_points+1):
            pa = np.random.uniform(a,b) if dist_mode==0 else np.random.normal(0,1) if dist_mode == 1 else random_normal(3,1)
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
    res = integrar_aleatorio(func,n,a,b,False,dist_mode=1)
    print("El valor de la integral {} es {}".format(i,res))