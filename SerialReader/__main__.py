#!/usr/bin/env python
# -*- coding: utf-8 -*
import time
import os

from MySerial import MySerial

myserial = MySerial()
if myserial.connect_serial():
    while myserial.read_line():
        # save to mysql

        result = myserial.save_serial_data_to_mysql

        # save to excel
        # result = myserial.save_serial_data_to_excel()
        if result is None :
            print("save failure")
        elif result > 0  :
            print("save successfully" +str(result))
        elif result == 0:
            print("No modification" +str(result))
        else:
            print("some thing error" + str(result))
            os._exit(result)
        time.sleep(10)
else:
    print("None equipment")

