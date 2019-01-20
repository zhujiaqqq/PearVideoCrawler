# config={
#     "host":"127.0.0.1",
#     "user":"root",
#     "password":"root",
#     "database":"pear"
# }
#
# db = pymysql.connect(**config)
#
# cursor = db.cursor()
#
# sql = 'insert pear_author (name, url) values (%(name)s,%(url)s)'
# author={'name':"zzzz","url":"sdsd"}
# cursor.execute(sql,author)
#
# cursor.execute('select * from pear_author')
#
# data = cursor.fetchall()
#
# print(data)
#
# cursor.close()
# db.close()


import logging
import sys

import pymysql

# 加入日志
# 获取logger实例
logger = logging.getLogger("baseSpider")
# 指定输出格式
formatter = logging.Formatter('%(asctime)s\
              %(levelname)-8s:%(message)s')
# 文件日志
file_handler = logging.FileHandler("baseSpider.log")
file_handler.setFormatter(formatter)
# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# 为logge添加具体的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.setLevel(logging.INFO)


class DBHelper:
    # 构造函数
    def __init__(self, host='127.0.0.1', user='root',
                 pwd='root', db='pear'):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.conn = None
        self.cur = None

    # 连接数据库
    def connect_database(self):
        try:
            self.conn = pymysql.connect(self.host, self.user,
                                        self.pwd, self.db, charset='utf8')
        except:
            logger.error("connectDatabase failed")
            return False
        self.cur = self.conn.cursor()
        return True

    # 关闭数据库
    def close(self):
        # 如果数据打开，则关闭；否则没有操作
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
        return True

    # 执行数据库的sq语句,主要用来做插入操作
    def execute(self, sql, params=None):
        # 连接数据库
        self.connect_database()
        try:
            if self.conn and self.cur:
                # 正常逻辑，执行sql，提交操作
                self.cur.execute(sql, params)
                self.conn.commit()
        except:
            logger.error("execute failed: " + sql)
            logger.error("params: " + params)
            self.close()
            return False
        return True

    # 用来查询表数据
    def fetchall(self, sql, params=None):
        self.execute(sql, params)
        return self.cur.fetchall()


if __name__ == '__main__':
    dbHelper = DBHelper()
    # 创建数据库的表
    # sql = "create table maoyan('id'varchar(8),\
    #         'title'varchar(50),\
    #         'star'varchar(200), \
    #         'time'varchar(100),primary key('id'));"
    # result = dbHelper.execute(sql, None)
    # if result:
    #     logger.info("maoyan　table创建成功")
    # else:
    #     logger.error("maoyan　table创建失败")
    sql = "select name from pear_video where name = %s"
    args=['微波炉和马克杯就可以做的蛋糕2选']
    result = dbHelper.fetchall(sql,args)
    print(len(result))

    pass
