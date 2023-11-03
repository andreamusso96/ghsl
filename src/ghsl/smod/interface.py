import xarray as xr
import geopandas as gpd

from .. import enums
from .. import utils

from .data import data


def get_data(year: enums.Year) -> xr.DataArray:
    return data.data(year=year)


def get_tiles_with_degree_of_urbanization_above_threshold(year: enums.Year, degree_of_urbanization_threshold: enums.DegreeOfUrbanization, centroid: bool = True) -> gpd.GeoDataFrame:
    data_ = get_data(year=year)
    stacked_data = data_.stack(z=('x', 'y'))
    degree_urbanization_and_xy_coords_tile_centroid = stacked_data.to_pandas().reset_index()
    degree_urbanization_and_xy_coords_tile_centroid.rename(columns={0: 'degree_of_urbanization'}, inplace=True)
    degree_urbanization_and_xy_coords_tile_centroid = degree_urbanization_and_xy_coords_tile_centroid[degree_urbanization_and_xy_coords_tile_centroid['degree_of_urbanization'] > degree_of_urbanization_threshold.value]
    degree_urbanization_and_xy_coords_tile_centroid.reset_index(drop=True, inplace=True)
    return utils.transform_xy_dataframe_into_geopandas(data=degree_urbanization_and_xy_coords_tile_centroid, centroid=centroid)