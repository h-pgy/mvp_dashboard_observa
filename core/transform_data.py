from flask import g
import pandas as pd 
import geopandas as gpd 
import os
import time
from .utils import solve_path, solve_dir, remover_acentos, list_files
from .download_data import ObservaDownload, download_shape_distritos

from .config import FOLDER_DISTRITOS, CSV_DOWNLOAD_DIR

class TransformarIndicadores:


    def __init__(self, csv_path=None):

        self.download_csv = ObservaDownload()
        if csv_path is None:
            csv_path = self.find_csv()
        self.csv_path = csv_path

    def find_csv(self, folder = CSV_DOWNLOAD_DIR):

        folder = solve_dir(folder)
        #pega o primeiro csv do folder
        csvs = list_files(folder, extension='.csv')

        if not csvs:
            self.download_csv()

        csvs = list_files(folder, extension='.csv')
        assert len(csvs) <2, 'Tem dois csvs salvos na pasta!'


        return csvs[0]

    def filtrar_distritos(self, df):
    
        mask = df['Região'].str.endswith('(Distrito)')
        
        return df[mask].copy().reset_index(drop=True)

    def filtrar_municipio(self, df):

        mask = df['Região'].str.endswith('(Município)')

        return df[mask].copy().reset_index(drop=True)

    def indicadores_interesse(self, df, list_indis=None):

        if list_indis is None:
            list_indis = self.list_indicadores
        interesse = df[df['Nome'].isin(list_indis)]
        interesse = interesse.reset_index(drop=True).copy()

        return interesse

    def clean_distrito_name(self, name):
    
        lowered = name.lower().replace('(distrito)', '').strip()
        sem_acento = remover_acentos(lowered)
        
        return sem_acento.upper()
    
    def nome_distritos(self, df):
        
        df = df.copy()
        df['ds_nome'] = df['Região'].apply(self.clean_distrito_name) 

        return df

    def stringbr_to_float(df, val):

        if pd.isnull(val):
            return 0
        
        if val == '':
            return 0
        
        if val == ' ':
            return 0

        val = str(val)

        val = val.replace(',', '.')

        try:
            if '.' in val:
                val = float(val)
            else:
                val = int(val)
        except ValueError:
            print(f'Erro no valor: {val}')
            return 0
        return val

    def resultados_float(self, df):

        df = df.copy()
        df['value'] = df['Resultado'].apply(self.stringbr_to_float)
        
        return df

    def pipeline_transform(self, list_indicadores, filtrar_distrito, df=None):

        if df is None:
            df = pd.read_csv(self.csv_path, sep=';', encoding='utf-8')

        df = self.indicadores_interesse(df, list_indicadores)
        if filtrar_distrito:
            df = self.filtrar_distritos(df)
            df = self.nome_distritos(df)

        else:
            df = self.filtrar_municipio(df)
        
        df = self.resultados_float(df)

        return df

    def __call__(self, list_indicadores, filtrar_distrito = False):

        return self.pipeline_transform(list_indicadores, filtrar_distrito)


class MakeShapefileDistritos:

    path_distritos = solve_path('SIRGAS_SHP_distrito_polygon.shp', parent=FOLDER_DISTRITOS)
    distritos_epsg = '31983'
    maps_epsg = '4326'

    def __init__(self):

        self.distritos = self.get_distritos()

    def set_crs(self, distritos, epsg):

        distritos = distritos.set_crs(epsg = epsg)

        return distritos

    def download_shp_if_not_present(self, path):

        if not os.path.exists(path):
            download_shape_distritos()

    def get_distritos(self, path=None, maps_epsg=True):

        if path is None:
            path = self.path_distritos
        
        distritos = gpd.read_file(path)
        distritos = self.set_crs(distritos, self.distritos_epsg)
        if maps_epsg:
            distritos = distritos.to_crs(epsg = self.maps_epsg)

        return distritos
    
    def get_city_boundaries(self, distritos=None):

        if distritos is None:
            distritos = self.distritos
        
        municipio_todo = distritos.dissolve()

        return municipio_todo
    