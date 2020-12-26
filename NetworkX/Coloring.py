# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 13:47:17 2020

@author: matis
"""

import networkx as nx

G=nx.complete_graph(6)
print (nx.coloring.greedy_color(G)) #greedy approach algorithm
#Los numeros del diccionario son los vértices
#Los números dentro de las llaves (vertices) del diccionario, son el color asignado
K=nx.gnm_random_graph(10,12)
print(nx.coloring.greedy_color(K))


