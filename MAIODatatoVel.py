#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 09:58:05 2020

@author: tychobovenschen
"""

from IPython import get_ipython
get_ipython().magic('reset -sf')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import pickle

# Load saved files:
file_rollingStd = open('RollingStd.pkl','rb')
RollingStd = pickle.load(file_rollingStd)
file_rollingStd.close()
file_rollingMean = open('RollingMean.pkl','rb')
RollingMean = pickle.load(file_rollingMean)
file_rollingMean.close()
file_Data = open('DataPerYear.pkl', 'rb')
Data = pickle.load(file_Data)
file_Data.close()

# Tresholds for the  filtering:
threshold_lon = 1e-6
threshold_lat = 1e-6

# Plot the filtered data
for key in Data.keys():
    plt.scatter(Data[key]['lon'][50:-50],Data[key]['lat'][50:-50],s=4, label= key) # Laatste punt is bijna altijd slecht omdat RollingStd wordt berekend tot eind-1 dus in plot ook alles tot eind-1
    plt.xlabel('Degrees longitude')
    plt.ylabel('Degrees latitude')
    plt.title('K-Transect #4 '+'threshold_lat='+str(threshold_lat)+', threshold_lon='+str(threshold_lon))
    plt.ticklabel_format(useOffset=False, style='plain')
    plt.legend()
plt.show()

for i in range(1,len(Data)):
    if i == 3:
        i = 4
    test = pd.concat(Data[i])

# for i in range(len(Data)):
#     Data[i].dropna(axis=0,inplace=True)
#     Data[i].reset_index(drop=True,inplace=True)

# for key in range(len(Data))
#     for i in range(len(Data[key]))
#         velocity = Data

