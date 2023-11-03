import xarray as xr

from .. import utils
from .. import enums
from . import config


# Lazy loading
class Data:
    def __init__(self):
        self._data = None
        self._year = None

    def data(self, year: enums.Year) -> xr.DataArray:
        if self._data is None or self._year != year:
            self._data = utils.open_raster_file(config.get_settlement_raster_file_path(year=year))
            self._data = self._data.squeeze(dim='band', drop=True)
        return self._data


data = Data()