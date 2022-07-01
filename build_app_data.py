import pickle
from core.utils import solve_path
from core.transform_data import TransformarIndicadores, MakeShapefileDistritos
from core.config import APP_DATA_FOLDER, LIST_INDICADORES_DISTRITO, LIST_INDICADORES_MUNICIPIO

#vou serializar porque o load time é mais rapido
def pickle_data(obj, name, folder = APP_DATA_FOLDER):

    fname = name + '.pi'
    fpath = solve_path(fname, parent = folder)
    
    with open(fpath, 'wb') as f:
        pickle.dump(obj, f)

def build_data():

    t = TransformarIndicadores()
    df_dists = t(LIST_INDICADORES_DISTRITO, filtrar_distrito = True)
    df_munin = t(LIST_INDICADORES_MUNICIPIO, filtrar_distrito = False)
    
    m = MakeShapefileDistritos()
    geodf_dists = m.join_distritos(df_dists)
    boundary_municipio = m.get_city_boundaries()


    pickle_data(geodf_dists, 'geodf_distritos')
    pickle_data(df_munin, 'df_municipio')
    pickle_data(boundary_municipio, 'boundary_municipio')


if __name__ == "__main__":

    build_data()




