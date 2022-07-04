from core.utils import solve_path
from core.transform_data import TransformarIndicadores, MakeShapefileDistritos
from core.config import APP_DATA_FOLDER, LIST_INDICADORES_DISTRITO, LIST_INDICADORES_MUNICIPIO


def build_data():

    t = TransformarIndicadores()
    df_dists = t(LIST_INDICADORES_DISTRITO, filtrar_distrito = True)
    
    df_munin = t(LIST_INDICADORES_MUNICIPIO, filtrar_distrito = False)
    
    m = MakeShapefileDistritos()
    distritos = m.get_distritos()
    boundary_municipio = m.get_city_boundaries()

    distritos.to_file(solve_path('distritos.shp', parent=APP_DATA_FOLDER))
    boundary_municipio.to_file(solve_path('limite_municipio.shp', parent=APP_DATA_FOLDER))

    df_dists.to_csv(solve_path('df_distritos.csv', parent=APP_DATA_FOLDER))
    df_munin.to_csv(solve_path('df_municipio.csv', parent=APP_DATA_FOLDER))

    


if __name__ == "__main__":

    build_data()




