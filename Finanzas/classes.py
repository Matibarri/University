# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 12:14:45 2020

@author: matibarri
"""

import numpy as np
import pandas as pd
import matplotlib as mpl
import scipy
import importlib
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, chi2, linregress
import static_functions
importlib.reload(static_functions) 

class jarque_bera_test():
    
    ##Constructor: Inicializar todos los atributos (En python se puede evitar, pero es una buena práctica)
    def __init__(self, ric): #Separar el constructor de los cálculos y el print
        self.ric = ric
        self.returns = []
        self.str_name = None
        self.size = 0
        self.round_digits = 4
        self.mean = 0.0
        self.std = 0.0
        self.skew = 0.0
        self.kurt = 0.0
        self.median = 0.0
        self.sharpe = 0.0
        self.var_95 = 0.0
        self.cvar_95 = 0.0
        self.jarque_bera = 0.0
        self.p_value = 0.0
        self.is_normal = 0.0
    
    def __str__(self):
        str_self = self.str_name + ' | size ' + str(self.size) + '\n' + self.plot_str()
        return str_self
        
    def get_data(self):
        self.returns, self.str_name, self.t = static_functions.load_time_series(self.ric)
        self.size = self.t.shape[0]
        
    def compute(self):
        self.size = self.t.shape[0]
        self.mean = np.mean(self.returns) #media
        self.std = np.std(self.returns) #volatility (volatibilidad) en mercados financieros
        self.skew = skew(self.returns)  #Skewness para ver qué tan simétrica es
        self.kurt = kurtosis(self.returns) #Kurtosis para ver qué tantas colas largas tiene
        self.median = np.median(self.returns)
        self.sharpe = self.mean/self.std * np.sqrt(252) #coeficiente de Sharpe (annualised: x_mean crece lineal en el tiempo y x_stdev raíz cuadrada en el tiempo)
        self.var_95 = np.percentile(self.returns,5)  #Valor en riesgo
        self.cvar_95 = np.mean(self.returns[self.returns <= self.var_95]) #CVaR: Valor en riesgo condicional (promedio de pérdidas)
        self.jarque_bera = self.size/6*(self.skew**2 + 1/4*self.kurt**2) #Estadístico Jarque-Bera
        self.p_value = 1-chi2.cdf(self.jarque_bera, df=2) #p-value chi cuadrado símil al JB
        self.is_normal = (self.p_value > 0.05)  #Para saber si la distribución es normal o no.
    
    def plot_str(self):
        plot_str = 'mean ' + str(np.round(self.mean,self.round_digits))\
            + ' | std dev ' + str(np.round(self.std,self.round_digits))\
            + ' | skewness ' + str(np.round(self.skew,self.round_digits))\
            + ' | kurtosis ' + str(np.round(self.kurt,self.round_digits))\
            + ' | Sharpe ratio ' + str(np.round(self.sharpe,self.round_digits)) + '\n'\
            + 'VaR 95% ' + str(np.round(self.var_95,self.round_digits))\
            + ' | CVaR 95% ' + str(np.round(self.cvar_95,self.round_digits))\
            + ' | jarque_bera ' + str(np.round(self.jarque_bera,self.round_digits))\
            + ' | p_value ' + str(np.round(self.p_value,self.round_digits))\
            + ' | is_normal ' + str(self.is_normal)  
        return plot_str
    
class capm_manager():
    
    def __init__(self, ric, benchmark):
        self.nb_decimals = 4
        self.ric=ric
        self.benchmark=benchmark
        self.x = []
        self.y = []
        self.t = pd.DataFrame()
        self.alpha = 0.0
        self.beta = 0.0
        self.p_value = 0.0
        self.null_hypothesis = False
        self.r_value = 0.0
        self.r_squared = 0.0
        self.predictor_linreg = []
        
    def __str__(self):
        str_self =  'linear regression | ric ' + self.ric\
            + ' | benchmark ' + self.benchmark + '\n'\
            + 'alpha (intercept)' + str(self.alpha)\
            + '| beta (slope) ' + str(self.beta) + '\n'\
            + 'p-value ' + str(self.p_value)\
            + ' | null hypothesis ' + str(self.null_hypothesis) + '\n'\
            + 'r-value ' + str(self.r_value)\
            + ' | r-squared ' + str(self.r_squared)
        return str_self
    
    def get_data(self):
        # load timeseries and synchronize them
        self.x, self.y, self.t = static_functions.sinchronize_timeseries(self.ric, self.benchmark)
        
    def compute(self):
        # linear regression of ric with respect to benchmark
        slope, intercept, r_value, p_value, std_err = linregress(self.x, self.y)
        self.beta = np.round(slope, self.nb_decimals)
        self.alpha = np.round(intercept, self.nb_decimals)
        self.p_value = np.round(p_value, self.nb_decimals)
        self.null_hypothesis = p_value > 0.05 # p_value < 0.05 -> reject null hypothesis: alpha=beta=0
        self.r_value = np.round(r_value, self.nb_decimals)
        self.r_squared = np.round(r_value**2, self.nb_decimals)
        self.predictor_linreg = self.alpha + self.beta*self.x
    
    def scatterplot(self):
        # scatterplot of returns
        str_title = 'Scatterplot of returns' + '\n' + self.__str__()
        plt.figure()
        plt.title(str_title)
        plt.scatter(self.x,self.y)
        plt.plot(self.x, self.predictor_linreg, color='green')
        plt.ylabel(self.ric)
        plt.xlabel(self.benchmark)
        plt.grid()
        plt.show()

    def plot_normalised(self):
        # plot 2 timeseries normalised at 100
        price_ric = self.t['price_1']
        price_benchmark = self.t['price_2']
        plt.figure(figsize=(12,5))
        plt.title('Time series of prices | normalised at 100')
        plt.xlabel('Time')
        plt.ylabel('Normalised prices')
        price_ric = 100 * price_ric/price_ric[0]
        price_benchmark = 100 * price_benchmark/price_benchmark[0]
        plt.plot(price_ric, color= 'blue', label=self.ric)
        plt.plot(price_benchmark, color='red', label=self.benchmark)
        plt.legend(loc=0)
        plt.grid()
        plt.show()
        
    def plot_dual_axes(self):
        # plot 2 timeseries 2 vertical axes
        plt.figure(figsize=(12,5))
        plt.title('Time series of prices')
        plt.xlabel('Time')
        plt.ylabel('Prices')
        ax1 = self.t['price_1'].plot(color='blue', grid=True, label=self.ric) # .plot es comando de pandas
        ax2 = self.t['price_2'].plot(color='red', grid=True, secondary_y=True,label=self.benchmark)
        ax1.legend(loc=2)
        ax2.legend(loc=1)
        plt.show()
       
        