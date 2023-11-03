import os

import pandas as pd
import rioxarray as rxr
import xarray as xr
import geopandas as gpd
from shapely.geometry import Polygon

data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data')


def open_raster_file(file_path: str) -> xr.DataArray:
    return rxr.open_rasterio(file_path)


def create_square_from_centroid(x_center: float, y_center: float, length_side: float) -> Polygon:
    half_length_side = length_side / 2
    x_min = x_center - half_length_side
    x_max = x_center + half_length_side
    y_min = y_center - half_length_side
    y_max = y_center + half_length_side
    return Polygon([(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max)])


def transform_xy_dataframe_into_geopandas(data: pd.DataFrame, centroid: bool) -> gpd.GeoDataFrame:
    if centroid:
        geometry = gpd.points_from_xy(data['x'], data['y'])
    else:
        geometry = data.apply(lambda row: create_square_from_centroid(row['x'], row['y'], length_side=1000), axis=1).values

    data = gpd.GeoDataFrame(data.drop(columns=['x', 'y']), geometry=geometry, crs='World_Mollweide')
    return data
