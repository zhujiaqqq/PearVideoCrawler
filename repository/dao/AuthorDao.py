from repository.MysqlRepo import MysqlHelper


class AuthorDao:
    """
+-------------+----------------------+------+-----+---------+----------------+
| Field       | Type                 | Null | Key | Default | Extra          |
+-------------+----------------------+------+-----+---------+----------------+
| id          | smallint(5) unsigned | NO   | PRI | NULL    | auto_increment |
| author_name | varchar(40)          | NO   |     | NULL    |                |
| home_url    | varchar(255)         | NO   |     | NULL    |                |
| info        | varchar(255)         | YES  |     | NULL    |                |
+-------------+----------------------+------+-----+---------+----------------+
    """

    @classmethod
    def insert(cls, author_name, home_url, info):
        sql = "insert into pear_author (author_name, home_url, info) " \
              "values ('%s','%s','%s') " % \
              (author_name, home_url, info)

        helper = MysqlHelper()
        if helper:
            return helper.execute(sql)
        else:
            return False

    @classmethod
    def find_by_id(cls, id):
        sql = "select * from pear_author where id = %s" % id
        helper = MysqlHelper()
        if helper:
            return helper.fetch_all(sql)
        else:
            return False

    @classmethod
    def find_all(cls):
        sql = "select * from pear_author"
        helper = MysqlHelper()
        if helper:
            return helper.fetch_all(sql)
        else:
            return False


if __name__ == '__main__':
    results = AuthorDao.find_all()
    for i in results:
        print(i)
