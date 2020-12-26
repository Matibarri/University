# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 11:35:45 2020

@author: matibarri
"""

import numpy as np
import pandas as pd
import matplotlib as mpl
import scipy
import importlib
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, chi2
"""

Goal: create a normality test, e.g. Jarque-Bera.

step 1: generate random variables
step 2: visualise histogram
step 3: what is Jarque-Bera

Borel Cantelli theorem: En el test de Jarque Bera, implica que si corro dicho
test "n" veces, aún cuando la distribución es normal, habrá casos donde el test
fallará.
"""

##generate random variable

x_size = 10**6
degrees_freedom = 2
type_random_variable = 'exponential' # normal exponential student chi-squared

if type_random_variable == 'normal':
    x = np.random.standard_normal(size = x_size)
    x_str = type_random_variable
elif type_random_variable == 'exponential':
    x = np.random.standard_exponential(size = x_size)
    x_str = type_random_variable
elif type_random_variable == 'student':
    x = np.random.standard_t(df=degrees_freedom, size = x_size)
    x_str = type_random_variable + ' (df=' + str(degrees_freedom) + ')'
elif type_random_variable == 'chi-squared':
    x = np.random.chisquare(df=degrees_freedom,size=x_size)
    x_str = type_random_variable + ' (df=' + str(degrees_freedom) + ')'


# compute "risk metrics"

x_mean = np.mean(x)
x_stdev = np.std(x)
x_skew = skew(x) #Integral del momento de orden 3
x_kurt = kurtosis(x) #excess kurtosis: kurtosis original-3 
#(la kurtosis de una variable aleatoria estándar es 3)
x_median = np.percentile(x, 50)
x_var_95 = np.percentile(x,5) # Solamente el 5% de los valores son maenores que el resultado de x_var_95
JB = x_size/6*(x_skew**2 + 1/4*x_kurt**2)
p_value = 1-chi2.cdf(JB, df=2) #Cuál es la probabiliad de tener puntos que caigan a la izquierda de dicho x_JB
is_normal = (p_value > 0.05) # equivalently JB < 6

# print metrics
print(x_str)
print('mean ' + str(x_mean))
print('std ' + str(x_stdev))
print('skewness ' + str(x_skew))
print('kurtosis ' + str(x_kurt))
print('VaR 95% ' + str(x_var_95))
print('x_JB ' + str(JB))
print('p-value ' + str(p_value))
print('is normal ' + str(is_normal))

##plot histogram
plt.figure(figsize=(12,6)) #genera la figura
plt.hist(x,bins=100) #crea el histograma y bins adelgaza las "barritas"
plt.title('Histogram ' + x_str)
#plt.xlabel(plot_str)
plt.show() #muestra la figura





