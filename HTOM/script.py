import numpy as np
import matplotlib.pyplot as plt
from scipy.special import sph_harm_y,assoc_laguerre

r_res = 100
th_res = 100
ph_res = 100
r = np.linspace(0,100,r_res)
phi = np.linspace(0,2*np.pi,ph_res,endpoint=False)
theta = np.linspace(0,np.pi,th_res)

R,Phi,Theta = np.meshgrid(r,phi,theta)
#Para estados de energia
n = 2
l = 1
m = -1
#Parametros del atomo
Z = 1
m_e = 1
hbar = 1
e = 1
e0 = 1


alpha = 2*Z/n

lag = assoc_laguerre(alpha*R,2*l+1,n-l-1 if n>1 else 0)
exp_t = np.exp(-alpha*R/2)


sph = sph_harm_y(l,m,Theta,Phi)
psi_nlm = sph*lag*exp_t*(alpha*R)**l


abs_psi = np.abs(psi_nlm)
psi_n = abs_psi/np.sum(abs_psi) #Normalización chafa, pero nos sirve, usted confie

max_psi = np.max(psi_n)


acc_points = []
num_points = 1000
gen_points = 0
while gen_points<num_points:
    i = np.random.randint(0,r_res)
    j = np.random.randint(0,ph_res)
    k = np.random.randint(0,th_res)

    rand_numb = np.random.uniform(0,max_psi)
    psi_ac = psi_n[i,j,k]
    if rand_numb<psi_ac:
        acc_points.append([i,j,k,psi_n[i,j,k]])
        gen_points += 1

x_p = []
y_p = []
z_p = []
al_p = []

for p in range(len(acc_points)):
    i,j,k,a = acc_points[p][0],acc_points[p][1],acc_points[p][2],acc_points[p][3]
    x_p.append(R[i,j,k]*np.cos(Theta[i,j,k])*np.sin(Phi[i,j,k]))
    y_p.append(R[i,j,k]*np.sin(Theta[i,j,k])*np.sin(Phi[i,j,k]))
    z_p.append(R[i,j,k]*np.cos(Phi[i,j,k]))
    al_p.append(a)

plt.style.use("dark_background")
fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot(111,projection="3d")


al_p = np.array(al_p)
al_p = al_p/np.max(al_p)

alpha_map = np.sqrt(al_p)
alpha_map = np.clip(alpha_map, 0.05, 1.0)

base_size = 0.5
size_map = base_size + 2 * al_p

ax.axis("off")
ax.scatter(x_p,y_p,z_p,alpha=alpha_map,s=size_map,c=al_p,cmap="inferno")
plt.show()
