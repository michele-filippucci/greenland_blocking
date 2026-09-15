import numpy as np
import numpy.ma as ma
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import statistics

region = 'GR'

#compute the two composites
if region == 'EU':
    plon,plat = 10,55 #European Blocking
if region == 'GR':
    plon,plat = -35,70 #Greenland Blocking

#IMPORT DATA

ds = xr.load_dataset("out.nc")
comp_exd = ds['comp_exd_'+region]
comp_kpt = ds['comp_kpt_'+region]
std_exd = ds['std_exd_'+region]
std_kpt = ds['std_kpt_'+region]

lon = ds['lon']
lat = ds['lat']

fig,ax = plt.subplots(nrows=1,ncols=2,figsize=(10,4),subplot_kw={'projection': ccrs.PlateCarree()})
ax.flatten()
titles = ("excluded",
          "retained")

#plot composite
for i,field in enumerate((comp_exd,comp_kpt)):
    field = ma.masked_array(field,field==0)
    if region == 'GR':
        extent =[-100,0,30,90] #Greenland
    if region == 'EU':
        extent =[-40,60,20,90] #Europe    
    ax[i].set_extent(extent, ccrs.PlateCarree())
    ax[i].coastlines(linewidth = 0.6)
    ax[i].plot(plon,plat,'or')
    #ax[i].gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--')
    cont = ax[i].contour(lon,lat,field,
                         colors = 'black',
                         levels = np.arange(4500,6000,40),
                         )
    
    if region == 'EU':
        levels = [5620]
    if region == 'GR':
        levels = [5420]
    
    ax[i].contour(lon,lat,field,
                 colors = 'black',
                 levels=levels,
                 linewidths = 3)
    
    ax[i].set_title(titles[i] + " (" + str(plon) + "E," + str(plat) + "W)")
                         
        
#plot variance
for i,field in enumerate((std_exd,std_kpt)):
    std = ax[i].contourf(lon,lat,field,
                         cmap = 'Reds_r',
                         levels = np.arange(0,240,40))    

fig.subplots_adjust(top=0.88,
                    bottom=0.11,
                    left=0.06,
                    right=0.87,
                    hspace=0.2,
                    wspace=0.135)

cbar_ax = fig.add_axes([0.90,0.25,0.01,0.5])
cbar = plt.colorbar(std, cax=cbar_ax, orientation='vertical',label="std_dev (m)",pad=0.08, aspect=60)

#plt.show()
plt.savefig("/home/mich/plots/POSTER/snapshots/composites_comp_(" + str(plon) + "E," + str(plat) + "W)_"+region,dpi = 400)