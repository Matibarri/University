
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def loglineal(x0,px0,n,f,g):
  x = np.empty(n+1, dtype=object) 
  x[0]=x0
  
  for i in range(1,n+1):
    x[i] = f(x[i-1])
  
  xl = np.empty(n+1, dtype=object) 
  xl[0]=px0
  
  for i in range(1,n+1):
    xl[i] = g(xl[i-1])
  
  fig, ax = plt.subplots(figsize=(9, 6))

  for spine in ['left', 'bottom']:
    ax.spines[spine].set_position(('data',0))
  for spine in ['right', 'top']:
    ax.spines[spine].set_color('none')

  ax.xaxis.set_ticks_position('bottom')
  ax.yaxis.set_ticks_position('left')

  ax.grid()
  ax.axhline(0.7391,0.05,0.95, label = "Estado estacionario", color = 'brown')

  ax.plot(x, 'or', label='$x_{t+1}$')
  ax.plot(x, '--b', lw=2)
  

  ax.set_xlabel('$t$ tiempo', fontsize=14, color='k')
  ax.plot(xl,'go',label='$\widetilde{x}_{t+1}$')
  ax.plot(xl,'--g')


  ax.legend(loc='best', shadow=True, fancybox=True)
  ax.set_title("Simulacion en tiempo discreto",
             fontsize=16,color='k',pad=20)
  ax.axhline(0,0.5,0.6,lw=0.1)

  xa = 0.7691 + 0.7691 * xl
  ax.plot(xa,'-k')
  
  plt.show()

def miplotdis(x):
    
  fig, ax = plt.subplots(figsize=(9, 6))

  for spine in ['left', 'bottom']:
    ax.spines[spine].set_position(('data',0))
  for spine in ['right', 'top']:
    ax.spines[spine].set_color('none')

  ax.xaxis.set_ticks_position('bottom')
  ax.yaxis.set_ticks_position('left')

  
  #ax.axhline(0.7391,0.05,0.95, label = "Estado estacionario", color = 'brown')#

  ax.plot(x, 'or', label='secuenia')
  ax.plot(x, '--b', lw=2)
  ax.axhline(0,0.5,0.55,lw=0.1)

  ax.set_xlabel('$t$ tiempo', fontsize=14, color='k')
  #ax.plot(xl,'go',label='$\widetilde{x}_{t+1}$')
  #ax.plot(xl,'--g')


  #ax.legend(loc='best', shadow=True, fancybox=True)
  ax.set_title("Simulacion en tiempo discreto",
             fontsize=16,color='k',pad=20)
  #ax.axhline(0,0.5,0.6,lw=0.1)

  
  plt.show()

def miplotdisv(x):
    
  fig, ax = plt.subplots(figsize=(9, 6))

  for spine in ['left', 'bottom']:
    ax.spines[spine].set_position(('data',0))
  for spine in ['right', 'top']:
    ax.spines[spine].set_color('none')

  ax.xaxis.set_ticks_position('bottom')
  ax.yaxis.set_ticks_position('left')

  
  #ax.axhline(0.7391,0.05,0.95, label = "Estado estacionario", color = 'brown')#
  
  cp=sns.color_palette("Set2", 10)
  
  for i in range(len(x)):
    ax.plot(x[i], 'o', color=cp[i])
    ax.plot(x[i], '--', color = cp[i], lw=2)

  ax.axhline(0,0.5,0.55,lw=0.1)

  ax.set_xlabel('$t$ tiempo', fontsize=14, color='k')
  #ax.plot(xl,'go',label='$\widetilde{x}_{t+1}$')
  #ax.plot(xl,'--g')


  #ax.legend(loc='best', shadow=True, fancybox=True)
  ax.set_title("Simulacion en tiempo discreto",
             fontsize=16,color='k',pad=20)
  #ax.axhline(0,0.5,0.6,lw=0.1)

  
  plt.show()

def imprimir(x):
  df = pd.DataFrame({'datos 1':x[0]}) 
  for i in range(1,len(x)):
    df['datos '+ str(i+1)]= pd.Series(x[i])
  return df