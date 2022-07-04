import dash
from dash.dependencies import Input, Output
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash import dash_table
import plotly.express as px

from core.config import LIST_INDICADORES_DISTRITO
from core.load_app_data import df_distritos, df_munin, geoseries_dists, boundary_municipio
from core.app_functions import make_map, make_table, make_mulher_x_homens_graph, make_indice_envelhecimento_graph

external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'MvP ObservaSampa'
server = app.server

ANOS = list(range(2000, 2021))
ANO_INICIAL = 2020

app.layout = html.Div([
    html.Div(children= [
         dcc.Graph(
            id="choropleth", 
            style = {'display' : 'inline-block','float' : 'left'},
         ),
            html.H6('Selecione o ano'),
            dcc.Dropdown(
                id = 'dropdown-ano',
                options=[
                        {'label': ano, 'value': ano}
                        for ano in ANOS
                    ],
                value = ANO_INICIAL

            ),
         dash_table.DataTable(id='data-table', 
            editable=False, 
            column_selectable=False,
            page_action="native",
            page_current= 0,
            page_size= 10,)
        ]),
    html.Div(children=[
        dcc.Graph(id="graph-mulher-x-homem",
        figure = make_mulher_x_homens_graph(df_munin)
        ),
        dcc.Graph(id='graph-envelhecimento-ano',
        figure = make_indice_envelhecimento_graph(df_munin)
        )
    ]
    )
    ])

@app.callback(
    Output("choropleth", "figure"), 
    [Input('dropdown-ano', 'value')])
def display_choropleth(ano):

    return make_map(df_distritos, geoseries_dists, "População total", ano, 
                    f'População por distrito {ano}')

@app.callback(
    Output("data-table", "data"),
    [Input('dropdown-ano', 'value')])
def display_table(ano):

    cols = ['Região', 'Período', 'Resultado']
    data = make_table(df_distritos, ano, "População total", cols = cols)
    return data


app.run_server(debug=True)