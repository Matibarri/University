#!/usr/bin/env python
# coding: utf-8

# In[195]:


#importamos bibliotecas 
import numpy as np 
import matplotlib.pyplot as plt
from docplex.mp.model import Model 


# In[196]:


#pruebe instancias 3 , 6 ,13 , 16 y 26 
archivo=open("16.txt","r")
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
#print(instalaciones,"\n")

for i in range (sdl[4]+1,sdl[5]): #clientes
        clientes.append(info[i])

for i in range (sdl[6]+1,len(info)):
    instalaciones_clientes.append(info[i])
#print(instalaciones_clientes)#indica cuantos clientes hay en cada instalacion y cuales son 

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
#print(tuplas_Iclientes)



# In[199]:


import matplotlib.pyplot as plt

plt.figure(figsize=(12,5))
plt.scatter(cord_cx,cord_cy,color="green") #clientes
plt.scatter(cord_x,cord_y,color="purple") #instalaciones
plt.scatter(cord_xD,cord_yD,color="red") #instalacion de abastecimietno
plt.show()


# In[200]:


X=cord_xD+cord_x #coordenada instalacion con deposito
Y=cord_yD+cord_y   #coordenada instalacion con deposito 
instalacionmasdeposito=[i for i in range(0,I+1)] 
instalacionsindeposito=[i for i in range(1,I+1)]
arcos={(i,j)for i in instalacionmasdeposito for j in instalacionmasdeposito if i!=j}
#print(arcos)
#print(instalacionmasdeposito)
#arcos


# In[201]:


distancia={(i,j):np.hypot(X[i]-X[j],Y[i]-Y[j]) for i,j in arcos}


# In[202]:


mdl=Model("tarea 1")


# In[203]:


x=mdl.binary_var_dict(arcos,name="x")
b=mdl.binary_var_dict(instalacionmasdeposito,name="b")
u=mdl.continuous_var_dict(instalacionmasdeposito,ub=P,name="u")
m=mdl.binary_var_dict(tuplas_Iclientes,name="m")


# In[204]:


#FO
mdl.minimize(mdl.sum(distancia[i]*x[i] for i in arcos))


# In[205]:


#deposito en uso siempre 
mdl.add_constraint(b[0]==1)
            
 #Segundo restricción sumatoria para todo j
for c in instalacionmasdeposito:
    mdl.add_constraint(mdl.sum(x[(i,j)] for i,j in arcos if j==c)==b[c])
    
#Primero restricción sumatoria para todo i
for c in instalacionmasdeposito:
    mdl.add_constraint(mdl.sum(x[(i,j)] for i,j in arcos if i==c)==b[c]) 
      
instaydep=I+1
for i,j in arcos: #subtor 
    if i!=0:
        mdl.add_constraint(u[i]-u[j]+(I+1)*x[(i,j)]<=I)
    
mdl.add_constraint(mdl.sum(m[(a,j)] for a,j in tuplas_Iclientes) >= P) #suma de mi beneficio tiene que ser mayor a iugal p

for j in cliente:
    mdl.add_constraint(mdl.sum(m[(i,k)] for i,k in tuplas_Iclientes if i==j)<=1) #que no existan clientes repetidps

for i in instalacionmasdeposito:
    for j in instalacionmasdeposito:
        if i!=j:
            mdl.add_constraint(x[(i,j)] + x[(j,i)] <= 1) #obliga ir en un sentido


for k in cliente:
    for j in instalacionmasdeposito:
        if (k,j) in tuplas_Iclientes:
            mdl.add_constraint(m[(k,j)] <= b[j])


# In[206]:


print(mdl.export_to_string())


# In[207]:


solucion=mdl.solve(log_output=True)
mdl.get_solve_status()


# In[208]:



solucion.display()


# In[209]:


#Imprimiento la solución óptima.


arcos_activos = [i for i in arcos if x[i].solution_value > 0.9]
for i,j in arcos_activos:
    plt.plot([X[i],X[j]],[Y[i],Y[j]],
              color='b', alpha=0.4, zorder=0)
plt.scatter(x=X, y=Y, color='blue', zorder=1) #instalacion activas en azul  
plt.xlabel("Distancia X")
plt.ylabel("Distancia Y")
plt.title("Ubicación de la instalaciones con ruta minima - TSP")
plt.figure(figsize=(12,5))
plt.scatter(cord_cx,cord_cy,color="green") #clientes
plt.scatter(cord_x,cord_y,color="purple") #instalaciones
plt.scatter(cord_xD,cord_yD,color="red") #instalacion de abastecimietno
plt.scatter
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:




