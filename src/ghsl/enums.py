from enum import Enum


class Year(Enum):
    """Enum for the years of the GHSL dataset."""
    y1975 = 1975
    y1980 = 1980
    y1985 = 1985
    y1990 = 1990
    y1995 = 1995
    y2000 = 2000
    y2005 = 2005
    y2010 = 2010
    y2015 = 2015
    y2020 = 2020
    y2025 = 2025
    y2030 = 2030


class DegreeOfUrbanization(Enum):
    URBAN_CENTRE = 30
    DENSE_URBAN_CLUSTER = 23
    SEMI_DENSE_URBAN_CLUSTER = 22
    SUBURBAN_OR_PERI_URBAN_CLUSTER = 21
    RURAL_CLUSTER = 13
    LOW_DENSITY_RURAL = 12
    VERY_LOW_DENSITY_RURAL = 11
    WATER = 0
    NO_DATA = -200


