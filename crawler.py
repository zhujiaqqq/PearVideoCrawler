import requests
from lxml import etree

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

class PearCrawler:
    def __init__(self):
        self.base_url = 'https://www.pearvideo.com/'
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
        item = {}

        response = requests.get('https://www.pearvideo.com/category_loading.jsp?', params=params, headers=self.headers)
        # print(response.text)

        tree = etree.HTML(response.content.decode("utf-8"))
        names = tree.xpath('/html/body/li/div/a/div[2]/text()')
        urls = tree.xpath('/html/body/li/div/a/@href')
        images = tree.xpath('/html/body/li/div/a/div[1]/div[1]/div/@style')

        for name, url, img in zip(names, urls, images):
            print(name)
            print(self.base_url + url)
            print(img[img.find('(') + 1:img.find(')')])

        pass


if __name__ == '__main__':
    crawler = PearCrawler()
    crawler.get_html(6, 0)
