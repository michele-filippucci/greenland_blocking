import numpy as np
import numpy.ma as ma
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import statistics

#IMPORT DATA

ds = xr.load_dataset("out2.nc")

comp_kpt = []
zg_an = []

for region in ['EU','GR']:
    comp_kpt.append(ds['comp_kpt_'+region])
    zg_an.append(ds['zg_an_'+region])

lon = ds['lon']
lat = ds['lat']

fig,ax = plt.subplots(nrows=2,ncols=1,figsize=(10,7),subplot_kw={'projection': ccrs.PlateCarree()})
ax.flatten()
titles = ("Europe",
          "Greenland")

#plot composite
for i,field in enumerate(comp_kpt):

    field = ma.masked_array(field,field==0)    
    if i == 0:
        #extent =[-40,60,20,80] #Europe 
        extent = [-180,180,0,90]
        plon,plat = 10,55 #European Blocking
    if i == 1:
        #extent =[-100,0,30,90] #Greenland 
        extent = [-180,180,0,90]
        plon,plat = -35,70 #Greenland Blocking

    ax[i].set_extent(extent, ccrs.PlateCarree())
    ax[i].coastlines(linewidth = 0.6)
    ax[i].plot(plon,plat,'ow')
    #ax[i].gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--')
    #cont = ax[i].contour(lon,lat,field,
    #                     colors = 'black',
    #                     levels = np.arange(4500,6000,40),
    #                     )
    
    if i == 0:
        levels = [5620]
    if i == 1:
        levels = [5420]
    
    ax[i].contour(lon,lat,field,
                 colors = 'black',
                 levels=levels,
                 linewidths = 3)
    
    ax[i].set_title(titles[i] + " (" + str(plon) + "E," + str(plat) + "W)")
                         
        
#plot variance
for i,field in enumerate(zg_an):
    std = ax[i].contourf(lon,lat,field,
                         cmap = 'bwr',
                         levels = np.arange(-180,190,40))    

fig.subplots_adjust(top=0.88,
                    bottom=0.11,
                    left=0.06,
                    right=0.87,
                    hspace=0.2,
                    wspace=0.135)

cbar_ax = fig.add_axes([0.90,0.25,0.01,0.5])
cbar = plt.colorbar(std, cax=cbar_ax, orientation='vertical',label="geopotential heigth anomaly (m)",pad=0.08, aspect=60)

#plt.show()
plt.savefig("/home/mich/plots/POSTER/snapshots/composites_global_(" + str(plon) + "E," + str(plat) + "W)_"+region,dpi = 400)