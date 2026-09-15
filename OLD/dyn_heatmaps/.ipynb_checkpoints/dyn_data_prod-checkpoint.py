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

PHASE = 0

#phase 0: find the labels
#phase 1: compute center of mass trajectories
#phase 2: plot trajectories
#phase 3: create dictionary

#coordinates of the point where we look for blocking
#plon,plat=-35.0,70.0 #Greenland
#plon,plat=10.0,55.0 #Europe
plon,plat=-10.0,55.0 #Western Europe

fn = "/home/michele/DATA/ERA5/"+\
    "ERA5_northem_2.5x2.5_Z500_daily_1959-2021_DAV_tracked_pers4_ml28.nc"

#loading dataset
ds = xr.open_dataset(fn)
lons,lats,z,DAV_bool = BP.check_zg_pIB(ds,"zg","DAV_tracked") #this function adds a cyclic point and adjust the
#dimensions of the needed fields.
lonHotSpot = BT.GetIndex(ds,"lon",str(plon))
latHotSpot = BT.GetIndex(ds,"lat",str(plat)) 
DAV_bool = np.ma.masked_equal(DAV_bool,0)#mask array1 when ==0
ds.close()

if PHASE ==0:
    """
    This loop finds the blocking events that cross the specified point
    (plon,plat)
    """
    #create a list of indexes
    indexes = []
    timings = []
    for t,time in tqdm(enumerate(ds["time"].values)):
        for l in np.unique(DAV_bool[t,:,:]):
            if np.all(l==DAV_bool[t:t+4,latHotSpot,lonHotSpot]) and not l in indexes: #DAV_bool[t-1,:,:]:
                indexes.append(l)
                timings.append(t)
    print(len(indexes))
    np.save("/home/michele/DATA/ERA5/data_tmp/indexes_"+str(plon)+"-"+str(plat)+".npy",indexes)
    np.save("/home/michele/DATA/ERA5/data_tmp/timings_"+str(plon)+"-"+str(plat)+".npy",timings)


if PHASE ==1:
    indexes = np.load("/home/michele/DATA/ERA5/data_tmp/indexes_"+str(plon)+"-"+str(plat)+".npy",allow_pickle=True)
    timings = np.load("/home/michele/DATA/ERA5/data_tmp/timings_"+str(plon)+"-"+str(plat)+".npy",allow_pickle=True)
    """
    A list of trajectories is then produced
    """
    xs = []
    ys = []
    areas = []
    for i,l in tqdm(enumerate(indexes)):
        x,y = BT.CenterofMass(DAV_bool,l)
        xs.append(x)
        ys.append(y)
        A = BT.Area(DAV_bool[timings[i],:,:],DAV_bool[timings[i],:,:] == l)
        areas.append(A)
    np.save("/home/michele/DATA/ERA5/data_tmp/xs_"+str(plon)+"-"+str(plat)+".npy",xs)
    np.save("/home/michele/DATA/ERA5/data_tmp/ys_"+str(plon)+"-"+str(plat)+".npy",ys)
    np.save("/home/michele/DATA/ERA5/data_tmp/areas_"+str(plon)+"-"+str(plat)+".npy",areas)

if PHASE == 2:
    xs = np.load("/home/michele/DATA/ERA5/data_tmp/xs_"+str(plon)+"-"+str(plat)+".npy",allow_pickle=True)
    ys = np.load("/home/michele/DATA/ERA5/data_tmp/ys_"+str(plon)+"-"+str(plat)+".npy",allow_pickle=True)
    indexes = np.load("/home/michele/DATA/ERA5/data_tmp/indexes_"+str(plon)+"-"+str(plat)+".npy",allow_pickle=True)
    output = "/home/mich/plots/POSTER/snapshots/trajectories_"+str(plon)+"-"+str(plat)+".png"
    #plot the trajectories to see what you are looking at
    mapcrs = ccrs.PlateCarree()
    datacrs = ccrs.PlateCarree()
    extent =[-120,+100,30,90]
    ax = plt.subplot(111, projection=mapcrs)
    #plt.figure(figsize=(10,4))
    ax.set_extent(extent, datacrs)
    ax.coastlines()
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                    linewidth=2, color='gray', alpha=0.1, linestyle='--')
    for i in range(len(xs)):
        cm = plt.plot(ys[i],xs[i],transform=datacrs)
    plt.text(65, 85, 'n_events='+str(len(xs)), fontsize = 10)
    #i = 50
    #print(indexes[i])
    #cm = plt.plot(ys[i],xs[i],transform=datacrs)
    plt.plot(lons[lonHotSpot],lats[latHotSpot],'ow',transform=datacrs)#transorm=datacrs)
    plt.title("Tracked center of mass of blocking events passing by "+str(plat) +"N"+str(plon)+"W", loc = 'left')

    #plt.show()
    plt.savefig(output,bbox_inches='tight',dpi=400)

if PHASE == 3:
    xs = np.load("/home/michele/DATA/ERA5/data_tmp/xs_"+str(plon)+"-"+str(plat)+".npy",allow_pickle=True)
    ys = np.load("/home/michele/DATA/ERA5/data_tmp/ys_"+str(plon)+"-"+str(plat)+".npy",allow_pickle=True)
    indexes = np.load("/home/michele/DATA/ERA5/data_tmp/indexes_"+str(plon)+"-"+str(plat)+".npy",allow_pickle=True)
    timings = np.load("/home/michele/DATA/ERA5/data_tmp/timings_"+str(plon)+"-"+str(plat)+".npy",allow_pickle=True)
    areas = np.load("/home/michele/DATA/ERA5/data_tmp/areas_"+str(plon)+"-"+str(plat)+".npy",allow_pickle=True)
    #we want to store:
    #-event label: dictionary key
    #-month
    #-year
    #-avg area in lifetime
    #-initial distance from point
    #-final distance from point 
    #-duration
    feature_dictionaries = []
    for i,l in tqdm(enumerate(indexes)):
        event = {"label":l,
                 "month":str(ds["time"].values[timings[i]])[5:7],
                 "year":str(ds["time"].values[timings[i]])[0:4],
                 "avg_area":np.mean(areas[i]),
                 "duration":len(xs[i]),
                 "initial_distance":((plon-xs[i][0])**2+(plat-ys[i][0])**2)**0.5,
                 "final_distance":((plon-xs[i][-1])**2+(plat-ys[i][-1])**2)**0.5,
                 "displacement_lon":plon-ys[i][0],
                 "displacement_lat":plat-xs[i][0]
                 }
        print(event["displacement_lon"])
        feature_dictionaries.append(event)
    np.save("/home/michele/DATA/ERA5/data_tmp/feature_dictionaries_"+str(plon)+"-"+str(plat)+".npy",feature_dictionaries)
        #print(event["duration"])


