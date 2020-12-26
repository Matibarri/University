# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 13:21:16 2020

@author: matis
"""
import networkx as nx
G=nx.DiGraph()
G.add_node(5)
G.add_node(8)
G.add_node('IIT')
G.add_edge(5,'IIT')
G.add_edge(8,'IIT')
#nx.draw(G,with_labels=True)
l=[6,7,9]
G.add_nodes_from(l)
#print(G.nodes())
H=nx.bull_graph() #planar undirected graph with 5 vertices and 5 edges
#nx.draw(H, with_labels=True)
G.add_nodes_from(H.nodes())
G.add_edges_from(H.edges())
print(G.nodes(),G.edges())
nx.draw(G,with_labels=1)

