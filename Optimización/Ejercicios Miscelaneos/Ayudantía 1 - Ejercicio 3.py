# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 20:23:03 2020

@author: matibarri
"""

from docplex.mp.model import Model

#Definición del modelo

mdl=Model("modelo")

#Definición de Parámetros

J=5
I=2
agentes=[i for i in range(I)]
tareas=[j for j in range(J)]
b=[[7,3,3,8,7],[5,3,8,4,1]]
bij=[b[i][j] for i in range(len(b)) for j in range(len(b[0]))]
c=[[8,2,8,9,1],[2,2,6,4,4]]
cij=[c[i][j] for i in range(len(c)) for j in range(len(c[0]))]
di=[11,7]

#Crear tuplas con agente_trabajo

ag_trab=[(i,j) for i in agentes for j in tareas]

#Diccionarios

Bij=dict(zip(ag_trab,bij))
Cij=dict(zip(ag_trab,cij))
Di=dict(zip(agentes,di))

#Variable

x=mdl.binary_var_dict(ag_trab,name="x")

#Función Objetivo

mdl.maximize(mdl.sum(x[i]*Bij[i] for i in ag_trab))

#Restricciones
for i in agentes:
    mdl.add_constraint(mdl.sum(x[(i,j)]*Cij[(i,j)] for j in tareas)<=Di[i])

for j in tareas:
    mdl.add_constraint(mdl.sum(x[(i,j)] for i in agentes)==1)
    
print(mdl.export_to_string())
solucion=mdl.solve(log_output=True)
solucion.display()