"""Utilities"""

import xarray as xr
import rioxarray
import odc.geo.xr
import numpy as np
import geopandas as gpd

def reproj_crop_for_vector(target_file, preproj_file, out_file=False):
    pre, tar = gpd.read_file(preproj_file), gpd.read_file(target_file)
    pre = pre.to_crs(tar.crs)
    pre = gpd.clip(pre, tar)
    if pre['geometry'][0].geom_type == 'Polygon':
        pre['geometry'] = pre['geometry'].buffer(0)
    if out_file:
        pre.to_file(out_file, driver='ESRI Shapefile')
    return pre
    
def reproj_crop_for_raster(target_file, preproj_file, out_file=False, resolution=(100,100)):
    # TD: add func & parameter docstring
    # TD: add lat lon validation
    # TD: add sampling method
    
    if target_file[-3:] == 'tif':
        pre, tar = rioxarray.open_rasterio(preproj_file), rioxarray.open_rasterio(target_file)
        out = pre.rio.reproject_match(tar)
    elif target_file[-3:] == 'shp':
        pre, tar = rioxarray.open_rasterio(preproj_file), gpd.read_file(target_file)         
        out = pre.rio.reproject(
            dst_crs=tar.crs,
            resolution=resolution
            )
        out = out.rio.clip(
            geometries=tar['geometry'], 
            crs=tar.crs,
            all_touched=True,
            from_disk=True
            )
    if out_file:
        out.rio.to_raster(out_file)
    return out