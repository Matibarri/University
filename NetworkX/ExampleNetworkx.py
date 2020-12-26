# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 20:28:21 2020

@author: matis
"""

import networkx as nx
import matplotlib.pyplot as plt

G=nx.Graph()
G.add_node('u')
G.add_node('v')
G.add_node('w')
G.add_node('y')
G.add_node('z')
G.add_edge('u','v')
G.add_edge('u','z')
G.add_edge('v','w')
G.add_edge('v','y')
G.add_edge('w','y')
G.add_edge('w','z')

A=nx.adjacency_matrix(G)
print("Matriz de adyacencia")
print(A.todense())

print("Lista de adyacencia")
for n, nbrdict in G.adjacency():
    print(n + " " + str(nbrdict))

IM = abs(nx.incidence_matrix(G, oriented=True))
print("Matriz de incidencia")
print(IM.toarray())
nx.draw(G, with_labels=True)
plt.show()