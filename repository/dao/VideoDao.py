from repository.MysqlRepo import MysqlHelper


class VideoDao:
    """
+-------------+------------------+------+-----+---------+----------------+
| Field       | Type             | Null | Key | Default | Extra          |
+-------------+------------------+------+-----+---------+----------------+
| id          | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
| name        | varchar(255)     | NO   |     | NULL    |                |
| author      | varchar(40)      | NO   |     | NULL    |                |
| page_url    | varchar(255)     | NO   |     | NULL    |                |
| video_url   | varchar(255)     | YES  |     | NULL    |                |
| image_url   | varchar(255)     | YES  |     | NULL    |                |
| create_time | varchar(20)      | YES  |     | NULL    |                |
| content     | varchar(255)     | YES  |     | NULL    |                |
+-------------+------------------+------+-----+---------+----------------+
    """

    @classmethod
    def insert(cls, name, author, page_url, video_url, image_url, create_time, content):
        """
        插入数据
        :param name:
        :param author:
        :param page_url:
        :param video_url:
        :param image_url:
        :param create_time:
        :param content:
        :return:
        """
        sql = "insert into pear_video (name, author, page_url, video_url, image_url, create_time, content) " \
              "values ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
              (name, author, page_url, video_url, image_url, create_time, content)

        helper = MysqlHelper()
        if helper:
            return helper.execute(sql)
        else:
            return False

    @classmethod
    def find_by_id(cls, id):
        """
        通过id查找数据
        :param id:
        :return:
        """
        sql = "select * from pear_video where id = %s" % id
        helper = MysqlHelper()
        if helper:
            return helper.fetch_all(sql)

    @classmethod
    def find_all(cls):
        """
        查询所有数据
        :return:
        """
        sql = "select * from pear_video"
        helper = MysqlHelper()
        if helper:
            return helper.fetch_all(sql)

    @classmethod
    def find_all_video_urls(cls) -> list:
        """
        获取所有video的url数据
        :return: video的url 以list形式
        """
        sql = "select video_url from pear_video"
        helper = MysqlHelper()
        res = []
        if helper:
            temp = helper.fetch_all(sql)
            for i in temp:
                res.append(i[0])
        return res


if __name__ == '__main__':
    # VideoDao.insert("zhujiaqqq", "zhujiaqq", "sss", "sss", "aaa", "bbb", "ccc")
    results = VideoDao.find_all_video_urls()
    print(results)
