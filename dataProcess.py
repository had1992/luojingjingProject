# coding=utf-8

import os
import sys
import xlrd
import csv
import shutil
import re

class DataProcess:
    def __init__(self):
        self.SNArr = []
        self.SNDict = {}

    def readSN(self, fileName):
        data = xlrd.open_workbook(fileName)  # open an excel
        table = data.sheets()[0]  # get a sheet by index
        SNcol = table.col_values(1)
        for i, ustr in enumerate(SNcol):
            if ustr != u'' and i != 0:
                SNstr = ustr.encode('utf-8')
                SNstr = SNstr[1:]
                self.SNArr.append(SNstr)

    def searchReadAndCompare(self, path, mode):
        readFunc = (self.__readInT3, self.__readInT1T2)[mode == 'T3']
        for SN in self.SNArr:
            fileList = self.__search(path, SN)
            if len(fileList) == 0:
                self.SNDict[SN] = ['0', 'Null', 'Null', 'Null']
                continue
            fileDict = {}
            for file in fileList:
                t, info = readFunc(file)
                fileDict[t] = [file, info]
            sortedTime = sorted(fileDict.keys(), cmp=self.__compareTime)
            self.SNDict[SN] = [str(len(fileList)),
                               sortedTime[0],
                               fileDict[sortedTime[0]][1],
                               self.__getFileNameFromRoad(fileDict[sortedTime[0]][0])]


    def __search(self, path, word):
        fileList = []
        for filename in os.listdir(path):
            fp = os.path.join(path, filename)
            if os.path.isfile(fp) and word in filename:
                fileList.append(fp)
            elif os.path.isdir(fp):
                self.__search(fp, word)
        return fileList

    def __readInT3(self, file):
        passInfo = ''
        Time = ''
        with open(file, 'rb') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 1:
                    Time = row[1]
                if i == 7:
                    passInfo = row[1]
                    break
        return Time, passInfo

    def __readInT1T2(self, file):#todo
        passInfo = 'PASS'
        Time = ''
        with open(file, 'rb') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 1:
                    Time = row[1]
                    break
        return Time, passInfo

    def __timeStrToInt(self, str):
        temp = re.findall(r'(.+)/(.+)/(.+) (.+):(.+):(.+) (.+)', str)
        Arr = []
        for i, str in enumerate(temp[0]):
            if i == 6 and str == 'PM':
                Arr[3] += 12
                break
            number = int(str)
            Arr.append(number)
        return [Arr[2], Arr[0], Arr[1], Arr[3], Arr[4], Arr[5]]

    def __compareTime(self, time1, time2):
        t1 = self.__timeStrToInt(time1)
        t2 = self.__timeStrToInt(time2)
        for i in range(6):
            if t1[i] > t2[i]:
                return True
            elif t1[i] < t2[i]:
                return False
        return True

    def __getFileNameFromRoad(self, road):
        l = len(road)
        idx = 0
        for i in range(l - 1, 0, -1):
            if road[i] == '/':
                idx = i
                break
        return road[(idx + 1):l]

#
#
#

#
# if __name__ == '__main__':
#
# 	SN_FILE_ROAD = '/Users/had/Desktop/xxx.xlsx' #SN file road
# 	TEST_FILE_DIR_ROAD = '/Users/had/Desktop'    #test file dir road
# 	COPY_TO_DIR_ROAD = '/Users/had/Desktop/Test'
#
# 	if not os.path.exists(COPY_TO_DIR_ROAD):
# 		os.mkdir(COPY_TO_DIR_ROAD)
# 	else:
# 		shutil.rmtree(COPY_TO_DIR_ROAD)
# 		os.mkdir(COPY_TO_DIR_ROAD)
# 	print 'create dir success\n'
#
# 	ALL_SN = readSN(SN_FILE_ROAD)
# 	print ALL_SN
# 	print 'S/N read Ok\n'
#
# 	for SN in ALL_SN:
# 		testFileDict = {}
# 		files = search(TEST_FILE_DIR_ROAD, SN)
# 		for file in files:
# 			time,info = readTestFile(file)
# 			print 'S/N:'+'H'+SN+'|time:'+time+'|result:'+info
# 			if info == 'PASS':
# 				testFileDict[time] = file
# 		if len(testFileDict):
# 			x = sorted(testFileDict.keys(),cmp = compareTime)
# 			print 'From S/N:'+'H'+SN+', choose time:'+x[0]+''
# 			readyToCopyFileName = testFileDict[x[0]]
# 			shutil.copy(readyToCopyFileName,COPY_TO_DIR_ROAD+'/'+getFileNameFromRoad(readyToCopyFileName))
# 			print 'copy success\n'












