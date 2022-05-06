import os


def search(path):
    files = os.listdir(path)  # 查找路径下的所有的文件夹及文件
    for dir_name in files:
        f = str(path + dir_name)  # 使用绝对路径
        if os.path.isdir(f):  # 判断是文件夹还是文件
            if not os.listdir(f):  # 判断文件夹是否为空
                print(dir_name)


if __name__ == '__main__':
    search('E:\\pic\\芝芝\\')
