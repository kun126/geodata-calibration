"""Utilities"""

import geopandas as gpd
import numpy as np
import odc.geo.xr
import rioxarray
import xarray as xr


def reproj_crop_for_vector(target_data, preproj_data, out_file=False):
    pre = preproj_data.to_crs(target_data.crs)
    pre = gpd.clip(preproj_data, target_data)
    if preproj_data["geometry"][0].geom_type == "Polygon":
        preproj_data["geometry"] = preproj_data["geometry"].buffer(0)
    if out_file:
        preproj_data.to_file(out_file, driver="ESRI Shapefile")
    return preproj_data


def reproj_crop_for_raster(
    target_data, preproj_data, out_file=False, resolution=(100, 100)
):
    # TD: add func & parameter docstring
    # TD: add lat lon validation
    # TD: add sampling method

    if type(target_data) == xr.core.dataarray.DataArray:
        out = preproj_data.rio.reproject_match(target_data)
    elif type(target_data) == gpd.geodataframe.GeoDataFrame:
        out = preproj_data.rio.reproject(dst_crs=target_data.crs, resolution=resolution)
        out = out.rio.clip(
            geometries=target_data["geometry"],
            crs=target_data.crs,
            all_touched=True,
            from_disk=True,
        )
    if out_file:
        out.rio.to_raster(out_file)
    return out
