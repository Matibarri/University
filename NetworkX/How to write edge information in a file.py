# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 22:42:59 2020

@author: matis
"""

import networkx as nx

g=nx.Graph()

g.add_edge(1,2)
g.add_edge(2,3)
g.add_edge(3,1)

nx.write_edgelist(g,'edgelist.txt') #Escribe arcos/aristas en un .txt