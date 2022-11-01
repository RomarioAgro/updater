import os
import re
import shutil
"""
скрипт раскопировнаия файла manager.pac по подпапкам магазинов
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

def copy_file_to_folders(i_file: str, i_path: str, subfolder_list: list) -> None:
    """
    функция копирования файла по суб папкам
    :param i_file: str имя файла
    :param i_path: str имя папки
    :param subfolder_list: list списокпапок по которым будем копировать
    :return: None
    """
    i = 1
    for fold in subfolder_list:
        full_path = i_path + '\\' + fold + '\\'
        if os.path.exists(full_path):
            shutil.copy(i_file, full_path+i_file)
            print(f'{i} {full_path}')
            i += 1

def main():
    """
    скрипт копирования file_to_copy по субпапкам папкам write_path
    список субпапок берется из read_path
    :return:
    """
    read_path = 'u:\\prg\\__\\_МагазиныWin10.prg'
    write_path = 'u:\\rpt\\'
    # write_path = 'W:\\'
    file_to_copy = 'manager.pac'
    # file_to_copy = '6_01_sale.json'
    # read_path = '_МагазиныWin10.prg'
    list_folders = read_file(read_path)
    copy_file_to_folders(file_to_copy, write_path, list_folders)
    # print(list_folders)

if __name__ == '__main__':
    main()
