import dash
from dash.dependencies import Input, Output
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
import plotly.express as px
import random

from core.config import LIST_INDICADORES_DISTRITO
import pandas as pd
from core.load_app_data import geodf_dists, df_munin, boundary_municipio


external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'MvP ObservaSampa'
server = app.server


def filtrar_indicador(df, indicador):

    mask = df['Nome']== indicador

    return df[mask].copy()

def filtrar_anos(df, ano):

    mask = df['Período']== ano

    return df[mask].copy()

def make_map(indicador, ano):

    data = filtrar_indicador(geodf_dists, indicador)
    data = filtrar_anos(data, ano)
    print(f'Building map for {indicador} : {ano} ')
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


indicador_inicial = random.choice(LIST_INDICADORES_DISTRITO)
anos_inicias = filtrar_indicador(geodf_dists, indicador_inicial)['Período'].unique()
ano_inicial = random.choice(anos_inicias)
#map_inicial = make_map(indicador_inicial, ano_inicial)

app.layout = html.Div([
    html.Div(
        children = [
            html.H6("Escolha o indicador"),
            dcc.Dropdown(
                id = 'dropdown-indicador',
                options=[
                        {'label': ind, 'value': ind}
                        for ind in LIST_INDICADORES_DISTRITO
                    ],
                value = indicador_inicial
            ),
            html.H6('Selecione o ano'),
            dcc.Dropdown(
                id = 'dropdown-ano',
                options=[
                        {'label': ano, 'value': ano}
                        for ano in anos_inicias
                    ],
                value = ano_inicial

            )
        ]
    ),
    html.Div([
         dcc.Graph(
            id="choropleth", style = {'display' : 'inline-block','float' : 'left'},
            #figure =map_inicial
         ),
    ]
    )

])


@app.callback(
    dash.dependencies.Output('dropdown-ano', 'options'),
    [dash.dependencies.Input('dropdown-indicador', 'value')])
def update_anos(ano):
    
    anos = filtrar_indicador(geodf_dists, ano)['Período']
    return [{'label': ano, 'value': ano}
            for ano in anos
        ]

@app.callback(
    Output("choropleth", "figure"), 
    [Input("dropdown-indicador", "value"), Input('dropdown-ano', 'value')])
def display_choropleth(indicador, ano):

    return make_map(indicador, ano)


app.run_server(debug=True)