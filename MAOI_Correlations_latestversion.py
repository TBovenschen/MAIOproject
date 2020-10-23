# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 11:24:31 2020

@author: Sander
"""
from IPython import get_ipython
get_ipython().magic('reset -sf')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import pickle
import datetime
from scipy.interpolate import interp1d

#%% Loading velocity files
filename = 'Ktransect-S4'+'_velocity'
file_velocity = open(filename+'.pkl','rb')
velocity_S4 = pickle.load(file_velocity)
velocity_S4 = velocity_S4.astype(float)
filename = 'Ktransect-SHR'+'_velocity'
file_velocity = open(filename+'.pkl','rb')
velocity_SHR = pickle.load(file_velocity)
velocity_SHR = velocity_SHR.astype(float)
filename = 'Ktransect-S7'+'_velocity'
file_velocity = open(filename+'.pkl','rb')
velocity_S7 = pickle.load(file_velocity)
velocity_S7 = velocity_S7.astype(float)
filename = 'Ktransect-S8'+'_velocity'
file_velocity = open(filename+'.pkl','rb')
velocity_S8 = pickle.load(file_velocity)
velocity_S8 = velocity_S8.astype(float)

#%%  In order to correlate, matrices must be same size right? 

S4_masked = np.ma.masked_invalid(velocity_S4)  
S7_masked = np.ma.masked_invalid(velocity_S7)  
S8_masked = np.ma.masked_invalid(velocity_S8)  
SHR_masked = np.ma.masked_invalid(velocity_SHR)  


#%% 


msk = (~S4_masked[:,1].mask & ~S7_masked[:,1].mask)
print(np.ma.corrcoef(S4_masked[msk,1],S7_masked[msk,1]))

msk = (~S4_masked[:,1].mask & ~S8_masked[:,1].mask)
print(np.ma.corrcoef(S4_masked[msk,1],S8_masked[msk,1]))

msk = (~S7_masked[:,1].mask & ~S8_masked[:,1].mask)
print(np.ma.corrcoef(S7_masked[msk,1],S8_masked[msk,1]))
#%% Loading weather data

weatherdata = pd.read_csv('Data/grl_aws06_HOUR-maio.txt', comment ='#',delim_whitespace=(True))
weatherdata = weatherdata[8780:]
S4_masked = S4_masked[:-49]
S7_masked = S7_masked[:-49]
S8_masked = S8_masked[:-49]
corr_weather_S4 = np.ma.corrcoef(S4_masked[~S4_masked[:,1].mask,1],weatherdata['T'][~S4_masked[:,1].mask])
# a = df[val_mask].index

#%%
weatherdata['T'] = weatherdata['T'].mask(weatherdata['T']<-100)
weatherdata['T'] = weatherdata['T'].mask(weatherdata['T']>25) #lower limit of longitude (deterimined visually)

N=100
Temp = np.asarray(weatherdata['T']) 
Temp_masked = np.ma.masked_invalid(Temp)  
Temp_rollingmean = np.ma.convolve(Temp_masked, np.ones((N,))/N, mode='same')
msk = (~S4_masked[:,1].mask & ~Temp_rollingmean.mask)
corr_weather_S4 = np.ma.corrcoef(S4_masked[msk,1],Temp_rollingmean[msk])

plt.figure()
plt.plot(np.arange(len(Temp_rollingmean)),Temp_rollingmean/abs(np.min(Temp_rollingmean)))
plt.plot(np.arange(len(Temp_rollingmean)), S4_masked[:,1]/np.max(S4_masked[:,1]))
plt.show()

weatherdata['M'] = weatherdata['M'].mask(weatherdata['M']<-200)
# meltwire = np.asarray(weatherdata['M'])
# meltwire_masked = np.ma.masked_invalid(meltwire)
plt.figure()
plt.plot(np.arange(len(weatherdata['M'])),weatherdata['M'])

plt.show()

#%%
# window = 240
# RollingMeanT = df['T'].rolling(window).mean()
# #%%
# RollingMeanT = RollingMeanT[240:]
# S4_masked = S4_masked[240:]
# msk = (~S4_masked[:,1].mask)
# print(np.ma.corrcoef(S4_masked[msk,1],RollingMeanT[msk])) 

acceleration = np.zeros(len(S7_masked)-1)
for i in range(len(S7_masked)-1):
    acceleration[i] = (S7_masked[i+1,1] - S7_masked[i,1])
acceleration = np.ma.masked_outside(acceleration,-0.001,0.001)
acceleration = np.ma.convolve(acceleration, np.ones((N,))/N, mode='same')
plt.figure()
plt.plot(np.arange(len(acceleration)),(acceleration-np.nanmin(acceleration))/(np.nanmax(acceleration)-np.nanmin(acceleration)))
plt.plot(np.arange(len(Temp_rollingmean)),(Temp_rollingmean-np.min(Temp_rollingmean))/(np.max(Temp_rollingmean)-np.min(Temp_rollingmean)))
plt.show()
