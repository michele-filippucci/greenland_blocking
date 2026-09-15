#import some basic classes
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.util as cutil
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from tqdm import tqdm
from scipy import stats

#my own classes
import sys
sys.path.append("/home/mich/prog/Github/AtmBlockPy/lib")
import BlockPlots as BP
import BlockTools as BT

plon,plat=-35.0,70.0 #Greenland
#plon,plat=10.0,55.0 #Scandinavia

plt.rcParams['figure.figsize'] = [5, 9]

feature_dictionaries = np.load("/home/mich/prog/summer_greenland_block_prel/data_tmp/feature_dictionaries_"+str(plon)+"-"+str(plat)+".npy",allow_pickle=True)

def Hist_Matrix_Season(feature_dictionaries,quantity,bin_size_y=5,year_range=(1959,2021)):
    y_array = np.arange(year_range[0],year_range[1]-bin_size_y,bin_size_y)
    seasons_mapping = {
    1: "Winter",
    2: "Spring",
    3: "Spring",
    4: "Spring",
    5: "Summer",
    6: "Summer",
    7: "Summer",
    8: "Autumn",
    9: "Autumn",
    10: "Autumn",
    11: "Winter",
    12: "Winter",
    }
    x_array = ("Winter","Spring","Summer","Autumn")
    arr = np.zeros((len(y_array),len(x_array)))
    for i,x in enumerate(x_array):
        for j,y in enumerate(y_array):
            count = 0
            for item in feature_dictionaries:
                if int(item["year"]) >= y and int(item["year"]) < y + bin_size_y and seasons_mapping[int(item["month"])] == x:
                    count += 1
                    try:
                        arr[j,i] += item[quantity]
                    except:
                        arr[j,i] += 1 #the number of events case
            if quantity != "number_of_events":
                arr[j,i] = arr[j,i]/count
    return x_array,y_array,arr

def Hist_Matrix(feature_dictionaries,quantity,bin_size_x="season",bin_size_y=5,year_range=(1959,2021)):
    y_array = np.arange(year_range[0],year_range[1]-bin_size_y,bin_size_y)
    x_array = np.arange(0,12,bin_size_x)
    arr = np.zeros((len(y_array),len(x_array)))
    for i,x in enumerate(x_array):
        for j,y in enumerate(y_array):
            count = 0
            for item in feature_dictionaries:
                if int(item["year"]) >= y and int(item["year"]) < y + bin_size_y and int(item["month"]) >= x and int(item["month"]) < x + bin_size_x:
                    count += 1
                    try:
                        arr[j,i] += item[quantity]
                    except:
                        arr[j,i] += 1 #the number of events case
            if quantity != "number_of_events":
                arr[j,i] = arr[j,i]/count
    return x_array,y_array,arr


def heatmap(data, row_labels, col_labels, ax = None,
            cbar_kw = {}, cbarlabel = "", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
      ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data,**kwargs,
                  vmin=np.amin(np.abs(data)), vmax=np.max(np.abs(data)))

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax = ax,aspect =50 ,**cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation = -90, va = "bottom")
    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_xticklabels(col_labels,)
    ax.set_yticks(np.arange(data.shape[0]))
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top = True, bottom = False,
                   labeltop = True, labelbottom = False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_yticklabels(), rotation = -30, ha = "right",
             rotation_mode = "anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1] + 1) - 0.5, minor = True)
    ax.set_yticks(np.arange(data.shape[0] + 1) - 0.5, minor = True)
    ax.grid(which = "minor", color = "w", linestyle = '-', linewidth = 3)
    ax.tick_params(which =  "minor", bottom = False, left = False)

    return im, cbar


quantity = "number_of_events"

x,y,data = Hist_Matrix_Season(feature_dictionaries=feature_dictionaries,
                       quantity=quantity,
                       )

# Labels
xlabs = ["Winter","Spring","Summer","Autumn"]
"""
xlabs = []
for month in x:
    xlabs.append(str(month+1))
"""
ylabs = []
for year in y:
    ylabs.append(str(year)+"-"+str(year+5))

fig, ax = plt.subplots()

heatmap(data, row_labels = ylabs, col_labels = xlabs,
        ax = ax, cmap = "viridis", cbarlabel = "number of events")

#plt.title("Greenland",fontsize = 14)

#plt.show()
plt.tight_layout()
plt.savefig("/home/mich/plots/POSTER/heatmaps/"+quantity+"_"+str(plon)+"-"+str(plat)+".png",dpi = 400)
