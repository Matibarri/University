#!/usr/bin/env python
# coding: utf-8

# In[195]:


#importamos bibliotecas 
import numpy as np 
import matplotlib.pyplot as plt


# In[196]:


#pruebe instancias 3 , 6 ,13 , 16 y 26 
archivo=open("13.txt","r")
l=archivo.readlines()
archivo.close()
info=[i.split() for i in l]
for j in range(len(info)):
    for z in range(len(info[j])):
        info[j][z]=int(float(info[j][z]))


# In[197]:


#deposito
V=int(info[0][0])
I=int(info[1][0])
C=int(info[2][0])
P=int(info[3][0])
instaydep=I+1

#listas vacias donde guardaremos nuestros valores
sdl=[]
instalaciones=[]
clientes=[]
instalaciones_clientes=[]

for i in range(len(info)):
    if info.index(info[0])==len(info[i]):
        sdl.append(i)
#sdl indica posicion salto de linea 

for i in range (sdl[2]+1,sdl[3]):
        instalaciones.append(info[i])
#instalaciones sin el deposito 
print(instalaciones,"\n")

for i in range (sdl[4]+1,sdl[5]): #clientes
        clientes.append(info[i])

for i in range (sdl[6]+1,len(info)):
    instalaciones_clientes.append(info[i])
print(instalaciones_clientes)#indica cuantos clientes hay en cada instalacion y cuales son 

###
profits = []
for i in range(len(instalaciones_clientes)): 
    profits.append(instalaciones_clientes[i][1])
    print(instalaciones_clientes[i][1])
profits.insert(0,0)
print(profits)
##LA INSTALACIÓN i EN LA LISTA PROFITS ES i-1
##LA INSTALACIÓN 1 EN PROFITS ES LA POSICIÓN 0.
    
deposito=(info[sdl[1]+1])
depositoo=list(deposito)

cord_xD=[depositoo[1]]
cord_yD=[depositoo[2]]

#print(cord_xD)
#print(cord_yD)
#deposito cordenadas 
insta_con_depo=[deposito]+instalaciones
#print(insta_con_depo)
Icd=[]
for i in range (len(insta_con_depo)):
    Icd.append(i)
#print(Icd) 

idI=[]
for i in range(1,len(instalaciones)+1):
    idI.append(i)
#print(id,"\n")
cord_x=[]
cord_y=[]
for i in range(1,len(instalaciones)+1):
    cord_x+=[insta_con_depo[i][1]]
    cord_y+=[insta_con_depo[i][2]]
#cordenada en x cordenada en y en inslaciones 

cord_cx=[]
cord_cy=[]
for i in clientes:
    cord_cx.append(i[1])
    cord_cy.append(i[2])


# In[198]:


#definicion de conjuntos 
cliente=[x for x in range(I+1,I+C+1)]
tuplas_Iclientes=[]
for i in instalaciones_clientes:
        I=i[0]
        for j in range(2,2+i[1]):
            tuplas_Iclientes.append((i[j],I))
#s={i for i in tuplas_Iclientes} 
tuplas_Iclientes=tuple(tuplas_Iclientes) #que instalacion abastece a que cliente 
print(tuplas_Iclientes)



# In[199]:


import matplotlib.pyplot as plt

plt.figure(figsize=(12,5))
plt.scatter(cord_cx,cord_cy,color="green") #clientes
plt.scatter(cord_x,cord_y,color="purple") #instalaciones
plt.scatter(cord_xD,cord_yD,color="red") #instalacion de abastecimieno
plt.show()


# In[200]:


X=cord_xD+cord_x #coordenada instalacion con deposito
Y=cord_yD+cord_y   #coordenada instalacion con deposito 
instalacionmasdeposito=[i for i in range(0,I+1)] 
instalacionsindeposito=[i for i in range(1,I+1)]
arcos={(i,j)for i in instalacionmasdeposito for j in instalacionmasdeposito if i!=j}
print(arcos)
print(instalacionmasdeposito)
#arcos


# In[201]:


distancia={(i,j):np.hypot(X[i]-X[j],Y[i]-Y[j]) for i,j in arcos}
beneficio = {(i,j): profits[i]+profits[j] for i,j in arcos}
print(beneficio)

# In[202]:

##Nearest Neighbor Heuristic

starting_node=0

NN=[starting_node]

while len(NN)<I:
    k=NN[-1] 
    #print(k)
    nn={(k,j): distancia[(k,j)]/beneficio[(k,j)] for j in instalacionmasdeposito if k!=j and j not in NN}
    print(nn)
    new=min(nn.items(), key=lambda x:x[1])
    #print(new)
    l=new[0][1]
    NN.append(new[0][1])
    P=P-profits[l]
    #print(P)
    if P<=0:
        break
NN.append(starting_node)


plt.figure(figsize=(12,6))
plt.scatter(X,Y,color="blue")
for i in range(len(X)):
    plt.annotate(str(i), xy=(X[i],Y[i]),xytext=(X[i]-1,Y[i]-1),color='red')
for i in range(len(NN)-1):
    plt.plot([X[NN[i]],X[NN[i+1]]],[Y[NN[i]],Y[NN[i+1]]],color='purple')
plt.xlabel("Coord_x")
plt.ylabel("Coord_y")
plt.title("vecino mas cercano")

plt.show()
#print(NN)

dist=0
for n in range(len(NN)-1):
    i=NN[n]
    j=NN[n+1]
    dist=dist+distancia[(i,j)]
#print(dist)    

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
#print(sol)


new_data = []
seen=set()
sol_mejor=set()
for i in tuplas_Iclientes:
    first=i[0]
    second=i[1]
    print(second)
    if first in seen:
        continue
    seen.add(first)
    new_data.append(i[1])
    
# =============================================================================
#     for j in new_data:
#             sol_mejor.add(j[1])
#             #P=P-profits[l]
#             s=list(sol_mejor)
# =============================================================================
new_data = set(new_data)
print(new_data)
print(s)


for i in range(1,len(NN)-1):
    NN[i]



dist=0
for n in range(len(NN)-1):
    i=NN[n]
    j=NN[n+1]
    dist=dist+distancia[(i,j)]
#print(dist) 


plt.figure(figsize=(12,6))
plt.scatter(X,Y,color="blue")
for i in range(len(X)):
    plt.annotate(str(i), xy=(X[i],Y[i]),xytext=(X[i]-1,Y[i]-1),color='red')
for i in range(len(NN)-1):
    plt.plot([X[NN[i]],X[NN[i+1]]],[Y[NN[i]],Y[NN[i+1]]],color='purple')
plt.xlabel("Coord_x")
plt.ylabel("Coord_y")
plt.title("vecino mas cercano")




# In[ ]:





# In[ ]:





# In[ ]:




