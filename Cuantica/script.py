import numpy as np
import matplotlib.pyplot as plt
from scipy.special import hermite
import math

res = 100
x = np.linspace(-1,1,res)
mw2 = 16.5
print("Graficando la funcion potencial")
plt.grid()
plt.xlabel("Posición x(m)")
plt.ylabel("Potencial V(J)")
plt.plot(x,mw2*x**2)
plt.show()

m = 1
w = 1

sqpi = math.sqrt(np.pi)

#Devuelve una funcion que corresponde al oscilador armonico
def HarmonicOscilatorObj(n):
    hermite_n = hermite(n)
    mterm = math.sqrt(1/(2**n*math.factorial(n)*sqpi))
    
    def f_a(eps):
        return hermite_n(eps)*np.exp(-eps**2/2)*mterm

    return f_a #Retornamos la funcion para que se pueda llamar


x = np.linspace(-5,5,5*res)
eps = np.sqrt(m*w)*x

harms = [HarmonicOscilatorObj(n) for n in range(0,5)]


min_r = 0
max_r = 4

plt.grid()
plt.title(r"Eigenfunciones $\psi_n(x)$")
plt.xlabel(r'Posición x(m)')
plt.ylabel(r'$\psi(x)$')
for i in range(min_r,max_r):
    psi_n = harms[i](eps)
    plt.plot(x,psi_n,label=r"$E_{}$".format(i))

plt.legend()
plt.savefig("figura_completa.png")
plt.show()



plt.grid()
plt.title(r"Densidad de probabilidad $\psi(x)$")
plt.xlabel(r'Posición x(m)')
plt.ylabel(r'$\psi^2(x) (m^{-1})$')
for i in range(min_r,max_r):
    psi_n = harms[i](eps)
    plt.plot(x,psi_n**2,label=r"$E_{}$".format(i))

plt.legend()
plt.savefig("figura_completa.png")
plt.show()


for i in range(min_r,max_r):
    psi_n = harms[i](eps)
    plt.grid()
    plt.title("Eigenfunción $\psi_{}(x)$".format(i))
    plt.plot(x,psi_n)
    plt.xlabel(r"Posición x(m)")
    plt.ylabel(r"$\psi(x)$")
    plt.show()

