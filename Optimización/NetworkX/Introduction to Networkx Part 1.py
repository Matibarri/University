# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 12:50:53 2020

@author: matis
"""

import networkx as nx
import matplotlib.pyplot as plt

G=nx.Graph()

#Añadiendo vértices
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_node(5)

#print(G.nodes()) #Imprime los vértices que tiene el grafo

#Añadiendo artistas/arcos

G.add_edge(1,2)
G.add_edge(2,3)
G.add_edge(2,4)
G.add_edge(2,5)

#print(G.edges()) #Imprime las aristas del grafo

#Si agregamos un arco donde uno de sus vértices
#no es parte del original, se crea dicho vértice.

G.add_edge(2,6)

print(G.nodes())
print(G.edges())

nx.draw(G,with_labels=1,node_color='r')
