# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 01:45:15 2020

@author: matibarri
"""

import numpy as np
import pandas as pd
import matplotlib as mpl
import scipy
import importlib
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, chi2

def load_time_series(ric, file_extension='csv'):
    
    # get market data
    # remember to modify the path to match your own directory
    path = 'C:\\Users\matis\\OneDrive - Universidad de Concepción\\Notebooks\\Programacion\\Finanzas\\' + ric + '.' + file_extension
    if file_extension == 'csv':
        table_raw = pd.read_csv(path)
        
    else: 
        table_raw = pd.read_excel(path)
    # create table of returns
    t = pd.DataFrame()
    t['date'] = pd.to_datetime(table_raw['Date'], dayfirst=True)
    t['close'] = table_raw['Close']
    t.sort_values(by='date', ascending=True)
    t['close_previous'] = t['close'].shift(1)
    t['return_close'] = t['close']/t['close_previous'] -1
    t = t.dropna()
    t = t.reset_index(drop=True) 
    x = t['return_close'].values # returns
    x_str = 'Real returns ' + ric # label e.g. ric
    
    
    return x, x_str, t

def plot_time_series_price(t, ric):
    
    #plot timeseries of prices
    plt.figure()
    plt.plot(t['date'],t['close'])
    plt.title('Time series real prices ' + ric)
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.show()
    
def plot_histogram(x, x_str, plot_str, bins=100):
    
    ##plot histogram (Distribucion de rendimientos/ganancias y pérdidas)
    plt.figure() #genera la figura
    plt.hist(x) #crea el histograma y bins adelgaza las "barritas"
    plt.title('Histogram ' + x_str)
    plt.xlabel(plot_str)
    plt.show() #muestra la figura
    
def sinchronize_timeseries(ric, benchmark, file_extension='csv'):
    # loading data from CSV or Excel file
    x1, str1, t1 = load_time_series(ric, file_extension)
    x2, str2, t2 = load_time_series(benchmark, file_extension)
    
    # synchronize timestamps
    timestamp1 = list(t1['date'].values)
    timestamp2 = list(t2['date'].values)
    timestamps = list(set(timestamp1) & set(timestamp2))
    
    # synchronised time series for x1 or ric
    t1_sync = t1[t1['date'].isin(timestamps)]
    t1_sync.sort_values(by='date', ascending=True)
    t1_sync = t1_sync.reset_index(drop=True)
    
    # synchronised time series for x2 or benchmark
    t2_sync = t2[t2['date'].isin(timestamps)]
    t2_sync.sort_values(by='date', ascending=True)
    t2_sync = t2_sync.reset_index(drop=True)
    
    # table of returns for ric and benchmark
    t = pd.DataFrame()
    t['date'] = t1_sync['date']
    t['price_1'] = t1_sync['close']
    t['price_2'] = t2_sync['close']
    t['return_1'] = t1_sync['return_close']
    t['return_2'] = t2_sync['return_close']
    
    # compute vectors of returns
    x = t['return_1'].values
    y = t['return_2'].values
    
    return x,y,t
        