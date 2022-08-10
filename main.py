import os
import re


def read_file(i_path):
    pattern = r''
    list_folders = []
    with open(i_path, 'r', encoding='cp866') as i_file:
        for line in i_file:
            print(line, end='')
    return list_folders

def main():
    # read_path = 'u:\\prg\\__\\_МагазиныWin10.prg'
    read_path = 'МагазиныWin10.prg'
    list_folders = read_file(read_path)
    pass

if __name__ == '__main__':
    main()
