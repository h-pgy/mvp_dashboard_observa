from .utils import solve_dir, solve_path
import os


CSV_DOWNLOAD_DIR = solve_path('csv_downloads', 'data')
JSON_DOWNLOAD_DIR = solve_path('json_downloads', 'data')
HEADLESS_BROWSER = False

FOLDER_MAPS = solve_path('maps', parent='static_files')
FOLDER_DISTRITOS = solve_path('SIRGAS_SHP_distrito', FOLDER_MAPS)

APP_DATA_FOLDER = solve_path('app', 'data')

LIST_INDICADORES_DISTRITO = [
    'População total',
    'População total - homens',
    'População total - mulheres',
    'Razão de sexos'
]

LIST_INDICADORES_MUNICIPIO = ['Índice de envelhecimento',
                            'População total - homens',
                            'População total - mulheres',
                            'Razão de sexos'
                            ]