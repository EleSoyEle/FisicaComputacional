import numpy as np

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
        f.append(f)
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
    if m_points:
        m_points.append(min(f))
        m_points.append(max(f))
    return m_points


f = lambda x:1/(x-1)**3
l = encontrar_maximo(f,-5,-1, num_points=1000)
print(l)