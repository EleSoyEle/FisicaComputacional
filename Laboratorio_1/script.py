import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
'''

--------------Promedio de la muestra-----------------

'''
def random_normal(mean,std,pts=1000):
    random_samples_1 = np.random.uniform(0,1,pts)
    random_samples_2 = np.random.uniform(0,1,pts)
    R = np.sqrt(-2*np.log(random_samples_1))
    theta = 2*np.pi*random_samples_2
    z0 = R*np.cos(theta)
    z1 = R*np.sin(theta)
    return z1


def PromedioDeLaMuestra(func,num_points,a,b,dist_mode=0):
    #En caso de que no busquemos grafica para comparar
    #Generamos los puntos aleatorios y evaluamos
    random_points = np.random.uniform(a,b,num_points) if dist_mode==0 else np.random.normal(5,1,num_points) if dist_mode == 1 else random_normal(0,1,num_points)
    random_points_d = np.array([rd if a<=rd<=b else 0 for rd in random_points])
    y = func(random_points_d)
    
    prom = np.mean(y) #Calculamos el promedio
    return prom*(b-a) #Multiplicamos por delta x



'''

Prueba y Error

'''

def encontrar_maximo(func,a,b,num_points=100):
    h = (b-a)/num_points
    m_points = []
    last_is_min = False
    min_points_array = []
    f = []
    x = []
    for i in range(num_points):
        ix = a + i*h
        fx = func(ix+h)
        df = (fx-func(ix))/h
        f.append(fx)
        x.append(ix)
        if abs(df)<0.001:
            #m_points.append((2*ix+h)/2)
            min_points_array.append((2*ix+h)/2)
            
            last_is_min = True
        else:
            if min_points_array != []:
                p = sum(min_points_array)/len(min_points_array)
                m_points.append(p)
                min_points_array = []
                last_is_min = False
    
    m_points.append(min(f))
    m_points.append(max(f))
    return m_points

def PruebaYError(func,a,b,num_points=1000):
    extremos = encontrar_maximo(func,a,b,1000)
    max_f = max(extremos)
    min_f = min(extremos)
    max_abs = max([abs(max_f),abs(min_f)])
    pi = 0
    for i in range(num_points):
        xp = np.random.uniform(a,b)
        
        fx = func(xp)
        yp = np.random.uniform(-max_abs,max_abs)
        if fx <= 0:
            if fx<=yp<=0:
                pi += 1
        else: 
            if 0<=yp<=fx:
                pi += 1
    prop = pi/num_points
    area = abs(b-a)*(2*max_abs)
    return area*prop



def comparar_metodos(title,func,a,b,pasos=[10,100,1000]):
    rm_1 = []
    rm_2 = []
    for i in range(len(pasos)):
        r1 = PromedioDeLaMuestra(func,pasos[i],a,b,0)
        r2 = PruebaYError(func,a,b,pasos[i])

        rm_1.append(r1)
        rm_2.append(r2)

    integral_real = quad(func,a,b)
    
    print('''
    
    ---------------{}-------------------
    Valor de la integral con scipy: {}
    Promedio de la muestra: {}
    Prueba y error: {}
    Numero de pasos maximo usado: {}
    '''.format(title,integral_real[0],rm_1[-1],rm_2[-1],pasos[-1]))

    print('''
    
    \\textbf{Numero de pasos}&\\textbf{Valor real}&\\textbf{Prueba y error}&\\textbf{Promedio de la muestra} \\\\ \\hline
    ''')
    for i in range(len(pasos)):
        print("{} & {} & {} & {} \\\\".format(pasos[i],round(integral_real[0],4),round(rm_2[i],4),round(rm_1[i],4)))

    sp = range(len(pasos))
    plt.grid()
    plt.title(title)
    plt.xticks(sp,pasos)
    plt.xlabel("Numero de pasos")
    plt.ylabel("Valor calculado")
    plt.text(1,integral_real[0],"I={}".format(round(integral_real[0],4)))
    plt.plot(np.ones_like(rm_1)*integral_real[0],label="Valor real")
    plt.plot(rm_1,label="Promedio de la muestra")
    plt.plot(rm_2,label="Prueba y Error")
    plt.legend()
    plt.savefig("{}.png".format(title))
    plt.show()


steps = [10,100,1000,10000,50000,100000]

funcs = [
    [lambda x:np.exp(-x**2),0,2],
    [lambda x:np.log(x**2+1),1,3],
    [lambda x:np.sin(x)/(x+1),0,np.pi],
    [lambda x:1/(1+x**4),0,1]
]

for i,l in enumerate(funcs):
    comparar_metodos("Integral {}".format(i+1),l[0],l[1],l[2],steps)
