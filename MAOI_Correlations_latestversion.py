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

#%% Loading weather data

df = pd.read_csv('Data/grl_aws06_HOUR-maio.txt', comment ='#',delim_whitespace=(True))
val_mask = df['Date'] == '2009/9/3' 
a = df[val_mask].index

#%% 


msk = (~S4_masked[:,1].mask & ~S7_masked[:,1].mask)
print(np.ma.corrcoef(S4_masked[msk,1],S7_masked[msk,1]))

msk = (~S4_masked[:,1].mask & ~S8_masked[:,1].mask)
print(np.ma.corrcoef(S4_masked[msk,1],S8_masked[msk,1]))

msk = (~S7_masked[:,1].mask & ~S8_masked[:,1].mask)
print(np.ma.corrcoef(S7_masked[msk,1],S8_masked[msk,1]))

#%% 
df        = df[8780:]
msk       = msk[:-49]
S4_masked = S4_masked[:-49]
S7_masked = S7_masked[:-49]
S8_masked = S8_masked[:-49]

#%%
window = 240
RollingMeanT = df['T'].rolling(window).mean()
#%%
RollingMeanT = RollingMeanT[240:]
S4_masked = S4_masked[240:]
msk = (~S4_masked[:,1].mask)
print(np.ma.corrcoef(S4_masked[msk,1],RollingMeanT[msk])) 

