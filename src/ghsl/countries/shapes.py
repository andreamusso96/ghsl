import geopandas as gpd

from .data import data


def get_country_shapes(year: int) -> gpd.GeoDataFrame:
    assert 1886 <= year, "Year must be after 1886"
    if year > 2019:
        print("Warning: Outputting country shapes in 2018")
        year_ = 2018
    else:
        year_ = year

    data_within_years = data.data.loc[(data.data['gwsyear'] <= year_) & (data.data['gweyear'] > year_)].copy()
    country_shapes = data_within_years[['cntry_name', 'gwcode', 'geometry']].copy()
    country_shapes['year'] = year
    country_shapes = country_shapes.rename(columns={'cntry_name': 'country_name', 'gwcode': 'country_code'})
    return country_shapes
