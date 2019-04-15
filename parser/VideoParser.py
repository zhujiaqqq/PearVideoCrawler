import requests
from lxml import etree


class VideoParser:
    """
    https://www.pearvideo.com/video_1538727
    """

    def __init__(self, tree):
        self.tree = tree

    @classmethod
    def get_tree(cls, url, params=None, headers=None):
        response = requests.get(url=url, params=params, headers=headers)
        tree = etree.HTML(response.content.decode('utf-8'))
        return cls(tree)

    def get_author(self) -> map:
        """
        获取作者信息
        :return:
        """
        author_url = self.tree.xpath('//*[@id="detailsbd"]/div[1]/div[3]/div[1]/div[1]/a/@href')[0]
        author_name = self.tree.xpath('//*[@id="detailsbd"]/div[1]/div[3]/div[1]/div[1]/a/div/text()')[0]
        author_info = self.tree.xpath('//*[@id="detailsbd"]/div[1]/div[3]/div[1]/div[1]/a/text()')[0]
        author = {'name': author_name, 'url': author_url, 'info': author_info}
        return author

    def get_tags(self) -> list:
        """
        获取标签数据
        :return:
        """
        tags = []
        tags_urls = self.tree.xpath('//*[@id="detailsbd"]/div[1]/div[3]/div[3]/a/@href')
        tags_name = self.tree.xpath('//*[@id="detailsbd"]/div[1]/div[3]/div[3]/a/span/text()')
        for name, url in zip(tags_name, tags_urls):
            tag = {'name': name, 'url': 'https://www.pearvideo.com/' + url}
            tags.append(tag)
        return tags

    def get_video(self):
        pass


if __name__ == '__main__':
    print(VideoParser.get_tree('https://www.pearvideo.com/video_1538727').get_tags())
