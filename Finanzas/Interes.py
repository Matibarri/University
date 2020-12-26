# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 11:02:34 2020

@author: matibarri
"""

import numpy as np
import matplotlib.pyplot as plt

def interes(cantidad, tasa, periodo, tiempo):
    pot = tiempo*periodo
    a = cantidad*pow((1+(tasa/100)/periodo), pot)
    return a

def plot_interes(n,cantidad, tasa, periodo, tiempo, time = 0):
    x = np.zeros(n)
    y = np.zeros(n)
    for i in range(n):
        time += 1
        x[i] = time
        y[i] = interes(cantidad, tasa, periodo, tiempo)
    plt.scatter(x,y, color = "red")
    plt.show()

# n = int(input("¿Cuántos años quieres calcular?"))

plot_interes(10, 17600, 4.5, 2,1)

