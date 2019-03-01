#!/usr/bin/env python
# -*- coding: utf-8 -*
import time
import os

from DataDisplay import DataDisplay
from MySerial import MySerial

myserial = MySerial()
if myserial.connect_serial():
    #
    # display = DataDisplay()
    # draw = display.display_air_quality_data()
    # draw.send(None)

    while myserial.read_line():
        # save to mysql

        # result = myserial.save_serial_data_to_mysql

        # save to excel
        result = myserial.save_serial_data_to_excel()
        if result is None :
            print("-----save failure-----")
        elif result > 0  :
            print("-----save successfully-----" +str(result))
            # draw.send(True)
        elif result == 0:
            print("-----No modification-----" +str(result))
        else:
            print("-----some thing error-----" + str(result))
            # draw.close()
            os._exit(result)
        time.sleep(10)
else:
    print("None equipment")

