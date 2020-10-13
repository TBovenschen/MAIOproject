

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

filename = 'C://Users/Sander/Documents/GitHub/MAIOproject/Ktransect-S4_input.txt'
df = pd.read_csv(filename, comment ='#',delim_whitespace=(True))
df['lon'] = df['lon'].mask(df['lon']<-51)
df['lon'] = df['lon'].mask(df['lon']>-49)
df['lat'] = df['lat'].mask(df['lat'] < 66)
df['lat']  = df['lat'].mask(df['lat'] > 68)
df['lat']  = df['lat'].mask(df['lat'] == 0)

NrJumps = df.nr2.unique()
Data = {elem : pd.DataFrame for elem in NrJumps}

for key in Data.keys():
    Data[key] = df[:][df.nr2 == key]
    

    
RollingMean = {elem : pd.DataFrame for elem in NrJumps}
RollingStd  = {elem : pd.DataFrame for elem in NrJumps}
for key in Data.keys():
    for key in RollingStd.keys():
        RollingStd[key]  = Data[key].rolling(window=1,win_type='boxcar').std()

threshold_lon = 0.0001
threshold_lat = 0.0001

for key in RollingStd.keys():
    for i in range(RollingStd[key].index[0],(len(RollingStd[key]['lon'])-1)):
        if np.abs(RollingStd[key]['lon'][i+1] - RollingStd[key]['lon'][i]) > threshold_lon:
            Data[key]['lon'][i+1] = np.nan 
        if np.abs(RollingStd[key]['lat'][i+1] - RollingStd[key]['lat'][i]) > threshold_lat:
            Data[key]['lat'][i+1] = np.nan
            
for key in Data.keys():
    for key in RollingMean.keys():
        RollingMean[key] = Data[key].rolling(window=60,win_type='boxcar',min_periods = 10).mean()


for key in Data.keys():
    count = Data[key]['lon'].isna().sum()
    
for key in RollingStd.keys():
    plt.scatter(Data[key]['lon'],Data[key]['lat'])
    plt.xlabel('Degrees longitude')
    plt.ylabel('Degrees latitude')
    plt.show()
