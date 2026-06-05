## This code extracts the dynamic topography (surface and CMB), geoid anomaly, gravity anomaly and heat flux data that are calculated using S20RTS.prm and S20RTS.sph found in the cookbook.
## This needs the following input:
## fname = the name of calculated parameter
## dataset = folder where the results are stored
## fileN = subfolders (for different radii, R) in a parent folder for certain degree  
 
## imported libraries 
import pandas as pd
import numpy as np
import os, sys, re
from pathlib import Path

## function that creates a data frame that collates all the data for different radius. 
#The format of the read file is [x,y,z,data]. The fourth column is retrieved, except for the first file.
def concat_data(fname,dataset,fileN):
    tmpstr0 = '\\Output\\' + fname + '.00000'
    folder = fileN[0]
    tmpstr = dataset + folder + tmpstr0 
    data= pd.read_csv(tmpstr, header=0, delim_whitespace=True, usecols=[0,1,2,3], names=['x','y','z',folder])
    
    # a counter to count the folders with R*, so that they will be sorted with rising number in data frame
    count = 1
    for i in range(1,len(fileN)):
        #if 'R' in fileN[i]:
        # use regular expression to check if the folder name starts with R* (* being a number between 0 and 9)
        r = re.compile('^R[0-9]')
        # check if the directory name is exactly R**, with * being a number between 0 and 9
        #r2 = re.compile('^R[0-9]{2}$')
        if r.match(fileN[i]):
            folder = 'R%d' % (count)
            # increase counter by 1 for the next folder that matches the criterium above
            count += 1
        else:
            # if the folder name does not start with R*, use the full folder name
            folder = fileN[i]
        
        tmpstr = dataset + folder + tmpstr0

        datat= pd.read_csv(tmpstr, header=0, delim_whitespace=True, usecols=[3], names=[folder])
        data = pd.concat([data, datat], axis=1)

    tmpstr = dataset + fname + '.txt'

    data.to_csv(tmpstr, sep = ' ', index=False)
    return data

## calculating the maximum, minimum and average values per degree-radius combination
## inputs are: data - the collated dataframe, dataset - folder name, fname - the file name of the input model results
def treated_data(data, fname, dataset):
    data_stats = pd.DataFrame() #creating an empty data frame with a variable name of data_stats
    data_coord = data.iloc[:,0:6]  #getting the coordinates
    data = data.iloc[:,6:]
    
    data_stats['mininum'] = data.min() #creating a column for minimum values with a header of 'minimum'
    data_stats['maximum'] = data.max() # for max values
    data_stats['average'] = data.mean() # for average  values
    diff = data - data.mean();
    data_stats['diff_minimum'] = diff.min()
    data_stats['diff_maximum'] = diff.max()
    data_stats['diff_mean'] = diff.mean()
    data_stats['ind_max'] = diff.idxmax()
    data_stats['ind_min'] = diff.idxmin()
    #creating a path and file name for saving
    tmpstr = dataset + fname + '_treated.txt'

    
    data_stats.to_csv(tmpstr, sep = ' ', index=True)
    
    tmpstr1 = dataset + fname + '_treatedData.txt'

    
    diff = pd.concat([data_coord,diff],axis=1)
    diff.to_csv(tmpstr1, sep = ' ', index=False)
    return



def ToSpherical(fname,dataset):
    pi = 3.1415926
    tmpstr = dataset + fname + '.txt'

    # read in all the data, but exclude the first three columns using iloc (index location)
    df1 = pd.read_csv(tmpstr, header=0, delim_whitespace=True).iloc[:,3:]
    df = pd.read_csv(tmpstr, header=0, delim_whitespace=True, usecols=[0,1,2], names=['x','y','z'])  ## load in raw data
    r = np.sqrt(df["x"]*df["x"] + df["y"]*df["y"] + df["z"]*df["z"])
    lat = np.arcsin(df["z"]/r) #theta, arccos as used in ASPECT
    lon = np.arctan2(df["y"],df["x"]) #phi; in ASPECT this is corrected to (0,360)
    
    df["r"] = r
    df["lat"] = lat*180/pi
    df["lon"] = lon*180/pi


    df = pd.concat([df, df1], axis=1)
    
    df.to_csv(dataset + fname + '_sph.txt', sep = ' ', index=False)

    return df



 
pathname = os.getcwd()

# Calculating for different harmonic degrees
#DegMax = [250,350,450,550,650,750,1050,1350,1650,1850,2450,2845]
DegMax = 1
for j in range(DegMax):#range(len(DegMax)):#
   
    #CHANGE the dataset, which is the path or directory of the data outputted by ASPECT
    dataset = 'deg2Visc_diffR_Deg2dRho_90km_gr4_selfg_Results\\1LEta0\\'
    fileN =next(os.walk(dataset))[1]
    print(dataset)
    print (fileN)
    
    #A. NO SELF-GRAVITATION 
    # for dynamic topography surface
    concat_data('dynamic_topography_surface',dataset,fileN)
    topo_surf = ToSpherical('dynamic_topography_surface',dataset)    
    treated_data(topo_surf,'dynamic_topography_surface',dataset)
    # for dynamic topography bottom
    concat_data('dynamic_topography_bottom',dataset,fileN)
    topo_bot = ToSpherical('dynamic_topography_bottom',dataset)
    treated_data(topo_bot,'dynamic_topography_bottom',dataset)
    # for geoid anomaly
    concat_data('geoid_anomaly',dataset,fileN)
    geoid_anom = ToSpherical('geoid_anomaly',dataset) 
    treated_data(geoid_anom,'geoid_anomaly',dataset)
    # for gravity_anomaly
    concat_data('gravity_anomaly',dataset,fileN)
    gravity_anom = ToSpherical('gravity_anomaly',dataset)
    treated_data(gravity_anom,'gravity_anomaly',dataset) 
    # for CMB geoid anomaly
    concat_data('CMBgeoid_anomaly',dataset,fileN)
    geoid_anom = ToSpherical('CMBgeoid_anomaly',dataset) 
    treated_data(geoid_anom,'CMBgeoid_anomaly',dataset)
    # for CMB gravity_anomaly
    concat_data('CMBgravity_anomaly',dataset,fileN)
    gravity_anom = ToSpherical('CMBgravity_anomaly',dataset)
    treated_data(gravity_anom,'CMBgravity_anomaly',dataset) 
    # for heat flux
    concat_data('heat_flux',dataset,fileN)
    heat_flux = ToSpherical('heat_flux',dataset)
    treated_data(heat_flux,'heat_flux',dataset)
    
    #B. WITH SELF-GRAVITATION
    # for dynamic topography surface
    concat_data('dynamic_topography_surface_selfg',dataset,fileN)
    topo_surf = ToSpherical('dynamic_topography_surface_selfg',dataset)    
    treated_data(topo_surf,'dynamic_topography_surface_selfg',dataset)
    # for dynamic topography bottom
    concat_data('dynamic_topography_bottom_selfg',dataset,fileN)
    topo_bot = ToSpherical('dynamic_topography_bottom_selfg',dataset)
    treated_data(topo_bot,'dynamic_topography_bottom_selfg',dataset)
    # for geoid anomaly
    concat_data('geoid_anomaly_selfg',dataset,fileN)
    geoid_anom = ToSpherical('geoid_anomaly_selfg',dataset) 
    treated_data(geoid_anom,'geoid_anomaly_selfg',dataset)
    # for gravity_anomaly
    concat_data('gravity_anomaly_selfg',dataset,fileN)
    gravity_anom = ToSpherical('gravity_anomaly_selfg',dataset) 
    treated_data(gravity_anom,'gravity_anomaly_selfg',dataset) 
    # for CMB geoid anomaly
    concat_data('CMBgeoid_anomaly_selfg',dataset,fileN)
    geoid_anom = ToSpherical('CMBgeoid_anomaly_selfg',dataset) 
    treated_data(geoid_anom,'CMBgeoid_anomaly_selfg',dataset)
    # for CMB gravity_anomaly
    concat_data('CMBgravity_anomaly_selfg',dataset,fileN)
    gravity_anom = ToSpherical('CMBgravity_anomaly_selfg',dataset)
    treated_data(gravity_anom,'CMBgravity_anomaly_selfg',dataset) 

    
