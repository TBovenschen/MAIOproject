#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 09:54:01 2020

@author: tychobovenschen, Sander Keulers
"""

from IPython import get_ipython
get_ipython().magic('reset -sf')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Read  the data from a file
file = 'Ktransect-S4_input.txt'
df = pd.read_csv(file, comment='#', delim_whitespace=True)

#Store data in numpy arrays
time = np.asarray(df['jday'])
lat = np.asarray(df['lat'])
lon = np.asarray(df['lon'])

#Mask values that are wrongly measured
latMasked = np.ma.masked_outside(lat,67,69)
lonMasked = np.ma.masked_outside(lon,-50.5,-50.1)
latMasked.filled(np.nan)
lonMasked.filled(np.nan)

latMasked = latMasked[~np.isnan(latMasked).any(axis=0)]    
lonMasked = lonMasked[~np.isnan(lonMasked)]   
#%%

#Range to calculate the moving average
N = 100
#Calculate moving averages
lat_mean = np.ma.convolve(latMasked, np.ones((N,))/N, mode='valid')
lon_mean= np.ma.convolve(lonMasked, np.ones((N,))/N, mode='valid')

latMasked = latMasked[int(N/2):int(-N/2+1)]
lonMasked = lonMasked[int(N/2):int(-N/2+1)]
    
latMasked1 = np.ma.masked_where((latMasked < lat_mean-np.ma.std(latMasked)) & 
                                (latMasked > lat_mean+np.ma.std(latMasked)), latMasked)

# latMasked1 = np.ma.filled(latMasked1, np.nan)
# latMasked2 = latMasked1[~np.isnan(latMasked1)]
# latMasked1.compressed()
# lonMasked = np.ma.masked_where(lonMasked,lon_mean-np.nanstd(lonMasked),lon_mean+np.nanstd(lonMasked))
#     if (latMasked[i] < lat_mean[i]-np.nanstd(latMasked)) or (latMasked[i] > lat_mean[i]+np.nanstd(latMasked)):
#         latMasked[i] = np.nan
# latMasked = np.ma.masked_invalid(latMasked)
        
plt.figure()
plt.scatter(lonMasked,latMasked1)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()



