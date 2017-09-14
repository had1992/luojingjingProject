# coding=utf-8

from window import *
from dataProcess import *
import Tkinter
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':

    root = Tkinter.Tk()
    root.title('测试文件搜索工具v1.0')

    pW = printWrapper.PrintWrapper()
    dP = DataProcess(pW)
    w = Window(root, dP)

    root.mainloop()
    pass
