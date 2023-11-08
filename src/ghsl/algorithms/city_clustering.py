import pandas as pd
import geopandas as gpd
import numpy as np
from sklearn.cluster import DBSCAN
import scipy

from .. import enums
from .. import pop
from .. import smod


def get_city_clusters_with_population(year: enums.Year, lower_bound_urbanization: enums.DegreeOfUrbanization = enums.DegreeOfUrbanization.SUBURBAN_OR_PERI_URBAN_CLUSTER,
                                      upper_bound_urbanization: enums.DegreeOfUrbanization = enums.DegreeOfUrbanization.URBAN_CENTRE,
                                      lower_bound_pop: int = 0, upper_bound_pop: int = np.inf, polygons: gpd.GeoDataFrame = None,
                                      eps_db_scan_km: float = 1.5, min_nbrs_db_scan: int = 2):
    clustered_tiles_with_population = get_clustered_tiles_with_population(year=year, lower_bound_urbanization=lower_bound_urbanization, upper_bound_urbanization=upper_bound_urbanization, polygons=polygons, eps_db_scan_km=eps_db_scan_km, min_nbrs_db_scan=min_nbrs_db_scan,
                                                                          lower_bound_pop=lower_bound_pop, upper_bound_pop=upper_bound_pop)
    city_clusters = clustered_tiles_with_population.dissolve(by='cluster', aggfunc={'population': 'sum', 'degree_of_urbanization': 'max', 'polygon_id': lambda x: scipy.stats.mode(x)[0]})
    city_clusters.drop(index=-1, inplace=True)
    city_clusters.reset_index(inplace=True)
    return city_clusters


def get_clustered_tiles_with_population(year: enums.Year, lower_bound_urbanization: enums.DegreeOfUrbanization = enums.DegreeOfUrbanization.SUBURBAN_OR_PERI_URBAN_CLUSTER,
                                        upper_bound_urbanization: enums.DegreeOfUrbanization = enums.DegreeOfUrbanization.URBAN_CENTRE,
                                        lower_bound_pop: int = 0, upper_bound_pop: int = np.inf, polygons: gpd.GeoDataFrame = None,
                                        eps_db_scan_km: float = 1.5, min_nbrs_db_scan: int = 2):
    clustered_tiles = get_clustered_tiles(year=year, lower_bound_urbanization=lower_bound_urbanization, upper_bound_urbanization=upper_bound_urbanization, polygons=polygons, eps_db_scan_km=eps_db_scan_km, min_nbrs_db_scan=min_nbrs_db_scan)
    population_and_centroids = pop.get_tiles(year=year, pop_lower_bound=lower_bound_pop, pop_upper_bound=upper_bound_pop, polygons=polygons, centroid=True)
    population_and_centroids.to_crs(clustered_tiles.crs, inplace=True)
    clustered_tiles_with_population = clustered_tiles.sjoin(population_and_centroids, how='inner', predicate='contains')
    clustered_tiles_with_population.drop(columns=['index_right', 'polygon_id_right'], inplace=True)
    clustered_tiles_with_population.rename(columns={'polygon_id_left': 'polygon_id'}, inplace=True)
    return clustered_tiles_with_population


def get_clustered_tiles(year: enums.Year, lower_bound_urbanization: enums.DegreeOfUrbanization = enums.DegreeOfUrbanization.SUBURBAN_OR_PERI_URBAN_CLUSTER,
                        upper_bound_urbanization: enums.DegreeOfUrbanization = enums.DegreeOfUrbanization.URBAN_CENTRE,
                        polygons: gpd.GeoDataFrame = None, eps_db_scan_km: float = 1.5, min_nbrs_db_scan: int = 2):
    tiles = smod.get_tiles(year=year, polygons=polygons, lower_bound=lower_bound_urbanization, upper_bound=upper_bound_urbanization, centroid=False)
    centroids = gpd.GeoDataFrame(geometry=tiles.centroid, crs=tiles.crs)
    clustered_centroids = cluster_cities_given_tile_centroids(tile_centroids=centroids, eps_db_scan_km=eps_db_scan_km, min_nbrs_db_scan=min_nbrs_db_scan)
    tiles['cluster'] = clustered_centroids['cluster']
    return tiles


def cluster_cities_given_tile_centroids(tile_centroids: gpd.GeoDataFrame, eps_db_scan_km: float, min_nbrs_db_scan: int):
    tile_centroids_ = tile_centroids.to_crs('EPSG:4326')

    # Here it is fundamental to use the inverted coordinates. Indeed, the first coordinate geopandas stores points as longitude, latitude (x, y) while the clustering algorithm expects latitude, longitude
    tile_centroids_lat_lon = pd.DataFrame([tile_centroids_.geometry.y, tile_centroids_.geometry.x], index=['lat', 'lon']).T

    # Need to convert to radians for the clustering algorithm
    tile_centroids_radians = np.radians(tile_centroids_lat_lon).values
    km_per_radian = 6371.0088
    eps = eps_db_scan_km / km_per_radian

    clustering_algorithm = DBSCAN(eps=eps, min_samples=min_nbrs_db_scan, algorithm='ball_tree', metric='haversine')
    clustering_algorithm.fit(tile_centroids_radians)
    tile_centroids['cluster'] = clustering_algorithm.labels_
    return tile_centroids
