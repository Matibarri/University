# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 17:31:31 2020

@author: matibarri
"""

from docplex.mp.model import Model
mdl=Model("modelo")

#Parámetros
n=9 #Cantidad de variables
DF=[1,0,1,0,1,0,0,1,1]
M=[1,1,1,1,1,1,0,1,0]
DL=[0,1,1,1,0,0,1,0,0]
Hab_balon=[2,3,2,4,4,4,3,4,3]
Disparo=[2,3,3,4,1,2,4,2,1]
Velocidad=[4,2,4,3,2,4,3,3,3]
Hab_defensivas=[2,2,3,1,4,2,1,3,4]

#Variables

x=mdl.binary_var_list(n,name="x")

#funcion objetivo

mdl.maximize(mdl.sum(Disparo[i]*x[i] for i in range(n)))

#Restricciones

mdl.add_constraint(mdl.sum(DF[i]*x[i] for i in range(n))>=3) #Defensa
mdl.add_constraint(mdl.sum(M[i]*x[i] for i in range(n))>=3) #Mediocampo
mdl.add_constraint(mdl.sum(DL[i]*x[i] for i in range(n))>=2) #Delantera
mdl.add_constraint(mdl.sum(Hab_balon[i]*x[i] for i in range(n))>=21) #Promedio Hab Balon
mdl.add_constraint(mdl.sum(Hab_defensivas[i]*x[i] for i in range(n))>=18) # Prom Hab Def
mdl.add_constraint(mdl.sum(Velocidad[i]*x[i] for i in range(n)) >=21) #Prom Vel
mdl.add_constraint(x[2]+x[4]<=1) #Juega uno o el otro
mdl.add_constraint(-x[0]+x[5]+x[6]>=1)
mdl.add_constraint(x[1]+x[3]==1)
mdl.add_constraint(mdl.sum(x[i] for i in range(n))==7)

print(mdl.export_to_string())

solucion=mdl.solve(log_output=True)

mdl.get_solve_status()

solucion.display()


