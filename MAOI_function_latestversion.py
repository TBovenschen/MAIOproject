
from IPython import get_ipython
get_ipython().magic('reset -sf')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import pickle

def filterdata(obs_nr, filename, threshold_lon, threshold_lat,window_std):
    """Function to load, filter and plot GPS data. Data that has a higher standard deviation
    than the given tresholds is filtered out.
    INPUT: 
    obs_nr:         The number of the observational station on the K-Transect
    filename:       The name of the data file
    threshold_lon:  The threshold in longitude above which the 
                    rolling Std dev has to increase in order to remove the data
    threshol_lat    The threshold in longitude above which the 
                    rolling Std dev has to increase in order to remove the data
    
    OUTPUT:         (the filtered data saved in external files:)
                    filename+RollingStd.pkl 
                    filename+DataPerYear.pkl"""
                    
    # Read Data from file into Pandas and mask the data that is wrong 
    df = pd.read_csv(filename, comment ='#',delim_whitespace=(True))
    df['lon'] = df['lon'].mask(df['lon']<-51) #lower limit of longitude (deterimined visually)
    df['lon'] = df['lon'].mask(df['lon']>-47) #upper limit of longitude (deterimined visually)
    df['lat'] = df['lat'].mask(df['lat'] < 66) #lower limit of latitude (deterimined visually)
    df['lat']  = df['lat'].mask(df['lat'] > 68) #upper limit of longitude (deterimined visually)
    
    #Remove the invalid data points
    df.dropna(axis=0,inplace=True)
    df.reset_index(drop=True,inplace=True)
    #%%
    #The threshold of the difference in the rolling standard deviation after adding a data point:
    
    ###################### USE THIS TO CREATE AND FILTER THE DATA (ONLY FIRST TIME) ################
    #Devide the data in different array for when the station is replaced:
    NrJumps = df.nr2.unique() #Deterimine number of replacements of station
    
    Data = {elem : pd.DataFrame for elem in NrJumps} #Create dictionary
    
    for key in Data.keys():
        Data[key] = df[:][df.nr2 == key] #Divide data in different arrays in a dictionary
        
    
    #Create dictionaries for rolling standard deviation  
    RollingStd  = {elem : pd.DataFrame for elem in NrJumps}
    
    #Compute the rolling standard deviation
    for key in RollingStd.keys():
        RollingStd[key]  = Data[key].rolling(window=window_std,win_type='boxcar').std() 
    
    #Filter out the data that has a bigger standard deviation than the threshold:
    for key in RollingStd.keys():
        for i in range(RollingStd[key].index[0],(RollingStd[key].index[0]+len(RollingStd[key]['lon'])-1)):
            if RollingStd[key]['lon'][i+1] - RollingStd[key]['lon'][i] > threshold_lon:
                Data[key].loc[i+1] = np.nan
            if RollingStd[key]['lat'][i+1] - RollingStd[key]['lat'][i] > threshold_lat:
                Data[key].loc[i+1] = np.nan 
    
                
    #Save the rolling standard deviation data in a file:
    a = open(filename+"RollingStd.pkl","wb")
    pickle.dump(RollingStd,a)
    #Save the data that is divided into different years in a file:
    b = open(filename+"DataPerYear.pkl","wb")
    pickle.dump(Data,b)
    a.close()
    b.close()
    
    #######################################################################################

