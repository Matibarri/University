# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 20:11:51 2020

@author: matibarri
"""

import docplex.mp #Cplex
from docplex.mp.model import Model
#para graficar
import numpy as np
from matplotlib import pyplot as plt

def py_doccplex(tipo):
    modelo = Model('modelo') #nombre  del modelo
    
    if tipo == "PL":    # definiendo variables continuas
        x1 = modelo.continuous_var(name='x1')
        x2 = modelo.continuous_var(name='x2')
    else:
        x1 = modelo.integer_var(name='x1')
        x2 = modelo.integer_var(name='x2')
    
    modelo.maximize(6.0*x1 + 5.0*x2) #Función Objetivo
    modelo.add_constraint(x2 >= 0.0) #Rest. No negativo
    modelo.add_constraint(1.0*x1 + 1.3*x2 <= 8.0) #Rest. Espacio
    modelo.add_constraint(3.0*x1 + 2.0*x2 <= 20.0) #Rest. Materia Prima
    modelo.add_constraint(x1/3.0 + x2/4.0 <= 5.0) #Rest. Producción
    modelo.add_constraint(x1 >= 0.0) #Rest. No negativo
    
    print(modelo.export_to_string()) #imprimir OPL de Cplex
    modelo.print_information() # imprimir información
    solucion = modelo.solve(log_output = True) # resolver
    solucion.display() # mostrar solución
    
def plot(tipo): # Graficar con matplot
    x_size , y_size = 11 , 16
    fig, ax = plt.subplots(figsize = (8,8))
    x1 = np.linspace(0, max(x_size, y_size))
    # Graficando restricciones y sus regiones (sombras)
    plt.plot(x1, (8 - 1.0*x1)/1.3 , lw=3, label="Espacio") #Rest. Espacio
    plt.fill_between(x1,0, (8 - 1.0*x1)/1.3, alpha=0.1) #Región Rest. Espacio
    plt.plot(x1, (20 - 3.0*x1)/2.0 , lw=3, label="Materia Prima") #Rest. Materia Prima
    plt.fill_between(x1,0, (20 - 3.0*x1)/2.0, alpha=0.1) #Región Rest. Materia Prima
    plt.plot(x1, (30 - 3.0*x1)/2.0 , lw=3, label="Producción") #Rest. Producción
    plt.fill_between(x1,0, (30 - 3.0*x1)/2.0, alpha=0.1) #Región Rest. Producción
    plt.plot(np.zeros_like(x1), x1, lw=3, label="$x_1$ No Negatividad.") #Rest. No Neg. x1
    plt.plot( x1, np.zeros_like(x1), lw=3, label="$x_2$ No Negatividad.") #Rest. No Neg. x2
    # Graficar punto: PL o PLE
    plt.plot(5.263, 2.105, "g*") if tipo =="PL" else plt.plot(6,1,"ro") #Formato ternario del if: True CONDITION False
    # Etiquetas de los ejes
    plt.xlabel("producto 1 ($x_1$)", fontsize = 16)
    plt.ylabel("producto 2 ($x_2$)", fontsize = 16)
    #Límite de los ejes
    plt.xlim(-0.05, x_size) #Para q se vean las restricciones de no neg (-0.05)
    plt.ylim(-0.03, y_size) #Para q se vean las restricciones de no neg (-0.03)
    # Salto de los números de los ejes (de uno en uno)
    x_ticks = np.arange(0, x_size, 1)
    plt.xticks(x_ticks)
    y_ticks = np.arange(0, y_size, 1)
    plt.yticks(y_ticks)
    plt.grid(True) #rejilla
    plt.legend(fontsize=12) #tamaño fuente de las leyendas
    plt.show()

def main():
    tipo = "PL"
    py_doccplex(tipo)
    plot(tipo)
    
if __name__ == "__main__":
    main()