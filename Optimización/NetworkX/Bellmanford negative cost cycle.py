# -*- coding: utf-8 -*-
"""
Created on Fri May  8 16:30:40 2020

@author: matis
"""

import networkx as nx
import matplotlib.pyplot as plt

G=nx.DiGraph()

#Añadiendo vértices

G.add_node('1', pos=(2,1))
G.add_node('2', pos=(2,3))
G.add_node('3', pos=(0,4))
G.add_node('4', pos=(4,4))
G.add_node('5', pos=(1,5))
G.add_node('6', pos=(3,5))
G.add_node('7', pos=(2,6))

#Añadiendo artistas/arcos

G.add_edge('1','2', weight=2) 
G.add_edge('1','3', weight=4)
G.add_edge('2','3', weight=1)
G.add_edge('2','4', weight=1)
G.add_edge('3','5', weight=5)
G.add_edge('4','3', weight=-1)
G.add_edge('4','6', weight=-1)
G.add_edge('5','4', weight=-2)
G.add_edge('5','7', weight=1)
G.add_edge('6','5', weight=2)
G.add_edge('6','7', weight=3)

weight = nx.get_edge_attributes(G,'weight')
pos = nx.get_node_attributes(G,'pos')

nx.draw_networkx(G,pos)
nx.draw_networkx_edge_labels(G,pos, edge_labels=weight)

#Código para dibujar las aristas del árbol de cobertura mínimo

MST=set()
for i in G.nodes():
    camino = nx.bellman_ford_path(G, '1' , i)
    camino_aristas = zip(camino, camino[1:])
    for j in camino_aristas:    
        MST.add(j)
nx.draw_networkx_edges(G,pos,edgelist=MST,edge_color='r',width=5)
plt.axis('off')
plt.show()