from .utils import solve_path
from .config import APP_DATA_FOLDER

import pandas as pd
import geopandas as gpd



geoseries_dists = gpd.read_file(solve_path('distritos.shp', parent=APP_DATA_FOLDER))
boundary_municipio = gpd.read_file(solve_path('limite_municipio.shp', parent=APP_DATA_FOLDER))

df_munin = pd.read_csv(solve_path('df_municipio.csv', parent=APP_DATA_FOLDER))
df_distritos = pd.read_csv(solve_path('df_distritos.csv', parent=APP_DATA_FOLDER))
