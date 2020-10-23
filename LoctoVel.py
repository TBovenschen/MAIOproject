#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 09:43:23 2020

@author: tychobovenschen
"""
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt


def LoctoVel(Data,filename, windowGPS, windowVel, save=True, plot=True):
    """Function to calculate the velocities from the GPS data. Velocities are in meters 
    INPUT:      Data:           A dictionary of dataframes sorted per year (output of function filterdata)
                filename:       The name of the input file of the original data
                windowGPS:      The window for the running mean of the location data
                windowVel:      The window for the running mean of the velocity data
                save(optional): Save the data to a pickle file if True (default is True)
                plot (optional): Plot the velocity data if True (default is True)
    OUTPUT:     velocity_all:   A numpy array of all velocities of one station. A running mean is taken over the GPS
                                data, and also over the velocities itself. The velocites are given in m/day"""
    #Drop the nans in the data and reset the index
    for key in Data.keys():
        Data[key].dropna(axis=0,inplace=True)
        Data[key].reset_index(drop=True,inplace=True)
    

    RollingMean = Data.copy() #Copy the data to a new dictionary
# Take the rolling mean of the location data    
    for key in RollingMean.keys():  
        RollingMean[key]['lon']  = Data[key]['lon'].rolling(window=windowGPS,win_type='boxcar').mean() # Only calculate Rollingmean for 'lon'
        RollingMean[key]['lat']  = Data[key]['lat'].rolling(window=windowGPS,win_type='boxcar').mean() # Only calculate Rollingmean for 'lat'

#Drop the nans in the rolling mean
    for key in RollingMean.keys():
        RollingMean[key].dropna(axis=0,inplace=True)
        RollingMean[key].reset_index(drop=True,inplace=True)

# Convert the rollingmeans from degrees to meters:
    for key in RollingMean.keys():
        for i in range(RollingMean[key].index[0],(RollingMean[key].index[0]+len(RollingMean[key]['lon']))):    
            RollingMean[key]['lon'][i] = RollingMean[key]['lon'][i]*(40075017/360*np.cos(67.09/180*np.pi)) # Convert degrees to meters
            RollingMean[key]['lat'][i] = RollingMean[key]['lat'][i]*(40007863/180)                         # Convert degrees to meters

#%% Calculate velocity
    Dates = []
# Copy the rolling mean data to a list with numpy arrays
    Data_listRollingMean = []
    for i in Data.keys():
        Data_listRollingMean.append(np.asarray(RollingMean[i]))
       
#Create an empty list for the velocities    
    velocity = list(range(0,len(Data)))  
                  
    lon = 4 #Assign a name to column number 
    lat = 5 #Assign a name to column number
    
#Calculate the velocities
    for i in range(len(Data_listRollingMean)):  #Loop over the years
        velocity[i] = np.zeros(len(Data_listRollingMean[i])-1)
        for j in range(len(Data_listRollingMean[i])-1): #Loop over data points
            velocity[i][j] = (np.sqrt((Data_listRollingMean[i][j+1,lon]-Data_listRollingMean[i][j,lon])**2+
                        (Data_listRollingMean[i][j+1,lat]-Data_listRollingMean[i][j,lat])**2)/
                          (Data_listRollingMean[i][j+1,0]-Data_listRollingMean[i][j,0]))
        
# Calculate a running mean over the velocities:        
    velocity_mean = list(range(0,len(Data)))  
    N=240 # Window over which averaging occurs 240 = 10 days, 168 = 7 days 
    
    for i in range(len(Data_listRollingMean)):
        velocity_mean[i] = np.convolve(velocity[i], np.ones((N,))/N, mode='valid')
    
    
    for i in range(len(Data)):
        Dates = np.append(Dates,Data_listRollingMean[i][int(N/2):-int(N/2),0])
        
# Store all velocities in 1 array (previously divided per year) and couple them to the corresponding date   
    velocity_all = np.empty(1)
    for i in range(len(velocity_mean)):
        velocity_all = np.append(velocity_all,velocity_mean[i])
        
    velocity_all = np.column_stack((velocity_all[1:],Dates))    
    
# Read original data:
    df = pd.read_csv(filename, comment ='#',delim_whitespace=(True))
    
#  Filling NaNs back into missing data using index as date     
    velocity_all = pd.DataFrame(velocity_all)                    # Create a pd.DataFrame from NumPy array
    new_index = pd.Index(np.arange(0,len(df),1.0))               # Create a new index from first index of velocity_all to last
    velocity_all = velocity_all.set_index([1]).reindex(new_index).reset_index() # Reindex the index of velocity_all with new_index (this automatically fills missing data with nan)
# Convert back to numpy array:
    velocity_all = velocity_all.to_numpy()
    
    # Saving velocities 
    if save==True:
        filename_output = filename[:-10]+'_'
        a = open(filename_output+"velocity.pkl","wb")
        pickle.dump(velocity_all,a)
        
    # Plot the velocities:
    if plot==True:
        plt.figure()
        plt.plot(velocity_all[1:,0],velocity_all[1:,1]*24)
        plt.xlabel('Time')
        plt.ylabel('Velocity [m/day]')
        plt.title('Velocities 2009-2019, K-Transect #'+filename[15:-10])
        plt.show()
    return(velocity_all)


         