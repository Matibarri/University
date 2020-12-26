# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 10:59:05 2020

@author: matibarri
"""

import sys
import numpy as np
from docplex.mp.model import Model
import docplex.mp.solution as Solucion
import matplotlib
import matplotlib.pyplot as plt

# coordenadas

coord_x = [4.17022005e+01, 7.20324493e+01, 1.14374817e-02, 3.02332573e+01, 1.46755891e+01, 9.23385948e+00]
coord_y = [18.6260214, 34.5560727, 39.67674742, 53.8816734, 41.91945144, 68.52195004]

# graficar

x=coord_x
y=coord_y
plt.figure(figsize=(12,5)) # tamaño de la figura
plt.scatter(x,y,color='blue') # color de los nodos
s=[]
for n in range(len(coord_x)): # lista de todos los valores de nuestras coordenadas
    s_temp=[]
    s_temp.append('%.1f' %coord_x[n])
    s_temp.append('%.1f' %coord_y[n])
    s.append(s_temp)
    
    plt.xlabel("Distancia X")
    plt.ylabel("Distancia Y")
    plt.title("Ubicación de las ciudades-TSP")
    
for m in range(len(coord_x)): # agregar el número del nodo para poder distinguirlos
    plt.annotate(str(m),xy=(coord_x[m], coord_y[m]), xytext=(coord_x[m]+0.5, coord_y[m] +0.5), color='red')
plt.show()

#Modelo matemático

n=len(coord_x)
ciudades = [i for i in range(n)]
arcos = [(i,j) for i in ciudades for j in ciudades if i != j] # no se puede ir de una ciudad a si misma
distancia = {(i,j): np.hypot(coord_x[i] - coord_x[j], coord_y[i] - coord_y[j]) for i,j in arcos }
mdl = Model('Problema del vendedor viajero')
#Definicion de variables
x = mdl.binary_var_dict(arcos, name = "x")
u = mdl.continuous_var_dict(ciudades, name = "u", lb = 1, ub = n) #lb y up son las cotas de u (restriccion (7) del MTZ)

mdl.minimize(mdl.sum(distancia[i]*x[i] for i in arcos))

for c in ciudades:
    mdl.add_constraint(mdl.sum(x[(i,j)] for i,j in arcos if i==c)==1, ctname="salida_%d" %c)
    
for c in ciudades:
    mdl.add_constraint(mdl.sum(x[(i,j)] for i,j in arcos if j==c)==1, ctname="entrada_%d" %c)

for i,j in arcos:
    if i!=0:
        mdl.add_constraint((u[i]-u[j]+1)-n*(1-x[(i,j)])<=0, ctname='mtz(%d_%d)' %(i,j))

print(mdl.export_to_string())
solucion = mdl.solve(log_output=True)
print(mdl.get_solve_status())
solucion.display()

# Gráfico solución

arcos_solucion = [i for i in arcos if x[i].solution_value>0.9]
plt.figure(figsize=(12,5))
plt.xlabel("Distancia X")
plt.ylabel("Distancia Y")
plt.title("Ubicación de las ciudades-TSP")
plt.scatter(x=coord_x, y=coord_y, color='blue', zorder =1)

for i,j in arcos_solucion:
    plt.plot([coord_x[i], coord_x[j]], [coord_y[i], coord_y[j]], color='purple', zorder=1)

plt.show()
