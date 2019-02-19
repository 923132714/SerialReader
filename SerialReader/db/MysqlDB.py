"""
@Time  : 2019/2/18 16:24
@author Logic923
@Project : SerialReader
@FileName: MysqlDB.py
@Software: PyCharm
"""
import pymysql


class MysqlDB:
    # 连接配置信息
    config = {
        'host': '127.0.0.1',
        'port': 3306,  # MySQL默认端口
        'user': 'logic',  # mysql默认用户名
        'password': 'logic',
        'db': 'logic',  # 数据库
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
    }

    def __init__(self):
        pass

    def __enter__(self):
        """
        调用前链接数据库
        :return: MysqlDB
        """

        print("MysqlDB __enter__")

        # connect database
        # self.db = pymysql.connect("localhost", "logic", "logic", "logic")
        self.db = pymysql.connect(**self.config)

        self.cursor = self.db.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("MysqlDB __exit__")
        self.db.close()

    def commit_air_quality_data(self, serials_data):
        '''
            根据数据字典，调用write_row存储数据，成功则行加一
            :param serials_data: 数据字典
            :return: boolean 成功与否
        '''

        # insert statement
        sql = """INSERT INTO fresh_air(pm2,pm10,temp,humi,addr,time) \
           values (%s, %s,  %s,  %s, %s, '%s' )""" % \
              (serials_data['pm2.5'], serials_data["pm10"], \
               serials_data["temp"], serials_data["humi"], \
               serials_data["addr"], serials_data["time"])
        print(sql)
        try:
            # execute sql

            result = self.cursor.execute(sql)
            # commit sql
            self.db.commit()
            return result
        except:
            print("something error ")
            self.db.rollback()
            return False
    def select_air_quality_data(self,line=8):
        sql = """SELECT INTO fresh_air(pm2,pm10,temp,humi,addr,time) \
                   values (%s, %s,  %s,  %s, %s, '%s' )""" % \
              (serials_data['pm2.5'], serials_data["pm10"], \
               serials_data["temp"], serials_data["humi"], \
               serials_data["addr"], serials_data["time"])
        print(sql)