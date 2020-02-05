# ​1、Python中，每个py文件被称之为模块，每个具有_init_.py文件的目录被称为包。
# 只要模块或者包所在的目录在sys.path中，就可以使用import模块或者import包来使用。
# 如果要使用的模块(py文件)和当前模块在同一目录，只要import相应的文件名即可，
# 比如在a.py中使用b.py：import b即可；但是如果要import一个不同目录的文件，
# 首先需要使用sys.path.append方法将b.py所在目录加入到搜索目录中，然后进行import即可，
# 例如：import sys   sys.path.append(‘c:\xxx\b.py’)
# from 文件夹.子文件夹 import 函数/类名
# 2、sys.path是python的搜索模块的路径集，是一个list；可以在python环境下
# 使用sys.path.append(path)添加相关的路径，但在退出python环境后添加的路径就会自动消i失了。
# 3、ImportError: No module named ‘xxx’：模块不在搜索路径里，从而导致路径搜索失败。
# 解决方法，设置超时时间
#
# pip --default-timeout=100 install -U Pillow

from urllib import request
import os
from user_agents import parse
import time
import random
import re
import requests
from xml import etree


class MeiziSpider():
    def __init__(self):
        # https://www.mzitu.com/150343
        self.url = 'https://www.mzitu.com/all/'

    def get_html(self, url):
        headers = {'User-Agent': random.choice(parse)}
        req = request.Request(url=url, headers=headers)
        res = request.urlopen(req)
        html = res.read()
        return html
        # print(html)

    def re_func(self, re_bds, html):
        pattern = re.compile(re_bds, re.S)
        r_list = pattern.findall(html)
        return r_list

    # 获取想要的数据 - 解析一级页面
    # def parse_html(self, url):
    #     one_html = self.get_html(url).decode()
    #     # print(one_html)
    #     re_bds = '<p class="url">.*?<a href="(.*?)" target="_blank">(.*?)</a>'
    #     one_list = self.re_func(re_bds, one_html)
    #     # print(one_list)
    #     # time.sleep(random.randint(1, 3))
    #     self.write_html(one_list)

    def parse_html(self, url):
        html = self.get_html(url).decode()
        parse_obj = etree.HTML(html)
        href_list = parse_obj.xpath('//div[@class="all"]/ul[@class="archives"]/li/p[@class="url"]/a/@href')
        print("href_list:", href_list)
        self.write_html(href_list)

    def write_html(self, href_list):
        for href in href_list:
            two_url = href
            print(two_url)
            time.sleep(random.randint(1, 3))
            self.save_image(two_url)

    def save_image(self, two_url):
        headers = {'Referer': two_url, 'User-Agent': random.choice(parse)}
        print('---------two_url-----------', two_url)
        # 向图片链接发请求.得到bytes类型
        i = 0
        while True:
            try:
                img_link = two_url + '/{}'.format(i)
                print("img_link:", img_link)
                html = requests.get(url=img_link, headers=headers).text
                re_bds = ' <div class="main-image"><p><a href="https://www.mzitu.com/.*?" ><img ' \
                         'src="(.*?)" alt="(.*?)" width=".*?" height=".*?" /></a></p>'
                img_html_list = self.re_func(re_bds, html)
                print("img_html_list", img_html_list)
                name = img_html_list[0][1]
                print("-----name:", name)
                direc = 'F:/data/mzitu/{}/'.format(name)
                print("direc:", direc)
                if not os.path.exists(direc):
                    os.makedirs(direc)
                img_ = requests.get(url=img_html_list[0][0], headers=headers).content
                filename = direc + name + img_link.split('/')[-1] + '.jpg'
                # print("img_:",img_)
                with open(filename, 'wb') as f:
                    f.write(img_)
                i += 1
            except Exception as e:
                break


if __name__ == '__main__':
    spider = MeiziSpider()
    spider.parse_html('https://www.mzitu.com/all')
