
from IPython import get_ipython
get_ipython().magic('reset -sf')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import pickle

start_time = time.time()


filename = 'Ktransect-S4_input.txt'
df = pd.read_csv(filename, comment ='#',delim_whitespace=(True))
df['lon'] = df['lon'].mask(df['lon']<-51)
df['lon'] = df['lon'].mask(df['lon']>-49)
df['lat'] = df['lat'].mask(df['lat'] < 66)
df['lat']  = df['lat'].mask(df['lat'] > 68)
df['lat']  = df['lat'].mask(df['lat'] == 0)


df.dropna(axis=0,inplace=True)
df.reset_index(drop=True,inplace=True)
#%%
threshold_lon = 1e-6
threshold_lat = 1e-6

###################### USE THIS TO CREATE AND FILTER THE DATA (ONLY FIRST TIME) ################
NrJumps = df.nr2.unique()
Data = {elem : pd.DataFrame for elem in NrJumps}

for key in Data.keys():
    Data[key] = df[:][df.nr2 == key]
    

    
RollingMean = {elem : pd.DataFrame for elem in NrJumps}
RollingStd  = {elem : pd.DataFrame for elem in NrJumps}

for key in RollingStd.keys():
    RollingStd[key]  = Data[key].rolling(window=100,win_type='boxcar').std()



for key in RollingStd.keys():
    for i in range(RollingStd[key].index[0],(RollingStd[key].index[0]+len(RollingStd[key]['lon'])-1)):
        if np.abs(RollingStd[key]['lon'][i+1] - RollingStd[key]['lon'][i]) > threshold_lon:
            Data[key].loc[i+1] = np.nan
        if np.abs(RollingStd[key]['lat'][i+1] - RollingStd[key]['lat'][i]) > threshold_lat:
            Data[key].loc[i+1] = np.nan 

            
for key in RollingMean.keys():
    RollingMean[key] = Data[key].rolling(window=100,win_type='boxcar',min_periods = 10).mean()
f = open("RollingMean.pkl","wb")
pickle.dump(RollingMean,f)
a = open("RollingStd.pkl","wb")
pickle.dump(RollingStd,a)
b = open("DataPerYear.pkl","wb")
pickle.dump(Data,b)
f.close()
a.close()
b.close()

#######################################################################################
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
#%%
# Plot the filtered data
for key in Data.keys():
    plt.scatter(Data[key]['lon'][50:-50],Data[key]['lat'][50:-50],s=4, label= key) # Laatste punt is bijna altijd slecht omdat RollingStd wordt berekend tot eind-1 dus in plot ook alles tot eind-1
    plt.xlabel('Degrees longitude')
    plt.ylabel('Degrees latitude')
    plt.title('K-Transect #4 '+'threshold_lat='+str(threshold_lat)+', threshold_lon='+str(threshold_lon))
    plt.ticklabel_format(useOffset=False, style='plain')
    plt.legend()
plt.show()

# #### Displacements
# Displacement = []
# for key in RollingMean.keys():
#     for i in range(RollingMean[key].index[0],(RollingMean[key].index[0]+len(RollingMean[key]['lon'])-1)):
#         Displacement[key] = RollingMean[key]['lat'] [i+1] - RollingMean[key]['lat'] [i]
#         Displacement[key] = RollingMean[key]['lon'] [i+1] - RollingMean[key]['lon'] [i]

print("--- %s seconds ---" % (time.time() - start_time))

#%%
