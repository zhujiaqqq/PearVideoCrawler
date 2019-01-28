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
        self.insert_video_sql = "insert pear_video (name, author, page_url, video_url, image_url, create_time, content)" \
                                " values (%(name)s, %(author)s, %(page_url)s, %(video_url)s, %(image_url)s, %(date)s, %(content)s)"
        self.insert_author_sql = "insert pear_author (author_name, home_url) values (%(name)s, %(url)s)"
        self.select_video_by_name = "select * from pear_video where name = %s"
        self.select_author_by_name = "select * from pear_author where author_name = %s"
        self.select_author_id = "select home_url from pear_author"
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
            res = self.dbHelper.fetchall(self.select_author_by_name, author_name)
            if len(res) >= 1:
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
        authors = tree.xpath('/html/body/li/div/div/a/text()')

        for name, url, img, author in zip(names, urls, images, authors):
            res = self.dbHelper.fetchall(self.select_video_by_name, name)
            if len(res) >= 1:
                continue
            else:
                url = self.base_url + url
                video_url, date, content = self.get_video_detail(url)
                item = {'name': name, 'page_url': url, 'image_url': img[img.find('(') + 1:img.find(')')],
                        'author': author, 'video_url': video_url, 'date': date, 'content': content}  # 视频元素
                items.append(item)
                self.dbHelper.execute(self.insert_video_sql, item)

        return items

    def get_video_detail(self, url):
        """
        获取视频页面的细节
        """
        response = requests.get(url, headers=self.headers)
        res = re.findall('srcUrl="(.*\.mp4)', response.text)
        res = set(res)
        video_url = res.pop()
        tree = etree.HTML(response.content.decode("utf-8"))
        date = tree.xpath('//*[@id="detailsbd"]/div[1]/div[2]/div/div[1]/div/div[1]/text()')[0]
        content = tree.xpath('//*[@id="detailsbd"]/div[1]/div[3]/div[1]/div[2]/text()')[0]
        return video_url, date, content

    def get_recommend_video(self):
        '''
        获取美食页面的1000条数据
        :return:
        '''
        for i in range(0, 999, 12):  # 获取0-1000的视频数据
            print(i)
            crawler.get_html(req_type=5, category_id=6, start=i, has_author=True)

    def get_authors_video(self):
        author_ids = []
        self.get_author_id(author_ids)
        for id in author_ids:
            print('作者：' + id)
            for i in range(0, 999, 12):
                print('第%d条' % i)
                res = crawler.get_html(req_type=30, category_id=id, start=i, has_author=False)
                if len(res) == 0:
                    break

    def get_author_id(self, author_ids):
        '''
        获取用户7位数id
        :param author_ids:
        :return:
        '''
        result = self.dbHelper.fetchall(self.select_author_id)
        for i in result:
            author_ids.append(i[0][-8:])


if __name__ == '__main__':
    crawler = PearCrawler()
    crawler.get_authors_video()

    # crawler.get_html(req_type=5, category_id=6, start=0, has_author=False)
