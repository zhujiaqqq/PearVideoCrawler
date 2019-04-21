from repository.MysqlRepo import MysqlHelper


class TagDao:
    """
+-----------------+--------------+------+-----+---------+----------------+
| Field           | Type         | Null | Key | Default | Extra          |
+-----------------+--------------+------+-----+---------+----------------+
| id              | int(11)      | NO   | PRI | NULL    | auto_increment |
| tag_name        | varchar(255) | NO   |     | NULL    |                |
| tag_id          | varchar(20)  | NO   |     | NULL    |                |
| tag_addr        | varchar(255) | NO   |     | NULL    |                |
| tag_video_count | int(11)      | YES  |     | NULL    |                |
+-----------------+--------------+------+-----+---------+----------------+
    """

    @classmethod
    def insert(cls, tag_name, tag_id, tag_addr, tag_video_count):
        sql = "insert into pear_tag (tag_name, tag_id, tag_addr, tag_video_count) " \
              "values ('%s','%s','%s','%s') " % \
              (tag_name, tag_id, tag_addr, tag_video_count)

        helper = MysqlHelper()
        if helper:
            return helper.execute(sql)
        else:
            return False

    @classmethod
    def find_by_id(cls, id):
        sql = "select * from pear_tag where id = %s" % id
        helper = MysqlHelper()
        if helper:
            return helper.fetch_all(sql)
        else:
            return False

    @classmethod
    def find_all(cls):
        sql = "select * from pear_tag"
        helper = MysqlHelper()
        if helper:
            return helper.fetch_all(sql)
        else:
            return False

    @classmethod
    def find_all_tag_urls(cls):
        sql = "select tag_addr from pear_tag"
        helper = MysqlHelper()
        res = []
        if helper:
            temp = helper.fetch_all(sql)
            for i in temp:
                res.append(i[0])
        return res


if __name__ == '__main__':
    print(TagDao.find_all_tag_urls())
