# -*- coding: utf-8 -*-
"""
Created on Tue May  5 16:11:22 2020

@author: matis
"""

import os.path
import networkx as nx
from sys import argv
import matplotlib.pyplot as plt

G=nx.DiGraph()
#nodos
G.add_node('2', pos=(2,2))
G.add_node('1', pos=(0,4))
G.add_node('5', pos=(4,4))
G.add_node('3', pos=(2,4))
G.add_node('4', pos=(2,6))
G.add_node('6', pos=(4,6))
#edges
G.add_edge('1','2', weight=2)
G.add_edge('2','3', weight=5)
G.add_edge('2','5', weight=8)
G.add_edge('1','4', weight=3)
G.add_edge('4','3', weight=2)
G.add_edge('3','5', weight=3)
G.add_edge('4','6', weight=9)
G.add_edge('5','6', weight=1)
G.add_edge('1','3', weight=6)

weight = nx.get_edge_attributes(G,'weight')
pos = nx.get_node_attributes(G,'pos')

nx.draw_networkx(G,pos)
nx.draw_networkx_edge_labels(G,pos, edge_labels=weight)

#print (nx.dijkstra_path(G, '1', target=None))
#print (nx.average_shortest_path_length(G))
largo, camino = nx.single_source_dijkstra(G, '1', target=None)
print(largo)

MST=set()
for i in G.nodes():
    camino = nx.dijkstra_path(G, '1', i, weight='weight')
    camino_aristas = zip(camino, camino[1:])
    for j in camino_aristas:    
        MST.add(j)
nx.draw_networkx_edges(G,pos,edgelist=MST,edge_color='r',width=5)
plt.axis('off')
plt.show()
