# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 13:42:16 2020

@author: matibarri
"""

import numpy as np
import pandas as pd
import matplotlib as mpl
import scipy
import importlib
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, chi2, linregress

# import our own files and reload
import static_functions
importlib.reload(static_functions) #Actualiza los cambios en static_functions
import classes
importlib.reload(classes) 

# input parameters
ric = '^VIX' # MT.AS SAN.MC BBVA.MC REP.MC VWS.CO EQNR.OL MXNUSD=X ^VIX
benchmark = '^S&P500' # ^STOXX ^STOXX50E ^S&P500 ^NASDAQ ^FCHI ^GDAXI

# x , y, t = static_functions.sinchronize_timeseries(ric, benchmark)
capm = classes.capm_manager(ric, benchmark)
capm.get_data()
capm.compute()
capm.scatterplot()
capm.plot_normalised()
capm.plot_dual_axes()
print(capm)


    


