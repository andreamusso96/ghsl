from .. import utils
data_path = f'{utils.data_path}/continents'

def get_continent_geo_file() -> str:
    file_name = f'continents.geojson'
    return f'{data_path}/{file_name}'