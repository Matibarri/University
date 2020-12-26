# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 10:32:28 2020

@author: 56939
"""

import numpy as np 
import matplotlib.pyplot as plt 

n=9 #más el depósito, 10.
ciudades=[ i for i in range(n)]
arcos=[(i,j) for i in ciudades for j in ciudades if i!=j]

profits=[0,1,6,3,1,2,4,7,2,3]
P=20

#rnd=np.random
#rnd.seed(0)
#coord_x=rnd.rand(n)*100
#coord_y=rnd.rand(n)*100
coord_x=[49,52,20,40,21,17,31,52,51]
coord_y=[49,64,26,30,47,63,62,33,21]

x=coord_x
y=coord_y
plt.figure(figsize=(12,6))
plt.scatter(x,y,color="blue")
plt.xlabel("Coord_x")
plt.ylabel("Coord_y")
plt.title("vecino mas cercano")

for i in range(len(x)):
    plt.annotate(str(i), xy=(x[i],y[i]),xytext=(x[i]-1,y[i]-1),color='red')
plt.show()
distancia = {(i,j): np.hypot(coord_x[i] - coord_x[j], coord_y[i] - coord_y[j]) for i, j in arcos}
beneficio = {(i,j): profits[i]+profits[j] for i,j in arcos}
print(beneficio) 

##Nearest Neighbor Heuristic

starting_node=0

NN=[starting_node]

while len(NN)<n:
    k=NN[-1] 
    #print(k)
    nn={(k,j): distancia[(k,j)]/beneficio[(k,j)] for j in ciudades if k!=j and j not in NN}
    print(nn)
    new=min(nn.items(), key=lambda x:x[1])
    print(new)
    l=new[0][1]
    NN.append(new[0][1])
    P=P-profits[l]
    print(P)
    if P<=0:
        break
NN.append(starting_node)

x=coord_x
y=coord_y
plt.figure(figsize=(12,6))
plt.scatter(x,y,color="blue")
for i in range(len(x)):
    plt.annotate(str(i), xy=(x[i],y[i]),xytext=(x[i]-1,y[i]-1),color='red')
for i in range(len(NN)-1):
    plt.plot([x[NN[i]],x[NN[i+1]]],[y[NN[i]],y[NN[i+1]]],color='purple')
plt.xlabel("Coord_x")
plt.ylabel("Coord_y")
plt.title("vecino mas cercano")

plt.show()
print(NN)
dist=0
for n in range(len(NN)-1):
    i=NN[n]
    j=NN[n+1]
    dist=dist+distancia[(i,j)]
print(dist)    

min_cambio=0
for i in range(len(NN)-2):
    for j in range(i+1,len(NN)-1):
        costo_actual=distancia[(NN[i],NN[i+1])]+distancia[(NN[j],NN[j+1])]
        costo_nuevo=distancia[(NN[i],NN[j])]+distancia[(NN[i+1],NN[j+1])]
        cambio=costo_nuevo-costo_actual
            
        if cambio <min_cambio:
            min_cambio=cambio
            min_i=i
            min_j=j
                
if min_cambio<0:
    NN[min_i+1:min_j+1]=NN[min_i+1:min_j+1][::-1]
     
sol=NN
print(sol)     

dist=0
for n in range(len(NN)-1):
    i=NN[n]
    j=NN[n+1]
    dist=dist+distancia[(i,j)]
print(dist) 

x=coord_x
y=coord_y
plt.figure(figsize=(12,6))
plt.scatter(x,y,color="blue")
for i in range(len(x)):
    plt.annotate(str(i), xy=(x[i],y[i]),xytext=(x[i]-1,y[i]-1),color='red')
for i in range(len(NN)-1):
    plt.plot([x[NN[i]],x[NN[i+1]]],[y[NN[i]],y[NN[i+1]]],color='purple')
plt.xlabel("Coord_x")
plt.ylabel("Coord_y")
plt.title("vecino mas cercano")
