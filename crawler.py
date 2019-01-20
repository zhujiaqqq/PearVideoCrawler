import requests
from lxml import etree

from mysqlUtil import DBHelper

CHANNEL_MAP = {
    'KNOWLEDGE': 'category_10',
    'CHINA': 'category_1',
    'WORLD': 'category_2',
    'SPORTS': 'category_9',
    'LIFE': 'category_5',
    'TECH': 'category_8',
    'ENTERTAINMENT': 'category_4',
    'FINANCE': 'category_3',
    'AUTO': 'category_31',
    'TASTE': 'category_6',
    'MUSIC': 'category_59',
}


# https://www.pearvideo.com/category_loading.jsp?reqType=5&categoryId=6&start=0
# 美食栏目的请求链接

class PearCrawler:
    def __init__(self):
        self.base_url = 'https://www.pearvideo.com/'
        self.dbHelper = DBHelper()
        self.insert_video_sql = "insert pear_video (name, url, img) values (%(name)s, %(url)s, %(img)s)"
        self.insert_author_sql = "insert pear_author (name,url) values (%(name)s, %(url)s)"
        self.select_video_by_name = "select * from pear_video where name = %s"
        self.select_author_by_name = "select * from pear_author where name = %s"
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }

    pass

    def get_html(self, category_id, start):
        params = {
            'reqType': '5',
            'categoryId': category_id,
            'start': start
        }

        response = requests.get('https://www.pearvideo.com/category_loading.jsp?', params=params, headers=self.headers)
        tree = etree.HTML(response.content.decode("utf-8"))
        items = self.get_item(tree)
        authors = self.get_author(tree)

        print(items)
        print(authors)
        return items, authors

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


if __name__ == '__main__':
    crawler = PearCrawler()
    for i in range(0, 999, 12):  # 获取0-1000的视频数据
        print(i)
        crawler.get_html(6, i)
