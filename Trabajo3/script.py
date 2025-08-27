import numpy as np
import matplotlib.pyplot as plt
import scipy

legendre = scipy.special.legendre(4)
print(legendre(10))

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


#f = lambda x:1/(x-1)**3
#l = encontrar_maximo(f,-2,-1, num_points=1000)
#print(l)
#f = lambda x:x**3
#f = lambda x:x
#f = lambda x: 1/np.sqrt(1+x)
#f = lambda x: 1/(1+x**2)
f = lambda x: np.sin(x)**2

def integrar(func,a,b,num_points=1000):
    extremos = encontrar_maximo(f,a,b,1000)
    max_f = max(extremos)
    min_f = min(extremos)
    max_abs = max([abs(max_f),abs(min_f)])
    pi = 0
    for i in range(num_points):
        xp = np.random.uniform(a,b)
        
        fx = f(xp)
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
print(integrar(legendre,0,np.pi,10000))
