import os
import platform
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options

from core.utils import solve_dir, list_files, solve_path


def delete_existing_files(folder, extension=None):

    folder = solve_dir(folder)

    files = list_files(folder, extension)
    if files:
        print('Found existing files')
    for file in files:
        os.remove(file)
        print(f'File {file} deleted.')


#TO DO: POR ENQUANTO SOH ESTOU BAIXANDO CSV DO INDICADORES, MAS DA PARA PEGAR MAIS
class ObservaDownload:

    base_url = 'https://observasampa.prefeitura.sp.gov.br/'
    csv_download_dir = os.environ.get('CSV_DOWNLOAD_DIR') or solve_path('csv_data', 'data')
    headless = os.environ.get('HEADLESS_BROWSER') or False

    def __init__(self):

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

        self.download_csv_pipeline()
        #HARDCODING THIS TILL I HAVE A MORE RELIABLE SOLUTION (CHECK FOR TEMPFILES FOR EXAMPLE)
        time.sleep(3)
        self.close_when_download_finished(self.csv_download_dir, '.csv')


if __name__ == "__main__":

    downloader = ObservaDownload()


