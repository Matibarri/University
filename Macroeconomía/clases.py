# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

class dindis():
  def __init__(self, x0=0.04, f = lambda x:np.cos(x),n=15):
    self.x0, self.f, self.n = x0, f, n
  
  def eval(self,x):
    return  self.f(x)
  
  def orbita(self, n=0):
    if n ==0:
      n = self.n
    x = np.empty(n+1, dtype=object) 
    x[0]=self.x0
    for i in range(1,n+1):
      x[i] = self.eval(x[i-1])
    return x
  
  def ee(self, x0=0):
    if x0==0:
      x0=self.x0
    g = lambda x: self.f(x)-x
    return fsolve(g,g(x0))
    
  def plot_orbita(self, n=0, ee=False, guarda = False, x0=0, eed = ''):
    if n ==0:
      n = self.n
    x = self.orbita(n)
    
    fig, ax = plt.subplots(figsize=(9, 6))
    for spine in ['left', 'bottom']:
      ax.spines[spine].set_position(('data',0))
    for spine in ['right', 'top']:
      ax.spines[spine].set_color('none')

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    #ax.grid()
    #ax.axhline(0.7391,0.05,0.95, label = "Estado estacionario", color = 'brown')

    ax.plot(x, 'or', label='$x_{t}$')
    ax.plot(x, '--b', lw=2)
    ax.set_xlabel('$t$ tiempo', fontsize=14, color='k')
    ax.set_title("Simulacion en tiempo discreto",
             fontsize=16,color='k',pad=20)
    
    ax.axhline(0,0.5,0.55,lw=0.1)

    if ee:
        if eed =='':
            ax.axhline(self.ee(x0),0.05,0.95,\
                       color = 'brown',\
                       label='$\overline{x}=%s$'%self.ee()+' Estado estacionario')
        else:
            ax.axhline(eed,0.05,0.95,\
                       color = 'brown',\
                       label='$\overline{x}=%s$'%eed+' Estado estacionario')
                    
    
    ax.legend(loc='best', shadow=True, fancybox=True)

    
    if guarda:
      plt.savefig("graficasc.png")
      plt.savefig("graficasc.svg")
      plt.savefig("graficasc.pdf")
   
    
    plt.show()


