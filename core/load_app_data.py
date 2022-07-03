from .utils import solve_path
from .config import APP_DATA_FOLDER

import pandas as pd
import geopandas as gpd



geodf_dists = gpd.read_file(solve_path('geodf_distritos.shp', parent=APP_DATA_FOLDER))
df_munin = pd.read_csv(solve_path('df_municipio.csv', parent=APP_DATA_FOLDER))
boundary_municipio = gpd.read_file(solve_path('limite_municipio.shp', parent=APP_DATA_FOLDER))
