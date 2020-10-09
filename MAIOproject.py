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

file = open(r'Ktransect-S7_input.txt')

df = pd.read_csv(file, comment='#', delim_whitespace=True)

time = np.asarray(df['jday'])
lat = np.asarray(df['lat'])
lon = np.asarray(df['lon'])


latMasked = np.ma.masked_outside(lat,64,71)
lonMasked = np.ma.masked_outside(lon,-50,-49)
latMasked.filled(np.nan)
lonMasked.filled(np.nan)

latmean = np.nanmean(latMasked)
lonmean = np.nanmean(lonMasked)


N = 100
result1 = np.convolve(latMasked, np.ones((N,))/N, mode='valid')

latMasked = np.ma.masked_outside(latMasked,np.nanmean(latMasked)-np.nanstd(latMasked),np.nanmean(latMasked)+np.nanstd(latMasked))
lonMasked = np.ma.masked_outside(lonMasked,np.nanmean(lonMasked)-np.nanstd(lonMasked),np.nanmean(lonMasked)+np.nanstd(lonMasked))

plt.figure()
plt.scatter(lonMasked,latMasked)
plt.show()