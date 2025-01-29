import time
from enum import Enum
class Month(Enum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

class Day(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

class HolidayDates():
    TYPE_START = 0
    TYPE_CUSTOM = 0
    TYPE_YEARLY = 1
    TYPE_MONTHLY = 2
    TYPE_WEEKLY = 3
    TYPE_DAILY = 4
    TYPE_COUNT = 5

    def __init__(self, dateType, dateList):
        self.dateType = dateType
        self.numDates = len(dateList) / 2
        self.startDates = []
        self.endDates = []
        for i in range(0, len(dateList), 2):
            self.startDates.append(dateList[i])
            self.endDates.append(dateList[i + 1])

    def getStartTime(self, index, date=None):
        dateTuple = self.startDates[index]
        return self.getTime(dateTuple, date)

    def getAdjustedStartTime(self, index, date=None):
        dateTuple = self.startDates[index]
        return self.getAdjustedTime(dateTuple, date)

    def getEndTime(self, index, date=None):
        dateTuple = self.endDates[index]
        return self.getTime(dateTuple, date)

    def getAdjustedEndTime(self, index, date=None):
        dateTuple = self.endDates[index]
        return self.getAdjustedTime(dateTuple, date)

    def getCurrentDate(self):
        localtime = time.localtime()
        date = (localtime[0], localtime[1], localtime[2], localtime[6])
        return date

    def getTime(self, t, date=None):
        if not date:
            date = self.getCurrentDate()
        if self.dateType == HolidayDates.TYPE_CUSTOM:
            return time.mktime((t[0], t[1], t[2], t[3], t[4], t[5], 0, 0, -1))
        if self.dateType == HolidayDates.TYPE_YEARLY:
            return time.mktime((date[0], t[0], t[1], t[2], t[3], t[4], 0, 0, -1))
        if self.dateType == HolidayDates.TYPE_MONTHLY:
            return time.mktime((date[0], date[1], t[0], t[1], t[2], t[3], 0, 0, -1))
        if self.dateType == HolidayDates.TYPE_WEEKLY:
            cWDay = date[3]
            sWDay = t[0]
            dayOffset = sWDay - cWDay
            day = date[2] + dayOffset
            return time.mktime((date[0], date[1], day, t[1], t[2], t[3], 0, 0, -1))
        if self.dateType == HolidayDates.TYPE_DAILY:
            return time.mktime((date[0], date[1], date[2], t[0], t[1], t[2], 0, 0, -1))

    def getAdjustedTime(self, t, date=None):
        if not date:
            date = self.getCurrentDate()
        if self.dateType == HolidayDates.TYPE_CUSTOM:
            return time.mktime((t[0], t[1], t[2], t[3], t[4], t[5], 0, 0, -1))
        if self.dateType == HolidayDates.TYPE_YEARLY:
            return time.mktime((date[0] + 1, t[0], t[1], t[2], t[3], t[4], 0, 0, -1))
        if self.dateType == HolidayDates.TYPE_MONTHLY:
            return time.mktime((date[0], date[1] + 1, t[0], t[1], t[2], t[3], 0, 0, -1))
        if self.dateType == HolidayDates.TYPE_WEEKLY:
            cWDay = date[3]
            sWDay = t[0]
            dayOffset = sWDay - cWDay
            day = date[2] + dayOffset
            return time.mktime((date[0], date[1], day + 7, t[1], t[2], t[3], 0, 0, -1))
        if self.dateType == HolidayDates.TYPE_DAILY:
            return time.mktime((date[0], date[1], date[2] + 1, t[0], t[1], t[2], 0, 0, -1))