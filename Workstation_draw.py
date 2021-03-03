import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import shapefile as shp
from netCDF4 import Dataset
import matplotlib.colors as mcolors
from netCDF4 import MFDataset
import imageio
from tqdm import tqdm
def Taiwan_map():
     sf = shp.Reader('World_Countries.shp')

     for shape in sf.shapeRecords():

            l = shape.shape.parts

            len_l = len(l)
            x = [i[0] for i in shape.shape.points[:]]
            y = [i[1] for i in shape.shape.points[:]]
            l.append(len(x))
            for k in range(len_l):

                plt.plot(x[l[k]:l[k + 1]],y[l[k]:l[k + 1]], 'k-')

nc_file_root = 'CCTM_ACONC_v531_gcc_Taiwan_20160101.nc'
nc_geo_root = 'GRIDCRO2D_Taiwan.nc'


data_nc = Dataset(nc_file_root)
data_geo_nc = Dataset(nc_geo_root)
NO2 = data_nc.variables['NO2']
X = data_geo_nc.variables['LON']
Y = data_geo_nc.variables['LAT']

NO2_min = 0
NO2_max = 0
for i in range(np.size(NO2, 0)):

    NO2_min = NO2_min + NO2[i, 0, :, :].min()
    NO2_max = NO2_max + NO2[i, 0, :, :].max()

NO2_min = NO2_min / np.size(NO2, 0)
NO2_max = NO2_max / np.size(NO2, 0)


with tqdm(total=np.size(NO2, 0)) as pbar:
    for i in range(np.size(NO2, 0)):
        
        fig = plt.figure(figsize = (14.5, 8))
        Taiwan_map()

        cmap = plt.cm.rainbow
        cbar_norm = mpl.colors.Normalize(vmin=NO2_min, vmax=NO2_max)
        norm = mcolors.Normalize(vmin=0, vmax=NO2_max)
        cs = plt.contourf(X[0, 0, :, :], Y[0, 0, :, :], NO2[i, 0, :, :], 20, cmap=cmap, norm=norm)
        cs.set_clim(vmin=NO2_min, vmax=NO2_max)
        fig.colorbar(mpl.cm.ScalarMappable(norm= cbar_norm, cmap=cmap))

        #range 
        #plt.xlim(119.5, 122.5)
        #plt.ylim(21.7, 25.5)

        plt.title("CMAQ 2016-1-1 "+ str(i) +":00:00 NO2(ppmV)", fontsize=18)
        Max_value = str(round(NO2[i, 0, :, :].max(), 2))
        Min_value = str(round(NO2[i, 0, :, :].min(), 2))
        plt.xlabel("min = "+Min_value+", "+"max = "+Max_value+" (ppmV)", horizontalalignment='right', fontsize=16)
        plt.tight_layout()
        #plt.show()
        plt.savefig("CMAQ 2016-1-1 "+ str(i) +"hr NO2.png", dpi=200)
        pbar.update(1)
        plt.close()
print('pass')

