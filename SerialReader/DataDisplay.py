"""
@Time  : 2019/2/19 13:36
@author Logic923
@Project : SerialReader
@FileName: DataDisplay.py
@Software: PyCharm
"""
from threading import Thread

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 解决中文乱码问题
from db.MysqlDB import MysqlDB

myfont = fm.FontProperties(fname= r"C:\\WINDOWS\\Fonts\\simsun.ttc" , size=14)
matplotlib.rcParams["axes.unicode_minus"] = False


class DataDisplay:
    def __init__(self):

        self._data = []
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("type: ", exc_type)
        print("val: ", exc_val)
        print("tb: ", exc_tb)


    @property
    def data(self):
        if None == self._data  :
            return None
        return  self._data

    @data.setter
    def data(self, value):
        self._data = value

    def get_data(self):
        with MysqlDB() as mydb:
            self.data = mydb.select_air_quality_data()

    def display_air_quality_data(self):
        plt.figure(1,figsize=(12, 10), dpi=80)

        re = ""

        while True:

            # 协程
            flag = yield re
            if flag == False:
                return False
            plt.ion()
            self.get_data()
            data = self.data
            if [] == data or None == data:
                print("ERROR data is empty")
                return None
            time, pm2, pm10, humi, temp = [], [], [], [], []
            for item in data:
                time.append(item['time'])
                pm2.append(item['pm2'])
                pm10.append(item['pm10'])
                temp.append(item["temp"])
                humi.append(item["humi"])

            plt.clf()
            plt.subplot(212)

            plt.title("pm2.5/10变化图", fontproperties=myfont)
            plt.grid(True)  # 网格

            plt.xlabel("时间", fontproperties=myfont)
            plt.xticks(rotation=50)
            plt.ylabel("数值", fontproperties=myfont)
            #
            # time ,pm2,pm10= [item['time'] for item in data],\
            #                 [item['pm2'] for item in data], \
            #                 [item['pm10'] for item in data], \


            plt.plot(time,pm2,'b--',linewidth=1.0,label="pm2.5")
            plt.plot(time, pm10, 'g-', linewidth=1.0, label="pm10")

            # 图例位置
            plt.legend(loc="upper left", prop= myfont , shadow = True)


            # 温度
            plt.subplot(221)
            plt.title("温度变化图", fontproperties=myfont)
            plt.grid(True)  # 网格

            plt.xlabel("时间", fontproperties=myfont)
            plt.xticks(rotation=50)
            plt.ylabel("数值", fontproperties=myfont)
            plt.plot(time, temp, 'b--', linewidth=1.0, label="temp")

            # 湿度
            plt.subplot(222)

            plt.title("湿度变化图", fontproperties=myfont)
            plt.grid(True)  # 网格

            plt.xlabel("时间", fontproperties=myfont)
            plt.xticks(rotation=50)
            plt.ylabel("数值", fontproperties=myfont)
            plt.plot(time, humi, 'b--', linewidth=1.0, label="humi")


            # plt.subplots_adjust(wspace=1, hspace=2)  # 调整子图间距
            plt.tight_layout()

            re = "400 OK"
            plt.pause(0.001)
            plt.ioff()
        # plt.ioff()
        plt.show()

        return

if __name__ == '__main__':
    DataDisplay().display_air_quality_data()