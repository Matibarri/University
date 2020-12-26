import tsplib95
import matplotlib.pyplot as plt
import random
import time

import array
import numpy
from deap import algorithms
from deap import base
from deap import creator
from deap import tools

graficar_ruta = False
coord_x = []
coord_y = []
problem = tsplib95.load('3.txt')

# distancia entre la ciudad i y j
def distancia(i, j):
    u = i+1, j+1
    return problem.get_weight(*u)

# Costo de la ruta
def costoTotal(ciudad):
    suma = 0
    i = 0
    while i < len(ciudad) - 1:
        # print(ciudad[i], ciudad[i +1])
        suma += distancia(ciudad[i], ciudad[i + 1])
        i += 1
    suma += distancia(ciudad[-1], ciudad[0])
    return suma,

# heurística del vecino más cercano
def vecinoMasCercano(n):
    desde = random.randrange(0, n)
    if random.uniform(0, 1) < 0.3:
        actual = desde
        ciudad = []
        ciudad.append(desde)
        seleccionada = [False] * n
        seleccionada[actual] = True
        # print(seleccionada)
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
        # print(ciudad)
        # print(costoTotal(ciudad))
    else:
        ciudad = [i for i in range(0, n)]
        random.shuffle(ciudad)
    return ciudad

def DosOpt(ciudad):

    actual = 0
    n = len(ciudad)
    flag = True
    contar = 0
    k = random.randint(0, len(ciudad) - 1)
    ciudad = ciudad[k:] + ciudad[:k]
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            nuevoCosto = distancia(ciudad[i], ciudad[j]) + distancia(ciudad[i + 1], ciudad[j + 1]) - distancia(ciudad[i], ciudad[i + 1]) - distancia(ciudad[j], ciudad[j + 1])
            if nuevoCosto < actual:
                actual = nuevoCosto
                min_i, min_j = i, j
                # Al primer cambio se sale
                contar += 1
                if contar == 1 :
                    flag = False

        if flag == False:
            break

    # Actualiza la subruta se encontró
    if actual < 0:
        ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]

def perturbation(ciudad):
    i = 0
    j = 0
    n = len(ciudad)
    while i == j:
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)

    # intercambio
    temp = ciudad[i]
    ciudad[i] = ciudad[j]
    ciudad[j] = temp

    return ciudad,

def perturbation3(ciudad):
    i = 0
    j = 0
    n = len(ciudad)
    while i == j:
        i = random.randint(0, n - 2)
        # j = random.randint(0, n - 1)
    j = i + 1
        # intercambio
    temp = ciudad[i]
    ciudad[i] = ciudad[j]
    ciudad[j] = temp

def perturbation2(ciudad):
    i = 0
    j = 0
    n = len(ciudad)
    while i >= j:
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
    ciudad[i : j] = ciudad[i : j][::-1]

def graficar_soluciones(soluciones):
    plt.plot([i for i in range(len(soluciones))], soluciones)
    plt.ylabel("Costo")
    plt.xlabel("Iteraciones")
    plt.title("Iteraciones vs Costo - TSP")
    plt.xlim((0, len(soluciones)))
    plt.show()

def graficar(coord_x, coord_y, solucion):
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
        plt.title("Ubicacion de las ciudades - TSP")

    ruta = list(solucion)
    if len(ruta) != 0:
        for i in range(len(ruta))[:-1]:
            plt.plot([coord_x[ruta[i]], coord_x[ruta[i+1]]],[coord_y[ruta[i]], coord_y[ruta[i+1]]], color='b', alpha=0.4, zorder=0)
            plt.scatter(x = coord_x, y = coord_y, color='blue', zorder=1)

    for n in range(len(coord_x)):
        plt.annotate(str(n), xy=(coord_x[n], coord_y[n] ), xytext=(coord_x[n]+0.5, coord_y[n]+1),color='red')


def AG(ciudad):
    creator.create("FitnessMin", base.Fitness, weights=(-1, ))
    creator.create("Individual", list, typecod="i", fitness=creator.FitnessMin)
    toolbox = base.Toolbox()
    n = len(ciudad)
    toolbox.register("indices", vecinoMasCercano, n) # generación población inicial
    #toolbox.register("indices", random.sample, range(n), n) # generación población inicial

    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices) # individuo
    toolbox.register("population", tools.initRepeat, list, toolbox.individual) # Población

    toolbox.register("evaluate", costoTotal) # función objetivo
    toolbox.register("select", tools.selTournament, tournsize = 3) # selección
    toolbox.register("mate", tools.cxOrdered) # cruzamiento
    #toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("mutate", perturbation)

    random.seed(1)

    poblacion = toolbox.population(n=100)

    hof = tools.HallOfFame(1)

    estadisticas = tools.Statistics(lambda ind: ind.fitness.values)
    estadisticas.register("avg", numpy.mean)
    estadisticas.register("min", numpy.min)
    estadisticas.register("max", numpy.max)
    estadisticas.register("std", numpy.std)

    numGen = 600

    inicioTiempo = time.time()
    resultados, log = algorithms.eaSimple(poblacion, toolbox, 0.9, 0.05, numGen, estadisticas, hof)
    finalTiempo = time.time()
    tiempo = finalTiempo - inicioTiempo

    minimo, promedio = log.select("min", "avg")

    plots = plt.plot(minimo, "c-", promedio, "b-")
    plt.show()


def main():
    G = problem.get_graph()
    ciudad = list(problem.get_nodes())
    info = problem.as_keyword_dict()

    if info['EDGE_WEIGHT_TYPE'] == 'EUC_2D': # se puede graficar la ruta
        global graficar_ruta
        graficar_ruta = True
        for i in range(1, len(ciudad) + 1):
            x, y = info['NODE_COORD_SECTION'][i]
            coord_x.append(x)
            coord_y.append(y)

    print("Algoritmos Genéticos")
    AG(ciudad)

if __name__ == "__main__":
    main()
