import xarray as xr
import pandas as pd
import geopandas as gpd
import numpy as np

from .. import enums
from .. import utils

from .data import data


def get_data(year: enums.Year) -> gpd.GeoDataFrame:
    return data.data(year=year)


def get_tiles(year: enums.Year, pop_lower_bound: int = 0, pop_upper_bound: int = np.inf, polygons: gpd.GeoDataFrame = None, centroid: bool = True) -> gpd.GeoDataFrame:
    population_and_xy_coords_tile_centroid = get_data(year=year)
    population_and_xy_coords_tile_centroid = utils.get_tiles_within_bounds(data=population_and_xy_coords_tile_centroid, column='population', lower_bound=pop_lower_bound, upper_bound=pop_upper_bound)

    if polygons is not None:
        population_and_xy_coords_tile_centroid = utils.get_tiles_intersecting_polygons(polygons=polygons, data=population_and_xy_coords_tile_centroid)

    else:
        population_and_xy_coords_tile_centroid['polygon_id'] = 0

    if not centroid:
        population_and_xy_coords_tile_centroid = utils.transform_centroids_into_squares(data=population_and_xy_coords_tile_centroid, length_side=1000)

    population_and_xy_coords_tile_centroid.reset_index(drop=True, inplace=True)
    return population_and_xy_coords_tile_centroid
