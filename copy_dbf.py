import os
from typing import List
import re
import shutil
import hashlib
from progress.bar import IncrementalBar, ShadyBar

"""
скрипт раскопирования файлов dbf
из папки 
\\shoprsync\rsync\inbox\EA\export\*.dbf
по папкам магазинов
\\shoprsync\magazin\EA\DBF\*.dbf
\\store\junk\90_Файлсервер\backup\dbf\EA\DBF\*.dbf
EA это переменная магазина как вы поняли
"""

def get_hash_md5(filename):
    with open(filename, 'rb') as f:
        m = hashlib.md5()
        while True:
            data = f.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


def read_file_in_folder(top_folder: str = '', folder_shops: List = [], folder_destination: list = []) -> None:
    """
    проходим по папке магазина смотрим дату создания файлов dbf
    и если в конечной папке нет этого файла или у него дата другая
    копируем этот файл
    :param top_folder: str корневая папка где лежат папки магазинов
    :param folder_shops: list список папок магазинов
    :param folder_destination: str корневая папка для аналитики и для бекапов, в ней тоже есть структура папок магазинов
    :return:
    """
    sub_dir_inbox = 'export'  #в инбоксе dbf файлы хранятся в папке export
    sub_dir_dest = 'dbf'  #конечная папка для аналитикии бекапов

    pattern = r'[A-Za-z]{2}[A-Ca-c0-9]{5}[N,Z]{1}.dbf'  #шаблон должен покрывать файлы такого вида KB10922Z.dbf
    shop_bar = ShadyBar('SHOPS', max=len(folder_shops))
    for shop in folder_shops:   #проходим по папкам магазинов
        shop_bar.next()
        print()
        inbox_export = top_folder + shop + '\\' +sub_dir_inbox
        filenames = next(os.walk(inbox_export), (None, None, []))[2]   #собираем список файлов
        files_bar = IncrementalBar('FILES in {0}'.format(shop), max=len(filenames))
        for files in filenames:
            files_bar.next()
            if re.fullmatch(pattern, files) is not None:
                # тут надо сравнить хэши первого файла и второго
                source_file = inbox_export + '\\' + files  #полное имя исходного файла
                hash_source = get_hash_md5(source_file)
                for elem in folder_destination:
                    dest_file = elem + '\\' + shop + '\\' + sub_dir_dest + '\\' + files  #полное имя конечного файла
                    copy_yes = False  #флаг делать копирование
                    if os.path.exists(dest_file):  #если конечный файл существует то надо сравнить хэши файлов
                        dest_source = get_hash_md5(dest_file)
                        # print(hash_source)
                        # print(dest_source)
                        if hash_source != dest_source:
                            copy_yes = True
                            print('ФАЙЛЫ ОТЛИЧАЮТСЯ! скопирован файл1 {0} в файл2 {1}'.format(source_file, dest_file))
                    else:
                        copy_yes = True
                        print('ФАЙЛА НЕТ! скопирован файл {0} в файл {1}'.format(source_file, dest_file))
                    if copy_yes == True:
                        shutil.copy2(source_file, dest_file)
        files_bar.finish()
    shop_bar.finish()



def read_path(in_path: str = '\\shoprsync\\rsync\\inbox\\') -> List:
    """
    функция поиска папок магазинов,
    папка магазина состоит из 2-х символов, буквы или цифры
    :param in_path: str путь где ищем папки магазинов
    :return: list список папок
    """
    pattern = r'[a-zA-Z0-9]{2}'
    o_dir = list(filter(lambda x: re.fullmatch(pattern, x) is not None, os.listdir(in_path)))
    return o_dir

def main():
    """
    скрипт копирования файлов dbf из инбокса по путям где их забирает аналитика
    и просто папка с бекапом, аналитика написана в 2005 году и никто не знает как ее
    переписать на новые пути
    :return: None
    """
    r_path = r'\\shoprsync\\rsync\\inbox\\'
    folder_shops = read_path(in_path=r_path)   #получаем список папок магазнов
    write_path = [r'\\shoprsync\\magazin\\', r'\\store\\junk\\90_Файлсервер\\backup\\dbf\\']  #пути куда нам надо закинуть наши dbf
    write_path = [r'\\shoprsync\\magazin\\']  # пути куда нам надо закинуть наши dbf
    # for elem in write_path:
    #     read_file_in_folder(top_folder=r_path, folder_shops=folder_shops, folder_destination=elem)
    read_file_in_folder(top_folder=r_path, folder_shops=folder_shops, folder_destination=write_path)

if __name__ == '__main__':
    main()
