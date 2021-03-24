#!/usr/bin/env python
# coding: utf-8

# In[1]:

import cmocean
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np
import xarray as xr

import platform
import sys

iprocess = int(sys.argv[1])

if platform.system()=='Darwin':
    lowres = True
    print("Use low resolution for macOS")
else:
    lowres = False
    print("Use high resolution for non-macOS")

if lowres:
    xcoord = 'lon'
    ycoord = 'lat'
    res = '360x180'
    #res = '180x90'
    filenames = 'atmf0??.nc.srh.nc.{}.nc'.format(res)
    filenames2 = 'sfcf0??.nc.orog.nc.{}.nc'.format(res)
else:
    #xcoord = 'grid_xt'
    #ycoord = 'grid_yt'
    #filenames = 'atmf0??.nc.srh.nc'
    #filenames2 = 'sfcf0??.nc.orog.nc'
    #
    xcoord = 'lon'
    ycoord = 'lat'
    res = '1440x720'
    #res = '720x360'
    filenames = 'atmf0??.nc.srh.nc.{}.nc'.format(res)
    filenames2 = 'sfcf0??.nc.orog.nc.{}.nc'.format(res)

print(filenames)

ds = xr.open_mfdataset(filenames, combine='by_coords', concat_dim='time')
da = ds['srh03']
print(da.shape)

ds2 = xr.open_mfdataset(filenames2, combine='by_coords', concat_dim='time')
da2 = ds2['orog']
print(da2.shape)

data = da.values
xcoord = ds[xcoord].values
ycoord = ds[ycoord].values

print(np.min(data), np.max(data))
data_transform = np.empty((data.shape[0], data.shape[1], data.shape[2]+1))
data_transform[:,:,0:-1] = data[:,:,:]
data_transform[:,:,-1] = data[:,:,0]

xcoord_transform =  np.empty((xcoord.shape[0]+1,))
xcoord_transform[0:-1] = xcoord[:]
xcoord_transform[-1] = 360.0
print(xcoord_transform)
ycoord_transform =  np.empty((ycoord.shape[0],))
ycoord_transform[:] = ycoord[:]
print(ycoord_transform)

print(data_transform.shape)
print(np.min(data_transform), np.max(data_transform))

data2 = da2.values

from matplotlib.axes import Axes
from cartopy.mpl.geoaxes import GeoAxes
GeoAxes._pcolormesh_patched = Axes.pcolormesh

for i in range(96):

    if not i == iprocess:
        continue

    f = plt.figure(figsize=(28,14))
    #if lowres:
    #    #ax = plt.axes(projection = ccrs.Mollweide(central_longitude=0, globe=None))
    #    ax = plt.axes(projection = ccrs.Robinson(central_longitude=0, globe=None))
    #else:
    ax = plt.axes(projection = ccrs.PlateCarree(central_longitude=0, globe=None))
    ax.set_global()
    ax.coastlines()
    print("Creating plot for time step {}".format(i))

    levels = [ -750 + x*25 for x in range(61) ]
    #if lowres:
    #    cbax2 = ax.contourf(ds[xcoord], ds[ycoord], data_transform[i,:,:], cmap='Blues', transform = ccrs.PlateCarree(), \
    #                        levels = np.array(levels))
    #else:
    cbax2 = ax.contourf(xcoord_transform, ycoord_transform, data_transform[i,:,:], cmap='bwr', levels = np.array(levels))
    
    
    #cbax = ax.pcolormesh(ds[xcoord], ds[ycoord], np.log(1+da[0,:,:]*1e5), cmap='Blues', transform = ccrs.PlateCarree())
    cbar = f.colorbar(cbax2)

    #plt.show()
    if lowres:
        # # DH* TODO - cleanup the Fortran Python index mess
        f.savefig("srh03_{num:02d}.png".format(num=i+1), bbox_inches='tight', dpi=300)
    else:
        f.savefig("srh03_{num:02d}.png".format(num=i+1), bbox_inches='tight', dpi=600)
    del f
    del ax
    del cbax2

    print("Finished creating plot for time step {}".format(i))
