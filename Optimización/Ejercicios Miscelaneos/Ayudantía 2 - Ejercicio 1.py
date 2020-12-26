# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 09:47:34 2020

@author: matibarri
"""

from docplex.mp.model import Model

mdl=Model("modelo")

#Parámetros

origenes= [i for i in range(3)]
ruta=[j for j in range(2)]
destino= [k for k in range(2)]
costo_fijo=[[[10,12],[20,24]],[[15,16],[25,32]],[[30,18],[35,36]]]
C_F=[costo_fijo[i][j][k] for i in origenes for j in ruta for k in destino]
costo_unitario=[[[10,12],[2,8]],[[5,12],[4,10]],[[7,16],[6,14]]]
C_U=[costo_unitario[i][j][k] for i in origenes for j in ruta for k in destino]
demanda=[300,500]
oferta=[200,400,600]
M=99999

#lista de tuplas con los subíndices

or_ruta_des=[(i,j,k) for i in origenes for j in ruta for k in destino]

#Diccionarios

CF=dict(zip(or_ruta_des,C_F))
print('or_ruta_des',or_ruta_des)
print('C_F',C_F)
print('CF',CF)
CU=dict(zip(or_ruta_des, C_U))
print('CU',CU)
d=dict(zip(destino, demanda))
o=dict(zip(origenes, oferta))
print('oferta', o)
print('destino',d)
#Variables

x=mdl.integer_var_dict(or_ruta_des,name="x")
y=mdl.binary_var_dict(or_ruta_des, name="y")
print(x)

#F.O

mdl.minimize (mdl.sum(x[i]*CU[i] + CF[i]*y[i] for i in or_ruta_des))

#Restricciones

for i in origenes:
    mdl.add_constraint(mdl.sum(x[(i,j,k)] for j in ruta for k in destino)<= o[i])

for k in destino:
    mdl.add_constraint(mdl.sum(x[(i,j,k)] for j in ruta for i in origenes) == d[k])
    
for m in or_ruta_des:
    mdl.add_constraint(x[m] <= M*y[m])
    
#Solucion

print(mdl.export_to_string())
print(mdl.solve(log_output=True))
print(mdl.get_solve_status())
