

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
        RollingStd[key]  = Data[key].rolling(window=3,win_type='boxcar').std()

threshold_lon = 0.0001
threshold_lat = 0.00001

for key in RollingStd.keys():
    for i in range(RollingStd[key].index[0],(len(RollingStd[key]['lon'])-1)):
        if np.abs(RollingStd[key]['lon'][i+1] - RollingStd[key]['lon'][i]) > threshold_lon:
           Data[key].loc[i+1] = np.nan
        if np.abs(RollingStd[key]['lon'][i+1] - RollingStd[key]['lon'][i]) == np.nan:
           Data[key].loc[i+1] = np.nan 
        if np.abs(RollingStd[key]['lat'][i+1] - RollingStd[key]['lat'][i]) > threshold_lat:
           Data[key].loc[i+1] = np.nan 
        if np.abs(RollingStd[key]['lat'][i+1] - RollingStd[key]['lat'][i]) == np.nan:
           Data[key].loc[i+1] = np.nan    
            
for key in Data.keys():
    for key in RollingMean.keys():
        RollingMean[key] = Data[key].rolling(window=24,win_type='boxcar',min_periods = 10).mean()


for key in Data.keys():
    count = Data[key]['lon'].isna().sum()
    



for key in Data.keys():
    plt.scatter(Data[key]['lon'][:-1],Data[key]['lat'][:-1])
    plt.xlabel('Degrees longitude')
    plt.ylabel('Degrees latitude')
    plt.title('K-Transect #4')
    
for key in RollingMean.keys():
    plt.scatter(RollingMean[key]['lon'][:-1],RollingMean[key]['lat'][:-1])
    plt.xlabel('Degrees longitude')
    plt.ylabel('Degrees latitude')
    plt.title('K-Transect #4')
     

plt.show()

# Er ligt hier nog 1 behoorlijke outlier maar dat komt doordat de Data rond het window van 24 1 NaN heeft (omdat er een GPS punt buiten de initiele bounds ligt) 
# Hierdoor krijgt het hele window van RollingStd 23 punten met NaNs waardoor de ene outlier er niet uit wordt gehaald want NaN[t+1] - NaN[t] 

