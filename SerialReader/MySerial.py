#!/usr/bin/env python
#-*- coding: utf-8 -*
import serial
import serial.tools.list_ports



from model.FADItem import FADItem
from db.MysqlDB import MysqlDB
from db.excel_save import Excel_io


class MySerial(object):

    SLEN = 16 # item length
    fa_data_buffer = [] # data buffer

    def __init__(self):
       pass
    def __get_serial_list(self):
        plist = list(serial.tools.list_ports.comports())
        print("plist")
        print(plist)
        if len(plist)<=0:
            print("Unable to find port list.")
            return None
        else:
            return plist



    def __get_serial_name(self):

        plist = self.__get_serial_list();

        lens = len(plist)
        com = lens+1
        while not com<=lens and com > 0:
            print("COM list:")
            for i in range(0,lens):
                print("(",i+1,")", plist[i])
            com = int(input("select COM with input number:"))

        comlist  = list(plist[com-1])
        print("COM info:")
        print(comlist)
        self.__serial_name = comlist[0]
        print("connect serial " + self.__serial_name)

        return self.__serial_name

    def connect_serial(self):
        # connect serial
        self.__ser = serial.Serial(self.__get_serial_name(),
                                   9600, timeout=60)
        if self.__ser: return self.__ser
        else:return None

    def read_gift(self):
        '''
        Empty fa_data_buffer , read all sensor data and save to fa_data_buffer.
        :return:
        '''
        self.fa_data_buffer = []
        print("in waitting byte :%s"%self.__ser.inWaiting())
        self.__ser.reset_input_buffer()
        buffer = self.__ser.read(self.SLEN)

        # print("RX_BUF %s"%RX_BUF.hex())

        # flag = self.__ser.inWaiting()//self.SLEN
        flag = 3
        self.packaged_data(buffer)
        while flag:
            flag-=1
            buffer = self.__ser.read(self.SLEN)
            self.packaged_data(buffer)
        return True

    def packaged_data(self, buffer):
        '''
        packaged all data, sava it to object.
        :param buffer:serial_data
        :return:
        '''

        fad_item = FADItem(buffer)
        if not fad_item.data_identification():
            return None
        else:
            fad_item.data_check()
            serial_data = {"pm2.5": fad_item.get_pm2(), "pm10":fad_item.get_pm10(),
                           "temp": fad_item.get_temp(), 'humi': fad_item.get_humi(),
                           "addr":fad_item.get_addr(), "time": fad_item.get_datetime()}
            self.fa_data_buffer.append(serial_data)
            print("DATA[ " + serial_data.__repr__() + " ]")
            return True


    def save_serial_data_to_mysql(self):

        if self.__pm2 and self.__pm10 and self.__temp and\
                self.__humi and   self.__addr and  self.__datetime:

            serial_data = {"pm2.5": self.__pm2, "pm10": self.__pm10,
                           "temp": self.__temp, 'humi': self.__humi,
                           "addr": self.__addr, "time": self.__datetime}
            print(serial_data)
            with  MysqlDB() as mydb:
                result = mydb.commit_air_quality_data(serial_data)

            return result
        else:
            print("Missing data ")
            return None

    def save_serial_data_to_excel(self):
        '''

        :return:
        '''

        # if self.__pm2 and self.__pm10 and self.__temp and\
        #         self.__humi and   self.__addr and  self.__datetime:
        for serial_data in self.fa_data_buffer:

            print(serial_data)
            excel = Excel_io("fresh_air_data_%a.xls"%serial_data["addr"])

            result = excel.write_data(serial_data)
            print(result)
        return True

    def __repr__(self):
        return self.fa_data_buffer.__repr__()
        # return """pm2 = %s, pm10 = %s,temp = %s, humi = %s,"""\
        #        """addr = %s, datetime = %s"""%\
        #        (self.__pm2,self.__pm10, self.__temp, self.__humi,self.__addr,self.__datetime)

if __name__ == "__main__":
    hh = ["asda","safa"]
    print(len(hh))
    com = int(input("select COM with input number:"))
    print(com)
    print(isinstance(com,int))
