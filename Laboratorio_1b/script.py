import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad


cmap = plt.cm.get_cmap("magma")

def integrar_aleatorio(title,func,num_points,a,b,mean,std):
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

    
    {}
    ------------------------------
    Valor real: {}
    Valor estimado: {}
    ------------------------------
    '''.format(title,integral_real[0],prom)) 
    sp = np.linspace(a,b,1000)
    plt.title(title)
    plt.xlabel("Eje x")
    plt.ylabel("Eje y")
    plt.grid()
    plt.plot(sp,func(sp),c="#AD1444",label="Función de integración")
    scale = 10/(abs(mean-random_points_d)+0.5)
    n_scale = scale/max(scale)
    colors = [cmap(n_scale[i]) for i in range(len(scale))]
    plt.scatter(random_points_d,-1*np.ones_like(random_points_d),s=scale,c=colors,label="Puntos aleatorios")
    plt.legend()
    plt.savefig("{}.png".format(title))
    plt.show()
    
    return prom

num_points = 1000
funcs = [
    [lambda x:10*np.exp(-5*(x-3)**4),-20,20,3,1],
    [lambda x:1/np.sqrt(2*np.pi)*np.exp(-x**2/2),1,3,2,0.1],
    [lambda x:1/np.sqrt(2*np.pi)*np.exp(-x**2/2),3,20,2,1],
    [lambda x:np.exp(-(x-6)**2/2),-20,20,6,1]
]

for i,elem in enumerate(funcs):
    integrar_aleatorio("Integral {}".format(i+1),elem[0],num_points,elem[1],elem[2],elem[3],elem[4])
