import xarray as xr
import geopandas as gpd

from .. import enums
from .. import utils

from .data import data


def get_data(year: enums.Year) -> gpd.GeoDataFrame:
    return data.data(year=year)


def get_tiles(year: enums.Year, lower_bound: enums.DegreeOfUrbanization = enums.DegreeOfUrbanization.LOW_DENSITY_RURAL, upper_bound: enums.DegreeOfUrbanization = enums.DegreeOfUrbanization.URBAN_CENTRE, polygons: gpd.GeoDataFrame = None, centroid: bool = True) -> gpd.GeoDataFrame:
    degree_urbanization_and_xy_coords_tile_centroid = get_data(year=year)
    degree_urbanization_and_xy_coords_tile_centroid = utils.get_tiles_within_bounds(data=degree_urbanization_and_xy_coords_tile_centroid, column='degree_of_urbanization', lower_bound=lower_bound.value, upper_bound=upper_bound.value)
    if polygons is not None:
        degree_urbanization_and_xy_coords_tile_centroid = utils.get_tiles_intersecting_polygons(polygons=polygons, data=degree_urbanization_and_xy_coords_tile_centroid)

    if not centroid:
        degree_urbanization_and_xy_coords_tile_centroid = utils.transform_centroids_into_squares(data=degree_urbanization_and_xy_coords_tile_centroid, length_side=1000)

    degree_urbanization_and_xy_coords_tile_centroid.reset_index(drop=True, inplace=True)
    return degree_urbanization_and_xy_coords_tile_centroid
