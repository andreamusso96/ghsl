from enum import Enum
from typing import Union, List
import geopandas as gpd

from .data import data


class Continent(Enum):
    EUROPE = 'Europe'
    AFRICA = 'Africa'
    ASIA = 'Asia'
    NORTH_AMERICA = 'North America'
    SOUTH_AMERICA = 'South America'
    OCEANIA = 'Oceania'
    ANTARCTICA = 'Antarctica'


def get_continent_shape(continent: Union[Continent, List[Continent]]) -> gpd.GeoDataFrame:
    continent_ = continent if isinstance(continent, list) else [continent]
    continent_shape = data.data[data.data['CONTINENT'].isin([c.value for c in continent_])][['CONTINENT', 'geometry']].copy()
    return continent_shape
