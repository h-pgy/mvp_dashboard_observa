import dash_bootstrap_components as dbc
from dash import html

from core.utils import solve_path_relative
from core.config import IMG_FOLDER

LOGO_OBSERVA = solve_path_relative('logo-pequeno-observa.png', parent=IMG_FOLDER)
MARK_GITHUB = solve_path_relative('GitHub-Mark-64px.png', parent=IMG_FOLDER)
BACKGROUND_IMG = solve_path_relative('bg-logo-cinza-1.png', parent=IMG_FOLDER)

TAMANHO_COL = 5
OFFSET_COL_LEFT = 1
OFFSET_COL_RIGHT = -1

navbar = dbc.Navbar(
    dbc.Row([
    dbc.Col(dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=LOGO_OBSERVA, height="40px")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://observasampa.prefeitura.sp.gov.br/",
                style={"textDecoration": "none"},
            ),
        ], 
    ), 
    width = {"size" : 1, 'offset' : 2}
    ),
    dbc.Col(
        dbc.NavItem(
            dbc.NavLink("SEPEP", 
                href="https://www.prefeitura.sp.gov.br/cidade/secretarias/governo/planejamento/")),
    width = {"size" : 1, 'offset' : 6}
    ),
    dbc.Col(
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Instrumentos de Planejamento", header=True),
                dbc.DropdownMenuItem("Programa de Metas 2021-2024", href="https://programademetas.prefeitura.sp.gov.br/"),
                dbc.DropdownMenuItem("Portal de Devolutivas PDM 21-24", href="https://devolutiva.pdm.prefeitura.sp.gov.br/"),
            ],
            nav=True,
            in_navbar=True,
            label="Mais",
        ),
    width = {"size" : 1, 'offset' : 1}
    ),
    ]),
    color="light",
    dark=False,
)

footer = dbc.Row(
    html.Footer(
        dbc.Row([
            dbc.Col(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=MARK_GITHUB, height="40px")),
                        ],
                        align="right",
                    ),
                    href="https://github.com/h-pgy/mvp_dashboard_observa",
                    style={"textDecoration": "none"},
                ),
            ],
        )],
    )
        ))

base_style = {
    'backgroundColor': '#d0cfce',
    }