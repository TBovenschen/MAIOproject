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

start_time = time.time()


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
# for key in Data.keys():
#     plt.scatter(Data[key]['lon'][50:-50],Data[key]['lat'][50:-50],s=4, label= key) # Laatste punt is bijna altijd slecht omdat RollingStd wordt berekend tot eind-1 dus in plot ook alles tot eind-1
#     plt.xlabel('Degrees longitude')
#     plt.ylabel('Degrees latitude')
#     plt.title('K-Transect #4 '+'threshold_lat='+str(threshold_lat)+', threshold_lon='+str(threshold_lon))
#     plt.ticklabel_format(useOffset=False, style='plain')
#     plt.legend()
# plt.show()


## Calculate average standard deviation for every 'year'
# Mean_std = np.array([elem : pd.DataFrame for elem in Data])
# for key in RollingStd.keys():
    # Mean_std[key] = (np.mean((np.mean(RollingStd[1]['lon'])*(40075017/360*np.cos(67.09/180*np.pi)) + np.mean(RollingStd[1]['lat'])*(40007863/180))))

 
for key in Data.keys():
    Data[key].dropna(axis=0,inplace=True)
    Data[key].reset_index(drop=True,inplace=True)
    
RollingMean = {elem : pd.DataFrame for elem in Data}
for key in RollingMean.keys():
    RollingMean[key] = Data[key] # Copy data into Rollingmean
    RollingMean[key]['lon']  = Data[key]['lon'].rolling(window=240,win_type='boxcar').mean() # Only calculate Rollingmean for 'lon'
    RollingMean[key]['lat']  = Data[key]['lat'].rolling(window=240,win_type='boxcar').mean() # Only calculate Rollingmean for 'lat'

for key in RollingMean.keys():
    RollingMean[key].dropna(axis=0,inplace=True)
    RollingMean[key].reset_index(drop=True,inplace=True)

#%% Convert to meters:

for key in RollingMean.keys():
    for i in range(RollingMean[key].index[0],(RollingMean[key].index[0]+len(RollingMean[key]['lon'])-1)):    
        RollingMean[key]['lon'][i] = RollingMean[key]['lon'][i]*(40075017/360*np.cos(67.09/180*np.pi)) # Convert degrees to meters
        RollingMean[key]['lat'][i] = RollingMean[key]['lat'][i]*(40007863/180)                         # Convert degrees to meters

#%% Calculate velocity

Data_listRollingMean = []
for i in range(1,len(RollingMean)+2):
    if i == 3:
        continue
    Data_listRollingMean.append(np.asarray(Data[i]))

    
Velocity = [0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0]                      


                            
# print("--- %s seconds ---" % (time.time() - start_time))
