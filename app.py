import dash
from dash.dependencies import Input, Output
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
import plotly.express as px

from core.config import LIST_INDICADORES_DISTRITO
from core.load_app_data import df_distritos, df_munin, geoseries_dists, boundary_municipio
from core.app_functions import inicializar_variaveis, filtrar_indicador, make_map

external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'MvP ObservaSampa'
server = app.server

indicador_inicial, anos_iniciais, ano_inicial = inicializar_variaveis(df_distritos)

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
                        for ano in anos_iniciais
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
    
    anos = filtrar_indicador(df_distritos, ano)['Período']
    return [{'label': ano, 'value': ano}
            for ano in anos
        ]

@app.callback(
    Output("choropleth", "figure"), 
    [Input("dropdown-indicador", "value"), Input('dropdown-ano', 'value')])
def display_choropleth(indicador, ano):

    return make_map(df_distritos, geoseries_dists, indicador, ano)


app.run_server(debug=True)