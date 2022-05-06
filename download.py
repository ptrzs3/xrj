# -*- coding: utf-8 -*-
import os
from multiprocessing import Pool

# 下载这个目录下的所有url.txt
path = 'D:\\crawler\\奈沐子\\'
directory = []


def download(cmd):
    # print(cmd)
    print(os.popen(cmd).read())


if __name__ == '__main__':
    for root, dirs, files in os.walk(path):
        for name in dirs:
            directory.append(os.path.join(root, name))
    cmd_list = []
    for m in range(len(directory)):
        if len(os.listdir(directory[m])) > 20:
            continue
        cmd = 'wget -c -i ' + directory[m] + '\\url.txt' + ' -P ' + directory[m]
        cmd_list.append(cmd)
    pool = Pool(40)
    pool.map(download, cmd_list)
    pool.close()
    pool.join()
