import numpy as np
import xarray as xr

from geodata_calibration.utils import reproj_crop_for_raster, reproj_crop_for_vector


def test_reproj_crop_for_vector():
    """Tests for reproj_crop_for_vector()."""
    pass


def test_reproj_crop_for_raster():
    """Tests for reproj_crop_for_raster()."""
    da1 = xr.DataArray(
        np.random.randint(300, size=(3, 3)),
        [
            ("y", [-40.04, -40.07, -40.1], {"id": 1, "y": "y"}),
            ("x", [47.1, 47.15, 47.2], {"id": 1, "x": "x"}),
        ],
    )
    da1.rio.write_crs(4326, inplace=True)

    da2 = xr.DataArray(
        np.random.randint(400, size=(4, 9)),
        [
            (
                "latitude",
                [-40.05733604, -40.06550543, -40.07367483, -40.08184423],
            ),
            (
                "longitude",
                [
                    47.13010332,
                    47.13827272,
                    47.14644211,
                    47.15461151,
                    47.16278091,
                    47.17095031,
                    47.17911971,
                    47.1872891,
                    47.1954585,
                ],
            ),
        ],
    )
    da2.rio.write_crs(3857, inplace=True)
    resampled = reproj_crop_for_raster(da2, da1)
    da1.rio.reproject_match(da2)
    assert resampled.rio.crs == da2.rio.crs
    assert resampled.x.attrs == {
        "axis": "X",
        "long_name": "x coordinate of projection",
        "standard_name": "projection_x_coordinate",
        "units": "metre",
    }
    assert resampled.y.attrs == {
        "axis": "Y",
        "long_name": "y coordinate of projection",
        "standard_name": "projection_y_coordinate",
        "units": "metre",
    }
    np.testing.assert_array_equal(resampled.x, da2.longitude)
    np.testing.assert_array_equal(resampled.y, da2.latitude)
