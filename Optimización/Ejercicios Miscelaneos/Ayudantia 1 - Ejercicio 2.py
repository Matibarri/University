# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 17:08:30 2020

@author: matibarri
"""

#Importar docplex
#Definir el modelo
#Definen parametros (si es que hay)
#Definen variables
#Definición de la función objetivo
#Definir las restricciones

from docplex.mp.model import Model
mdl=Model("Modelo")

#Definicion de parametros (en este caso no es necesario)
#Definir variables

x1=mdl.binary_var(name="x1")
x2=mdl.binary_var(name="x2")
x3=mdl.binary_var(name="x3")
x4=mdl.binary_var(name="x4")
x5=mdl.binary_var(name="x5")
x6=mdl.binary_var(name="x6")
x7=mdl.binary_var(name="x7")
x8=mdl.binary_var(name="x8")
x9=mdl.binary_var(name="x9")

#Definir función objetivo

mdl.maximize(2*x1+3*x2+3*x3+4*x4+x5+2*x6+4*x7+2*x8+x9)

#Restricciones

mdl.add_constraint(x1+x2+x5+x8+x9>=3) #Defensa
mdl.add_constraint(x1+x2+x3+x4+x5+x6+x8>=3) #Mediocampo
mdl.add_constraint(x2+x3+x4+x7>=2) #Delantera
mdl.add_constraint(2*x1+3*x2+2*x3+4*x4+4*x5+4*x6+3*x7+4*x8+3*x9>=21) #
mdl.add_constraint(4*x1+2*x2+4*x3+3*x4+2*x5+4*x6+3*x7+3*x8+3*x9>=21) #
mdl.add_constraint(2*x1+2*x2+3*x3+x4+4*x5+2*x6+x7+3*x8+4*x9>=18) #
mdl.add_constraint(4*x1+2*x2+4*x3+3*x4+2*x5+4*x6+3*x7+3*x8+3*x9>=21) #
mdl.add_constraint(x3+x5<=1) #Juega uno o el otro
mdl.add_constraint(-x1+x6+x7>=1)
mdl.add_constraint(x2+x4==1)
mdl.add_(x1+x2+x3+x4+x5+x6+x7+x8+x9==7)

print(mdl.export_to_string("Modelo")) #Imprime el modelo, sirve para revisar

solucion=mdl.solve(log_output=True)

mdl.get_solve_status()

solucion.display()
