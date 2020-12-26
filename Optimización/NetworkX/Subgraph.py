# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 14:07:08 2020

@author: matis
"""

import networkx as nx

K=nx.star_graph(5)
#nx.draw(K,with_labels=1)

nodes=[0,3,5]
K1=K.subgraph(nodes)
#nx.draw(K1,with_labels=1)

nodelist=[1,4,6,9]
K2=K.subgraph(nodelist)
#nx.draw(K2,with_labels=1) #graph disconnected

G=nx.ego_graph(K,1) #subgrafo usando el vertice 1
nx.draw(G,with_labels=1)