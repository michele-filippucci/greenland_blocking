#import some basic classes
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.util as cutil
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy import stats

#my own classes
import sys
sys.path.append("/home/mich/prog/Github/AtmBlockPy/lib")
import BlockPlots as BP
import BlockTools as BT

plt.figure(figsize=(16,8))

#coordinates of the point where we look for blocking
plon = -40.0
plat = 70.0

label = 1296

ds = xr.load_dataset("/home/mich/data/Greenland_Blocking/"+\
    "ERA5_northem_2.5x2.5_Z500_daily_1959-2021_jja_DAV_tracked.nc")

output = "/home/mich/prog/summer_greenland_block_prel/snapshots/event_"+str(label)+".png"
#plot the trajectories to see what you are looking at
BP.PlotLabel(ds,
            output,
            label,
            shuffle = True,
            pIB_tracked="pIB_tracked", #name of IB matrix variable, may vary from file to file
            zg="z", #name of zg500 matrix, may vary from file to file
            mapcrs = ccrs.PlateCarree(),
            datacrs = ccrs.PlateCarree(),
            extent =[-180,180,0,90])

plt.savefig(output,bbox_inches='tight',dpi=180)
