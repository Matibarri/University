# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 12:25:20 2020

@author: matis
"""

import networkx as nx
import matplotlib.pyplot as plt

g=nx.read_edgelist('one.txt', create_using=nx.Graph(),nodetype=int)

print(nx.info(g))

nx.draw(g, with_labels=True)

plt.show()