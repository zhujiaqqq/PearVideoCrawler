import requests
import re
from lxml import etree

from mysqlUtil import DBHelper

CHANNEL_MAP = {
    'KNOWLEDGE': '10',
    'CHINA': '1',
    'WORLD': '2',
    'SPORTS': '9',
    'LIFE': '5',
    'TECH': '8',
    'ENTERTAINMENT': '4',
    'FINANCE': '3',
    'AUTO': '31',
    'TASTE': '6',
    'MUSIC': '59',
}


# https://www.pearvideo.com/category_loading.jsp?reqType=5&categoryId=6&start=0
# 美食栏目的请求链接

# https://www.pearvideo.com/category_loading.jsp?reqType=30&categoryId=11794266&start=0
# 获取播主视频

class PearCrawler:
    def __init__(self):
        self.base_url = 'https://www.pearvideo.com/'
        self.dbHelper = DBHelper()
        self.insert_video_sql = "insert pear_video (name, url, img) values (%(name)s, %(url)s, %(img)s)"
        self.insert_author_sql = "insert pear_author (name,url) values (%(name)s, %(url)s)"
        self.select_video_by_name = "select * from pear_video where name = %s"
        self.select_author_by_name = "select * from pear_author where name = %s"
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/71.0.3578.98 Safari/537.36'
        }

    pass

    def get_html(self, req_type, category_id, start, has_author):
        params = {
            'reqType': req_type,
            'categoryId': category_id,
            'start': start
        }

        response = requests.get('https://www.pearvideo.com/category_loading.jsp?', params=params, headers=self.headers)
        tree = etree.HTML(response.content.decode("utf-8"))
        items = self.get_item(tree)
        print(items)
        if has_author:
            authors = self.get_author(tree)
        return items

        pass

    def get_author(self, tree):
        authors = []  # 作者元素列表
        author_names = tree.xpath('/html/body/li/div/div/a/text()')
        author_urls = tree.xpath('/html/body/li/div/div/a/@href')
        for author_name, author_url in zip(author_names, author_urls):
            author = {'name': author_name, 'url': self.base_url + author_url}  # 作者元素
            authors.append(author)
            result = self.dbHelper.fetchall(self.select_author_by_name, author_name)
            if len(result) >= 1:
                continue
            else:
                self.dbHelper.execute(self.insert_author_sql, author)
        return authors

    pass

    def get_item(self, tree):
        items = []  # 视频元素列表
        names = tree.xpath('/html/body/li/div/a/div[2]/text()')
        urls = tree.xpath('/html/body/li/div/a/@href')
        images = tree.xpath('/html/body/li/div/a/div[1]/div[1]/div/@style')
        for name, url, img in zip(names, urls, images):
            item = {'name': name, 'url': self.base_url + url, 'img': img[img.find('(') + 1:img.find(')')]}  # 视频元素
            items.append(item)
            result = self.dbHelper.fetchall(self.select_video_by_name, name)
            if len(result) >= 1:
                continue
            else:
                self.dbHelper.execute(self.insert_video_sql, item)

        return items

    def get_video_src(self, url):
        """
        获取视频页面的视频地址
        :param url: 视频页面地址
        :return: 视频地址
        """
        response = requests.get(url, headers=self.headers)
        result = re.findall('srcUrl="(.*\.mp4)', response.text)
        result = set(result)
        print(result.pop())


if __name__ == '__main__':
    crawler = PearCrawler()
    # 获取美食页面的1000条数据
    # for i in range(0, 999, 12):  # 获取0-1000的视频数据
    #     print(i)
    #     crawler.get_html(req_type=5, category_id=6, start=i, has_author=True)

    # 获取一个播主的视频数据
    # for i in range(0, 999, 12):
    #     result = crawler.get_html(req_type=30, category_id=11794266, start=i, has_author=False)
    #     if len(result) == 0:
    #         break
    # pass

    crawler.get_video_src('https://www.pearvideo.com/video_1508205')
