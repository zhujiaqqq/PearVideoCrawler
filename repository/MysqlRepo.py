import logging
import sys
import pymysql

logger = logging.getLogger("mysql_repo")

formatter = logging.Formatter('%(asctime)s\
              %(levelname)-8s:%(message)s')

# file_handler = logging.FileHandler('pearVideo.log')
# file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.setLevel(logging.DEBUG)


class MysqlHelper:
    def __init__(self,
                 host='127.0.0.1',
                 user='root',
                 pwd='root',
                 db='pear'):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.conn = None
        self.cur = None

    def connect_database(self):
        """
        连接数据库
        :return: True 成功；False 失败
        """
        try:
            self.conn = pymysql.connect(self.host,
                                        self.user,
                                        self.pwd,
                                        self.db,
                                        charset='utf8')
        except pymysql.Error:
            logging.error('connect database failed')
            return False

        self.cur = self.conn.cursor()
        return True

    def close(self):
        """
        关闭数据库
        :return: True 成功
        """
        if self.conn and self.cur:
            self.conn.close()
            self.cur.close()
        return True

    def execute(self, sql, params=None):
        """
        执行数据
        :param sql: sql语句模版
        :param params: 参数
        :return: True 成功；False 失败
        """
        self.connect_database()
        try:
            if self.conn and self.cur:
                self.cur.execute(sql, params)
                self.conn.commit()

        except pymysql.Error:
            # logger.error("execute failed: " + sql)
            # logger.error("params: " + params)
            self.conn.rollback()
            self.close()
            return False
        return True

    def fetch_all(self, sql, params=None):
        """
        查询表中所有数据
        :param sql:数据库模版
        :param params:参数
        :return:查询结果
        """
        self.execute(sql, params)
        return self.cur.fetchall()

    def fetch_one(self, sql, params):
        """
        查询单个结果
        :param sql: 数据库模版
        :param params: 参数
        :return: 查询结果
        """
        self.execute(sql, params)
        return self.cur.fetchone()


if __name__ == '__main__':

    helper = MysqlHelper()
    results = helper.fetch_all('select * from pear_video limit 10')
    for row in results:
        print(row)
