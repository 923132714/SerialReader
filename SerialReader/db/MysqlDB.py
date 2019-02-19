"""
@Time  : 2019/2/18 16:24
@author Logic923
@Project : SerialReader
@FileName: MysqlDB.py
@Software: PyCharm
"""
import pymysql


class MysqlDB:

    def __enter__(self):
        """
        调用前链接数据库
        :return:
        """
        # connect database
        self.db = pymysql.connect("localhost", "logic", "logic", "logic")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close

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
