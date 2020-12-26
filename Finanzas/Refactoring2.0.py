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

#input parameters
ric = 'ANTO.L' # ^IXIC DBK.DE CLP=X ANTO.L

# compute risk metrics in class jarque_bera_test

jb = classes.jarque_bera_test(ric)
jb.get_data()
jb.compute()
print(jb)

# plots

static_functions.plot_time_series_price(jb.t, jb.ric)
static_functions.plot_histogram(jb.returns, jb.str_name, jb.plot_str())

