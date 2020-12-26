# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 14:36:04 2020

@author: matis
"""

import networkx as nx

G1=nx.Graph()

G1.add_nodes_from(['KA','TN','TL','KL','GO'])
G1.add_edges_from([('KA','TN'),('KA','AP'),('KA','TL'),('KA','KL'),('KA','GO')])
#nx.draw(G1,with_labels=1)

G2=nx.star_graph(5)
#nx.draw(G2,with_labels=True)
print(nx.is_isomorphic(G1,G2))