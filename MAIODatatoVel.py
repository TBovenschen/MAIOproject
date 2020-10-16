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

#Convert dataframe to list of arrays
Data_list = []
for i in range(1,len(Data)+2):
    if i == 3:
        continue
    Data_list.append(np.asarray(Data[i]))
    
 
for key in Data.keys():
    Data[key].dropna(axis=0,inplace=True)
    Data[key].reset_index(drop=True,inplace=True)
    
RollingMean = {elem : pd.DataFrame for elem in Data}
for key in RollingMean.keys():
    RollingMean[key] = Data[key]
    RollingMean[key]['lon']  = Data[key]['lon'].rolling(window=240,win_type='boxcar').mean()
    RollingMean[key]['lat']  = Data[key]['lat'].rolling(window=240,win_type='boxcar').mean()

#%%
# for i in range(len(Data)):
#     Data[i].dropna(axis=0,inplace=True)
#     Data[i].reset_index(drop=True,inplace=True)
# for i in range(9):
#     Data_list[i] = np.ma.masked_invalid(Data_list[i])
# for i in range(len(Data_list))
#     for i in range(len(Data[key]))
#         velocity = Data
    
# for i in range(len(Data_list)): 
#     Data_list[i] = Data_list[i][~np.isnan(Data_list).any(axis=0),4]
# test = Data_list[i]
#%% Convert to velocity:
Data_list_meter = Data_list
for i in range(len(Data_list)):
    Data_list_meter[i][:,4] = Data_list[i][:,4]*(40007863/180)
    Data_list_meter[i][:,5] = Data_list[i][:,5]*(40075017/360*np.cos(67.09/180*np.pi))
velocity = [0,1,2,3,4,5,6,7,8]
for i in range(len(Data_list)):
    velocity[i] = np.zeros(len(Data_list[i])-1)
    for j in range(len(Data_list[i])-1):
        velocity[i][j] = np.sqrt((Data_list[i][j+1,4]-Data_list[i][j,4])**2+
                        (Data_list[i][j+1,5]-Data_list[i][j,5])**2)/(Data_list[i][j+1,0]-Data_list[i][j,0])

