import random
import multiprocessing
import numpy as np
num_points = 1e8
p = 0

def evaluate_e7(q):
    p=0
    for i in range(int(1e7)):
        p0 = random.random()*2-1
        p1 = random.random()*2-1
        if p0**2+p1**2<=1:
            p+=1
    return p

if num_points<1e8:
    for i in range(int(num_points)):
        p0 = np.random.uniform(-1,1)
        p1 = np.random.uniform(-1,1)
        if p0**2+p1**2<=1:
            p+=1

    print("La estimación de pi es: ")
    pc = p/num_points
    print(4*pc)
else:
    np = int(num_points/1e7) #Convertimos a entero para evitar problemitas
    print(np)
    with multiprocessing.Pool() as pool:
        ps = pool.map(evaluate_e7,range(np))
    prom = sum(ps)
    print(4*prom/num_points)
