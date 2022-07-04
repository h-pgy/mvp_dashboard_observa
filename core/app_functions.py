from ntpath import join
import random
import pandas as pd
import geopandas as gpd
import plotly.express as px

from core.config import LIST_INDICADORES_DISTRITO
from core.transform_data import MakeShapefileDistritos

def filtrar_indicador(df, indicador):

    mask = df['Nome']== indicador

    return df[mask].copy()

def filtrar_anos(df, ano):

    mask = df['Período']== ano

    return df[mask].copy()

def join_distritos(df_distritos, shp_distritos):
       
        merged = pd.merge(df_distritos, shp_distritos, how='left', on='ds_nome')
        geodf = gpd.GeoDataFrame(merged, geometry='geometry')

        geodf = geodf.set_crs(epsg='4326')
        geodf.set_index('ds_nome', inplace=True)

        return geodf

def make_map(df_distritos, shp_distritos, indicador, ano):

    data = filtrar_indicador(df_distritos, indicador)
    data = filtrar_anos(data, ano)
    print(f'Building map for {indicador} : {ano} ')
    data = join_distritos(data, shp_distritos)
    fig = px.choropleth(
        data,
        geojson=data.geometry,
        locations=data.index,
        color = 'value',
        color_continuous_scale = 'Blues'
        )
    fig.update_geos(fitbounds="locations", visible=False)

    print('map finished')

    return fig


def inicializar_variaveis(df):

    indicador_inicial = random.choice(LIST_INDICADORES_DISTRITO)
    anos_iniciais = filtrar_indicador(df, indicador_inicial)['Período'].unique()
    ano_inicial = random.choice(anos_iniciais)
    
    return indicador_inicial, anos_iniciais, ano_inicial

