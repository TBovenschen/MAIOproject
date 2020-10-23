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
import datetime
from MAOI_function_latestversion import filterdata
from LoctoVel import LoctoVel


filenr = ['S4','SHR','S7','S8'] #The numbers of the stations

#Loop over the stations
for nr in range(len(filenr)):
    filename = 'Data/Ktransect-'+filenr[nr]+'_input.txt' #name of input file
    
    ##### Parameters for the  filtering:######
    threshold_lon = 2e-6
    threshold_lat = 2e-6
    window_std = 60 #window of rolling standard deviation
    obs_nr = 4
    #
    # filterdata(obs_nr, filename, threshold_lon, threshold_lat, window_std)
    # Load saved files:
    file_rollingStd = open(filename+'RollingStd.pkl','rb')
    RollingStd = pickle.load(file_rollingStd)
    file_rollingStd.close()


    file_Data = open(filename+'DataPerYear.pkl', 'rb')
    Data = pickle.load(file_Data)
    file_Data.close()
    
#Plot the location data:
    plt.figure()
    for key in Data.keys():
        plt.scatter(Data[key]['lon'][50:-50],Data[key]['lat'][50:-50],s=4, label= key) # Laatste punt is bijna altijd slecht omdat RollingStd wordt berekend tot eind-1 dus in plot ook alles tot eind-1
    plt.xlabel('Degrees longitude')
    plt.ylabel('Degrees latitude')
    plt.title('K-Transect ' + str(filenr[nr]) + ', threshold = '+str(threshold_lat))
    plt.ticklabel_format(useOffset=False, style='plain')
    plt.legend()
    plt.show()

#Calculate velocities using function LoctoVel
    velocity_all = LoctoVel(Data,filename,240,240)
    

