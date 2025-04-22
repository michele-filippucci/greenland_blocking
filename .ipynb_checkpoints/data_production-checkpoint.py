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


get_ipython().run_line_magic('cd', '/emmy-noether/home/mf671/DATA/IFS')
get_ipython().system('ls')


# In[3]:


print("Starting operation")

#'''
data_dir='/emmy-noether/home/mf671/DATA/ERA5/geop/'
fn = data_dir + "ERA5_northem_2.5x2.5_zg500_daily_1940-2023.nc"
work_dic='/emmy-noether/home/mf671/DATA/ERA5/gr_tracking/'
fn_out_unfilt = work_dic + "ERA5_northem_2.5x2.5_zg_DAV_tracked_unfilt_daily_1940-2023.nc"
fn_out = work_dic + "ERA5_northem_2.5x2.5_zg_DAV_tracked_daily_1940-2023.nc"
fn_dic_unfilt = work_dic + "dictionaries/ERA5_northem_2.5x2.5_zg_DAV_tracked_unfilt_daily_1940-2023_DIC.npy"
fn_dic = work_dic + "dictionaries/ERA5_northem_2.5x2.5_zg_DAV_tracked_daily_1940-2023_DIC.npy"
'''
data_dir='/emmy-noether/home/mf671/DATA/ERA5/geop/'
fn = data_dir + "ERA5_northem_2.5x2.5_zg500_daily_1960-1963.nc"
work_dic='/emmy-noether/home/mf671/DATA/ERA5/gr_tracking/'
fn_out_unfilt = work_dic + "ERA5_northem_2.5x2.5_zg_DAV_tracked_unfilt_daily_1960-1963.nc"
fn_out = work_dic + "ERA5_northem_2.5x2.5_zg_DAV_tracked_daily_1960-1963.nc"
fn_dic_unfilt = work_dic + "dictionaries/ERA5_northem_2.5x2.5_zg_DAV_tracked_unfilt_daily_1960-1963_DIC.npy"
fn_dic = work_dic + "dictionaries/ERA5_northem_2.5x2.5_zg_DAV_tracked_daily_1960-1963_DIC.npy"
'''

ds = xr.load_dataset(fn)
print("Data correctly read")
ds = BT.DAV(ds,mer_gradient_filter = True, tyrlis_correction=True)
print(np.amax(ds['DAV_freq']))
print("DAV function correctly executed")
ds,dic_unfilt = BT.ContourTracking2D(ds,var_name = "DAV",max_dist=1000)
#saving temporary data
ds.to_netcdf(fn_out_unfilt)
np.save(fn_dic_unfilt,dic_unfilt)


# In[5]:


from importlib import reload
reload(BT)
ds = xr.load_dataset(fn_out_unfilt)
dic_unfilt = np.load(fn_dic_unfilt,allow_pickle=True)
ds2,dic_filt = BT.FilterEvents(ds,dic_unfilt,var_name = "DAV",
                              pers_min = 5,min_avg_area = 5e5)
print("ContourTracking2D function correclty executed")


# In[6]:


#saving data
np.save(fn_dic,dic_filt)
ds2.to_netcdf(fn_out)
print("Data created")
  
print("--- %s seconds ---" % (time.time() - start_time))


# In[7]:


print(dic_filt[154])

