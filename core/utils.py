import os
import zipfile

def solve_dir(folder):

    if not os.path.exists(folder):
        os.mkdir(folder)
    
    return os.path.abspath(folder)

def solve_path(path, parent = None):

    if parent:
        parent = solve_dir(parent)
        path = os.path.join(parent, path)

    return os.path.abspath(path)

def list_files(folder, extension=None):

    folder = solve_path(folder)
    files = [os.path.join(folder, file) for file in os.listdir(folder)]
    
    if extension is not None:
        return [f for f in files if f.endswith(extension)]
    
    return files


def remover_acentos(name):
    
    acento_letra = {
        'ç' : 'c',
        'á' : 'a',
        'â' : 'a',
        'à' : 'a',
        'ã' : 'a',
        'ä' : 'a',
        'é' : 'e',
        'ê' : 'e',
        'è' : 'e',
        'ë' : 'e',
        'í' : 'i',
        'î' : 'i',
        'ì' : 'i',
        'ï' : 'i',
        'ó' : 'o',
        'ô' : 'o',
        'ò' : 'o',
        'ø' : 'o',
        'õ' : 'o',
        'ö' : 'o',
        'ú' : 'u',
        'û' : 'u',
        'ù' : 'u',
        'ü' : 'u',
        'ñ' : 'n',
        'ý' : 'y'
    }
    
    chars = list(name)
    
    return ''.join([acento_letra.get(char, char) for char in chars])


def delete_existing_files(folder, extension=None):

    folder = solve_dir(folder)

    files = list_files(folder, extension)
    if files:
        print('Found existing files')
    for file in files:
        os.remove(file)
        print(f'File {file} deleted.')

def unzip_bytes_io(bytes_io, save_folder):

    with zipfile.ZipFile(bytes_io) as zip_ref:
        zip_ref.extractall(save_folder)


    