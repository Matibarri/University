# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 12:50:53 2020

@author: matis
"""

import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import tree

G=nx.Graph()

#Añadiendo vértices
G.add_node('A', pos=(4,4))
G.add_node('B', pos=(2,4))
G.add_node('C', pos=(0,4))
G.add_node('D', pos=(3,6))
G.add_node('E', pos=(1,6))
G.add_node('O', pos=(2,2))
G.add_node('T', pos=(2,8))

#print(G.nodes()) #Imprime los vértices que tiene el grafo

#Añadiendo artistas/arcos

G.add_edge('A', 'B', weight=2)
G.add_edge('A', 'D', weight=7)
G.add_edge('A', 'O', weight=2)
G.add_edge('B', 'C', weight=1)
G.add_edge('B', 'O', weight=5)
G.add_edge('B', 'D', weight=4)
G.add_edge('B', 'E', weight=3)
G.add_edge('C', 'O', weight=4)
G.add_edge('C', 'E', weight=4)
G.add_edge('D', 'E', weight=1)
G.add_edge('D', 'T', weight=5)
G.add_edge('E', 'T', weight=7)
#print(G.edges()) #Imprime las aristas del grafo

#Si agregamos un arco donde uno de sus vértices
#no es parte del original, se crea dicho vértice.
weight = nx.get_edge_attributes(G,'weight')
pos = nx.get_node_attributes(G,'pos')
#print(G.nodes())
#print(G.edges())

nx.draw_networkx(G,pos)
nx.draw_networkx_edge_labels(G,pos, edge_labels=weight)


T=nx.minimum_spanning_tree(G)
mst = tree.minimum_spanning_edges(G, algorithm='prim', data=False)
edgelist = list(mst)
print(edgelist)
nx.draw(T,pos, edge_color='r') #dibuja el árbol de cobertura mínima en el grafo
plt.axis('off')
plt.show()


    

        

    
