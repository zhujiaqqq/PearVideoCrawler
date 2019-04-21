import requests
from lxml import etree


class CategoryParser:
    """
    分类页面解析器
    https://www.pearvideo.com/category_loading.jsp?reqType=5&categoryId=6&start=0
    """

    def __init__(self, tree):
        self.tree = tree

    @classmethod
    def get_tree(cls, url, params=None, headers=None):
        response = requests.get(url=url, params=params, headers=headers)
        tree = etree.HTML(response.content.decode('utf-8'))
        return cls(tree)

    def get_video_urls(self) -> list:
        """
        获取当前页面的视频urls
        :return: url列表
        """
        video_urls = self.tree.xpath('/html/body/li/div/a/@href')
        for i in range(len(video_urls)):
            video_urls[i] = "https://www.pearvideo.com/" + video_urls[i]
        return video_urls


if __name__ == '__main__':
    params = {
        'reqType': 5,
        'categoryId': 6,
        'start': 0
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/71.0.3578.98 Safari/537.36'
    }
    print(CategoryParser.get_tree('https://www.pearvideo.com/category_loading.jsp?', params=params,
                                  headers=headers).get_video_urls())
