import sys
import os
# import win32api
import datetime

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

    def length_calc(self, length):
        length_1 = length & 0xFF
        length_2 = (length >> 8) & 0xFF
        length_3 = (length >> 16) & 0xFF
        length_4 = (length >> 24) & 0xFF

        value = chr(length_4) + chr(length_3) + chr(length_2) + chr(length_1)

        return value