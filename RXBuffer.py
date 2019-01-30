import datetime

class RXBuffer(object):

    def __init__(self, RX_BUF):

        self.__RX_BUF = RX_BUF

    # Data identification
    def data_identification(self):
        if not self.__RX_BUF[0] == 170 and self.__RX_BUF[1] == 90:
            print("Data identification error")
            return False
        else:
            print("Data header verification succeeded")
            return True

    # Data check
    def data_check(self):
        check = self.__RX_BUF[14] + self.__RX_BUF[15]
        # print(type(check))
        check_sum = 0
        for index in range(0, 14):
            # print(self.__RX_BUF[index])
            check_sum += self.__RX_BUF[index]
        print("check = %s, check_sum = %s"%(check,check_sum))

        # print(check_sum & 0b11111111)
        # print(type(check_sum))
        # print(check_sum & 255)
        return check_sum&255==check

    # Read conversion PM2.5 data
    def get_pm2(self):
        pm2 = self.__RX_BUF[2] * 256 + self.__RX_BUF[3]
        # print("pm2.5 = ")
        # print(pm2)
        return pm2

    def get_pm10(self):
        # Read conversion PM10 data
        pm10 = self.__RX_BUF[4] * 256 + self.__RX_BUF[5]
        # print("pm10 = ")
        # print(pm10)
        return pm10

    def get_temp(self):
        # Read conversion temp data
        if (self.__RX_BUF[6] & 0x80):
            temp = -((self.__RX_BUF[6] & 0x7f) * 256 + self.__RX_BUF[7])
        else:
            temp = self.__RX_BUF[6] * 256 + self.__RX_BUF[7]
        # print("temp = ")
        temp = temp / 10
        # print(temp)
        return temp

    def get_humi(self):
        # Read conversion humi data
        humi = self.__RX_BUF[8] * 256 + self.__RX_BUF[9]

        # print("humi = ")
        humi = humi / 10
        # print(humi)
        return humi

    def get_addr(self):
        # Read collection point address
        addr = self.__RX_BUF[13]
        # print("addr = ")
        # print(addr)
        return addr

    def get_datetime(self):
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # print("datetime : " + dt)
        return dt