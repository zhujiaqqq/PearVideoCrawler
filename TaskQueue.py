from queue import Queue


class TaskQueue(object):
    """
    数据队列
    """
    videoQueue = Queue()
    authorQueue = Queue()
    tagQueue = Queue()

    def __init__(self):
        pass

    @classmethod
    def getVideoQueue(cls):
        return cls.videoQueue

    @classmethod
    def getAuthorQueue(cls):
        return cls.authorQueue

    @classmethod
    def getTagQueue(cls):
        return cls.tagQueue

    @classmethod
    def isVideoQueueEmpty(cls):
        return cls.videoQueue.empty()

    @classmethod
    def isAuthorQueueEmpty(cls):
        return cls.authorQueue.empty()

    @classmethod
    def isTagQueueEmpty(cls):
        return cls.tagQueue.empty()

    @classmethod
    def putToVideoQueue(cls, item):
        return cls.videoQueue.put(item)

    @classmethod
    def putToAuthorQueue(cls, item):
        return cls.authorQueue.put(item)

    @classmethod
    def putToTagQueue(cls, item):
        return cls.tagQueue.put(item)

    @classmethod
    def getFromVideoQueue(cls):
        return cls.videoQueue.get() @ classmethod

    def getFromAuthorQueue(cls):
        return cls.authorQueue.get() @ classmethod

    def getFromTagQueue(cls):
        return cls.tagQueue.get()
