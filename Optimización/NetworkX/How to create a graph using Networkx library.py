# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 20:46:17 2020

@author: matis
"""

import networkx as nx
import matplotlib.pyplot as plt

g=nx.Graph() #Grafo vacío

g.add_node(2) #Agrega vértice/nodo
g.add_node(5)

g.add_edge(2,5) #Agrega arista/arco
g.add_edge(4,1)

g.add_edges_from([(2,5),(1,3)])

print(nx.info(g))

nx.draw(g, with_labels=True) #Dibuja el Grafo con matplotlib

plt.show() #Muestra el Grafo dibujado
