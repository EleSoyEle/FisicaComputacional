import numpy as np
import matplotlib.pyplot as plt
num_points = 1000
p = 0
points_x = []
points_y = []
p_est = []
for i in range(num_points):
        p0 = np.random.uniform(-1,1)
        p1 = np.random.uniform(-1,1)
        points_x.append(p0)
        points_y.append(p1)
        if p0**2+p1**2<=1:
            p+=1    
        pc = p/num_points
        npi = 4*pc
        p_est.append(npi)        
print("La estimación de pi es: ")
pc = p/num_points
npi = 4*pc
print(npi)
x0 = np.linspace(0,2*np.pi,100)
print("g={}".format(npi**2))

plt.scatter(points_x,points_y)
plt.plot(np.cos(x0),np.sin(x0))
plt.show()


esp = np.array(range(0,len(p_est)))

plt.plot(esp,p_est)
plt.plot(esp,np.ones_like(esp)*np.pi)
plt.show()