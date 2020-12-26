# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class animacion:
    def __init__(self, historial, x, y, costs):
        self.historial = historial
        self.costs = costs
        self.points = np.column_stack((x, y))
        self.fig, self.ax = plt.subplots()
        self.line, = plt.plot([], [], lw = 2)
        self.title = self.ax.text(0.8, 1.035, "", bbox={'facecolor':'w', 'alpha':0.5, 'pad':5}, transform = self.ax.transAxes, ha = "center")

    # genera los nodos vacíos
    def iniciar(self):
        # graficar nodos
        x = [self.points[i][0] for i in self.historial[0]]
        y = [self.points[i][1] for i in self.historial[0]]
        plt.plot(x, y, 'co')
        # dibujar ejes
        extra_x = (max(x) - min(x)) * 0.05
        extra_y = (max(y) - min(y)) * 0.05
        self.ax.set_xlim(min(x) - extra_x, max(x) + extra_x)
        self.ax.set_ylim(min(y) - extra_y, max(y) + extra_y)
        # inicializar solución vacía
        self.line.set_data([], [])
        return self.line,

    # por cada frame actualiza la solución en el grafo
    def actualizar(self, frame):
        x = [self.points[i, 0] for i in self.historial[frame] + [self.historial[frame][0]]]
        y = [self.points[i, 1] for i in self.historial[frame] + [self.historial[frame][0]]]
        self.title.set_text("Iteracion {}, costo {}".format(frame, self.costs[frame]))
        self.line.set_data(x, y)
        return self.line

    # Anima el gráfico
    def animacionRutas(self):
        div = len(self.historial) // 3
        key_frames_mult = len(self.historial) // div
        ani = FuncAnimation(self.fig, self.actualizar, frames = range(0, len(self.historial), key_frames_mult), init_func = self.iniciar, interval = 3, repeat = False)
        plt.title("Ruta - TSP")
        plt.show()
