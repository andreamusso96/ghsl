from .. import utils
from .. import enums

data_path = f'{utils.data_path}/pop'


def get_population_raster_file_path(year: enums.Year) -> str:
    folder = f'{data_path}/GHS_POP_E{year.value}_GLOBE_R2023A_54009_1000_V1_0'
    file_name = f'GHS_POP_E{year.value}_GLOBE_R2023A_54009_1000_V1_0.tif'
    return f'{folder}/{file_name}'

