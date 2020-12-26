# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 13:14:07 2020

@author: matis
"""

import networkx as nx
K=nx.complete_graph(10)
pos=nx.circular_layout(K)
nx.draw(K,pos,with_labels=True)
#nx.draw_spring(K,with_labels=True)