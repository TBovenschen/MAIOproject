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

filenr = ['S4','SHR','S7','S8'] 
for nr in range(len(filenr)):
    start_time = time.time()
    filename = 'Data/Ktransect-'+filenr[nr]+'_input.txt'
    # Tresholds for the  filtering:
    threshold_lon = 2e-6
    threshold_lat = 2e-6
    window_std = 60
    obs_nr = 4
    filterdata(obs_nr, filename, threshold_lon, threshold_lat, window_std)
    # Load saved files:
    file_rollingStd = open(filename+'RollingStd.pkl','rb')
    RollingStd = pickle.load(file_rollingStd)
    file_rollingStd.close()


    file_Data = open(filename+'DataPerYear.pkl', 'rb')
    Data = pickle.load(file_Data)
    file_Data.close()
    

    plt.figure()
    for key in Data.keys():
        plt.scatter(Data[key]['lon'][50:-50],Data[key]['lat'][50:-50],s=4, label= key) # Laatste punt is bijna altijd slecht omdat RollingStd wordt berekend tot eind-1 dus in plot ook alles tot eind-1
    plt.xlabel('Degrees longitude')
    plt.ylabel('Degrees latitude')
    plt.title('K-Transect ' + str(filenr[nr]) + ', threshold = '+str(threshold_lat))
    plt.ticklabel_format(useOffset=False, style='plain')
    plt.legend()
    plt.show()

#%%

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
        for i in range(RollingMean[key].index[0],(RollingMean[key].index[0]+len(RollingMean[key]['lon']))):    
            RollingMean[key]['lon'][i] = RollingMean[key]['lon'][i]*(40075017/360*np.cos(67.09/180*np.pi)) # Convert degrees to meters
            RollingMean[key]['lat'][i] = RollingMean[key]['lat'][i]*(40007863/180)                         # Convert degrees to meters

#%% Calculate velocity

    Data_listRollingMean = []
    Dates = []
    Dates2 = []
    for i in Data.keys():
        Data_listRollingMean.append(np.asarray(Data[i]))
       
    
    velocity = list(range(0,len(Data)))                    
    lon = 4
    lat = 5
    for i in range(len(Data_listRollingMean)):
        velocity[i] = np.zeros(len(Data_listRollingMean[i])-1)
        for j in range(len(Data_listRollingMean[i])-1):
            velocity[i][j] = (np.sqrt((Data_listRollingMean[i][j+1,lon]-Data_listRollingMean[i][j,lon])**2+
                        (Data_listRollingMean[i][j+1,lat]-Data_listRollingMean[i][j,lat])**2)/
                          (Data_listRollingMean[i][j+1,0]-Data_listRollingMean[i][j,0]))
            
    velocity_mean = list(range(0,len(Data)))  
    
    N=240 # Window over which averaging occurs 240 = 10 days, 168 = 7 days 
    for i in range(len(Data_listRollingMean)):
        velocity_mean[i] = np.convolve(velocity[i], np.ones((N,))/N, mode='valid')
    
    
    for i in range(len(Data)):
        Dates = np.append(Dates,Data_listRollingMean[i][int(N/2):-int(N/2),0])
        
    
    velocity_all = np.empty(1)
    for i in range(len(velocity_mean)):
        velocity_all = np.append(velocity_all,velocity_mean[i])
        
    velocity_all = np.column_stack((velocity_all[1:],Dates))     # Create array of all velocities stacked next to the Dates
    
#%%
    df = pd.read_csv(filename, comment ='#',delim_whitespace=(True))
    
#%%  Filling NaNs back into missing data using index as date     

    velocity_all = pd.DataFrame(velocity_all)                    # Create a pd.DataFrame from NumPy array
    new_index = pd.Index(np.arange(0,len(df),1.0))               # Create a new index from first index of velocity_all to last
    velocity_all = velocity_all.set_index([1]).reindex(new_index).reset_index() # Reindex the index of velocity_all with new_index (this automatically fills missing data with nan)

    velocity_all = velocity_all.to_numpy()                       # Convert pd.dataframe back into np.array :) 



#%%
    plt.figure()
    plt.plot(velocity_all[1:,0],velocity_all[1:,1]*24)
    plt.xlabel('Time')
    plt.ylabel('Velocity [m/day]')
    plt.title('Velocities 2009-2019, K-Transect #'+str(filenr[nr]))
    plt.show()                            



#%% Saving velocities 
    
    filename_output = 'Ktransect-'+filenr[nr]+'_'
    a = open(filename_output+"velocity.pkl","wb")
    pickle.dump(velocity_all,a)
    
    
print("--- %s seconds ---" % (time.time() - start_time))
