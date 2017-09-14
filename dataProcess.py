# coding=utf-8

import os
import sys
import xlrd
import csv
import shutil
import re
import printWrapper


class DataProcess:
    def __init__(self,pW=None):
        self.mP = pW
        self.SNMode = []
        self.SNArr = []
        self.SNDict = {}

    def readSN(self, fileName):
        del self.SNArr[:]
        data = xlrd.open_workbook(fileName)  # open an excel
        table = data.sheets()[0]  # get a sheet by index
        SNcol = table.col_values(1)
        for i, ustr in enumerate(SNcol):
            if ustr != u'' and i != 0:
                SNstr = ustr.encode('utf-8')
                # SNstr = SNstr[1:]
                self.SNArr.append(SNstr)
        self.mP.myPrint(printWrapper.SUCCESS, '读取' + str(len(self.SNArr)) + '个SN号\n')

    def addSN(self, newSN):
        for SN in self.SNArr:
            if SN == newSN:
                self.mP.myPrint(printWrapper.WARN, 'SN:' + SN + ' 已存在，请勿重复添加\n')
                return False
        self.SNArr.append(newSN)
        self.mP.myPrint(printWrapper.SUCCESS, 'SN:' + newSN + ' 已添加\n')
        return True

    def deleteSN(self, SN):
        self.SNArr.remove(SN)
        self.mP.myPrint(printWrapper.SUCCESS, 'SN:' + SN + ' 已删除\n')

    def searchReadAndCompare(self, path, mode):
        self.SNDict.clear()
        readFunc = (self.__readInT1T2, self.__readInT3)[mode == 'T3']
        self.mP.myPrintInfo({'SN个数': str(len(self.SNArr)), '文件夹路径': path, '工作模式': mode, 'text': '开始搜索！'})
        for SN in self.SNArr:
            self.mP.myPrint(text='搜索'+SN+':')
            fileList = self.__search(path, SN)
            if len(fileList) == 0:
                self.mP.myPrint(text='找不到匹配的文件')
                self.SNDict[SN] = ['0','Null','Null','Null']
                continue
            fileDict = {}
            passInfoRowIdx = (6,7)[SN[0] == 'H']
            for file in fileList:
                t, info = readFunc(file, passInfoRowIdx=passInfoRowIdx)
                self.mP.myPrint(text=self.__getFileNameFromRoad(file)+' | '+t+' | '+info)
                fileDict[t] = [file, info]
                sortedTime = sorted(fileDict.keys(), cmp=self.__compareTime, reverse=False)
                self.SNDict[SN] = [str(len(fileList)),
                                   sortedTime[0],
                                   fileDict[sortedTime[0]][1],
                                   self.__getFileNameFromRoad(fileDict[sortedTime[0]][0])]
            self.mP.myPrint(text='')
        self.mP.myPrint(text='\n搜索完成')

    def __search(self, path, word):
        fileList = []
        word = word[1:]
        for filename in os.listdir(path):
            fp = os.path.join(path, filename)
            if os.path.isfile(fp) and word in filename:
                fileList.append(fp)
            elif os.path.isdir(fp):
                self.__search(fp, word)
        return fileList

    def __readInT3(self, file, passInfoRowIdx, timeRowIdx=1):
        passInfo = ''
        Time = ''
        with open(file, 'rb') as f:
            reader = csv.reader((line.replace('\0', '') for line in f))
            for i, row in enumerate(reader):
                if i == timeRowIdx:
                    Time = row[1]
                if i == passInfoRowIdx:
                    passInfo = row[1]
                    break
            return Time, passInfo

    def __readInT1T2(self, file, passInfoRowIdx=1, timeRowIdx=1):  # todo
        passInfo = 'PASS'
        Time = ''
        with open(file, 'rb') as f:
            reader = csv.reader((line.replace('\0', '') for line in f))
            for i, row in enumerate(reader):
                if i == timeRowIdx:
                    Time = row[3]
                    break
        return Time, passInfo

    def __timeStrToInt(self, str):
        is12Style = (str[-2:] == 'PM' or str[-2:] == 'AM')
        temp = (re.findall(r'(.+)/(.+)/(.+) (.+):(.+):(.+)', str),
                re.findall(r'(.+)/(.+)/(.+) (.+):(.+):(.+) (.+)', str))[is12Style]
        if len(temp) == 0:
            self.mP.myPrint(printWrapper.ERROR,'时间格式不对或者工作模式不匹配')
            return
        Arr = []
        for i, str in enumerate(temp[0]):
            if i == 6:
                if str == 'PM':
                    Arr[3] += 12
                break
            number = int(str)
            Arr.append(number)
        return [Arr[2], Arr[0], Arr[1], Arr[3], Arr[4], Arr[5]]

    def __compareTime(self, time1, time2):
        t1 = self.__timeStrToInt(time1)
        t2 = self.__timeStrToInt(time2)
        for i in range(6):
            if (t1[i] > t2[i]):
                return -1
            elif (t1[i] < t2[i]):
                return 1
        return 0

    def __getFileNameFromRoad(self, road):
        l = len(road)
        idx = 0
        for i in range(l - 1, 0, -1):
            if road[i] == '\\':
                idx = i
                break
        return road[(idx + 1):l]