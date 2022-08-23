import os
import re
import shutil
"""
скрипт редактирования файлов rsync.cmd
в магазинах с WinXP
"""

def slice_elem(elem):
    """
    очищаем элементы от лишнего первого символа
    :param elem:
    :return:
    """
    return elem[1:]


def read_file(i_path):
    """
    функция поиска папок магазинов в котрых win10
    :param i_path: str путь до фала который расссматриваем
    и в котором ищем список папок с магазинами win10
    :return: list список папок
    """
    pattern = r';\w\w'
    list_folders = []
    with open(i_path, 'r', encoding='cp866') as i_file:
        for line in i_file:
            intermediate_list = re.findall(pattern, line)
            if len(intermediate_list) > 0:
                print(line, end='')
                list_folders = list(map(slice_elem, intermediate_list))
    return list_folders

def list_WinXP(list_WIN10: str = [], all_path: str = ''):
    """
    функция из общего списка папок магазинов,
    получаем только c WinXP
    :param list_WIN10:
    :return:
    """
    all_dir = os.listdir(all_path)
    winXp = set(all_dir) - set(list_WIN10)
    winXp.remove('__')
    # print(all_dir)
    # print(list_WIN10)
    return list(winXp)


def editing_rsync(work_path: str = '', list_WinXP: list = [], add_string: str = '') -> None:
    """
    функция перезаписи файлов rsync,
    добавляем строку вызова скрипта с ярлыком и распаковокой
    :param work_path: str папка где у нас лежат фалы для редактирования
    :param list_WinXP: list список магазинов с WinXP
    :param add_string: str строка которую добавляем в скрипт rsync
    :return:
    """

    for i_shop in list_WinXP:
        my_path = os.path.abspath(work_path + i_shop + '\\rsync.cmd')
        with open(my_path, 'a') as i_file:
            i_file.write(add_string + '\n')

def clear_rsync(work_path: str = '', list_WinXP: list = [], add_string: str = '') -> None:
    """
    функция возврата файлов rsync, к исходному состоянию
    убираем строку вызова скрипта с ярлыком и распаковокой
    :param work_path: str папка где у нас лежат фалы для редактирования
    :param list_WinXP: list список магазинов с WinXP
    :param add_string: str строка которую добавляем в скрипт rsync
    :return:
    """
    new_file_name = 'rsync.txt'

    for i_shop in list_WinXP:
        os.chdir(work_path + i_shop + '\\')
        my_path = os.path.abspath('rsync.cmd')
        new_file = open(new_file_name, 'w')
        with open(my_path, 'r') as i_file:
            for line in i_file:
                if line.startswith(add_string) is False:
                    new_file.write(line)
        new_file.close()
        os.remove('rsync.cmd')
        os.rename(new_file_name, 'rsync.cmd')

def main():
    read_path = 'u:\\prg\\__\\_МагазиныWin10.prg'
    write_path = 'u:\\rsync\\'
    write_file = 'rsync.cmd'
    read_path = '_МагазиныWin10.prg'

    # str_for_run = 'pip install e:\\dropbox\\distr\\python\\pkg\\pywin32-224-cp34-cp34m-win32.whl'
    list_folders_Win10 = read_file(read_path)
    list_folders_WinXP = list_WinXP(list_folders_Win10, write_path)
    # list_folders_WinXP = ['AT']
    # editing_rsync(work_path=write_path, list_WinXP=list_folders_WinXP, add_string=str_for_run)
    str_for_run = 'python d:\\kassa\\script_py\\360Chrom.py'
    # editing_rsync(work_path=write_path, list_WinXP=list_folders_WinXP, add_string=str_for_run)
    clear_rsync(work_path=write_path, list_WinXP=list_folders_WinXP, add_string=str_for_run)

if __name__ == '__main__':
    main()
