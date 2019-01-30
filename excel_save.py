# -*- coding: utf-8 -*-

"""
@author Logic923
"""


import re
import tkinter
import tkinter.messagebox #这个是消息框，对话框的关键

import xlwt
from xlwt import Workbook
from xlrd import open_workbook
from xlutils.copy import copy

class Excel_io():

    def write_row(self,sheet,row,serials_data):
        '''
        写入一行数据，未保存，供类内部使用。
        :param sheet: 表对象
        :param row: 写入行
        :param serials_data: 数据字典
        :return:
        '''
        sheet.write(row,0,serials_data['pm2.5'])
        sheet.write(row,1,serials_data['pm10'])
        sheet.write(row,2,serials_data['temp'])
        sheet.write(row,3,serials_data['humi'])
        sheet.write(row,4,serials_data['addr'])
        sheet.write(row,5,serials_data['time'])

    def create_excel(self,filename):
        '''
        新建数据excel文件
        :param filename: 文件名
        :return:
        '''
        book = Workbook(encoding='utf-8')
        sheet1 = book.add_sheet('Sheet 1')
        # pm2, pm10, temp, humi, addr, time
        # 写入抬头
        head ={ "pm2.5":"pm2.5", "pm10":"pm10",
                "temp":"temp", 'humi':'humi',
                "addr":"addr", "time":"time"}
        self.write_row(sheet1,0,head)

        return book.save(filename)

    def __init__(self,filename):
        '''
        构造函数，打开文件，没有则新建。
        :param filename: 文件名
        '''
        pattern = re.compile(r'(.)*\.xls')
        m = pattern.match(filename)
        if(m==None):
            filename = "fresh_air.xls"
        self.filename = filename
        try:
            rexcel = open_workbook(filename) # 用wlrd提供的方法读取一个excel文件
            self.row = rexcel.sheets()[0].nrows  # 用wlrd提供的方法获得现在已有的行数
            self.excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
        except FileNotFoundError : # 没有则创建
            self.excel = self.create_excel(filename)
            self.row = 1


    def get_row (self):
        '''
        获取当前行数
        :return:
        '''
        return self.row

    def write_data(self,serials_data):
        '''
        根据数据字典，调用write_row存储数据，成功则行加一
        :param serials_data: 数据字典
        :return: boolean 成功与否
        '''
        try:
            table = self.excel.get_sheet(0) # 用xlwt对象的方法获得要操作的sheet
            # print(table)
            self.write_row(table,self.row,serials_data)
            self.excel.save(self.filename)  # xlwt对象的保存方法，这时便覆盖掉了原来的excel
            self.row+=1
            return True
        except PermissionError:
            tkinter.messagebox.showerror('SerialReader', '请关闭文件:' + self.filename + "后重启程序")
            return -1
        except :
            return False

# haha =Excel_io("hhh.xls")
# print(haha.get_row())