from locale import dcgettext
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

def make_map(df_distritos, shp_distritos, indicador, ano, title):

    data = filtrar_indicador(df_distritos, indicador)
    data = filtrar_anos(data, ano)
    print(f'Building map for {indicador} : {ano} ')
    data = join_distritos(data, shp_distritos)
    fig = px.choropleth(
        data,
        geojson=data.geometry,
        locations=data.index,
        color = 'value',
        color_continuous_scale = 'Blues',
        title = title
        )
    fig.update_geos(fitbounds="locations", visible=False)

    print('map finished')

    return fig

def make_table(df_distritos, ano, indicador, cols):

    df = filtrar_indicador(df_distritos, indicador)
    df = filtrar_anos(df, ano)

    df = df[cols]

    df = df.to_dict('records')

    return df

def make_mulher_x_homens_graph(df_municipio):

    mulheres = filtrar_indicador(df_municipio, 'População total - mulheres')
    homens = filtrar_indicador(df_municipio, 'População total - homens')

    data = pd.concat([mulheres, homens])

    figure = px.bar(data, x="Período", y="value", 
                 color="Nome", barmode="group",
                 title = 'População por sexo por ano')
    
    return figure


def make_indice_envelhecimento_graph(df_municipio):

    df = filtrar_indicador(df_municipio, 'Índice de envelhecimento')

    figure = px.bar(df, x = 'Período', y='value', title='Índice de envelhecimento por ano')

    return figure
    

