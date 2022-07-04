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

from core.app_layout import navbar


#objetos com estilo customizado tem que vir depois do import do tema
external_stylesheets = [dbc.themes.LUX]



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'MvP ObservaSampa'
server = app.server

ANOS = list(range(2000, 2021))
ANO_INICIAL = 2020

app.layout = html.Div([
    dbc.Row(navbar),
    dbc.Row(
        [
            dbc.Col(html.H6(f"População total: {100000}")),
            dbc.Col(html.H6(f"Razão de sexos: {100000}")),
            dbc.Col(html.H6(f"Área do Município: {100000}"))
        ]
    ),
    dbc.Row(children= [
        dbc.Col(
            [
         dbc.Row([
            html.H6('Selecione o ano'),
            dcc.Dropdown(
                id = 'dropdown-ano',
                options=[
                        {'label': ano, 'value': ano}
                        for ano in ANOS
                    ],
                value = ANO_INICIAL
            ),
             dbc.Tooltip(
            "Selecione o ano para ver a distribuição da população total por distrito da cidade",
            target="dropdown-ano",
        )
            ]),
        dbc.Row(
            dcc.Graph(
            id="choropleth", 
            style = {'display' : 'inline-block','float' : 'left'},
         )),
        
         ]),
         dbc.Col(
         dash_table.DataTable(id='data-table', 
            editable=False, 
            column_selectable=False,
            page_action="native",
            page_current= 0,
            page_size= 10,)
        )
        ]),
    dbc.Row(children=[
        dbc.Col(
        dcc.Graph(id="graph-mulher-x-homem",
        figure = make_mulher_x_homens_graph(df_munin)
        )
        ),
        dbc.Col(
        dcc.Graph(id='graph-envelhecimento-ano',
        figure = make_indice_envelhecimento_graph(df_munin)
        )
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