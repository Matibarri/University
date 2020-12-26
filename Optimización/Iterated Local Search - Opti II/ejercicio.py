# -*- coding: utf-8 -*-
import tsplib95
import matplotlib.pyplot as plt
import random
import time
from visualizar import animacion

graficar_ruta = False
coord_x = []
coord_y = []
nombre = input("Ingrese el nombre del archivo:")
#pruebe instancias 
archivo=open(nombre,"r")
l=archivo.readlines()
archivo.close()
info=[i.split() for i in l]
for j in range(len(info)):
    for z in range(len(info[j])):
        info[j][z]=int(float(info[j][z]))
        
# Instancias oficiales desde http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/
problem = tsplib95.load('instancias/st70.tsp')

# distancia entre la ciudad i y j
def distancia(i, j):
    u = i+1, j+1
    return problem.get_weight(*u)

# Cálcula el costo de la ruta
def costoTotal(ciudad):
    suma = 0
    i = 0
    while i < len(ciudad) - 1:
        # print(ciudad[i], ciudad[i +1])
        suma += distancia(ciudad[i], ciudad[i + 1])
        i += 1
    suma += distancia(ciudad[-1], ciudad[0])
    return suma

# heurística del vecino más cercano
def vecinoMasCercano(n, desde):
    actual = desde
    ciudad = []
    ciudad.append(desde)
    seleccionada = [False] * n
    seleccionada[actual] = True

    while len(ciudad) < n:
        min = 9999999
        for candidata in range(n):
            if seleccionada[candidata] == False and candidata != actual:
                costo = distancia(actual, candidata)
                if costo < min:
                    min = costo
                    siguiente = candidata

        ciudad.append(siguiente)
        seleccionada[siguiente] = True
        actual = siguiente

    return ciudad

# Búsqueda Local 2-opt
def DosOpt(ciudad):
    n = len(ciudad)
    flag = True #Bandera: Variable binaria que activa o desactiva cosas.
    contar = 0
    costoActual = 0
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            nuevoCosto = distancia(ciudad[i], ciudad[j]) + distancia(ciudad[i + 1], ciudad[j + 1]) - distancia(ciudad[i], ciudad[i + 1]) - distancia(ciudad[j], ciudad[j + 1])
            if nuevoCosto < costoActual:
                costoActual = nuevoCosto
                min_i, min_j = i, j
                contar += 1
                if contar == 1:
                    flag = False
                    #ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]
                    # break
        if flag == False:
            break
    if contar > 0:
        ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]


# perturbación
def perturbacion(ciudad):
    n = len(ciudad)
    i = random.randint(0, n-1)
    j = 0
    if i != n - 1:
        j = i + 1

    # intercambio
    temp = ciudad[i]
    ciudad[i] = ciudad[j]
    ciudad[j] = temp

# ILS
def ILS(ciudad):
    random.seed(1)
    lista_soluciones = []
    lista_costos = []
    n = len(ciudad)
    inicioTiempo = time.time()
    ciudadInicial = 0#random.randint(0, n)
    s = vecinoMasCercano(n, ciudadInicial) #SOLUCION INICIAL
    # finTiempo = time.time()
    # tiempo = finTiempo - inicioTiempo
    #costo = costoTotal(s)
    # print("Costo  : %d" % costo)
    # print("Tiempo : %f" % tiempo)
    # print(s)
    #    graficar(solucion, costo)
    # lista_costos.append(costo)
    # lista_soluciones.append(s)
    # inicioTiempo = time.time()
    DosOpt(s)
    s_mejor = s[:]
    costo = costoTotal(s)
    costoMejor = costo
    # print("Costo  : %d" % costo)
    # print("Tiempo : %f" % tiempo)
    #print(s)
    iteracion_max = 350
    lista_costos.append(costo)
    lista_soluciones.append(s)

#Repeat del pseudocódigo
    
    for iter in range(iteracion_max):
        # Perturbacion linea 5 del pseudocodigo
        perturbacion(s)

        # Búsqueda Local linea 6 del pseudocodigo
        DosOpt(s)
        DosOpt(s)
        costo_candidato = costoTotal(s)
        #print("%d\t%d" % (iter, costo_candidato)) #Imprime todas las soluciones que genera
        
        # linea 7 del pseudocodigo
        if costoMejor > costo_candidato:
            costoMejor = costo_candidato
            s_mejor = s[:]
            print("\t%d\t%d" % (iter, costoMejor))

        lista_costos.append(costo_candidato)
        lista_soluciones.append(s)
        
        # Criterio de aceptación linea 8 del pseudocodigo
        if abs(costoMejor - costo_candidato) / costoMejor > 0.005:
            s = s_mejor[:]


    finTiempo = time.time()
    tiempo = finTiempo - inicioTiempo

    print("Costo  : %d" % costoMejor)
    print("Tiempo : %f" % tiempo)
    print(s)

    lista_costos.append(costoMejor)
    lista_soluciones.append(s_mejor)
    ver = animacion(lista_soluciones, coord_x, coord_y, lista_costos)
    ver.animacionRutas()
    #graficar(solucion, costo)

def graficar(solucion, costo):
    plt.figure(figsize = (20,20))
    plt.scatter(coord_x, coord_y, color = 'blue')
    s = []
    for n in range(len(coord_x)):
        s_temp = []
        s_temp.append("%.1f" % coord_x[n])
        s_temp.append("%.1f" % coord_y[n])
        s.append(s_temp)

        plt.xlabel("Distancia X")
        plt.ylabel("Distancia Y")
        plt.title("Ubicacion de las ciudades - TSP, costo: %d" %(costo))

    ruta = list(solucion)
    if len(ruta) != 0:
        for i in range(len(ruta))[:-1]:
            plt.plot([coord_x[ruta[i]], coord_x[ruta[i+1]]],[coord_y[ruta[i]], coord_y[ruta[i+1]]], color='b', alpha=0.4, zorder=0)
            plt.scatter(x = coord_x, y = coord_y, color='blue', zorder=1)
        plt.plot([coord_x[ruta[-1]], coord_x[ruta[0]]],[coord_y[ruta[-1]], coord_y[ruta[0]]], color='b', alpha=0.4, zorder=0)

    for n in range(len(coord_x)):
        plt.annotate(str(n), xy=(coord_x[n], coord_y[n] ), xytext=(coord_x[n]+0.5, coord_y[n]+1),color='red')

    plt.show()

def main():
    #G = problem.get_graph()
    ciudad = [i-1 for i in list(problem.get_nodes())]

    info = problem.as_keyword_dict()
    print(info)

    if info['EDGE_WEIGHT_TYPE'] == 'EUC_2D': # se puede graficar la ruta
        global graficar_ruta
        graficar_ruta = True
        for i in range(1, len(ciudad) + 1):
            x, y = info['NODE_COORD_SECTION'][i]
            coord_x.append(x)
            coord_y.append(y)

    ILS(ciudad)

if __name__ == "__main__":
    main()
