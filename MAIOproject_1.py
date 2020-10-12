

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

NrYears = df.nr2.unique()
Data = {elem : pd.DataFrame for elem in NrYears}

for key in Data.keys():
    Data[key] = df[:][df.nr2 == key]
    
## Nu staat de data in een dictionary waarbij ik ze dus heb gesplitst op hun getal in de laatste kolom,
## dus iedere keer dat ze verplaatst zijn in een ander boorgat
    
RollingMean = {elem : pd.DataFrame for elem in NrYears}
RollingStd  = {elem : pd.DataFrame for elem in NrYears}
for key in Data.keys():
    for key in RollingMean.keys():
        RollingMean[key] = Data[key].rolling(window=60,win_type='boxcar',min_periods = 10).mean()
        RollingStd[key]  = Data[key].rolling(window=60,win_type='boxcar',min_periods = 10).std()
     
threshold = 0.1
for key in RollingStd.keys():
    for i in range(len(RollingStd[key])-1):
        if RollingStd[key,i+1] - RollingStd[key,i] > threshold:
            Data[key,i+1] == np.nan
            
## Ik krijg in stukje code hierboven dus errors omdat hij het niet leuk vind als ik probeer te loopen over 
## de dictionary en over de individuele punten van elke dataframe in 1 dictionary. 


        
        
            
