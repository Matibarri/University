# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 20:56:24 2020

@author: matibarri
"""

import docplex.mp #Cplex
from docplex.mp.model import Model

def kp():
  #Datos
  W = 100
  n = 5
  w = [10,20,30,40,40]
  v = [20,30,66,40,60]
  #Modelo
  modelo = Model("KP")
  x = modelo.binary_var_list(n, name="x")
  modelo.maximize(modelo.sum(v[i]*x[i] for i in range(0,n))) #F.O
  modelo.add(modelo.sum(w[i]*x[i] for i in range(0,n)) <= W ) #Restricción capacidad.
  
  print(modelo.export_to_string()) #Imprimir OPL de Cplex
  modelo.print_information() #Imprimir información

  solucion = modelo.solve(log_output=True) #Resolver
  solucion.display() #mostrar solucion

def main():
  kp()

if __name__ == "__main__":
  main()