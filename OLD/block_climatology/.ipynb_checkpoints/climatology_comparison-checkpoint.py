#!/usr/bin/env python
# coding: utf-8

# ## Climatology Comparison
# In this notebook we compare the climatology of atmospheric blocking with ad without the activation of detection filters

# In[1]:


import numpy as np
import numpy.ma as ma
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


#my own classes
import sys
sys.path.append("/home/mich/prog/Github/AtmBlockPy/lib")
import BlockPlots as BP
import BlockTools as BT


# In[2]:


#BASE DATASET
ds = xr.load_dataset("/home/mich/data/Greenland_Blocking/"+\
                     "ERA5_northem_2.5x2.5_Z500_daily_1959-2021_DAV.nc")
pIB_tracked = ds["DAV"]
pIB_tracked = xr.where(pIB_tracked>0,1,0)
frequency_base =  np.mean(pIB_tracked,axis=0)*100
#FILTERED DATASET
ds = xr.load_dataset("/home/mich/data/Greenland_Blocking/"+\
                     "ERA5_northem_2.5x2.5_Z500_daily_1959-2021_DAV_tracked_pers4_ml28.nc")
pIB_tracked = ds["DAV"]
pIB_tracked = xr.where(pIB_tracked>0,1,0)
frequency_filt =  np.mean(pIB_tracked,axis=0)*100

lon = ds["lon"]
lat = ds["lat"]


# In[ ]:


fig,ax = plt.subplots(nrows=1,ncols=2,figsize=(10,4),subplot_kw={'projection': ccrs.PlateCarree()})
ax.flatten()
titles = ("IB",
         "Lagrangian Tracking")
for i,field in enumerate((frequency_base,frequency_filt)):
    field = ma.masked_array(field,field==0)
    extent =[-100,120,20,90]
    ax[i].set_extent(extent, ccrs.PlateCarree())
    ax[i].coastlines(linewidth = 0.6)
    #ax[i].gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--')
    cont = ax[i].contourf(lon,lat,field,
                          np.arange(0,16,1),
                          extent=[0,90,-180,180],
                          cmap = "Spectral")
    ax[i].set_title(titles[i])
        
cbar_ax = fig.add_axes([0.95,0.25,0.01,0.5])
cbar = plt.colorbar(cont, cax=cbar_ax, orientation='vertical',label="% days",pad=0.08, aspect=60)


plt.show()



# In[ ]:




