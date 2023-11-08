import os
from typing import List

import pandas as pd
import rioxarray as rxr
import xarray as xr
import geopandas as gpd
from shapely.geometry import Polygon

data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data')


def open_raster_file(file_path: str) -> xr.DataArray:
    return rxr.open_rasterio(file_path)


def transform_xarray_into_geopandas(data: xr.DataArray, column_name: str, remove_vals: List[int]) -> gpd.GeoDataFrame:
    stacked_xr = data.stack(z=('x', 'y'))
    pandas_df = stacked_xr.to_pandas().reset_index()
    pandas_df.rename(columns={0: column_name}, inplace=True)
    pandas_df = pandas_df.loc[~pandas_df[column_name].isin(set(remove_vals))]
    geometry = gpd.points_from_xy(pandas_df['x'], pandas_df['y'])
    geopandas_df = gpd.GeoDataFrame(pandas_df.drop(columns=['x', 'y']), geometry=geometry, crs='World_Mollweide')
    geopandas_df.reset_index(drop=True, inplace=True)
    return geopandas_df


def get_tiles_intersecting_polygons(polygons: gpd.GeoDataFrame, data: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    polygons_ = polygons.to_crs(data.crs)
    tiles_polygons_join = gpd.sjoin(data, polygons_, how='inner', predicate='intersects')
    tiles_polygons_join.rename(columns={'index_right': 'polygon_id'}, inplace=True)
    return tiles_polygons_join


def get_tiles_within_bounds(data: pd.DataFrame, column: str, lower_bound: int, upper_bound: int) -> gpd.GeoDataFrame:
    mask_ub_lb = (data[column] > lower_bound) & (data[column] <= upper_bound)
    data = data[mask_ub_lb].copy()
    return data


def transform_centroids_into_squares(data: gpd.GeoDataFrame, length_side: float) -> gpd.GeoDataFrame:
    data['geometry'] = data['geometry'].apply(lambda centroid: create_square_from_centroid(centroid.x, centroid.y, length_side=length_side))
    return data


def create_square_from_centroid(x_center: float, y_center: float, length_side: float) -> Polygon:
    half_length_side = length_side / 2
    x_min = x_center - half_length_side
    x_max = x_center + half_length_side
    y_min = y_center - half_length_side
    y_max = y_center + half_length_side
    return Polygon([(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max)])