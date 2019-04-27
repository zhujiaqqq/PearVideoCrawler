import random
import threading
import time

from BloomFilter import BloomFilter
from TaskQueue import TaskQueue
from parsers.CategoryParser import CategoryParser
from parsers.VideoParser import VideoParser
from repository.dao.AuthorDao import AuthorDao
from repository.dao.TagDao import TagDao
from repository.dao.VideoDao import VideoDao


def formatParams(req_type: int, category_id: int, start: int) -> dict:
    return {
        'reqType': req_type,
        'categoryId': category_id,
        'start': start
    }


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

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/71.0.3578.98 Safari/537.36'
}


class Robot:

    def __init__(self,
                 video_filter: BloomFilter,
                 author_filter: BloomFilter,
                 tag_filter: BloomFilter,
                 task_queue: TaskQueue):
        self.v_filter = video_filter
        self.a_filter = author_filter
        self.t_filter = tag_filter
        self.task_queue = task_queue

    def initFilter(self, urls: list, authors: list, tags: list):
        """
        将数据载入到过滤器
        :param urls:
        :return:
        """
        print('加载数据库中视频数据到布隆过滤器')
        ts = int(round(time.time() * 1000))

        for url in urls:
            self.v_filter.add(url)
        for author_url in authors:
            self.a_filter.add(author_url)
        for tag_url in tags:
            self.t_filter.add(tag_url)

        te = int(round(time.time() * 1000))
        print('加载完成,耗时 %s ms' % (te - ts))

    def urlIsExist(self, url: str) -> bool:
        """
        URL是否已存在数据库
        :param url:
        :return: True 已存在；False 不存在
        """
        return self.v_filter.contains(url)

    def urlAddToFilter(self, url: str):
        """
        将新URL加入过滤器
        :param url:
        :return:
        """
        self.v_filter.add(url)

    def getVideoByCategory(self, category_id: str) -> list:
        """
        抓取单个类别到视频URL
        :param category_id: 类别名称
        :return: 视频URL list
        """
        ts = int(round(time.time() * 1000))
        res = []
        for i in range(0, 999, 12):
            # 随机等待2-6s
            time.sleep(random.randrange(2, 6))
            params = formatParams(5, int(category_id), i)
            video_urls = CategoryParser.get_tree('https://www.pearvideo.com/category_loading.jsp?', params,
                                                 headers).get_video_urls()
            exist_count = 0

            for url in video_urls:
                if self.v_filter.contains(url):
                    exist_count += 1
                    print(exist_count)
                else:
                    # print(url)
                    res.append(url)
                    self.task_queue.putToVideoQueue(url)

            if exist_count == 12:
                break
        te = int(round(time.time() * 1000))
        print('当前类别搜索完毕,耗时 %s ms' % (te - ts))
        print('抓取 %s 个视频地址' % len(res))
        return res

    def getAllCategoriesVideos(self) -> list:
        """
        获取各类别到视频url
        :return: 视频URL list
        """
        res = []
        for i in CHANNEL_MAP.keys():
            print('当前类别：%s' % i)
            temp = self.getVideoByCategory(CHANNEL_MAP[i])
            res.append(temp)
        return res

    def getVideoInfo(self, url: str):
        video_tree = VideoParser.get_tree(url, headers=headers)
        author = self.getAuthorByVideoPage(video_tree)

        self.getTagsByVideoPage(video_tree)

        self.getVideoByVideoPage(author, url, video_tree)
        pass

    def getVideoByVideoPage(self, author, url, video_tree):
        """
        在视频页面获取video信息，并存入数据库
        :param author:
        :param url:
        :param video_tree:
        :return:
        """
        video = video_tree.get_video()
        if not self.v_filter.contains(video['url']):
            print(video.get('title'))
            VideoDao.insert(name=video['title'],
                            author=author,
                            page_url=url,
                            video_url=video['url'],
                            image_url=video['img'],
                            create_time=video['date'],
                            content=video['content'])
            self.v_filter.add(video['url'])
        pass

    def getTagsByVideoPage(self, video_tree):
        """
        在视频页面获取tag信息，并存入数据库
        :param video_tree:
        :return:
        """
        tags = video_tree.get_tags()
        for tag in tags:
            # print(tag)
            if not self.t_filter.contains(tag['url']):
                TagDao.insert(tag_name=tag['name'],
                              tag_id=tag['id'],
                              tag_addr=tag['url'],
                              tag_video_count='0')
                self.t_filter.add(tag['url'])
        pass

    def getAuthorByVideoPage(self, video_tree) -> str:
        """
        在视频页面获取author信息，并存入数据库
        :param video_tree:
        :return:
        """
        author = video_tree.get_author()
        # print(author)
        if not self.a_filter.contains(author['url']):
            AuthorDao.insert(author_name=author['name'],
                             home_url=author['url'],
                             info=author['info'])
            self.a_filter.add(author['url'])
        return author['name']


isRunning = True


class Producer(threading.Thread):
    def __init__(self, robot: Robot):
        super().__init__()
        self.robot = robot

    def run(self):
        global isRunning

        robot.getAllCategoriesVideos()
        isRunning = False


class Consumer(threading.Thread):
    def __init__(self, robot: Robot):
        super().__init__()
        self.robot = robot

    def run(self):

        while isRunning:

            if not self.robot.task_queue.isVideoQueueEmpty():
                url = self.robot.task_queue.getFromVideoQueue()
                self.robot.getVideoInfo(url)
            else:
                print('等待中...')
                time.sleep(random.randrange(5, 10))


if __name__ == '__main__':
    v_bloom = BloomFilter(500000)
    a_bloom = BloomFilter(10000)
    t_bloom = BloomFilter(30000)
    task_queue = TaskQueue()
    robot = Robot(v_bloom, a_bloom, t_bloom, task_queue)
    currentVideos = VideoDao.find_all_video_urls()
    currentAuthors = AuthorDao.find_all_author_urls()
    currentTags = TagDao.find_all_tag_urls()

    robot.initFilter(currentVideos, currentAuthors, currentTags)

    p = Producer(robot=robot)
    p.start()

    time.sleep(10)
    c = Consumer(robot=robot)
    c.start()

