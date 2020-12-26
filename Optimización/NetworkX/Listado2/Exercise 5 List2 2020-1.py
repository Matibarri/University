# -*- coding: utf-8 -*-
"""
Created on Tue May  5 15:43:34 2020

@author: matis
"""

import networkx as nx
import matplotlib.pyplot as plt

G=nx.DiGraph()

#Añadiendo vértices
G.add_node('C', pos=(4,4))
G.add_node('E', pos=(4,6))
G.add_node('B', pos=(0,4))
G.add_node('F', pos=(0,8))
G.add_node('D', pos=(0,6))
G.add_node('A', pos=(2,2))
G.add_node('H', pos=(4,8))
G.add_node('G', pos=(2,8))
G.add_node('I', pos=(2,10))

#print(G.nodes()) #Imprime los vértices que tiene el grafo

#Añadiendo artistas/arcos

G.add_edge('A', 'B', weight=5)
G.add_edge('A', 'C', weight=3)
G.add_edge('B', 'C', weight= -2)
G.add_edge('B','D', weight=3)
G.add_edge('C','D', weight=4)
G.add_edge('C','E', weight=2)
G.add_edge('C','G', weight=8)
G.add_edge('D','F', weight=3)
G.add_edge('D','G', weight= -6)
G.add_edge('E','G', weight= -1)
G.add_edge('E','H', weight=4)
G.add_edge('F','G', weight=4)
G.add_edge('H','G', weight=5)
G.add_edge('G','I', weight=3)
G.add_edge('F','I', weight=2)
G.add_edge('H','I', weight=4)
#print(G.edges()) #Imprime las aristas del grafo

#Si agregamos un arco donde uno de sus vértices
#no es parte del original, se crea dicho vértice.
weight = nx.get_edge_attributes(G,'weight')
pos = nx.get_node_attributes(G,'pos')
#print(G.nodes())
#print(G.edges())

nx.draw_networkx(G,pos)
nx.draw_networkx_edge_labels(G,pos, edge_labels=weight)

#Código para dibujar las aristas del árbol de cobertura mínimo

MST=set()
for i in G.nodes():
    camino = nx.bellman_ford_path(G, 'A', i)
    camino_aristas = zip(camino, camino[1:])
    for j in camino_aristas:    
        MST.add(j)
nx.draw_networkx_edges(G,pos,edgelist=MST,edge_color='r',width=5)
plt.axis('off')
plt.show()
    
    
    


    

        
       




