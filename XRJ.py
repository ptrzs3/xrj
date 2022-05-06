import os
import re
import requests
import time
from multiprocessing import Pool
import common

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
           'Connection': 'close',
           'Accpet': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'Cookie': 'UM_distinctid=17d60aa5416409-07efa061da4286-978183a-146d15-17d60aa5417e39; CNZZDATA1278618868=374377226-1637997196-|1638826109; __tins__20641871={"sid": 1638831744318, "vd": 1, "expires": 1638833544318}; __51cke__=; __51laig__=1'
           }


class XRJ:
    def __init__(self, kwd):
        self.website = common.website
        self.prefix = common.prefix
        self.kwd = kwd
        self.path = common.parent_path
        self.downloaded = []
        self.update_mode = False
        self.replenish_mode = False

    def search(self):
        try:
            os.makedirs(self.path + self.kwd)
        except FileExistsError:
            print("关键词文件夹存在\n")
        link = self.generate_search_link()
        html = requests.get(link, headers=headers)
        html.encoding = 'UTF-8'
        html = re.sub("<font.*font>", self.kwd, html.text)
        all_pages = re.findall("</a>  <a href=\"(.*?)\" >", html)
        for i in range(len(all_pages)):
            all_pages[i] = common.search + all_pages[i]
        # 获取搜索结果所有的页码
        all_pages.insert(0, link)
        print("共有%d页结果" % len(all_pages))
        self.cope_every_single_search_page(all_pages)

    def check_empty_folder(self):
        self.replenish_mode = True
        empty_folder = []
        single_prefix = []
        temp_path = self.path + self.kwd + '\\'
        print(temp_path)
        files = os.listdir(temp_path)  # 查找路径下的所有的文件夹及文件
        for dir_name in files:
            f = str(temp_path + dir_name)  # 使用绝对路径
            if os.path.isdir(f):  # 判断是文件夹还是文件
                if not os.listdir(f):  # 判断文件夹是否为空
                    empty_folder.append(dir_name.split('.')[1][0:12])
                    single_prefix.append(dir_name.split('.')[0])
            else:
                print('f', f)
        file = open('search_result_temp.txt', 'w', encoding='utf-8')
        for i in range(len(empty_folder)):
            link = self.website + "plus/search/index.asp?keyword=" + empty_folder[i]
            try:
                html = requests.get(link, headers=headers)
            except requests.exceptions.ConnectionError:
                print("sleep\n")
                time.sleep(10)
                html = requests.get(link, headers=headers)
            html.encoding = 'UTF-8'
            name = re.findall("<span style=\"color:#000;\">(.*?)<font color=red>", html.text)
            link = re.findall("<h2><a href=\"/(.*?)\">", html.text)
            for j in range(len(name)):
                if name[j][0:5] == single_prefix[i][0:5]:
                    file.write(self.website + link[j] + '\n')
        file.close()
        self.cope_search_result('search_result_temp.txt')

    # 只检查第一页搜索结果，把本地没有的下载下来
    # 需要在parent_path下有kwd文件夹
    def update(self):
        self.update_mode = True
        self.check_download()
        link = self.generate_search_link()
        all_pages = [link]
        self.cope_every_single_search_page(all_pages)

    def check_download(self):
        for root, dirs, files in os.walk(self.path):
            for name in dirs:
                self.downloaded.append(name)

    def generate_search_link(self):
        link = self.website + "plus/search/index.asp?keyword=" + self.kwd
        return link

    def cope_every_single_search_page(self, all_search_pages):
        print(all_search_pages)
        log = open('log.txt', 'a+', encoding='utf-8')
        log.write('\n')
        log.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n')
        log.write(self.kwd + ' 搜索结果\n')
        links_file = open('links.txt', 'a+', encoding='utf-8')
        links_file.write('\n')
        links_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n')
        links_file.write(self.kwd + ' 搜索结果\n')
        search_result = open('search_result_temp.txt', 'w', encoding='utf-8')
        for item in all_search_pages:
            log.write(item + '\n')
        page_counter = 0
        for single_search_page in all_search_pages:
            page_counter += 1
            print("正在处理第%d页内容" % page_counter)
            html = requests.get(single_search_page, headers=headers)
            html.encoding = 'UTF-8'
            html = re.sub("<font.*font>", self.kwd, html.text)
            single_names = re.findall("<span style=\"color:#000;\">(.*?) &nbsp", html)
            single_links = re.findall("<h2><a href=\"(.*?)\">", html)
            for i in range(len(single_links)):
                # 补全，是可以访问的每一张专辑
                single_links[i] = self.website + single_links[i]
                print(single_names[i])
                print(single_links[i])
                log.write(single_names[i] + '\n')
                log.write(single_links[i] + '\n')
                links_file.write(single_links[i] + '\n')
                search_result.write(single_links[i] + '\n')
        print("页面处理完毕\n")
        log.close()
        links_file.close()
        search_result.close()
        self.cope_search_result('search_result_temp.txt')

    def cope_search_result(self, file_name):
        f = open(file_name, 'r', encoding='utf-8')
        contents = f.readlines()
        for i in range(len(contents)):
            contents[i] = contents[i].replace('\n', '')
        print("共%d张专辑\n" % len(contents))
        if self.update_mode or self.replenish_mode:
            pool = Pool(5)
        else:
            pool = Pool(40)
        pool.map(self.cope_single, contents)
        pool.close()
        pool.join()

    def cope_single(self, single_link):
        # 如果状态码400，检查是不是链接多换行符
        try:
            html = requests.get(single_link, headers=headers)
        except requests.exceptions.ConnectionError:
            print("sleep\n")
            time.sleep(10)
            html = requests.get(single_link, headers=headers)
        html.encoding = 'UTF-8'
        single_name = re.findall("<meta name=\"description\" content=\"(.*?)\"/>", html.text)
        print(single_name[0])
        p = self.path + self.kwd + '\\' + single_name[0]
        # 文件夹不存在或者补充模式
        if not os.path.isdir(p) or self.replenish_mode:
            try:
                os.makedirs(p)
            except FileExistsError:
                if self.replenish_mode:
                    print("文件夹已存在\n")
            single_all_page = re.findall("\d</a><a href=\"/(.*?)\">", html.text)
            del single_all_page[int(len(single_all_page) / 2) - 1:]
            for i in range(len(single_all_page)):
                single_all_page[i] = self.website + single_all_page[i]
            single_all_page.insert(0, single_link)
            pic_urls = []
            for son_page in single_all_page:
                try:
                    html = requests.get(son_page, headers=headers)
                except requests.exceptions.ConnectionError:
                    print("sleep\n")
                    time.sleep(10)
                    html = requests.get(son_page, headers=headers)
                html.encoding = 'UTF-8'
                temp_link = re.findall("/uploadfile/(.*?)\" />", html.text)
                for t in temp_link:
                    pic_urls.append(self.prefix + t)
            url_file = open(p + '\\url.txt', 'w', encoding='utf-8')
            for url in pic_urls:
                url_file.write(url + '\n')
            url_file.close()
        else:
            print("专辑已存在")


if __name__ == "__main__":
    kwd_ = input("input kwd\n")
    xrj = XRJ(kwd=kwd_)
    ch = int(input("1.搜索\n2.更新\n3.文件夹查空\n"))
    if ch == 1:
        xrj.search()
    elif ch == 2:
        xrj.update()
    elif ch == 3:
        xrj.check_empty_folder()
    else:
        print("无效输入")
        exit(0)
