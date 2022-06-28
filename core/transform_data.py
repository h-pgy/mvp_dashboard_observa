import pandas as pd 
import geopandas as gpd 
import os
import time
from .utils import solve_path, solve_dir, remover_acentos, list_files
from .download_data import ObservaDownload, download_shape_distritos

from .config import LIST_INDICADORES, FOLDER_DISTRITOS, CSV_DOWNLOAD_DIR, APP_DATA_FOLDER

class TransformarIndicadores:

    list_indicadores = LIST_INDICADORES

    def __init__(self, csv_path=None):


        self.download_csv = ObservaDownload()

        if csv_path is None:
            csv_path = self.find_csv()
        self.df = pd.read_csv(csv_path, sep=';', encoding='utf-8')


    def find_csv(self, folder = CSV_DOWNLOAD_DIR):

        folder = solve_dir(folder)
        #pega o primeiro csv do folder
        csvs = list_files(folder, extension='.csv')

        if not csvs:
            self.download_csv()
            #hard-coded para dar tempo de dar o download
            #to do: esse tempo ser programatico (inspecionar processo selenium?)
            time.sleep(30)

        csvs = list_files(folder, extension='.csv')
        assert len(csvs) <2, 'Tem dois csvs salvos na pasta!'


        return csvs[0]

    def filtrar_distritos(self, df):
    
        mask = df['Região'].str.endswith('(Distrito)')
        
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

    def pipeline_transform(self, df=None, list_indis=None):

        if df is None:
            df = self.df
        
        df = self.indicadores_interesse(df, list_indis)
        df = self.filtrar_distritos(df)
        df = self.nome_distritos(df)


        return df

    def __call__(self):

        return self.pipeline_transform()


class MakeShapefiles:

    path_distritos = solve_path('SIRGAS_SHP_distrito_polygon.shp', parent=FOLDER_DISTRITOS)
    distritos_epsg = '31983'

    def __init__(self, df):

        self.distritos = gpd.read_file(self.path_distritos)
        self.df = self.get_distritos()

    def set_crs(self, distritos):

        distritos = distritos.set_crs(epsg = self.distritos_epsg)

        return distritos

    def get_distritos(self):

        if path is None:
            path = self.path_distritos
        
        distritos = gpd.read_file(path)
        distritos = self.set_crs(distritos)

        return distritos
    
    def get_city_boundaries(self, distritos=None):

        if distritos is None:
            distritos = self.distritos
        
        municipio_todo = distritos.dissolve()

        return municipio_todo

    def join_distritos(self, df=None, distritos=None):

        if df is None:
            df = self.df
        if distritos is None:
            distritos = self.distritos
        


    
    