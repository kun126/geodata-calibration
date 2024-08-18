import geopandas as gpd
import numpy as np
import xarray as xr
from shapely.geometry import Polygon

from geodata_calibration.utils import reproj_crop_for_raster, reproj_crop_for_vector


def test_reproj_crop_for_vector():
    """Tests for reproj_crop_for_vector()."""
    pass


def test_reproj_crop_for_raster_da():
    """Tests for reproj_crop_for_raster()."""
    # When target data is xr.core.dataarray.DataArray
    da1 = xr.DataArray(
        np.random.randint(300, size=(3, 3)),
        [
            ("y", [-40.04, -40.07, -40.1], {"id": 1, "y": "y"}),
            ("x", [47.1, 47.15, 47.2], {"id": 1, "x": "x"}),
        ],
    )
    da1.rio.write_crs(4326, inplace=True)

    da2 = xr.DataArray(
        np.random.randint(400, size=(3, 7)),
        [
            (
                "latitude",
                [-40.06, -40.07, -40.08],
            ),
            (
                "longitude",
                [
                    47.13,
                    47.14,
                    47.15,
                    47.16,
                    47.17,
                    47.18,
                    47.19,
                ],
            ),
        ],
    )
    da2.rio.write_crs(3857, inplace=True)
    out = reproj_crop_for_raster(da2, da1)
    assert out.rio.crs == da2.rio.crs
    assert out.x.attrs == {
        "axis": "X",
        "long_name": "x coordinate of projection",
        "standard_name": "projection_x_coordinate",
        "units": "metre",
    }
    assert out.y.attrs == {
        "axis": "Y",
        "long_name": "y coordinate of projection",
        "standard_name": "projection_y_coordinate",
        "units": "metre",
    }
    np.testing.assert_array_equal(out.x, da2.longitude)
    np.testing.assert_array_equal(out.y, da2.latitude)


def test_reproj_crop_for_raster_gdf():
    """Tests for reproj_crop_for_raster()."""
    # When target data is gpd.geodataframe.GeoDataFrame
    x_val, y_val = np.arange(46.5, 48, 0.1), np.arange(-39, -41, -0.1)
    da = xr.DataArray(
        np.random.randint(300, size=(len(y_val), len(x_val))),
        [
            ("y", y_val, {"id": 1, "y": "y"}),
            ("x", x_val, {"id": 1, "x": "x"}),
        ],
    )
    da.rio.write_crs(3857, inplace=True)

    x1, x2, y1, y2 = 46.73, 47.68, -40.58, -40.82
    d = Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
    g = gpd.GeoDataFrame(index=[0], crs="EPSG:3857", geometry=[d])
    out = reproj_crop_for_raster(g, da, resolution=None)

    assert out.rio.crs == g.crs
    assert out.x.attrs == {
        "axis": "X",
        "long_name": "x coordinate of projection",
        "standard_name": "projection_x_coordinate",
        "units": "metre",
    }
    assert out.y.attrs == {
        "axis": "Y",
        "long_name": "y coordinate of projection",
        "standard_name": "projection_y_coordinate",
        "units": "metre",
    }
    assert np.round(out.x[0], 1) == np.round(x1, 1)
    assert np.round(out.x[-1], 1) == np.round(x2, 1)
    assert np.round(out.y[0], 1) == np.round(y1, 1)
    assert np.round(out.y[-1], 1) == np.round(y2, 1)
