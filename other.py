import sys
import os
# import win32api
import datetime
import socket
import requests

class Other_function:
    def __init__(self):
        super().__init__()

    def win_set_time(self, daylist=[]):
        if daylist == []:
            print("day list in none")
        else:
            year = int(daylist[0] + daylist[1])
            month = int(daylist[2])
            day = int(daylist[3])
            dayOfWeek = datetime.date(year, month, day).weekday() + 1
            hour = int(daylist[4])
            minute = int(daylist[5])
            sec = int(daylist[6])

            # win32api.SetSystemTime(year, month, dayOfWeek, day, hour, minute, sec, 0)

    def get_controller_number(self, cont_num):
        datalist = []
        for i in range(0, len(cont_num), 2):
            datalist.append(int(cont_num[i: i + 2], 16))

        result = ''
        for i in datalist:
            result = result + chr(i)
        return result

    def length_calc(self, length):
        length_1 = length & 0xFF
        length_2 = (length >> 8) & 0xFF
        length_3 = (length >> 16) & 0xFF
        length_4 = (length >> 24) & 0xFF

        value = chr(length_4) + chr(length_3) + chr(length_2) + chr(length_1)

        return value

    def make_16ip(self, sip='127.0.0.1'):
        strings = sip.split('.')

        ipli = []
        for spip in strings:
            if len(spip) >= 3:
                ipli.append(spip)
            elif len(spip) == 2:
                three = '0'+spip
                ipli.append(three)
            elif len(spip) == 1:
                three = '00'+spip
                ipli.append(three)

        iplong = '.'.join(ipli)

        return iplong

    def nack_find(self, msg=None, csn=None):
        nacklist=[]
        op = msg[43]
        csn_msg = msg[32:39]
        opcode = [chr(0xFF), chr(0xFE), chr(0x01), chr(0x04), chr(0x05), chr(0x07),
                  chr(0x0C), chr(0x0D), chr(0x0E), chr(0x0F), chr(0x11), chr(0x12),
                  chr(0x13), chr(0x15), chr(0x16), chr(0x17), chr(0x18), chr(0x19), chr(0x1E),]
        try:
            response = requests.get("https://www.naver.com", timeout=2)
        except Exception as ex:
            print("network_check_error")
            nacklist = [False, op, chr(0x01)]
            return nacklist

        if len(msg) < 44:
            nacklist = [False, 0, chr(0x02)]
            return nacklist
        elif csn_msg != csn:
            nacklist = [False, op, chr(0x03)]
            return nacklist
        elif op not in opcode:
            nacklist = [False, op, chr(0x04)]
            return nacklist
        elif len(msg) == 44:
            if op in [chr(0x01),chr(0x0E), chr(0x0F), chr(0x13), chr(0x17), chr(0x18), chr(0x19)]:
                nacklist = [False, op, chr(0x05)]
                return nacklist
            else:
                nacklist = [True, op, 0]
                print(nacklist)
                return nacklist
        elif len(msg) > 44:
            if op not in [chr(0x01),chr(0xFE),chr(0x0E), chr(0x0F), chr(0x13), chr(0x17), chr(0x18), chr(0x19)]:
                nacklist = [False, op, chr(0x05)]
                return nacklist
            elif (op in [chr(0x01),chr(0x0F), chr(0x17)]) and (len(msg) != 45):
                nacklist = [False, op, chr(0x05)]
                return nacklist
            elif (op == chr(0x17)) and (msg[44] not in [chr(0), chr(1), chr(2)]):
                x=hex(ord(msg[44]))
                nacklist = [False, op, chr(0x05)]
                return nacklist
            elif (op == chr(0x18)) and (len(msg) != 51):
                nacklist = [False, op, chr(0x05)]
                return nacklist
            else:
                nacklist = [True, op, 0]
                print(nacklist)
                return nacklist
        else:
            nacklist = [True, op, 0]
            print(nacklist)
            return nacklist


