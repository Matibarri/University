import tsplib95
import matplotlib.pyplot as plt
import random
import time
from visualizar import animacion

import array
import numpy
from deap import algorithms
from deap import base
from deap import creator
from deap import tools

graficar_ruta = False
coord_x = []
coord_y = []
problem = tsplib95.load('instancias/st70.tsp')

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

def mutSet(ciudad):
    #perturbation(ciudad)
    # value = random.uniform(0, 1)
    # if value < 0.3:
    #     perturbation(ciudad)
    # elif value >= 0.3 and value < 0.6:
    #     perturbation2(ciudad)
    # elif value >= 0.6 and value < 0.85:
    perturbation2(ciudad)
    # else:
    #     DosOpt(ciudad)

    return ciudad,

def GA(ciudad):
    n = len(ciudad)
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, typecode='i', fitness=creator.FitnessMin) #minimizar, la poblacion la voy aminimizar 
    toolbox = base.Toolbox()# inicializar, estamos creando un cosntructor generico, este va 

    # Attribute generator
    #toolbox.register("indices", random.sample, range(n), n)

    toolbox.register("indices", vecinoMasCercano, n)

    # Structure initializers
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # toolbox.register("mate", tools.cxPartialyMatched)
    #toolbox.register("mate", tools.cxUniformPartialyMatched)
    toolbox.register("mate", tools.cxOrdered) # cxorddered vista en clases 
    #toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("mutate", mutSet)
    toolbox.register("select", tools.selTournament, tournsize=4)
    toolbox.register("evaluate", costoTotal)


    random.seed(1)#si cambiaramos el numero de la semilla van a ir cambiando 
    pop = toolbox.population(n=100) # estamos definiendo el tamaño de la poblacion

    hof = tools.HallOfFame(1)# calcular la estadistica

    stats = tools.Statistics(lambda ind: ind.fitness.values)# cargando la estadistica, quiere el prom,la desv
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    iterMax = 100
    inicioTiempo = time.time()
    result, log = algorithms.eaSimple(pop, toolbox, 0.9, 0.1, iterMax, stats=stats, halloffame=hof) #var 0.9 de crecimimiento,0.1 de mutacion
    # result, log = algorithms.eaSimple(pop, toolbox, cxpb=0.8, mutpb=0.2, ngen=400, verbose=False)
    finTiempo = time.time()
    tiempo = finTiempo - inicioTiempo

    minimo, promedio = log.select("min", "avg")

    best_individual = tools.selBest(result, k=1)[0] #rescatando el mejor individuo
    print('Costo  : %d' % costoTotal(best_individual)[0])
    print("Tiempo : %f" % tiempo)

    print(best_individual)
    # graficar
    graficar_soluciones(minimo)
    plt.figure(figsize=(12, 8))
    plt.xlim((0, iterMax))
 

    plots = plt.plot(minimo,'c-', promedio, 'b-')
    #print( log.select('mean'))
    plt.legend(plots, ('Costo Mínimo', 'Costo Promedio'), frameon=True)
    plt.ylabel('Costo')
    plt.xlabel('Iteraciones')
    plt.show()
    # lala = tools.selBest(result, 500)
    # for i in lala:
    #     print(costoTotal(i))

    # plt.figure(figsize=(12, 8))
    # plt.xlim((0, iterMax))


    # plots = plt.plot(minimo,'c-', promedio, 'b-')
    # #print( log.select('mean'))
    # plt.legend(plots, ('Costo Mínimo', 'Costo Promedio'), frameon=True)
    # plt.ylabel('Costo')
    # plt.xlabel('Iteraciones')
    # plt.show()


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

    #graficar(coord_x, coord_y, [])
    #GA2(ciudad)
    GA(ciudad)

if __name__ == "__main__":
    main()
