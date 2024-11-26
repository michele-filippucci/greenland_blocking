#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np 
import xarray as xr

#my own classes
import sys
sys.path.append("/emmy-noether/home/mf671/github/blocktrack/lib")
import blocktoolbox as BT
import time
start_time = time.time()


# In[2]:

get_ipython().run_line_magic('cd', '/emmy-noether/home/mf671/DATA/')
get_ipython().system('ls')


# In[ ]:


print("Starting operation")

#'''
data_dir='/emmy-noether/home/mf671/DATA/ERA5/geop/'
fn = data_dir + "ERA5_northem_2.5x2.5_zg500_daily_1940-2023.nc"
work_dic='/emmy-noether/home/mf671/DATA/ERA5/gr_tracking/'
fn_out_unfilt = work_dic + "ERA5_northem_2.5x2.5_zg_MIX_tracked_unfilt_daily_1940-2023.nc"
fn_out = work_dic + "ERA5_northem_2.5x2.5_zg_MIX_tracked_daily_1940-2023.nc"
fn_dic_unfilt = work_dic + "dictionaries/ERA5_northem_2.5x2.5_zg_MIX_tracked_unfilt_daily_1940-2023_DIC.npy"
fn_dic = work_dic + "dictionaries/ERA5_northem_2.5x2.5_zg_MIX_tracked_daily_1940-2023_DIC.npy"
'''
data_dir='/emmy-noether/home/mf671/DATA/ERA5/geop/'
fn = data_dir + "ERA5_northem_2.5x2.5_zg500_daily_1960-1963.nc"
work_dic='/emmy-noether/home/mf671/DATA/ERA5/gr_tracking/'
fn_out_unfilt = work_dic + "ERA5_northem_2.5x2.5_zg_MIX_tracked_unfilt_daily_1960-1963.nc"
fn_out = work_dic + "ERA5_northem_2.5x2.5_zg_MIX_tracked_daily_1960-1963.nc"
fn_dic_unfilt = work_dic + "dictionaries/ERA5_northem_2.5x2.5_zg_MIX_tracked_unfilt_daily_1960-1963_DIC.npy"
fn_dic = work_dic + "dictionaries/ERA5_northem_2.5x2.5_zg_MIX_tracked_daily_1960-1963_DIC.npy"
'''
ds = xr.load_dataset(fn)
print("Data correctly read")
ds = BT.MIX(ds,multiplicative_threshold=1.26,overlap_area=15000)
print(np.amax(ds['MIX_freq']))
print("MIX function correctly executed")
ds,dic_unfilt = BT.ContourTracking2D(ds,var_name = "MIX",overlap=0.5)
#saving temporary data
ds.to_netcdf(fn_out_unfilt)
np.save(fn_dic_unfilt,dic_unfilt)
ds,dic_filt = BT.FilterEvents(ds,dic_unfilt,var_name = "MIX",
                     pers_min = 5,min_avg_area = 2e6,max_avg_dist=700)
print("ContourTracking2D function correclty executed")


# In[ ]:


#saving data
np.save(fn_dic,dic_filt)
ds.to_netcdf(fn_out)
print("Data created")
  
print("--- %s seconds ---" % (time.time() - start_time))


# In[ ]:


dic_filt[0]


# In[ ]:




