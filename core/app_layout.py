import dash_bootstrap_components as dbc
from dash import html

from core.utils import solve_path_relative
from core.config import IMG_FOLDER

LOGO_OBSERVA = solve_path_relative('logo-pequeno-observa.png', parent=IMG_FOLDER)

print(LOGO_OBSERVA)
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=LOGO_OBSERVA, height="30px")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://observasampa.prefeitura.sp.gov.br/",
                style={"textDecoration": "none"},
            ),
        ],
    ),
    color="light",
    dark=False,
)