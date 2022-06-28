from .utils import solve_dir, solve_path
import os


CSV_DOWNLOAD_DIR = solve_path('csv_downloads', 'data'),
JSON_DOWNLOAD_DIR = solve_path('json_downloads', 'data'),
HEADLESS_BROWSER = False

FOLDER_MAPS = solve_path('maps', parent='static_files')

APP_DATA_FOLDER = solve_path('app', 'data')

distorcao_idade_ano = [
    '04.01.03 Taxa de distorção da idade-ano para o ano no Ensino Fundamental nos anos iniciais (%)',
   '04.01.04 Taxa de distorção da idade-ano para o ano no Ensino Fundamental nos anos finais (%)',
]

raca_alunos = [
    'Alunos da rede municipal de ensino da raça/cor amarela (%)',
    'Alunos da rede municipal de ensino da raça/cor branca (%)',
    'Alunos da rede municipal de ensino da raça/cor indígena (%)',
    'Alunos da rede municipal de ensino da raça/cor parda (%)',
    'Alunos da rede municipal de ensino da raça/cor preta (%)',
       
       ]

abandono = [
    'Taxa de abandono escolar no Ensino Fundamental da rede municipal (%)',
   'Taxa de abandono escolar no Ensino Médio da rede municipal (%)',
]


LIST_INDICADORES = []
LIST_INDICADORES.extend(distorcao_idade_ano)
LIST_INDICADORES.extend(raca_alunos)
LIST_INDICADORES.extend(abandono)