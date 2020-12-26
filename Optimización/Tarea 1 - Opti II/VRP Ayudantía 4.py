# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 19:37:09 2020

@author: matibarri
"""
import sys
import numpy as np
from docplex.mp.model import Model
import docplex.mp.solution as Solucion
import matplotlib
import matplotlib.pyplot as plt



from docplex.mp.model import Model
from docplex.mp.conflict_refiner import ConflictRefiner

nCamiones = 8
n = 16
capacidad = 35
coord_x = [30, 37, 49, 52, 31, 52, 42, 52, 57, 62, 42, 27, 43, 58, 58, 37]
coord_y = [40, 52, 49, 64, 62, 33, 41, 41, 58, 42, 57, 68, 67, 48, 27, 69]
demanda = [0, 19, 30, 16, 23, 11, 31, 15, 28, 8, 8, 7, 14, 6, 19, 11]
print(" Cordenadas de X para todas las ciudades")

x = coord_x
y = coord_y
plt.figure(figsize=(12,5))
plt.scatter(x,y,color='blue')
s=[]
for n in range(len(coord_x)):
    s_temp=[]
    s_temp.append("%.1f" %coord_x[n])
    s_temp.append("%.1f" %coord_y[n])
    s.append(s_temp)

    plt.xlabel("Distancia X")
    plt.ylabel("Distancia Y")
    plt.title("Ubicacion de las ciudades - TSP")

    #for n in range(len(coord_x)): # imprimir coordenadas
    #    plt.annotate(str(s[n]), xy=(coord_x[n],coord_y[n] ), xytext=(coord_x[n]-4,coord_y[n]-4),
    #                 color='purple')

    for n in range(len(coord_x)):
        plt.annotate(str(n), xy=(coord_x[n],coord_y[n] ), xytext=(coord_x[n]+0.5,coord_y[n]+1), color='red')
plt.show()


n = len(coord_x)
ciudades = [i for i in range(n)]
arcos = [(i,j) for i in ciudades for j in ciudades if i != j]
distancia = {(i, j): round(np.hypot(coord_x[i] - coord_x[j], coord_y[i] - coord_y[j])) for i, j in arcos}
mdl = Model('VRP')
x = mdl.binary_var_dict(arcos, name = 'x')
#x = mdl.continuous_var_dict(arcos,name = 'x', lb = 0, ub = 1) # relajamos

mdl.minimize(mdl.sum(distancia[i] * x[i] for i in arcos))

for c in ciudades: # restricciones de salida
    if c > 0:
        mdl.add_constraint(mdl.sum(x[(i,j)] for i,j in arcos if i == c) == 1, ctname = 'salida_%d' % c)

for c in ciudades: # restricciones de entrada
    if c > 0:
        mdl.add_constraint(mdl.sum(x[(i,j)] for i,j in arcos if j == c) == 1, ctname = 'entrada_%d' % c)

mdl.add_constraint(mdl.sum(x[(i,j)] for i,j in arcos if i == 0) == nCamiones, ctname = 'inicio_vehiculos')
mdl.add_constraint(mdl.sum(x[(i,j)] for i,j in arcos if j == 0) == nCamiones, ctname = 'fin_vehiculos')
u = mdl.continuous_var_dict(ciudades, name = 'u')
for i, j in arcos:
    if i != 0:
        #mdl.add_constraint((u[i] - u[j]) >=  demanda[i] - capacidad * (1 - x[(i,j)]), ctname = 'mtz(%d,_%d)' % (i, j))
        mdl.add_constraint((u[i] - u[j]) +  demanda[i] <= capacidad * (1 - x[(i,j)]), ctname = 'mtz(%d,_%d)' % (i, j))
        #mdl.add_indicator_constraints(mdl.indicator_constraint(x[(i,j)], u[i] + demanda[j] == u[j]) for i,j in arcos if i != 0 and j != 0)

    # mdl.add_constraints(u[i] >= demanda[i] for i in ciudades)
    # mdl.add_constraints(u[i] <= capacidad for i in ciudades)
for i in ciudades:
    if i > 0:
        mdl.add_constraint(u[i] >= 1, ctname = 'mtz_lb__%d' % i)

for i in ciudades:
    if i > 0:
        print(capacidad, demanda[i])
        mdl.add_constraint(u[i] <= capacidad - demanda[i], ctname = 'mtz_ub_%d' % i)

solucion = mdl.solve(log_output=True)

mdl.get_solve_status()

solucion.display()

plt.figure(figsize=(12,6))
plt.xlabel("Distancia X")
plt.ylabel("Distancia Y")
plt.title("Solución para el VRP (costo %.3f)" % (solucion.get_objective_value()))

arcos_activos = [i for i in arcos if x[i].solution_value > 0.0001]
s=[]
for n in range(len(u)):
    s_temp=[]
    s_temp.append("%.1f" % u[n].solution_value)
    print(u[n].solution_value)
    s.append(s_temp)


for i,j in arcos_activos:
    plt.plot([coord_x[i],coord_x[j]],[coord_y[i],coord_y[j]], color='b', alpha=0.4, zorder=0)
    plt.scatter(x=coord_x, y=coord_y, color='blue', zorder=1)


        # for n in range(len(coord_x)):
        #     # plt.annotate(str(s[n]), xy=(coord_x[n],coord_y[n]), xytext=(coord_x[n]-4,coord_y[n]-4), color='purple')
        #     plt.annotate(str(n), xy=(coord_x[n],coord_y[n] ), xytext=(coord_x[n]+0.5,coord_y[n]+1), color='red')

for n in range(len(coord_x)):
    plt.annotate(str(n), xy=(coord_x[n],coord_y[n] ), xytext=(coord_x[n]+1,coord_y[n]+1), color='red')
   

plt.show()    