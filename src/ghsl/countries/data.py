import geopandas as gpd

from . import config


# Lazy loading
class Data:
    def __init__(self):
        self._data = None

    @property
    def data(self) -> gpd.GeoDataFrame:
        if self._data is None:
            self._data = gpd.read_file(config.get_country_border_change_file())
        return self._data


data = Data()
