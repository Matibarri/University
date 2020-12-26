# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 08:02:56 2020

@author: matibarri
"""

from docplex.mp.model import Model

mdl=Model("modelo")

#Parámetros

productos=[j for j in range(3)]
plantas=[i for i in range(2)]
tiempo=[[3,4,2],[4,6,2]]
TIEMPO=[tiempo[i][j] for i in plantas for j in productos]
horas_disponibles=[30,40]
Ganancia_un=[[5,7,3], [5,7,3]]
GAN_UN=[Ganancia_un[i][j] for i in plantas for j in productos]
Ventas_p=[7,5,9]
M=99999

#Lista con los subíndices

prod_planta=[(i,j) for i in plantas for j in productos]

#Diccionarios

t=dict(zip(prod_planta,TIEMPO))
g=dict(zip(prod_planta, GAN_UN))
v=dict(zip(productos,Ventas_p))
h_d=dict(zip(plantas,horas_disponibles))

#Variables

x=mdl.integer_var_dict(prod_planta,name="x")
y=mdl.binary_var_dict(plantas, name="y")
z=mdl.binary_var_dict(productos, name="z")

#F.O

mdl.maximize(mdl.sum(x[i]*g[i] for i in prod_planta))

#Restricciones

for i in plantas:
    mdl.add_constraint(mdl.sum(x[(i,j)] for j in productos)<= M*y[i])
    mdl.add_constraint(mdl.sum(x[(i,j)]*t[(i,j)] for j in productos)<= h_d[i])
    
for j in productos:
    mdl.add_constraint(mdl.sum(x[(i,j)] for i in plantas)<= M*z[j])
    mdl.add_constraint(mdl.sum(x[(i,j)] for i in plantas)<= v[j])

mdl.add_constraint(mdl.sum(z[j] for j in productos)<= 2)
mdl.add_constraint(mdl.sum(y[i] for i in plantas) ==1)

#Solucion

print(mdl.export_to_string())
solucion=mdl.solve(log_output=True)
print(solucion)
print(mdl.get_solve_status())


