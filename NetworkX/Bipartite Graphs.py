# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 13:54:26 2020

@author: matis
"""

import networkx as nx
from networkx.algorithms import bipartite

B=nx.Graph()
B.add_nodes_from([1,2,3,4,5],bipartite=0)
B.add_nodes_from(['a','b','c'],bipartite=1)
B.add_edges_from([(1,'a'),(1,'b'),(2,'c'),(2,'b'),(3,'c'),(4,'a'),(5,'b')])

#nx.draw(B,with_labels=True)

G=nx.path_graph(4)
print(bipartite.is_bipartite(G)) #Verifica si es grafo bipartito
X=set([1,3])
print(bipartite.is_bipartite_node_set(G,X))
print(X)
Y=set([1,2])
print(bipartite.is_bipartite_node_set(G,Y))
print(Y)

