import xarray as xr
import pandas as pd
import geopandas as gpd

from .. import enums
from .. import utils

from .data import data


def get_data(year: enums.Year) -> xr.DataArray:
    return data.data(year=year)


def get_tiles_with_population_above_threshold(year: enums.Year, threshold: int = 0, centroid: bool = True) -> gpd.GeoDataFrame:
    data_ = get_data(year=year)
    stacked_data = data_.stack(z=('x', 'y'))
    population_and_xy_coords_tile_centroid = stacked_data.to_pandas().reset_index()
    population_and_xy_coords_tile_centroid.rename(columns={0: 'population'}, inplace=True)
    population_and_xy_coords_tile_centroid = population_and_xy_coords_tile_centroid[population_and_xy_coords_tile_centroid['population'] > threshold]
    population_and_xy_coords_tile_centroid.reset_index(drop=True, inplace=True)
    return utils.transform_xy_dataframe_into_geopandas(data=population_and_xy_coords_tile_centroid, centroid=centroid)