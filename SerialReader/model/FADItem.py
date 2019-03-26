import datetime

class FADItem(object):
    '''
    Frash Air Data Item
    @input bytelist 串口数据(16位)
    '''

    def __init__(self, RX_BUF):

        self.__RX_BUF = RX_BUF

    # Data identification
    def data_identification(self):
        if not self.__RX_BUF[0] == 170 and self.__RX_BUF[1] == 90:
            print("Data identification error")
            return False
        elif self.data_check():
            print("Data check succeeded")
            return True
        else:
            print("Data checksum mistake")
            return False

    # Data check
    def data_check(self):
        check = self.__RX_BUF[14] + self.__RX_BUF[15]
        # print(type(check))
        check_sum = 0
        for index in range(0, 14):
            # print(self.__RX_BUF[index])
            check_sum += self.__RX_BUF[index]
        print("check = %s, check_sum = %s"%(check,check_sum))

        return check_sum%255==check

    # Read conversion PM2.5 data
    def get_pm2(self):
        pm2 = self.__RX_BUF[2] * 256 + self.__RX_BUF[3]

        return pm2

    def get_pm10(self):
        # Read conversion PM10 data
        pm10 = self.__RX_BUF[4] * 256 + self.__RX_BUF[5]

        return pm10

    def get_temp(self):
        # Read conversion temp data
        if (self.__RX_BUF[6] & 0x80):
            temp = -((self.__RX_BUF[6] & 0x7f) * 256 + self.__RX_BUF[7])
        else:
            temp = self.__RX_BUF[6] * 256 + self.__RX_BUF[7]

        temp = temp / 10

        return temp

    def get_humi(self):
        # Read conversion humi data
        humi = self.__RX_BUF[8] * 256 + self.__RX_BUF[9]

        humi = humi / 10

        return humi

    def get_addr(self):
        # Read collection point address
        addr = self.__RX_BUF[13]
        return addr

    def get_datetime(self):
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return dt