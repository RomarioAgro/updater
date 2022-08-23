import zipfile
import os
from win32com.client import Dispatch


path_260 = 'E:\\dropbox\\distr\\360Chrome.zip'

def path_to_desktop():
    # desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Рабочий стол')
    desktop = os.path.join(os.path.join(os.environ['ALLUSERSPROFILE']), 'Рабочий стол')
    return desktop

def create_shortcut(i_deck: str = '', file_name: str = '', target: str = '', work_dir: str = ''):
    i_path = os.path.join(i_deck, 'Bitrix.lnk')
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(i_path)
    shortcut.TargetPath = target
    shortcut.WorkingDirectory = work_dir
    shortcut.save()

def extract_all(i_path, e_path):

    with zipfile.ZipFile(i_path) as zf:
        zf.extractall(e_path)

def main():
    """
    распаковываем браузер 360Chrom в рознице
    на WinXP
    """
    o_path = 'd:\\360Chrome\\'
    e_path = 'd:\\'
    if os.path.exists(o_path) is False:
        extract_all(path_260, e_path)
    brouser_path = path_to_desktop()
    create_shortcut(i_deck=brouser_path, file_name='360Loader.exe', target='d:\\360Chrome\\360Loader.exe', work_dir=o_path)

if __name__ == '__main__':
    main()