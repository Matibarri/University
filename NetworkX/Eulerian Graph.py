# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 14:42:56 2020

@author: matis
"""

import networkx as nx
G=nx.complete_graph(5)
#print(nx.is_eulerian(G))
L=list(nx.eulerian_circuit(G))
print(L)
nx.draw(G,with_labels=True)