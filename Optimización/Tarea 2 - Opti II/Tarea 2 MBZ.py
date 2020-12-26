# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 21:15:41 2020

@author: matibarri
"""

#importamos bibliotecas 
import numpy as np 
import matplotlib.pyplot as plt
import random
import time
#pruebe instancias


nombre = input("Ingrese el nombre del archivo:")

def lectura_archivo(Archivo):
    archivo=open(Archivo,"r")
    l=archivo.readlines()
    archivo.close()
    Info=[i.split() for i in l]
    for j in range(len(Info)):
        for z in range(len(Info[j])):
            Info[j][z]=int(float(Info[j][z]))
    return Info

def distance(i,j):
    return np.hypot(X[i]-X[j],Y[i]-Y[j])

def costoTotal(ciudad):
    suma = 0.00
    i = 0
    while i < len(ciudad) - 1:
        # print(ciudad[i], ciudad[i +1])
        suma += distance(ciudad[i], ciudad[i + 1])
        i += 1
    suma += distance(ciudad[-1], ciudad[0])
    return suma

#deposito
info = lectura_archivo(nombre)
V=int(info[0][0])
I=int(info[1][0])
C=int(info[2][0])
P=int(info[3][0])
instaydep=I+1

#print(P)
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
#indica cuantos clientes hay en cada instalacion y cuales son 

###
profits = []
for i in range(len(instalaciones_clientes)): 
    profits.append(instalaciones_clientes[i][1])
    #print(instalaciones_clientes[i][1])
profits.insert(0,0)

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

#definicion de conjuntos 
cliente=[x for x in range(I+1,I+C+1)]
tuplas_Iclientes=[]
for i in instalaciones_clientes:
        I=i[0]
        for j in range(2,2+i[1]):
            tuplas_Iclientes.append((i[j],I))
#s={i for i in tuplas_Iclientes} 
tuplas_Iclientes=tuple(tuplas_Iclientes) #que instalacion abastece a que cliente 


#GRAFICO INSTALACIONES Y CLIENTES
plt.figure(figsize=(12,5))
plt.scatter(cord_cx,cord_cy,color="green") #clientes
plt.scatter(cord_x,cord_y,color="purple") #instalaciones
plt.scatter(cord_xD,cord_yD,color="red") #instalacion de abastecimieno
plt.show()
###

X=cord_xD+cord_x #coordenada instalacion con deposito
Y=cord_yD+cord_y   #coordenada instalacion con deposito 
instalacionmasdeposito=[i for i in range(0,I+1)] 
instalacionsindeposito=[i for i in range(1,I+1)]
arcos={(i,j)for i in instalacionmasdeposito for j in instalacionmasdeposito if i!=j}

#arcos

distancia={(i,j):np.hypot(X[i]-X[j],Y[i]-Y[j]) for i,j in arcos}
beneficio = {(i,j): profits[i]+profits[j] for i,j in arcos}



###HERUSTICA VECINO MAS CERCANO 
def vecinoMasCercano_P(n,starting_node):
# =============================================================================
#     starting_node=0
# ============================================================================
    sol_mejor=set()
    starting_node=0
    p=0
    NN=[starting_node]
    new_data = []
    seen=set()
    #len(NN)<=I
    while p<P:
        k=NN[-1] 
        nn={(k,j): distancia[(k,j)]/beneficio[(k,j)] for j in range(len(instalaciones)) if k!=j and j not in NN}
        new=min(nn.items(), key=lambda x:x[1])
        mm={(k,j): distancia[(j,k)]/beneficio[(j,k)] for j in range(len(instalaciones)) if k!=j and j not in NN and j not in sol_mejor}
        NEW=min(mm.items(), key=lambda x:x[1])
       
        NN.append(NEW[0][1])
        NN.append(new[0][1])
        
        #print(delta)
        #if p<=P:
        for i in tuplas_Iclientes:
            first=i[0]
            second=i[1]
            if second in NN:
                if first in seen:
                    continue
                new_data.append(i)
                #print(i)
                seen.add(first)
                #print(seen)
                p=len(seen)

        for i in new_data:
            sol_mejor.add(i[1])
            #print(sol_mejor)
            s=list(sol_mejor)
            #print(p)
            
        if p>=P:
            #print(p)
            break

        #print(seen)
        
        #print(new_data)
    s.append(0)
    s.insert(0,0)
    return s


# Búsqueda Local 2-opt
def DosOpt(ciudad):
    n = len(ciudad)
    flag = True #Bandera: Variable binaria que activa o desactiva cosas.
    contar = 0
    costoActual = 0
    for i in range(1,n - 2):
        for j in range(i + 1, n - 1):
            if i!=0 and j!=0:
                nuevoCosto = distance(ciudad[i], ciudad[j]) + distance(ciudad[i + 1], ciudad[j + 1]) - distance(ciudad[i], ciudad[i + 1]) - distance(ciudad[j], ciudad[j + 1])
                if nuevoCosto < costoActual:
                    costoActual = nuevoCosto
                    min_i, min_j = i, j
                    contar += 1
                    if contar == 2:
                        flag = False
                        #ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]
                        # break
        if flag == False:
            break
    if contar > 0:
        ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]

def reverse_segment_if_better(tour, i, j, k):
    """If reversing tour[i:j] would make the tour shorter, then do it."""
    # Given tour [...A-B...C-D...E-F...]
    A, B, C, D, E, F = tour[i-1], tour[i], tour[j-1], tour[j], tour[k-1], tour[k % len(tour)]
    d0 = distance(A, B) + distance(C, D) + distance(E, F)
    d1 = distance(A, C) + distance(B, D) + distance(E, F)
    d2 = distance(A, B) + distance(C, E) + distance(D, F)
    d3 = distance(A, D) + distance(E, B) + distance(C, F)
    d4 = distance(F, B) + distance(C, D) + distance(E, A)

    if d0 > d1:
        tour[i:j] = reversed(tour[i:j])
        return -d0 + d1
    elif d0 > d2:
        tour[j:k] = reversed(tour[j:k])
        return -d0 + d2
    elif d0 > d4:
        tour[i:k] = reversed(tour[i:k])
        return -d0 + d4
    elif d0 > d3:
        tmp = tour[j:k] + tour[i:j]
        tour[i:k] = tmp
        return -d0 + d3
    return 0

def all_segments(n: int):
    """Generate all segments combinations"""
    return ((i, j, k)
        for i in range(1,n)
        for j in range(i + 2, n)
        for k in range(j + 2, n + (i > 0)))

def three_opt(tour):
    """Iterative improvement based on 3 exchange."""
    while True:
        delta = 0
        for (a, b, c) in all_segments(len(tour)):
            delta += reverse_segment_if_better(tour, a, b, c)
        if delta >= 0:
            break
    
    return tour



# perturbación
def perturbacion(ciudad):
    random.seed(1)
    n = len(ciudad)
    i = random.randint(0, n-1)
    j = 0#random.randint(0,n-1)
    if i != n - 1:
        j = i + 1

    # intercambio
    it=30
    for q in range(it):
        temp = ciudad[i]
        ciudad[i] = ciudad[j]
        ciudad[j] = temp

  
def ILS(ciudad):
    lista_soluciones = []
    lista_costos = []
    #n = len(ciudad)
    inicioTiempo = time.time()
    ciudadInicial = 0 #random.randint(0, n)
    NN=vecinoMasCercano_P(instalacionmasdeposito,ciudadInicial) #SOLUCION INICIAL
    three_opt(NN)
    s_mejor = NN[:]
    costo = costoTotal(NN)
    costoMejor = costo
    iteracion_max = 100
    lista_costos.append(costo)
    lista_soluciones.append(NN)
#Repeat del pseudocódigo
    
    for iter in range(iteracion_max):
        # Perturbacion linea 5 del pseudocodigo
        perturbacion(NN)
        
        # Búsqueda Local linea 6 del pseudocodigo

      
        DosOpt(NN)
        DosOpt(NN)
        three_opt(NN)
        three_opt(NN)
        costo_candidato = costoTotal(NN)
        print("%d\t%d" % (iter, costo_candidato)) #Imprime todas las soluciones que genera
        
        # linea 7 del pseudocodigo
        if costoMejor > costo_candidato:
            costoMejor = costo_candidato
            s_mejor = NN[:]
            print("\t%d\t%d" % (iter, costoMejor))

        lista_costos.append(costo_candidato)
        lista_soluciones.append(NN)
        
        # Criterio de aceptación linea 8 del pseudocodigo
        if costo_candidato<=costoMejor:
            NN=s_mejor[:]
# =============================================================================
#         if abs(costoMejor - costo_candidato) / costoMejor > 0.50:
#             NN = s_mejor[:]
# =============================================================================

    finTiempo = time.time()
    tiempo = finTiempo - inicioTiempo

    print("Costo  : %d" % costoMejor)
    print("Tiempo : %f" % tiempo)
    print(NN)

    lista_costos.append(costoMejor)
    lista_soluciones.append(s_mejor)

    ##Gráfico
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


ILS(instalacionmasdeposito)



