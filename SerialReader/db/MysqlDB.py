"""
@Time  : 2019/2/18 16:24
@author Logic923
@Project : SerialReader
@FileName: MysqlDB.py
@Software: PyCharm
"""
import pymysql

from db.Memory import Memory


class MysqlDB(Memory):
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

        print("-----MysqlDB __enter__-----")

        # connect database
        # self.db = pymysql.connect("localhost", "logic", "logic", "logic")
        self.db = pymysql.connect(**self.config)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("-----MysqlDB __exit__-----")
        print("type: ", exc_type)
        print("val: ", exc_val)
        print("tb: ", exc_tb)
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
            # 获取会话指针
            with self.db.cursor() as cursor:
            # execute sql
                result = cursor.execute(sql)
                # commit sql
                self.db.commit()
                return result
        except:
            print("something error ")
            self.db.rollback()
            return False

    def select_air_quality_data(self, line=50):
        serials_data ={}
        sql = """SELECT id,pm2,pm10,temp,humi,addr,time 
        from fresh_air ORDER BY id DESC LIMIT %s""" %\
              (line,)
        try:
            # 获取会话指针
            with self.db.cursor() as cursor:
                # 执行sql语句
                conut = cursor.execute(sql) # 行数
                print(conut)
                # 查询数据
                result = cursor.fetchall()      # 查询所有数据
                print(result)

                # {'id': 93, 'pm2': 125.0, 'pm10': 143.0,
                #  'temp': 28.0, 'humi': 23.0, 'addr': 15,
                #  'time': datetime.datetime(2019, 2, 19, 13, 1, 32)}
                return result[::-1]
        except:
            print("something error ")
            self.db.rollback()
            return False

if __name__ == '__main__':
    with MysqlDB() as mydb:
        mydb.select_air_quality_data()