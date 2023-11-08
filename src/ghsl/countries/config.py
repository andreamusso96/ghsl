
from .. import utils

data_path = f'{utils.data_path}/countries'


def get_country_border_change_file() -> str:
    folder = f'{data_path}/CShapes-2.0'
    file_name = f'CShapes-2.0.shp'
    return f'{folder}/{file_name}'



