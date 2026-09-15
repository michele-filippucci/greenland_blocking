### Filter composites
# 
# In this notebook we study what is changing of the detected atmospheric blocking

import numpy as np
import numpy.ma as ma
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import statistics


#my own classes
import sys
sys.path.append("/home/mich/prog/Github/AtmBlockPy/lib")
import BlockPlots as BP
import BlockTools as BT


#BASE DATASET
ds = xr.open_dataset("/home/mich/data/Greenland_Blocking/"+\
                     "ERA5_northem_2.5x2.5_Z500_daily_1959-2021_DAV.nc")
pIB_tracked = ds["DAV"]
pIB_tracked_base = xr.where(pIB_tracked>0,1,0)
frequency_base =  np.mean(pIB_tracked_base,axis=0)*100
ds.close()
#FILTERED DATASET
ds = xr.open_dataset("/home/mich/data/Greenland_Blocking/"+\
                     "ERA5_northem_2.5x2.5_Z500_daily_1959-2021_DAV_tracked_pers4_ml28.nc")
pIB_tracked = ds["DAV"]
pIB_tracked_filt = xr.where(pIB_tracked>0,1,0)
frequency_filt =  np.mean(pIB_tracked_filt,axis=0)*100

lon = ds["lon"]
lat = ds["lat"]
zg = ds["zg"]/9.8

ds.close()

print("data successfully read")


#compute the exluded blocked days and the kept blocked days
excluded = pIB_tracked_base - pIB_tracked_filt
kept = pIB_tracked_filt

for region in ('EU','GR'):

    #GREENLAND
    print("Starting Process for composite over " + region)

    #compute the two composites
    if region == 'EU':
        plon,plat = 10,55 #European Blocking
    if region == 'GR':
        plon,plat = -35,70 #Greenland Blocking

    #COMP EXCLUDED
    series_exd = excluded.loc[:,plat,plon]
    list_exd = []
    for t in range(len(zg[:,0,0])):
        if series_exd[t] == 1:
            list_exd.append(zg[t,:,:])
    comp_exd = sum(list_exd) / len(list_exd)
    var_exd = sum([((x - comp_exd) ** 2) for x in list_exd])/len(list_exd)
    std_exd = var_exd**0.5

    #COMP KEPT
    series_kpt = kept.loc[:,plat,plon]
    list_kpt = []
    for t in range(len(zg[:,0,0])):
        if series_kpt[t] == 1:
            list_kpt.append(zg[t,:,:])
    comp_kpt = sum(list_kpt) / len(list_kpt)
    var_kpt = sum([((x - comp_kpt) ** 2) for x in list_kpt])/len(list_kpt)
    std_kpt = var_kpt**0.5

    comp_kpt = xr.DataArray(data=comp_kpt, coords=[lat,lon], dims=['lat','lon'])
    std_kpt = xr.DataArray(data=std_kpt, coords=[lat,lon], dims=['lat','lon'])
    comp_exd = xr.DataArray(data=comp_exd, coords=[lat,lon], dims=['lat','lon'])
    std_exd = xr.DataArray(data=std_exd, coords=[lat,lon], dims=['lat','lon'])
    
    if region == 'EU':
        comp_kpt.name = 'comp_kpt_EU'
        ds = comp_kpt.to_dataset()
    else:
        ds['comp_kpt_GR'] = comp_kpt
        
    ds['comp_exd_'+region] = comp_exd 
    ds['std_kpt_'+region] = std_kpt 
    ds['std_exd_'+region] = std_exd 

print("composites successfully computed")

ds.to_netcdf("out.nc")

print("dataset exported")






