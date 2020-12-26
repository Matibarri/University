# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 01:31:03 2020

@author: matibarri
"""

import numpy as np
import pandas as pd
import matplotlib as mpl
import scipy
import importlib
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, chi2

# import our own files and reload

import static_functions
importlib.reload(static_functions) #Actualiza los cambios en static_functions
import classes
importlib.reload(classes) 

#input
ric = 'ANTO.L' # ^IXIC DBK.DE CLP=X ANTO.L
file_extension = 'csv' # csv o excel extension

#get market data

x, x_str, t = static_functions.load_time_series(ric, file_extension)

static_functions.plot_time_series_price(t, ric)


## Recycled code ##

# compute "risk metrics"
x_size = t['return_close'].shape[0]
x_mean = np.mean(x) #media
x_std = np.std(x) #volatility (volatibilidad) en mercados financieros
x_skew = skew(x)  #Skewness para ver qué tan simétrica es
x_kurt = kurtosis(x) #Kurtosis para ver qué tantas colas largas tiene
x_sharpe = x_mean/x_std * np.sqrt(252) #coeficiente de Sharpe (annualised: x_mean crece lineal en el tiempo y x_stdev raíz cuadrada en el tiempo)
x_median = np.percentile(x, 50) # 
x_var_95 = np.percentile(x,5)  #Valor en riesgo
x_cvar_95 = np.mean(x[x <= x_var_95]) #CVaR: Valor en riesgo condicional (promedio de pérdidas)
JB = x_size/6*(x_skew**2 + 1/4*x_kurt**2) #Estadístico Jarque-Bera
p_value = 1-chi2.cdf(JB, df=2) #p-value chi cuadrado símil al JB
is_normal = (p_value > 0.05)  #Para saber si la distribución es normal o no.


# print metrics
round_digits = 4
plot_str = 'mean ' + str(np.round(x_mean,round_digits))\
    + ' | std dev ' + str(np.round(x_std,round_digits))\
    + ' | skewness ' + str(np.round(x_skew,round_digits))\
    + ' | kurtosis ' + str(np.round(x_kurt,round_digits))\
    + ' | Sharpe ratio ' + str(np.round(x_sharpe,round_digits)) + '\n'\
    + 'VaR 95% ' + str(np.round(x_var_95,round_digits))\
    + ' | CVaR 95% ' + str(np.round(x_cvar_95,round_digits))\
    + ' | jarque_bera ' + str(np.round(JB,round_digits))\
    + ' | p_value ' + str(np.round(p_value,round_digits))\
    + ' | is_normal ' + str(is_normal)

static_functions.plot_histogram(x, x_str, plot_str )

