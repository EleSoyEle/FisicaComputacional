import numpy as np
import matplotlib.pyplot as plt
#Puntos a generar
num_points = 100
#Puntos dentro de la circunferencia
p = 0

#Arrays para graficar los resultados
points_x = []
points_y = []
p_est = [] #Guardamos cada estimación sucesiva de pi
colors = []
for i in range(num_points):
        #Generamos aleatoriamente dos numeros entre -1 y 1
        p0 = np.random.uniform(-1,1)
        p1 = np.random.uniform(-1,1)
        points_x.append(p0)
        points_y.append(p1)
        
        is_in = False
        #Comprobamos que esten dentro de la circunferencia
        if p0**2+p1**2<=1:
            p+=1    
            is_in = True
        pc = p/num_points
        npi = 4*pc
        p_est.append(npi) #Añadimos los puntos generados
        colors.append("red" if is_in else "blue") #Le asignamos un color


print("La estimación de pi es: ")
pc = p/num_points
npi = 4*pc
print(npi)
x0 = np.linspace(0,2*np.pi,100)

#Graficamos los puntos
plt.title("Gráfica de puntos generados")
plt.scatter(points_x,points_y,c=colors)
plt.plot(np.cos(x0),np.sin(x0))
plt.show()


esp = np.array(range(1,len(p_est)+1))
plt.title("Aproximación sucesiva de pi")
plt.grid()
plt.plot(esp,p_est,label="Pi")
plt.plot(esp,np.ones_like(esp)*np.pi,dashes=[6,2],label="Aproximación",)
plt.xlabel("Puntos generados")
plt.ylabel("Aproximación de pi")
plt.legend()
plt.show()