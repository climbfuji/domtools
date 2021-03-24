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
    filenames = 'atmf0??.nc.maxvort02.nc.{}.nc'.format(res)
    filenames2 = 'sfcf0??.nc.orog.nc.{}.nc'.format(res)
else:
    #xcoord = 'grid_xt'
    #ycoord = 'grid_yt'
    #filenames = 'atmf0??.nc.maxvort02.nc'
    #filenames2 = 'sfcf0??.nc.orog.nc'
    #
    xcoord = 'lon'
    ycoord = 'lat'
    #res = '1440x720'
    res = '720x360'
    filenames = 'atmf0??.nc.maxvort02.nc.{}.nc'.format(res)
    filenames2 = 'sfcf0??.nc.orog.nc.{}.nc'.format(res)

ds = xr.open_mfdataset(filenames, combine='by_coords', concat_dim='time')
da = ds['maxvort02']
#da.plot()
print(da.shape)
#da[1,:,:].plot()

ds2 = xr.open_mfdataset(filenames2, combine='by_coords', concat_dim='time')
da2 = ds2['orog']
print(da2.shape)

#p = da[1,:,:].plot()# transform=ccrs.PlateCarree())# ,  # the data's projection
            #col='time', col_wrap=1,  # multiplot settings
            #x='grid_xt', y='grid_yt')
#            aspect=ds.dims['grid_xt'] / ds.dims['grid_yt'])  # for a sensible figsize
#            subplot_kws={'projection': map_proj})  # the plot's projection)


#ax = plt.axes(projection=ccrs.Orthographic(central_longitude=0.0, central_latitude=0.0, globe=None))
#ax.set_global()
#da[0].plot(ax=ax, transform=ccrs.Orthographic(central_longitude=0.0, central_latitude=0.0, globe=None), x='grid_xt', y='grid_yt', add_colorbar=False)
#ax.coastlines()
#ax.set_ylim([0,90]);

from matplotlib.axes import Axes
from cartopy.mpl.geoaxes import GeoAxes
GeoAxes._pcolormesh_patched = Axes.pcolormesh

for i in range(96):

    f = plt.figure(figsize=(28,14))
    ax = plt.axes(projection = ccrs.Mollweide(central_longitude=0, globe=None))
    ax.set_global()
    ax.coastlines()
    print("HERE A {}".format(i))
    #cmap = matplotlib.cm.get_cmap(name='Blues')
    #cbax = ax.contourf(ds[xcoord], ds[ycoord], np.log(1+da[0,:,:]*1e5), cmap='cmo.dense', transform = ccrs.PlateCarree())
    #

    data = da.values
    print(np.min(data), np.max(data))
    #data_transform = np.log(1+data*1e5)
    data_transform = data*1e5
    print(data_transform.shape)
    print(np.min(data_transform), np.max(data_transform))
    
    data2 = da2.values
    
    #print(data_transform[i,0,0])
    #print(data_transform[i,-1,-1])
    cbax1 = ax.contourf(ds[xcoord], ds[ycoord], data2[i,:,:], cmap='gray_r', transform = ccrs.PlateCarree())
    #cbax2 = ax.contourf(ds[xcoord], ds[ycoord], data_transform[i,:,:], cmap='Blues', transform = ccrs.PlateCarree(), levels = [ i/4+10 for i in range(80)])
    cbax2 = ax.contourf(ds[xcoord], ds[ycoord], data_transform[i,:,:], cmap='Blues', transform = ccrs.PlateCarree(), \
            levels = np.array([ 9.5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40 ]))
            #levels = np.array([ 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40 ]))
            #levels = np.array([ 9.25, 9.5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 44, 48, 52 ])) # inferno_r, viridis_r
    
    
    
    #cbax = ax.pcolormesh(ds[xcoord], ds[ycoord], np.log(1+da[0,:,:]*1e5), cmap='Blues', transform = ccrs.PlateCarree())
    cbar = f.colorbar(cbax2)

    print("HERE B {}".format(i))
    #plt.show()
    # # DH* TODO - cleanup the Fortran Python index mess
    if lowres:
        f.savefig("maxvort02_{num:02d}.png".format(num=i+1), bbox_inches='tight', dpi=300)
    else:
        f.savefig("maxvort02_{num:02d}.png".format(num=i+1), bbox_inches='tight', dpi=600)
    del f
    del ax
    del cbax1
    del cbax2
    if i==5:
        break
