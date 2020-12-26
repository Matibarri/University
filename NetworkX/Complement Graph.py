# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 14:15:23 2020

@author: matis
"""

import networkx as nx

#Hacemos un ejemplo random.
G=nx.gnm_random_graph(15,10)
#nx.draw(G,with_labels=1)
GC=nx.complement(G)
#nx.draw(GC,with_labels=1)
# El complemento es lo opuesto al grafo. Lo conectado aparecerá desconectado y viceversa.

#Ejemplo de grafo completo.
H=nx.complete_graph(5)
HC=nx.complement(H)
#nx.draw(HC)

#Ejemplo cycle
K=nx.cycle_graph(5)
KC=nx.complement(K)
print(K.nodes()== KC.nodes())


