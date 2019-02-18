#!/usr/bin/env python
#-*- coding: utf-8 -*
import serial
import serial.tools.list_ports



from RXBuffer import RXBuffer
from db import serial_DB
from excel_save import Excel_io


class MySerial(object):


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
            comlist_0 =list(plist[0])
            print("COM list:")
            print(comlist_0)
        return comlist_0

    def __get_serial_name(self):

        comlist_0 = self.__get_serial_list();
        self.__serial_name = comlist_0[0]
        print("connect serial " + self.__serial_name)

        return self.__serial_name

    def connect_serial(self):
        # connect serial
        self.__ser = serial.Serial(self.__get_serial_name(),
                                   9600, timeout=60)
        if self.__ser: return self.__ser
        else:return None

    def read_line(self):
        print("in waitting byte :%s"%self.__ser.inWaiting())
        self.__ser.reset_input_buffer()
        RX_BUF = self.__ser.read(16)
        # print("RX_BUF %s"%RX_BUF.hex())

        rx_buffer = RXBuffer(RX_BUF)



        if not rx_buffer.data_identification():
            return None
        else:
            rx_buffer.data_check()
            self.__pm2 = rx_buffer.get_pm2()
            self.__pm10 = rx_buffer.get_pm10()
            self.__temp = rx_buffer.get_temp()
            self.__humi = rx_buffer.get_humi()
            self.__addr = rx_buffer.get_addr()
            self.__datetime = rx_buffer.get_datetime()
            print("DATA[ "+self.to_string()+ " ]")
            return True


    def save_serial_data_to_mysql(self):

        if self.__pm2 and self.__pm10 and self.__temp and\
                self.__humi and   self.__addr and  self.__datetime:
            result = serial_DB.commit_air_quality_data(
                self.__pm2, self.__pm10, self.__temp,
                self.__humi, self.__addr, self.__datetime)

            return result
        else:
            print("Missing data ")
            return None

    def save_serial_data_to_excel(self):

        if self.__pm2 and self.__pm10 and self.__temp and\
                self.__humi and   self.__addr and  self.__datetime:


            serial_data ={ "pm2.5":self.__pm2, "pm10":self.__pm10,
            "temp":self.__temp, 'humi': self.__humi,
            "addr": self.__addr, "time": self.__datetime}
            print(serial_data)
            excel = Excel_io("fresh_air_data.xls")

            result = excel.write_data(serial_data)

            return result
        else:
            print("Missing data ")
            return None


    def to_string(self):

        return """pm2 = %s, pm10 = %s,temp = %s, humi = %s,"""\
               """addr = %s, datetime = %s"""%\
               (self.__pm2,self.__pm10, self.__temp, self.__humi,self.__addr,self.__datetime)
