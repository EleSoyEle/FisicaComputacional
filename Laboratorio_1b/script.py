import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad


cmap = plt.cm.get_cmap("magma")

def integrar_aleatorio(func,num_points,a,b,mean,std):
    #Generamos los puntos aleatorios y evaluamos
    random_points = np.random.normal(mean,std,num_points)
    random_points_d = []
    for rd in random_points:
        if a<=rd<=b:
            random_points_d.append(rd)
    random_points_d = np.array(random_points_d)
    pdf = np.exp(-(random_points_d-mean)**2/(2*std**2))/np.sqrt(2*np.pi*std)
    y = func(random_points_d)
    prom = np.mean(y/pdf) #Calculamos el promedio

    integral_real = quad(func,a,b)   
    print('''
    
    Valor real: {}
    Valor estimado: {}

    '''.format(integral_real[0],prom)) 
    sp = np.linspace(a,b,1000)
    plt.title("Gráfica de la función")
    plt.xlabel("Eje x")
    plt.ylabel("Eje y")
    plt.grid()
    plt.plot(sp,func(sp),c="#AD1444",label="Función de integración")
    scale = 10/(abs(mean-random_points_d)+0.5)
    n_scale = scale/max(scale)
    colors = [cmap(n_scale[i]) for i in range(len(scale))]
    plt.scatter(random_points_d,-1*np.ones_like(random_points_d),s=scale,c=colors,label="Puntos aleatorios")
    plt.legend()
    plt.show()
    
    return prom

num_points = 1000
f = lambda x:10*np.exp(-5*(x-3)**4)
integrar_aleatorio(f,10000,-10,10,3,1)