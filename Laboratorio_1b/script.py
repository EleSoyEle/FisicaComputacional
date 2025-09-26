import numpy as np
import matplotlib.pyplot as plt

def integrar_aleatorio(func,num_points,a,b,mean,std):
    #Generamos los puntos aleatorios y evaluamos
    random_points = np.random.normal(mean,std,num_points)
    random_points_d = []
    for rd in random_points:
        if a<=rd<=b:
            random_points_d.append(rd)
        
    random_points_d = np.array(random_points_d)
    pdf = np.exp(-(random_points_d-mean)**2/(2*std**2))/np.sqrt(2*np.pi*std)
    y = func(random_points_d)/pdf
    prom = np.mean(y) #Calculamos el promedio
    return prom


f = lambda x:10*np.exp(-5*(x-3)**4)
print(integrar_aleatorio(f,100000,-100,100,3,1))
