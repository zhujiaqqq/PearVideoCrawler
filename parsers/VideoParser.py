import re

import requests
from lxml import etree


class VideoParser:
    """
    https://www.pearvideo.com/video_1538727
    """

    def __init__(self, tree, response):
        self.tree = tree
        self.response = response

    @classmethod
    def get_tree(cls, url, params=None, headers=None):
        response = requests.get(url=url, params=params, headers=headers)
        tree = etree.HTML(response.content.decode('utf-8'))
        return cls(tree, response)

    def get_author(self) -> dict:
        """
        获取作者信息
        :return:
        """
        try:
            author_url = self.tree.xpath('//*[@id="detailsbd"]/div[1]/div[3]/div[1]/div[1]/a/@href')
            if author_url is not None:
                author_url = author_url[0]
            else:
                author_url = ''
            author_name = self.tree.xpath('//*[@id="detailsbd"]/div[1]/div[3]/div[1]/div[1]/a/div/text()')[0]
            author_info = self.tree.xpath('//*[@id="detailsbd"]/div[1]/div[3]/div[1]/div[1]/a/text()')[0]
            author = {'name': author_name, 'url': 'https://www.pearvideo.com/' + author_url, 'info': author_info}
        except:
            author = {'name': '', 'url': '', 'info': ''}
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
            tag_id = url[url.find('_') + 1:]
            tag = {'name': name, 'url': 'https://www.pearvideo.com/' + url, 'id': tag_id}
            tags.append(tag)
        return tags

    def get_video(self) -> dict:
        res = re.findall('srcUrl="(.*\.mp4)', self.response.text)
        res = set(res)
        try:
            video_url = res.pop()
            video_img_url = self.tree.xpath('//*[@id="poster"]/img/@src')[0]
            video_date = self.tree.xpath('//*[@id="detailsbd"]/div[1]/div[2]/div/div[1]/div/div[1]/text()')[0]
            video_content = self.tree.xpath('//*[@id="detailsbd"]/div[1]/div[3]/div[1]/div[2]/text()')[0]
            video_title = self.tree.xpath('//*[@id="detailsbd"]/div[1]/div[2]/div/div[1]/h1/text()')[0]
            video = {'title': video_title, 'url': video_url, 'img': video_img_url, 'date': video_date,
                     'content': video_content}
        except:
            video = {'title': '', 'url': '', 'img': '', 'date': '', 'content': ''}
        return video
        pass


if __name__ == '__main__':
    print(VideoParser.get_tree('https://www.pearvideo.com/video_1538727').get_tags())
