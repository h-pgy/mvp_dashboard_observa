import os
import platform
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options

from requests import Session
from io import BytesIO

from .utils import solve_dir, list_files, solve_path, delete_existing_files, unzip_bytes_io
from .config import CSV_DOWNLOAD_DIR, HEADLESS_BROWSER, FOLDER_DISTRITOS



def download_shape_distritos(folder = FOLDER_DISTRITOS):

    
    #checa se tem arquivos ja dentro do folder
    #nesse caso nao faz sentido atualizar porque os distritos nao mudam
    if os.path.exists(folder) and len(os.listdir(folder))>1:
        print('Dados de distritos ja salvos')
        return

    session = Session()
    home = 'http://geosampa.prefeitura.sp.gov.br/PaginasPublicas/'

    link_download = ("http://download.geosampa.prefeitura.sp.gov.br/" # o servico de download esta em outro dominio
                    "PaginasPublicas/downloadArquivo.aspx?orig=DownloadCamadas"
                    "&arq=01_Limites%20Administrativos%5C%5CDistrito%5C%5CShapefile%5C%5CSIRGAS_SHP_distrito"
                    "&arqTipo=Shapefile")

    #entrando na home para pegar cookies
    session.get(home)

    with session.get(link_download) as r:
        binary = r.content
    bytes_io = BytesIO(binary)

    unzip_bytes_io(bytes_io, folder)

#TO DO: POR ENQUANTO SOH ESTOU BAIXANDO CSV DO INDICADORES, MAS DA PARA PEGAR MAIS
class ObservaDownload:

    base_url = 'https://observasampa.prefeitura.sp.gov.br/'
    csv_download_dir = CSV_DOWNLOAD_DIR
    headless = HEADLESS_BROWSER

    def inicialize(self):

        browser_profile = self.create_profile()
        self.browser = self.create_driver(browser_profile)

        #DELETANDO CSVS
        delete_existing_files(self.csv_download_dir, '.csv')
    
    def get_webdriver_path(self):
    
        my_os = platform.system()
        
        if my_os == 'Windows':
            return os.path.abspath(os.path.join('gecko_drivers', 'win64.exe'))
        else:
            return os.path.abspath(os.path.join('gecko_drivers', 'linux64'))

    def create_profile(self):

        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.dir", self.csv_download_dir),
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip,text/csv")

        return profile

    def create_driver(self, profile):
        
        options = Options()
        options.headless = self.headless
        exec_path = self.get_webdriver_path()
        return webdriver.Firefox(profile, options=options, executable_path=exec_path)

    def enter_home(self):

        self.browser.get(self.base_url)

    def enter_downloads(self):

        self.browser.get(self.base_url+'Download')

    #TO DO: O PRIMEIRO BOTAO EH INDICADORES CSV, MAS PODEMOS PEGAR OUTROS
    def csv_download_button(self):

        div_download = self.browser.find_element_by_class_name('download2')
        button = div_download.find_element_by_class_name('offer')

        return button

    def download_csv(self, button):
        
        action = ActionChains(self.browser)

        action.move_to_element(button).perform()
        button.click()

    def download_csv_pipeline(self):

        self.enter_home()
        self.enter_downloads()
        botao = self.csv_download_button()
        self.download_csv(botao)

    #WILL ONLY WORK IF DIR IS PREVIOUSLY EMPTIED
    def check_file_in_dir(self, path, extension):

        files = list_files(path, extension)

        if files:
            return True
        return False

    #IT SEEMS TO BE WORKING BUT NEVERTHELESS I GET A WARNING FROM FIREFOX
    def close_when_download_finished(self, download_dir, extension):

            check = self.check_file_in_dir(download_dir, extension)
            if check:
                self.browser.close()
                return
            time.sleep(3)
            self.close_when_download_finished(download_dir, extension)

    #TO DO: DOWNLOAD OUTROS ELEMENTOS
    def __call__(self):

        self.inicialize()
        self.download_csv_pipeline()
        #HARDCODING THIS TILL I HAVE A MORE RELIABLE SOLUTION (CHECK FOR TEMPFILES FOR EXAMPLE)
        time.sleep(10)
        self.close_when_download_finished(self.csv_download_dir, '.csv')

